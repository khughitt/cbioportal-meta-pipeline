# science:code
# status: library
# science:end
"""Tests for the q027 therapy-signature feasibility audit."""

from __future__ import annotations

import pandas as pd

from audit_q027_therapy_signature_substrate import (
    ANY_LOOKUP_KEY,
    CandidateStudy,
    audit_candidate_study,
    discover_candidate_studies,
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
                "has_treatment_signature_expectation": True,
            },
            {
                "study_id": "primary_without_comparator",
                "primary_patient_denominator": True,
                "target_signatures_present": True,
                "n_count_floor_passing_samples": 50,
                "has_retained_clinical_comparator": False,
                "has_treatment_signature_expectation": True,
            },
            {
                "study_id": "primary_with_comparator",
                "primary_patient_denominator": True,
                "target_signatures_present": True,
                "n_count_floor_passing_samples": 25,
                "has_retained_clinical_comparator": True,
                "has_treatment_signature_expectation": True,
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
                "has_treatment_signature_expectation": True,
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


def test_discover_candidate_studies_scans_raw_metadata_for_target_signatures(
    tmp_path,
) -> None:
    data_dir = tmp_path / "raw"
    glioma_dir = data_dir / "glioma_tmz"
    bladder_dir = data_dir / "bladder_platinum"
    generic_dir = data_dir / "generic_chemo"
    quiet_dir = data_dir / "quiet_study"
    pdx_dir = data_dir / "pdx_platinum"
    transplant_dir = data_dir / "post_transplant_entity"
    for study_dir in [
        glioma_dir,
        bladder_dir,
        generic_dir,
        quiet_dir,
        pdx_dir,
        transplant_dir,
    ]:
        study_dir.mkdir(parents=True)

    (glioma_dir / "meta_study.txt").write_text(
        "description: recurrent glioma treated with TMZ\n"
    )
    (glioma_dir / "data_clinical_sample.txt").write_text(
        "SAMPLE_ID\tTMZ_TREATMENT\nS1\tYes\n"
    )
    (bladder_dir / "meta_study.txt").write_text(
        "description: cisplatin-treated bladder cohort\n"
    )
    (bladder_dir / "data_clinical_sample.txt").write_text(
        "SAMPLE_ID\tTREATMENT\nB1\tCarboplatin\n"
    )
    (generic_dir / "meta_study.txt").write_text(
        "description: post-chemotherapy cohort\n"
    )
    (generic_dir / "data_clinical_sample.txt").write_text("SAMPLE_ID\tCHEMO\nG1\tYes\n")
    (quiet_dir / "meta_study.txt").write_text(
        "description: untreated sequencing cohort\n"
    )
    (quiet_dir / "data_clinical_sample.txt").write_text(
        "SAMPLE_ID\tNOTE\nQ1\tbaseline\n"
    )
    (pdx_dir / "meta_study.txt").write_text(
        "description: cisplatin-treated PDX models\n"
    )
    (pdx_dir / "data_clinical_sample.txt").write_text(
        "SAMPLE_ID\tTREATMENT\nP1\tcisplatin\n"
    )
    (transplant_dir / "meta_study.txt").write_text(
        "description: Post-Transplant Lymphoproliferative Disorder sequencing cohort\n"
    )
    (transplant_dir / "data_clinical_sample.txt").write_text(
        "SAMPLE_ID\tNOTE\nT1\tbaseline\n"
    )

    candidates = discover_candidate_studies(
        config={
            "studies": [
                "glioma_tmz",
                "bladder_platinum",
                "generic_chemo",
                "quiet_study",
                "pdx_platinum",
                "post_transplant_entity",
            ]
        },
        data_dir=data_dir,
    )

    by_id = {candidate.study_id: candidate for candidate in candidates}
    assert by_id["glioma_tmz"].target_signatures == ("SBS11",)
    assert by_id["glioma_tmz"].expected_lookup_key == ANY_LOOKUP_KEY
    assert by_id["glioma_tmz"].expectation_tier == "explicit"
    assert by_id["bladder_platinum"].target_signatures == ("SBS31", "SBS35")
    assert by_id["generic_chemo"].target_signatures == ("SBS11", "SBS31", "SBS35")
    assert by_id["generic_chemo"].expectation_tier == "generic"
    assert by_id["quiet_study"].target_signatures == ()
    assert by_id["quiet_study"].expectation_tier == "none"
    assert by_id["pdx_platinum"].primary_patient_denominator is False
    assert by_id["post_transplant_entity"].target_signatures == ()
    assert by_id["post_transplant_entity"].expectation_tier == "none"


def test_decide_feasibility_requires_explicit_treatment_signature_expectation() -> None:
    audit = pd.DataFrame(
        [
            {
                "study_id": "high_count_no_treatment_signal",
                "primary_patient_denominator": True,
                "target_signatures_present": True,
                "n_count_floor_passing_samples": 100,
                "has_retained_clinical_comparator": True,
                "has_treatment_signature_expectation": False,
            },
            {
                "study_id": "generic_chemo_only",
                "primary_patient_denominator": True,
                "target_signatures_present": True,
                "n_count_floor_passing_samples": 100,
                "has_retained_clinical_comparator": True,
                "has_treatment_signature_expectation": False,
            },
            {
                "study_id": "explicit_tmz",
                "primary_patient_denominator": True,
                "target_signatures_present": True,
                "n_count_floor_passing_samples": 25,
                "has_retained_clinical_comparator": True,
                "has_treatment_signature_expectation": True,
            },
        ]
    )

    decision = decide_feasibility(audit, min_passing_samples=25)

    assert decision["continue_to_wp2"] is True
    assert decision["passing_primary_patient_studies"] == ["explicit_tmz"]


def test_audit_candidate_any_lookup_key_scans_all_supported_cancer_strata() -> None:
    candidate = CandidateStudy(
        study_id="mixed_test",
        target_signatures=("SBS11",),
        expected_lookup_key=ANY_LOOKUP_KEY,
        primary_patient_denominator=True,
    )
    samples = _samples(
        [
            ("mixed_test", "G1", "Diffuse Glioma"),
            ("mixed_test", "B1", "Bladder Cancer"),
            ("mixed_test", "U1", "Cancer of Unknown Primary"),
        ]
    )
    mutations = _mutations(
        [
            ("G1", "1", 10, "C", "T", "TP53"),
            ("B1", "1", 11, "C", "T", "TP53"),
        ]
    )
    treatment = _treatment(
        [
            ("mixed_test", "G1", True, False, False),
            ("mixed_test", "B1", True, False, False),
            ("mixed_test", "U1", True, False, False),
        ]
    )

    out = audit_candidate_study(
        candidate=candidate,
        mutations=mutations,
        samples=samples,
        treatment_annotations=treatment,
        reference_columns=["SBS1", "SBS11"],
        count_floor=1,
        min_passing_samples=1,
    )

    assert set(out["lookup_key"]) == {"bladder", "cns", "unsupported"}


def test_audit_candidate_normalizes_numeric_sample_ids_before_counting_and_joining() -> (
    None
):
    candidate = CandidateStudy(
        study_id="numeric_id_test",
        target_signatures=("SBS11",),
        expected_lookup_key=ANY_LOOKUP_KEY,
        primary_patient_denominator=True,
    )
    samples = pd.DataFrame(
        {
            "study_id": ["numeric_id_test"],
            "sample_id": [1001],
            "cancer_type": ["Diffuse Glioma"],
        }
    )
    mutations = _mutations([("1001", "1", 10, "C", "T", "TP53")])
    treatment = _treatment([("numeric_id_test", "1001", True, False, False)])

    out = audit_candidate_study(
        candidate=candidate,
        mutations=mutations,
        samples=samples,
        treatment_annotations=treatment,
        reference_columns=["SBS1", "SBS11"],
        count_floor=1,
        min_passing_samples=1,
    )

    row = out.iloc[0]
    assert row["n_sbs_filter_passing_variants"] == 1
    assert row["n_count_floor_passing_samples"] == 1
    assert row["n_count_floor_passing_retained_clinical_comparator"] == 1


def test_audit_candidate_without_target_expectation_skips_expensive_variant_counting() -> (
    None
):
    candidate = CandidateStudy(
        study_id="quiet_test",
        target_signatures=(),
        expected_lookup_key=ANY_LOOKUP_KEY,
        primary_patient_denominator=True,
        expectation_tier="none",
    )
    samples = _samples([("quiet_test", "Q1", "Diffuse Glioma")])
    treatment = _treatment([("quiet_test", "Q1", True, False, False)])

    out = audit_candidate_study(
        candidate=candidate,
        mutations=pd.DataFrame(columns=["not_a_mutation_schema"]),
        samples=samples,
        treatment_annotations=treatment,
        reference_columns=["SBS1", "SBS11"],
        count_floor=1,
        min_passing_samples=1,
    )

    row = out.iloc[0]
    assert row["unsupported_reason"] == "no_treatment_signature_expectation"
    assert row["n_sbs_filter_passing_variants"] == 0
    assert row["passes_wp1_gate"] == False  # noqa: E712


def test_audit_candidate_can_report_context_count_errors_for_broad_discovery() -> None:
    candidate = CandidateStudy(
        study_id="bad_coordinate_test",
        target_signatures=("SBS11",),
        expected_lookup_key=ANY_LOOKUP_KEY,
        primary_patient_denominator=True,
    )
    samples = _samples([("bad_coordinate_test", "S1", "Diffuse Glioma")])
    mutations = _mutations([("S1", "1", "x16179154", "C", "T", "TP53")])
    treatment = _treatment([("bad_coordinate_test", "S1", True, False, False)])

    out = audit_candidate_study(
        candidate=candidate,
        mutations=mutations,
        samples=samples,
        treatment_annotations=treatment,
        reference_columns=["SBS1", "SBS11"],
        count_floor=1,
        min_passing_samples=1,
        allow_count_errors=True,
    )

    row = out.iloc[0]
    assert row["unsupported_reason"] == "mutation_context_count_error"
    assert row["n_count_floor_passing_samples"] == 0
    assert row["passes_wp1_gate"] == False  # noqa: E712
