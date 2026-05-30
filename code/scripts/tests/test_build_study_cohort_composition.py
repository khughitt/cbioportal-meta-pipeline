# science:code
# status: library
# science:end
"""Tests for build_study_cohort_composition."""

from __future__ import annotations

from typing import SupportsFloat, cast

import pandas as pd
import pytest

import build_study_cohort_composition as mod


def _annotated(rows: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    if len(df) > 0:
        df["is_metastatic"] = df["is_metastatic"].astype("boolean")
        df["is_pre_treated"] = df["is_pre_treated"].astype("boolean")
    else:
        df["is_metastatic"] = pd.Series([], dtype="boolean")
        df["is_pre_treated"] = pd.Series([], dtype="boolean")
    return df


def _as_float(value: object) -> float:
    return float(cast(SupportsFloat, value))


def test_percentages_sum_to_one_within_each_axis() -> None:
    samples = _annotated(
        [
            {"is_metastatic": True, "is_pre_treated": False},
            {"is_metastatic": False, "is_pre_treated": False},
            {"is_metastatic": pd.NA, "is_pre_treated": pd.NA},
            {"is_metastatic": True, "is_pre_treated": True},
        ]
    )
    row = mod.build_composition("S", samples)
    assert _as_float(row["pct_metastatic"]) + _as_float(row["pct_primary"]) + _as_float(
        row["pct_metastatic_unknown"]
    ) == pytest.approx(1.0)
    assert _as_float(row["pct_pre_treated"]) + _as_float(row["pct_naive"]) + _as_float(
        row["pct_pre_treated_unknown"]
    ) == pytest.approx(1.0)


def test_dominance_classes_cover_all_four_states() -> None:
    # 80% metastatic, 80% naive
    metastatic_dominant = _annotated(
        [{"is_metastatic": True, "is_pre_treated": False}] * 8
        + [{"is_metastatic": False, "is_pre_treated": False}] * 2
    )
    assert (
        mod.build_composition("M", metastatic_dominant)["dominant_site_class"]
        == "metastatic_dominant"
    )

    primary_dominant = _annotated(
        [{"is_metastatic": False, "is_pre_treated": False}] * 9
        + [{"is_metastatic": True, "is_pre_treated": True}] * 1
    )
    assert (
        mod.build_composition("P", primary_dominant)["dominant_site_class"]
        == "primary_dominant"
    )

    mixed = _annotated(
        [{"is_metastatic": True, "is_pre_treated": False}] * 5
        + [{"is_metastatic": False, "is_pre_treated": False}] * 5
    )
    assert mod.build_composition("X", mixed)["dominant_site_class"] == "mixed"

    unknown_dominant = _annotated(
        [{"is_metastatic": pd.NA, "is_pre_treated": pd.NA}] * 9
        + [{"is_metastatic": True, "is_pre_treated": True}] * 1
    )
    assert (
        mod.build_composition("U", unknown_dominant)["dominant_site_class"]
        == "unknown_dominant"
    )


def test_empty_study_returns_explicit_row_with_zero_percentages() -> None:
    samples = _annotated([])
    row = mod.build_composition("E", samples)
    assert row["n_samples_total"] == 0
    assert row["pct_metastatic"] == 0.0
    assert row["pct_primary"] == 0.0
    assert row["dominant_site_class"] == "unknown_dominant"
    assert row["dominant_treatment_class"] == "unknown_dominant"
