# science:code
# status: library
# science:end
"""Tests for the workflow-level Snakemake DAG contract validator."""

from __future__ import annotations

from pathlib import Path

from validate_snakemake_dag_contract import (
    RuleContract,
    detect_duplicate_outputs,
    detect_hardcoded_project_reads,
    detect_orphan_internal_inputs,
    parse_rule_contracts,
    scan_literal_project_reads,
)


def test_detect_duplicate_outputs_reports_single_writer_violation() -> None:
    rules = [
        RuleContract(
            name="make_a", inputs=set(), outputs={"{out_dir}/same.feather"}, script=None
        ),
        RuleContract(
            name="make_b", inputs=set(), outputs={"{out_dir}/same.feather"}, script=None
        ),
    ]

    findings = detect_duplicate_outputs(rules)

    assert len(findings) == 1
    assert findings[0].check == "single-writer output ownership"
    assert "make_a" in findings[0].details
    assert "make_b" in findings[0].details


def test_detect_orphan_internal_inputs_allows_external_data_inputs() -> None:
    rules = [
        RuleContract(
            name="consumer",
            inputs={
                "{out_dir}/missing.feather",
                "data/source.tsv",
                "{data_dir}/{id}/raw.tsv",
            },
            outputs={"{out_dir}/made.feather"},
            script=None,
        )
    ]

    findings = detect_orphan_internal_inputs(rules)

    assert [finding.path for finding in findings] == ["{out_dir}/missing.feather"]


def test_scan_literal_project_reads_finds_hardcoded_data_reads(tmp_path: Path) -> None:
    script = tmp_path / "script.py"
    script.write_text(
        "\n".join(
            [
                "import pandas as pd",
                "df = pd.read_csv('data/grch37.tsv', sep='\\t')",
                "other = pd.read_feather(snek.input.table)",
            ]
        )
    )

    reads = scan_literal_project_reads(script)

    assert [(read.path, read.line) for read in reads] == [("data/grch37.tsv", 2)]


def test_detect_hardcoded_project_reads_requires_declared_input(tmp_path: Path) -> None:
    script = tmp_path / "script.py"
    script.write_text("import pandas as pd\npd.read_csv('data/grch37.tsv')\n")
    rules = [
        RuleContract(
            name="convert", inputs={"data/grch38.tsv"}, outputs=set(), script=script
        )
    ]

    findings = detect_hardcoded_project_reads(rules)

    assert len(findings) == 1
    assert findings[0].check == "declared-input completeness for script reads"
    assert findings[0].path == "data/grch37.tsv"


def test_parse_rule_contracts_extracts_script_inputs_and_outputs() -> None:
    snakefile = """
rule make_table:
  input:
    raw = data_dir.joinpath("{id}/raw.tsv"),
    ref = "data/reference.tsv"
  output:
    out_dir.joinpath("summary/table.feather")
  script:
    "../scripts/make_table.py"
"""

    rules = parse_rule_contracts(snakefile, workflow_dir=Path("code/workflows"))

    assert len(rules) == 1
    assert rules[0].name == "make_table"
    assert rules[0].inputs == {"{data_dir}/{id}/raw.tsv", "data/reference.tsv"}
    assert rules[0].outputs == {"{out_dir}/summary/table.feather"}
    assert rules[0].script == Path("code/scripts/make_table.py")
