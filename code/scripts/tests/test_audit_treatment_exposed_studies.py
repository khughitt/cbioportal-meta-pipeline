# science:code
# status: library
# science:end

from pathlib import Path

from audit_treatment_exposed_studies import (
    audit_study,
    classify_study_text,
    parse_meta_study,
)


def test_parse_meta_study_handles_carriage_return_separated_fields(
    tmp_path: Path,
) -> None:
    meta = tmp_path / "meta_study.txt"
    meta.write_text(
        "type_of_cancer: brca\rcancer_study_identifier: brca_dfci_2020\r"
        "name: Metastatic Breast Cancer (DFCI, Cancer Discov 2020)\r"
        "description: Whole-exome sequencing of metastatic breast cancer biopsies.\r",
        encoding="utf-8",
    )

    parsed = parse_meta_study(meta)

    assert parsed["cancer_study_identifier"] == "brca_dfci_2020"
    assert parsed["name"] == "Metastatic Breast Cancer (DFCI, Cancer Discov 2020)"
    assert parsed["description"].startswith("Whole-exome sequencing")


def test_classify_study_text_separates_prior_treatment_from_pretreatment_samples() -> (
    None
):
    explicit = classify_study_text(
        "Whole exome sequencing of pretreated melanoma tumor-normal pairs after ipilimumab."
    )
    pretreatment = classify_study_text(
        "Whole-exome sequencing of pre-treatment samples from metastatic melanoma treated with anti-PD1."
    )

    assert explicit.tier == "explicit_treatment_exposed"
    assert explicit.recommendation == "flag_exposed"
    assert "pretreated" in explicit.signals
    assert pretreatment.tier == "advanced_metastatic_enriched"
    assert pretreatment.recommendation == "review_for_fraction"
    assert "pre-treatment" in pretreatment.negative_signals


def test_classify_study_text_marks_treatment_naive_as_do_not_flag() -> None:
    classification = classify_study_text(
        "Whole-genome sequencing of treatment-naive never smoker patients with lung cancer."
    )

    assert classification.tier == "treatment_naive_or_pretreatment"
    assert classification.recommendation == "do_not_flag"
    assert "treatment-naive" in classification.negative_signals


def test_classify_study_text_flags_drug_exposed_cohorts_without_flagging_pretreatment_samples() -> (
    None
):
    drug_exposed = classify_study_text(
        "Whole-exome sequencing of CDK4/6i exposed metastatic breast cancer tumors."
    )
    drug_treated = classify_study_text(
        "Targeted sequencing of buparlisib + letrozole-treated metastatic ER+ breast tumors."
    )

    assert drug_exposed.tier == "explicit_treatment_exposed"
    assert drug_exposed.recommendation == "flag_exposed"
    assert "exposed" in drug_exposed.signals
    assert drug_treated.tier == "explicit_treatment_exposed"
    assert "treated" in drug_treated.signals


def test_audit_study_skips_tcga_and_preserves_candidate_reason(tmp_path: Path) -> None:
    tcga_dir = tmp_path / "brca_tcga_pan_can_atlas_2018"
    tcga_dir.mkdir()
    (tcga_dir / "meta_study.txt").write_text(
        "cancer_study_identifier: brca_tcga_pan_can_atlas_2018\n"
        "name: Breast TCGA\n"
        "description: TCGA PanCanAtlas cohort.\n",
        encoding="utf-8",
    )

    candidate_dir = tmp_path / "mel_ucla_2016"
    candidate_dir.mkdir()
    (candidate_dir / "meta_study.txt").write_text(
        "cancer_study_identifier: mel_ucla_2016\n"
        "name: Metastatic Melanoma (UCLA, Cell 2016)\n"
        "description: Whole-exome sequencing of 38 pretreated melanoma tumor-normal pairs.\n",
        encoding="utf-8",
    )

    assert audit_study("brca_tcga_pan_can_atlas_2018", tmp_path) is None
    row = audit_study("mel_ucla_2016", tmp_path)

    assert row is not None
    assert row["study_id"] == "mel_ucla_2016"
    assert row["candidate_tier"] == "explicit_treatment_exposed"
    assert row["recommendation"] == "flag_exposed"
    assert row["signals"] == "metastatic;pretreated"


def test_audit_study_promotes_neutral_metadata_with_treatment_clinical_columns(
    tmp_path: Path,
) -> None:
    study_dir = tmp_path / "neutral_study"
    study_dir.mkdir()
    (study_dir / "meta_study.txt").write_text(
        "cancer_study_identifier: neutral_study\n"
        "name: Neutral Cancer Study\n"
        "description: Sequencing of cancer samples.\n",
        encoding="utf-8",
    )
    (study_dir / "data_clinical_sample.txt").write_text(
        "#Patient Identifier\tSample Identifier\tTumor Treated\n"
        "#Patient identifier\tSample identifier\tWhether tumor was treated\n"
        "#STRING\tSTRING\tSTRING\n"
        "#1\t1\t1\n"
        "PATIENT_ID\tSAMPLE_ID\tTUMOR_TREATED\n"
        "P1\tS1\tYes\n",
        encoding="utf-8",
    )

    row = audit_study("neutral_study", tmp_path)

    assert row is not None
    assert row["candidate_tier"] == "clinical_signal_present"
    assert row["recommendation"] == "review_for_fraction"
    assert row["clinical_signal_columns"] == "TUMOR_TREATED"
