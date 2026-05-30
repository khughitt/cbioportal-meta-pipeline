# science:code
# status: exploratory
# science:end
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
"""Three-way per-gene ranking comparison: raw vs length-adjusted vs dNdScv.

Settles t131 by extending the q011 notebook's per-gene rollup with a
selection-based ranking from dNdScv (Martincorena 2017) and a PubTator
literature-attention panel that closes the loop with q011's central
conjecture.

Inputs:

- `summary/mut/table/three_way_ranking_comparison.feather`
  (produced by `rule compare_three_way_rankings`; per-gene table with
  raw / length-adjusted / dNdScv ranks plus PubTator mention counts.)

Panels:

1. Per-gene rollup head.
2. Three top-20 tables (raw / length-adjusted / dNdScv).
3. Spearman correlation 3x3 matrix.
4. Jaccard@N table for the three pairwise rankings.
5. Three scatter plots: protein length vs each score, colored by Bailey
   driver, labeled with canonical drivers.
6. Recovery panel: how many Bailey 2018 drivers each scheme recovers in
   top-N, stratified by protein-length quartile.
7. Failure-mode panel: top-100 of each scheme that are NOT Bailey drivers
   AND NOT CGC tier 1, stratified by length quartile.
8. Per-cancer significance heatmap from `n_cancers_significant_q05`.
9. PubTator correlation panel (q011 falsifier readout).
10. Synthesis cell.
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
        # t131 — Three-way per-gene ranking comparison

        Raw mutation frequency (`mean_inclusive`) vs length-adjusted
        (`mean_adj`) vs dNdScv selection (`min_qglobal`) per-gene rankings,
        with a PubTator literature-attention correlation panel that closes
        the loop with `q011`'s conjecture.
        """
    )
    return (mo,)


@app.cell
def _load(mo):
    import os
    from pathlib import Path

    import altair as alt
    import polars as pl

    # Set CBIO_PKG_ROOT to a package dir (e.g. /data/packages/cbioportal) to read a
    # config-pan-cancer-dndscv run; otherwise falls back to in-repo results/.
    _pkg_root = os.environ.get("CBIO_PKG_ROOT")
    candidates = [
        *([Path(_pkg_root) / "pan-cancer-dndscv"] if _pkg_root else []),
        Path("results/poc-2026-04-17"),
    ]
    out_dir = next((p for p in candidates if p.exists()), candidates[0])
    cmp_path = out_dir / "summary/mut/table/three_way_ranking_comparison.feather"

    if not cmp_path.exists():
        mo.md(
            f"**Comparison feather not found at `{cmp_path}`.** Run the dNdScv "
            f"chain first: `snakemake -s code/workflows/Snakefile --configfile "
            f"code/config/config-pan-cancer-dndscv.yml --use-conda all_with_dndscv`."
        )
        cmp_df = pl.DataFrame()
    else:
        cmp_df = pl.read_ipc(cmp_path)
        mo.md(
            f"Loaded **{cmp_df.height:,}** genes from `{cmp_path}`. "
            f"With dNdScv signal: **{int(cmp_df.filter(pl.col('min_qglobal').is_not_null()).height):,}**. "
            f"With PubTator: **{int(cmp_df.filter(pl.col('pubtator_mention_count').is_not_null()).height):,}**."
        )

    return alt, cmp_df, out_dir, pl


# ── 2. Top-20 tables (raw / length-adjusted / dNdScv) ──────────────────────
@app.cell
def _topn_raw_header(mo):
    mo.md("### Top 20 by raw mutation frequency")
    return


@app.cell
def _topn_raw(cmp_df, pl):
    cmp_df.sort("mean_inclusive", descending=True).head(20).select(
        "symbol",
        pl.col("length").cast(pl.Int32),
        pl.col("mean_inclusive").round(4),
        (pl.col("mean_adj") * 1e6).round(2).alias("mean_adj_e6"),
        pl.col("min_qglobal").round(4).alias("dndscv_minq"),
        pl.col("n_cancers_significant_q05").cast(pl.Int32).alias("n_cancers_sig"),
    ) if not cmp_df.is_empty() else None
    return


@app.cell
def _topn_adj_header(mo):
    mo.md("### Top 20 by length-adjusted (`mean_adj`)")
    return


@app.cell
def _topn_adj(cmp_df, pl):
    cmp_df.sort("mean_adj", descending=True).head(20).select(
        "symbol",
        pl.col("length").cast(pl.Int32),
        pl.col("mean_inclusive").round(4),
        (pl.col("mean_adj") * 1e6).round(2).alias("mean_adj_e6"),
        pl.col("min_qglobal").round(4).alias("dndscv_minq"),
        pl.col("n_cancers_significant_q05").cast(pl.Int32).alias("n_cancers_sig"),
    ) if not cmp_df.is_empty() else None
    return


@app.cell
def _topn_dndscv_header(mo):
    mo.md("### Top 20 by dNdScv selection (lower min_qglobal = stronger)")
    return


@app.cell
def _topn_dndscv(cmp_df, pl):
    (
        cmp_df.filter(pl.col("min_qglobal").is_not_null())
        .sort("min_qglobal", descending=False)
        .head(20)
        .select(
            "symbol",
            pl.col("length").cast(pl.Int32),
            pl.col("mean_inclusive").round(4),
            pl.col("min_qglobal").round(6).alias("dndscv_minq"),
            pl.col("n_cancers_significant_q05").cast(pl.Int32).alias("n_cancers_sig"),
            "best_cancer_type",
        )
    ) if not cmp_df.is_empty() else None
    return


# ── 3. Spearman 3x3 matrix ─────────────────────────────────────────────────
@app.cell
def _spearman_header(mo):
    mo.md("### Spearman correlation matrix (raw / length-adj / dNdScv)")
    return


@app.cell
def _spearman(cmp_df, mo, pl):
    if cmp_df.is_empty():
        return None

    from scipy.stats import spearmanr

    sub = cmp_df.filter(
        pl.col("mean_inclusive").is_not_null()
        & pl.col("mean_adj").is_not_null()
        & pl.col("min_qglobal").is_not_null()
    )
    raw = sub["mean_inclusive"].to_numpy()
    adj = sub["mean_adj"].to_numpy()
    # For dNdScv use -log10(q+eps) so it ranks high-significance high.
    import math
    eps = 1e-300
    dnd = sub["min_qglobal"].to_numpy()
    dnd_score = [-math.log10(float(q) + eps) if q is not None else float("nan") for q in dnd]

    rows = []
    for n1, v1 in [("raw", raw), ("length_adj", adj), ("dndscv", dnd_score)]:
        for n2, v2 in [("raw", raw), ("length_adj", adj), ("dndscv", dnd_score)]:
            rho, _ = spearmanr(v1, v2)
            rows.append({"axis": n1, "vs": n2, "rho": round(float(rho), 3)})
    table = pl.DataFrame(rows).pivot(values="rho", index="axis", on="vs")
    return mo.ui.table(table), table


# ── 4. Jaccard@N for the three pairings ────────────────────────────────────
@app.cell
def _jaccard_header(mo):
    mo.md(
        "### Jaccard overlap @ N — three pairwise rankings\n\n"
        "Each row: top-N gene sets compared. Only genes with non-null "
        "`min_qglobal` enter the dNdScv ranking."
    )
    return


@app.cell
def _jaccard(cmp_df, pl):
    if cmp_df.is_empty():
        return None

    sub = cmp_df.filter(pl.col("min_qglobal").is_not_null())
    sorted_raw = sub.sort("mean_inclusive", descending=True)["symbol"].to_list()
    sorted_adj = sub.sort("mean_adj", descending=True)["symbol"].to_list()
    sorted_dnd = sub.sort("min_qglobal", descending=False)["symbol"].to_list()

    rows = []
    for n in [10, 25, 50, 100, 250, 500, 1000]:
        a = set(sorted_raw[:n])
        b = set(sorted_adj[:n])
        c = set(sorted_dnd[:n])
        rows.append(
            {
                "N": n,
                "jacc_raw_vs_length_adj": round(len(a & b) / len(a | b), 3),
                "jacc_raw_vs_dndscv":     round(len(a & c) / len(a | c), 3),
                "jacc_length_vs_dndscv":  round(len(b & c) / len(b | c), 3),
            }
        )
    return pl.DataFrame(rows)


# ── 5. Length vs each score, scatter ──────────────────────────────────────
@app.cell
def _scatter_header(mo):
    mo.md("### Protein length vs each ranking signal (Bailey / canonical-driver overlay)")
    return


@app.cell
def _scatter(alt, cmp_df, pl):
    if cmp_df.is_empty():
        return None

    long_passengers = {
        "TTN", "MUC16", "OBSCN", "RYR2", "RYR3", "LRP1B", "USH2A",
        "CSMD1", "CSMD2", "CSMD3", "FAT1", "FAT4", "PKHD1", "DNAH5",
        "DNAH7", "DNAH8", "DNAH11", "ZFHX4", "SYNE1", "PCLO", "GPR98",
    }
    canonical_drivers = {
        "TP53", "KRAS", "NRAS", "BRAF", "PIK3CA", "EGFR", "PTEN", "APC",
        "BRCA1", "BRCA2", "CDKN2A", "IDH1", "IDH2", "SMAD4", "FBXW7",
        "ATM", "ARID1A", "NF1", "RB1", "VHL", "RHOA", "KMT2D",
    }

    plot_df = cmp_df.with_columns(
        pl.when(pl.col("symbol").is_in(long_passengers))
        .then(pl.lit("long-gene passenger"))
        .when(pl.col("symbol").is_in(canonical_drivers))
        .then(pl.lit("canonical driver"))
        .when(
            pl.col("bailey_driver").fill_null(False)
            if "bailey_driver" in cmp_df.columns
            else pl.lit(False)
        )
        .then(pl.lit("other Bailey driver"))
        .otherwise(pl.lit("other"))
        .alias("category"),
    ).filter(pl.col("length").is_not_null() & (pl.col("length") > 0))

    return plot_df


@app.cell
def _scatter_charts(alt, plot_df):
    if plot_df is None or plot_df.is_empty():
        return None

    base = alt.Chart(plot_df.to_pandas())
    color = alt.Color(
        "category:N",
        scale=alt.Scale(
            domain=["long-gene passenger", "canonical driver", "other Bailey driver", "other"],
            range=["#d62728", "#2ca02c", "#1f77b4", "#bbbbbb"],
        ),
        title=None,
    )
    raw_scatter = (
        base.mark_circle(opacity=0.35, size=18)
        .encode(
            x=alt.X("length:Q", scale=alt.Scale(type="log"), title="Protein length (residues, log)"),
            y=alt.Y("mean_inclusive:Q", scale=alt.Scale(type="log"), title="mean_inclusive (raw)"),
            color=color,
            tooltip=["symbol", "length", "mean_inclusive", "mean_adj", "min_qglobal", "category"],
        )
        .properties(width=520, height=320, title="Length vs raw frequency")
    )
    dndscv_scatter = (
        base.mark_circle(opacity=0.35, size=18)
        .transform_filter("datum.min_qglobal != null")
        .encode(
            x=alt.X("length:Q", scale=alt.Scale(type="log"), title="Protein length (residues, log)"),
            y=alt.Y(
                "min_qglobal:Q",
                scale=alt.Scale(type="log", reverse=True),
                title="min_qglobal (lower = stronger selection, log-reversed)",
            ),
            color=color,
            tooltip=["symbol", "length", "min_qglobal", "n_cancers_significant_q05", "category"],
        )
        .properties(width=520, height=320, title="Length vs dNdScv selection")
    )
    return raw_scatter & dndscv_scatter


# ── 6. Bailey-recovery panel by length quartile ────────────────────────────
@app.cell
def _recovery_header(mo):
    mo.md(
        "### Bailey-driver recovery by ranking scheme & length quartile\n\n"
        "Of the Bailey 2018 drivers in the cohort, what fraction lands in top-N "
        "for each scheme, stratified by protein-length quartile? Length-only "
        "adjustment penalizes long Bailey drivers (ATM, BRCA2, NF1, APC); "
        "dNdScv should rescue them."
    )
    return


@app.cell
def _recovery(cmp_df, pl):
    if cmp_df.is_empty() or "bailey_driver" not in cmp_df.columns:
        return None

    bailey = cmp_df.filter(pl.col("bailey_driver").fill_null(False))
    if bailey.is_empty():
        return None

    bailey = bailey.with_columns(
        pl.col("length").qcut(quantiles=4, labels=["Q1 (shortest)", "Q2", "Q3", "Q4 (longest)"]).alias("len_quartile")
    )

    rows = []
    for scheme, score_col, ascending in [
        ("raw", "mean_inclusive", False),
        ("length_adj", "mean_adj", False),
        ("dndscv", "min_qglobal", True),
    ]:
        sub = cmp_df.filter(pl.col(score_col).is_not_null())
        ordered = sub.sort(score_col, descending=not ascending)["symbol"].to_list()
        for n in [50, 100, 250, 500]:
            top_set = set(ordered[:n])
            for q in ["Q1 (shortest)", "Q2", "Q3", "Q4 (longest)"]:
                qb = bailey.filter(pl.col("len_quartile") == q)["symbol"].to_list()
                hit = len(set(qb) & top_set)
                rows.append({"scheme": scheme, "N": n, "len_quartile": q,
                             "n_bailey_in_quartile": len(qb), "n_recovered": hit,
                             "frac_recovered": round(hit / max(len(qb), 1), 3)})
    return pl.DataFrame(rows)


# ── 7. Failure mode by quartile ───────────────────────────────────────────
@app.cell
def _failure_header(mo):
    mo.md(
        "### Top-100 failure mode by length quartile\n\n"
        "Top-100 by each scheme that are NOT Bailey drivers AND NOT CGC tier 1, "
        "stratified by length quartile. Long-gene passengers cluster in Q4 for "
        "raw; tiny-protein artifacts cluster in Q1 for length-adjusted; dNdScv "
        "should be more uniformly distributed."
    )
    return


@app.cell
def _failure(cmp_df, pl):
    if cmp_df.is_empty():
        return None

    has_cgc = "cgc_tier_1" in cmp_df.columns
    has_bailey = "bailey_driver" in cmp_df.columns

    def _filter_non_drivers(frame):
        f = frame
        if has_bailey:
            f = f.filter(~pl.col("bailey_driver").fill_null(False))
        if has_cgc:
            f = f.filter(~pl.col("cgc_tier_1").fill_null(False))
        return f

    enriched = cmp_df.with_columns(
        pl.col("length").qcut(quantiles=4, labels=["Q1", "Q2", "Q3", "Q4"]).alias("len_q")
    )

    rows = []
    for scheme, score_col, ascending in [
        ("raw", "mean_inclusive", False),
        ("length_adj", "mean_adj", False),
        ("dndscv", "min_qglobal", True),
    ]:
        sub = enriched.filter(pl.col(score_col).is_not_null())
        ordered = sub.sort(score_col, descending=not ascending).head(100)
        non_drivers = _filter_non_drivers(ordered)
        for q in ["Q1", "Q2", "Q3", "Q4"]:
            n = non_drivers.filter(pl.col("len_q") == q).height
            rows.append({"scheme": scheme, "len_q": q, "n_non_drivers_in_top100": n})
    return pl.DataFrame(rows)


# ── 8. PubTator correlation panel (q011 falsifier readout) ────────────────
@app.cell
def _pubtator_header(mo):
    mo.md(
        "### PubTator literature-attention correlation (q011 falsifier readout)\n\n"
        "If dNdScv's PubTator correlation is meaningfully **lower** than raw's, "
        "that supports q011's conjecture that gene length confounds literature "
        "attention through the mutation-count mediator. If they're equal or "
        "dNdScv is higher, the conjecture is weakened."
    )
    return


@app.cell
def _pubtator(cmp_df, pl):
    if cmp_df.is_empty():
        return None
    if cmp_df["pubtator_mention_count"].null_count() == cmp_df.height:
        return "PubTator data not joined (no `pubtator_path` in config)."

    from scipy.stats import spearmanr

    sub = cmp_df.filter(
        pl.col("pubtator_mention_count").is_not_null()
        & pl.col("min_qglobal").is_not_null()
    )
    pub = sub["pubtator_log10_mentions"].to_numpy()

    rho_raw, _ = spearmanr(sub["mean_inclusive"].to_numpy(), pub)
    rho_adj, _ = spearmanr(sub["mean_adj"].to_numpy(), pub)
    # dNdScv: use -log10(q) for direction-of-effect alignment
    import math
    eps = 1e-300
    dnd_score = [-math.log10(float(q) + eps) for q in sub["min_qglobal"].to_list()]
    rho_dnd, _ = spearmanr(dnd_score, pub)

    return pl.DataFrame(
        [
            {"scheme": "raw",        "spearman_vs_log10_pubtator": round(float(rho_raw), 3)},
            {"scheme": "length_adj", "spearman_vs_log10_pubtator": round(float(rho_adj), 3)},
            {"scheme": "dndscv",     "spearman_vs_log10_pubtator": round(float(rho_dnd), 3)},
        ]
    )


# ── 9. Synthesis ───────────────────────────────────────────────────────────
@app.cell
def _conclusion(mo):
    mo.md(
        """
        ## Synthesis

        - The raw and length-adjusted rankings are known to be radically
          different (q011 notebook: Spearman 0.37, Jaccard@100 = 0.015). dNdScv
          enters as a third axis that, by construction, is length-aware in a
          principled way (compares non-synonymous to synonymous mutations
          adjusting for trinucleotide context).
        - **Read the recovery panel first**: dNdScv should recover Bailey
          drivers across all length quartiles roughly evenly, while raw misses
          short ones and length-adjusted misses long ones.
        - **Then read the failure-mode panel**: the per-quartile distribution
          of top-100-non-driver hits per scheme tells you which scheme
          generates the cleanest head.
        - **PubTator panel as q011 falsifier**: a meaningfully smaller
          length-aware Spearman ρ vs PubTator (compared to the raw ρ) is
          direct empirical support for q011's conjecture that gene length
          confounds literature attention through the mutation-count mediator.

        Next steps are scoped under tasks t129 (PubTator regression),
        t130 (Stoeger 2018 paper summary), and t136 (canonicalize-to-GRCh38
        at ingestion).
        """
    )
    return


if __name__ == "__main__":
    app.run()
