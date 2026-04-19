"""Tests for extract_normal_tissue_spectra.

See plan Task 3 onward for detailed test specifications.
"""
import pandas as pd
import pytest

from extract_normal_tissue_spectra import validate_input_contract


def _df(**cols: list) -> pd.DataFrame:
    return pd.DataFrame(cols)


def test_contract_rejects_multiallelic_alt() -> None:
    df = _df(
        donor_id=["D1"], tissue_label=["Liver"],
        chrom=["chr1"], pos=[1000], ref=["A"], alt=["C,T"],
    )
    with pytest.raises(ValueError, match="multi-allelic"):
        validate_input_contract(df, source="li2021", assembly="GRCh37")


def test_contract_drops_indel_rows_and_reports_count() -> None:
    df = _df(
        donor_id=["D1", "D1"], tissue_label=["Liver", "Liver"],
        chrom=["chr1", "chr1"], pos=[1000, 2000],
        ref=["A", "AG"], alt=["C", "A"],  # second row is an indel (ref length 2)
    )
    cleaned, stats = validate_input_contract(df, source="li2021", assembly="GRCh37")
    assert len(cleaned) == 1
    assert stats["n_indels_dropped"] == 1
    assert cleaned.iloc[0]["ref"] == "A"


def test_contract_rejects_non_acgt_alleles() -> None:
    df = _df(
        donor_id=["D1"], tissue_label=["Liver"],
        chrom=["chr1"], pos=[1000], ref=["A"], alt=["N"],
    )
    with pytest.raises(ValueError, match="non-ACGT"):
        validate_input_contract(df, source="li2021", assembly="GRCh37")


def test_contract_drops_mitochondrial_rows() -> None:
    df = _df(
        donor_id=["D1", "D1"], tissue_label=["Liver", "Liver"],
        chrom=["chr1", "chrM"], pos=[1000, 500],
        ref=["A", "C"], alt=["C", "T"],
    )
    cleaned, stats = validate_input_contract(df, source="li2021", assembly="GRCh37")
    assert len(cleaned) == 1
    assert stats["n_mito_dropped"] == 1
    assert cleaned.iloc[0]["chrom"] == "chr1"


def test_contract_dedups_exact_duplicates() -> None:
    df = _df(
        donor_id=["D1", "D1"], tissue_label=["Liver", "Liver"],
        chrom=["chr1", "chr1"], pos=[1000, 1000],
        ref=["A", "A"], alt=["C", "C"],
    )
    cleaned, stats = validate_input_contract(df, source="li2021", assembly="GRCh37")
    assert len(cleaned) == 1
    assert stats["n_duplicates_collapsed"] == 1


def test_contract_keeps_cross_donor_duplicates() -> None:
    df = _df(
        donor_id=["D1", "D2"], tissue_label=["Liver", "Liver"],
        chrom=["chr1", "chr1"], pos=[1000, 1000],
        ref=["A", "A"], alt=["C", "C"],
    )
    cleaned, stats = validate_input_contract(df, source="li2021", assembly="GRCh37")
    assert len(cleaned) == 2
    assert stats["n_duplicates_collapsed"] == 0


def test_contract_normalises_chrom_prefix() -> None:
    # Input without chr prefix should be normalised to chrN
    df = _df(
        donor_id=["D1"], tissue_label=["Liver"],
        chrom=["1"], pos=[1000], ref=["A"], alt=["C"],
    )
    cleaned, stats = validate_input_contract(df, source="li2021", assembly="GRCh37")
    assert cleaned.iloc[0]["chrom"] == "chr1"


def test_contract_rejects_invalid_chromosome() -> None:
    df = _df(
        donor_id=["D1"], tissue_label=["Liver"],
        chrom=["chrZ"], pos=[1000], ref=["A"], alt=["C"],
    )
    with pytest.raises(ValueError, match="unknown chromosome"):
        validate_input_contract(df, source="li2021", assembly="GRCh37")
