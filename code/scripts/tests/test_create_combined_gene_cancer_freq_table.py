"""Tests for ``create_combined_gene_cancer_freq_table.combine_paired_pivot``.

Specification is task 7b of the t081 plan at ``doc/plans/2026-04-13-t081-
hypermutator-annotation-pipeline-plan.md``. The combined step must pivot the
paired inclusive/exclusive per-study columns produced by t098 part A into
cross-study wide-format feathers with paired pooled mean columns.
"""

import pandas as pd
import pytest

from create_combined_gene_cancer_freq_table import combine_paired_pivot


def _per_study_frame(
    rows: list[tuple[str, str, int, int, float, float]],
) -> pd.DataFrame:
    """Rows are ``(cancer_type, symbol, num_inclusive, num_exclusive,
    ratio_inclusive, ratio_exclusive)``."""
    return pd.DataFrame.from_records(
        rows,
        columns=[
            "cancer_type",
            "symbol",
            "num_inclusive",
            "num_exclusive",
            "ratio_inclusive",
            "ratio_exclusive",
        ],
    )


def test_pivot_emits_paired_per_study_columns() -> None:
    study_a = _per_study_frame([("A", "G", 10, 8, 0.10, 0.08)])
    study_b = _per_study_frame([("A", "G", 20, 19, 0.20, 0.19)])
    num_df, ratio_df = combine_paired_pivot(
        [("study_a", study_a), ("study_b", study_b)]
    )

    # Legacy column per study is the inclusive variant for backward compat.
    assert "study_a" in num_df.columns
    assert "study_b" in num_df.columns
    # Plus explicit _exclusive columns.
    assert "study_a_exclusive" in num_df.columns
    assert "study_b_exclusive" in num_df.columns
    assert "study_a" in ratio_df.columns
    assert "study_b" in ratio_df.columns
    assert "study_a_exclusive" in ratio_df.columns
    assert "study_b_exclusive" in ratio_df.columns


def test_mean_inclusive_and_mean_exclusive_pooled_across_studies() -> None:
    study_a = _per_study_frame([("A", "G", 10, 8, 0.10, 0.08)])
    study_b = _per_study_frame([("A", "G", 20, 16, 0.20, 0.16)])
    _, ratio_df = combine_paired_pivot([("a", study_a), ("b", study_b)])
    row = ratio_df.reset_index().iloc[0]
    assert row["mean_inclusive"] == pytest.approx(0.15)
    assert row["mean_exclusive"] == pytest.approx(0.12)


def test_mean_legacy_alias_equals_mean_inclusive() -> None:
    # Kept for backward compat until downstream consumers migrate; documented
    # deviation from plan review finding #3.
    study_a = _per_study_frame([("A", "G", 10, 10, 0.10, 0.10)])
    _, ratio_df = combine_paired_pivot([("a", study_a)])
    row = ratio_df.reset_index().iloc[0]
    assert row["mean"] == row["mean_inclusive"]


def test_no_hypermutator_regression_mean_inclusive_eq_mean_exclusive() -> None:
    # When no hypermutators exist in any study, inclusive and exclusive stats
    # are bitwise identical.
    study_a = _per_study_frame(
        [
            ("A", "G1", 10, 10, 0.10, 0.10),
            ("A", "G2", 5, 5, 0.05, 0.05),
        ]
    )
    study_b = _per_study_frame(
        [
            ("A", "G1", 20, 20, 0.20, 0.20),
            ("A", "G2", 8, 8, 0.08, 0.08),
        ]
    )
    num_df, ratio_df = combine_paired_pivot([("a", study_a), ("b", study_b)])
    # mean_inclusive == mean_exclusive bitwise for every row.
    assert (ratio_df["mean_inclusive"] == ratio_df["mean_exclusive"]).all()
    # Per-study inclusive == exclusive bitwise.
    assert (num_df["a"] == num_df["a_exclusive"]).all()
    assert (num_df["b"] == num_df["b_exclusive"]).all()


def test_per_study_columns_carry_inclusive_values_in_legacy_slot() -> None:
    study_a = _per_study_frame([("A", "G", 7, 3, 0.70, 0.30)])
    num_df, ratio_df = combine_paired_pivot([("study_a", study_a)])
    row_num = num_df.reset_index().iloc[0]
    row_ratio = ratio_df.reset_index().iloc[0]
    assert row_num["study_a"] == 7
    assert row_num["study_a_exclusive"] == 3
    assert row_ratio["study_a"] == pytest.approx(0.70)
    assert row_ratio["study_a_exclusive"] == pytest.approx(0.30)


def test_mean_columns_skip_missing_values() -> None:
    # Study A has a row for G; study B does not (NaN). Mean over one non-NaN
    # value equals that value.
    study_a = _per_study_frame([("A", "G", 10, 8, 0.10, 0.08)])
    study_b = _per_study_frame([])  # no rows at all
    _, ratio_df = combine_paired_pivot([("a", study_a), ("b", study_b)])
    row = ratio_df.reset_index().iloc[0]
    assert row["mean_inclusive"] == pytest.approx(0.10)
    assert row["mean_exclusive"] == pytest.approx(0.08)


def test_output_indexed_on_cancer_type_and_symbol() -> None:
    study_a = _per_study_frame(
        [
            ("A", "G1", 1, 1, 0.1, 0.1),
            ("B", "G1", 2, 2, 0.2, 0.2),
        ]
    )
    num_df, ratio_df = combine_paired_pivot([("a", study_a)])
    assert num_df.index.names == ["cancer_type", "symbol"]
    assert ratio_df.index.names == ["cancer_type", "symbol"]
