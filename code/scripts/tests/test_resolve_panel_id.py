"""Tests for resolve_panel_id (t070 spec)."""

import pandas as pd
import pytest

from resolve_panel_id import (
    infer_panel_from_sample_id,
    normalize_panel_id,
    resolve_panel_ids,
)


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


# ---------------------------------------------------------------------------
# resolve_panel_ids orchestrator
# ---------------------------------------------------------------------------


def _samples(ids: list[str]) -> pd.DataFrame:
    return pd.DataFrame({"sample_id": ids})


def _matrix(rows: list[tuple[str, str]]) -> pd.DataFrame:
    return pd.DataFrame.from_records(rows, columns=["SAMPLE_ID", "mutations"])


def test_resolve_via_matrix() -> None:
    samples = _samples(["P-0000004-T01-IM3", "P-0029974-T02-IM6"])
    matrix = _matrix(
        [("P-0000004-T01-IM3", "IMPACT341"), ("P-0029974-T02-IM6", "IMPACT468")]
    )
    result = resolve_panel_ids(
        samples,
        matrix=matrix,
        study_id="msk_impact_2017",
        study_panel_map={},
        is_panel_study=True,
    )
    assert list(result) == ["MSK-IMPACT-341", "MSK-IMPACT-468"]


def test_resolve_via_suffix_when_matrix_missing() -> None:
    samples = _samples(["P-0000012-N02-IM6", "P-0000023-N01-IM3"])
    result = resolve_panel_ids(
        samples,
        matrix=None,
        study_id="msk_ch_2023",
        study_panel_map={},
        is_panel_study=True,
    )
    assert list(result) == ["MSK-IMPACT-468", "MSK-IMPACT-341"]


def test_resolve_via_study_fallback() -> None:
    samples = _samples(["FOO-1", "FOO-2"])
    result = resolve_panel_ids(
        samples,
        matrix=None,
        study_id="custom_panel_2025",
        study_panel_map={"custom_panel_2025": "MSK-IMPACT-410"},
        is_panel_study=True,
    )
    assert list(result) == ["MSK-IMPACT-410", "MSK-IMPACT-410"]


def test_non_panel_study_returns_all_none() -> None:
    samples = _samples(["TCGA-AB-1234-01", "TCGA-CD-5678-01"])
    result = resolve_panel_ids(
        samples,
        matrix=None,
        study_id="brca_tcga",
        study_panel_map={},
        is_panel_study=False,
    )
    assert result.isna().all()


def test_panel_study_with_unresolvable_sample_raises() -> None:
    samples = _samples(["P-0000001-T01-IM3", "MYSTERY-SAMPLE"])
    matrix = _matrix([("P-0000001-T01-IM3", "IMPACT341")])
    with pytest.raises(ValueError, match="MYSTERY-SAMPLE"):
        resolve_panel_ids(
            samples,
            matrix=matrix,
            study_id="msk_impact_2017",
            study_panel_map={},
            is_panel_study=True,
        )


def test_matrix_takes_precedence_over_suffix() -> None:
    # If matrix says IMPACT468 but suffix says IMPACT341, matrix wins
    samples = _samples(["P-0000001-T01-IM3"])
    matrix = _matrix([("P-0000001-T01-IM3", "IMPACT468")])
    result = resolve_panel_ids(
        samples,
        matrix=matrix,
        study_id="msk_impact_2017",
        study_panel_map={},
        is_panel_study=True,
    )
    assert list(result) == ["MSK-IMPACT-468"]


def test_matrix_with_unrecognized_panel_raises_with_context() -> None:
    samples = _samples(["P-X-T01-IM3"])
    matrix = _matrix([("P-X-T01-IM3", "FOUNDATIONONE-CDX")])
    with pytest.raises(ValueError, match="P-X-T01-IM3.*FOUNDATIONONE-CDX"):
        resolve_panel_ids(
            samples,
            matrix=matrix,
            study_id="msk_impact_2017",
            study_panel_map={},
            is_panel_study=True,
        )


def test_matrix_missing_required_columns_raises() -> None:
    samples = _samples(["P-1-T01-IM3"])
    bad_matrix = pd.DataFrame({"WRONG_COL": ["P-1-T01-IM3"], "OTHER": ["IMPACT341"]})
    with pytest.raises(ValueError, match="must have 'SAMPLE_ID' and 'mutations'"):
        resolve_panel_ids(
            samples,
            matrix=bad_matrix,
            study_id="msk_impact_2017",
            study_panel_map={},
            is_panel_study=True,
        )
