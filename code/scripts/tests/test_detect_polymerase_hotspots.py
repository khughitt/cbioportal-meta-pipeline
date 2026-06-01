# science:code
# status: library
# science:end
"""Tests for ``detect_polymerase_hotspots.detect_hotspots_per_sample``.

Specification is task 3 of the t081 hypermutator / TMB annotation plan at
``doc/plans/2026-04-13-t081-hypermutator-annotation-pipeline-plan.md``.
"""

import pandas as pd

from detect_polymerase_hotspots import (
    POLD1_HOTSPOTS,
    POLE_HOTSPOTS,
    detect_hotspots_per_sample,
)


_COLS = ["sample_id_tumor", "symbol", "hgvsp_short"]


def _muts(rows: list[tuple[str, str, str]]) -> pd.DataFrame:
    return pd.DataFrame.from_records(rows, columns=_COLS)


def test_pole_p286r_detected() -> None:
    muts = _muts([("S1", "POLE", "p.P286R")])
    out = detect_hotspots_per_sample(muts)
    row = out.loc[out["sample_id_tumor"] == "S1"].iloc[0]
    assert row["pole_hotspot_detected"]
    assert not row["pold1_hotspot_detected"]


def test_pole_p286l_not_detected_wrong_amino_acid() -> None:
    muts = _muts([("S1", "POLE", "p.P286L")])
    out = detect_hotspots_per_sample(muts)
    # S1 has a POLE mutation but not a hotspot — it should still appear in the output
    # (there was a POLE row to group on) but with both flags False.
    row = out.loc[out["sample_id_tumor"] == "S1"].iloc[0]
    assert not row["pole_hotspot_detected"]
    assert not row["pold1_hotspot_detected"]


def test_pole_non_hotspot_position_not_detected() -> None:
    muts = _muts([("S1", "POLE", "p.G100R")])
    out = detect_hotspots_per_sample(muts)
    row = out.loc[out["sample_id_tumor"] == "S1"].iloc[0]
    assert not row["pole_hotspot_detected"]


def test_hotspot_aa_in_different_gene_not_counted_as_pole_hotspot() -> None:
    # A p.P286R mutation on a gene that isn't POLE must not trigger the POLE flag —
    # the detector is gated on symbol.
    muts = _muts([("S1", "APC", "p.P286R")])
    out = detect_hotspots_per_sample(muts)
    # No POLE/POLD1 mutations at all → sample may be absent from output.
    if "S1" in set(out["sample_id_tumor"]):
        row = out.loc[out["sample_id_tumor"] == "S1"].iloc[0]
        assert not row["pole_hotspot_detected"]
        assert not row["pold1_hotspot_detected"]


def test_all_canonical_pole_hotspots_detected() -> None:
    rows = [(f"S_{aa}", "POLE", f"p.{aa}") for aa in sorted(POLE_HOTSPOTS)]
    out = detect_hotspots_per_sample(_muts(rows))
    assert len(out) == len(POLE_HOTSPOTS)
    assert out["pole_hotspot_detected"].all()


def test_all_canonical_pold1_hotspots_detected() -> None:
    rows = [(f"S_{aa}", "POLD1", f"p.{aa}") for aa in sorted(POLD1_HOTSPOTS)]
    out = detect_hotspots_per_sample(_muts(rows))
    assert len(out) == len(POLD1_HOTSPOTS)
    assert out["pold1_hotspot_detected"].all()


def test_pole_and_pold1_in_same_sample_both_flags_true() -> None:
    muts = _muts(
        [
            ("S1", "POLE", "p.P286R"),
            ("S1", "POLD1", "p.P327L"),
        ]
    )
    out = detect_hotspots_per_sample(muts)
    row = out.loc[out["sample_id_tumor"] == "S1"].iloc[0]
    assert row["pole_hotspot_detected"]
    assert row["pold1_hotspot_detected"]


def test_one_sample_one_row_in_output() -> None:
    # Sample with 3 POLE mutations (one hotspot + two not) collapses to one output row.
    muts = _muts(
        [
            ("S1", "POLE", "p.P286R"),
            ("S1", "POLE", "p.G100R"),
            ("S1", "POLE", "p.L50F"),
        ]
    )
    out = detect_hotspots_per_sample(muts)
    assert len(out[out["sample_id_tumor"] == "S1"]) == 1


def test_case_sensitive_aa_match_lowercase_not_hotspot() -> None:
    # hgvsp_short with lowercase amino-acid letters should not match the canonical
    # uppercase hotspot set — the matching is case-sensitive.
    muts = _muts([("S1", "POLE", "p.p286r")])
    out = detect_hotspots_per_sample(muts)
    if "S1" in set(out["sample_id_tumor"]):
        row = out.loc[out["sample_id_tumor"] == "S1"].iloc[0]
        assert not row["pole_hotspot_detected"]


def test_missing_hgvsp_short_handled_safely() -> None:
    muts = _muts([("S1", "POLE", "")])
    muts.loc[0, "hgvsp_short"] = pd.NA
    out = detect_hotspots_per_sample(muts)
    if "S1" in set(out["sample_id_tumor"]):
        row = out.loc[out["sample_id_tumor"] == "S1"].iloc[0]
        assert not row["pole_hotspot_detected"]
        assert not row["pold1_hotspot_detected"]


def test_absent_hgvsp_short_column_handled_like_missing_annotation() -> None:
    muts = pd.DataFrame(
        {
            "sample_id_tumor": ["S1"],
            "symbol": ["POLE"],
            "start": [133241028],
        }
    )
    out = detect_hotspots_per_sample(muts)
    row = out.loc[out["sample_id_tumor"] == "S1"].iloc[0]
    assert not row["pole_hotspot_detected"]
    assert not row["pold1_hotspot_detected"]


def test_output_has_expected_columns_and_dtypes() -> None:
    muts = _muts([("S1", "POLE", "p.P286R")])
    out = detect_hotspots_per_sample(muts)
    assert list(out.columns) == [
        "sample_id_tumor",
        "pole_hotspot_detected",
        "pold1_hotspot_detected",
    ]
    assert out["pole_hotspot_detected"].dtype == bool
    assert out["pold1_hotspot_detected"].dtype == bool


def test_empty_input_returns_empty_output_with_schema() -> None:
    muts = _muts([])
    out = detect_hotspots_per_sample(muts)
    assert out.empty
    assert list(out.columns) == [
        "sample_id_tumor",
        "pole_hotspot_detected",
        "pold1_hotspot_detected",
    ]
