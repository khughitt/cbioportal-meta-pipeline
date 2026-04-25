"""Tests for annotate_cohort_stage.

Implements the 12 tests pre-registered in
doc/plans/2026-04-24-t052-cohort-stage-descriptor-design.md (v2 §Testing).
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

import annotate_cohort_stage as mod


# ---------------------------------------------------------------------------
# Registry validation (3 tests)
# ---------------------------------------------------------------------------


def _registry_dict_to_tsv(rows: list[dict], tmp_path: Path) -> Path:
    df = pd.DataFrame(rows)
    path = tmp_path / "registry.tsv"
    df.to_csv(path, sep="\t", index=False)
    return path


def test_registry_validation_rejects_invalid_enum_value(tmp_path: Path) -> None:
    path = _registry_dict_to_tsv(
        [
            {
                "pattern": "x",
                "pattern_kind": "study_id",
                "default_is_metastatic": "yes",  # invalid
                "default_is_pre_treated": "false",
                "priority": "100",
                "source": "test",
                "notes": "",
            }
        ],
        tmp_path,
    )
    with pytest.raises(ValueError, match="default_is_metastatic"):
        mod.load_and_validate_registry(path)


def test_registry_validation_rejects_duplicate_pattern_kind_pair(
    tmp_path: Path,
) -> None:
    path = _registry_dict_to_tsv(
        [
            {
                "pattern": "x",
                "pattern_kind": "study_id",
                "default_is_metastatic": "true",
                "default_is_pre_treated": "false",
                "priority": "100",
                "source": "first",
                "notes": "",
            },
            {
                "pattern": "x",
                "pattern_kind": "study_id",
                "default_is_metastatic": "false",
                "default_is_pre_treated": "true",
                "priority": "200",
                "source": "second",
                "notes": "",
            },
        ],
        tmp_path,
    )
    with pytest.raises(ValueError, match="duplicate"):
        mod.load_and_validate_registry(path)


def test_registry_validation_rejects_empty_source(tmp_path: Path) -> None:
    path = _registry_dict_to_tsv(
        [
            {
                "pattern": "x",
                "pattern_kind": "study_id",
                "default_is_metastatic": "true",
                "default_is_pre_treated": "false",
                "priority": "100",
                "source": "  ",
                "notes": "",
            }
        ],
        tmp_path,
    )
    with pytest.raises(ValueError, match="source"):
        mod.load_and_validate_registry(path)


# ---------------------------------------------------------------------------
# Value normalization (1 test)
# ---------------------------------------------------------------------------


def test_normalize_collapses_case_punctuation_and_whitespace() -> None:
    canonical = "treatment naive"
    assert mod._normalize("Treatment-naive") == canonical
    assert mod._normalize("treatment_naive") == canonical
    assert mod._normalize("  TREATMENT  NAIVE  ") == canonical
    assert mod._normalize("Treatment Naive") == canonical


# ---------------------------------------------------------------------------
# Metastatic-axis classifier (5 tests)
# ---------------------------------------------------------------------------


def _toy_registry(tmp_path: Path) -> pd.DataFrame:
    return mod.load_and_validate_registry(
        _registry_dict_to_tsv(
            [
                {
                    "pattern": "*_tcga_pan_can_atlas_*",
                    "pattern_kind": "glob",
                    "default_is_metastatic": "false",
                    "default_is_pre_treated": "false",
                    "priority": "100",
                    "source": "tcga family fallback",
                    "notes": "",
                },
                {
                    "pattern": "tcga_mc3",
                    "pattern_kind": "study_id",
                    "default_is_metastatic": "false",
                    "default_is_pre_treated": "false",
                    "priority": "50",
                    "source": "MC3",
                    "notes": "",
                },
                {
                    "pattern": "msk_impact_*",
                    "pattern_kind": "glob",
                    "default_is_metastatic": "unknown",
                    "default_is_pre_treated": "unknown",
                    "priority": "100",
                    "source": "MSK clinical seq",
                    "notes": "",
                },
            ],
            tmp_path,
        )
    )


def test_metastatic_sample_metadata_wins_over_registry(tmp_path: Path) -> None:
    registry = _toy_registry(tmp_path)
    sample_row = {"sample_type": "Metastasis"}
    val, src = mod.classify_metastatic(sample_row, "msk_impact_2017", registry)
    assert val is True
    assert src == "sample_metadata:sample_type"


def test_metastatic_site_forces_true_when_value_is_real_site(tmp_path: Path) -> None:
    registry = _toy_registry(tmp_path)
    sample_row = {"sample_type": "", "METASTATIC_SITE": "Liver"}
    val, src = mod.classify_metastatic(sample_row, "msk_impact_2017", registry)
    assert val is True
    assert src == "sample_metadata:metastatic_site"


def test_metastatic_site_sentinel_falls_through_to_registry(tmp_path: Path) -> None:
    registry = _toy_registry(tmp_path)
    sample_row = {"sample_type": "", "METASTATIC_SITE": "Not Applicable"}
    val, src = mod.classify_metastatic(sample_row, "msk_impact_2017", registry)
    # msk_impact_* registry default is unknown -> pd.NA via registry_glob
    assert pd.isna(val)
    assert src == "registry_glob"


def test_metastatic_registry_study_id_wins_over_glob(tmp_path: Path) -> None:
    registry = _toy_registry(tmp_path)
    sample_row = {}
    val, src = mod.classify_metastatic(sample_row, "tcga_mc3", registry)
    # study_id row priority=50 wins; glob row priority=100 also matches but study_id always wins
    assert val is False
    assert src == "registry_study"


def test_metastatic_glob_pattern_with_leading_wildcard_matches(tmp_path: Path) -> None:
    registry = _toy_registry(tmp_path)
    sample_row = {}
    val, src = mod.classify_metastatic(
        sample_row, "brca_tcga_pan_can_atlas_2018", registry
    )
    assert val is False
    assert src == "registry_glob"


# ---------------------------------------------------------------------------
# Treatment-axis classifier (2 tests)
# ---------------------------------------------------------------------------


def test_pre_treated_resolves_via_sample_type_detailed(tmp_path: Path) -> None:
    registry = _toy_registry(tmp_path)
    sample_row = {"sample_type_detailed": "Post-treatment"}
    val, src = mod.classify_pre_treated(sample_row, "msk_impact_2017", registry)
    assert val is True
    assert src == "sample_metadata:sample_type_detailed"


def test_pre_treated_normalization_handles_punctuation_variants(tmp_path: Path) -> None:
    registry = _toy_registry(tmp_path)
    for raw in ("Treatment-naive", "treatment_naive", "  TREATMENT  NAIVE  "):
        sample_row = {"sample_type_detailed": raw}
        val, src = mod.classify_pre_treated(sample_row, "msk_impact_2017", registry)
        assert val is False, f"failed for {raw!r}"
        assert src == "sample_metadata:sample_type_detailed"


# ---------------------------------------------------------------------------
# Combined per-sample classifier + per-study annotator (1 test)
# ---------------------------------------------------------------------------


def test_axes_resolve_independently_one_via_metadata_other_via_registry(
    tmp_path: Path,
) -> None:
    registry = _toy_registry(tmp_path)
    samples = pd.DataFrame(
        [
            {"sample_id": "s1", "sample_type": "Metastasis"},
            {"sample_id": "s2", "sample_type": "Primary"},
            {"sample_id": "s3", "sample_type": ""},
        ]
    )
    out = mod.annotate_samples(samples, "msk_impact_2017", registry)
    # s1: metastatic=True (sample), pre_treated=NA (registry msk_impact_* default)
    # s2: metastatic=False (sample), pre_treated=NA (registry default)
    # s3: metastatic=NA (registry default), pre_treated=NA (registry default)
    assert out.loc[0, "is_metastatic"] is True
    assert pd.isna(out.loc[0, "is_pre_treated"])
    assert out.loc[0, "cohort_stage_metastatic_source"] == "sample_metadata:sample_type"
    assert out.loc[0, "cohort_stage_treatment_source"] == "registry_glob"

    assert out.loc[1, "is_metastatic"] is False
    assert pd.isna(out.loc[2, "is_metastatic"])
    assert out.loc[2, "cohort_stage_metastatic_source"] == "registry_glob"
