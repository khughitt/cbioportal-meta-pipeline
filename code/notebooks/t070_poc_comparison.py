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
# ]
# ///
"""Pre-vs-post-t070 comparison for the PoC run (msk_impact_2017 focus).

Loads per-sample TMB + per-(gene, cancer) ratio outputs from the two parallel
pipeline runs and quantifies the bias fixes introduced by t070. Three axes:

1. Frequency rates — top-20 affected (cancer, gene) rows in msk_impact_2017,
   pre vs post.
2. TMB distributions — per-sample TMB stratified by panel_id, pre vs post.
3. Hypermutator flag transitions — Campbell / GMM / reason category shifts.

Out paths (config-driven):
- pre:  /data/packages/cbioportal/poc-pre-t070
- post: results/poc-2026-04-17 (relative to worktree root)
"""

import marimo

__generated_with = "0.13.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl
    import altair as alt
    from pathlib import Path

    pre_dir = Path("/data/packages/cbioportal/poc-pre-t070")
    post_dir = Path("results/poc-2026-04-17")
    study_id = "msk_impact_2017"

    mo.md(
        f"""
        # t070 PoC pre/post comparison

        **Study:** `{study_id}`
        **Pre-t070:** `{pre_dir}` (panel_bearing_studies=[])
        **Post-t070:** `{post_dir}` (panel_bearing_studies=[msk_impact_2017])
        """
    )
    return alt, mo, pl, pre_dir, post_dir, study_id


# ── Axis 1: per-sample TMB distributions ─────────────────────────────
@app.cell
def _load_tmb(pl, pre_dir, post_dir, study_id):
    pre_tmb = pl.read_ipc(pre_dir / f"studies/{study_id}/metadata/samples_tmb.feather")
    post_tmb = pl.read_ipc(post_dir / f"studies/{study_id}/metadata/samples_tmb.feather")
    # Align on sample_id for direct comparison
    joined = pre_tmb.select(["sample_id", "tmb", "panel_callable_mb"]).rename(
        {"tmb": "tmb_pre", "panel_callable_mb": "mb_pre"}
    ).join(
        post_tmb.select(["sample_id", "tmb", "panel_callable_mb"]).rename(
            {"tmb": "tmb_post", "panel_callable_mb": "mb_post"}
        ),
        on="sample_id",
        how="inner",
    )
    # Enrich with panel_id from post samples.feather
    post_samples = pl.read_ipc(post_dir / f"studies/{study_id}/metadata/samples.feather")
    joined = joined.join(
        post_samples.select(["sample_id", "panel_id"]),
        on="sample_id",
        how="left",
    )
    return joined, post_samples, post_tmb, pre_tmb


@app.cell
def _tmb_summary(joined, mo, pl):
    summary = (
        joined.group_by("panel_id")
        .agg(
            n=pl.len(),
            median_tmb_pre=pl.col("tmb_pre").median(),
            median_tmb_post=pl.col("tmb_post").median(),
            mean_tmb_pre=pl.col("tmb_pre").mean(),
            mean_tmb_post=pl.col("tmb_post").mean(),
            median_mb_pre=pl.col("mb_pre").median(),
            median_mb_post=pl.col("mb_post").median(),
        )
        .with_columns(ratio=pl.col("median_tmb_post") / pl.col("median_tmb_pre"))
        .sort("panel_id")
    )
    mo.md(f"""
    ## TMB summary by panel_id

    Pre-t070 uses `wes_default_callable_mb = 30 Mb` for all MSK samples.
    Post-t070 uses the per-panel Mb value (0.89 / 1.01 / 1.22 / 1.45).
    Expected TMB ratio ≈ 30 / panel_mb ≈ 20-34×.
    """)
    return (summary,)


@app.cell
def _tmb_summary_display(mo, summary):
    mo.ui.table(summary.to_pandas())
    return


@app.cell
def _tmb_hist(alt, joined, pl):
    # Melt pre vs post into a single "tmb" column with a "run" categorical
    melted = pl.concat(
        [
            joined.select("panel_id", pl.col("tmb_pre").alias("tmb"))
            .with_columns(run=pl.lit("pre-t070")),
            joined.select("panel_id", pl.col("tmb_post").alias("tmb"))
            .with_columns(run=pl.lit("post-t070")),
        ]
    ).filter(pl.col("tmb").is_not_null())

    chart = (
        alt.Chart(melted.to_pandas())
        .mark_bar(opacity=0.6)
        .encode(
            x=alt.X(
                "tmb:Q",
                bin=alt.Bin(maxbins=60),
                scale=alt.Scale(type="log", domainMin=0.01),
                title="TMB (mut/Mb, log scale)",
            ),
            y=alt.Y("count():Q", title="Samples"),
            color=alt.Color("run:N", title="Run"),
            column=alt.Column("panel_id:N", title="Panel"),
        )
        .properties(width=200, height=200)
        .resolve_scale(y="independent")
    )
    chart
    return chart, melted


# ── Axis 2: hypermutator flag transitions ────────────────────────────
@app.cell
def _load_hypermutators(pl, pre_dir, post_dir):
    pre_ann = pl.read_ipc(pre_dir / "metadata/samples_annotated.feather")
    post_ann = pl.read_ipc(post_dir / "metadata/samples_annotated.feather")
    hm = pre_ann.select(
        ["sample_id", "is_hypermutator", "hypermutator_reason"]
    ).rename(
        {
            "is_hypermutator": "is_hypermutator_pre",
            "hypermutator_reason": "reason_pre",
        }
    ).join(
        post_ann.select(
            ["sample_id", "is_hypermutator", "hypermutator_reason"]
        ).rename(
            {
                "is_hypermutator": "is_hypermutator_post",
                "hypermutator_reason": "reason_post",
            }
        ),
        on="sample_id",
        how="inner",
    )
    return hm, post_ann, pre_ann


@app.cell
def _hypermutator_flips(hm, mo, pl):
    # Filter to MSK samples only for the study-level comparison
    flips = hm.with_columns(
        flipped=pl.col("is_hypermutator_pre") != pl.col("is_hypermutator_post")
    )
    n_total = flips.height
    n_flipped = flips.filter(pl.col("flipped")).height
    n_false_to_true = flips.filter(
        (~pl.col("is_hypermutator_pre")) & pl.col("is_hypermutator_post")
    ).height
    n_true_to_false = flips.filter(
        pl.col("is_hypermutator_pre") & (~pl.col("is_hypermutator_post"))
    ).height

    mo.md(
        f"""
        ## Hypermutator flag transitions

        - **Total samples compared:** {n_total}
        - **Flag flipped:** {n_flipped} ({100 * n_flipped / n_total:.1f}%)
        - **False → True** (newly flagged hypermutator post-t070): {n_false_to_true}
        - **True → False** (unflagged post-t070): {n_true_to_false}

        Expected direction: post-t070 MSK samples have ~25-30× higher TMB,
        so many should cross Campbell 2017's 10 mut/Mb threshold and be newly flagged.
        """
    )
    return (flips,)


@app.cell
def _reason_transitions(flips, mo, pl):
    transitions = (
        flips.group_by(["reason_pre", "reason_post"])
        .agg(n=pl.len())
        .sort("n", descending=True)
    )
    mo.md("### `hypermutator_reason` transitions (pre → post)")
    return (transitions,)


@app.cell
def _reason_display(mo, transitions):
    mo.ui.table(transitions.to_pandas())
    return


# ── Axis 3: frequency-rate comparison ─────────────────────────────────
@app.cell
def _load_ratios(pl, pre_dir, post_dir):
    pre_ratio = pl.read_ipc(pre_dir / "summary/mut/table/gene_cancer_study_ratio_annotated.feather")
    post_ratio = pl.read_ipc(post_dir / "summary/mut/table/gene_cancer_study_ratio_annotated.feather")
    # Focus on msk_impact_2017 column (per-study)
    study_col = "msk_impact_2017"
    pre_rate = pre_ratio.select(
        ["cancer_type", "symbol", study_col]
    ).rename({study_col: "rate_pre"})
    post_rate = post_ratio.select(
        ["cancer_type", "symbol", study_col]
    ).rename({study_col: "rate_post"})
    merged = pre_rate.join(
        post_rate, on=["cancer_type", "symbol"], how="inner"
    ).with_columns(
        delta=pl.col("rate_post") - pl.col("rate_pre"),
        ratio=pl.col("rate_post") / pl.col("rate_pre"),
    )
    return merged, post_ratio, pre_ratio


@app.cell
def _top_rate_deltas(merged, mo, pl):
    top = (
        merged.filter(
            (pl.col("rate_pre").is_not_null())
            & (pl.col("rate_post").is_not_null())
            & (pl.col("rate_pre") > 0.001)
        )
        .sort(pl.col("ratio").abs(), descending=True)
        .head(20)
    )
    mo.md(
        """
        ## Top-20 (cancer, gene) rate shifts in msk_impact_2017

        Sorted by |ratio| (post-t070 rate / pre-t070 rate).
        Genes added in IMPACT-410+ should show ratio ≈ 10945 / 8136 = 1.345
        (26% of samples drop out of the denominator).
        Genes on IMPACT-341 should show ratio ≈ 1.0.
        """
    )
    return (top,)


@app.cell
def _top_display(mo, top):
    mo.ui.table(top.to_pandas())
    return


if __name__ == "__main__":
    app.run()
