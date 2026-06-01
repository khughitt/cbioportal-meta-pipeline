# science:code
# status: library
# science:end
"""Tests for convert_to_feather panel_id ingestion (t070)."""

from pathlib import Path

import pandas as pd
import pyarrow as pa
import pytest

from feather_compat import coerce_mixed_object_columns_to_string
from resolve_panel_id import resolve_panel_ids


def _write_clinical_sample(p: Path, ids: list[str]) -> None:
    header = "PATIENT_ID\tSAMPLE_ID\tCANCER_TYPE\tCANCER_TYPE_DETAILED\tONCOTREE_CODE\n"
    body = "".join(f"{i.split('-T')[0]}\t{i}\tLung Cancer\tLUAD\tLUAD\n" for i in ids)
    p.write_text("#" + header + "#" + header + "#STRING\n#1\n" + header + body)


def _write_matrix(p: Path, rows: list[tuple[str, str]]) -> None:
    p.write_text(
        "SAMPLE_ID\tmutations\tcna\tstructural_variants\n"
        + "".join(f"{sid}\t{panel}\t{panel}\t{panel}\n" for sid, panel in rows)
    )


def test_resolve_panel_ids_via_matrix(tmp_path: Path) -> None:
    """Smoke test: matrix-based resolution end-to-end through resolve_panel_ids."""
    sample_p = tmp_path / "data_clinical_sample.txt"
    matrix_p = tmp_path / "data_gene_panel_matrix.txt"
    _write_clinical_sample(sample_p, ["P-1-T01-IM3", "P-2-T01-IM6"])
    _write_matrix(
        matrix_p, [("P-1-T01-IM3", "IMPACT341"), ("P-2-T01-IM6", "IMPACT468")]
    )

    samples = pd.read_csv(sample_p, sep="\t", comment="#")
    samples = samples.rename(columns={"SAMPLE_ID": "sample_id"})
    matrix = pd.read_csv(matrix_p, sep="\t")

    panel_ids = resolve_panel_ids(
        samples,
        matrix=matrix,
        study_id="msk_impact_2017",
        study_panel_map={},
        is_panel_study=True,
    )
    assert list(panel_ids) == ["MSK-IMPACT-341", "MSK-IMPACT-468"]


def test_coerce_mixed_object_columns_to_string_makes_clinical_metadata_feather_safe(
    tmp_path: Path,
) -> None:
    """Mixed numeric/string clinical fields should not crash Feather serialization."""
    raw = pd.DataFrame(
        {
            "sample_id": ["S1", "S2", "S3"],
            "TUMOR_PURITY": pd.Series([70.0, "80", None], dtype=object),
            "FACETS_WGD": pd.Series([True, "False", None], dtype=object),
            "canonical_numeric": [1.0, 2.0, 3.0],
        }
    )

    with pytest.raises((TypeError, ValueError, pa.lib.ArrowInvalid)):
        raw.to_feather(tmp_path / "raw.feather")

    out = coerce_mixed_object_columns_to_string(raw)
    out.to_feather(tmp_path / "coerced.feather")

    assert str(out["TUMOR_PURITY"].dtype) == "string"
    assert str(out["FACETS_WGD"].dtype) == "string"
    assert str(out["canonical_numeric"].dtype) == "float64"
