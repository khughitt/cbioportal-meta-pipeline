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
    rows: list[tuple[str, str, int, int, float, float, int, int]],
) -> pd.DataFrame:
    """Rows are ``(cancer_type, symbol, num_inclusive, num_exclusive,
    ratio_inclusive, ratio_exclusive, n_samples_inclusive, n_samples_exclusive)``."""
    return pd.DataFrame.from_records(
        rows,
        columns=[
            "cancer_type",
            "symbol",
            "num_inclusive",
            "num_exclusive",
            "ratio_inclusive",
            "ratio_exclusive",
            "n_samples_inclusive",
            "n_samples_exclusive",
        ],
    )


def test_pivot_emits_paired_per_study_columns() -> None:
    study_a = _per_study_frame([("A", "G", 10, 8, 0.10, 0.08, 100, 80)])
    study_b = _per_study_frame([("A", "G", 20, 19, 0.20, 0.19, 100, 95)])
    num_df, ratio_df, _, _ = combine_paired_pivot(
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
    study_a = _per_study_frame([("A", "G", 10, 8, 0.10, 0.08, 100, 80)])
    study_b = _per_study_frame([("A", "G", 20, 16, 0.20, 0.16, 100, 100)])
    _, ratio_df, _, _ = combine_paired_pivot([("a", study_a), ("b", study_b)])
    row = ratio_df.reset_index().iloc[0]
    assert row["mean_inclusive"] == pytest.approx(0.15)
    assert row["mean_exclusive"] == pytest.approx(0.12)


def test_mean_legacy_alias_equals_mean_inclusive() -> None:
    # Kept for backward compat until downstream consumers migrate; documented
    # deviation from plan review finding #3.
    study_a = _per_study_frame([("A", "G", 10, 10, 0.10, 0.10, 100, 100)])
    _, ratio_df, _, _ = combine_paired_pivot([("a", study_a)])
    row = ratio_df.reset_index().iloc[0]
    assert row["mean"] == row["mean_inclusive"]


def test_no_hypermutator_regression_mean_inclusive_eq_mean_exclusive() -> None:
    # When no hypermutators exist in any study, inclusive and exclusive stats
    # are bitwise identical.
    study_a = _per_study_frame(
        [
            ("A", "G1", 10, 10, 0.10, 0.10, 100, 100),
            ("A", "G2", 5, 5, 0.05, 0.05, 100, 100),
        ]
    )
    study_b = _per_study_frame(
        [
            ("A", "G1", 20, 20, 0.20, 0.20, 100, 100),
            ("A", "G2", 8, 8, 0.08, 0.08, 100, 100),
        ]
    )
    num_df, ratio_df, _, _ = combine_paired_pivot([("a", study_a), ("b", study_b)])
    # mean_inclusive == mean_exclusive bitwise for every row.
    assert (ratio_df["mean_inclusive"] == ratio_df["mean_exclusive"]).all()
    # Per-study inclusive == exclusive bitwise.
    assert (num_df["a"] == num_df["a_exclusive"]).all()
    assert (num_df["b"] == num_df["b_exclusive"]).all()


def test_per_study_columns_carry_inclusive_values_in_legacy_slot() -> None:
    study_a = _per_study_frame([("A", "G", 7, 3, 0.70, 0.30, 10, 10)])
    num_df, ratio_df, _, _ = combine_paired_pivot([("study_a", study_a)])
    row_num = num_df.reset_index().iloc[0]
    row_ratio = ratio_df.reset_index().iloc[0]
    assert row_num["study_a"] == 7
    assert row_num["study_a_exclusive"] == 3
    assert row_ratio["study_a"] == pytest.approx(0.70)
    assert row_ratio["study_a_exclusive"] == pytest.approx(0.30)


def test_mean_columns_skip_missing_values() -> None:
    # Study A has a row for G; study B does not (NaN). Mean over one non-NaN
    # value equals that value.
    study_a = _per_study_frame([("A", "G", 10, 8, 0.10, 0.08, 100, 80)])
    study_b = _per_study_frame([])  # no rows at all
    _, ratio_df, _, _ = combine_paired_pivot([("a", study_a), ("b", study_b)])
    row = ratio_df.reset_index().iloc[0]
    assert row["mean_inclusive"] == pytest.approx(0.10)
    assert row["mean_exclusive"] == pytest.approx(0.08)


def test_output_indexed_on_cancer_type_and_symbol() -> None:
    study_a = _per_study_frame(
        [
            ("A", "G1", 1, 1, 0.1, 0.1, 10, 10),
            ("B", "G1", 2, 2, 0.2, 0.2, 10, 10),
        ]
    )
    num_df, ratio_df, _, _ = combine_paired_pivot([("a", study_a)])
    assert num_df.index.names == ["cancer_type", "symbol"]
    assert ratio_df.index.names == ["cancer_type", "symbol"]


def test_paired_panel_covered_samples_columns() -> None:
    """t070: paired n_panel_covered_samples_{inclusive,exclusive} columns must
    sum per-study panel-restricted denominators across studies; differ by the
    count of panel-callable hypermutators."""
    # Two studies in Cancer X. Study A has 10 inclusive samples for GENE1
    # (8 exclusive — 2 hypermutators), Study B has 8 inclusive (8 exclusive — no hyper).
    # GENE2 only on Study A's panel (6 inclusive samples).
    study_a = _per_study_frame(
        [
            ("Cancer X", "GENE1", 5, 4, 0.5, 0.5, 10, 8),
            ("Cancer X", "GENE2", 2, 2, 0.333, 0.333, 6, 6),
        ]
    )
    study_b = _per_study_frame(
        [
            ("Cancer X", "GENE1", 3, 3, 0.375, 0.375, 8, 8),
        ]
    )

    from create_combined_gene_cancer_freq_table import (
        _annotate_callability,
        combine_paired_pivot,
    )

    num_df, ratio_df, n_incl_df, n_excl_df = combine_paired_pivot(
        [("study_a", study_a), ("study_b", study_b)]
    )

    panel_coverage = pd.DataFrame(
        {
            "panel_id": ["PANEL_A", "PANEL_A", "PANEL_B"],
            "gene": ["GENE1", "GENE2", "GENE1"],
        }
    )
    num_out, ratio_out = _annotate_callability(
        num_df,
        ratio_df,
        studies=["study_a", "study_b"],
        panel_coverage=panel_coverage,
        study_panel_map={"study_a": "PANEL_A", "study_b": "PANEL_B"},
        n_inclusive_df=n_incl_df,
        n_exclusive_df=n_excl_df,
    )

    g1 = ratio_out.loc[("Cancer X", "GENE1")]
    # Per-study denominators sum: 10 + 8 = 18 inclusive, 8 + 8 = 16 exclusive
    assert g1["n_panel_covered_samples_inclusive"] == 18
    assert g1["n_panel_covered_samples_exclusive"] == 16
    assert (
        g1["n_panel_covered_samples_inclusive"]
        - g1["n_panel_covered_samples_exclusive"]
    ) == 2  # 2 panel-callable hypermutators (in study_a)

    # GENE2 only present in study_a (NaN in study_b column).
    g2 = ratio_out.loc[("Cancer X", "GENE2")]
    assert g2["n_panel_covered_samples_inclusive"] == 6
    assert g2["n_panel_covered_samples_exclusive"] == 6


def test_callable_sample_fraction_uses_per_cancer_denominator() -> None:
    """t070: callable_sample_fraction is per-cancer (sum of cohort sizes for
    that cancer across studies), not global."""
    # Two cancers, two studies.
    study_a = _per_study_frame(
        [
            ("Cancer X", "GENE1", 5, 5, 0.5, 0.5, 10, 10),
            ("Cancer Y", "GENE1", 3, 3, 0.5, 0.5, 6, 6),
        ]
    )
    study_b = _per_study_frame(
        [
            ("Cancer X", "GENE1", 4, 4, 0.5, 0.5, 8, 8),
            ("Cancer Y", "GENE1", 2, 2, 0.5, 0.5, 4, 4),
        ]
    )

    from create_combined_gene_cancer_freq_table import (
        _annotate_callability,
        combine_paired_pivot,
    )

    num_df, ratio_df, n_incl_df, n_excl_df = combine_paired_pivot(
        [("study_a", study_a), ("study_b", study_b)]
    )
    panel_coverage = pd.DataFrame(
        {
            "panel_id": ["PANEL_A", "PANEL_B"],
            "gene": ["GENE1", "GENE1"],
        }
    )
    _, ratio_out = _annotate_callability(
        num_df,
        ratio_df,
        studies=["study_a", "study_b"],
        panel_coverage=panel_coverage,
        study_panel_map={"study_a": "PANEL_A", "study_b": "PANEL_B"},
        n_inclusive_df=n_incl_df,
        n_exclusive_df=n_excl_df,
    )

    # Cancer X: total samples = 10 + 8 = 18; covered samples = 18 → fraction = 1.0
    # Cancer Y: total samples = 6 + 4 = 10; covered samples = 10 → fraction = 1.0
    cx = ratio_out.loc[("Cancer X", "GENE1")]
    cy = ratio_out.loc[("Cancer Y", "GENE1")]
    assert cx["callable_sample_fraction_inclusive"] == pytest.approx(1.0)
    assert cy["callable_sample_fraction_inclusive"] == pytest.approx(1.0)
