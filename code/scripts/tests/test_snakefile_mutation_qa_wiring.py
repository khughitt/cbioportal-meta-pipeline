# science:code
# status: library
# science:end
"""Verify mutation artifact QA is a Snakemake-visible target."""

from pathlib import Path

SNAKEFILE = Path(__file__).resolve().parents[3] / "code" / "workflows" / "Snakefile"


EXPECTED_QA_RULES = [
    "qa_per_study_mutation_substrates",
    "qa_samples_annotated",
    "qa_gene_cancer_pooled_input",
    "qa_gene_cancer_pooled_bundle",
    "qa_gene_cancer_study_annotated",
    "qa_gene_cancer_study_ratio_annotated",
    "all_qa",
]


def test_mutation_qa_rules_present() -> None:
    text = SNAKEFILE.read_text()
    for rule_name in EXPECTED_QA_RULES:
        assert f"rule {rule_name}:" in text, f"missing rule {rule_name}"


def test_rule_all_includes_mutation_qa_reports() -> None:
    text = SNAKEFILE.read_text()
    rule_all = _extract_rule_block(text, "all")

    assert "mutation_qa_reports" in rule_all
    assert "qa/mutation/samples_annotated.qa_report.md" in text
    assert "qa/mutation/gene_cancer_pooled_bundle.qa_report.md" in text
    assert "qa/mutation/gene_cancer_study_ratio_annotated.qa_report.md" in text
    assert "studies/{id}/qa/mutation_substrates.qa_report.md" in text


def test_mutation_qa_rules_use_shared_validator_script() -> None:
    text = SNAKEFILE.read_text()
    for rule_name in EXPECTED_QA_RULES[:-1]:
        block = _extract_rule_block(text, rule_name)
        assert "validate_mutation_pipeline_artifacts.py" in block, (
            f"{rule_name} missing validator script"
        )


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
