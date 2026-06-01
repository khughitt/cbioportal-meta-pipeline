# science:code
# status: library
# science:end
"""Tests for q027 signature-high frequency views."""

from __future__ import annotations

import pandas as pd

from create_q027_signature_high_freq_tables import (
    COHORT_VIEWS,
    compute_q027_signature_high_freq_table,
)


def _muts(rows: list[tuple[str, str]]) -> pd.DataFrame:
    return pd.DataFrame.from_records(rows, columns=["symbol", "sample_id_tumor"])


def _samples(rows: list[tuple[str, str, str]]) -> pd.DataFrame:
    return pd.DataFrame.from_records(
        rows, columns=["sample_id", "cancer_type", "cancer_type_detailed"]
    )


def _labels(rows: list[tuple[str, bool, bool, bool, bool]]) -> pd.DataFrame:
    return pd.DataFrame.from_records(
        rows,
        columns=[
            "sample_id",
            "passes_count_floor",
            "therapy_signature_high",
            "therapy_signature_high_sensitivity_20",
            "therapy_signature_high_sensitivity_fraction_10",
        ],
    )


def _hyper(rows: list[tuple[str, bool]]) -> pd.DataFrame:
    return pd.DataFrame.from_records(rows, columns=["sample_id", "is_hypermutator"])


def test_q027_frequency_views_remove_primary_high_samples() -> None:
    muts = _muts([("TP53", "S1"), ("TP53", "S2"), ("BRAF", "S3")])
    samples = _samples(
        [
            ("S1", "Glioma", "Glioma"),
            ("S2", "Glioma", "Glioma"),
            ("S3", "Glioma", "Glioma"),
            ("S4", "Glioma", "Glioma"),
        ]
    )
    labels = _labels(
        [
            ("S1", True, True, True, True),
            ("S2", True, False, True, False),
            ("S3", False, False, False, False),
            ("S4", True, False, False, False),
        ]
    )
    hyper = _hyper([("S1", False), ("S2", False), ("S3", False), ("S4", False)])

    out = compute_q027_signature_high_freq_table(muts, samples, labels, hyper)
    tp53 = out.loc[out["symbol"] == "TP53"].set_index("cohort_view")

    assert set(COHORT_VIEWS) <= set(tp53.index)
    assert tp53.loc["all_samples", "n_samples"] == 4
    assert tp53.loc["all_samples", "num"] == 2
    assert tp53.loc["therapy_signature_high", "n_samples"] == 1
    assert tp53.loc["therapy_signature_high", "num"] == 1
    assert tp53.loc["therapy_signature_high_excluded_primary", "n_samples"] == 3
    assert tp53.loc["therapy_signature_high_excluded_primary", "num"] == 1
    assert tp53.loc["signature_evaluable", "n_samples"] == 3


def test_q027_frequency_views_require_labels_for_every_sample() -> None:
    muts = _muts([])
    samples = _samples([("S1", "Glioma", "Glioma")])
    labels = _labels([])
    hyper = _hyper([("S1", False)])

    try:
        compute_q027_signature_high_freq_table(muts, samples, labels, hyper)
    except ValueError as exc:
        assert "missing q027 signature labels" in str(exc)
    else:
        raise AssertionError("Expected missing-label failure")
