# science:code
# status: workflow-owned
# science:end
"""
build_expression_nmf_modules.py

Derive the frozen NMF expression-module covariate set for one h08 positive-control arm
stratum (`pre-registration:h08-positive-control`, § Total Comparison Count, as clarified by
Amendment 001). Implements the locked rule EXACTLY:

  - substrate: per-study cBioPortal PanCanAtlas RNA-seq (`data_mrna_seq_v2_rsem.txt`),
    restricted to the MC3-overlapping samples for this arm;
  - transform: log2(RSEM_V2 + 1);
  - gene filter: drop genes expressed (> 0) in < 10% of samples, then retain the top 2,000
    genes by median-absolute-deviation (MAD);
  - K selection: NMF for K in {5, 10, ..., 50} with 50 random restarts each; cophenetic
    correlation (Brunet et al. 2004) of the per-K sample consensus matrix; choose the LARGEST
    K before the cophenetic coefficient drops below 0.90 (ties broken toward the smaller K).

LEAKAGE FIREWALL (pre-reg invariant): this script reads only (a) the expression matrix and
(b) MC3 *sample identity* (`tcga_mc3` samples.feather: sample_id + cancer_type, to enumerate
which barcodes belong to the arm). It NEVER reads signature exposures `H`, mutation calls, or
any covariate — so K cannot be tuned against the association gate. The selected K and the
per-K cophenetic curve are written before any covariate<->signature rank is computed.

Outputs (per arm):
  - nmf_gene_modules.feather      gene x module loadings (H), at the selected K
  - nmf_sample_loadings.feather   sample x module scores (W), at the selected K — the covariates
  - cophenetic_curve.feather      K, cophenetic_corr, dispersion (the selection record)
  - module_selection.json         selected_K + realized n + filter sizes + provenance
"""

import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from scipy.cluster.hierarchy import cophenet, linkage
from scipy.spatial.distance import squareform
from sklearn.decomposition import NMF
from threadpoolctl import threadpool_limits

logger = logging.getLogger(__name__)
if not logging.getLogger().handlers:
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s %(name)s: %(message)s"
    )

K_GRID = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
COPHENETIC_THRESHOLD = 0.90
N_RESTARTS = 50
MIN_EXPRESSED_FRAC = 0.10
TOP_MAD_GENES = 2000


def barcode15(s: pd.Series) -> pd.Series:
    """TCGA sample-level barcode (patient + sample-type, 15 chars) for the MC3<->RNA join."""
    return s.astype(str).str.slice(0, 15)


def load_rsem_matrix(path: Path) -> pd.DataFrame:
    """Load a cBioPortal RSEM matrix as genes x samples (Hugo_Symbol index, numeric values)."""
    df = pd.read_csv(path, sep="\t", dtype={"Hugo_Symbol": str})
    df = df.drop(columns=[c for c in ("Entrez_Gene_Id",) if c in df.columns])
    df = df[df["Hugo_Symbol"].notna() & (df["Hugo_Symbol"] != "")]
    # collapse duplicate gene symbols by max expression (cBioPortal occasionally repeats Hugo)
    df = df.groupby("Hugo_Symbol", sort=False).max(numeric_only=True)
    # columns are sample barcodes; coerce to numeric, drop all-NaN sample columns
    df = df.apply(pd.to_numeric, errors="coerce")
    return df


def filter_genes(expr: pd.DataFrame) -> pd.DataFrame:
    """Drop genes expressed in < 10% of samples, then keep the top-2000 MAD genes.

    `expr` is genes x samples on the raw RSEM scale (filtering is unit-agnostic for the
    >0 expressed test; MAD is computed on the log2(RSEM+1) scale to match the NMF input).
    """
    n_samples = expr.shape[1]
    expressed_frac = (expr > 0).sum(axis=1) / n_samples
    expr = expr.loc[expressed_frac >= MIN_EXPRESSED_FRAC]
    logged = np.log2(expr + 1.0)
    mad = (logged.sub(logged.median(axis=1), axis=0)).abs().median(axis=1)
    top = mad.sort_values(ascending=False).head(TOP_MAD_GENES).index
    return logged.loc[top]


def _restart_labels(x: np.ndarray, k: int, random_state: int) -> np.ndarray:
    """One NMF restart -> per-sample hard cluster assignment (argmax over components of W).

    Pinned to a single BLAS thread: the restarts are parallelised across processes, so each
    worker must stay single-threaded or the box is oversubscribed (n_jobs x BLAS-threads).
    """
    with threadpool_limits(limits=1):
        model = NMF(
            n_components=k,
            init="random",
            solver="cd",
            max_iter=500,
            random_state=random_state,
        )
        return model.fit_transform(x).argmax(axis=1)


def consensus_cophenetic(
    x: np.ndarray, k: int, base_seed: int, n_jobs: int
) -> tuple[float, float, np.ndarray]:
    """Brunet 2004 consensus + cophenetic correlation for one K.

    `x` is samples x genes (non-negative). Runs N_RESTARTS NMF fits with distinct random
    initialisations (deterministic per-restart seeds, so parallelism does not change the
    result), assigns each sample to argmax(W) cluster, accumulates the sample x sample
    connectivity matrix, and returns (cophenetic_corr, dispersion, consensus_matrix).
    """
    n = x.shape[0]
    all_labels = Parallel(n_jobs=n_jobs, prefer="processes")(
        delayed(_restart_labels)(x, k, base_seed + r) for r in range(N_RESTARTS)
    )
    consensus = np.zeros((n, n), dtype=float)
    for labels in all_labels:
        consensus += (labels[:, None] == labels[None, :]).astype(float)
    consensus /= N_RESTARTS

    # dispersion (Kim & Park 2007): 1.0 for a perfectly bimodal {0,1} consensus
    dispersion = float(np.sum(4.0 * (consensus - 0.5) ** 2) / (n * n))

    # cophenetic correlation of the consensus, via average-linkage on the consensus distance
    dist = 1.0 - consensus
    np.fill_diagonal(dist, 0.0)
    condensed = squareform(dist, checks=False)
    z = linkage(condensed, method="average")
    coph_corr, _ = cophenet(z, condensed)
    return float(coph_corr), dispersion, consensus


def select_k(curve: pd.DataFrame) -> int:
    """Largest K before cophenetic drops below 0.90; ties broken toward the smaller K.

    If every K clears the threshold, the largest K wins. If none clears it, the smallest K
    is chosen (loudly logged) so the pipeline produces a module set rather than failing.
    """
    passing = curve.loc[curve["cophenetic_corr"] >= COPHENETIC_THRESHOLD, "k"]
    if passing.empty:
        chosen = int(curve["k"].min())
        logger.warning(
            "no K reaches cophenetic >= %.2f; falling back to smallest K=%d (loud missingness)",
            COPHENETIC_THRESHOLD,
            chosen,
        )
        return chosen
    # "largest K before the coefficient drops below 0.90": the largest K in the leading
    # contiguous passing run starting at the smallest K.
    ks = sorted(curve["k"].tolist())
    leading = []
    pass_set = set(passing.tolist())
    for k in ks:
        if k in pass_set:
            leading.append(k)
        else:
            break
    return int(max(leading)) if leading else int(min(pass_set))


def main() -> None:
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821
    arm = str(snek.params.arm)
    base_seed = int(snek.config.get("random_seed", 0))
    n_jobs = int(snek.config.get("nmf_n_jobs", 12))

    rsem_path = Path(snek.input["rsem"])
    mc3_samples_path = Path(snek.input["mc3_samples"])

    modules_out = Path(snek.output["modules"])
    loadings_out = Path(snek.output["loadings"])
    curve_out = Path(snek.output["cophenetic"])
    selection_out = Path(snek.output["selection"])
    modules_out.parent.mkdir(parents=True, exist_ok=True)

    # --- arm membership from MC3 sample IDENTITY only (firewall: no exposures/mutations) ---
    mc3 = pd.read_feather(mc3_samples_path)
    arm_barcodes = set(barcode15(mc3.loc[mc3["cancer_type"] == arm, "sample_id"]))
    if not arm_barcodes:
        raise ValueError(
            f"build_expression_nmf_modules ({arm}): no MC3 samples for this arm"
        )

    expr = load_rsem_matrix(rsem_path)  # genes x samples
    rsem_by15: dict[str, str] = {}
    for col in expr.columns:
        rsem_by15.setdefault(
            col[:15], col
        )  # first column wins on duplicate sample-type collisions
    shared = sorted(arm_barcodes & set(rsem_by15))
    n_mc3, n_rsem, n_shared = len(arm_barcodes), len(rsem_by15), len(shared)
    logger.info(
        "%s: MC3 arm n=%d, RSEM samples=%d, intersection=%d",
        arm,
        n_mc3,
        n_rsem,
        n_shared,
    )
    if n_shared < max(K_GRID):
        raise ValueError(
            f"build_expression_nmf_modules ({arm}): intersection n={n_shared} < max K "
            f"{max(K_GRID)} — NMF rank selection is ill-posed"
        )

    expr = expr[[rsem_by15[b] for b in shared]]
    expr.columns = shared
    logged = filter_genes(expr)  # genes x samples, log2(RSEM+1)
    n_genes = logged.shape[0]
    logger.info(
        "%s: %d genes retained after <10%%-expressed + top-%d MAD",
        arm,
        n_genes,
        TOP_MAD_GENES,
    )

    x = logged.to_numpy().T  # samples x genes (non-negative)

    rows = []
    for k in K_GRID:
        coph, disp, _ = consensus_cophenetic(x, k, base_seed, n_jobs)
        rows.append({"arm": arm, "k": k, "cophenetic_corr": coph, "dispersion": disp})
        logger.info("%s: K=%2d cophenetic=%.4f dispersion=%.4f", arm, k, coph, disp)
    curve = pd.DataFrame(rows)
    chosen_k = select_k(curve)
    logger.info("%s: selected K=%d", arm, chosen_k)

    # final factorization at the selected K (deterministic: base_seed)
    final = NMF(
        n_components=chosen_k,
        init="random",
        solver="cd",
        max_iter=600,
        random_state=base_seed,
    )
    w = final.fit_transform(x)  # samples x K
    h = final.components_  # K x genes
    module_cols = [f"module_{i + 1:02d}" for i in range(chosen_k)]

    gene_modules = pd.DataFrame(h.T, index=logged.index, columns=module_cols)
    gene_modules.insert(0, "gene", gene_modules.index)
    gene_modules.reset_index(drop=True).to_feather(modules_out)

    sample_loadings = pd.DataFrame(w, index=shared, columns=module_cols)
    sample_loadings.insert(0, "sample_id", sample_loadings.index)
    sample_loadings.reset_index(drop=True).to_feather(loadings_out)

    curve.to_feather(curve_out)

    selection = {
        "arm": arm,
        "selected_k": chosen_k,
        "cophenetic_threshold": COPHENETIC_THRESHOLD,
        "k_grid": K_GRID,
        "n_restarts": N_RESTARTS,
        "random_seed": base_seed,
        "substrate": str(rsem_path),
        "unit": "log2(RSEM_V2 + 1)",
        "amendment": "pre-registration:h08-positive-control amendment-001",
        "n_mc3_arm_samples": n_mc3,
        "n_rsem_samples": n_rsem,
        "n_intersection": n_shared,
        "n_genes_after_filter": int(n_genes),
        "min_expressed_frac": MIN_EXPRESSED_FRAC,
        "top_mad_genes": TOP_MAD_GENES,
        "reconstruction_err_at_selected_k": float(final.reconstruction_err_),
        "cophenetic_at_selected_k": float(
            curve.loc[curve["k"] == chosen_k, "cophenetic_corr"].iloc[0]
        ),
    }
    selection_out.write_text(json.dumps(selection, indent=2))


if __name__ == "__main__":
    main()
