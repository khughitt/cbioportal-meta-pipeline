"""Tests for ``combine_samples_tmb.combine_samples_tmb``.

Small glue step consumed by the GMM fit (task 5) — concatenates per-study
samples_tmb feathers and left-joins POLE/POLD1 hotspot flags.
"""

import pandas as pd

from combine_samples_tmb import combine_samples_tmb


def _tmb(study_id: str, sample_ids: list[str], tmb_values: list[float]) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "study_id": study_id,
            "sample_id": sample_ids,
            "cancer_type": ["Test Cancer"] * len(sample_ids),
            "tmb": tmb_values,
            "tmb_log10": [pd.NA] * len(sample_ids),
            "panel_callable_mb": [1.0] * len(sample_ids),
            "tmb_source": ["bed_sum"] * len(sample_ids),
            "msi_type": [pd.NA] * len(sample_ids),
            "msi_score": [pd.NA] * len(sample_ids),
        }
    )


def _hotspots(
    sample_ids: list[str], pole: list[bool], pold1: list[bool]
) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "sample_id_tumor": sample_ids,
            "pole_hotspot_detected": pole,
            "pold1_hotspot_detected": pold1,
        }
    )


def test_concat_preserves_study_id_across_studies() -> None:
    out = combine_samples_tmb(
        per_study_tmb=[
            _tmb("study_a", ["A1", "A2"], [1.0, 2.0]),
            _tmb("study_b", ["B1"], [3.0]),
        ],
        per_study_hotspots=[
            _hotspots([], [], []),
            _hotspots([], [], []),
        ],
    )
    assert set(out["study_id"]) == {"study_a", "study_b"}
    assert len(out) == 3


def test_hotspots_left_joined_onto_samples() -> None:
    out = combine_samples_tmb(
        per_study_tmb=[_tmb("s", ["A1", "A2"], [1.0, 2.0])],
        per_study_hotspots=[_hotspots(["A1"], [True], [False])],
    )
    row_a1 = out.loc[out["sample_id"] == "A1"].iloc[0]
    row_a2 = out.loc[out["sample_id"] == "A2"].iloc[0]
    assert row_a1["pole_hotspot_detected"]
    assert not row_a1["pold1_hotspot_detected"]
    # A2 had no hotspot row → flags default to False
    assert not row_a2["pole_hotspot_detected"]
    assert not row_a2["pold1_hotspot_detected"]


def test_samples_with_no_hotspot_row_get_false_not_nan() -> None:
    # Explicit contract: missing hotspot rows map to False, not NaN.
    out = combine_samples_tmb(
        per_study_tmb=[_tmb("s", ["A", "B", "C"], [1.0, 2.0, 3.0])],
        per_study_hotspots=[_hotspots([], [], [])],
    )
    assert not out["pole_hotspot_detected"].any()
    assert not out["pold1_hotspot_detected"].any()
    assert out["pole_hotspot_detected"].dtype == bool
    assert out["pold1_hotspot_detected"].dtype == bool


def test_output_contains_required_columns() -> None:
    out = combine_samples_tmb(
        per_study_tmb=[_tmb("s", ["A"], [1.0])],
        per_study_hotspots=[_hotspots(["A"], [True], [False])],
    )
    for col in (
        "study_id",
        "sample_id",
        "cancer_type",
        "tmb",
        "tmb_log10",
        "panel_callable_mb",
        "tmb_source",
        "pole_hotspot_detected",
        "pold1_hotspot_detected",
    ):
        assert col in out.columns, f"missing column {col!r}"


def test_empty_studies_list_returns_empty_dataframe_with_schema() -> None:
    out = combine_samples_tmb(per_study_tmb=[], per_study_hotspots=[])
    assert out.empty
    assert "pole_hotspot_detected" in out.columns
