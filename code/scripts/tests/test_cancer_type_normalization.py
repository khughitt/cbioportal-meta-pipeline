"""Tests for t083 cancer-type label normalization."""

import pandas as pd
import pytest

from cancer_type_normalization import (
    canonicalize_alias_map,
    extract_label_alias_maps,
    normalize_code_label,
    normalize_human_label,
)


def test_human_label_strips_collapses_and_preserves_case() -> None:
    assert normalize_human_label("  Breast   Cancer  ") == "Breast Cancer"
    assert normalize_human_label("breast cancer") == "breast cancer"


def test_code_label_strips_collapses_and_uppercases() -> None:
    assert normalize_code_label("  luad  ") == "LUAD"
    assert normalize_code_label(" nsclc  nos ") == "NSCLC NOS"


@pytest.mark.parametrize("value", ["", "   ", None, pd.NA, float("nan")])
def test_blank_and_missing_labels_return_none(value: object) -> None:
    assert normalize_human_label(value) is None
    assert normalize_code_label(value) is None


def test_alias_map_keys_and_values_are_normalized() -> None:
    aliases = canonicalize_alias_map(
        {"  Breast   Cancer ": "Breast carcinoma"},
        normalizer=normalize_human_label,
    )
    assert aliases == {"Breast Cancer": "Breast carcinoma"}


def test_code_alias_map_uses_code_normalization() -> None:
    aliases = canonicalize_alias_map(
        {" luad ": " lung adeno "}, normalizer=normalize_code_label
    )
    assert aliases == {"LUAD": "LUNG ADENO"}


def test_alias_map_is_single_pass_and_self_loops_are_allowed() -> None:
    aliases = canonicalize_alias_map(
        {"A": "B", "B": "C", "C": "C"},
        normalizer=normalize_human_label,
    )
    assert aliases == {"A": "B", "B": "C", "C": "C"}


def test_duplicate_normalized_alias_keys_fail() -> None:
    with pytest.raises(ValueError, match="Duplicate alias key"):
        canonicalize_alias_map(
            {"Breast Cancer": "A", "  Breast   Cancer ": "B"},
            normalizer=normalize_human_label,
        )


@pytest.mark.parametrize("bad_key", ["", "   ", None, pd.NA])
def test_empty_alias_keys_fail(bad_key: object) -> None:
    with pytest.raises(ValueError, match="empty alias key"):
        canonicalize_alias_map(
            {bad_key: "Breast Cancer"}, normalizer=normalize_human_label  # type: ignore[dict-item]
        )


@pytest.mark.parametrize("bad_value", ["", "   "])
def test_empty_alias_values_fail(bad_value: object) -> None:
    with pytest.raises(ValueError, match="empty alias value"):
        canonicalize_alias_map(
            {"Breast Cancer": bad_value}, normalizer=normalize_human_label
        )


@pytest.mark.parametrize("bad_value", [None, pd.NA, 123])
def test_non_string_alias_values_raise_typeerror(bad_value: object) -> None:
    with pytest.raises(TypeError, match="must be a string"):
        canonicalize_alias_map(
            {"Breast Cancer": bad_value}, normalizer=normalize_human_label  # type: ignore[dict-item]
        )


def test_non_mapping_alias_config_fails() -> None:
    with pytest.raises(TypeError, match="cancer_type_alias_map"):
        extract_label_alias_maps({"cancer_type_alias_map": ["not", "a", "mapping"]})


def test_none_alias_config_is_treated_as_empty() -> None:
    assert extract_label_alias_maps({"cancer_type_alias_map": None}) == {}


def test_extract_label_alias_maps_ignores_unrelated_config() -> None:
    maps = extract_label_alias_maps(
        {
            "cancer_type_alias_map": {" breast  cancer ": "Breast carcinoma"},
            "oncotree_code_alias_map": {" luad ": "LUAD"},
            "unrelated": {"A": "B"},
        }
    )
    assert maps == {
        "cancer_type": {"breast cancer": "Breast carcinoma"},
        "oncotree_code": {"LUAD": "LUAD"},
    }
