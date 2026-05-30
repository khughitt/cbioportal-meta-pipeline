# science:code
# status: library
# science:end
"""Tests for ``prepare_dndscv_input.prepare_dndscv_input``.

t131 dndscv chain entry point: per-study mut.feather + samples.feather -> the
schema-validated input feather consumed by combine_mut_per_cancer_type.

Covers:
  - basic happy path: SNV filter, sample-join, schema contract
  - mixed sample_id dtypes (regression for the pog570_bcgsc_2020 int64
    sample_id failure surfaced in the t131 full pan-cancer-dndscv run
    2026-04-25 — the merge `out.merge(samples_join)` raised
    `ValueError: You are trying to merge on str and int64 columns`)
  - sentinel ref/alt rows dropped (empty, "-", "nan")
  - non-SNV variants dropped
  - build validation
  - rows with no samples-table entry dropped (inner join contract)
"""

import pandas as pd
import pytest

from prepare_dndscv_input import prepare_dndscv_input


def _mut(rows: list[dict]) -> pd.DataFrame:
    """Build a mut.feather-shaped frame.

    Required columns: sample_id_tumor, chromosome, start, reference_allele,
    tumor_seq_allele2, variant_type, symbol.
    """
    defaults = {
        "chromosome": "1",
        "start": 100,
        "reference_allele": "A",
        "tumor_seq_allele2": "T",
        "variant_type": "SNP",
        "symbol": "GENE1",
    }
    return pd.DataFrame([{**defaults, **r} for r in rows])


def _samples(rows: list[dict]) -> pd.DataFrame:
    """Build a samples.feather-shaped frame.

    Required columns: sample_id, cancer_type.
    """
    defaults = {"cancer_type": "Test Cancer"}
    return pd.DataFrame([{**defaults, **r} for r in rows])


def test_happy_path_str_sample_ids() -> None:
    mut = _mut(
        [
            {"sample_id_tumor": "S1"},
            {"sample_id_tumor": "S2"},
            {"sample_id_tumor": "S3"},
        ]
    )
    samples = _samples(
        [
            {"sample_id": "S1"},
            {"sample_id": "S2"},
            {"sample_id": "S3"},
        ]
    )
    out = prepare_dndscv_input(mut, samples, build="hg19")
    assert len(out) == 3
    assert list(out.columns) == [
        "sample_id",
        "cancer_type",
        "chr",
        "pos",
        "ref",
        "alt",
        "build",
        "modality",
    ]
    assert (out["build"] == "hg19").all()
    assert (out["modality"] == "wes").all()  # no panel_id column → wes


def test_int_sample_ids_join_correctly() -> None:
    """Reproduces the pog570_bcgsc_2020 int64 sample_id failure."""
    mut = _mut(
        [
            {"sample_id_tumor": 100},
            {"sample_id_tumor": 200},
            {"sample_id_tumor": 300},
        ]
    )
    samples = _samples(
        [
            {"sample_id": 100},
            {"sample_id": 200},
            {"sample_id": 300},
        ]
    )
    out = prepare_dndscv_input(mut, samples, build="hg19")
    assert len(out) == 3
    # Output sample_id must be str regardless of input dtype.
    assert all(isinstance(v, str) for v in out["sample_id"])
    assert set(out["sample_id"]) == {"100", "200", "300"}


def test_non_snv_rows_dropped() -> None:
    mut = _mut(
        [
            {"sample_id_tumor": "S1", "variant_type": "SNP"},
            {"sample_id_tumor": "S2", "variant_type": "INS"},  # dropped
            {"sample_id_tumor": "S3", "variant_type": "DEL"},  # dropped
            {"sample_id_tumor": "S4", "variant_type": "SNP"},
        ]
    )
    samples = _samples(
        [{"sample_id": s} for s in ("S1", "S2", "S3", "S4")]
    )
    out = prepare_dndscv_input(mut, samples, build="hg19")
    assert set(out["sample_id"]) == {"S1", "S4"}


def test_sentinel_alleles_dropped() -> None:
    mut = _mut(
        [
            {"sample_id_tumor": "S1", "reference_allele": "A", "tumor_seq_allele2": "T"},
            {"sample_id_tumor": "S2", "reference_allele": "-", "tumor_seq_allele2": "T"},
            {"sample_id_tumor": "S3", "reference_allele": "", "tumor_seq_allele2": "T"},
            {"sample_id_tumor": "S4", "reference_allele": "A", "tumor_seq_allele2": "-"},
            {"sample_id_tumor": "S5", "reference_allele": "A", "tumor_seq_allele2": "nan"},
        ]
    )
    samples = _samples([{"sample_id": s} for s in ("S1", "S2", "S3", "S4", "S5")])
    out = prepare_dndscv_input(mut, samples, build="hg19")
    assert set(out["sample_id"]) == {"S1"}


def test_mut_sample_with_no_samples_row_dropped() -> None:
    """Inner-join contract: a mutation row whose sample isn't in samples.feather
    cannot be assigned a cancer_type, so it must be dropped."""
    mut = _mut(
        [
            {"sample_id_tumor": "S1"},
            {"sample_id_tumor": "GHOST"},  # not in samples
        ]
    )
    samples = _samples([{"sample_id": "S1"}])
    out = prepare_dndscv_input(mut, samples, build="hg19")
    assert set(out["sample_id"]) == {"S1"}


def test_invalid_build_raises() -> None:
    mut = _mut([{"sample_id_tumor": "S1"}])
    samples = _samples([{"sample_id": "S1"}])
    with pytest.raises(ValueError, match="hg19, hg38"):
        prepare_dndscv_input(mut, samples, build="grch37")


def test_missing_mut_column_raises() -> None:
    mut = _mut([{"sample_id_tumor": "S1"}]).drop(columns=["chromosome"])
    samples = _samples([{"sample_id": "S1"}])
    with pytest.raises(ValueError, match="mut missing columns"):
        prepare_dndscv_input(mut, samples, build="hg19")


def test_chr_prefix_stripped() -> None:
    """dndscv expects no `chr` prefix; some studies store it that way."""
    mut = _mut(
        [
            {"sample_id_tumor": "S1", "chromosome": "chr1"},
            {"sample_id_tumor": "S2", "chromosome": "chrX"},
        ]
    )
    samples = _samples([{"sample_id": "S1"}, {"sample_id": "S2"}])
    out = prepare_dndscv_input(mut, samples, build="hg19")
    assert set(out["chr"]) == {"1", "X"}


def test_panel_modality_inferred_from_panel_id() -> None:
    """Samples with non-null panel_id are tagged modality=panel; null → wes."""
    mut = _mut([{"sample_id_tumor": s} for s in ("S1", "S2", "S3")])
    samples = pd.DataFrame(
        [
            {"sample_id": "S1", "cancer_type": "C", "panel_id": "PANEL_X"},
            {"sample_id": "S2", "cancer_type": "C", "panel_id": None},
            {"sample_id": "S3", "cancer_type": "C", "panel_id": "PANEL_Y"},
        ]
    )
    out = prepare_dndscv_input(mut, samples, build="hg38")
    out_by_sample = out.set_index("sample_id")
    assert out_by_sample.loc["S1", "modality"] == "panel"
    assert out_by_sample.loc["S2", "modality"] == "wes"
    assert out_by_sample.loc["S3", "modality"] == "panel"
