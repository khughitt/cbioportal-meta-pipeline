"""Tests for ``msi_normalization``.

Specification is task 4 of the t081 hypermutator / TMB annotation plan at
``doc/plans/2026-04-13-t081-hypermutator-annotation-pipeline-plan.md``.
"""

import pandas as pd

from msi_normalization import (
    MSI_TYPE_NORMALIZATION,
    normalize_msi_columns,
)


def _df(columns: dict[str, list]) -> pd.DataFrame:
    return pd.DataFrame(columns)


def test_msi_type_column_parsed_and_normalized() -> None:
    out = normalize_msi_columns(
        _df(
            {
                "sample_id": ["A", "B", "C"],
                "MSI_TYPE": ["MSI-H", "MSS", "Indeterminate"],
            }
        )
    )
    assert list(out["msi_type"]) == ["MSI-H", "MSS", "Indeterminate"]


def test_msi_status_used_when_msi_type_absent() -> None:
    out = normalize_msi_columns(
        _df({"sample_id": ["A", "B"], "MSI_STATUS": ["MSI-H", "MSS"]})
    )
    assert list(out["msi_type"]) == ["MSI-H", "MSS"]


def test_msi_type_preferred_over_msi_status_when_both_present() -> None:
    out = normalize_msi_columns(
        _df(
            {
                "sample_id": ["A"],
                "MSI_TYPE": ["MSI-H"],
                "MSI_STATUS": ["MSS"],
            }
        )
    )
    # MSI_TYPE wins.
    assert out.loc[0, "msi_type"] == "MSI-H"


def test_msi_score_numeric_preserved_as_float() -> None:
    out = normalize_msi_columns(
        _df({"sample_id": ["A", "B"], "MSI_SCORE": [23.5, 0.1]})
    )
    assert out["msi_score"].dtype == float
    assert list(out["msi_score"]) == [23.5, 0.1]


def test_msi_sensor_score_used_when_msi_score_absent() -> None:
    out = normalize_msi_columns(
        _df({"sample_id": ["A", "B"], "MSI_SENSOR_SCORE": [15.0, 2.0]})
    )
    assert list(out["msi_score"]) == [15.0, 2.0]


def test_both_msi_type_and_msi_score_when_both_columns_present() -> None:
    out = normalize_msi_columns(
        _df(
            {
                "sample_id": ["A"],
                "MSI_TYPE": ["MSI-H"],
                "MSI_SCORE": [27.0],
            }
        )
    )
    assert out.loc[0, "msi_type"] == "MSI-H"
    assert out.loc[0, "msi_score"] == 27.0


def test_missing_msi_columns_emits_nan_columns_with_correct_names() -> None:
    out = normalize_msi_columns(_df({"sample_id": ["A", "B"]}))
    assert "msi_type" in out.columns
    assert "msi_score" in out.columns
    assert out["msi_type"].isna().all()
    assert out["msi_score"].isna().all()


def test_normalization_maps_instable_and_high_to_msi_h() -> None:
    out = normalize_msi_columns(
        _df(
            {
                "sample_id": ["A", "B", "C", "D"],
                "MSI_TYPE": ["Instable", "High", "MSI", "Unstable"],
            }
        )
    )
    assert list(out["msi_type"]) == ["MSI-H", "MSI-H", "MSI-H", "MSI-H"]


def test_normalization_maps_stable_to_mss() -> None:
    out = normalize_msi_columns(
        _df(
            {
                "sample_id": ["A", "B"],
                "MSI_TYPE": ["Stable", "Microsatellite stable"],
            }
        )
    )
    assert list(out["msi_type"]) == ["MSS", "MSS"]


def test_normalization_is_case_insensitive() -> None:
    out = normalize_msi_columns(
        _df(
            {
                "sample_id": ["A", "B", "C", "D"],
                "MSI_TYPE": ["msi-h", "MSS", "  MSI-H  ", "INSTABLE"],
            }
        )
    )
    assert list(out["msi_type"]) == ["MSI-H", "MSS", "MSI-H", "MSI-H"]


def test_unrecognized_msi_value_becomes_na() -> None:
    out = normalize_msi_columns(
        _df({"sample_id": ["A", "B"], "MSI_TYPE": ["something else", "MSI-H"]})
    )
    assert pd.isna(out.loc[0, "msi_type"])
    assert out.loc[1, "msi_type"] == "MSI-H"


def test_empty_string_and_nan_inputs_become_na() -> None:
    out = normalize_msi_columns(
        _df({"sample_id": ["A", "B", "C"], "MSI_TYPE": ["", None, "MSS"]})
    )
    assert pd.isna(out.loc[0, "msi_type"])
    assert pd.isna(out.loc[1, "msi_type"])
    assert out.loc[2, "msi_type"] == "MSS"


def test_original_input_not_mutated() -> None:
    df = _df({"sample_id": ["A"], "MSI_TYPE": ["MSI-H"]})
    normalize_msi_columns(df)
    assert list(df.columns) == ["sample_id", "MSI_TYPE"]


def test_normalization_table_exports_canonical_targets() -> None:
    # Defensive: the normalization table must only map to the canonical target set.
    canonical_targets = {"MSI-H", "MSI-L", "MSS", "Indeterminate"}
    assert set(MSI_TYPE_NORMALIZATION.values()) <= canonical_targets
