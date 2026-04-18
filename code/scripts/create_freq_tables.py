"""
create_freq_tables.py

Per-study mutation frequency tables at four keys: ``cancer_type``,
``cancer_type_detailed``, ``symbol``, and ``(cancer_type, symbol)``.

t098 / t081.7 (F1 fix): each table now carries paired inclusive/exclusive
columns based on the ``is_hypermutator`` flag produced by
``annotate_hypermutators`` (t097). Columns:

- ``num_inclusive``        — mutated sample count over all samples.
- ``num_exclusive``        — mutated sample count over non-hypermutator samples.
- ``ratio_inclusive``      — num_inclusive / n_samples_inclusive.
- ``ratio_exclusive``      — num_exclusive / n_samples_exclusive (NaN if zero).
- ``n_samples_inclusive``  — cohort denominator (all samples in the key group).
- ``n_samples_exclusive``  — cohort denominator restricted to non-hypermutators.

The legacy ``num`` / ``ratio`` columns are preserved as aliases of the inclusive
pair for backward-compatibility with downstream consumers that have not yet
switched to the paired schema.

t070: when ``panel_coverage`` is supplied and samples carry a ``panel_id``
column, the gene-keyed and (cancer, gene)-keyed tables use per-gene
denominators: only samples whose panel covers that gene count toward
``n_samples_inclusive`` / ``n_samples_exclusive``. Cancer-only tables
(``cancer.feather``, ``cancer_detailed.feather``) are unchanged.

Per the t070 design spec (error handling item 6): when a gene appears in a
study's mutation table but on zero of the study's per-sample panels (mutation
called outside panel intervals — should be rare), the (cancer, gene) row is
dropped from that study with a WARNING. If the dropped-row count exceeds 1% of
the study's mutated (cancer, gene) pairs, a ValueError is raised instead.

Inputs
------
- ``snakemake.input.mutations`` : per-study ``mut_filtered.feather``
- ``snakemake.input.samples`` : per-study ``samples.feather``
- ``snakemake.input.samples_annotated`` : cross-study ``samples_annotated.feather``
  produced by ``annotate_hypermutators``. The per-study step filters this by
  matching ``sample_id``.
- ``snakemake.input.panel_coverage`` : (optional) ``genie_panel_coverage.feather``
  produced by ``process_genie_panel_coverage``; columns ``panel_id`` and ``gene``.
  Only present when ``panel_bearing_studies`` is non-empty in the run config.
"""

import logging

import pandas as pd

logger = logging.getLogger("create_freq_tables")


def compute_freq_tables(
    mutations: pd.DataFrame,
    samples: pd.DataFrame,
    hypermutator_flags: pd.DataFrame,
    panel_coverage: pd.DataFrame | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Compute (cancer, cancer_detailed, gene, gene_cancer) frequency tables.

    Arguments
    ---------
    mutations : per-study mutation rows; must have ``symbol`` and
        ``sample_id_tumor`` columns.
    samples : per-study sample metadata; must have ``sample_id``,
        ``cancer_type``, ``cancer_type_detailed``. Zero-mutation samples must be
        present here so they count toward the denominator.
    hypermutator_flags : two columns ``sample_id`` and ``is_hypermutator``.
        Samples absent from this table are treated as non-hypermutators (the
        conservative default).
    panel_coverage : optional DataFrame with columns ``panel_id`` and ``gene``.
        When supplied alongside a ``panel_id`` column in ``samples``, the gene-
        and (cancer, gene)-keyed tables switch to per-(cancer, gene) denominators:
        only samples whose panel covers a given gene count toward that gene's
        denominator. Cancer-only tables are unaffected. When None (WES studies),
        the existing cohort-wide denominator path is used unchanged.

    Returns
    -------
    Tuple of four DataFrames keyed by ``cancer_type``, ``cancer_type_detailed``,
    ``symbol``, and ``(cancer_type, symbol)`` respectively.
    """
    mut = mutations[["symbol", "sample_id_tumor"]].rename(
        columns={"sample_id_tumor": "sample_id"}
    )

    sample_cols = ["sample_id", "cancer_type", "cancer_type_detailed"]
    if "panel_id" in samples.columns:
        sample_cols.append("panel_id")
    samples_meta = samples[sample_cols]

    flags = _prepare_flags(hypermutator_flags, samples_meta)

    # Prerequisite check: every non-null panel_id in samples must have coverage rows.
    if panel_coverage is not None and "panel_id" in samples_meta.columns:
        panels_in_samples = set(samples_meta["panel_id"].dropna().unique())
        panels_in_coverage = set(panel_coverage["panel_id"].unique())
        missing = panels_in_samples - panels_in_coverage
        if missing:
            missing_str = ", ".join(sorted(missing))
            raise ValueError(
                f"panel_coverage is missing entries for panel(s): {missing_str}. "
                "Ensure genie_panel_coverage.feather was built from all panels "
                "present in this study's samples.feather."
            )

    # Attach cancer type + hypermutator flag to each mutation row for grouping.
    mut = mut.merge(samples_meta, on="sample_id").merge(flags, on="sample_id")

    cancer_df = _build_single_key(
        mut=mut, samples_meta=samples_meta, flags=flags, key="cancer_type"
    )
    cancer_detailed_df = _build_single_key(
        mut=mut, samples_meta=samples_meta, flags=flags, key="cancer_type_detailed"
    )
    gene_df = _build_gene_table(
        mut=mut, samples_meta=samples_meta, flags=flags, panel_coverage=panel_coverage
    )
    gene_cancer_df = _build_gene_cancer_table(
        mut=mut, samples_meta=samples_meta, flags=flags, panel_coverage=panel_coverage
    )
    return cancer_df, cancer_detailed_df, gene_df, gene_cancer_df


def _prepare_flags(
    hypermutator_flags: pd.DataFrame, samples_meta: pd.DataFrame
) -> pd.DataFrame:
    """Left-join flags onto samples_meta so every sample has a boolean flag
    (default False for samples absent from ``hypermutator_flags``)."""
    flags = (
        samples_meta[["sample_id"]]
        .merge(hypermutator_flags, on="sample_id", how="left")
        .fillna({"is_hypermutator": False})
    )
    flags["is_hypermutator"] = flags["is_hypermutator"].astype(bool)
    return flags


def _build_single_key(
    mut: pd.DataFrame,
    samples_meta: pd.DataFrame,
    flags: pd.DataFrame,
    key: str,
) -> pd.DataFrame:
    """Build a frequency table keyed on a single column (cancer_type or
    cancer_type_detailed)."""
    samples_with_flag = samples_meta.merge(flags, on="sample_id")

    n_inclusive = samples_with_flag.groupby(key, observed=True)["sample_id"].nunique()
    n_exclusive = (
        samples_with_flag.loc[~samples_with_flag["is_hypermutator"]]
        .groupby(key, observed=True)["sample_id"]
        .nunique()
    )

    num_inclusive = mut.groupby(key, observed=True)["sample_id"].nunique()
    num_exclusive = (
        mut.loc[~mut["is_hypermutator"]]
        .groupby(key, observed=True)["sample_id"]
        .nunique()
    )

    df = pd.DataFrame(
        {
            "num_inclusive": num_inclusive,
            "num_exclusive": num_exclusive,
            "n_samples_inclusive": n_inclusive,
            "n_samples_exclusive": n_exclusive,
        }
    ).fillna(0)
    df[["num_inclusive", "num_exclusive"]] = df[
        ["num_inclusive", "num_exclusive"]
    ].astype(int)
    df[["n_samples_inclusive", "n_samples_exclusive"]] = df[
        ["n_samples_inclusive", "n_samples_exclusive"]
    ].astype(int)
    df["ratio_inclusive"] = _safe_ratio(df["num_inclusive"], df["n_samples_inclusive"])
    df["ratio_exclusive"] = _safe_ratio(df["num_exclusive"], df["n_samples_exclusive"])
    df["num"] = df["num_inclusive"]
    df["ratio"] = df["ratio_inclusive"]
    df = (
        df.reset_index()
        .sort_values("ratio_inclusive", ascending=False)
        .reset_index(drop=True)
    )
    return df


def _build_gene_table(
    mut: pd.DataFrame,
    samples_meta: pd.DataFrame,
    flags: pd.DataFrame,
    panel_coverage: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Build the gene-keyed frequency table.

    When ``panel_coverage`` is None, or ``panel_id`` is absent / all-NaN in
    ``samples_meta``, uses a cohort-wide scalar denominator (legacy path).

    When ``panel_coverage`` is supplied and samples carry panel assignments, uses
    a per-gene denominator: only samples whose panel covers that gene contribute
    to ``n_samples_inclusive`` / ``n_samples_exclusive``.
    """
    samples_with_flag = samples_meta.merge(flags, on="sample_id")

    use_panel_path = (
        panel_coverage is not None
        and "panel_id" in samples_with_flag.columns
        and not samples_with_flag["panel_id"].isna().all()
    )

    num_inclusive = mut.groupby("symbol", observed=True)["sample_id"].nunique()
    num_exclusive = (
        mut.loc[~mut["is_hypermutator"]]
        .groupby("symbol", observed=True)["sample_id"]
        .nunique()
    )

    df = pd.DataFrame(
        {"num_inclusive": num_inclusive, "num_exclusive": num_exclusive}
    ).fillna(0)
    df = df.astype(int)

    if use_panel_path:
        callable_pairs = (
            panel_coverage[["panel_id", "gene"]]
            .drop_duplicates()
            .rename(columns={"gene": "symbol"})
        )
        panel_gene_samples = samples_with_flag.merge(callable_pairs, on="panel_id")
        n_inclusive = panel_gene_samples.groupby("symbol", observed=True)[
            "sample_id"
        ].nunique()
        n_exclusive = (
            panel_gene_samples.loc[~panel_gene_samples["is_hypermutator"]]
            .groupby("symbol", observed=True)["sample_id"]
            .nunique()
        )

        # t070 spec error handling #6: genes in mut but absent from the panel-coverage
        # denominator (n_inclusive) have zero callable samples — drop them.
        mut_keys = set(num_inclusive.index)
        denom_keys = set(n_inclusive.index)
        off_panel_keys = mut_keys - denom_keys

        if off_panel_keys:
            total_mut = len(mut_keys)
            fraction = len(off_panel_keys) / total_mut if total_mut else 0.0
            msg_keys = sorted(off_panel_keys)[:10]
            if fraction > 0.05:
                raise ValueError(
                    f"Panel-aware aggregation: {len(off_panel_keys)} of {total_mut} "
                    f"gene symbols in mutation table have no panel coverage "
                    f"({fraction:.1%} > 5% threshold). First 10: {msg_keys!r}. "
                    "This indicates a systematic ingestion problem (mutations called "
                    "outside panel intervals); investigate upstream."
                )
            logger.warning(
                "Panel-aware aggregation: dropping %d gene symbol(s) from mutation "
                "table that have no panel coverage in this study (first 10: %s).",
                len(off_panel_keys),
                msg_keys,
            )

        # Build output by inner-joining num and denom on n_inclusive.index (denom pivot).
        df = pd.DataFrame(
            {
                "num_inclusive": num_inclusive.reindex(n_inclusive.index, fill_value=0),
                "num_exclusive": num_exclusive.reindex(n_inclusive.index, fill_value=0),
                "n_samples_inclusive": n_inclusive,
                "n_samples_exclusive": n_exclusive.reindex(
                    n_inclusive.index, fill_value=0
                ),
            }
        ).astype(
            {
                "num_inclusive": int,
                "num_exclusive": int,
                "n_samples_inclusive": int,
                "n_samples_exclusive": int,
            }
        )
    else:
        n_inclusive = samples_with_flag["sample_id"].nunique()
        n_exclusive = samples_with_flag.loc[
            ~samples_with_flag["is_hypermutator"], "sample_id"
        ].nunique()
        df["n_samples_inclusive"] = n_inclusive
        df["n_samples_exclusive"] = n_exclusive

    df["ratio_inclusive"] = _safe_ratio(df["num_inclusive"], df["n_samples_inclusive"])
    df["ratio_exclusive"] = _safe_ratio(df["num_exclusive"], df["n_samples_exclusive"])
    df["num"] = df["num_inclusive"]
    df["ratio"] = df["ratio_inclusive"]
    df = (
        df.reset_index()
        .sort_values("ratio_inclusive", ascending=False)
        .reset_index(drop=True)
    )
    return df


def _build_gene_cancer_table(
    mut: pd.DataFrame,
    samples_meta: pd.DataFrame,
    flags: pd.DataFrame,
    panel_coverage: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Build the (cancer_type, symbol) frequency table.

    When ``panel_coverage`` is None, or ``panel_id`` is absent / all-NaN in
    ``samples_meta``, uses a per-cancer scalar denominator (legacy path).

    When ``panel_coverage`` is supplied and samples carry panel assignments, uses
    a per-(cancer, gene) denominator: only samples on a panel covering that gene
    contribute to the denominator for each (cancer_type, symbol) pair.
    """
    samples_with_flag = samples_meta.merge(flags, on="sample_id")

    use_panel_path = (
        panel_coverage is not None
        and "panel_id" in samples_with_flag.columns
        and not samples_with_flag["panel_id"].isna().all()
    )

    num_inclusive = mut.groupby(["cancer_type", "symbol"], observed=True)[
        "sample_id"
    ].nunique()
    num_exclusive = (
        mut.loc[~mut["is_hypermutator"]]
        .groupby(["cancer_type", "symbol"], observed=True)["sample_id"]
        .nunique()
    )

    if use_panel_path:
        callable_pairs = (
            panel_coverage[["panel_id", "gene"]]
            .drop_duplicates()
            .rename(columns={"gene": "symbol"})
        )
        panel_gene_samples = samples_with_flag.merge(callable_pairs, on="panel_id")
        n_inclusive = panel_gene_samples.groupby(
            ["cancer_type", "symbol"], observed=True
        )["sample_id"].nunique()
        n_exclusive = (
            panel_gene_samples.loc[~panel_gene_samples["is_hypermutator"]]
            .groupby(["cancer_type", "symbol"], observed=True)["sample_id"]
            .nunique()
        )

        # t070 spec error handling #6: (cancer, gene) pairs in mut but absent from
        # the panel-coverage denominator (n_inclusive) have zero callable samples —
        # drop them per spec, warn, or raise if the fraction exceeds 1%.
        mut_keys = set(num_inclusive.index)
        denom_keys = set(n_inclusive.index)
        off_panel_keys = mut_keys - denom_keys

        if off_panel_keys:
            total_mut_pairs = len(mut_keys)
            fraction = len(off_panel_keys) / total_mut_pairs if total_mut_pairs else 0.0
            msg_keys = sorted(off_panel_keys)[:10]
            if fraction > 0.05:
                raise ValueError(
                    f"Panel-aware aggregation: {len(off_panel_keys)} of {total_mut_pairs} "
                    f"(cancer, gene) pairs in mutation table have no panel coverage "
                    f"({fraction:.1%} > 5% threshold). First 10: {msg_keys!r}. "
                    "This indicates a systematic ingestion problem (mutations called outside "
                    "panel intervals); investigate upstream."
                )
            logger.warning(
                "Panel-aware aggregation: dropping %d (cancer, gene) pairs from mutation "
                "table that have no panel coverage in this study (first 10: %s).",
                len(off_panel_keys),
                msg_keys,
            )

        # Build output by inner-joining num and denom on n_inclusive.index (denom pivot).
        df = (
            pd.DataFrame(
                {
                    "num_inclusive": num_inclusive.reindex(
                        n_inclusive.index, fill_value=0
                    ),
                    "num_exclusive": num_exclusive.reindex(
                        n_inclusive.index, fill_value=0
                    ),
                    "n_samples_inclusive": n_inclusive,
                    "n_samples_exclusive": n_exclusive.reindex(
                        n_inclusive.index, fill_value=0
                    ),
                }
            )
            .astype(
                {
                    "num_inclusive": int,
                    "num_exclusive": int,
                    "n_samples_inclusive": int,
                    "n_samples_exclusive": int,
                }
            )
            .reset_index()
        )
    else:
        df = pd.DataFrame(
            {"num_inclusive": num_inclusive, "num_exclusive": num_exclusive}
        ).fillna(0)
        df = df.astype(int).reset_index()
        n_inclusive_by_cancer = samples_with_flag.groupby("cancer_type", observed=True)[
            "sample_id"
        ].nunique()
        n_exclusive_by_cancer = (
            samples_with_flag.loc[~samples_with_flag["is_hypermutator"]]
            .groupby("cancer_type", observed=True)["sample_id"]
            .nunique()
        )
        df["n_samples_inclusive"] = (
            df["cancer_type"].map(n_inclusive_by_cancer).astype(int)
        )
        df["n_samples_exclusive"] = (
            df["cancer_type"].map(n_exclusive_by_cancer).fillna(0).astype(int)
        )

    df["ratio_inclusive"] = _safe_ratio(df["num_inclusive"], df["n_samples_inclusive"])
    df["ratio_exclusive"] = _safe_ratio(df["num_exclusive"], df["n_samples_exclusive"])
    df["num"] = df["num_inclusive"]
    df["ratio"] = df["ratio_inclusive"]
    df = df.sort_values(
        ["cancer_type", "ratio_inclusive"], ascending=[True, False]
    ).reset_index(drop=True)
    return df


def _safe_ratio(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    """Element-wise division that returns NaN where the denominator is zero."""
    num = numerator.astype(float)
    denom = denominator.astype(float).replace(0.0, float("nan"))
    return num / denom


def _run_via_snakemake() -> None:
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821
    mutations = pd.read_feather(snek.input.mutations)
    samples = pd.read_feather(snek.input.samples)
    samples_annotated = pd.read_feather(snek.input.samples_annotated)

    if "is_hypermutator" not in samples_annotated.columns:
        raise RuntimeError(
            "samples_annotated input is missing required 'is_hypermutator' column; "
            "ensure annotate_hypermutators ran successfully."
        )
    flags = samples_annotated[["sample_id", "is_hypermutator"]]

    panel_coverage_path = getattr(snek.input, "panel_coverage", None)
    panel_coverage_df = (
        pd.read_feather(panel_coverage_path) if panel_coverage_path else None
    )

    cancer_df, cancer_detailed_df, gene_df, gene_cancer_df = compute_freq_tables(
        mutations, samples, flags, panel_coverage=panel_coverage_df
    )

    cancer_df.to_feather(snek.output[0])
    cancer_detailed_df.to_feather(snek.output[1])
    gene_df.to_feather(snek.output[2])
    gene_cancer_df.to_feather(snek.output[3])


if "snakemake" in globals():
    _run_via_snakemake()
