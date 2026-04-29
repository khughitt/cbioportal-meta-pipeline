"""Tests for t083 cancer-type label normalization."""

import pandas as pd
import pytest

from cancer_type_normalization import (
    LabelNormalizationStats,
    canonicalize_alias_map,
    extract_label_alias_maps,
    normalize_code_label,
    normalize_human_label,
    normalize_sample_labels,
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


def _sample_labels() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "sample_id": ["S1", "S2", "S3", "S4"],
            "cancer_type": pd.Series(
                ["  Breast   Cancer ", "Lung Cancer", "   ", "breast cancer"],
                dtype="category",
            ),
            "cancer_type_detailed": pd.Series(
                ["  Invasive   Breast Carcinoma ", "LUAD", None, "LUAD"],
                dtype="category",
            ),
            "primary_site": pd.Series(
                [" Breast ", " Lung ", " ", "Breast"], dtype="category"
            ),
            "sample_class": pd.Series(
                [" Tumor ", "Tumor", " ", None], dtype="category"
            ),
            "sample_type": pd.Series(
                [" Primary  Tumor ", "Metastasis", "", None], dtype="category"
            ),
            "sample_type_detailed": pd.Series(
                [" Primary ", " Distant   Metastasis ", "", None], dtype="category"
            ),
            "oncotree_code": pd.Series([" brca ", " luad ", " ", None], dtype="category"),
        }
    )


def test_normalize_sample_labels_cleans_aliases_and_rebuilds_categories() -> None:
    out, stats = normalize_sample_labels(
        _sample_labels(),
        {
            "cancer_type": {"breast cancer": "Breast Carcinoma"},
            "cancer_type_detailed": {"LUAD": "Lung Adenocarcinoma"},
            "oncotree_code": {"BRCA": "BRCA"},
        },
    )

    assert out["cancer_type"].tolist()[:2] == ["Breast Cancer", "Lung Cancer"]
    assert out.loc[3, "cancer_type"] == "Breast Carcinoma"
    assert pd.isna(out.loc[2, "cancer_type"])
    assert out["cancer_type_detailed"].tolist()[:2] == [
        "Invasive Breast Carcinoma",
        "Lung Adenocarcinoma",
    ]
    assert out["primary_site"].tolist()[:2] == ["Breast", "Lung"]
    assert out["sample_class"].tolist()[:2] == ["Tumor", "Tumor"]
    assert out["sample_type"].tolist()[:2] == ["Primary Tumor", "Metastasis"]
    assert out["sample_type_detailed"].tolist()[:2] == [
        "Primary",
        "Distant Metastasis",
    ]
    assert out["oncotree_code"].tolist()[:2] == ["BRCA", "LUAD"]

    for column in [
        "cancer_type",
        "cancer_type_detailed",
        "primary_site",
        "sample_class",
        "sample_type",
        "sample_type_detailed",
        "oncotree_code",
    ]:
        assert str(out[column].dtype) == "category"

    by_column = {item.column: item for item in stats}
    assert by_column["cancer_type"].alias_rewritten == 1
    assert by_column["cancer_type"].blanked_to_na == 1
    assert by_column["oncotree_code"].changed == 3


def test_normalize_sample_labels_is_idempotent() -> None:
    first, _ = normalize_sample_labels(
        _sample_labels(), {"cancer_type": {"breast cancer": "Breast Carcinoma"}}
    )
    second, stats = normalize_sample_labels(
        first, {"cancer_type": {"breast cancer": "Breast Carcinoma"}}
    )
    pd.testing.assert_frame_equal(first, second)
    assert all(
        item.changed == 0 and item.alias_rewritten == 0 and item.blanked_to_na == 0
        for item in stats
    )


def test_normalize_sample_labels_alias_resolution_is_single_pass() -> None:
    frame = pd.DataFrame({"sample_id": ["S1"], "cancer_type": ["A"]})
    out, _ = normalize_sample_labels(frame, {"cancer_type": {"A": "B", "B": "C"}})
    assert out.loc[0, "cancer_type"] == "B"


def test_normalize_sample_labels_ignores_missing_optional_columns() -> None:
    frame = pd.DataFrame({"sample_id": ["S1"], "cancer_type": ["  A  "]})
    out, stats = normalize_sample_labels(frame, {"primary_site": {"X": "Y"}})
    assert out["cancer_type"].tolist() == ["A"]
    assert "primary_site" not in out.columns
    assert [item.column for item in stats] == ["cancer_type"]


def test_normalize_sample_labels_returns_copy() -> None:
    frame = pd.DataFrame({"sample_id": ["S1"], "cancer_type": ["  A  "]})
    out, _ = normalize_sample_labels(frame, {})
    assert out is not frame
    assert frame.loc[0, "cancer_type"] == "  A  "
