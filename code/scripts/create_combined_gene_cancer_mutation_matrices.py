# science:code
# status: workflow-owned
# science:end
"""
create_combined_gene_cancer_mutation_matrices.py

Pivots the combined gene x cancer frequency tables (from
``create_combined_gene_cancer_freq_table``) into gene x cancer matrices — one
count matrix (sum-across-studies) and one ratio matrix (mean-across-studies),
both keyed on symbol (rows) by cancer_type (columns).

As of t098 part C / t081.7c, the script filters per-study columns to the
**inclusive view only** (skipping the ``{study}_exclusive`` paired columns and
the new callability / mean metadata columns). Producing an exclusive-view
matrix variant is a follow-up — downstream consumers (clustering, summary
report) read the inclusive matrix at present.

Inputs
------
- ``snakemake.input[0]`` : ``summary/mut/table/gene_cancer_study.feather``
  (counts; per-study inclusive + exclusive + metadata columns).
- ``snakemake.input[1]`` : ``summary/mut/table/gene_cancer_study_ratio.feather``
  (ratios; per-study inclusive + exclusive + metadata columns).

Outputs
-------
- ``snakemake.output[0]`` : ``summary/mut/matrix/gene_cancer.feather`` —
  counts matrix (gene rows x cancer cols), summed across per-study inclusive
  columns.
- ``snakemake.output[1]`` : ``summary/mut/matrix/gene_cancer_ratio.feather`` —
  ratio matrix (gene rows x cancer cols), averaged across per-study
  inclusive columns.
"""

import pandas as pd


_RESERVED_COLUMNS: frozenset[str] = frozenset(
    {
        "cancer_type",
        "symbol",
        "mean",
        "mean_adj",
        "mean_inclusive",
        "mean_exclusive",
        "n_total_studies",
        "n_contributing_studies",
        "n_panel_covered_studies",
        "callable_fraction",
    }
)


def _per_study_columns(df: pd.DataFrame) -> list[str]:
    """Return the inclusive-view per-study column names in ``df``.

    A per-study inclusive slot is the bare ``{study}`` column, identified
    structurally by the presence of its paired ``{study}_exclusive`` twin.
    Saturation / callability / metadata columns (``cancer_saturation_status``,
    ``lawrence2014_*``, ``n_*``, ``*_inclusive``) never carry that twin and are
    excluded. This is robust to new metadata columns being added upstream by
    ``create_combined_gene_cancer_freq_table`` — unlike a hardcoded skip-list,
    which silently drifts and (for string columns) breaks the numeric aggregate.
    """
    columns = set(df.columns)
    return [
        c
        for c in df.columns
        if c not in _RESERVED_COLUMNS
        and not c.endswith("_exclusive")
        and not c.endswith("_inclusive")
        and f"{c}_exclusive" in columns
    ]


def aggregate_matrix(df: pd.DataFrame, agg: str) -> pd.DataFrame:
    """Aggregate per-study inclusive columns into a gene x cancer_type matrix.

    ``agg`` is ``"sum"`` (for count matrices) or ``"mean"`` (for ratio matrices).
    """
    cols = _per_study_columns(df)
    per_study = df[cols]
    if agg == "sum":
        aggregated = per_study.sum(axis=1)
        value_name = "num"
    elif agg == "mean":
        aggregated = per_study.mean(axis=1)
        value_name = "ratio"
    else:
        raise ValueError(f"agg must be 'sum' or 'mean'; got {agg!r}")
    long_df = pd.DataFrame(
        {
            "cancer_type": df["cancer_type"],
            "symbol": df["symbol"],
            value_name: aggregated,
        }
    )
    return long_df.pivot_table(
        index="symbol", columns="cancer_type", values=value_name, fill_value=0
    )


def _run_via_snakemake() -> None:
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821

    count_df = pd.read_feather(snek.input[0])
    count_mat = aggregate_matrix(count_df, agg="sum")
    count_mat.reset_index().to_feather(snek.output[0])

    ratio_df = pd.read_feather(snek.input[1])
    ratio_mat = aggregate_matrix(ratio_df, agg="mean")
    ratio_mat.reset_index().to_feather(snek.output[1])


if "snakemake" in globals():
    _run_via_snakemake()
