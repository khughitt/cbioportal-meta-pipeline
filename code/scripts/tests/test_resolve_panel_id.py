"""Tests for resolve_panel_id (t070 spec)."""

import pytest

from resolve_panel_id import normalize_panel_id


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("IMPACT341", "MSK-IMPACT-341"),
        ("MSK-IMPACT341", "MSK-IMPACT-341"),
        ("MSK-IMPACT-341", "MSK-IMPACT-341"),
        ("IMPACT410", "MSK-IMPACT-410"),
        ("IMPACT468", "MSK-IMPACT-468"),
        ("IMPACT505", "MSK-IMPACT-505"),
        ("IMPACT-HEME-400", "MSK-IMPACT-HEME-400"),
        ("MSK-IMPACT-HEME-400", "MSK-IMPACT-HEME-400"),
    ],
)
def test_normalize_panel_id_known(raw: str, expected: str) -> None:
    assert normalize_panel_id(raw) == expected


def test_normalize_panel_id_strips_whitespace() -> None:
    assert normalize_panel_id("  IMPACT468  ") == "MSK-IMPACT-468"


def test_normalize_panel_id_unknown_raises() -> None:
    with pytest.raises(ValueError, match="Unrecognized panel_id"):
        normalize_panel_id("FOUNDATIONONE-CDX")
