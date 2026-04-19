"""Tests for extract_normal_tissue_spectra.

See plan Task 3 onward for detailed test specifications.
"""

from pathlib import Path

import pandas as pd
import pytest

from extract_normal_tissue_spectra import (
    CONTEXT_96,
    aggregate_donor_averaged_fraction,
    aggregate_per_donor_rows,
    aggregate_pooled_counts,
    attach_assay_metadata,
    attach_uberon,
    validate_input_contract,
)


def _df(**cols: list[object]) -> pd.DataFrame:
    return pd.DataFrame(cols)


def test_contract_rejects_multiallelic_alt() -> None:
    df = _df(
        donor_id=["D1"],
        tissue_label=["Liver"],
        chrom=["chr1"],
        pos=[1000],
        ref=["A"],
        alt=["C,T"],
    )
    with pytest.raises(ValueError, match="multi-allelic"):
        validate_input_contract(df, source="li2021", assembly="GRCh37")


def test_contract_drops_indel_rows_and_reports_count() -> None:
    df = _df(
        donor_id=["D1", "D1"],
        tissue_label=["Liver", "Liver"],
        chrom=["chr1", "chr1"],
        pos=[1000, 2000],
        ref=["A", "AG"],
        alt=["C", "A"],  # second row is an indel (ref length 2)
    )
    cleaned, stats = validate_input_contract(df, source="li2021", assembly="GRCh37")
    assert len(cleaned) == 1
    assert stats["n_indels_dropped"] == 1
    assert cleaned.iloc[0]["ref"] == "A"


def test_contract_rejects_non_acgt_alleles() -> None:
    df = _df(
        donor_id=["D1"],
        tissue_label=["Liver"],
        chrom=["chr1"],
        pos=[1000],
        ref=["A"],
        alt=["N"],
    )
    with pytest.raises(ValueError, match="non-ACGT"):
        validate_input_contract(df, source="li2021", assembly="GRCh37")


def test_contract_drops_mitochondrial_rows() -> None:
    df = _df(
        donor_id=["D1", "D1"],
        tissue_label=["Liver", "Liver"],
        chrom=["chr1", "chrM"],
        pos=[1000, 500],
        ref=["A", "C"],
        alt=["C", "T"],
    )
    cleaned, stats = validate_input_contract(df, source="li2021", assembly="GRCh37")
    assert len(cleaned) == 1
    assert stats["n_mito_dropped"] == 1
    assert cleaned.iloc[0]["chrom"] == "chr1"


def test_contract_dedups_exact_duplicates() -> None:
    df = _df(
        donor_id=["D1", "D1"],
        tissue_label=["Liver", "Liver"],
        chrom=["chr1", "chr1"],
        pos=[1000, 1000],
        ref=["A", "A"],
        alt=["C", "C"],
    )
    cleaned, stats = validate_input_contract(df, source="li2021", assembly="GRCh37")
    assert len(cleaned) == 1
    assert stats["n_duplicates_collapsed"] == 1


def test_contract_keeps_cross_donor_duplicates() -> None:
    df = _df(
        donor_id=["D1", "D2"],
        tissue_label=["Liver", "Liver"],
        chrom=["chr1", "chr1"],
        pos=[1000, 1000],
        ref=["A", "A"],
        alt=["C", "C"],
    )
    cleaned, stats = validate_input_contract(df, source="li2021", assembly="GRCh37")
    assert len(cleaned) == 2
    assert stats["n_duplicates_collapsed"] == 0


def test_contract_keeps_cross_tissue_duplicates() -> None:
    df = _df(
        donor_id=["D1", "D1"],
        tissue_label=["Liver", "Esophagus"],
        chrom=["chr1", "chr1"],
        pos=[1000, 1000],
        ref=["A", "A"],
        alt=["C", "C"],
    )
    cleaned, stats = validate_input_contract(df, source="li2021", assembly="GRCh37")
    assert len(cleaned) == 2
    assert stats["n_duplicates_collapsed"] == 0


def test_contract_normalises_chrom_prefix() -> None:
    # Input without chr prefix should be normalised to chrN
    df = _df(
        donor_id=["D1"],
        tissue_label=["Liver"],
        chrom=["1"],
        pos=[1000],
        ref=["A"],
        alt=["C"],
    )
    cleaned, stats = validate_input_contract(df, source="li2021", assembly="GRCh37")
    assert cleaned.iloc[0]["chrom"] == "chr1"


def test_contract_rejects_invalid_chromosome() -> None:
    df = _df(
        donor_id=["D1"],
        tissue_label=["Liver"],
        chrom=["chrZ"],
        pos=[1000],
        ref=["A"],
        alt=["C"],
    )
    with pytest.raises(ValueError, match="unknown chromosome"):
        validate_input_contract(df, source="li2021", assembly="GRCh37")


def _mapping_tsv(tmp_path: Path) -> Path:
    p = tmp_path / "map.tsv"
    p.write_text(
        "source\ttissue_label\ttissue_uberon\tuberon_label\tnotes\n"
        "li2021\tLiver\tUBERON:0002107\tliver\t\n"
        "li2021\tEsophagus\tUBERON:0001043\tesophagus\t\n"
    )
    return p


def test_attach_uberon_joins_on_source_and_tissue_label(tmp_path: Path) -> None:
    df = _df(
        donor_id=["D1", "D1"],
        tissue_label=["Liver", "Esophagus"],
        chrom=["chr1", "chr1"],
        pos=[1, 2],
        ref=["A", "A"],
        alt=["C", "C"],
    )
    out = attach_uberon(df, _mapping_tsv(tmp_path), source="li2021")
    assert list(out["tissue_uberon"]) == ["UBERON:0002107", "UBERON:0001043"]
    assert list(out["uberon_label"]) == ["liver", "esophagus"]


def test_attach_uberon_raises_on_unmapped_tissue(tmp_path: Path) -> None:
    df = _df(
        donor_id=["D1"],
        tissue_label=["Pancreas"],
        chrom=["chr1"],
        pos=[1],
        ref=["A"],
        alt=["C"],
    )
    with pytest.raises(ValueError, match="unmapped"):
        attach_uberon(df, _mapping_tsv(tmp_path), source="li2021")


def test_attach_assay_metadata_li2021_esophagus_gets_v6() -> None:
    df = _df(
        donor_id=["D1"],
        tissue_label=["Esophagus"],
        chrom=["chr1"],
        pos=[1],
        ref=["A"],
        alt=["C"],
    )
    out = attach_assay_metadata(df, source="li2021")
    row = out.iloc[0]
    assert row["sequencing_modality"] == "WES"
    assert row["capture_kit_or_panel"] == "SureSelectXT V6"
    assert row["callable_mb"] == 60.0


def test_attach_assay_metadata_li2021_nonesophagus_gets_v7() -> None:
    df = _df(
        donor_id=["D1"],
        tissue_label=["Liver"],
        chrom=["chr1"],
        pos=[1],
        ref=["A"],
        alt=["C"],
    )
    out = attach_assay_metadata(df, source="li2021")
    row = out.iloc[0]
    assert row["capture_kit_or_panel"] == "SureSelectXT V7"
    assert row["callable_mb"] == 48.2


def test_attach_assay_metadata_missing_source_raises() -> None:
    df = _df(
        donor_id=["D1"],
        tissue_label=["Liver"],
        chrom=["chr1"],
        pos=[1],
        ref=["A"],
        alt=["C"],
    )
    with pytest.raises(KeyError, match="nonexistent"):
        attach_assay_metadata(df, source="nonexistent")


def test_attach_assay_metadata_li2021_mixed_tissues_dispatches_correctly() -> None:
    df = _df(
        donor_id=["D1", "D2"],
        tissue_label=["Esophagus", "Liver"],
        chrom=["chr1", "chr1"],
        pos=[1, 2],
        ref=["A", "A"],
        alt=["C", "C"],
    )
    out = attach_assay_metadata(df, source="li2021")
    assert out.iloc[0]["capture_kit_or_panel"] == "SureSelectXT V6"
    assert out.iloc[1]["capture_kit_or_panel"] == "SureSelectXT V7"
    assert out.iloc[0]["callable_mb"] == 60.0
    assert out.iloc[1]["callable_mb"] == 48.2


def test_context_96_ordering_is_sigprofiler_canonical() -> None:
    """CONTEXT_96 ordering is load-bearing: must match SigProfiler's SBS96
    row order so the Task 10 transpose aligns columns correctly."""
    assert CONTEXT_96[0] == "A[C>A]A"
    assert CONTEXT_96[3] == "A[C>A]T"
    assert CONTEXT_96[4] == "A[C>G]A"  # substitution changes within same 5' base
    assert CONTEXT_96[23] == "A[T>G]T"  # last A[*]* entry (24 per 5' base)
    assert CONTEXT_96[24] == "C[C>A]A"  # 5' base changes here
    assert CONTEXT_96[-1] == "T[T>G]T"
    assert len(CONTEXT_96) == 96


def _synthetic_context_df(donor_counts: dict[str, dict[str, int]]) -> pd.DataFrame:
    """Build a per-donor 96-context count DataFrame from a nested dict.

    donor_counts: {donor_id: {context: count, ...}}
    Contexts not listed default to 0.
    """
    rows: list[dict[str, object]] = []
    for donor, ctx_counts in donor_counts.items():
        row: dict[str, object] = {ctx: 0 for ctx in CONTEXT_96}
        row.update(ctx_counts)
        row["donor_id"] = donor
        rows.append(row)
    return pd.DataFrame(rows)


def test_pooled_counts_is_column_wise_sum_across_donors() -> None:
    per_donor = _synthetic_context_df(
        {
            "D1": {"A[C>A]A": 3, "T[T>G]T": 2},
            "D2": {"A[C>A]A": 1, "T[T>G]T": 7},
            "D3": {"A[C>A]A": 5},
        }
    )
    row = aggregate_pooled_counts(per_donor)
    assert row["A[C>A]A"] == 9
    assert row["T[T>G]T"] == 9
    assert row["total_snvs"] == 18
    assert row["n_donors"] == 3


def test_donor_averaged_fraction_sums_to_one() -> None:
    per_donor = _synthetic_context_df(
        {
            "D1": {"A[C>A]A": 4, "T[T>G]T": 6},  # 10 total
            "D2": {"A[C>A]A": 8, "T[T>G]T": 2},  # 10 total
        }
    )
    row, audit = aggregate_donor_averaged_fraction(per_donor, threshold=2)
    total = sum(row[ctx] for ctx in CONTEXT_96)
    assert total == pytest.approx(1.0, abs=1e-9)
    # D1 fraction: 0.4/0.6; D2: 0.8/0.2 → averaged: 0.6/0.4
    assert row["A[C>A]A"] == pytest.approx(0.6, abs=1e-9)
    assert row["T[T>G]T"] == pytest.approx(0.4, abs=1e-9)
    assert audit["n_donors_included"] == 2
    assert audit["n_donors_excluded_low_snvs"] == 0


def test_donor_averaged_fraction_excludes_low_snv_donors() -> None:
    per_donor = _synthetic_context_df(
        {
            "D1": {"A[C>A]A": 50, "T[T>G]T": 50},  # 100 total — included
            "D2": {"A[C>A]A": 49},  # 49 total — excluded at threshold=50
        }
    )
    row, audit = aggregate_donor_averaged_fraction(per_donor, threshold=50)
    assert audit["n_donors_included"] == 1
    assert audit["n_donors_excluded_low_snvs"] == 1
    assert row["A[C>A]A"] == pytest.approx(0.5, abs=1e-9)
    assert row["T[T>G]T"] == pytest.approx(0.5, abs=1e-9)


def test_donor_averaged_fraction_empty_when_all_excluded() -> None:
    per_donor = _synthetic_context_df(
        {
            "D1": {"A[C>A]A": 10},
            "D2": {"T[T>G]T": 5},
        }
    )
    row, audit = aggregate_donor_averaged_fraction(per_donor, threshold=50)
    assert audit["n_donors_included"] == 0
    assert audit["n_donors_excluded_low_snvs"] == 2
    assert sum(row[ctx] for ctx in CONTEXT_96) == 0.0


def test_per_donor_rows_one_row_per_donor_with_counts() -> None:
    per_donor = _synthetic_context_df(
        {
            "D1": {"A[C>A]A": 3},
            "D2": {"T[T>G]T": 5},
            "D3": {"A[C>A]A": 1, "T[T>G]T": 2},
        }
    )
    rows = aggregate_per_donor_rows(per_donor)
    assert len(rows) == 3
    by_donor = {r["donor_id"]: r for r in rows}
    assert by_donor["D1"]["A[C>A]A"] == 3
    assert by_donor["D1"]["total_snvs"] == 3
    assert by_donor["D2"]["T[T>G]T"] == 5
    assert by_donor["D3"]["total_snvs"] == 3
