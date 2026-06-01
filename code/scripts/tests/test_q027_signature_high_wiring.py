# science:code
# status: library
# science:end
"""Verify q027 signature-high config and Snakemake wiring."""

from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[3]
CONFIG = ROOT / "code" / "config" / "config-q027-therapy-signature-high.yml"
SNAKEFILE = ROOT / "code" / "workflows" / "Snakefile"


def test_q027_config_scopes_first_pass_to_wp1_passing_glass_sbs11() -> None:
    config = yaml.safe_load(CONFIG.read_text()) or {}

    assert config["studies"] == ["difg_glass_2019"]
    assert config["signature_assignment_lookup_keys"] == ["cns"]
    assert config["signature_assignment_extra_signatures"] == [
        "SBS11",
        "SBS31",
        "SBS35",
        "SBS87",
    ]
    assert config["q027_therapy_signature_targets"] == {
        "difg_glass_2019": {
            "target_signatures": ["SBS11"],
            "primary_patient_denominator": True,
            "wp1_gate": "passed",
        }
    }


def test_snakefile_exposes_separate_q027_signature_high_target_and_datapackage() -> (
    None
):
    text = SNAKEFILE.read_text()
    assignment_rule = _extract_rule_block(
        text, "run_q027_restricted_sigprofiler_assignment_per_sample"
    )
    labels_rule = _extract_rule_block(text, "annotate_q027_signature_high")
    freq_rule = _extract_rule_block(text, "create_q027_signature_high_freq_tables")
    impact_rule = _extract_rule_block(text, "create_q027_signature_high_impact_table")
    package_rule = _extract_rule_block(text, "package_q027_signature_high_impact")
    target = _extract_rule_block(text, "all_q027_signature_high_impact")

    assert "restricted_assignment_q027_per_sample.feather" in assignment_rule
    assert "run_restricted_sigprofiler_assignment.py" in assignment_rule
    assert "samples_q027_signature_high.feather" in labels_rule
    assert "annotate_q027_signature_high.py" in labels_rule
    assert "gene_cancer_q027_signature_high_views.feather" in freq_rule
    assert "create_q027_signature_high_freq_tables.py" in freq_rule
    assert "gene_cancer_q027_signature_high_impact.feather" in impact_rule
    assert "gene_cancer_q027_signature_high_impact_ratio.feather" in impact_rule
    assert "create_q027_signature_high_impact_table.py" in impact_rule
    assert "gene_cancer_q027_signature_high_impact.datapackage.json" in package_rule
    assert "write_datapackage.py" in package_rule
    assert "gene_cancer_q027_signature_high_impact_ratio.feather" in target
    assert "gene_cancer_q027_signature_high_impact.datapackage.json" in target


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
