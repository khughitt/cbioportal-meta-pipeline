"""
create_combined_gene_cancer_freq_table.py

Concatenates per-study gene x cancer mutation frequency tables into cross-study
wide-format feathers keyed by (cancer_type, symbol).

As of t098 part B / t081.7b, each per-study input is expected to carry paired
inclusive / exclusive columns (``num_inclusive``, ``num_exclusive``,
``ratio_inclusive``, ``ratio_exclusive``) produced by ``create_freq_tables.py``
once the hypermutator-annotation step (t097) has landed. The combined output
preserves that paired structure: every per-study column exists twice — once as
the legacy backward-compat name ``{study_id}`` (the inclusive view) and once
as ``{study_id}_exclusive`` (the hypermutator-excluded view). Two pooled-mean
columns (``mean_inclusive``, ``mean_exclusive``) are emitted alongside the
legacy ``mean`` / ``mean_adj`` aliases.

Deviation from plan review finding #3 (2026-04-14): the plan specifies
dropping the legacy ``mean`` column entirely to force consumers to pick
``mean_inclusive`` or ``mean_exclusive`` explicitly. We currently keep the
``mean`` / ``mean_adj`` aliases for backward compatibility with downstream
consumers (``annotate.py``, ``annotate_ch.py``, the R summary report) that
have not yet migrated. A follow-up task will drop the aliases once those
consumers are updated.

Outputs:
  - ``gene_cancer_study.feather``       : per-study mutation counts (num) with
                                          paired inclusive/exclusive columns
                                          plus callability metadata.
  - ``gene_cancer_study_ratio.feather`` : per-study mutation ratios with
                                          paired inclusive/exclusive columns,
                                          ``mean_inclusive`` / ``mean_exclusive``
                                          plus legacy ``mean`` / ``mean_adj``
                                          and callability metadata.

Callability annotation columns (closes audit F2 partially; unchanged from the
pre-t098 pass):

  - ``n_total_studies``           : total number of studies in the aggregation.
  - ``n_contributing_studies``    : count of per-study inclusive columns with
                                    a non-null value for this row.
  - ``n_panel_covered_studies``   : number of studies whose panel covers this
                                    gene (GENIE + ``study_panel_map``).
  - ``callable_fraction``         : ``n_panel_covered_studies / n_total_studies``.

Config
------
- ``study_panel_map`` (``dict[str, str]``): optional. Studies listed here are
  treated as panel-restricted; studies not in the map are treated as WES.
"""

from __future__ import annotations

import os
import sys

import pandas as pd


def combine_paired_pivot(
    per_study_frames: list[tuple[str, pd.DataFrame]],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Pivot per-study paired columns into cross-study wide-format DataFrames.

    Input: list of ``(study_id, frame)`` pairs. Each ``frame`` must have
    ``cancer_type``, ``symbol``, ``num_inclusive``, ``num_exclusive``,
    ``ratio_inclusive``, ``ratio_exclusive`` columns.

    Returns ``(num_df, ratio_df)``. Both are indexed on
    ``(cancer_type, symbol)``. Per-study columns appear twice: ``{study_id}``
    (= inclusive, legacy-compat) and ``{study_id}_exclusive``. ``ratio_df``
    additionally carries ``mean_inclusive`` and ``mean_exclusive`` (row-wise
    mean across per-study columns of the matching variant, NaN-skipping) plus
    legacy ``mean`` (= ``mean_inclusive``).
    """
    num_frames: list[pd.DataFrame] = []
    ratio_frames: list[pd.DataFrame] = []
    for study_id, frame in per_study_frames:
        if frame.empty:
            continue
        indexed = frame.set_index(["cancer_type", "symbol"])
        num_frames.append(
            pd.DataFrame(
                {
                    study_id: indexed["num_inclusive"],
                    f"{study_id}_exclusive": indexed["num_exclusive"],
                }
            )
        )
        ratio_frames.append(
            pd.DataFrame(
                {
                    study_id: indexed["ratio_inclusive"],
                    f"{study_id}_exclusive": indexed["ratio_exclusive"],
                }
            )
        )

    if not num_frames:
        empty_index = pd.MultiIndex.from_tuples([], names=["cancer_type", "symbol"])
        return (
            pd.DataFrame(index=empty_index),
            pd.DataFrame(index=empty_index),
        )

    num_df = pd.concat(num_frames, axis=1)
    ratio_df = pd.concat(ratio_frames, axis=1)

    inclusive_ratio_cols = [c for c in ratio_df.columns if not c.endswith("_exclusive")]
    exclusive_ratio_cols = [c for c in ratio_df.columns if c.endswith("_exclusive")]
    ratio_df["mean_inclusive"] = ratio_df[inclusive_ratio_cols].mean(
        axis=1, skipna=True
    )
    ratio_df["mean_exclusive"] = ratio_df[exclusive_ratio_cols].mean(
        axis=1, skipna=True
    )
    # Legacy alias (deviation from plan review finding #3; see module docstring).
    ratio_df["mean"] = ratio_df["mean_inclusive"]

    return num_df, ratio_df


def _annotate_callability(
    num_df: pd.DataFrame,
    ratio_df: pd.DataFrame,
    studies: list[str],
    panel_coverage: pd.DataFrame,
    study_panel_map: dict[str, str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Attach n_total_studies / n_contributing_studies / n_panel_covered_studies /
    callable_fraction columns to both num_df and ratio_df."""
    gene_to_panels: dict[str, set[str]] = (
        panel_coverage.groupby("gene")["panel_id"].apply(lambda s: set(s)).to_dict()
    )
    n_total_studies = len(studies)
    gene_symbols_in_output = (
        ratio_df.index.get_level_values("symbol").astype(str).str.upper()
    )

    def _count_covered(gene_upper: str) -> int:
        covering = 0
        covering_panels = gene_to_panels.get(gene_upper, set())
        for study in studies:
            panel = study_panel_map.get(study)
            if panel is None or panel in covering_panels:
                covering += 1
        return covering

    unique_genes = pd.Series(gene_symbols_in_output.unique())
    unique_gene_cov = {g: _count_covered(g) for g in unique_genes}
    n_panel_covered_per_row = gene_symbols_in_output.map(unique_gene_cov).astype(int)

    inclusive_cols = [c for c in ratio_df.columns if c in studies]
    n_contributing_per_row = ratio_df[inclusive_cols].notna().sum(axis=1).astype(int)

    for df in (num_df, ratio_df):
        df["n_total_studies"] = n_total_studies
        df["n_panel_covered_studies"] = n_panel_covered_per_row.to_numpy()
        df["callable_fraction"] = df["n_panel_covered_studies"] / n_total_studies
    num_df["n_contributing_studies"] = (
        num_df[inclusive_cols].notna().sum(axis=1).astype(int).to_numpy()
    )
    ratio_df["n_contributing_studies"] = n_contributing_per_row.to_numpy()

    return num_df, ratio_df


def _protein_length_adjusted(
    ratio_df: pd.DataFrame, protein_lengths: pd.DataFrame
) -> pd.DataFrame:
    """Attach ``mean_adj`` (== ``mean_inclusive`` / protein_length, NaN-filled with median)."""
    plengths = protein_lengths[
        protein_lengths.symbol.isin(ratio_df.index.get_level_values("symbol"))
    ].set_index("symbol")
    median_length = float(plengths["length"].astype(float).median())
    mean_mi = ratio_df["mean_inclusive"]
    merged = pd.merge(mean_mi, plengths, left_index=True, right_index=True, how="left")
    merged["length"] = merged["length"].astype(float).fillna(median_length)
    ratio_df["mean_adj"] = merged["mean_inclusive"] / merged["length"]
    return ratio_df


def _run_via_snakemake() -> None:
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821

    per_study_paths: list[str] = list(snek.input.per_study)
    protein_lengths_path: str = snek.input.protein_lengths
    panel_coverage_path: str = snek.input.panel_coverage

    frames: list[tuple[str, pd.DataFrame]] = []
    studies: list[str] = []
    for infile in per_study_paths:
        df = pd.read_feather(infile)
        study = os.path.basename(
            os.path.dirname(os.path.dirname(os.path.dirname(infile)))
        )
        studies.append(study)
        frames.append((study, df))

    num_df, ratio_df = combine_paired_pivot(frames)

    # Sort by mean_inclusive descending for stable ranking.
    ratio_df = ratio_df.sort_values("mean_inclusive", ascending=False)
    num_df = num_df.reindex(ratio_df.index)

    ratio_df = _protein_length_adjusted(ratio_df, pd.read_feather(protein_lengths_path))

    panel_coverage = pd.read_feather(panel_coverage_path)
    study_panel_map: dict[str, str] = snek.config.get("study_panel_map", {}) or {}
    num_df, ratio_df = _annotate_callability(
        num_df, ratio_df, studies, panel_coverage, study_panel_map
    )

    num_df = num_df.reset_index()
    ratio_df = ratio_df.reset_index()

    num_df = num_df.astype({"cancer_type": "category", "symbol": "category"})
    ratio_df = ratio_df.astype({"cancer_type": "category", "symbol": "category"})

    num_df.to_feather(snek.output[0])
    ratio_df.to_feather(snek.output[1])

    n_mapped = sum(1 for s in studies if s in study_panel_map)
    print(
        f"Callability annotation: {len(studies)} studies total "
        f"({n_mapped} mapped to a GENIE panel, {len(studies) - n_mapped} treated as WES). "
        f"Median per-gene callable_fraction = {ratio_df['callable_fraction'].median():.3f}. "
        f"Hypermutator-paired columns emitted: mean_inclusive + mean_exclusive.",
        file=sys.stderr,
    )


if "snakemake" in globals():
    _run_via_snakemake()
