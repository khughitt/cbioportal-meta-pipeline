"""q047 — hypermutation as a confound on driver tissue-specificity (poc-2026-04-17 cohort).

Question: q047-hypermutation-confound-on-driver-tissue-specificity.

Tests, at PER-SAMPLE resolution, whether hypermutated tumors (MMR/MSI, POLE/POLD1) dilute the
restricted-lineage-oncogene signal and inflate breadth via passenger recurrence — which would
confound q042 (restricted-oncogene specificity) and q043 (breadth distribution).

Three tests, all stratified WITHIN cancer type (hypermutators concentrate in CRC/UCEC/melanoma):
  T1  Mutational load: drivers vs background genes per sample, hyper vs non-hyper.
  T2  Driver share of load: fraction of a sample's mutated genes that are CGC drivers — expected to
      DROP in hypermutators (passenger dilution).
  T3  Per-gene prevalence ratio (hyper/non-hyper) by gene class — background/passenger genes should
      inflate MORE than restricted lineage oncogenes (the dilution-of-selection signal).

Class definitions reuse q043 breadth (oncogene-only, three bands): restricted_oncogene = breadth<=2;
mid_oncogene = 3..9; broad_oncogene = breadth>=10. Plus tsg / oncogene_and_tsg / cgc_other by CGC
role; background = non-CGC panel genes.

Run:  uv run --frozen python code/notebooks/q047_hypermutation_specificity_confound.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path("results/poc-2026-04-17")
OUT = BASE / "analysis" / "q047"
OUT.mkdir(parents=True, exist_ok=True)

STUDIES = [
    "ucec_tcga_pan_can_atlas_2018",
    "skcm_tcga_pan_can_atlas_2018",
    "brca_tcga_pan_can_atlas_2018",
    "msk_impact_2017",
]
PANEL_STUDY = "msk_impact_2017"
SYNONYMOUS = {"Silent", "synonymous_variant", "Synonymous"}
MIN_HYPER = 15  # cancer types need at least this many hypermutators to be tested
MIN_NONHYPER = 30
RESTRICTED_BREADTH = 2  # oncogene breadth <= this -> restricted
BROAD_BREADTH = 10  # oncogene breadth >= this -> broad; in between -> mid


def load_roster_with_breadth() -> pd.DataFrame:
    cgc = pd.read_csv("data/cosmic_cgc.tsv", sep="\t")
    role = cgc["Role in Cancer"].fillna("").str.lower()
    r = pd.DataFrame(
        {
            "symbol": cgc["Gene Symbol"],
            "is_oncogene": role.str.contains("oncogene"),
            "is_tsg": role.str.contains("tsg"),
        }
    ).set_index("symbol")
    breadth = pd.read_feather(
        BASE / "analysis/q043/breadth_inclusive_2pct.feather"
    ).set_index("symbol")
    r = r.join(breadth, how="left")
    r["breadth"] = r["breadth"].fillna(0)

    def cls(row):
        if row.is_oncogene and not row.is_tsg:
            if row.breadth <= RESTRICTED_BREADTH:
                return "restricted_oncogene"
            if row.breadth >= BROAD_BREADTH:
                return "broad_oncogene"
            return "mid_oncogene"
        if row.is_tsg and not row.is_oncogene:
            return "tsg"
        if row.is_oncogene and row.is_tsg:
            return "oncogene_and_tsg"
        return "cgc_other"

    r["q047_class"] = r.apply(cls, axis=1)
    return r


def load_panel_genes() -> set[str]:
    g = pd.read_feather(BASE / "summary/mut/table/gene_cancer_study.feather")
    return set(g.loc[g[PANEL_STUDY].fillna(0) > 0, "symbol"].unique())


def load_sample_mutations(samples: pd.DataFrame) -> pd.DataFrame:
    """Long (sample_id, symbol) coding-nonsynonymous calls across all studies, joined to sample meta."""
    frames = []
    for s in STUDIES:
        m = pd.read_feather(BASE / f"studies/{s}/mut/table/mut_filtered.feather")
        m = m[~m["variant_class"].isin(SYNONYMOUS)]
        m = m.rename(columns={"sample_id_tumor": "sample_id"})[["sample_id", "symbol"]]
        frames.append(m)
    muts = pd.concat(frames, ignore_index=True).drop_duplicates(["sample_id", "symbol"])
    meta = samples.set_index("sample_id")[
        ["cancer_type", "is_hypermutator", "hypermutator_reason"]
    ]
    muts = muts.join(meta, on="sample_id")
    matched = muts["cancer_type"].notna().mean()
    print(
        f"  per-sample mutation rows: {len(muts)} | sample-meta join coverage: {matched:.1%}"
    )
    return muts[muts["cancer_type"].notna()].copy()


def testable_cancer_types(samples: pd.DataFrame) -> list[str]:
    g = samples.groupby("cancer_type")["is_hypermutator"]
    n_hyper = g.sum()
    n_non = g.count() - n_hyper
    keep = (n_hyper >= MIN_HYPER) & (n_non >= MIN_NONHYPER)
    types = sorted(keep[keep].index)
    print(
        f"  testable cancer types (>= {MIN_HYPER} hyper & {MIN_NONHYPER} non-hyper): {types}"
    )
    return types


def main() -> None:
    samples = pd.read_feather(BASE / "metadata/samples_annotated.feather")
    samples["is_hypermutator"] = samples["is_hypermutator"].fillna(False)
    roster = load_roster_with_breadth()
    panel = load_panel_genes()

    print("=" * 78)
    print(
        "q047 — hypermutation as a driver-specificity confound | cohort: poc-2026-04-17"
    )
    print(
        f"hypermutators: {int(samples['is_hypermutator'].sum())} / {len(samples)} "
        f"({samples['is_hypermutator'].mean():.1%})"
    )
    muts = load_sample_mutations(samples)
    types = testable_cancer_types(samples)

    cls_of = roster["q047_class"]

    def gene_class(sym: str) -> str:
        if sym in cls_of.index:
            return (
                cls_of.loc[sym]
                if isinstance(cls_of.loc[sym], str)
                else cls_of.loc[sym].iloc[0]
            )
        return "background" if sym in panel else "off_panel"

    muts["q047_class"] = muts["symbol"].map(gene_class)
    muts_panel = muts[muts["q047_class"] != "off_panel"]

    # ---- T1 + T2: per-sample load and driver share, within cancer type ----
    # Build from the AUTHORITATIVE sample list (testable types) so samples with ZERO panel
    # nonsynonymous mutations are included as total=0, not silently dropped (sample_id is unique
    # in samples_annotated).
    print(f"\n{'=' * 28} T1/T2: per-sample load & driver share {'=' * 12}")
    class_counts = (
        muts_panel.groupby(["sample_id", "q047_class"])
        .size()
        .unstack("q047_class", fill_value=0)
    )
    class_cols = list(class_counts.columns)
    base = samples.loc[
        samples["cancer_type"].isin(types),
        ["sample_id", "cancer_type", "is_hypermutator"],
    ]
    ps = base.merge(class_counts, on="sample_id", how="left")
    ps[class_cols] = ps[class_cols].fillna(0)
    ps["total"] = ps[class_cols].sum(axis=1)
    driver_cols = [
        c
        for c in [
            "restricted_oncogene",
            "mid_oncogene",
            "broad_oncogene",
            "tsg",
            "oncogene_and_tsg",
            "cgc_other",
        ]
        if c in class_cols
    ]
    ps["driver_total"] = ps[driver_cols].sum(axis=1)
    ps["driver_share"] = ps["driver_total"] / ps["total"].replace(0, np.nan)
    summ = (
        ps.groupby(["cancer_type", "is_hypermutator"])
        .agg(
            n=("sample_id", "size"),
            med_total=("total", "median"),
            med_driver=("driver_total", "median"),
            med_driver_share=("driver_share", "median"),
        )
        .round(3)
    )
    print(summ.to_string())

    # ---- T3: per-gene prevalence ratio (hyper/non-hyper) by class, within cancer type ----
    print(f"\n{'=' * 28} T3: prevalence inflation by class {'=' * 14}")
    rows = []
    n_by = samples.groupby(["cancer_type", "is_hypermutator"]).size()
    for ct in types:
        for hyper in (True, False):
            denom = n_by.get((ct, hyper), 0)
            if denom == 0:
                continue
            sub = muts_panel[
                (muts_panel.cancer_type == ct) & (muts_panel.is_hypermutator == hyper)
            ]
            prev = sub.groupby("symbol").size() / denom
            for sym, p in prev.items():
                rows.append((ct, sym, hyper, p))
    pv = pd.DataFrame(rows, columns=["cancer_type", "symbol", "is_hyper", "prev"])
    wide = pv.pivot_table(
        index=["cancer_type", "symbol"], columns="is_hyper", values="prev"
    ).dropna()
    wide.columns = ["prev_non", "prev_hyper"]
    wide = wide[
        (wide.prev_non >= 0.02) | (wide.prev_hyper >= 0.02)
    ]  # focus on genes recurrent in either
    wide["log2_ratio"] = np.log2((wide.prev_hyper + 1e-3) / (wide.prev_non + 1e-3))
    wide["q047_class"] = wide.index.get_level_values("symbol").map(gene_class)
    by_class = (
        wide.groupby("q047_class")["log2_ratio"].agg(["median", "count"]).round(3)
    )
    print(
        "  median log2(prev_hyper / prev_non) by gene class (higher = more inflated by hypermutation):"
    )
    print(by_class.to_string().replace("\n", "\n    "))
    print(
        "\n  CAUTION: this raw log-ratio is BASELINE-CONFOUNDED and does NOT isolate passenger "
        "dilution. Already-common genes (broad oncogenes) have a compressed ratio (ceiling); rare "
        "genes (restricted oncogenes, background) yield mechanically large ratios from a near-zero "
        "baseline — so restricted_oncogene scoring high here is an artifact, not dilution. The one "
        "robust read: broad_oncogene (the q043 hubs) is the most STABLE class under hypermutation. "
        "A baseline-prevalence-matched metric is required (see the q047 entity)."
    )

    wide.reset_index().to_feather(OUT / "prevalence_ratio_by_gene.feather")
    print(f"\nartifacts -> {OUT}")


if __name__ == "__main__":
    main()
