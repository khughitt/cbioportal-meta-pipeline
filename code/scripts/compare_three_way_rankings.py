# science:code
# status: workflow-owned
# science:end
#
# compare_three_way_rankings.py (t131)
#
# Build a per-gene three-way ranking comparison feather joining:
#   1. Raw mutation frequency           (mean_inclusive, pan-cancer mean)
#   2. Length-adjusted frequency        (mean_adj = mean_inclusive / protein_length)
#   3. dNdScv selection-based ranking   (min_qglobal across cancer types from
#                                        summary/mut/table/dndscv_pooled.feather)
#
from __future__ import annotations

import math

import pandas as pd

from symbol_normalization import driver_overlay_symbol


def build_three_way_comparison(
    annotated: pd.DataFrame,
    pooled: pd.DataFrame,
    lengths: pd.DataFrame,
    *,
    pubtator: pd.DataFrame | None = None,
    ensembl: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Build the per-gene three-way comparison table."""
    per_gene = _per_gene_rollup(annotated)
    per_gene = per_gene[per_gene["mean_inclusive"] > 0].copy()
    print(f"compare_three_way_rankings: {len(per_gene):,} genes with mean_inclusive>0")

    lengths = lengths.copy()
    lengths["symbol"] = lengths["symbol"].astype(str)
    per_gene = per_gene.merge(lengths, on="symbol", how="left")

    pooled_prepared = pooled.copy()
    pooled_prepared["symbol"] = pooled_prepared["symbol"].astype(str)
    per_gene = per_gene.merge(
        pooled_prepared[
            [
                "symbol",
                "min_qglobal",
                "n_cancers_significant_q05",
                "best_cancer_type",
            ]
        ],
        on="symbol",
        how="outer",
    )
    per_gene = _attach_overlay_flags(per_gene, annotated)

    per_gene = _join_pubtator(per_gene, pubtator=pubtator, ensembl=ensembl)
    per_gene = _add_rank_columns(per_gene)
    return _finalize_columns(per_gene)


def _per_gene_rollup(annot: pd.DataFrame) -> pd.DataFrame:
    """Aggregate annotated feather (per (gene, cancer_type)) to per-gene."""
    annot = annot.copy()
    annot["symbol"] = annot["symbol"].astype(str)
    out = annot.groupby("symbol").agg(
        mean_inclusive=("mean_inclusive", "mean"),
        mean_adj=("mean_adj", "mean"),
        n_cancers=("cancer_type", "nunique"),
    )
    return out.reset_index()


def _attach_overlay_flags(per_gene: pd.DataFrame, annot: pd.DataFrame) -> pd.DataFrame:
    out = per_gene.copy()
    out["symbol"] = out["symbol"].astype(str)
    out["_driver_overlay_symbol"] = out["symbol"].map(driver_overlay_symbol)
    overlay = _overlay_flags_by_symbol(annot)
    out = out.merge(overlay, on="_driver_overlay_symbol", how="left")
    for col in ("bailey_driver", "cgc_tier_1", "ch_priority_gene"):
        if col in out.columns:
            out[col] = out[col].fillna(False).astype(bool)
    return out.drop(columns=["_driver_overlay_symbol"])


def _overlay_flags_by_symbol(annot: pd.DataFrame) -> pd.DataFrame:
    annot = annot.copy()
    annot["symbol"] = annot["symbol"].astype(str)
    annot["_driver_overlay_symbol"] = annot["symbol"].map(driver_overlay_symbol)
    specs = {
        "bailey2018_driver": "bailey_driver",
        "cgc_tier_1": "cgc_tier_1",
        "ch_priority_gene": "ch_priority_gene",
    }
    rows = pd.DataFrame(
        {"_driver_overlay_symbol": sorted(set(annot["_driver_overlay_symbol"]))}
    )
    for input_col, output_col in specs.items():
        if input_col in annot.columns:
            flags = (
                annot.groupby("_driver_overlay_symbol")[input_col]
                .max()
                .rename(output_col)
            )
            rows = rows.merge(flags, on="_driver_overlay_symbol", how="left")
    return rows


def _join_pubtator(
    per_gene: pd.DataFrame,
    *,
    pubtator: pd.DataFrame | None,
    ensembl: pd.DataFrame | None,
) -> pd.DataFrame:
    if pubtator is None or ensembl is None:
        out = per_gene.copy()
        out["pubtator_mention_count"] = pd.NA
        out["pubtator_log10_mentions"] = pd.NA
        return out

    ens = ensembl.dropna(subset=["entrez", "symbol"]).drop_duplicates().copy()
    ens["entrez"] = ens["entrez"].astype("Int64").astype(str)
    ens["symbol"] = ens["symbol"].astype(str)
    pub = pubtator.copy()
    pub["concept_id"] = pub["concept_id"].astype(str)
    pub_per_symbol = (
        pub.merge(ens, left_on="concept_id", right_on="entrez", how="inner")
        .groupby("symbol", as_index=False)["n"]
        .sum()
        .rename(columns={"n": "pubtator_mention_count"})
    )
    out = per_gene.merge(pub_per_symbol, on="symbol", how="left")
    out["pubtator_log10_mentions"] = out["pubtator_mention_count"].apply(
        lambda value: (
            math.log10(float(value) + 1.0) if pd.notna(value) else float("nan")
        )
    )
    n_pub = int(out["pubtator_mention_count"].notna().sum())
    print(
        f"compare_three_way_rankings: PubTator joined; {n_pub:,} / {len(out):,} "
        "genes with mention counts"
    )
    return out


def _add_rank_columns(per_gene: pd.DataFrame) -> pd.DataFrame:
    out = per_gene.copy()
    out["rank_raw"] = (
        out["mean_inclusive"]
        .rank(method="dense", ascending=False, na_option="bottom")
        .astype("Int64")
    )
    out["rank_length_adj"] = (
        out["mean_adj"]
        .rank(method="dense", ascending=False, na_option="bottom")
        .astype("Int64")
    )
    dndscv_sorted = out[["min_qglobal", "n_cancers_significant_q05"]].sort_values(
        by=["min_qglobal", "n_cancers_significant_q05"],
        ascending=[True, False],
        na_position="last",
        kind="mergesort",
    )
    dndscv_ranks = (
        dndscv_sorted.groupby(
            ["min_qglobal", "n_cancers_significant_q05"],
            dropna=False,
            sort=False,
        ).ngroup()
        + 1
    )
    out["rank_dndscv"] = dndscv_ranks.reindex(out.index).astype("Int64")
    out["shift_raw_to_length"] = out["rank_length_adj"] - out["rank_raw"]
    out["shift_raw_to_dndscv"] = out["rank_dndscv"] - out["rank_raw"]
    out["shift_length_to_dndscv"] = out["rank_dndscv"] - out["rank_length_adj"]
    return out


def _finalize_columns(per_gene: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "symbol",
        "length",
        "mean_inclusive",
        "mean_adj",
        "min_qglobal",
        "n_cancers_significant_q05",
        "best_cancer_type",
        "pubtator_mention_count",
        "pubtator_log10_mentions",
        "rank_raw",
        "rank_length_adj",
        "rank_dndscv",
        "shift_raw_to_length",
        "shift_raw_to_dndscv",
        "shift_length_to_dndscv",
    ]
    for opt in ("bailey_driver", "cgc_tier_1", "ch_priority_gene"):
        if opt in per_gene.columns:
            cols.append(opt)
    return per_gene[cols].reset_index(drop=True)


def _run_via_snakemake() -> None:
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821
    annotated = pd.read_feather(snek.input.annotated)
    pooled = pd.read_feather(snek.input.pooled)
    lengths = pd.read_feather(snek.input.lengths)

    pubtator_path = getattr(snek.input, "pubtator", None)
    ensembl_path = getattr(snek.input, "ensembl", None)
    pubtator = None
    ensembl = None
    if pubtator_path and ensembl_path:
        try:
            pubtator = pd.read_feather(pubtator_path)
            ensembl = pd.read_csv(ensembl_path, sep="\t", usecols=["entrez", "symbol"])
        except FileNotFoundError as error:
            print(
                f"compare_three_way_rankings: PubTator path missing ({error}); skipping join"
            )

    out = build_three_way_comparison(
        annotated=annotated,
        pooled=pooled,
        lengths=lengths,
        pubtator=pubtator,
        ensembl=ensembl,
    )
    out.to_feather(snek.output[0])
    print(
        f"compare_three_way_rankings: wrote {len(out):,} rows to {snek.output[0]}\n"
        f"  - {int(out['min_qglobal'].notna().sum()):,} with dndscv signal\n"
        f"  - {int(out['pubtator_mention_count'].notna().sum()):,} with PubTator counts"
    )


if "snakemake" in globals():
    _run_via_snakemake()
