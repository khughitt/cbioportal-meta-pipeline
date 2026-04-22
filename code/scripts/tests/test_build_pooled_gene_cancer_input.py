"""Tests for the long-format pooled-input adapter used by t077."""

import pandas as pd
import pytest

from build_pooled_gene_cancer_input import build_pooled_input


def _per_study_frame(
    rows: list[tuple[str, str, int, int, float, float, int, int]],
) -> pd.DataFrame:
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


def test_build_pooled_input_emits_long_rows_and_covariates() -> None:
    study_wes = _per_study_frame([("A", "TP53", 10, 8, 0.10, 0.08, 100, 80)])
    study_panel = _per_study_frame([("A", "TP53", 5, 4, 0.10, 0.08, 50, 50)])

    pooled = build_pooled_input(
        per_study_frames=[("study_wes", study_wes), ("study_panel", study_panel)],
        cancer_presence_by_study={
            "study_wes": {"A": (100, 80)},
            "study_panel": {"A": (50, 50)},
        },
        matched_normal_studies={"study_wes"},
        study_panel_map={"study_panel": "MSK-IMPACT-410"},
        sample_panel_ids_by_study={"study_panel": {"MSK-IMPACT-410"}},
    )

    assert list(pooled.columns) == [
        "study_id",
        "cancer_type",
        "symbol",
        "y_inclusive",
        "y_exclusive",
        "n_inclusive",
        "n_exclusive",
        "panel_class",
        "matched_normal",
    ]

    wes_row = pooled.loc[
        (pooled["study_id"] == "study_wes")
        & (pooled["cancer_type"] == "A")
        & (pooled["symbol"] == "TP53")
    ].iloc[0]
    panel_row = pooled.loc[
        (pooled["study_id"] == "study_panel")
        & (pooled["cancer_type"] == "A")
        & (pooled["symbol"] == "TP53")
    ].iloc[0]

    assert wes_row["y_inclusive"] == 10
    assert wes_row["y_exclusive"] == 8
    assert wes_row["n_inclusive"] == 100
    assert wes_row["n_exclusive"] == 80
    assert wes_row["panel_class"] == "WES"
    assert bool(wes_row["matched_normal"]) is True

    assert panel_row["y_inclusive"] == 5
    assert panel_row["y_exclusive"] == 4
    assert panel_row["n_inclusive"] == 50
    assert panel_row["n_exclusive"] == 50
    assert panel_row["panel_class"] == "large_hybrid_capture"
    assert bool(panel_row["matched_normal"]) is False


def test_build_pooled_input_zero_fills_missing_wes_cell_when_cancer_present() -> None:
    study_a = _per_study_frame([("A", "TP53", 10, 8, 0.10, 0.08, 100, 80)])
    study_b = _per_study_frame([("A", "KRAS", 3, 2, 0.06, 0.05, 50, 40)])

    pooled = build_pooled_input(
        per_study_frames=[("study_a", study_a), ("study_b", study_b)],
        cancer_presence_by_study={
            "study_a": {"A": (100, 80)},
            "study_b": {"A": (50, 40)},
        },
        matched_normal_studies=set(),
        study_panel_map={},
        sample_panel_ids_by_study={},
    )

    row = pooled.loc[
        (pooled["study_id"] == "study_b")
        & (pooled["cancer_type"] == "A")
        & (pooled["symbol"] == "TP53")
    ].iloc[0]

    assert row["y_inclusive"] == 0
    assert row["y_exclusive"] == 0
    assert row["n_inclusive"] == 50
    assert row["n_exclusive"] == 40
    assert row["panel_class"] == "WES"


def test_build_pooled_input_skips_missing_panel_bearing_cells() -> None:
    study_a = _per_study_frame([("A", "TP53", 10, 8, 0.10, 0.08, 100, 80)])
    study_panel = _per_study_frame([("A", "KRAS", 3, 2, 0.06, 0.05, 50, 40)])

    pooled = build_pooled_input(
        per_study_frames=[("study_a", study_a), ("study_panel", study_panel)],
        cancer_presence_by_study={
            "study_a": {"A": (100, 80)},
            "study_panel": {"A": (50, 40)},
        },
        matched_normal_studies=set(),
        study_panel_map={},
        panel_bearing_studies={"study_panel"},
        sample_panel_ids_by_study={"study_panel": {"MSK-IMPACT-410"}},
    )

    assert pooled.loc[
        (pooled["study_id"] == "study_panel")
        & (pooled["cancer_type"] == "A")
        & (pooled["symbol"] == "TP53")
    ].empty


def test_build_pooled_input_marks_mc3_studies_explicitly() -> None:
    mc3 = _per_study_frame([("BRCA", "TP53", 20, 20, 0.20, 0.20, 100, 100)])

    pooled = build_pooled_input(
        per_study_frames=[("tcga_mc3", mc3)],
        cancer_presence_by_study={"tcga_mc3": {"BRCA": (100, 100)}},
        matched_normal_studies={"tcga_mc3"},
        study_panel_map={},
        sample_panel_ids_by_study={},
    )

    row = pooled.iloc[0]
    assert row["panel_class"] == "MC3"
    assert bool(row["matched_normal"]) is True


def test_unknown_panel_class_requires_explicit_override() -> None:
    study_panel = _per_study_frame([("A", "TP53", 5, 5, 0.10, 0.10, 50, 50)])

    with pytest.raises(ValueError, match="Could not infer panel_class"):
        build_pooled_input(
            per_study_frames=[("study_panel", study_panel)],
            cancer_presence_by_study={"study_panel": {"A": (50, 50)}},
            matched_normal_studies=set(),
            study_panel_map={},
            panel_bearing_studies={"study_panel"},
            sample_panel_ids_by_study={"study_panel": {"mystery_panel_v1"}},
        )
