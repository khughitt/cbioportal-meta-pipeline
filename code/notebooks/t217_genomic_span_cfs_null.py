"""t217 — genomic-span / common-fragile-site null test for neural-gene mutation enrichment.

Question: q032 (neural-gene length null) / hypothesis h12-neural-gene-enrichment-length-histology-artifact.
Plan: doc/plans/2026-06-06-neural-gene-enrichment-meta-analysis-plan.md (step 3, t217 — P1 primary).
Gate redirect: doc/interpretations/2026-06-08-t215-neural-gene-reproduction-gate.md (F4/F5).

The t215 gate confirmed a real high-tail enrichment of the 9 candidate "neural" genes, but redirected
the correction test: **protein-aa length is the WRONG yardstick** — the candidates are SHORT proteins
(131-397 aa, below the genome median) yet the co-top non-driver class is a LARGE genomic locus /
common-fragile-site (CFS) set. So the operative covariate is genomic / CDS span, not amino-acid length.

This script runs the two-armed normalization that the redirect demands and contrasts them:

  ARM A  mutations-per-CDS-kb     (coding-target size; CDS_bp approx (aa+1)*3 from UniProt length)
         -> does NOT dissolve the enrichment: candidates are SHORT CDS, so a coding-length null
            UNDER-corrects (their per-CDS-kb rate stays high). This is the gate's F4 made quantitative.
  ARM B  mutations-per-genomic-kb (gene-body span end-start from gene_replication_timing.feather)
         -> DOES dissolve it: candidates are top-1% genomic loci, so per-genomic-kb deflates them.

Plus three confirmatory arms:
  - Wilcoxon of candidate genomic span vs background (one-sided greater) — the positive confound.
  - dndscv min_qglobal per candidate — are any under positive selection? (Expect: none.)
  - Span-matched empirical null — draw size/late-replication-matched random gene sets and ask whether
    the candidate set's RAW-count enrichment is exceptional vs random large loci. (Expect: it is not.)

CFS is operationalized two ways, both in-repo (no new download): the constitutively-late-replication
label (`rt_constitutive_label == 'CL'`, `rt_cl_fraction`) from data/gene_replication_timing.feather,
and a small curated canonical-CFS gene list for cross-validation/labeling only.

Reported on `full` AND `pan-cancer` (tail-sensitivity / q016 panel-ascertainment coupling), per the
gate's corrected F3. random_seed=0 (reproducibility covenant).

Run:  uv run --frozen python code/notebooks/t217_genomic_span_cfs_null.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

# --- candidate set (FAM19A2 is the pipeline symbol; TAFA2 is the HGNC primary) ---
CANDIDATES = [
    "NKAIN2",
    "KCNIP4",
    "FAM19A2",
    "RIT2",
    "CALN1",
    "RBFOX1",
    "LSAMP",
    "SGCZ",
    "OPCML",
]
# canonical neural EFFECTORS (positive control: bona-fide cancer-neuroscience genes, mostly LONG proteins)
EFFECTORS = [
    "NLGN3",
    "ADRB2",
    "NTRK1",
    "NTRK2",
    "CHRM3",
    "GRIN2A",
    "GRIN2B",
    "NGF",
    "BDNF",
]
CANDIDATE_ALIASES = {"FAM19A2": "TAFA2"}

# Curated canonical common-fragile-site host genes (large, late-replicating; literature-recurrent across
# Le Tallec 2013 / Wilson 2015 / Glover 2017 CFS reviews). Used for cross-validation/labeling ONLY; the
# workhorse CFS operationalization is the constitutive-late-replication label in the rep-timing feather.
CANONICAL_CFS = {
    "FHIT",
    "WWOX",
    "PRKN",
    "PARK2",
    "MACROD2",
    "DLG2",
    "NBEA",
    "GRID2",
    "CCSER1",
    "LRP1B",
    "CTNNA3",
    "DAB1",
    "IMMP2L",
    "RBFOX1",
    "A2BP1",
    "NAALADL2",
    "PDE4D",
    "CNTNAP2",
    "DMD",
    "FHIT",
    "GMDS",
    "LSAMP",
    "CSMD1",
    "EYS",
    "PCDH15",
    "MAGI2",
    "AGBL4",
    "DPP10",
    "ROBO2",
}

META = ["cancer_type", "symbol"]
_NONSTUDY_EXACT = {"mean", "mean_adj"}
_NONSTUDY_PREFIXES = ("mean_", "n_", "callable_")

CONFIGS = {
    "full": "/data/packages/cbioportal/full/summary/mut/table",
    "pan-cancer": "/data/packages/cbioportal/pan-cancer/summary/mut/table",
}
REPTIMING = Path("data/gene_replication_timing.feather")
UNIPROT = Path("data/uniprotkb_hsapiens_protein_lengths.tsv.gz")
DNDSCV = Path(
    "/data/packages/cbioportal/pan-cancer/summary/mut/table/dndscv_pooled.feather"
)
OUT = Path("results/neural-gene-span-null-2026-06-08")

RANDOM_SEED = 0
N_NULL = 5000  # span-matched null draws
TOPN_OCC = 100  # top-N occupancy for the enrichment hypergeometric


def study_columns(df: pd.DataFrame) -> list[str]:
    """Inclusive per-study columns only — drop meta, pooled summaries, `_exclusive` twins, metadata."""
    out = []
    for c in df.columns:
        if c in META or c in _NONSTUDY_EXACT or c.endswith("_exclusive"):
            continue
        if c.startswith(_NONSTUDY_PREFIXES):
            continue
        out.append(c)
    return out


def load_driver_symbols() -> set[str]:
    bailey = set(
        pd.read_csv("data/bailey2018_table_s1.tsv", sep="\t")["Gene"]
        .dropna()
        .astype(str)
    )
    cgc = set(
        pd.read_csv("data/cosmic_cgc.tsv", sep="\t")["Gene Symbol"].dropna().astype(str)
    )
    return {g.strip() for g in (bailey | cgc)}


def load_protein_cds_kb() -> dict[str, float]:
    """Synonym-aware coding-target size in kb: CDS_bp approx (aa+1)*3 incl. stop codon.

    UniProt 'Gene Names' is space-separated synonyms; map every synonym to the max coding length so a
    gene carried under any alias resolves. This is the ARM-A denominator (coding target, the classic
    length confound) — deliberately a proxy; the point is that it is SMALL for the candidates.
    """
    u = pd.read_csv(UNIPROT, sep="\t").dropna(subset=["Gene Names", "Length"])
    cds_kb: dict[str, float] = {}
    for names, aa in zip(u["Gene Names"].astype(str).str.split(), u["Length"]):
        kb = (float(aa) + 1.0) * 3.0 / 1000.0
        for t in names:
            if kb > cds_kb.get(t, 0.0):
                cds_kb[t] = kb
    return cds_kb


def per_gene_count(count_path: Path) -> tuple[pd.Series, int]:
    """Per-gene total mutation count summed over inclusive study columns. Returns (series, n_studies)."""
    cnt = pd.read_feather(count_path)
    cols = study_columns(cnt)
    total = cnt.groupby("symbol")[cols].sum(min_count=1).sum(axis=1)
    return total, len(cols)


def load_span() -> pd.DataFrame:
    """Per-gene genomic span (bp) + replication-timing CFS proxy from the in-repo feather."""
    rt = pd.read_feather(REPTIMING)
    rt = rt[rt["biotype"] == "protein_coding"].copy()
    rt["span_bp"] = (rt["end"] - rt["start"]).astype(float)
    rt = rt.dropna(subset=["symbol", "span_bp"])
    rt = rt[rt["span_bp"] > 0]
    # one row per symbol (largest span if a symbol maps to several loci)
    rt = rt.sort_values("span_bp", ascending=False).drop_duplicates("symbol")
    rt["is_late_cl"] = rt["rt_constitutive_label"].eq("CL")
    return rt.set_index("symbol")[
        ["span_bp", "rt_cl_fraction", "rt_constitutive_label", "is_late_cl"]
    ]


def enrichment(metric: pd.Series, gene_set: list[str], topn: int = TOPN_OCC) -> dict:
    """One-sided MWU (set ranks higher than rest) + median percentile + top-N hypergeometric."""
    s = metric.dropna()
    present = [g for g in gene_set if g in s.index]
    if not present:
        return {
            "n_in_set": 0,
            "median_pct": np.nan,
            "mwu_p_greater": np.nan,
            "n_in_topN": 0,
            "exp_in_topN": np.nan,
            "hypergeom_topN_p": np.nan,
        }
    in_set = s.index.isin(present)
    _u, p = stats.mannwhitneyu(
        s[in_set].to_numpy(), s[~in_set].to_numpy(), alternative="greater"
    )
    rk = s.rank(ascending=False, method="min")
    median_pct = float(100.0 * rk[present].median() / len(s))
    topN = int((rk[present] <= topn).sum())
    return {
        "n_in_set": len(present),
        "median_pct": round(median_pct, 3),
        "mwu_p_greater": float(p),
        "n_in_topN": topN,
        "exp_in_topN": round(len(present) * topn / len(s), 3),
        "hypergeom_topN_p": float(
            stats.hypergeom.sf(topN - 1, len(s), topn, len(present))
        ),
    }


def span_matched_null(
    metric: pd.Series, span: pd.Series, present: list[str], rng, n: int, knn: int = 200
) -> dict:
    """Empirical p: is the candidate set's median raw-count percentile exceptional vs random gene sets
    TIGHTLY matched on genomic span?

    Decile matching is too coarse at the extreme tail (the candidates sit at the very top of the top
    decile, so a decile pool is mostly smaller genes). Instead, for each candidate we take its ``knn``
    nearest genes by |Δlog10(span)| (excluding the candidates themselves) and draw one per candidate.
    This controls span to a caliper we also report (median |Δlog10 span| over the matched pools), so the
    residual — if any — cannot be a coarse-binning artifact.

    Interpretation:
      * ``null_median_pct_mean`` is the "random gene of the same size" baseline — how high a typical
        span-matched locus already sits by raw mutation count (quantifies how much span ALONE explains).
      * ``empirical_p_le_observed`` = P(matched random set ranks at least as high as the candidates).
        Large p  -> span fully accounts for the enrichment.  Small p -> a residual remains above span.
    """
    common = metric.dropna().index.intersection(span.dropna().index)
    m = metric.loc[common]
    logsp = np.log10(span.loc[common].astype(float))
    rk = m.rank(ascending=False, method="min")
    pct = 100.0 * rk / len(m)
    pres = [g for g in present if g in common]
    obs = float(pct[pres].median())

    cand_set = set(pres)
    pools: list[np.ndarray] = []
    calipers: list[float] = []
    for g in pres:
        d = (logsp - logsp[g]).abs()
        d = d.drop(
            index=[x for x in cand_set if x in d.index]
        )  # exclude candidates from the pool
        nn = d.nsmallest(knn)
        pools.append(nn.index.to_numpy())
        calipers.append(
            float(nn.max())
        )  # widest log10-span gap admitted for this candidate

    draws = np.empty(n)
    for i in range(n):
        picks = [rng.choice(pool) for pool in pools]
        draws[i] = float(np.median(pct.loc[picks]))
    emp_p = float((draws <= obs).mean())
    return {
        "n_matched": len(pres),
        "knn": knn,
        "median_caliper_dlog10_span": round(float(np.median(calipers)), 4),
        "observed_median_pct": round(obs, 3),
        "null_median_pct_mean": round(float(draws.mean()), 3),
        "null_median_pct_p05": round(float(np.percentile(draws, 5)), 3),
        "empirical_p_le_observed": emp_p,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(RANDOM_SEED)
    drivers = load_driver_symbols()
    cds_kb = load_protein_cds_kb()
    span = load_span()
    dnds = pd.read_feather(DNDSCV).set_index("symbol")

    span_kb = span["span_bp"] / 1000.0
    cds_series = pd.Series(cds_kb)

    enrich_rows: list[dict] = []
    null_rows: list[dict] = []
    contrast_rows: list[dict] = []
    per_gene_frames: list[pd.DataFrame] = []
    study_counts: dict[str, int] = {}

    for cfg, base in CONFIGS.items():
        cpath = Path(base) / "gene_cancer_study.feather"
        if not cpath.exists():
            print(f"[skip] {cfg}: {cpath} absent")
            continue
        print(f"[{cfg}] loading counts ...")
        total, n_studies = per_gene_count(cpath)
        study_counts[cfg] = n_studies

        df = pd.DataFrame({"total_count": total})
        df["cds_kb"] = cds_series.reindex(df.index)
        df["span_kb"] = span_kb.reindex(df.index)
        df["is_late_cl"] = span["is_late_cl"].reindex(df.index).fillna(False)
        df["rt_cl_fraction"] = span["rt_cl_fraction"].reindex(df.index)
        df["min_qglobal"] = dnds["min_qglobal"].reindex(df.index)
        df["is_driver"] = df.index.isin(drivers)
        df["is_canonical_cfs"] = df.index.isin(CANONICAL_CFS)
        # the two normalized rates (require positive denominators)
        df["per_cds_kb"] = df["total_count"] / df["cds_kb"].where(df["cds_kb"] > 0)
        df["per_genomic_kb"] = df["total_count"] / df["span_kb"].where(
            df["span_kb"] > 0
        )

        metric_cols = {
            "total_count": "raw count (baseline)",
            "per_cds_kb": "mutations per CDS-kb (coding-target / length null)",
            "per_genomic_kb": "mutations per genomic-kb (locus-size / CFS null)",
        }
        for col, label in metric_cols.items():
            for setname, gs in [("candidates", CANDIDATES), ("effectors", EFFECTORS)]:
                e = enrichment(df[col], gs)
                enrich_rows.append(
                    {
                        "config": cfg,
                        "metric": col,
                        "metric_label": label,
                        "gene_set": setname,
                        **e,
                    }
                )

        # span-matched empirical null on the RAW-count metric (does the candidate set beat random large loci?)
        present = [g for g in CANDIDATES if g in df.index]
        nm = span_matched_null(df["total_count"], df["span_kb"], present, rng, N_NULL)
        null_rows.append({"config": cfg, "metric": "total_count", **nm})

        # per-gene contrast rows for candidates + effectors
        ranks = {c: df[c].rank(ascending=False, method="min") for c in metric_cols}
        n_tot = {c: int(df[c].notna().sum()) for c in metric_cols}
        for g in CANDIDATES + EFFECTORS:
            if g not in df.index:
                continue
            row = {
                "config": cfg,
                "gene": g,
                "role": "candidate" if g in CANDIDATES else "effector",
                "total_count": float(df.loc[g, "total_count"])
                if pd.notna(df.loc[g, "total_count"])
                else np.nan,
                "cds_kb": float(df.loc[g, "cds_kb"])
                if pd.notna(df.loc[g, "cds_kb"])
                else np.nan,
                "span_kb": float(df.loc[g, "span_kb"])
                if pd.notna(df.loc[g, "span_kb"])
                else np.nan,
                "is_late_cl": bool(df.loc[g, "is_late_cl"]),
                "is_canonical_cfs": bool(df.loc[g, "is_canonical_cfs"]),
                "min_qglobal": float(df.loc[g, "min_qglobal"])
                if pd.notna(df.loc[g, "min_qglobal"])
                else np.nan,
            }
            for c in metric_cols:
                r = ranks[c].get(g, np.nan)
                row[f"pct_{c}"] = (
                    round(100.0 * r / n_tot[c], 3) if pd.notna(r) else np.nan
                )
            contrast_rows.append(row)

        df2 = df.reset_index().rename(columns={"index": "symbol"})
        df2.insert(0, "config", cfg)
        per_gene_frames.append(df2)

    enrich = pd.DataFrame(enrich_rows)
    nulls = pd.DataFrame(null_rows)
    contrast = pd.DataFrame(contrast_rows)
    per_gene = pd.concat(per_gene_frames, ignore_index=True)

    # Wilcoxon/MWU: candidate genomic span vs genome background (one-sided greater) — the positive confound
    span_test_rows = []
    bg_span = span["span_bp"].dropna()
    for setname, gs in [("candidates", CANDIDATES), ("effectors", EFFECTORS)]:
        present = [g for g in gs if g in bg_span.index]
        set_span = bg_span[present]
        _u, p = stats.mannwhitneyu(
            set_span.to_numpy(), bg_span.drop(present).to_numpy(), alternative="greater"
        )
        span_test_rows.append(
            {
                "gene_set": setname,
                "n": len(present),
                "median_span_kb": round(float(set_span.median() / 1000.0), 1),
                "genome_median_span_kb": round(float(bg_span.median() / 1000.0), 1),
                "median_span_pctile": round(
                    float(
                        100.0
                        * (bg_span.values[None, :] < set_span.values[:, None])
                        .mean(axis=1)
                        .mean()
                    ),
                    2,
                ),
                "mwu_span_p_greater": float(p),
            }
        )
    span_test = pd.DataFrame(span_test_rows)

    # --- write artifacts ---
    per_gene.to_feather(OUT / "gene_span_metrics.feather")
    enrich.to_csv(OUT / "enrichment_by_normalization.tsv", sep="\t", index=False)
    nulls.to_csv(OUT / "span_matched_null.tsv", sep="\t", index=False)
    contrast.to_csv(OUT / "candidate_span_length_contrast.tsv", sep="\t", index=False)
    span_test.to_csv(OUT / "span_wilcoxon.tsv", sep="\t", index=False)

    datapackage = {
        "name": "neural-gene-span-null-2026-06-08",
        "title": "t217 genomic-span / CFS null test for neural-gene mutation enrichment",
        "description": "q032 / h12. Two-armed normalization of the candidate-set mutation enrichment: "
        "per-CDS-kb (coding target, length null) vs per-genomic-kb (locus size / CFS null), plus a "
        "span-matched empirical null, a candidate-span Wilcoxon, and a dndscv positive-selection check. "
        "Shows the confound is genomic span / common-fragile-site, NOT amino-acid/CDS length.",
        "created": "2026-06-08",
        "sources": [
            {
                "name": "gene_cancer_study",
                "configs": list(CONFIGS),
                "path": "{config}/.../gene_cancer_study.feather",
            },
            {"name": "gene_replication_timing", "path": str(REPTIMING)},
            {"name": "uniprot_protein_lengths", "path": str(UNIPROT)},
            {"name": "dndscv_pooled", "path": str(DNDSCV)},
        ],
        "tasks": ["t217"],
        "related": [
            "question:q032-neural-gene-length-null",
            "hypothesis:h12-neural-gene-enrichment-length-histology-artifact",
            "interpretation:2026-06-08-t215-neural-gene-reproduction-gate",
        ],
        "resources": [
            {"name": "gene_span_metrics", "path": "gene_span_metrics.feather"},
            {
                "name": "enrichment_by_normalization",
                "path": "enrichment_by_normalization.tsv",
            },
            {"name": "span_matched_null", "path": "span_matched_null.tsv"},
            {
                "name": "candidate_span_length_contrast",
                "path": "candidate_span_length_contrast.tsv",
            },
            {"name": "span_wilcoxon", "path": "span_wilcoxon.tsv"},
        ],
        "parameters": {
            "random_seed": RANDOM_SEED,
            "n_null_draws": N_NULL,
            "topn_occupancy": TOPN_OCC,
            "candidates": CANDIDATES,
            "effectors": EFFECTORS,
            "inclusive_study_counts": study_counts,
            "cds_kb_definition": "(protein_aa + 1) * 3 / 1000 (UniProt length proxy, incl. stop codon)",
            "genomic_span_definition": "end - start from data/gene_replication_timing.feather (protein_coding)",
            "cfs_operationalization": "rt_constitutive_label == 'CL' (constitutively late-replicating) + "
            "curated canonical-CFS gene list for cross-validation",
            "note": "raw counts are not panel-callable-territory normalized; per-genomic-kb uses full "
            "gene-body span (couples to q016 panel ascertainment).",
        },
    }
    (OUT / "datapackage.json").write_text(json.dumps(datapackage, indent=2))

    # --- console summary ---
    pd.set_option("display.width", 220, "display.max_columns", 40)
    print("\n================ INCLUSIVE STUDY COLUMNS ================")
    print(f"  {study_counts}")
    print(
        "\n================ ENRICHMENT BY NORMALIZATION (candidate set) ================"
    )
    print(
        enrich[enrich.gene_set == "candidates"][
            [
                "config",
                "metric",
                "n_in_set",
                "median_pct",
                "mwu_p_greater",
                "n_in_topN",
                "hypergeom_topN_p",
            ]
        ].to_string(index=False)
    )
    print("\n  (effectors, positive control):")
    print(
        enrich[enrich.gene_set == "effectors"][
            ["config", "metric", "median_pct", "mwu_p_greater", "n_in_topN"]
        ].to_string(index=False)
    )
    print(
        "\n================ CANDIDATE SPAN vs PROTEIN/CDS LENGTH (the 'wrong yardstick') ================"
    )
    print(span_test.to_string(index=False))
    print(
        "\n================ SPAN-MATCHED EMPIRICAL NULL (raw count, kNN log-span) ================"
    )
    print(
        "  null_median_pct_mean = how high a random same-size locus already sits (span's share);\n"
        "  empirical_p large => span fully explains it;  small => a residual remains above span."
    )
    print(nulls.to_string(index=False))
    print(
        "\n================ dndscv POSITIVE-SELECTION CHECK (candidates) ================"
    )
    cc = contrast[(contrast.config == "full") & (contrast.role == "candidate")]
    print(
        cc[
            [
                "gene",
                "total_count",
                "cds_kb",
                "span_kb",
                "is_late_cl",
                "is_canonical_cfs",
                "min_qglobal",
                "pct_total_count",
                "pct_per_cds_kb",
                "pct_per_genomic_kb",
            ]
        ].to_string(index=False)
    )
    print(f"\nArtifacts written to {OUT}/")


if __name__ == "__main__":
    main()
