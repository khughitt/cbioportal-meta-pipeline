# science:code
# status: library
# science:end
"""Tests for ``create_combined_gene_cancer_mutation_matrices._per_study_columns``.

t098 part C: the matrices step must skip the paired ``_exclusive`` per-study
columns and the new callability metadata so that the inclusive-view matrix
is not double-counted nor polluted with metadata.
"""

import pandas as pd
import pytest

from create_combined_gene_cancer_mutation_matrices import (
    _per_study_columns,
    aggregate_matrix,
)


def test_per_study_columns_skip_exclusive_suffix() -> None:
    df = pd.DataFrame(columns=["cancer_type", "symbol", "study_a", "study_a_exclusive"])
    assert _per_study_columns(df) == ["study_a"]


def test_per_study_columns_skip_means_and_callability_metadata() -> None:
    df = pd.DataFrame(
        columns=[
            "cancer_type",
            "symbol",
            "study_a",
            "study_b",
            "mean",
            "mean_adj",
            "mean_inclusive",
            "mean_exclusive",
            "n_total_studies",
            "n_contributing_studies",
            "n_panel_covered_studies",
            "callable_fraction",
        ]
    )
    assert _per_study_columns(df) == ["study_a", "study_b"]


def test_aggregate_matrix_sum_over_inclusive_only() -> None:
    df = pd.DataFrame(
        {
            "cancer_type": ["A", "A"],
            "symbol": ["G1", "G2"],
            "study_a": [3, 4],
            "study_a_exclusive": [1, 2],
            "study_b": [5, 6],
            "study_b_exclusive": [2, 3],
            "mean_inclusive": [4.0, 5.0],
            "mean_exclusive": [1.5, 2.5],
        }
    )
    mat = aggregate_matrix(df, agg="sum")
    # G1 row: 3 + 5 = 8 in cancer A; _exclusive slots skipped.
    assert mat.loc["G1", "A"] == 8
    assert mat.loc["G2", "A"] == 10


def test_aggregate_matrix_mean_over_inclusive_only() -> None:
    df = pd.DataFrame(
        {
            "cancer_type": ["A"],
            "symbol": ["G"],
            "study_a": [0.10],
            "study_a_exclusive": [0.05],
            "study_b": [0.20],
            "study_b_exclusive": [0.10],
        }
    )
    mat = aggregate_matrix(df, agg="mean")
    # (0.10 + 0.20) / 2 = 0.15; exclusive slots skipped.
    assert mat.loc["G", "A"] == pytest.approx(0.15)
