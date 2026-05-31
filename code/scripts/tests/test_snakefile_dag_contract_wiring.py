# science:code
# status: library
# science:end
"""Verify the workflow DAG contract guard is exposed as a Snakemake target."""

from pathlib import Path

SNAKEFILE = Path(__file__).resolve().parents[3] / "code" / "workflows" / "Snakefile"


def test_workflow_dag_contract_rule_present() -> None:
    text = SNAKEFILE.read_text()

    assert "rule validate_workflow_dag_contract:" in text
    assert "validate_snakemake_dag_contract.py" in text
    assert "qa/workflow/dag_contract.qa_report.md" in text


def test_all_workflow_qa_target_present() -> None:
    text = SNAKEFILE.read_text()

    assert "rule all_workflow_qa:" in text
    assert "workflow_qa_reports" in text


def test_all_qa_includes_workflow_qa_reports() -> None:
    text = SNAKEFILE.read_text()
    all_qa = _extract_rule_block(text, "all_qa")

    assert "mutation_qa_reports" in all_qa
    assert "workflow_qa_reports" in all_qa


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
