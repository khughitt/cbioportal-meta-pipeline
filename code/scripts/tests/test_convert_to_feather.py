# science:code
# status: library
# science:end
"""Tests for convert_to_feather panel_id ingestion (t070)."""

from pathlib import Path

import pandas as pd

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
