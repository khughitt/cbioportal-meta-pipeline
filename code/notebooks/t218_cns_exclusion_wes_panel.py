# science:code
# status: exploratory
# science:end
"""t218 — CNS-exclusion + WES-restriction + panel-membership stratification for neural enrichment.

Question: q033 (CNS exclusion) / hypothesis h12-neural-gene-enrichment-length-histology-artifact.
Plan: doc/plans/2026-06-06-neural-gene-enrichment-meta-analysis-plan.md (step 3, t218).
Closes the residual left by t217: doc/interpretations/2026-06-08-t217-genomic-span-cfs-null.md (F5) —
a small candidate over-enrichment ABOVE the genomic-span trend (`full` span-matched p = 0.006). t217
GUESSED panel ascertainment (q016). This script tests that head-to-head against CNS histology and finds
BOTH are wrong: the residual is a single-WGS-study assay-reach effect (see OUTCOME below).

Assay class is read straight from the substrate (no defaulted metadata): `panel_callable_mb` is pinned
to the 30 Mb WES default for almost all studies here, so it cannot discriminate assay. Instead a study is
called **WES/WGS** if it reports mutations across >= `WES_GENE_THR` distinct genes and **panel/limited**
otherwise — targeted panels tile only hundreds of genes, exomes thousands.

Restrictions (each recomputes candidate median percentile, MWU p, top-100 occupancy, and the kNN
genomic-span-matched empirical residual p from t217):
  baseline            all studies, all cancers           (reproduces t217)
  cns_excluded        drop CNS/glioma cancer types        (q033 core; neuroendocrine left to t219)
  wes_only            keep only WES/WGS study columns      (removes panel ascertainment)
  wes_only_cns_excl   WES/WGS studies AND CNS removed       (cleanest: both confounds gone)
  panel_only          keep only panel/limited studies      (contrast)
  wes_hypermut_excl   WES studies, hypermutator samples removed (where `_exclusive` twins exist)
  wes_excl_wgs_driver WES studies minus the sole LOSO driver (a high-burden WGS cohort)

OUTCOME (recorded here so the script self-documents): the t217 F5 "panel ascertainment" guess is WRONG.
The residual lives in the WES/WGS-class studies (p~0.002) and is ABSENT in panels (p~1.0; panels barely
tile these genes). It is robust to span-matching, span+late-replication-class matching, and CNS exclusion
— but it is driven ENTIRELY by one cohort (pog570_bcgsc_2020): dropping it returns the candidates to the
span-matched null (p 0.002 -> 0.19). That cohort's mutation table is all-region (t218b: 98.5% of its
candidate variant rows are intronic) and carries 0/570 hypermutators, so these CFS loci accrue whole-span
counts — the genomic-span confound amplified by call-set region coverage, not by assay label, panel
ascertainment, hypermutators, or biology. q033 answered (candidate-set mutational thread): NOT CNS-driven.
NB the aggregate hypermutator arm (pan-cancer wes_hypermut_excl) tests an already-non-significant arm and
does NOT bear on the significant full-WES residual; the driver-cohort zero-hypermutator fact (t218b) does.

Plus: per-candidate CNS contribution (q033 deliverable, esp. LSAMP/OPCML/RBFOX1), leave-one-study-out
(single-study vs diffuse origin), and a panel-membership check (are the candidates tiled by the panels
that report them?). random_seed = 0.

Run:  uv run --frozen python code/notebooks/t218_cns_exclusion_wes_panel.py
"""

from __future__ import annotations

import json
import re
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
FOCUS = ["LSAMP", "OPCML", "RBFOX1"]  # q033 names these explicitly

META = ["cancer_type", "symbol"]
_NONSTUDY_EXACT = {"mean", "mean_adj"}
_NONSTUDY_PREFIXES = ("mean_", "n_", "callable_")

CONFIGS = {
    "full": PACKAGE_ROOT / "full/summary/mut/table",
    "pan-cancer": PACKAGE_ROOT / "pan-cancer/summary/mut/table",
}
REPTIMING = Path("data/gene_replication_timing.feather")
GENIE_COV = Path(
    PACKAGE_ROOT / "pan-cancer/metadata/genie_panel_coverage.feather"
)
OUT = Path("results/neural-gene-cns-wes-2026-06-08")

WES_GENE_THR = (
    5000  # >= this many distinct genes covered => WES/WGS; else panel/limited
)
# Sole study flagged by leave-one-study-out as moving candidate median > 0.1 pct. Its mutation table is
# all-region (t218b: ~98.5% of candidate variant rows intronic) despite a `wes` study_panels label, so it
# tiles these multi-Mb loci across their whole gene body. Recorded as a named constant for the driver arm.
LOSO_DRIVER = "pog570_bcgsc_2020"
RANDOM_SEED = 0
N_NULL = 5000

# CNS / glioma cancer types. Match neural-structural histologies but EXCLUDE neuroendocrine tumours
# (Gastrointestinal/Renal NET) — those are the q034/t219 exclusion, not CNS.
_CNS_RE = re.compile(
    r"gliom|glioblast|astrocyt|oligodendro|ependym|medullo|brain|cns|neuroepithelial|nerve sheath|"
    r"meningi|schwann|neuroblast",
    re.I,
)


def study_columns(df: pd.DataFrame) -> list[str]:
    out = []
    for c in df.columns:
        if c in META or c in _NONSTUDY_EXACT or c.endswith("_exclusive"):
            continue
        if c.startswith(_NONSTUDY_PREFIXES):
            continue
        out.append(c)
    return out


def cns_cancer_types(values) -> list[str]:
    """CNS labels = CNS-regex hits that are NOT neuroendocrine."""
    return sorted(
        v
        for v in pd.unique(values)
        if isinstance(v, str)
        and _CNS_RE.search(v)
        and "neuroendocrine" not in v.lower()
    )


def load_span() -> tuple[pd.Series, pd.Series]:
    """Return (genomic span bp, constitutively-late-replicating flag) per symbol."""
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
    """Is the candidate raw enrichment exceptional vs genomic-span-matched random genes (t217 residual)?

    If ``klass`` is given (a per-gene categorical, here the constitutively-late-replicating flag), each
    candidate is matched only to genes of the SAME class — so the null controls span AND replication
    timing together. If the span-only residual then dissolves, the residual was the late-replication /
    CFS axis that span alone does not capture.
    """
    idx = metric.dropna().index.intersection(span.dropna().index)
    if klass is not None:
        idx = idx.intersection(klass.dropna().index)
    if len(idx) < knn + len(gene_set):
        return {
            "observed_median_pct": np.nan,
            "null_median_pct_mean": np.nan,
            "empirical_p_le_observed": np.nan,
        }
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
    """Per-gene total mutation count over the given (row-subset, study-subset)."""
    return frame.groupby("symbol")[study_cols].sum(min_count=1).sum(axis=1)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(RANDOM_SEED)
    span, is_late_cl = load_span()

    restriction_rows: list[dict] = []
    contrib_rows: list[dict] = []
    loso_rows: list[dict] = []
    assay_rows: list[dict] = []

    for cfg, base in CONFIGS.items():
        cpath = Path(base) / "gene_cancer_study.feather"
        if not cpath.exists():
            print(f"[skip] {cfg}: {cpath} absent")
            continue
        cnt = pd.read_feather(cpath)
        cols = study_columns(cnt)

        # assay classification from genes-covered-per-study
        genes_per_study = (cnt.groupby("symbol")[cols].sum(min_count=1) > 0).sum()
        wes_cols = [c for c in cols if genes_per_study[c] >= WES_GENE_THR]
        panel_cols = [c for c in cols if genes_per_study[c] < WES_GENE_THR]
        assay_rows.append(
            {
                "config": cfg,
                "n_studies": len(cols),
                "n_wes": len(wes_cols),
                "n_panel": len(panel_cols),
                "wes_gene_thr": WES_GENE_THR,
            }
        )

        cns = cns_cancer_types(cnt["cancer_type"])
        non_cns_mask = ~cnt["cancer_type"].isin(cns)
        print(
            f"[{cfg}] {len(cols)} studies ({len(wes_cols)} WES / {len(panel_cols)} panel); "
            f"{len(cns)} CNS cancer types"
        )

        restrictions = {
            "baseline": (cnt, cols),
            "cns_excluded": (cnt[non_cns_mask], cols),
            "wes_only": (cnt, wes_cols),
            "wes_only_cns_excl": (cnt[non_cns_mask], wes_cols),
            "panel_only": (cnt, panel_cols),
        }
        # Hypermutator-excluded arm: where the aggregate carries per-study `{study}_exclusive` twins
        # (is_hypermutator-removed counts), re-run the WES residual on them. Tests whether the residual
        # is hypermutator/TMB sample-composition (long late genes accruing counts in hypermutated tumours).
        wes_excl = [
            f"{c}_exclusive" for c in wes_cols if f"{c}_exclusive" in cnt.columns
        ]
        if wes_excl:
            restrictions["wes_hypermut_excl"] = (cnt, wes_excl)
        # Driver-excluded arm: leave-one-study-out flags pog570_bcgsc_2020 as the SOLE study moving
        # candidate median > 0.1 pct. Its mutation table is all-region (t218b: ~98.5% of candidate variant
        # rows intronic), so these multi-Mb CFS loci accrue whole-gene-body counts there — an amplified form
        # of the genomic-span confound, not exonic signal. Dropping it returns candidates to the span null.
        if LOSO_DRIVER in wes_cols:
            restrictions["wes_excl_wgs_driver"] = (
                cnt,
                [c for c in wes_cols if c != LOSO_DRIVER],
            )
        for name, (frame, scols) in restrictions.items():
            if not scols:
                continue
            totals = gene_totals(frame, scols)
            e = enrichment(totals, CANDIDATES)
            sm = span_matched_p(totals, span, CANDIDATES, rng, N_NULL)
            smc = span_matched_p(
                totals, span, CANDIDATES, rng, N_NULL, klass=is_late_cl
            )
            restriction_rows.append(
                {
                    "config": cfg,
                    "restriction": name,
                    "n_studies": len(scols),
                    **e,
                    **sm,
                    "p_span_class_matched": smc["empirical_p_le_observed"],
                }
            )

        # per-candidate CNS contribution (full only, for brevity / q033 focus)
        if cfg == "full":
            for g in CANDIDATES:
                grow = cnt[cnt.symbol == g]
                tot = float(grow[cols].sum(min_count=1).sum())
                cns_tot = (
                    float(
                        grow[grow["cancer_type"].isin(cns)][cols].sum(min_count=1).sum()
                    )
                    if tot > 0
                    else 0.0
                )
                # top contributing cancer types
                by_ct = (
                    grow.set_index("cancer_type")[cols]
                    .sum(axis=1)
                    .sort_values(ascending=False)
                )
                top_ct = "; ".join(
                    f"{k}:{int(v)}" for k, v in by_ct.head(4).items() if v > 0
                )
                contrib_rows.append(
                    {
                        "gene": g,
                        "total_count": int(tot),
                        "cns_count": int(cns_tot),
                        "cns_fraction": round(cns_tot / tot, 4) if tot > 0 else np.nan,
                        "top_cancer_types": top_ct,
                    }
                )

            # leave-one-study-out on WES set: which study's removal most shifts candidate median pct?
            base_tot = gene_totals(cnt, wes_cols)
            base_med = enrichment(base_tot, CANDIDATES)["median_pct"]
            for c in wes_cols:
                tot = gene_totals(cnt, [x for x in wes_cols if x != c])
                med = enrichment(tot, CANDIDATES)["median_pct"]
                loso_rows.append(
                    {
                        "dropped_study": c,
                        "candidate_median_pct": med,
                        "delta_vs_base": round(med - base_med, 4),
                    }
                )

    restr = pd.DataFrame(restriction_rows)
    contrib = pd.DataFrame(contrib_rows)
    # sort by MAGNITUDE of shift so the most influential studies (either direction) sort first —
    # the sole large driver (pog570_bcgsc_2020) raises the median when dropped (positive delta).
    loso = pd.DataFrame(loso_rows)
    loso = loso.reindex(loso["delta_vs_base"].abs().sort_values(ascending=False).index)
    assay = pd.DataFrame(assay_rows)

    # panel-membership: which candidates are tiled by GENIE panels (mechanism evidence for ascertainment)
    panel_mem = pd.DataFrame()
    if GENIE_COV.exists():
        cov = pd.read_feather(GENIE_COV)
        inc = cov[cov["included"]] if "included" in cov.columns else cov
        n_panels = inc["panel_id"].nunique()
        cand_cov = (
            inc[inc["gene"].isin(CANDIDATES)]
            .groupby("gene")["panel_id"]
            .nunique()
            .reindex(CANDIDATES)
            .fillna(0)
            .astype(int)
        )
        panel_mem = pd.DataFrame(
            {
                "gene": cand_cov.index,
                "n_genie_panels_tiling": cand_cov.values,
                "frac_genie_panels": (cand_cov / n_panels).round(4).values,
            }
        )
        panel_mem.attrs["n_panels"] = n_panels

    # --- write artifacts ---
    restr.to_csv(OUT / "enrichment_by_restriction.tsv", sep="\t", index=False)
    contrib.to_csv(OUT / "candidate_cns_contribution.tsv", sep="\t", index=False)
    loso.to_csv(OUT / "leave_one_study_out_wes.tsv", sep="\t", index=False)
    assay.to_csv(OUT / "assay_classification.tsv", sep="\t", index=False)
    if not panel_mem.empty:
        panel_mem.to_csv(OUT / "candidate_panel_membership.tsv", sep="\t", index=False)

    datapackage = {
        "name": "neural-gene-cns-wes-2026-06-08",
        "title": "t218 CNS-exclusion + WES-restriction + panel-membership for neural enrichment",
        "description": "q033 / h12. Recomputes the candidate mutation enrichment and the t217 "
        "genomic-span-matched residual p under baseline / CNS-excluded / WES-only / WES+CNS-excluded / "
        "panel-only, to separate panel ascertainment (q016) from CNS histology as the source of the "
        "t217 residual. Plus per-candidate CNS contribution, leave-one-study-out, panel membership.",
        "created": "2026-06-08",
        "sources": [
            {"name": "gene_cancer_study", "configs": list(CONFIGS)},
            {"name": "gene_replication_timing", "path": str(REPTIMING)},
            {"name": "genie_panel_coverage", "path": str(GENIE_COV)},
        ],
        "tasks": ["t218"],
        "related": [
            "question:q033-neural-enrichment-cns-exclusion",
            "question:q016-panel-induced-ascertainment",
            "hypothesis:h12-neural-gene-enrichment-length-histology-artifact",
            "interpretation:2026-06-08-t217-genomic-span-cfs-null",
        ],
        "resources": [
            {
                "name": "enrichment_by_restriction",
                "path": "enrichment_by_restriction.tsv",
            },
            {
                "name": "candidate_cns_contribution",
                "path": "candidate_cns_contribution.tsv",
            },
            {"name": "leave_one_study_out_wes", "path": "leave_one_study_out_wes.tsv"},
            {"name": "assay_classification", "path": "assay_classification.tsv"},
            {
                "name": "candidate_panel_membership",
                "path": "candidate_panel_membership.tsv",
            },
            {
                "name": "pog570_driver_forensics",
                "path": "pog570_*.{tsv,json}",
                "note": "variant-class + hypermutator forensic on the sole LOSO driver; "
                "written by code/notebooks/t218b_pog570_driver_forensics.py",
            },
        ],
        "parameters": {
            "random_seed": RANDOM_SEED,
            "n_null_draws": N_NULL,
            "wes_gene_threshold": WES_GENE_THR,
            "candidates": CANDIDATES,
            "assay_rule": "study is WES/WGS if it reports mutations across >= wes_gene_threshold distinct "
            "genes, else panel/limited (panel_callable_mb is defaulted to 30 Mb here and cannot classify).",
            "cns_definition": "regex on cancer_type for CNS/glioma histologies, EXCLUDING neuroendocrine "
            "(left to t219/q034).",
        },
    }
    (OUT / "datapackage.json").write_text(json.dumps(datapackage, indent=2))

    # --- console summary ---
    pd.set_option("display.width", 230, "display.max_columns", 40)
    print("\n================ ASSAY CLASSIFICATION ================")
    print(assay.to_string(index=False))
    print(
        "\n================ CANDIDATE ENRICHMENT + t217 SPAN-MATCHED RESIDUAL BY RESTRICTION ================"
    )
    print(
        "  (empirical_p_le_observed: LARGE => span fully explains it / residual gone; small => residual remains)"
    )
    print(
        restr[
            [
                "config",
                "restriction",
                "n_studies",
                "median_pct",
                "n_in_top100",
                "observed_median_pct",
                "null_median_pct_mean",
                "empirical_p_le_observed",
                "p_span_class_matched",
            ]
        ].to_string(index=False)
    )
    print(
        "  empirical_p_le_observed = span-matched (t217); p_span_class_matched = span + late-replication matched"
    )
    print("\n================ PER-CANDIDATE CNS CONTRIBUTION (full) ================")
    print(contrib.to_string(index=False))
    print(
        "\n========== LEAVE-ONE-STUDY-OUT (WES, full) — 6 most influential by |delta| =========="
    )
    print(loso.head(6).to_string(index=False))
    n_big = int((loso["delta_vs_base"].abs() > 0.1).sum())
    print(
        f"   ({n_big} of {len(loso)} WES studies shift candidate median by > 0.1 pct; "
        f"max |delta| = {loso['delta_vs_base'].abs().max():.3f} pct points)"
    )
    if not panel_mem.empty:
        print(
            f"\n================ CANDIDATE GENIE-PANEL MEMBERSHIP (of {panel_mem.attrs['n_panels']} panels) ================"
        )
        print(panel_mem.to_string(index=False))
    print(f"\nArtifacts written to {OUT}/")


if __name__ == "__main__":
    main()
