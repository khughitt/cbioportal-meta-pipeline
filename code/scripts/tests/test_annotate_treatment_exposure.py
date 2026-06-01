# science:code
# status: library
# science:end
"""Tests for the H10 treatment exposure annotation layer."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from annotate_treatment_exposure import (
    annotate_treatment_exposure,
    load_treatment_config,
    write_label_counts,
)


def _samples(rows: list[dict[str, object]]) -> pd.DataFrame:
    defaults = {"cancer_type": "Cancer", "is_hypermutator": False}
    return pd.DataFrame([{**defaults, **row} for row in rows])


def _base_config(**overrides: object) -> dict[str, object]:
    block: dict[str, object] = {
        "broad_treatment_exposed_studies": [],
        "mutagenic_treatment_signal_studies": [],
        "mutagenic_treatment_signal_sensitivity_only_studies": [],
        "positive_naive_or_pretreatment_studies": [],
        "unknown_treatment_metadata_studies": [],
        "sample_level_rules": {},
    }
    block.update(overrides)
    return {"h10_treatment_denominator": block}


def _write_clinical(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(path, sep="\t", index=False)


def test_load_treatment_config_accepts_empty_schema() -> None:
    cfg = load_treatment_config(_base_config())

    assert cfg.broad_treatment_exposed_studies == frozenset()
    assert cfg.sample_level_rules == {}


def test_load_treatment_config_rejects_primary_mutagenic_positive_naive_overlap() -> (
    None
):
    with pytest.raises(ValueError, match="primary mutagenic and positive-naive"):
        load_treatment_config(
            _base_config(
                mutagenic_treatment_signal_studies=["study_a"],
                positive_naive_or_pretreatment_studies=["study_a"],
            )
        )


def test_load_treatment_config_rejects_primary_mutagenic_sensitivity_overlap() -> None:
    with pytest.raises(ValueError, match="primary mutagenic and sensitivity-only"):
        load_treatment_config(
            _base_config(
                mutagenic_treatment_signal_studies=["pdx_a"],
                mutagenic_treatment_signal_sensitivity_only_studies=["pdx_a"],
            )
        )


def test_study_level_labels_and_no_detected_comparator_are_assigned() -> None:
    samples = _samples(
        [
            {"study_id": "blca_dfarber_mskcc_2014", "sample_id": "B1"},
            {"study_id": "sclc_cancercell_gardner_2017", "sample_id": "S1"},
            {"study_id": "lung_nci_2022", "sample_id": "L1"},
            {"study_id": "aml_stjude_2024", "sample_id": "A1"},
            {"study_id": "unflagged", "sample_id": "U1"},
        ]
    )
    cfg = load_treatment_config(
        _base_config(
            broad_treatment_exposed_studies=["blca_dfarber_mskcc_2014"],
            mutagenic_treatment_signal_studies=["blca_dfarber_mskcc_2014"],
            mutagenic_treatment_signal_sensitivity_only_studies=[
                "sclc_cancercell_gardner_2017"
            ],
            positive_naive_or_pretreatment_studies=["lung_nci_2022"],
            unknown_treatment_metadata_studies=["aml_stjude_2024"],
        )
    )

    out = annotate_treatment_exposure(samples, cfg, data_dir=Path("/unused"))

    by_sample = out.set_index("sample_id")
    assert by_sample.loc["B1", "treatment_exposed_broad"]
    assert by_sample.loc["B1", "mutagenic_treatment_signal"]
    assert not by_sample.loc["B1", "no_detected_treatment_signal"]
    assert by_sample.loc["S1", "mutagenic_treatment_signal_sensitivity_only"]
    assert by_sample.loc["L1", "positive_naive_or_pretreatment"]
    assert by_sample.loc["L1", "no_detected_treatment_signal"]
    assert by_sample.loc["A1", "treatment_metadata_unknown"]
    assert not by_sample.loc["A1", "no_detected_treatment_signal"]
    assert by_sample.loc["U1", "no_detected_treatment_signal"]
    assert by_sample.loc["U1", "treatment_label_source"] == "no-detected-signal"


def test_sample_level_rule_maps_raw_clinical_sample_ids_and_marks_primary_signal(
    tmp_path: Path,
) -> None:
    samples = _samples(
        [
            {"study_id": "difg_glass_2019", "sample_id": "D1"},
            {"study_id": "difg_glass_2019", "sample_id": "D2"},
            {"study_id": "difg_glass_2019", "sample_id": "D3"},
        ]
    )
    _write_clinical(
        tmp_path / "difg_glass_2019" / "data_clinical_sample.txt",
        [
            {"SAMPLE_ID": "D1", "TMZ_TREATMENT": "Yes"},
            {"SAMPLE_ID": "D2", "TMZ_TREATMENT": "No"},
            {"SAMPLE_ID": "D3", "TMZ_TREATMENT": ""},
        ],
    )
    cfg = load_treatment_config(
        _base_config(
            sample_level_rules={
                "difg_tmz": {
                    "study_id": "difg_glass_2019",
                    "target": "mutagenic_treatment_signal",
                    "clinical_sample_file": "data_clinical_sample.txt",
                    "sample_id_column": "SAMPLE_ID",
                    "positive_columns": {"TMZ_TREATMENT": ["Yes"]},
                }
            }
        )
    )

    out = annotate_treatment_exposure(samples, cfg, data_dir=tmp_path)

    by_sample = out.set_index("sample_id")
    assert by_sample.loc["D1", "mutagenic_treatment_signal"]
    assert by_sample.loc["D1", "treatment_exposed_broad"]
    assert by_sample.loc["D1", "treatment_rule_id"] == "difg_tmz"
    assert not by_sample.loc["D2", "mutagenic_treatment_signal"]
    assert by_sample.loc["D2", "no_detected_treatment_signal"]
    assert by_sample.loc["D3", "no_detected_treatment_signal"]


def test_sample_level_rule_hard_fails_on_missing_clinical_column(
    tmp_path: Path,
) -> None:
    samples = _samples([{"study_id": "difg_glass_2019", "sample_id": "D1"}])
    _write_clinical(
        tmp_path / "difg_glass_2019" / "data_clinical_sample.txt",
        [{"SAMPLE_ID": "D1", "OTHER": "Yes"}],
    )
    cfg = load_treatment_config(
        _base_config(
            sample_level_rules={
                "difg_tmz": {
                    "study_id": "difg_glass_2019",
                    "target": "mutagenic_treatment_signal",
                    "clinical_sample_file": "data_clinical_sample.txt",
                    "sample_id_column": "SAMPLE_ID",
                    "positive_columns": {"TMZ_TREATMENT": ["Yes"]},
                }
            }
        )
    )

    with pytest.raises(ValueError, match="missing required clinical columns"):
        annotate_treatment_exposure(samples, cfg, data_dir=tmp_path)


def test_sample_level_rule_hard_fails_on_unmatched_raw_sample_id(
    tmp_path: Path,
) -> None:
    samples = _samples([{"study_id": "difg_glass_2019", "sample_id": "D1"}])
    _write_clinical(
        tmp_path / "difg_glass_2019" / "data_clinical_sample.txt",
        [{"SAMPLE_ID": "D2", "TMZ_TREATMENT": "Yes"}],
    )
    cfg = load_treatment_config(
        _base_config(
            sample_level_rules={
                "difg_tmz": {
                    "study_id": "difg_glass_2019",
                    "target": "mutagenic_treatment_signal",
                    "clinical_sample_file": "data_clinical_sample.txt",
                    "sample_id_column": "SAMPLE_ID",
                    "positive_columns": {"TMZ_TREATMENT": ["Yes"]},
                }
            }
        )
    )

    with pytest.raises(ValueError, match="raw SAMPLE_ID values not present"):
        annotate_treatment_exposure(samples, cfg, data_dir=tmp_path)


def test_write_label_counts_reports_counts_by_study(tmp_path: Path) -> None:
    samples = _samples(
        [
            {"study_id": "study_a", "sample_id": "A1"},
            {"study_id": "study_a", "sample_id": "A2"},
            {"study_id": "study_b", "sample_id": "B1"},
        ]
    )
    cfg = load_treatment_config(
        _base_config(
            broad_treatment_exposed_studies=["study_a"],
            positive_naive_or_pretreatment_studies=["study_b"],
        )
    )
    annotated = annotate_treatment_exposure(samples, cfg, data_dir=Path("/unused"))
    out_path = tmp_path / "counts.tsv"

    write_label_counts(annotated, out_path)

    counts = pd.read_csv(out_path, sep="\t").set_index("study_id")
    assert counts.loc["study_a", "n_samples"] == 2
    assert counts.loc["study_a", "n_treatment_exposed_broad"] == 2
    assert counts.loc["study_b", "n_positive_naive_or_pretreatment"] == 1
