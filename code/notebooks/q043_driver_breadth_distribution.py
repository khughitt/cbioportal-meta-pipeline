"""q043 — driver cancer-type-breadth distribution (first pass on the poc-2026-04-17 cohort).

Question: q043-driver-cancer-type-breadth-distribution.

Measures, in our own aggregated cohort, the distribution of how many distinct cancer types each
driver recurs in, and compares it to IntOGen's restricted-vs-pan-cancer split (Martinez-Jimenez
2020: 360/568 = 63% restricted to 1-2 tumor types; 12 cancer-wide).

Design decisions baked in (from the q043 entity):
- Breadth is counted from the RAW, un-broadcast ``gene_cancer_study.feather`` (per-study counts),
  NEVER the ``bailey2018_driver`` flag (which ORs PANCAN drivers into every cancer row).
- Cross-cancer breadth is only interpretable for genes assayed across all cancer types. In this
  cohort only MSK-IMPACT spans the 57 types, so the breadth distribution is computed on the
  PANEL-COVERED gene set (the honest ascertainment control, q016) and reported separately from the
  naive all-gene view.
- Recurrence threshold is swept (1/2/5 %); breadth is reported per COSMIC role (OG vs TSG).
- Inclusive vs hypermutator-exclusive breadth delta is reported as a teaser for q047.

Run:  uv run --frozen python code/notebooks/q043_driver_breadth_distribution.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

BASE = Path("results/poc-2026-04-17")
OUT = BASE / "analysis" / "q043"
OUT.mkdir(parents=True, exist_ok=True)

STUDIES = [
    "ucec_tcga_pan_can_atlas_2018",
    "skcm_tcga_pan_can_atlas_2018",
    "brca_tcga_pan_can_atlas_2018",
    "msk_impact_2017",
]
# the single study that spans all cancer types -> defines the panel-covered gene set
PANEL_STUDY = "msk_impact_2017"

# IntOGen cancer-wide drivers (Martinez-Jimenez 2020), hard-coded from q042 for the cross-check
INTOGEN_CANCER_WIDE = {
    "TP53",
    "KRAS",
    "PIK3CA",
    "PTEN",
    "KMT2D",
    "KMT2C",
    "LRP1B",
    "ARID1A",
    "RB1",
    "FAT4",
    "NF1",
    "CDKN2A",
}

MIN_CANCER_N = 25  # ignore cancer types with too few samples to define a frequency
THRESHOLDS = [0.01, 0.02, 0.05]


def load_roster() -> pd.DataFrame:
    """COSMIC CGC role table -> per-gene oncogene/TSG/fusion class flags."""
    cgc = pd.read_csv("data/cosmic_cgc.tsv", sep="\t")
    role = cgc["Role in Cancer"].fillna("").str.lower()
    out = pd.DataFrame(
        {
            "symbol": cgc["Gene Symbol"],
            "tier": cgc["Tier"],
            "is_oncogene": role.str.contains("oncogene"),
            "is_tsg": role.str.contains("tsg"),
            "is_fusion": role.str.contains("fusion"),
        }
    )

    def cls(r):
        if r.is_oncogene and r.is_tsg:
            return "oncogene_and_tsg"
        if r.is_oncogene:
            return "oncogene"
        if r.is_tsg:
            return "tsg"
        if r.is_fusion:
            return "fusion_only"
        return "other"

    out["cgc_class"] = out.apply(cls, axis=1)
    return out


def load_bailey() -> pd.DataFrame:
    """Bailey 2018 per-cancer roster; PANCAN rows kept separate (NOT broadcast)."""
    b = pd.read_csv("data/bailey2018_table_s1.tsv", sep="\t")
    b["is_pancan"] = b["Cancer"].str.upper() == "PANCAN"
    return b


def per_cancer_counts(exclusive: bool) -> pd.DataFrame:
    """Raw per-(cancer_type, symbol) mutated-sample count, summed across studies."""
    g = pd.read_feather(BASE / "summary/mut/table/gene_cancer_study.feather")
    suffix = "_exclusive" if exclusive else ""
    cols = [f"{s}{suffix}" for s in STUDIES]
    g["mutated_count"] = g[cols].sum(axis=1, min_count=1)
    # panel-covered genes: any nonzero count in the pan-cancer panel study
    panel_genes = set(
        g.loc[g[f"{PANEL_STUDY}{suffix}"].fillna(0) > 0, "symbol"].unique()
    )
    return g[["cancer_type", "symbol", "mutated_count"]].copy(), panel_genes


def cancer_sample_counts(samples: pd.DataFrame, exclusive: bool) -> pd.Series:
    s = samples if not exclusive else samples[~samples["is_hypermutator"].fillna(False)]
    return s.groupby("cancer_type").size()


def breadth_table(
    counts: pd.DataFrame, n_by_cancer: pd.Series, thresh: float
) -> pd.Series:
    df = counts.copy()
    df["n_cancer"] = df["cancer_type"].map(n_by_cancer)
    df = df[df["n_cancer"] >= MIN_CANCER_N]
    df["freq"] = df["mutated_count"] / df["n_cancer"]
    recurrent = df[(df["freq"] >= thresh) & (df["mutated_count"] >= 3)]
    return recurrent.groupby("symbol")["cancer_type"].nunique()  # breadth per gene


def summarize(breadth: pd.Series, roster: pd.DataFrame, label: str) -> None:
    drivers = roster.set_index("symbol")
    b = breadth.to_frame("breadth").join(drivers[["cgc_class"]], how="left")
    b["cgc_class"] = b["cgc_class"].fillna("non_cgc")
    is_driver = b["cgc_class"].isin(["oncogene", "tsg", "oncogene_and_tsg"])
    drv = b[is_driver]
    print(
        f"\n--- {label} | genes recurrent in >=1 type: {len(b)} (drivers: {len(drv)}) ---"
    )
    if len(drv) == 0:
        return
    restricted = (drv["breadth"] <= 2).mean()
    print(f"  drivers restricted to 1-2 types: {restricted:.1%}  (IntOGen ref: 63%)")
    print(
        f"  driver breadth: median={drv['breadth'].median():.0f} max={drv['breadth'].max():.0f}"
    )
    # the cancer-wide hub set (top of the tail)
    hubs = drv.sort_values("breadth", ascending=False).head(15)
    print("  top-15 broadest drivers:")
    for sym, row in hubs.iterrows():
        tag = " [IntOGen-cancer-wide]" if sym in INTOGEN_CANCER_WIDE else ""
        print(f"    {sym:8s} breadth={int(row['breadth']):3d}  {row['cgc_class']}{tag}")
    # OG vs TSG breadth contrast
    print("  median breadth by class:")
    print(
        drv.groupby("cgc_class")["breadth"]
        .agg(["median", "count"])
        .to_string()
        .replace("\n", "\n    ")
    )
    # IntOGen-12 recovery
    found = [g for g in INTOGEN_CANCER_WIDE if g in drv.index]
    if found:
        sub = drv.loc[found, "breadth"].sort_values(ascending=False)
        print(
            f"  IntOGen-12 cancer-wide present here: {len(found)}/12, breadth "
            f"median={sub.median():.0f} min={sub.min():.0f}"
        )


def main() -> None:
    roster = load_roster()
    bailey = load_bailey()
    samples = pd.read_feather(BASE / "metadata/samples_annotated.feather")

    print("=" * 78)
    print("q043 — driver cancer-type-breadth distribution | cohort: poc-2026-04-17")
    print(
        f"cancer types (samples): {samples['cancer_type'].nunique()} | samples: {len(samples)}"
    )
    print(
        f"CGC genes: {len(roster)} | Bailey rows: {len(bailey)} "
        f"(PANCAN: {bailey['is_pancan'].sum()}, specific: {(~bailey['is_pancan']).sum()})"
    )

    # Bailey external cross-check: roster breadth with PANCAN EXCLUDED
    spec = bailey[~bailey["is_pancan"]]
    bailey_breadth = spec.groupby("Gene")["Cancer"].nunique()
    pancan_only = set(bailey.loc[bailey["is_pancan"], "Gene"]) - set(spec["Gene"])
    print(
        f"\n[Bailey roster, PANCAN excluded] genes with >=1 specific-cancer call: {len(bailey_breadth)}"
    )
    print(f"  restricted to 1-2 cancers: {(bailey_breadth <= 2).mean():.1%}")
    print(
        f"  genes appearing ONLY as PANCAN (would be lost if PANCAN-encoded only): {len(pancan_only)}"
    )
    print(
        f"  broadest Bailey genes: "
        f"{bailey_breadth.sort_values(ascending=False).head(8).to_dict()}"
    )

    # Empirical breadth in our cohort, panel-covered genes, swept threshold
    for exclusive in (False, True):
        counts, panel_genes = per_cancer_counts(exclusive=exclusive)
        n_by_cancer = cancer_sample_counts(samples, exclusive=exclusive)
        counts = counts[counts["symbol"].isin(panel_genes)]
        tag = "HYPERMUTATOR-EXCLUSIVE" if exclusive else "inclusive"
        print(
            f"\n{'=' * 30} {tag} | panel-covered genes: {len(panel_genes)} {'=' * 10}"
        )
        for th in THRESHOLDS:
            breadth = breadth_table(counts, n_by_cancer, th)
            summarize(breadth, roster, f"thresh={th:.0%}")
            if not exclusive and th == 0.02:
                breadth.rename("breadth").reset_index().to_feather(
                    OUT / "breadth_inclusive_2pct.feather"
                )

    # inclusive vs exclusive breadth delta (q047 teaser) at 2%
    inc_counts, panel = per_cancer_counts(False)
    exc_counts, _ = per_cancer_counts(True)
    inc_b = breadth_table(
        inc_counts[inc_counts.symbol.isin(panel)],
        cancer_sample_counts(samples, False),
        0.02,
    )
    exc_b = breadth_table(
        exc_counts[exc_counts.symbol.isin(panel)],
        cancer_sample_counts(samples, True),
        0.02,
    )
    delta = (inc_b - exc_b.reindex(inc_b.index).fillna(0)).sort_values(ascending=False)
    drv_delta = delta[
        delta.index.isin(
            roster.loc[
                roster.cgc_class.isin(["oncogene", "tsg", "oncogene_and_tsg"]), "symbol"
            ]
        )
    ]
    print(
        f"\n{'=' * 20} q047 teaser: breadth inflation by hypermutators (2%) {'=' * 10}"
    )
    print(
        f"  genes losing >=1 cancer-type of breadth when hypermutators excluded: "
        f"{(delta > 0).sum()} (drivers: {(drv_delta > 0).sum()})"
    )
    print(f"  largest driver breadth drops: {drv_delta.head(10).astype(int).to_dict()}")
    print(f"\nartifacts -> {OUT}")


if __name__ == "__main__":
    main()
