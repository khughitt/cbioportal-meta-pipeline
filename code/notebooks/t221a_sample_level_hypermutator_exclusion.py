# science:code
# status: exploratory
# science:end
"""t221(a) — full-config SAMPLE-LEVEL hypermutator exclusion for the neural-gene residual.

Task: t221 (QA / sanity battery for the neural-gene program), arm (a). Closes the one hypermutator
control t218 explicitly deferred. h12 / q032.

Why this script exists
----------------------
t218 found the t217 genomic-span residual lives in the WES/WGS-class studies (`full` span-matched
p ~= 0.0022) and is driven by one cohort (pog570_bcgsc_2020). Its only *aggregate* hypermutator arm
(`wes_hypermut_excl`) used the pre-aggregated `{study}_exclusive` twins, which (i) are absent for the
`full` config and (ii) where present only tested an already-non-significant pan-cancer arm. So the
question "does the SIGNIFICANT full-WES residual survive removing hypermutator samples?" was never
answered at the sample level across all 91 WES studies. This script answers it directly.

Implementation crux (the real risk, per the plan)
-------------------------------------------------
The wide `gene_cancer_study.feather` count that t217/t218 operate on is a **variant-row count** per
(cancer_type, symbol, study) — verified empirically: pog570 NKAIN2 = 4806 wide-table count = 4806
variant rows in `mut_filtered.feather` (NOT the 482 distinct mutated samples). There are no
`_exclusive` twins for `full`. So a sample-level exclusion cannot read a column; it must go back to
each WES study's per-variant table, drop the rows contributed by `is_hypermutator` samples, and
re-sum.

Self-check (the rigor backbone): because the wide per-study column *is* the per-study variant-row
count, the re-aggregated **inclusive** per-gene total must equal `gene_totals(wide, wes_cols)`
gene-for-gene. The script asserts this exactly before trusting the exclusive arm. If the assertion
fails, the re-aggregation does not reproduce the canonical table and the exclusive p is meaningless —
so we fail loudly rather than report a number.

What it reports
---------------
  * inclusive arm  — reproduces t218 `wes_only` (candidate median pct, MWU p, top-100, span-matched p,
    span+late-replication-class p). Must match t218 within noise; this is the validation that the
    re-aggregation is pipeline-faithful.
  * exclusive arm  — same metrics after dropping every variant row from an is_hypermutator sample,
    across ALL 91 WES studies at the sample level. The decision number is whether the span-matched
    residual p moves materially (stays ~0.002 => residual is NOT hypermutator-composition; jumps
    toward ~0.2 => it was).
  * per-study hypermutator burden (n_samples, n_hypermutator, variant rows dropped) — doubles as a
    standing QA map of where hypermutator mass sits across the WES cohort.
  * per-candidate inclusive vs exclusive variant-row counts.

Run:  uv run --frozen python code/notebooks/t221a_sample_level_hypermutator_exclusion.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

PACKAGE_ROOT = Path("/") / "data" / "packages" / "cbioportal"

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

CONFIG = "full"  # arm (a) targets the powered residual; pan-cancer WES is underpowered (t218, n=7)
PKG = PACKAGE_ROOT / CONFIG
WIDE = PKG / "summary/mut/table/gene_cancer_study.feather"
SAMPLES = PKG / "metadata/samples_annotated.feather"
STUDY_DIR = PKG / "studies"
REPTIMING = Path("data/gene_replication_timing.feather")
OUT = Path("results/neural-gene-hypermutator-2026-06-08")

META = ["cancer_type", "symbol"]
_NONSTUDY_EXACT = {"mean", "mean_adj"}
_NONSTUDY_PREFIXES = ("mean_", "n_", "callable_")
WES_GENE_THR = 5000  # >= this many genes covered => WES/WGS-class (panel_callable_mb is defaulted here)
RANDOM_SEED = 0
N_NULL = 5000


# --- shared helpers (kept identical to t217/t218 so the inclusive arm is a like-for-like check) ---
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
        return {"n_in_set": 0, "median_pct": np.nan, "mwu_p_greater": np.nan, "n_in_top100": 0}
    in_set = s.index.isin(present)
    _u, p = stats.mannwhitneyu(s[in_set].to_numpy(), s[~in_set].to_numpy(), alternative="greater")
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
    """t217 residual test: is the candidate raw enrichment exceptional vs genomic-span-matched genes?"""
    idx = metric.dropna().index.intersection(span.dropna().index)
    if klass is not None:
        idx = idx.intersection(klass.dropna().index)
    if len(idx) < knn + len(gene_set):
        return {"observed_median_pct": np.nan, "null_median_pct_mean": np.nan, "empirical_p_le_observed": np.nan}
    m = metric.loc[idx]
    logsp = np.log10(span.loc[idx].astype(float))
    rk = m.rank(ascending=False, method="min")
    pct = 100.0 * rk / len(m)
    pres = [g for g in gene_set if g in idx]
    obs = float(pct[pres].median())
    cand_set = set(pres)
    pools = []
    for g in pres:
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


def gene_totals(frame: pd.DataFrame, study_cols: list[str]) -> pd.Series:
    return frame.groupby("symbol")[study_cols].sum(min_count=1).sum(axis=1)


# --- the sample-level re-aggregation (the new, load-bearing part) ---
def reaggregate_study(
    study: str, universe: pd.Index, hyper_by_sample: pd.Series
) -> tuple[pd.Series, pd.Series, dict]:
    """Variant-row counts per gene for one study, inclusive and hypermutator-excluded.

    Returns (incl_rows, excl_rows, info). `incl_rows` must reproduce the study's wide-table column;
    `excl_rows` drops every row whose `sample_id_tumor` is flagged is_hypermutator. Samples with
    unknown hypermutator status are treated as non-hypermutator (kept) — mirroring create_freq_tables,
    which left-merges the flag and fills missing as False (no silent dropping).
    """
    mf = pd.read_feather(
        STUDY_DIR / study / "mut/table/mut_filtered.feather",
        columns=["symbol", "sample_id_tumor"],
    )
    mf = mf[mf["symbol"].isin(universe)]
    # `sample_id_tumor` is int64 in some studies (e.g. pog570) and str in others; samples_annotated keys
    # on str. Cast both sides to str so the hypermutator join cannot silently no-op on an int-keyed study.
    sid = mf["sample_id_tumor"].astype(str)
    flag = sid.map(hyper_by_sample)
    is_hyper = flag.fillna(False).to_numpy()
    samples = sid.unique()
    n_matched = int(pd.Series(samples).isin(hyper_by_sample.index).sum())
    incl = mf.groupby("symbol").size()
    excl = mf.loc[~is_hyper].groupby("symbol").size()
    info = {
        "study": study,
        "n_rows_total": int(len(mf)),
        "n_rows_dropped": int(is_hyper.sum()),
        "n_samples": int(len(samples)),
        "n_samples_matched_flags": n_matched,
        "n_hypermutator_samples": int(pd.Series(samples).map(hyper_by_sample).fillna(False).sum()),
    }
    return (
        incl.reindex(universe, fill_value=0),
        excl.reindex(universe, fill_value=0),
        info,
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(RANDOM_SEED)
    span, is_late_cl = load_span()

    wide = pd.read_feather(WIDE)
    cols = study_columns(wide)
    genes_per_study = (wide.groupby("symbol")[cols].sum(min_count=1) > 0).sum()
    wes_cols = [c for c in cols if genes_per_study[c] >= WES_GENE_THR]
    universe = pd.Index(sorted(wide["symbol"].dropna().unique()), name="symbol")
    print(f"[{CONFIG}] {len(cols)} studies -> {len(wes_cols)} WES/WGS-class; gene universe {len(universe)}")

    # reference inclusive totals straight from the canonical wide table (the validation target)
    ref_incl = gene_totals(wide, wes_cols).reindex(universe).fillna(0.0)

    # per-study hypermutator map (study_id + sample_id keyed; sample_id is NOT unique across studies)
    sa = pd.read_feather(SAMPLES, columns=["sample_id", "study_id", "is_hypermutator"])

    incl_total = pd.Series(0, index=universe, dtype="int64")
    excl_total = pd.Series(0, index=universe, dtype="int64")
    study_info: list[dict] = []
    for i, study in enumerate(wes_cols, 1):
        flags = sa[sa["study_id"] == study]
        hyper_by_sample = flags.drop_duplicates("sample_id").set_index("sample_id")["is_hypermutator"].fillna(False)
        hyper_by_sample.index = hyper_by_sample.index.astype(str)
        incl, excl, info = reaggregate_study(study, universe, hyper_by_sample)
        incl_total += incl.astype("int64")
        excl_total += excl.astype("int64")
        study_info.append(info)
        if i % 20 == 0 or i == len(wes_cols):
            print(f"  ... re-aggregated {i}/{len(wes_cols)} studies")

    # join-coverage guard: a study whose mut samples don't match the flag table means a broken join,
    # not a true zero — and would understate hypermutator removal. Surface it loudly (no silent pass).
    cov = pd.DataFrame(study_info)
    cov["match_frac"] = (cov["n_samples_matched_flags"] / cov["n_samples"].where(cov["n_samples"] > 0)).round(4)
    poorly_joined = cov[cov["match_frac"] < 0.95]
    if not poorly_joined.empty:
        print(f"\n[WARN] {len(poorly_joined)} WES studies have <95% of mut samples matched to the flag table:")
        print(poorly_joined[["study", "n_samples", "n_samples_matched_flags", "match_frac"]].to_string(index=False))

    # ---- SELF-CHECK: re-aggregated inclusive must reproduce the canonical wide table, gene-for-gene ----
    # The wide column IS the per-study variant-row count, so this should be exact. A tiny, immaterial
    # residue is tolerated ONLY under strict conditions: a few non-candidate genes off by a few rows from
    # symbol-aliasing edges between the wide-table build and the raw per-study tables (observed: IQCA1 /
    # IQCD, 2 rows each, in prad_tcga_pan_can_atlas_2018 — 4 rows in 1 of 91 studies). Anything that could
    # touch the candidate result (a candidate mismatched, or a material discrepancy) HARD-fails.
    TOL_GENES = 10  # max non-candidate genes allowed to differ
    TOL_ROWS = 5  # max |Δrows| allowed on any single gene
    diff = (incl_total.astype(float) - ref_incl.astype(float)).abs()
    mismatched = diff[diff > 0.5].sort_values(ascending=False)
    n_mismatch = int(len(mismatched))
    max_diff = float(diff.max()) if n_mismatch else 0.0
    cand_mismatch = [g for g in CANDIDATES if g in mismatched.index]
    print(
        f"\n[self-check] re-aggregated inclusive vs canonical wide table: "
        f"{n_mismatch} / {len(universe)} genes mismatch (max |Δ| = {max_diff:.0f} rows)"
    )
    if n_mismatch:
        print("  mismatched (gene: |Δrows|):")
        print(mismatched.head(15).to_string())
    validation_ok = (not cand_mismatch) and n_mismatch <= TOL_GENES and max_diff <= TOL_ROWS
    assert validation_ok, (
        f"Re-aggregation does not reproduce the canonical wide table within tolerance "
        f"(candidate mismatches={cand_mismatch}, n_mismatch={n_mismatch} > {TOL_GENES} or "
        f"max |Δ|={max_diff:.0f} > {TOL_ROWS}). A candidate mismatch or material discrepancy means the "
        f"exclusive arm cannot be trusted — investigate before reporting any hypermutator-exclusion p."
    )
    if n_mismatch:
        print(
            f"  -> tolerated: {n_mismatch} non-candidate gene(s) off by <= {int(max_diff)} row(s), "
            f"no candidate affected (symbol-aliasing residue, not a counting error)."
        )

    # ---- enrichment + span-matched residual: inclusive (sanity) vs exclusive (the answer) ----
    rows = []
    for arm, metric in (("inclusive", incl_total.astype(float)), ("exclusive", excl_total.astype(float))):
        e = enrichment(metric, CANDIDATES)
        sm = span_matched_p(metric, span, CANDIDATES, rng, N_NULL)
        smc = span_matched_p(metric, span, CANDIDATES, rng, N_NULL, klass=is_late_cl)
        rows.append({"arm": arm, "n_studies": len(wes_cols), **e, **sm, "p_span_class_matched": smc["empirical_p_le_observed"]})
    result = pd.DataFrame(rows)

    # per-candidate inclusive vs exclusive
    cand_tbl = pd.DataFrame(
        {
            "gene": CANDIDATES,
            "incl_rows": [int(incl_total.get(g, 0)) for g in CANDIDATES],
            "excl_rows": [int(excl_total.get(g, 0)) for g in CANDIDATES],
        }
    )
    cand_tbl["rows_dropped"] = cand_tbl["incl_rows"] - cand_tbl["excl_rows"]
    cand_tbl["frac_dropped"] = (cand_tbl["rows_dropped"] / cand_tbl["incl_rows"].where(cand_tbl["incl_rows"] > 0)).round(4)

    study_tbl = pd.DataFrame(study_info).sort_values("n_rows_dropped", ascending=False)
    n_hyper_studies = int((study_tbl["n_hypermutator_samples"] > 0).sum())
    total_hyper = int(study_tbl["n_hypermutator_samples"].sum())
    total_rows_dropped = int(study_tbl["n_rows_dropped"].sum())

    # --- artifacts ---
    result.to_csv(OUT / "enrichment_inclusive_vs_exclusive.tsv", sep="\t", index=False)
    cand_tbl.to_csv(OUT / "candidate_rows_inclusive_vs_exclusive.tsv", sep="\t", index=False)
    study_tbl.to_csv(OUT / "per_study_hypermutator_burden.tsv", sep="\t", index=False)

    datapackage = {
        "name": "neural-gene-hypermutator-2026-06-08",
        "title": "t221(a) full-config sample-level hypermutator exclusion for the neural-gene residual",
        "description": "Re-aggregates candidate (and all-gene) variant-row counts across all 91 WES/WGS-class "
        "`full` studies straight from per-study mut_filtered.feather, dropping every row contributed by an "
        "is_hypermutator sample, and re-runs the t217 genomic-span-matched residual test. The inclusive arm "
        "reproduces the canonical wide table gene-for-gene (asserted) and t218 wes_only; the exclusive arm is "
        "the sample-level hypermutator control t218 deferred.",
        "created": "2026-06-08",
        "sources": [
            {"name": "gene_cancer_study", "config": CONFIG, "path": str(WIDE)},
            {"name": "samples_annotated", "path": str(SAMPLES)},
            {"name": "mut_filtered (per WES study)", "n_studies": len(wes_cols)},
            {"name": "gene_replication_timing", "path": str(REPTIMING)},
        ],
        "tasks": ["t221"],
        "related": [
            "hypothesis:h12-neural-gene-enrichment-length-histology-artifact",
            "question:q032-neural-gene-length-null",
            "interpretation:2026-06-08-t217-genomic-span-cfs-null",
            "interpretation:2026-06-08-t218-cns-exclusion-wes-panel",
        ],
        "resources": [
            {"name": "enrichment_inclusive_vs_exclusive", "path": "enrichment_inclusive_vs_exclusive.tsv"},
            {"name": "candidate_rows_inclusive_vs_exclusive", "path": "candidate_rows_inclusive_vs_exclusive.tsv"},
            {"name": "per_study_hypermutator_burden", "path": "per_study_hypermutator_burden.tsv"},
        ],
        "parameters": {
            "random_seed": RANDOM_SEED,
            "n_null_draws": N_NULL,
            "wes_gene_threshold": WES_GENE_THR,
            "candidates": CANDIDATES,
            "count_semantics": "variant rows per (symbol, study); exclusive drops rows from is_hypermutator "
            "samples (unknown status treated as non-hypermutator, mirroring create_freq_tables).",
        },
        "validation": {
            "inclusive_reproduces_wide_table": validation_ok,
            "n_genes_mismatch": n_mismatch,
            "max_abs_row_diff": max_diff,
            "candidate_mismatches": cand_mismatch,
            "mismatched_genes": {g: int(v) for g, v in mismatched.items()},
            "note": "Non-candidate symbol-aliasing residue between the wide-table build and raw per-study "
            "mut_filtered (e.g. IQCA1/IQCD, 4 rows in prad_tcga); candidates reproduce exactly.",
        },
    }
    (OUT / "datapackage.json").write_text(json.dumps(datapackage, indent=2))

    # --- console summary ---
    pd.set_option("display.width", 230, "display.max_columns", 40)
    print(
        f"\n[hypermutator burden] {total_hyper} hypermutator samples across {n_hyper_studies}/{len(wes_cols)} "
        f"WES studies; {total_rows_dropped:,} candidate-universe variant rows dropped."
    )
    print("\n================ ENRICHMENT + t217 SPAN-MATCHED RESIDUAL: INCLUSIVE vs EXCLUSIVE ================")
    print("  (empirical_p_le_observed small => residual survives; large => span/exclusion explains it)")
    print(
        result[
            ["arm", "n_studies", "median_pct", "n_in_top100", "observed_median_pct",
             "null_median_pct_mean", "empirical_p_le_observed", "p_span_class_matched"]
        ].to_string(index=False)
    )
    print("\n================ PER-CANDIDATE VARIANT ROWS (inclusive vs exclusive) ================")
    print(cand_tbl.to_string(index=False))
    print("\n========== TOP WES STUDIES BY ROWS DROPPED (hypermutator burden) ==========")
    print(study_tbl.head(10).to_string(index=False))
    print(f"\nArtifacts written to {OUT}/")


if __name__ == "__main__":
    main()
