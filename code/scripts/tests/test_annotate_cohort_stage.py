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
