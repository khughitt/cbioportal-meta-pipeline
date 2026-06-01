# science:code
# status: library
# science:end
"""Verify H10 treatment-denominator config and Snakemake wiring."""

from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[3]
CONFIG_FULL = ROOT / "code" / "config" / "config-full.yml"
SNAKEFILE = ROOT / "code" / "workflows" / "Snakefile"
H10_FREQ_SCRIPT = ROOT / "code" / "scripts" / "create_h10_treatment_freq_tables.py"


def test_config_full_defines_curated_h10_treatment_denominator_labels() -> None:
    config = yaml.safe_load(CONFIG_FULL.read_text()) or {}
    block = config["h10_treatment_denominator"]

    assert block["broad_treatment_exposed_studies"] == [
        "blca_dfarber_mskcc_2014",
        "brca_dfci_2020",
        "brca_fuscc_2020",
        "brca_mskcc_2019",
        "mel_ucla_2016",
        "mixed_allen_2018",
        "nepc_wcm_2016",
        "nsclc_mskcc_2018",
        "prad_su2c_2019",
        "skcm_mskcc_2014",
    ]
    assert block["mutagenic_treatment_signal_studies"] == ["blca_dfarber_mskcc_2014"]
    assert block["mutagenic_treatment_signal_sensitivity_only_studies"] == [
        "sclc_cancercell_gardner_2017",
        "pptc_2019",
    ]
    assert block["positive_naive_or_pretreatment_studies"] == [
        "lung_nci_2022",
        "lusc_cptac_2021",
        "mbl_dkfz_2017",
    ]
    assert block["unknown_treatment_metadata_studies"] == [
        "aml_stjude_2024",
        "msk_impact_50k_2026",
    ]
    assert block["sample_level_rules"] == {
        "difg_glass_2019_tmz": {
            "study_id": "difg_glass_2019",
            "target": "mutagenic_treatment_signal",
            "clinical_sample_file": "data_clinical_sample.txt",
            "sample_id_column": "SAMPLE_ID",
            "positive_columns": {"TMZ_TREATMENT": ["Yes"]},
        },
        "difg_glass_2019_tmz_unknown": {
            "study_id": "difg_glass_2019",
            "target": "treatment_metadata_unknown",
            "clinical_sample_file": "data_clinical_sample.txt",
            "sample_id_column": "SAMPLE_ID",
            "positive_columns": {"TMZ_TREATMENT": [""]},
        },
        "blca_cornell_2016_post_chemo": {
            "study_id": "blca_cornell_2016",
            "target": "mutagenic_treatment_signal",
            "clinical_sample_file": "data_clinical_sample.txt",
            "sample_id_column": "SAMPLE_ID",
            "positive_columns": {
                "SPECIMEN_COLLECTION_PRE_OR_POST_CHEMO": ["post-chemotherapy"]
            },
        },
        "blca_cornell_2016_pre_chemo": {
            "study_id": "blca_cornell_2016",
            "target": "positive_naive_or_pretreatment",
            "clinical_sample_file": "data_clinical_sample.txt",
            "sample_id_column": "SAMPLE_ID",
            "positive_columns": {
                "SPECIMEN_COLLECTION_PRE_OR_POST_CHEMO": ["pre-chemotherapy"]
            },
        },
    }


def test_snakefile_exposes_h10_treatment_annotation_target() -> None:
    text = SNAKEFILE.read_text()
    rule = _extract_rule_block(text, "annotate_treatment_exposure")
    target = _extract_rule_block(text, "all_h10_treatment_annotations")

    assert "metadata/samples_treatment_exposure.feather" in rule
    assert "metadata/samples_treatment_exposure_counts.tsv" in rule
    assert "metadata/samples_annotated.feather" in rule
    assert "annotate_treatment_exposure.py" in rule
    assert "--data-dir {params.data_dir}" in rule
    assert "metadata/samples_treatment_exposure.feather" in target


def test_snakefile_exposes_h10_treatment_frequency_views_target() -> None:
    text = SNAKEFILE.read_text()
    rule = _extract_rule_block(text, "create_h10_treatment_freq_tables")
    target = _extract_rule_block(text, "all_h10_treatment_freq_tables")

    assert "studies/{id}/mut/table/gene_cancer_h10_treatment_views.feather" in rule
    assert "create_h10_treatment_freq_tables.py" in rule
    assert "mut_filtered.feather" in text
    assert "studies/{wildcards.id}/metadata/samples.feather" in text
    assert "metadata/samples_treatment_exposure.feather" in text
    assert "gene_cancer_h10_treatment_views.feather" in target


def test_h10_treatment_frequency_script_is_snakemake_script_compatible() -> None:
    text = H10_FREQ_SCRIPT.read_text()

    assert "from __future__ import annotations" not in text
    assert 'elif __name__ == "__main__":' in text


def test_snakefile_exposes_h10_treatment_impact_target_and_datapackage() -> None:
    text = SNAKEFILE.read_text()
    rule = _extract_rule_block(text, "create_h10_treatment_impact_table")
    package_rule = _extract_rule_block(text, "package_h10_treatment_impact")
    target = _extract_rule_block(text, "all_h10_treatment_impact")

    assert "gene_cancer_h10_treatment_views.feather" in rule
    assert "gene_cancer_h10_treatment_impact.feather" in rule
    assert "gene_cancer_h10_treatment_impact_ratio.feather" in rule
    assert "create_h10_treatment_impact_table.py" in rule
    assert "gene_cancer_h10_treatment_impact.datapackage.json" in package_rule
    assert "write_datapackage.py" in package_rule
    assert "gene_cancer_h10_treatment_impact_ratio.feather" in target
    assert "gene_cancer_h10_treatment_impact.datapackage.json" in target


def _extract_rule_block(text: str, rule_name: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    in_rule = False
    rule_indent = ""
    for line in lines:
        stripped = line.lstrip()
        indent = line[: len(line) - len(stripped)]
        if stripped.startswith(f"rule {rule_name}:"):
            in_rule = True
            rule_indent = indent
            out.append(line)
            continue
        if in_rule:
            if line.strip() == "":
                out.append(line)
                continue
            if len(indent) > len(rule_indent):
                out.append(line)
            else:
                break
    assert out, f"rule {rule_name} not found"
    return "\n".join(out)
