"""Tests for resolve_panel_id (t070 spec)."""

import pytest

from resolve_panel_id import infer_panel_from_sample_id, normalize_panel_id


@pytest.mark.parametrize(
    "raw,expected",
    [
        # IMPACT-341
        ("IMPACT341", "MSK-IMPACT-341"),
        ("MSK-IMPACT341", "MSK-IMPACT-341"),
        ("MSK-IMPACT-341", "MSK-IMPACT-341"),
        # IMPACT-410
        ("IMPACT410", "MSK-IMPACT-410"),
        ("MSK-IMPACT410", "MSK-IMPACT-410"),
        ("MSK-IMPACT-410", "MSK-IMPACT-410"),
        # IMPACT-468
        ("IMPACT468", "MSK-IMPACT-468"),
        ("MSK-IMPACT468", "MSK-IMPACT-468"),
        ("MSK-IMPACT-468", "MSK-IMPACT-468"),
        # IMPACT-505
        ("IMPACT505", "MSK-IMPACT-505"),
        ("MSK-IMPACT505", "MSK-IMPACT-505"),
        ("MSK-IMPACT-505", "MSK-IMPACT-505"),
        # IMPACT-HEME-400
        ("IMPACT-HEME-400", "MSK-IMPACT-HEME-400"),
        ("MSK-IMPACT-HEME-400", "MSK-IMPACT-HEME-400"),
        # IMPACT-HEME-468
        ("IMPACT-HEME-468", "MSK-IMPACT-HEME-468"),
        ("MSK-IMPACT-HEME-468", "MSK-IMPACT-HEME-468"),
    ],
)
def test_normalize_panel_id_known(raw: str, expected: str) -> None:
    assert normalize_panel_id(raw) == expected


def test_normalize_panel_id_strips_whitespace() -> None:
    assert normalize_panel_id("  IMPACT468  ") == "MSK-IMPACT-468"


def test_normalize_panel_id_unknown_raises() -> None:
    with pytest.raises(ValueError, match="Unrecognized panel_id"):
        normalize_panel_id("FOUNDATIONONE-CDX")


@pytest.mark.parametrize(
    "sample_id,expected",
    [
        ("P-0000004-T01-IM3", "MSK-IMPACT-341"),
        ("P-0029495-T03-IM5", "MSK-IMPACT-410"),
        ("P-0029974-T02-IM6", "MSK-IMPACT-468"),
        ("P-0050000-T01-IM7", "MSK-IMPACT-505"),
        ("P-0034805-T01-IH3", "MSK-IMPACT-HEME-400"),
    ],
)
def test_infer_panel_from_sample_id_known(sample_id: str, expected: str) -> None:
    assert infer_panel_from_sample_id(sample_id) == expected


@pytest.mark.parametrize(
    "sample_id",
    [
        "TCGA-AB-1234-01",  # TCGA — no IMPACT suffix
        "P-0000001-T01",  # truncated
        "P-0000001-T01-XYZ",  # unrecognized suffix
        "",
    ],
)
def test_infer_panel_from_sample_id_returns_none(sample_id: str) -> None:
    assert infer_panel_from_sample_id(sample_id) is None
