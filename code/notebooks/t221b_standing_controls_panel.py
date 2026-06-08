"""t221(b) — standing-controls panel for the neural-gene program.

Task: t221 (QA / sanity battery), arm (b). Follows t221(a) (sample-level hypermutator exclusion, ruled
out). h12 / q032. Four controls, each recomputing the t217 genomic-span-matched residual on the `full`
WES/WGS-class study set so the candidate verdict can be stress-tested from independent angles:

  1. Per-study intronic-fraction covariate (the generalisation of the pog570 lesson). The wide-table count
     is variant rows, which scale with how much non-coding territory a study's call set reports. We measure
     each WES study's intronic fraction directly and stratify the residual by it. Expectation: the residual
     concentrates in high-intronic ("all-region") studies and dissolves in exonic-clean ones — i.e. the
     residual is a call-set-region-scope artifact, not biology, and pog570 is the extreme of a gradient.

  2. CFS positive-control gene panel. The candidate residual should behave like KNOWN common-fragile-site
     genes (large late-replicating loci), not like driver genes. We run the same enrichment + span-matched
     null on the t216 `is_cfs` panel and compare. Expectation: candidates track the CFS panel (both raw-
     enriched, both large-locus, both with the same span-matched behaviour).

  3. Germline-leak control (matched-normal proxy). Matched-normal sequencing exists to remove germline /
     dbSNP variants; the candidates are 99.4th-pctile loci where leaked common SNPs would inflate counts.
     A faithful study-level matched/unmatched split is NOT available here (config-full.yml carries no
     `matched_normal_studies` list, and substrate proxies — sample_id_norm barcode presence — conflate
     matched-normal with assay type: TCGA/pog record normal barcodes, msk_impact is matched but records
     none). So we test germline leak DIRECTLY: the dbSNP-membership fraction of candidate variant rows vs
     background, and the residual recomputed after excluding every dbSNP-flagged ("rs...") row (a
     conservative upper bound — this over-excludes rare somatic-but-catalogued variants too). Expectation:
     candidate rows are not dbSNP-enriched and the residual survives, so germline leak is not the driver.

  4. Data-driven vs hand-labelled set sensitivity. The conclusion must not ride on the hand-picked 9. We
     take the most CNS-specific genes by t216's label-free `neural_score_pct` (excluding the candidates and
     effectors) as a data-driven neural set and run the same metrics. Expectation: a data-driven neural set
     shows the same span-confounded raw enrichment, confirming the pattern is a property of "large CNS
     genes", not of the specific 9.

Substrate: `full` wide `gene_cancer_study.feather` (variant-row counts; validated in t221a to equal the
per-study tables gene-for-gene), per-study `mut_filtered.feather` (consequence + dbsnp_rs, one pass),
`data/gene_replication_timing.feather` (genomic span + constitutive-late-replication class), and the t216
`gene_neural_enrichment.feather` (is_cfs / is_candidate / is_effector / neural_score_pct). random_seed = 0.

Run:  uv run --frozen python code/notebooks/t221b_standing_controls_panel.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
from scipy import stats


def read_available(path: Path, want: list[str]) -> tuple[pd.DataFrame, set[str]]:
    """Read only the wanted columns that exist (per-study mut tables have heterogeneous schemas).

    Missing columns are added as NA so callers can branch on presence without try/except chains. The
    schema is read from the Feather/Arrow footer (cheap) before pulling column data.
    """
    try:
        with pa.memory_map(str(path), "r") as src:
            names = set(pa.ipc.open_file(src).schema.names)
    except Exception:
        names = set(pd.read_feather(path).columns)
    have = [c for c in want if c in names]
    df = pd.read_feather(path, columns=have)
    for c in want:
        if c not in have:
            df[c] = pd.NA
    return df, names

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
PKG = Path(f"/data/packages/cbioportal/{CONFIG}")
WIDE = PKG / "summary/mut/table/gene_cancer_study.feather"
STUDY_DIR = PKG / "studies"
REPTIMING = Path("data/gene_replication_timing.feather")
NEURAL = Path("results/neural-gene-label-free-2026-06-08/gene_neural_enrichment.feather")
OUT = Path("results/neural-gene-standing-controls-2026-06-08")

META = ["cancer_type", "symbol"]
_NONSTUDY_EXACT = {"mean", "mean_adj"}
_NONSTUDY_PREFIXES = ("mean_", "n_", "callable_")
WES_GENE_THR = 5000
ALLREGION_THR = 0.50  # intronic fraction at/above which a study's call set is "all-region" (vs exonic)
DATADRIVEN_K = 25  # size of the data-driven neural set (top neural_score_pct, excl. candidates/effectors)
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
    rt = rt.sort_values("span_bp", ascending=False).drop_duplicates("symbol").set_index("symbol")
    return rt["span_bp"], rt["rt_constitutive_label"].eq("CL")


def coarse_region(consequence: str) -> str:
    c = str(consequence).lower()
    if any(k in c for k in ("missense", "stop_gain", "frameshift", "inframe", "start_lost", "stop_lost")):
        return "coding_nonsynonymous"
    if "synonymous" in c or "coding_sequence" in c or "incomplete_terminal" in c:
        return "coding_synonymous"
    if "splice" in c:
        return "splice"
    if "intron" in c:
        return "intronic"
    if "utr" in c:
        return "utr"
    if "upstream" in c or "downstream" in c or "intergenic" in c:
        return "flanking_intergenic"
    return "other"


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
    idx = metric.dropna().index.intersection(span.dropna().index)
    if klass is not None:
        idx = idx.intersection(klass.dropna().index)
    present = [g for g in gene_set if g in idx]
    if len(idx) < knn + len(present) or not present:
        return {"observed_median_pct": np.nan, "null_median_pct_mean": np.nan, "empirical_p_le_observed": np.nan}
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


def gene_totals(frame: pd.DataFrame, study_cols: list[str]) -> pd.Series:
    return frame.groupby("symbol")[study_cols].sum(min_count=1).sum(axis=1)


def span_pct(span: pd.Series, gene_set: list[str]) -> float:
    """Median genomic-span percentile of a gene set (positive-confound readout, as in t217 F3)."""
    s = span.dropna()
    present = [g for g in gene_set if g in s.index]
    if not present:
        return float("nan")
    rk = s.rank(ascending=True, method="min")  # ascending => larger span = higher percentile
    return round(float(100.0 * rk[present].median() / len(s)), 2)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(RANDOM_SEED)
    span, is_late_cl = load_span()

    wide = pd.read_feather(WIDE)
    cols = study_columns(wide)
    genes_per_study = (wide.groupby("symbol")[cols].sum(min_count=1) > 0).sum()
    wes_cols = [c for c in cols if genes_per_study[c] >= WES_GENE_THR]
    universe = pd.Index(sorted(wide["symbol"].dropna().unique()), name="symbol")
    wide_g = wide.groupby("symbol")[wes_cols].sum(min_count=1)  # per-study per-gene variant rows (validated t221a)
    full_wes_total = wide_g.sum(axis=1).reindex(universe).fillna(0.0)
    print(f"[{CONFIG}] {len(cols)} studies -> {len(wes_cols)} WES/WGS-class; gene universe {len(universe)}")

    # one pass over the WES per-study tables: intronic fraction + non-dbSNP per-gene counts ---------------
    intronic_frac: dict[str, float] = {}
    coding_frac: dict[str, float] = {}
    nondbsnp_total = pd.Series(0, index=universe, dtype="int64")
    cand_dbsnp_rows = 0  # candidate rows flagged dbSNP, counted only where the column exists
    cand_rows_dbknown = 0  # candidate rows in studies that record dbsnp_rs (the fraction's denominator)
    n_studies_with_dbsnp = 0
    for i, study in enumerate(wes_cols, 1):
        path = STUDY_DIR / study / "mut/table/mut_filtered.feather"
        mf, names = read_available(path, ["symbol", "consequence", "dbsnp_rs"])
        has_db = "dbsnp_rs" in names
        has_consequence = "consequence" in names
        mf = mf[mf["symbol"].isin(universe)]
        if has_consequence:
            region = mf["consequence"].map(coarse_region)
            intronic_frac[study] = float(region.eq("intronic").mean())
            coding_frac[study] = float(region.isin(["coding_nonsynonymous", "coding_synonymous"]).mean())
        else:  # cannot classify call-set region without a consequence column
            intronic_frac[study] = float("nan")
            coding_frac[study] = float("nan")
        is_db = mf["dbsnp_rs"].astype(str).str.strip().str.startswith("rs").to_numpy()
        nondbsnp_total = nondbsnp_total.add(
            mf.loc[~is_db].groupby("symbol").size().reindex(universe, fill_value=0).astype("int64"),
            fill_value=0,
        )
        cmask = mf["symbol"].isin(CANDIDATES).to_numpy()
        if has_db:
            n_studies_with_dbsnp += 1
            cand_rows_dbknown += int(cmask.sum())
            cand_dbsnp_rows += int((cmask & is_db).sum())
        if i % 20 == 0 or i == len(wes_cols):
            print(f"  ... scanned {i}/{len(wes_cols)} studies")
    nondbsnp_total = nondbsnp_total.astype(float)

    # ---- Section 1: intronic-fraction covariate + stratified residual --------------------------------
    ifrac = pd.Series(intronic_frac).dropna().sort_values(ascending=False)
    classifiable = list(ifrac.index)  # studies with a consequence column (intronic fraction defined)
    allregion = [s for s in classifiable if intronic_frac[s] >= ALLREGION_THR]
    exonic = [s for s in classifiable if intronic_frac[s] < ALLREGION_THR]
    n_unclassifiable = len(wes_cols) - len(classifiable)
    strata = {
        "all_wes": wes_cols,
        f"all_region_intronic>={ALLREGION_THR:g}": allregion,
        f"exonic_intronic<{ALLREGION_THR:g}": exonic,
    }
    sec1_rows = []
    for name, scols in strata.items():
        if not scols:
            continue
        tot = wide_g[scols].sum(axis=1).reindex(universe).fillna(0.0)
        e = enrichment(tot, CANDIDATES)
        sm = span_matched_p(tot, span, CANDIDATES, rng, N_NULL)
        sec1_rows.append({"stratum": name, "n_studies": len(scols), **e, "span_matched_p": sm["empirical_p_le_observed"]})
    sec1 = pd.DataFrame(sec1_rows)
    per_study_ifrac = pd.DataFrame(
        {"study": ifrac.index, "intronic_frac": ifrac.round(4).values, "coding_frac": [round(coding_frac[s], 4) for s in ifrac.index]}
    )

    # ---- Section 2: CFS positive-control panel vs candidates -----------------------------------------
    neural = pd.read_feather(NEURAL)
    cfs_set = neural.loc[neural["is_cfs"], "symbol"].tolist()
    sec2_rows = []
    for name, gs in (("candidates", CANDIDATES), ("cfs_panel", cfs_set)):
        e = enrichment(full_wes_total, gs)
        sm = span_matched_p(full_wes_total, span, gs, rng, N_NULL)
        smc = span_matched_p(full_wes_total, span, gs, rng, N_NULL, klass=is_late_cl)
        sec2_rows.append(
            {"gene_set": name, "n_genes": len([g for g in gs if g in full_wes_total.index]),
             "median_span_pct": span_pct(span, gs), **e,
             "span_matched_p": sm["empirical_p_le_observed"], "span_class_matched_p": smc["empirical_p_le_observed"]}
        )
    sec2 = pd.DataFrame(sec2_rows)

    # ---- Section 3: germline-leak (dbSNP) control ----------------------------------------------------
    e_incl = enrichment(full_wes_total, CANDIDATES)
    sm_incl = span_matched_p(full_wes_total, span, CANDIDATES, rng, N_NULL)
    e_nodb = enrichment(nondbsnp_total, CANDIDATES)
    sm_nodb = span_matched_p(nondbsnp_total, span, CANDIDATES, rng, N_NULL)
    cand_dbsnp_frac = cand_dbsnp_rows / cand_rows_dbknown if cand_rows_dbknown else float("nan")
    sec3 = pd.DataFrame(
        [
            {"arm": "inclusive", "candidate_dbsnp_frac": round(cand_dbsnp_frac, 4),
             "median_pct": e_incl["median_pct"], "span_matched_p": sm_incl["empirical_p_le_observed"]},
            {"arm": "dbsnp_excluded", "candidate_dbsnp_frac": 0.0,
             "median_pct": e_nodb["median_pct"], "span_matched_p": sm_nodb["empirical_p_le_observed"]},
        ]
    )

    # ---- Section 4: data-driven vs hand-labelled set -------------------------------------------------
    # Two label-free axes: the composite neural_score and the CNS-structural sub-score (the candidates'
    # actual axis). Reporting both preempts "what if you'd ranked by the CNS sub-score?". Neither should
    # reproduce the candidate enrichment if the driver is locus size, not the neural label.
    exclude = set(CANDIDATES) | set(neural.loc[neural["is_effector"], "symbol"])
    pool = neural[~neural["symbol"].isin(exclude)]
    dd_neural = pool.dropna(subset=["neural_score"]).sort_values("neural_score", ascending=False).head(DATADRIVEN_K)["symbol"].tolist()
    dd_cns = pool.dropna(subset=["cns_score"]).sort_values("cns_score", ascending=False).head(DATADRIVEN_K)["symbol"].tolist()
    sec4_rows = []
    sec4_sets = (
        ("hand_labelled_candidates", CANDIDATES),
        (f"data_driven_top{DATADRIVEN_K}_neural_score", dd_neural),
        (f"data_driven_top{DATADRIVEN_K}_cns_score", dd_cns),
    )
    for name, gs in sec4_sets:
        e = enrichment(full_wes_total, gs)
        sm = span_matched_p(full_wes_total, span, gs, rng, N_NULL)
        sec4_rows.append(
            {"gene_set": name, "n_genes": len([g for g in gs if g in full_wes_total.index]),
             "median_span_pct": span_pct(span, gs), **e, "span_matched_p": sm["empirical_p_le_observed"]}
        )
    sec4 = pd.DataFrame(sec4_rows)
    dd_set_df = pd.concat([
        pd.DataFrame({"axis": "neural_score", "symbol": dd_neural}),
        pd.DataFrame({"axis": "cns_score", "symbol": dd_cns}),
    ], ignore_index=True)

    # --- artifacts ---
    sec1.to_csv(OUT / "intronic_fraction_stratified_residual.tsv", sep="\t", index=False)
    per_study_ifrac.to_csv(OUT / "per_study_intronic_fraction.tsv", sep="\t", index=False)
    sec2.to_csv(OUT / "cfs_positive_control.tsv", sep="\t", index=False)
    sec3.to_csv(OUT / "germline_dbsnp_control.tsv", sep="\t", index=False)
    sec4.to_csv(OUT / "data_driven_set_sensitivity.tsv", sep="\t", index=False)
    dd_set_df.to_csv(OUT / "data_driven_neural_set.tsv", sep="\t", index=False)

    datapackage = {
        "name": "neural-gene-standing-controls-2026-06-08",
        "title": "t221(b) standing-controls panel for the neural-gene program",
        "description": "Four standing controls on the `full` WES study set: (1) per-study intronic-fraction "
        "covariate + stratified residual, (2) CFS positive-control gene panel, (3) germline-leak (dbSNP) "
        "control, (4) data-driven vs hand-labelled neural set. Each recomputes the t217 genomic-span-matched "
        "residual. random_seed=0.",
        "created": "2026-06-08",
        "sources": [
            {"name": "gene_cancer_study", "config": CONFIG, "path": str(WIDE)},
            {"name": "mut_filtered (per WES study)", "n_studies": len(wes_cols)},
            {"name": "gene_replication_timing", "path": str(REPTIMING)},
            {"name": "gene_neural_enrichment (t216)", "path": str(NEURAL)},
        ],
        "tasks": ["t221"],
        "related": [
            "hypothesis:h12-neural-gene-enrichment-length-histology-artifact",
            "question:q032-neural-gene-length-null",
            "interpretation:2026-06-08-t217-genomic-span-cfs-null",
            "interpretation:2026-06-08-t218-cns-exclusion-wes-panel",
            "interpretation:2026-06-08-t221a-sample-level-hypermutator-exclusion",
        ],
        "resources": [
            {"name": "intronic_fraction_stratified_residual", "path": "intronic_fraction_stratified_residual.tsv"},
            {"name": "per_study_intronic_fraction", "path": "per_study_intronic_fraction.tsv"},
            {"name": "cfs_positive_control", "path": "cfs_positive_control.tsv"},
            {"name": "germline_dbsnp_control", "path": "germline_dbsnp_control.tsv"},
            {"name": "data_driven_set_sensitivity", "path": "data_driven_set_sensitivity.tsv"},
            {"name": "data_driven_neural_set", "path": "data_driven_neural_set.tsv"},
        ],
        "parameters": {
            "random_seed": RANDOM_SEED,
            "n_null_draws": N_NULL,
            "wes_gene_threshold": WES_GENE_THR,
            "all_region_intronic_threshold": ALLREGION_THR,
            "data_driven_k": DATADRIVEN_K,
            "candidates": CANDIDATES,
        },
        "runtime": {
            "n_wes_studies": len(wes_cols),
            "n_studies_with_dbsnp": n_studies_with_dbsnp,
            "candidate_dbsnp_frac": round(cand_dbsnp_frac, 4),
            "n_all_region_studies": len(allregion),
            "n_classifiable_intronic": len(classifiable),
            "n_unclassifiable_no_consequence": n_unclassifiable,
        },
        "caveats": {
            "matched_normal_split": "config-full.yml carries no matched_normal_studies list, and substrate "
            "proxies (sample_id_norm barcode presence) conflate matched-normal with assay type. Section 3 "
            "therefore tests germline leak directly via dbSNP membership rather than a study-level "
            "matched/unmatched split. Follow-up: populate matched_normal_studies for the full config to "
            "enable a true matched-normal stratification.",
            "dbsnp_excluded_is_conservative": "Excluding all 'rs...' rows over-excludes rare somatic-but-"
            "catalogued variants, so it is an upper bound on germline contamination, not a germline-only filter.",
        },
    }
    (OUT / "datapackage.json").write_text(json.dumps(datapackage, indent=2))

    # --- console summary ---
    pd.set_option("display.width", 230, "display.max_columns", 40)
    print(f"\n[intronic fraction] {len(allregion)}/{len(classifiable)} classifiable WES studies are all-region "
          f"(intronic >= {ALLREGION_THR:g}); {n_unclassifiable} lack a consequence column; "
          f"top: {', '.join(f'{s}={intronic_frac[s]:.2f}' for s in ifrac.index[:4])}")
    print("\n================ (1) INTRONIC-FRACTION-STRATIFIED RESIDUAL ================")
    print(sec1.to_string(index=False))
    print("\n================ (2) CFS POSITIVE-CONTROL PANEL vs CANDIDATES ================")
    print(sec2.to_string(index=False))
    print(f"\n================ (3) GERMLINE-LEAK (dbSNP) CONTROL  [candidate dbSNP frac = {cand_dbsnp_frac:.3f}, "
          f"{n_studies_with_dbsnp}/{len(wes_cols)} studies record dbsnp_rs] ================")
    print(sec3.to_string(index=False))
    print(f"\n================ (4) DATA-DRIVEN (top-{DATADRIVEN_K}) vs HAND-LABELLED ================")
    print(sec4.to_string(index=False))
    print(f"  top neural_score: {', '.join(dd_neural[:10])}")
    print(f"  top cns_score:    {', '.join(dd_cns[:10])}")
    print(f"\nArtifacts written to {OUT}/")


if __name__ == "__main__":
    main()
