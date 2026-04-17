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

Inputs
------
- ``snakemake.input[0]`` : per-study ``mut_filtered.feather``
- ``snakemake.input[1]`` : per-study ``samples.feather``
- ``snakemake.input.samples_annotated`` : cross-study ``samples_annotated.feather``
  produced by ``annotate_hypermutators``. The per-study step filters this by
  matching ``sample_id``.
"""


import pandas as pd


def compute_freq_tables(
    mutations: pd.DataFrame,
    samples: pd.DataFrame,
    hypermutator_flags: pd.DataFrame,
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

    Returns
    -------
    Tuple of four DataFrames keyed by ``cancer_type``, ``cancer_type_detailed``,
    ``symbol``, and ``(cancer_type, symbol)`` respectively.
    """
    mut = mutations[["symbol", "sample_id_tumor"]].rename(
        columns={"sample_id_tumor": "sample_id"}
    )
    samples_meta = samples[["sample_id", "cancer_type", "cancer_type_detailed"]]
    flags = _prepare_flags(hypermutator_flags, samples_meta)

    # Attach cancer type + hypermutator flag to each mutation row for grouping.
    mut = mut.merge(samples_meta, on="sample_id").merge(flags, on="sample_id")

    cancer_df = _build_single_key(
        mut=mut, samples_meta=samples_meta, flags=flags, key="cancer_type"
    )
    cancer_detailed_df = _build_single_key(
        mut=mut, samples_meta=samples_meta, flags=flags, key="cancer_type_detailed"
    )
    gene_df = _build_gene_table(mut=mut, samples_meta=samples_meta, flags=flags)
    gene_cancer_df = _build_gene_cancer_table(
        mut=mut, samples_meta=samples_meta, flags=flags
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
) -> pd.DataFrame:
    """Build the gene-keyed frequency table (global denominator is the whole cohort)."""
    samples_with_flag = samples_meta.merge(flags, on="sample_id")
    n_inclusive = samples_with_flag["sample_id"].nunique()
    n_exclusive = samples_with_flag.loc[
        ~samples_with_flag["is_hypermutator"], "sample_id"
    ].nunique()

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
) -> pd.DataFrame:
    """Build the (cancer_type, symbol) frequency table."""
    samples_with_flag = samples_meta.merge(flags, on="sample_id")

    n_inclusive_by_cancer = samples_with_flag.groupby("cancer_type", observed=True)[
        "sample_id"
    ].nunique()
    n_exclusive_by_cancer = (
        samples_with_flag.loc[~samples_with_flag["is_hypermutator"]]
        .groupby("cancer_type", observed=True)["sample_id"]
        .nunique()
    )

    num_inclusive = mut.groupby(["cancer_type", "symbol"], observed=True)[
        "sample_id"
    ].nunique()
    num_exclusive = (
        mut.loc[~mut["is_hypermutator"]]
        .groupby(["cancer_type", "symbol"], observed=True)["sample_id"]
        .nunique()
    )

    df = pd.DataFrame(
        {"num_inclusive": num_inclusive, "num_exclusive": num_exclusive}
    ).fillna(0)
    df = df.astype(int).reset_index()
    df["n_samples_inclusive"] = df["cancer_type"].map(n_inclusive_by_cancer).astype(int)
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
    mutations = pd.read_feather(snek.input[0])
    samples = pd.read_feather(snek.input[1])
    samples_annotated = pd.read_feather(snek.input.samples_annotated)

    if "is_hypermutator" not in samples_annotated.columns:
        raise RuntimeError(
            "samples_annotated input is missing required 'is_hypermutator' column; "
            "ensure annotate_hypermutators ran successfully."
        )
    flags = samples_annotated[["sample_id", "is_hypermutator"]]

    cancer_df, cancer_detailed_df, gene_df, gene_cancer_df = compute_freq_tables(
        mutations, samples, flags
    )

    cancer_df.to_feather(snek.output[0])
    cancer_detailed_df.to_feather(snek.output[1])
    gene_df.to_feather(snek.output[2])
    gene_cancer_df.to_feather(snek.output[3])


if "snakemake" in globals():
    _run_via_snakemake()
