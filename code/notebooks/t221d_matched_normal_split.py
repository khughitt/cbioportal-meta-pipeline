# science:code
# status: exploratory
# science:end
"""t221(d) — true study-level matched- vs unmatched-normal germline-leak split on the WES candidate residual.

Task: t221 follow-up. Closes the F3 caveat of t221(b): with `matched_normal_studies` now populated in
config-full.yml (t221c, evidence-derived from per-variant normal barcodes), we can finally run the
germline-leak control the way matched-normal sequencing actually serves it — a STUDY-LEVEL matched vs
unmatched split — instead of the dbSNP-membership proxy.

The logic: patient-matched-normal sequencing exists to subtract germline / private SNP variants. If the
candidate enrichment (large late-replicating CNS/CFS loci, ~99.4th span percentile, where leaked common
SNPs would inflate variant-row counts) were driven by germline contamination, it would be carried by the
UNMATCHED (tumor-only / pooled-normal) studies and be ABSENT or much weaker in the MATCHED ones. Prediction
(consistent with t221b-F3's dbSNP control): the residual is present in BOTH arms and is not preferentially
in the unmatched arm — i.e. germline leak is not the driver.

The confound this run must disentangle (named explicitly because it is load-bearing): the entire residual
lives in the 6 "all-region" cohorts (t221b-F1), and those split 2 matched / 4 unmatched. So a naive
matched-vs-unmatched contrast is partly a region-scope contrast. We therefore also run the matched/unmatched
split WITHIN each region stratum (a 2x2), and we lean on the single sharpest datum: pog570 — the biggest
single-cohort residual-carrier (t218) — is MATCHED-normal, so the largest piece of the residual cannot be
germline leak by construction.

Substrate: `full` wide `gene_cancer_study.feather` (variant-row counts; validated gene-for-gene in t221a),
`data/gene_replication_timing.feather` (genomic span + constitutive-late-replication class), the t221b
per-study intronic-fraction table (region stratum labels), and `matched_normal_studies` from config-full.yml
(t221c). random_seed = 0.

Run:  uv run --frozen python code/notebooks/t221d_matched_normal_split.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from scipy import stats

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

CONFIG = "full"
PACKAGE_ROOT = Path("/") / "data" / "packages" / "cbioportal"
PKG = PACKAGE_ROOT / CONFIG
WIDE = PKG / "summary/mut/table/gene_cancer_study.feather"
REPTIMING = Path("data/gene_replication_timing.feather")
CONFIG_YML = Path("code/config/config-full.yml")
PER_STUDY_IFRAC = Path(
    "results/neural-gene-standing-controls-2026-06-08/per_study_intronic_fraction.tsv"
)
OUT = Path("results/neural-gene-matched-normal-split-2026-06-08")

META = ["cancer_type", "symbol"]
_NONSTUDY_EXACT = {"mean", "mean_adj"}
_NONSTUDY_PREFIXES = ("mean_", "n_", "callable_")
WES_GENE_THR = 5000
ALLREGION_THR = 0.50
RANDOM_SEED = 0
N_NULL = 5000


def study_columns(df: pd.DataFrame) -> list[str]:
    out = []
    for c in df.columns:
        if c in META or c in _NONSTUDY_EXACT or c.endswith("_exclusive"):
            continue
        if c.startswith(_NONSTUDY_PREFIXES):
            continue
        out.append(c)
    return out


def load_span() -> tuple[pd.Series, pd.Series]:
    rt = pd.read_feather(REPTIMING)
    rt = rt[rt["biotype"] == "protein_coding"].copy()
    rt["span_bp"] = (rt["end"] - rt["start"]).astype(float)
    rt = rt.dropna(subset=["symbol", "span_bp"]).query("span_bp > 0")
    rt = (
        rt.sort_values("span_bp", ascending=False)
        .drop_duplicates("symbol")
        .set_index("symbol")
    )
    return rt["span_bp"], rt["rt_constitutive_label"].eq("CL")


def enrichment(metric: pd.Series, gene_set: list[str], topn: int = 100) -> dict:
    s = metric.dropna()
    present = [g for g in gene_set if g in s.index]
    if not present:
        return {
            "n_in_set": 0,
            "median_pct": np.nan,
            "mwu_p_greater": np.nan,
            "n_in_top100": 0,
        }
    in_set = s.index.isin(present)
    _u, p = stats.mannwhitneyu(
        s[in_set].to_numpy(), s[~in_set].to_numpy(), alternative="greater"
    )
    rk = s.rank(ascending=False, method="min")
    return {
        "n_in_set": len(present),
        "median_pct": round(float(100.0 * rk[present].median() / len(s)), 3),
        "mwu_p_greater": float(p),
        "n_in_top100": int((rk[present] <= topn).sum()),
    }


def span_matched_p(
    metric: pd.Series,
    span: pd.Series,
    gene_set: list[str],
    rng,
    n: int,
    knn: int = 200,
    klass: pd.Series | None = None,
) -> dict:
    idx = metric.dropna().index.intersection(span.dropna().index)
    if klass is not None:
        idx = idx.intersection(klass.dropna().index)
    present = [g for g in gene_set if g in idx]
    if len(idx) < knn + len(present) or not present:
        return {
            "observed_median_pct": np.nan,
            "null_median_pct_mean": np.nan,
            "empirical_p_le_observed": np.nan,
        }
    m = metric.loc[idx]
    logsp = np.log10(span.loc[idx].astype(float))
    rk = m.rank(ascending=False, method="min")
    pct = 100.0 * rk / len(m)
    obs = float(pct[present].median())
    cand_set = set(present)
    pools = []
    for g in present:
        elig = logsp
        if klass is not None:
            elig = logsp[klass.loc[idx] == klass[g]]
        d = (elig - logsp[g]).abs().drop(index=[x for x in cand_set if x in elig.index])
        pools.append(d.nsmallest(knn).index.to_numpy())
    draws = np.empty(n)
    for i in range(n):
        draws[i] = float(np.median(pct.loc[[rng.choice(p) for p in pools]]))
    return {
        "observed_median_pct": round(obs, 3),
        "null_median_pct_mean": round(float(draws.mean()), 3),
        "empirical_p_le_observed": float((draws <= obs).mean()),
    }


def arm_metrics(
    wide_g: pd.DataFrame,
    universe: pd.Index,
    span: pd.Series,
    is_late_cl: pd.Series,
    cols: list[str],
    rng,
) -> dict:
    """Enrichment + span-matched + span+class-matched residual for the candidate set over an arm's studies."""
    if not cols:
        return {
            "n_studies": 0,
            "cand_rows": 0,
            "n_in_set": 0,
            "median_pct": np.nan,
            "n_in_top100": 0,
            "span_matched_p": np.nan,
            "span_class_matched_p": np.nan,
        }
    tot = wide_g[cols].sum(axis=1).reindex(universe).fillna(0.0)
    e = enrichment(tot, CANDIDATES)
    sm = span_matched_p(tot, span, CANDIDATES, rng, N_NULL)
    smc = span_matched_p(tot, span, CANDIDATES, rng, N_NULL, klass=is_late_cl)
    return {
        "n_studies": len(cols),
        "cand_rows": int(tot.reindex(CANDIDATES).fillna(0).sum()),
        "n_in_set": e["n_in_set"],
        "median_pct": e["median_pct"],
        "n_in_top100": e["n_in_top100"],
        "span_matched_p": sm["empirical_p_le_observed"],
        "span_class_matched_p": smc["empirical_p_le_observed"],
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(RANDOM_SEED)
    span, is_late_cl = load_span()

    cfg = yaml.safe_load(CONFIG_YML.read_text())
    matched_set = set(cfg.get("matched_normal_studies", []))
    print(f"matched_normal_studies in {CONFIG_YML}: {len(matched_set)} studies")

    wide = pd.read_feather(WIDE)
    cols = study_columns(wide)
    genes_per_study = (wide.groupby("symbol")[cols].sum(min_count=1) > 0).sum()
    wes_cols = [c for c in cols if genes_per_study[c] >= WES_GENE_THR]
    universe = pd.Index(sorted(wide["symbol"].dropna().unique()), name="symbol")
    wide_g = wide.groupby("symbol")[wes_cols].sum(min_count=1)
    print(
        f"[{CONFIG}] {len(cols)} studies -> {len(wes_cols)} WES/WGS-class; gene universe {len(universe)}"
    )

    # primary split: matched vs unmatched over all WES studies ------------------------------------------
    matched_cols = [c for c in wes_cols if c in matched_set]
    unmatched_cols = [c for c in wes_cols if c not in matched_set]
    print(
        f"WES split: {len(matched_cols)} matched-normal, {len(unmatched_cols)} unmatched (tumor-only/pooled)"
    )

    arms = {
        "all_wes": wes_cols,
        "matched_normal": matched_cols,
        "unmatched": unmatched_cols,
    }
    primary = pd.DataFrame(
        [
            {"arm": name, **arm_metrics(wide_g, universe, span, is_late_cl, c, rng)}
            for name, c in arms.items()
        ]
    )

    # region-stratified 2x2: disentangle matched-status from call-set region scope ---------------------
    # the residual lives entirely in the all-region cohorts (t221b-F1), which split 2 matched / 4 unmatched,
    # so the clean germline test is matched-vs-unmatched WITHIN region scope.
    ifrac = pd.read_csv(PER_STUDY_IFRAC, sep="\t").set_index("study")["intronic_frac"]
    allregion = set(ifrac[ifrac >= ALLREGION_THR].index)
    region_of = {
        s: ("all_region" if s in allregion else "exonic")
        for s in wes_cols
        if s in ifrac.index
    }
    cells = {
        ("all_region", "matched"): [
            s for s in matched_cols if region_of.get(s) == "all_region"
        ],
        ("all_region", "unmatched"): [
            s for s in unmatched_cols if region_of.get(s) == "all_region"
        ],
        ("exonic", "matched"): [
            s for s in matched_cols if region_of.get(s) == "exonic"
        ],
        ("exonic", "unmatched"): [
            s for s in unmatched_cols if region_of.get(s) == "exonic"
        ],
    }
    twobytwo = pd.DataFrame(
        [
            {
                "region": r,
                "normal_status": ns,
                "studies": ", ".join(sorted(c)),
                **arm_metrics(wide_g, universe, span, is_late_cl, c, rng),
            }
            for (r, ns), c in cells.items()
        ]
    )

    # per-study residual-carrier census within each arm (descriptive, sharpest = pog570 is matched) -----
    cand_by_study = wide_g.reindex(CANDIDATES).fillna(0.0).sum(axis=0)
    carriers = pd.DataFrame(
        {
            "study": cand_by_study.index,
            "candidate_rows": cand_by_study.astype(int).values,
            "normal_status": [
                "matched" if s in matched_set else "unmatched"
                for s in cand_by_study.index
            ],
            "region": [region_of.get(s, "unclassifiable") for s in cand_by_study.index],
        }
    ).sort_values("candidate_rows", ascending=False)

    # --- artifacts ---
    primary.to_csv(OUT / "matched_unmatched_primary.tsv", sep="\t", index=False)
    twobytwo.to_csv(OUT / "matched_unmatched_by_region.tsv", sep="\t", index=False)
    carriers.to_csv(OUT / "candidate_carrier_studies.tsv", sep="\t", index=False)

    matched_cand_rows = int(
        cand_by_study[[s for s in cand_by_study.index if s in matched_set]].sum()
    )
    total_cand_rows = int(cand_by_study.sum())
    datapackage = {
        "name": "neural-gene-matched-normal-split-2026-06-08",
        "title": "t221(d) true study-level matched- vs unmatched-normal split on the WES candidate residual",
        "description": "Splits the `full` WES study set into patient-matched-normal vs unmatched (tumor-only/"
        "pooled) arms using config-full's matched_normal_studies (t221c) and recomputes the t217 genomic-span-"
        "matched candidate residual in each, plus a region x normal-status 2x2 to disentangle matched-status "
        "from call-set region scope. Closes the t221b-F3 dbSNP-proxy caveat. random_seed=0.",
        "created": "2026-06-08",
        "sources": [
            {"name": "gene_cancer_study", "config": CONFIG, "path": str(WIDE)},
            {"name": "gene_replication_timing", "path": str(REPTIMING)},
            {
                "name": "per_study_intronic_fraction (t221b)",
                "path": str(PER_STUDY_IFRAC),
            },
            {"name": "matched_normal_studies (t221c)", "path": str(CONFIG_YML)},
        ],
        "tasks": ["t221"],
        "related": [
            "hypothesis:h12-neural-gene-enrichment-length-histology-artifact",
            "question:q032-neural-gene-length-null",
            "question:q016-panel-induced-ascertainment",
            "interpretation:2026-06-08-t221b-standing-controls-panel",
        ],
        "resources": [
            {
                "name": "matched_unmatched_primary",
                "path": "matched_unmatched_primary.tsv",
            },
            {
                "name": "matched_unmatched_by_region",
                "path": "matched_unmatched_by_region.tsv",
            },
            {
                "name": "candidate_carrier_studies",
                "path": "candidate_carrier_studies.tsv",
            },
        ],
        "parameters": {
            "random_seed": RANDOM_SEED,
            "n_null_draws": N_NULL,
            "wes_gene_threshold": WES_GENE_THR,
            "all_region_intronic_threshold": ALLREGION_THR,
            "candidates": CANDIDATES,
        },
        "runtime": {
            "n_wes_studies": len(wes_cols),
            "n_matched": len(matched_cols),
            "n_unmatched": len(unmatched_cols),
            "candidate_rows_matched_frac": round(matched_cand_rows / total_cand_rows, 4)
            if total_cand_rows
            else None,
        },
        "caveats": {
            "region_confound": "The residual lives entirely in the 6 all-region cohorts (t221b-F1), which "
            "split 2 matched / 4 unmatched, so the primary matched-vs-unmatched contrast is partly a "
            "region-scope contrast; the by-region 2x2 is the de-confounded view (thin power: 2 vs 4 studies "
            "in the all-region row).",
            "matched_list_is_lower_bound": "matched_normal_studies (t221c) is a high-precision evidence-derived "
            "lower bound; matched-by-design-but-unrecorded cohorts (MSK-IMPACT family) are panels, excluded "
            "from the WES set anyway, so they do not affect this split.",
            "variant_row_substrate": "Metric is variant-row counts (the t217/t218 substrate the span confound "
            "lives in), not sample-level ratios.",
        },
    }
    (OUT / "datapackage.json").write_text(json.dumps(datapackage, indent=2))

    # --- console summary ---
    pd.set_option("display.width", 230, "display.max_columns", 40)
    print(
        "\n================ (1) PRIMARY: matched vs unmatched (all WES) ================"
    )
    print(primary.to_string(index=False))
    print(
        "\n================ (2) REGION x NORMAL-STATUS 2x2 (de-confounds region scope) ================"
    )
    print(twobytwo.drop(columns=["studies"]).to_string(index=False))
    for _, row in twobytwo.iterrows():
        print(
            f"  [{row['region']}/{row['normal_status']}] {row['n_studies']} studies: {row['studies']}"
        )
    print(
        f"\n================ (3) CANDIDATE-ROW CARRIERS (top 12; matched frac = "
        f"{matched_cand_rows / total_cand_rows:.3f}) ================"
    )
    print(carriers.head(12).to_string(index=False))
    print(f"\nArtifacts written to {OUT}/")


if __name__ == "__main__":
    main()
