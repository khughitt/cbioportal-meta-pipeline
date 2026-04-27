#
# compare_three_way_rankings.py (t131)
#
# Build a per-gene three-way ranking comparison feather joining:
#   1. Raw mutation frequency           (mean_inclusive, pan-cancer mean)
#   2. Length-adjusted frequency        (mean_adj = mean_inclusive / protein_length)
#   3. dNdScv selection-based ranking   (min_qglobal across cancer types from
#                                        summary/mut/table/dndscv_pooled.feather)
#
# PLUS literature-attention (PubTator gene-mention counts) for the q011
# correlation panel.
#
# Inputs (snek.input):
#   annotated   — summary/mut/table/gene_cancer_study_ratio_annotated_dndscv.feather
#                 (post-join_dndscv_into_annotated; carries dndscv columns)
#   pooled      — summary/mut/table/dndscv_pooled.feather
#   lengths     — metadata/protein_lengths.feather
#   ensembl     — data/grch37.tsv (entrez↔symbol mapping for PubTator join)
#   pubtator    — /data/proj/lit-explore/pubtator/2026-01-16/counts/gene_concept_ids.feather
#                 OPTIONAL — handled gracefully if absent. Wired via Snakefile
#                 with conditional input (the path is constant; if the file
#                 doesn't exist the rule's `input` declaration must be guarded
#                 by config or removed for environments without /data/proj).
#
# Output (snek.output[0]):
#   summary/mut/table/three_way_ranking_comparison.feather
#
# Output schema (per-gene):
#   symbol, length, mean_inclusive, mean_adj, min_qglobal,
#   n_cancers_significant_q05, best_cancer_type,
#   pubtator_mention_count, pubtator_log10_mentions,
#   rank_raw, rank_length_adj, rank_dndscv,
#   shift_raw_to_length, shift_raw_to_dndscv, shift_length_to_dndscv,
#   bailey_driver, cgc_tier_1, ch_priority_gene
#
import math

import pandas as pd

snek = snakemake  # type: ignore[name-defined]  # noqa: F821


def _per_gene_rollup(annot: pd.DataFrame) -> pd.DataFrame:
    """Aggregate annotated feather (per (gene, cancer_type)) → per-gene."""
    annot = annot.copy()
    annot["symbol"] = annot["symbol"].astype(str)
    bailey = (
        annot.groupby("symbol")["bailey2018_driver"].max()
        if "bailey2018_driver" in annot.columns
        else pd.Series(dtype="boolean")
    )
    cgc = (
        annot.groupby("symbol")["cgc_tier_1"].max()
        if "cgc_tier_1" in annot.columns
        else pd.Series(dtype="boolean")
    )
    ch = (
        annot.groupby("symbol")["ch_priority_gene"].max()
        if "ch_priority_gene" in annot.columns
        else pd.Series(dtype="boolean")
    )
    out = annot.groupby("symbol").agg(
        mean_inclusive=("mean_inclusive", "mean"),
        mean_adj=("mean_adj", "mean"),
        n_cancers=("cancer_type", "nunique"),
    )
    if not bailey.empty:
        out["bailey_driver"] = bailey
    if not cgc.empty:
        out["cgc_tier_1"] = cgc
    if not ch.empty:
        out["ch_priority_gene"] = ch
    return out.reset_index()


# ---------------------------------------------------------------------------
# Load inputs.
# ---------------------------------------------------------------------------
annot = pd.read_feather(snek.input.annotated)
pooled = pd.read_feather(snek.input.pooled)
lengths = pd.read_feather(snek.input.lengths)

# ---------------------------------------------------------------------------
# Per-gene rollup of annotated feather.
# ---------------------------------------------------------------------------
per_gene = _per_gene_rollup(annot)
per_gene = per_gene[per_gene["mean_inclusive"] > 0].copy()
print(f"compare_three_way_rankings: {len(per_gene):,} genes with mean_inclusive>0")

# Join lengths.
lengths = lengths.copy()
lengths["symbol"] = lengths["symbol"].astype(str)
per_gene = per_gene.merge(lengths, on="symbol", how="left")

# Join pooled dndscv signal (per-gene).
pooled = pooled.copy()
pooled["symbol"] = pooled["symbol"].astype(str)
per_gene = per_gene.merge(
    pooled[["symbol", "min_qglobal", "n_cancers_significant_q05", "best_cancer_type"]],
    on="symbol",
    how="left",
)

# ---------------------------------------------------------------------------
# PubTator join (optional).
# ---------------------------------------------------------------------------
pubtator_path = getattr(snek.input, "pubtator", None)
ensembl_path = getattr(snek.input, "ensembl", None)
if pubtator_path and ensembl_path:
    try:
        pub = pd.read_feather(pubtator_path)
        ens = pd.read_csv(
            ensembl_path,
            sep="\t",
            usecols=["entrez", "symbol"],
        )
        ens = ens.dropna(subset=["entrez", "symbol"]).drop_duplicates()
        ens["entrez"] = ens["entrez"].astype("Int64").astype(str)
        ens["symbol"] = ens["symbol"].astype(str)
        pub = pub.copy()
        pub["concept_id"] = pub["concept_id"].astype(str)
        # Sum mentions per HGNC symbol across all entrez IDs that map to it.
        pub_per_symbol = (
            pub.merge(ens, left_on="concept_id", right_on="entrez", how="inner")
            .groupby("symbol", as_index=False)["n"]
            .sum()
            .rename(columns={"n": "pubtator_mention_count"})
        )
        per_gene = per_gene.merge(pub_per_symbol, on="symbol", how="left")
        per_gene["pubtator_log10_mentions"] = per_gene["pubtator_mention_count"].apply(
            lambda v: math.log10(float(v) + 1.0) if pd.notna(v) else float("nan")
        )
        n_pub = int(per_gene["pubtator_mention_count"].notna().sum())
        print(
            f"compare_three_way_rankings: PubTator joined; {n_pub:,} / {len(per_gene):,} "
            "genes with mention counts"
        )
    except FileNotFoundError as e:
        print(f"compare_three_way_rankings: PubTator path missing ({e}); skipping join")
        per_gene["pubtator_mention_count"] = pd.NA
        per_gene["pubtator_log10_mentions"] = pd.NA
else:
    per_gene["pubtator_mention_count"] = pd.NA
    per_gene["pubtator_log10_mentions"] = pd.NA

# ---------------------------------------------------------------------------
# Compute three rank columns.
#   rank_raw            descending in mean_inclusive
#   rank_length_adj     descending in mean_adj
#   rank_dndscv         ascending in min_qglobal (lower q = higher significance)
# Use dense rank. Genes with NaN scores in a given metric get the worst rank.
# ---------------------------------------------------------------------------
per_gene["rank_raw"] = per_gene["mean_inclusive"].rank(
    method="dense", ascending=False, na_option="bottom"
).astype("Int64")
per_gene["rank_length_adj"] = per_gene["mean_adj"].rank(
    method="dense", ascending=False, na_option="bottom"
).astype("Int64")
# Composite-key dense rank for dNdScv (t144): primary key min_qglobal asc,
# secondary key n_cancers_significant_q05 desc. Single-column rank() collapses
# all q=0 BH-FDR-floor ties to rank 1; the per-gene rollup's secondary key
# breaks those ties so the gene with the most cancer types significant at
# q<0.05 ranks first among the q=0 set.
_dndscv_sorted = per_gene[["min_qglobal", "n_cancers_significant_q05"]].sort_values(
    by=["min_qglobal", "n_cancers_significant_q05"],
    ascending=[True, False],
    na_position="last",
    kind="mergesort",
)
_dndscv_ranks = (
    _dndscv_sorted.groupby(
        ["min_qglobal", "n_cancers_significant_q05"], dropna=False, sort=False
    ).ngroup()
    + 1
)
per_gene["rank_dndscv"] = _dndscv_ranks.reindex(per_gene.index).astype("Int64")

# Pairwise rank-shift columns (signed Δrank).
per_gene["shift_raw_to_length"] = per_gene["rank_length_adj"] - per_gene["rank_raw"]
per_gene["shift_raw_to_dndscv"] = per_gene["rank_dndscv"] - per_gene["rank_raw"]
per_gene["shift_length_to_dndscv"] = per_gene["rank_dndscv"] - per_gene["rank_length_adj"]

# ---------------------------------------------------------------------------
# Final column order.
# ---------------------------------------------------------------------------
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

out = per_gene[cols].reset_index(drop=True)
out.to_feather(snek.output[0])

print(
    f"compare_three_way_rankings: wrote {len(out):,} rows to {snek.output[0]}\n"
    f"  - {int(out['min_qglobal'].notna().sum()):,} with dndscv signal\n"
    f"  - {int(out['pubtator_mention_count'].notna().sum()):,} with PubTator counts"
)
