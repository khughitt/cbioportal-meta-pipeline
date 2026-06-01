# science:code
# status: library
# science:end
"""Tests for H10 treatment-aware per-study frequency views."""

from __future__ import annotations

import pandas as pd
import pytest

from create_freq_tables import compute_freq_tables
from create_h10_treatment_freq_tables import (
    COHORT_VIEWS,
    compute_h10_treatment_freq_table,
)


def _muts(rows: list[tuple[str, str]]) -> pd.DataFrame:
    return pd.DataFrame.from_records(rows, columns=["symbol", "sample_id_tumor"])


def _samples(rows: list[tuple[str, str, str]]) -> pd.DataFrame:
    return pd.DataFrame.from_records(
        rows, columns=["sample_id", "cancer_type", "cancer_type_detailed"]
    )


def _treatment(
    rows: list[tuple[str, bool, bool, bool, bool, bool, bool]],
) -> pd.DataFrame:
    return pd.DataFrame.from_records(
        rows,
        columns=[
            "sample_id",
            "is_hypermutator",
            "treatment_exposed_broad",
            "mutagenic_treatment_signal",
            "mutagenic_treatment_signal_sensitivity_only",
            "positive_naive_or_pretreatment",
            "treatment_metadata_unknown",
        ],
    )


def test_all_samples_reproduces_canonical_gene_cancer_frequency_columns() -> None:
    muts = _muts(
        [
            ("TP53", "S1"),
            ("TP53", "S2"),
            ("TP53", "S6"),
            ("BRAF", "S3"),
        ]
    )
    samples = _samples(
        [
            ("S1", "Cancer A", "A"),
            ("S2", "Cancer A", "A"),
            ("S3", "Cancer B", "B"),
            ("S4", "Cancer A", "A"),
            ("S5", "Cancer B", "B"),
            ("S6", "Cancer A", "A"),
        ]
    )
    treatment = _treatment(
        [
            ("S1", False, False, False, False, False, False),
            ("S2", False, True, True, False, False, False),
            ("S3", False, False, False, True, False, False),
            ("S4", False, False, False, False, True, False),
            ("S5", False, False, False, False, False, True),
            ("S6", True, False, False, False, False, False),
        ]
    )

    _, _, _, canonical = compute_freq_tables(
        muts,
        samples,
        treatment[["sample_id", "is_hypermutator"]],
    )
    h10 = compute_h10_treatment_freq_table(muts, samples, treatment)
    all_samples = h10.loc[h10["cohort_view"] == "all_samples"]

    merged = canonical.merge(
        all_samples, on=["cancer_type", "symbol"], suffixes=("_canonical", "_h10")
    )
    assert len(merged) == len(canonical)
    assert (merged["num_h10"] == merged["num_inclusive"]).all()
    assert (merged["n_samples"] == merged["n_samples_inclusive"]).all()
    assert (merged["ratio_h10"] == merged["ratio_inclusive"]).all()
    assert (merged["num_hypermutator_excluded"] == merged["num_exclusive"]).all()
    assert (
        merged["n_samples_hypermutator_excluded"] == merged["n_samples_exclusive"]
    ).all()
    assert (merged["ratio_hypermutator_excluded"] == merged["ratio_exclusive"]).all()


def test_treatment_cohort_views_apply_distinct_denominator_semantics() -> None:
    muts = _muts(
        [
            ("TP53", "S1"),
            ("TP53", "S2"),
            ("TP53", "S6"),
            ("BRAF", "S3"),
        ]
    )
    samples = _samples(
        [
            ("S1", "Cancer A", "A"),
            ("S2", "Cancer A", "A"),
            ("S3", "Cancer B", "B"),
            ("S4", "Cancer A", "A"),
            ("S5", "Cancer B", "B"),
            ("S6", "Cancer A", "A"),
        ]
    )
    treatment = _treatment(
        [
            ("S1", False, False, False, False, False, False),
            ("S2", False, True, True, False, False, False),
            ("S3", False, False, False, True, False, False),
            ("S4", False, False, False, False, True, False),
            ("S5", False, False, False, False, False, True),
            ("S6", True, False, False, False, False, False),
        ]
    )

    out = compute_h10_treatment_freq_table(muts, samples, treatment)

    assert set(out["cohort_view"]) == set(COHORT_VIEWS)

    tp53_no_detected = _row(out, "Cancer A", "TP53", "no_detected_treatment_signal")
    assert (
        tp53_no_detected["n_samples"] == 3
    )  # S1 + positive-naive S4 + hypermutator S6
    assert tp53_no_detected["num"] == 2
    assert tp53_no_detected["n_samples_hypermutator_excluded"] == 2
    assert tp53_no_detected["num_hypermutator_excluded"] == 1

    tp53_confirmed_naive = _row(
        out, "Cancer A", "TP53", "confirmed_naive_or_pretreatment"
    )
    assert tp53_confirmed_naive["n_samples"] == 1
    assert tp53_confirmed_naive["num"] == 0
    assert tp53_confirmed_naive["ratio"] == 0.0

    braf_primary = _row(out, "Cancer B", "BRAF", "mutagenic_treatment_excluded_primary")
    assert (
        braf_primary["n_samples"] == 2
    )  # PDX sensitivity-only S3 is retained in primary view.
    assert braf_primary["num"] == 1

    braf_pdx_sensitivity = _row(
        out, "Cancer B", "BRAF", "mutagenic_treatment_excluded_with_pdx_sensitivity"
    )
    assert braf_pdx_sensitivity["n_samples"] == 1  # S3 excluded; unknown S5 remains.
    assert braf_pdx_sensitivity["num"] == 0


def test_panel_aware_exclusion_can_emit_zero_denominator_nan_ratio() -> None:
    muts = _muts([("GENE_B", "S2")])
    samples = pd.DataFrame(
        {
            "sample_id": ["S1", "S2", "S3"],
            "cancer_type": ["Cancer A", "Cancer A", "Cancer A"],
            "cancer_type_detailed": ["A", "A", "A"],
            "panel_id": ["PANEL_SMALL", "PANEL_BIG", "PANEL_SMALL"],
        }
    )
    treatment = _treatment(
        [
            ("S1", False, False, False, False, False, False),
            ("S2", False, True, True, False, False, False),
            ("S3", False, False, False, False, True, False),
        ]
    )
    panel_coverage = pd.DataFrame(
        {
            "panel_id": ["PANEL_SMALL", "PANEL_BIG", "PANEL_BIG"],
            "gene": ["GENE_A", "GENE_A", "GENE_B"],
        }
    )

    out = compute_h10_treatment_freq_table(
        muts, samples, treatment, panel_coverage=panel_coverage
    )

    row = _row(out, "Cancer A", "GENE_B", "mutagenic_treatment_excluded_primary")
    assert row["num"] == 0
    assert row["n_samples"] == 0
    assert pd.isna(row["ratio"])


def test_missing_treatment_annotation_for_sample_fails_loud() -> None:
    muts = _muts([("TP53", "S1")])
    samples = _samples([("S1", "Cancer A", "A"), ("S2", "Cancer A", "A")])
    treatment = _treatment([("S1", False, False, False, False, False, False)])

    with pytest.raises(ValueError, match="missing treatment annotations"):
        compute_h10_treatment_freq_table(muts, samples, treatment)


def _row(
    df: pd.DataFrame, cancer_type: str, symbol: str, cohort_view: str
) -> pd.Series:
    match = df.loc[
        (df["cancer_type"] == cancer_type)
        & (df["symbol"] == symbol)
        & (df["cohort_view"] == cohort_view)
    ]
    assert len(match) == 1
    return match.iloc[0]
