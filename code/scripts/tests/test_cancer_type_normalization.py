"""Tests for t083 cancer-type label normalization."""

import pandas as pd
import pytest

from cancer_type_normalization import normalize_code_label, normalize_human_label


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
