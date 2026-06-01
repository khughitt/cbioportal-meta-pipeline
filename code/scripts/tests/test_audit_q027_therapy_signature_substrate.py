# science:code
# status: library
# science:end
"""Tests for the q027 therapy-signature feasibility audit."""

from __future__ import annotations

import pandas as pd

from audit_q027_therapy_signature_substrate import (
    CandidateStudy,
    audit_candidate_study,
    decide_feasibility,
    summarize_audit,
)


def _samples(rows: list[tuple[str, str, str]]) -> pd.DataFrame:
    return pd.DataFrame.from_records(
        rows, columns=["study_id", "sample_id", "cancer_type"]
    )


def _mutations(rows: list[tuple[str, str, str, int, str, str]]) -> pd.DataFrame:
    return pd.DataFrame.from_records(
        rows,
        columns=[
            "sample_id_tumor",
            "chromosome",
            "start",
            "reference_allele",
            "tumor_seq_allele2",
            "symbol",
        ],
    )


def _treatment(rows: list[tuple[str, str, bool, bool, bool]]) -> pd.DataFrame:
    return pd.DataFrame.from_records(
        rows,
        columns=[
            "study_id",
            "sample_id",
            "no_detected_treatment_signal",
            "positive_naive_or_pretreatment",
            "treatment_metadata_unknown",
        ],
    )


def test_audit_candidate_counts_sbs_filter_and_retained_comparator_support() -> None:
    candidate = CandidateStudy(
        study_id="glioma_test",
        target_signatures=("SBS11",),
        expected_lookup_key="cns",
        primary_patient_denominator=True,
    )
    samples = _samples(
        [
            ("glioma_test", "S1", "Diffuse Glioma"),
            ("glioma_test", "S2", "Diffuse Glioma"),
            ("glioma_test", "S3", "Diffuse Glioma"),
        ]
    )
    mutations = _mutations(
        [
            ("S1", "1", 10, "C", "T", "TP53"),
            ("S1", "chr2", 11, "A", "G", "IDH1"),
            ("S1", "MT", 12, "C", "A", "DROP_CHROM"),
            ("S1", "3", 13, "CT", "A", "DROP_INDEL"),
            ("S2", "3", 14, "G", "A", "ATRX"),
        ]
    )
    treatment = _treatment(
        [
            ("glioma_test", "S1", False, False, False),
            ("glioma_test", "S2", True, False, False),
            ("glioma_test", "S3", False, False, True),
        ]
    )

    out = audit_candidate_study(
        candidate=candidate,
        mutations=mutations,
        samples=samples,
        treatment_annotations=treatment,
        reference_columns=["SBS1", "SBS11"],
        count_floor=2,
        min_passing_samples=1,
    )

    row = out.iloc[0]
    assert row["study_id"] == "glioma_test"
    assert row["lookup_key"] == "cns"
    assert row["n_samples"] == 3
    assert row["n_sbs_filter_passing_variants"] == 3
    assert row["n_count_floor_passing_samples"] == 1
    assert row["n_count_floor_passing_retained_clinical_comparator"] == 0
    assert row["target_signatures_present"] == True  # noqa: E712
    assert row["has_retained_clinical_comparator"] == False  # noqa: E712
    assert row["passes_wp1_gate"] == False  # noqa: E712


def test_decide_feasibility_requires_primary_patient_study_with_comparator() -> None:
    audit = pd.DataFrame(
        [
            {
                "study_id": "pdx_only",
                "primary_patient_denominator": False,
                "target_signatures_present": True,
                "n_count_floor_passing_samples": 50,
                "has_retained_clinical_comparator": True,
            },
            {
                "study_id": "primary_without_comparator",
                "primary_patient_denominator": True,
                "target_signatures_present": True,
                "n_count_floor_passing_samples": 50,
                "has_retained_clinical_comparator": False,
            },
            {
                "study_id": "primary_with_comparator",
                "primary_patient_denominator": True,
                "target_signatures_present": True,
                "n_count_floor_passing_samples": 25,
                "has_retained_clinical_comparator": True,
            },
        ]
    )

    decision = decide_feasibility(audit, min_passing_samples=25)

    assert decision["continue_to_wp2"] is True
    assert decision["passing_primary_patient_studies"] == ["primary_with_comparator"]


def test_audit_candidate_records_unsupported_cancer_type_without_aborting() -> None:
    candidate = CandidateStudy(
        study_id="pdx_test",
        target_signatures=("SBS11",),
        expected_lookup_key="cns",
        primary_patient_denominator=False,
    )
    samples = _samples([("pdx_test", "P1", "Cancer of Unknown Primary")])
    treatment = _treatment([("pdx_test", "P1", True, False, False)])

    out = audit_candidate_study(
        candidate=candidate,
        mutations=_mutations([]),
        samples=samples,
        treatment_annotations=treatment,
        reference_columns=["SBS11"],
        count_floor=2,
        min_passing_samples=1,
    )

    row = out.iloc[0]
    assert row["lookup_key"] == "unsupported"
    assert row["unsupported_reason"] == "unsupported_cancer_type_for_signature_lookup"
    assert row["passes_wp1_gate"] == False  # noqa: E712


def test_summarize_audit_markdown_names_non_arbitrating_stop_reason() -> None:
    audit = pd.DataFrame(
        [
            {
                "study_id": "primary_low_count",
                "cancer_type": "Diffuse Glioma",
                "lookup_key": "cns",
                "primary_patient_denominator": True,
                "target_signatures": "SBS11",
                "target_signatures_present": True,
                "n_samples": 10,
                "n_count_floor_passing_samples": 10,
                "n_count_floor_passing_retained_clinical_comparator": 5,
                "has_retained_clinical_comparator": True,
                "passes_wp1_gate": False,
            }
        ]
    )

    note = summarize_audit(
        audit, decide_feasibility(audit, min_passing_samples=25), min_passing_samples=25
    )

    assert "non-arbitrating" in note
    assert "No primary patient candidate passed the WP1 feasibility gate" in note
    assert "| `primary_low_count` |" in note
