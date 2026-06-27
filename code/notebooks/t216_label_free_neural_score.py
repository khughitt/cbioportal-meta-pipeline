# science:code
# status: exploratory
# science:end
"""t216 — label-free neural-enrichment gene score from the GTEx expression atlas.

Question: q035 (label-free neural-gene definition) / hypothesis h12-neural-gene-enrichment-length-
histology-artifact. Plan: doc/plans/2026-06-06-neural-gene-enrichment-meta-analysis-plan.md (step 2).
Gate redirect: doc/interpretations/2026-06-08-t215-neural-gene-reproduction-gate.md (benchmark the
score against a SIZE-MATCHED large-locus / CFS null, not only housekeeping negatives).

Goal: replace the hand-labelled 9-gene candidate list with a reproducible, data-driven per-gene neural-
enrichment score so the downstream enrichment statistic does not depend on human/AI labels (q035). No
GO terms are used (GO is reserved as a sensitivity comparator elsewhere).

Score (per gene, from GTEx median TPM over 53 tissues):
  neural_score = log2( (mean TPM over neural tissues + 1) / (mean TPM over non-neural tissues + 1) )
with the Cortese-2020 sub-partition:
  cns_score            -> 12 brain regions
  pns_score            -> tibial nerve
  neuroendocrine_score -> pituitary + adrenal gland
plus tau (Yanai 2005 tissue-specificity index) as a generic specificity covariate.

Validation:
  * Positive control: canonical cancer-neuroscience effectors should score high.
  * Easy negative:    housekeeping genes should score low  -> AUC(effectors vs housekeeping).
  * HARD negative (the redirect): a genomic-span-matched large-locus / CFS control set. Many large CFS
    genes are themselves brain-expressed (CSMD1, CNTNAP2, DLG2 ...), so a neural-expression score may
    NOT separate bona-fide neural cancer genes from incidental large brain loci. AUC(effectors vs
    CFS-matched) near 0.5 would mean the score cannot rescue the candidate enrichment from the size
    confound (t217). random_seed = 0.

HPA tissue-specificity (plan's secondary atlas) is NOT available locally and is left as a deferred
sensitivity layer — flagged loudly here rather than silently skipped.

Output: results/neural-gene-label-free-2026-06-08/gene_neural_enrichment.feather (reusable covariate).

Run:  uv run --frozen python code/notebooks/t216_label_free_neural_score.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

RAW_ROOT = Path("/") / "data" / "raw"
GTEX = RAW_ROOT / "expression-atlas/gtex/E-GTEX-8-query-results.tpms.tsv"
REPTIMING = Path("data/gene_replication_timing.feather")
OUT = Path("results/neural-gene-label-free-2026-06-08")
RANDOM_SEED = 0
N_MATCH_DRAWS = 2000

CNS_TISSUES = [
    "amygdala",
    "anterior cingulate cortex",
    "caudate nucleus",
    "cerebellar hemisphere",
    "cerebellum",
    "cerebral cortex",
    "frontal cortex",
    "hippocampus",
    "hypothalamus",
    "nucleus accumbens",
    "putamen",
    "substantia nigra",
]
PNS_TISSUES = ["tibial nerve"]
NEUROENDOCRINE_TISSUES = ["pituitary gland", "adrenal gland"]
NEURAL_TISSUES = CNS_TISSUES + PNS_TISSUES + NEUROENDOCRINE_TISSUES

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
# Eisenberg & Levanon 2013 constitutive housekeeping genes (easy negative control).
HOUSEKEEPING = [
    "ACTB",
    "GAPDH",
    "B2M",
    "TBP",
    "PGK1",
    "RPLP0",
    "GUSB",
    "HPRT1",
    "PPIA",
    "TFRC",
    "RPL13A",
    "SDHA",
    "UBC",
    "YWHAZ",
    "EEF1A1",
    "PSMB4",
    "RAB7A",
    "REEP5",
    "C1orf43",
    "EMC7",
]
# Large CFS / large-locus genes for the hard-negative pool (literature-recurrent CFS hosts).
CANONICAL_CFS = [
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
    "NAALADL2",
    "PDE4D",
    "CNTNAP2",
    "DMD",
    "GMDS",
    "CSMD1",
    "EYS",
    "PCDH15",
    "MAGI2",
    "AGBL4",
    "DPP10",
    "ROBO2",
    "NRXN1",
    "NRXN3",
    "CADM2",
    "CDH13",
    "FHIT",
]


# GTEx carries some genes under their current HGNC symbol; map to the symbol the pipeline uses so
# candidates/effectors resolve (FAM19A2 is carried as TAFA2 in GTEx).
GTEX_SYMBOL_ALIASES = {"TAFA2": "FAM19A2"}


def load_gtex() -> pd.DataFrame:
    """GTEx median-TPM matrix (gene x tissue); one row per symbol (max-expressed transcript)."""
    df = pd.read_csv(GTEX, sep="\t", comment="#")
    df = df.rename(columns={"Gene Name": "symbol", "Gene ID": "ensembl"})
    df["symbol"] = df["symbol"].replace(GTEX_SYMBOL_ALIASES)
    tissue_cols = [c for c in df.columns if c not in ("symbol", "ensembl")]
    df[tissue_cols] = df[tissue_cols].apply(pd.to_numeric, errors="coerce").fillna(0.0)
    df = df.dropna(subset=["symbol"])
    df["_tot"] = df[tissue_cols].sum(axis=1)
    df = (
        df.sort_values("_tot", ascending=False)
        .drop_duplicates("symbol")
        .drop(columns="_tot")
    )
    return df.set_index("symbol")


def tau(row: np.ndarray) -> float:
    """Yanai 2005 tissue-specificity index: 0 = ubiquitous, 1 = single-tissue specific."""
    mx = row.max()
    if mx <= 0:
        return np.nan
    return float((1.0 - row / mx).sum() / (len(row) - 1))


def neural_scores(gtex: pd.DataFrame) -> pd.DataFrame:
    tissue_cols = [c for c in gtex.columns if c != "ensembl"]
    nonneural = [c for c in tissue_cols if c not in NEURAL_TISSUES]

    def grp_ratio(cols: list[str]) -> pd.Series:
        return np.log2(
            (gtex[cols].mean(axis=1) + 1.0) / (gtex[nonneural].mean(axis=1) + 1.0)
        )

    out = pd.DataFrame(index=gtex.index)
    out["ensembl"] = gtex["ensembl"]
    out["mean_neural_tpm"] = gtex[NEURAL_TISSUES].mean(axis=1)
    out["mean_nonneural_tpm"] = gtex[nonneural].mean(axis=1)
    out["neural_score"] = grp_ratio(NEURAL_TISSUES)
    out["cns_score"] = grp_ratio(CNS_TISSUES)
    out["pns_score"] = grp_ratio(PNS_TISSUES)
    out["neuroendocrine_score"] = grp_ratio(NEUROENDOCRINE_TISSUES)
    out["tau"] = gtex[tissue_cols].apply(lambda r: tau(r.to_numpy()), axis=1)
    out["neural_score_pct"] = (
        100.0 * out["neural_score"].rank(ascending=False, method="min") / len(out)
    )
    return out


def auc(pos: np.ndarray, neg: np.ndarray) -> float:
    """AUC via Mann-Whitney U (P(pos > neg))."""
    pos, neg = pos[~np.isnan(pos)], neg[~np.isnan(neg)]
    if len(pos) == 0 or len(neg) == 0:
        return np.nan
    u, _ = stats.mannwhitneyu(pos, neg, alternative="two-sided")
    return float(u / (len(pos) * len(neg)))


def span_matched_auc(
    scores: pd.DataFrame, span: pd.Series, pos_genes: list[str], rng, n: int
) -> dict:
    """AUC(effectors vs a genomic-span-matched random control), averaged over n matched control draws.

    For each positive gene, draw a control gene of similar genomic span (200-NN on log10 span, positives
    and the candidate set excluded). This is the redirect's hard negative: can the neural score separate
    true neural effectors from random loci OF THE SAME SIZE?
    """
    common = scores.index.intersection(span.dropna().index)
    sc = scores.loc[common, "neural_score"]
    logsp = np.log10(span.loc[common].astype(float))
    pos = [g for g in pos_genes if g in common]
    pos_vals = sc.loc[pos].to_numpy()
    exclude = set(pos) | set(CANDIDATES)
    pools = []
    for g in pos:
        d = (
            (logsp - logsp[g])
            .abs()
            .drop(index=[x for x in exclude if x in logsp.index])
        )
        pools.append(d.nsmallest(200).index.to_numpy())
    aucs = np.empty(n)
    for i in range(n):
        ctrl = sc.loc[[rng.choice(p) for p in pools]].to_numpy()
        aucs[i] = auc(pos_vals, ctrl)
    return {
        "auc_effectors_vs_span_matched_mean": round(float(np.nanmean(aucs)), 3),
        "auc_effectors_vs_span_matched_p05": round(float(np.nanpercentile(aucs, 5)), 3),
        "auc_effectors_vs_span_matched_p95": round(
            float(np.nanpercentile(aucs, 95)), 3
        ),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(RANDOM_SEED)
    gtex = load_gtex()
    scores = neural_scores(gtex)

    scores["is_candidate"] = scores.index.isin(CANDIDATES)
    scores["is_effector"] = scores.index.isin(EFFECTORS)
    scores["is_housekeeping"] = scores.index.isin(HOUSEKEEPING)
    scores["is_cfs"] = scores.index.isin(CANONICAL_CFS)

    # genomic span for the hard-negative matched benchmark
    rt = pd.read_feather(REPTIMING)
    rt = rt[rt["biotype"] == "protein_coding"].copy()
    rt["span_bp"] = (rt["end"] - rt["start"]).astype(float)
    span = rt.dropna(subset=["symbol", "span_bp"]).query("span_bp > 0")
    span = (
        span.sort_values("span_bp", ascending=False)
        .drop_duplicates("symbol")
        .set_index("symbol")["span_bp"]
    )

    s = scores["neural_score"]
    eff = s[scores.is_effector].to_numpy()
    hk = s[scores.is_housekeeping].to_numpy()
    cfs = s[scores.is_cfs].to_numpy()
    cand = s[scores.is_candidate].to_numpy()

    auc_rows = {
        "n_effectors_scored": int(scores.is_effector.sum()),
        "n_housekeeping_scored": int(scores.is_housekeeping.sum()),
        "n_cfs_scored": int(scores.is_cfs.sum()),
        "n_candidates_scored": int(scores.is_candidate.sum()),
        "auc_effectors_vs_housekeeping": round(auc(eff, hk), 3),
        "auc_effectors_vs_cfs": round(auc(eff, cfs), 3),
        "auc_candidates_vs_housekeeping": round(auc(cand, hk), 3),
        "auc_candidates_vs_cfs": round(auc(cand, cfs), 3),
        **span_matched_auc(scores, span, EFFECTORS, rng, N_MATCH_DRAWS),
        "median_neural_score_pct_effectors": round(
            float(scores.loc[scores.is_effector, "neural_score_pct"].median()), 2
        ),
        "median_neural_score_pct_candidates": round(
            float(scores.loc[scores.is_candidate, "neural_score_pct"].median()), 2
        ),
        "median_neural_score_pct_cfs": round(
            float(scores.loc[scores.is_cfs, "neural_score_pct"].median()), 2
        ),
    }

    # control-gene detail for the report
    detail = scores.loc[
        scores.is_candidate | scores.is_effector | scores.is_housekeeping,
        [
            "neural_score",
            "cns_score",
            "pns_score",
            "neuroendocrine_score",
            "tau",
            "neural_score_pct",
            "is_candidate",
            "is_effector",
            "is_housekeeping",
        ],
    ].copy()
    detail["role"] = np.where(
        detail.is_candidate,
        "candidate",
        np.where(detail.is_effector, "effector", "housekeeping"),
    )
    detail = detail.sort_values(["role", "neural_score"], ascending=[True, False])

    # --- write artifacts ---
    scores.reset_index().rename(columns={"index": "symbol"}).to_feather(
        OUT / "gene_neural_enrichment.feather"
    )
    pd.Series(auc_rows).to_frame("value").to_csv(OUT / "validation_auc.tsv", sep="\t")
    detail.reset_index().rename(columns={"index": "symbol"}).to_csv(
        OUT / "control_gene_scores.tsv", sep="\t", index=False
    )

    datapackage = {
        "name": "neural-gene-label-free-2026-06-08",
        "title": "t216 label-free neural-enrichment gene score (GTEx)",
        "description": "Data-driven per-gene neural-enrichment score from GTEx median TPM (q035), with "
        "CNS/PNS/neuroendocrine sub-scores and tau. Validated by AUC vs housekeeping (easy) and vs a "
        "genomic-span-matched CFS/large-locus null (hard, per t215 redirect). HPA layer deferred.",
        "created": "2026-06-08",
        "sources": [
            {"name": "gtex_median_tpm", "path": str(GTEX)},
            {"name": "gene_replication_timing", "path": str(REPTIMING)},
        ],
        "tasks": ["t216"],
        "related": [
            "question:q035-label-free-neural-gene-definition",
            "hypothesis:h12-neural-gene-enrichment-length-histology-artifact",
            "interpretation:2026-06-08-t217-genomic-span-cfs-null",
        ],
        "resources": [
            {
                "name": "gene_neural_enrichment",
                "path": "gene_neural_enrichment.feather",
            },
            {"name": "validation_auc", "path": "validation_auc.tsv"},
            {"name": "control_gene_scores", "path": "control_gene_scores.tsv"},
        ],
        "parameters": {
            "random_seed": RANDOM_SEED,
            "n_match_draws": N_MATCH_DRAWS,
            "neural_score": "log2((mean neural TPM + 1)/(mean non-neural TPM + 1))",
            "cns_tissues": CNS_TISSUES,
            "pns_tissues": PNS_TISSUES,
            "neuroendocrine_tissues": NEUROENDOCRINE_TISSUES,
            "candidates": CANDIDATES,
            "effectors": EFFECTORS,
            "hpa_status": "NOT AVAILABLE LOCALLY — deferred sensitivity layer (plan secondary atlas).",
        },
    }
    (OUT / "datapackage.json").write_text(json.dumps(datapackage, indent=2))

    # --- console summary ---
    pd.set_option("display.width", 220, "display.max_columns", 40)
    print(
        f"[t216] scored {len(scores)} genes over {len(NEURAL_TISSUES)} neural tissues "
        f"({len(CNS_TISSUES)} CNS + {len(PNS_TISSUES)} PNS + {len(NEUROENDOCRINE_TISSUES)} neuroendocrine)"
    )
    print("\n================ VALIDATION AUC ================")
    for k, v in auc_rows.items():
        print(f"  {k:42s} {v}")
    print("\n================ CONTROL-GENE NEURAL SCORES ================")
    print(
        detail[
            [
                "role",
                "neural_score",
                "cns_score",
                "pns_score",
                "neuroendocrine_score",
                "tau",
                "neural_score_pct",
            ]
        ]
        .round(3)
        .to_string()
    )
    print(f"\nArtifacts written to {OUT}/")
    print(
        "NOTE: HPA tissue-specificity not available locally — deferred sensitivity layer."
    )


if __name__ == "__main__":
    main()
