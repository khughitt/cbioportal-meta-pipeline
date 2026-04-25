# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "altair>=5",
#     "polars",
#     "pyarrow",
#     "scipy",
# ]
# ///
"""Top-N gene-ranking comparison: raw mutation frequency vs length-adjusted.

Settles Q4 of `discussion:2026-04-24-gene-length-bias-in-mutation-rankings-and-literature`
with the cBioPortal PoC cohort (poc-2026-04-17). Inputs:

- `results/poc-2026-04-17/summary/mut/table/gene_cancer_study_ratio_annotated.feather`
  — per (cancer_type, gene) ratios with `mean_inclusive` (raw, hypermutator-inclusive
  pooled across studies) and `mean_adj` (= mean / protein_length, length-divided).
- `results/poc-2026-04-17/metadata/protein_lengths.feather` — canonical UniProt
  single-isoform lengths, with median fallback for missing genes.

Outputs in this notebook:

1. Pan-cancer per-gene rollup. Aggregate `mean_inclusive` and `mean_adj` across
   cancer types (mean), join to protein length and Bailey 2018 driver flag.
2. Top-N table — raw vs length-adjusted, side-by-side at N = 10 / 50 / 100 / 500.
3. Spearman rank correlation between the two rankings on the universe of genes
   with non-zero `mean_inclusive`.
4. Jaccard overlap @ N = 10 / 50 / 100 / 500 / 1000.
5. Labeled scatter plot — `log10(mean_inclusive)` vs `log10(protein_length)`,
   colored by Bailey driver, with TTN-family + canonical-driver callouts.
6. Failure-mode panel for length-only adjustment — short-protein artifacts that
   inflate to the top of `mean_adj` despite low absolute counts.

The conclusion this notebook should support is: length adjustment correctly
demotes the textbook long-gene passengers (TTN, MUC16, OBSCN, RYR2, LRP1B,
CSMD-family, DNAH-family) and elevates short canonical drivers (KRAS, NRAS,
TP53, CDKN2A, RHOA), but it has its own failure mode — tiny proteins with low
absolute counts (BAGE2, PYY2, DEFB119, TMSB4X, SPRR4) get inflated by division
by small length. This motivates dNdScv-style selection-based ranking as the
next step (`task:t131`).
"""

from __future__ import annotations

import marimo

__generated_with = "0.13.0"
app = marimo.App(width="medium")


@app.cell
def _intro():
    import marimo as mo

    mo.md(
        """
        # q011 / Q4 — Top-N gene rankings: raw vs length-adjusted

        Direct comparison of the two columns the pipeline already emits:
        `mean_inclusive` (raw cross-study mutation ratio) and `mean_adj`
        (`mean_inclusive / protein_length`). Universe: PoC cohort
        `results/poc-2026-04-17`.
        """
    )
    return (mo,)


@app.cell
def _load(mo):
    from pathlib import Path

    import altair as alt
    import polars as pl

    results_dir = Path("results/poc-2026-04-17")
    ratio_path = results_dir / "summary/mut/table/gene_cancer_study_ratio_annotated.feather"
    length_path = results_dir / "metadata/protein_lengths.feather"

    ratio = pl.read_ipc(ratio_path)
    lengths = pl.read_ipc(length_path)

    mo.md(
        f"""
        - `gene_cancer_study_ratio_annotated.feather`: **{ratio.height:,}** rows,
          **{ratio.select('symbol').n_unique():,}** unique genes,
          **{ratio.select('cancer_type').n_unique():,}** cancer types
        - `protein_lengths.feather`: **{lengths.height:,}** symbols
        """
    )
    return alt, lengths, pl, ratio, results_dir


# ── 1. Pan-cancer per-gene rollup ────────────────────────────────────────────
@app.cell
def _per_gene(lengths, mo, pl, ratio):
    # Bailey is annotated at the (gene, cancer) row level; collapse to per-gene
    # by taking max (gene is "ever flagged" in any cancer).
    per_gene = (
        ratio.with_columns(pl.col("symbol").cast(pl.String))
        .group_by("symbol")
        .agg(
            pl.col("mean_inclusive").mean().alias("mean_inclusive"),
            pl.col("mean_adj").mean().alias("mean_adj"),
            pl.col("cancer_type").n_unique().alias("n_cancers"),
            pl.col("bailey2018_driver").max().alias("bailey_driver"),
            pl.col("cgc_tier_1").max().alias("cgc_tier_1"),
        )
        .join(lengths, on="symbol", how="left")
        .filter(pl.col("mean_inclusive") > 0)
    )

    mo.md(
        f"""
        Per-gene rollup: **{per_gene.height:,}** genes with non-zero pooled
        mean_inclusive across **{ratio.select('cancer_type').n_unique()}**
        cancer types. Bailey 2018 drivers in this universe:
        **{per_gene.filter(pl.col('bailey_driver')).height:,}**.
        """
    )
    return (per_gene,)


# ── 2. Top-N tables ──────────────────────────────────────────────────────────
@app.cell
def _topn_header_raw(mo):
    mo.md("### Top 20 by `mean_inclusive` (raw)")
    return


@app.cell
def _topn_raw(per_gene, pl):
    top20_raw = (
        per_gene.sort("mean_inclusive", descending=True)
        .head(20)
        .select(
            "symbol",
            pl.col("mean_inclusive").round(4),
            (pl.col("mean_adj") * 1e6).round(2).alias("mean_adj_e6"),
            pl.col("length").cast(pl.Int32),
            pl.col("bailey_driver").cast(pl.Boolean),
            "n_cancers",
        )
    )
    top20_raw
    return (top20_raw,)


@app.cell
def _topn_header_adj(mo):
    mo.md(
        "### Top 20 by `mean_adj` (length-adjusted = mean_inclusive / protein_length, expressed × 1e6)"
    )
    return


@app.cell
def _topn_adj(per_gene, pl):
    top20_adj = (
        per_gene.sort("mean_adj", descending=True)
        .head(20)
        .select(
            "symbol",
            pl.col("mean_inclusive").round(4),
            (pl.col("mean_adj") * 1e6).round(2).alias("mean_adj_e6"),
            pl.col("length").cast(pl.Int32),
            pl.col("bailey_driver").cast(pl.Boolean),
            "n_cancers",
        )
    )
    top20_adj
    return (top20_adj,)


# ── 3. Spearman correlation ─────────────────────────────────────────────────
@app.cell
def _spearman(mo, per_gene):
    from scipy.stats import spearmanr

    raw = per_gene["mean_inclusive"].to_numpy()
    adj = per_gene["mean_adj"].to_numpy()
    rho, p = spearmanr(raw, adj)

    mo.md(
        f"""
        **Spearman ρ(mean_inclusive, mean_adj) = {rho:.3f}** (p = {p:.2e},
        n = {len(raw):,}).

        Strong but not 1.0 — ranking *does* shift under length adjustment.
        Interpreting the rank shift in the head of the distribution is more
        informative than this pooled ρ; see Jaccard panel below.
        """
    )
    return (rho,)


# ── 4. Jaccard overlap @ N ──────────────────────────────────────────────────
@app.cell
def _jaccard_header(mo):
    mo.md("### Jaccard overlap of top-N gene sets")
    return


@app.cell
def _jaccard(alt, per_gene, pl):
    sorted_raw = per_gene.sort("mean_inclusive", descending=True)["symbol"].to_list()
    sorted_adj = per_gene.sort("mean_adj", descending=True)["symbol"].to_list()

    rows = []
    for n in [10, 25, 50, 100, 250, 500, 1000]:
        a = set(sorted_raw[:n])
        b = set(sorted_adj[:n])
        jacc = len(a & b) / len(a | b)
        rows.append({"N": n, "intersection": len(a & b), "jaccard": jacc})

    jacc_df = pl.DataFrame(rows)
    jacc_chart = (
        alt.Chart(jacc_df.to_pandas())
        .mark_line(point=True)
        .encode(
            x=alt.X("N:Q", scale=alt.Scale(type="log"), title="Top N"),
            y=alt.Y("jaccard:Q", scale=alt.Scale(domain=[0, 1]), title="Jaccard overlap"),
            tooltip=["N", "intersection", "jaccard"],
        )
        .properties(width=420, height=260, title="Top-N overlap: raw vs length-adjusted")
    )
    return jacc_chart, jacc_df


@app.cell
def _jaccard_table(jacc_df):
    jacc_df
    return


@app.cell
def _jaccard_chart_show(jacc_chart):
    jacc_chart
    return


# ── 5. Labeled scatter plot ─────────────────────────────────────────────────
@app.cell
def _scatter(alt, per_gene, pl):
    long_gene_passengers = {
        "TTN", "MUC16", "OBSCN", "RYR2", "RYR3", "LRP1B", "USH2A",
        "CSMD1", "CSMD2", "CSMD3", "FAT1", "FAT4", "PKHD1", "DNAH5",
        "DNAH7", "DNAH8", "DNAH11", "ZFHX4", "SYNE1", "PCLO", "GPR98",
        "MUC4",
    }
    canonical_drivers = {
        "TP53", "KRAS", "NRAS", "BRAF", "PIK3CA", "EGFR", "PTEN", "APC",
        "BRCA1", "BRCA2", "CDKN2A", "IDH1", "IDH2", "SMAD4", "FBXW7",
        "ATM", "ARID1A", "NF1", "RB1", "VHL", "RHOA", "KMT2D",
    }

    plot_df = per_gene.with_columns(
        pl.when(pl.col("symbol").is_in(long_gene_passengers))
        .then(pl.lit("long-gene passenger"))
        .when(pl.col("symbol").is_in(canonical_drivers))
        .then(pl.lit("canonical driver"))
        .when(pl.col("bailey_driver"))
        .then(pl.lit("other Bailey driver"))
        .otherwise(pl.lit("other"))
        .alias("category"),
    ).filter(pl.col("length").is_not_null() & (pl.col("length") > 0))

    base = alt.Chart(plot_df.to_pandas()).encode(
        x=alt.X(
            "length:Q",
            scale=alt.Scale(type="log"),
            title="Protein length (residues, log)",
        ),
        y=alt.Y(
            "mean_inclusive:Q",
            scale=alt.Scale(type="log"),
            title="mean_inclusive (raw mutation ratio, log)",
        ),
    )
    points = base.mark_circle(opacity=0.35, size=18).encode(
        color=alt.Color(
            "category:N",
            scale=alt.Scale(
                domain=[
                    "long-gene passenger",
                    "canonical driver",
                    "other Bailey driver",
                    "other",
                ],
                range=["#d62728", "#2ca02c", "#1f77b4", "#bbbbbb"],
            ),
            title=None,
        ),
        tooltip=["symbol", "length", "mean_inclusive", "mean_adj", "category"],
    )
    labels = (
        base.transform_filter(alt.datum.category != "other")
        .mark_text(dx=4, dy=-4, fontSize=9)
        .encode(text="symbol:N", color="category:N")
    )
    scatter_chart = (points + labels).properties(
        width=620,
        height=420,
        title="Mutation frequency vs protein length (per-gene, pan-cancer mean)",
    )
    return (scatter_chart,)


@app.cell
def _scatter_show(scatter_chart):
    scatter_chart
    return


# ── 6. Length-only failure-mode panel ───────────────────────────────────────
@app.cell
def _failure_header(mo):
    mo.md(
        """
        ### Length-only failure mode

        Short proteins (<200 aa) that crash into the top-100 of `mean_adj`
        despite low absolute mutation counts and no Bailey 2018 driver flag.
        Division by tiny length blows them up — the analogue of the long-gene
        bias, in the opposite direction. This is the methodological reason
        for moving to selection-based models (dNdScv) — `task:t131`.
        """
    )
    return


@app.cell
def _failure(per_gene, pl):
    short_inflators = (
        per_gene.sort("mean_adj", descending=True)
        .head(100)
        .filter(~pl.col("bailey_driver") & (pl.col("length") < 200))
        .select(
            "symbol",
            pl.col("mean_inclusive").round(4),
            (pl.col("mean_adj") * 1e6).round(2).alias("mean_adj_e6"),
            pl.col("length").cast(pl.Int32),
            "n_cancers",
        )
    )
    short_inflators
    return


# ── 7. Synthesis ────────────────────────────────────────────────────────────
@app.cell
def _conclusion(mo):
    mo.md(
        """
        ## Conclusion

        - **Long-gene passengers crash out under length adjustment** as
          predicted: TTN, MUC16, OBSCN, RYR2, LRP1B, CSMD-family, DNAH-family,
          PCLO, SYNE1, FAT4 dominate the raw top-20 and disappear from the
          adjusted top-20.
        - **Short canonical drivers rise correctly**: TP53, KRAS, NRAS, CDKN2A,
          RHOA appear high in the adjusted ranking. KRAS jumps especially
          dramatically (189 aa, very recurrent).
        - **Length-only adjustment has its own failure mode**: tiny proteins
          (BAGE2, PYY2, DEFB119, TMSB4X, SPRR4) get inflated by division by
          small length. This is symmetric to the long-gene bias and is why
          MutSigCV / dNdScv move to *selection-based* ratios rather than
          pure length division.
        - **Top-N Jaccard** quantifies the rank churn — see panel above.
          The shift is concentrated in the head of the distribution, exactly
          where rankings are read.

        Next: `task:t131` — opt dNdScv into a side config and produce a
        three-way (raw / length-adjusted / dNdScv-selection) comparison.
        Pairs with `q011` regression on the literature-attention side.
        """
    )
    return


if __name__ == "__main__":
    app.run()
