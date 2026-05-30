# science:code
# status: library
# science:end
"""Verify all SELECT rules are present in the Snakefile under the opt-in gate."""

from pathlib import Path

SNAKEFILE = Path(__file__).resolve().parents[3] / "code" / "workflows" / "Snakefile"

EXPECTED_RULES = [
    "preflight_select_env",
    "build_panel_gene_sets",
    "build_select_gene_universe",
    "build_select_gam",
    "build_select_gam_pathway_aggregated",
    "run_select_per_cell",
    "aggregate_select_results",
    "run_select_pathway_aggregated",
]


def test_all_select_rules_present():
    text = SNAKEFILE.read_text()
    for rule_name in EXPECTED_RULES:
        assert f"rule {rule_name}:" in text, f"missing rule {rule_name}"


def test_select_rules_under_opt_in_gate():
    text = SNAKEFILE.read_text()
    assert "if select_enabled:" in text or 'config["select"]["enabled"]' in text


def test_run_select_rules_use_conda_env():
    text = SNAKEFILE.read_text()
    for rule_name in (
        "preflight_select_env",
        "run_select_per_cell",
        "run_select_pathway_aggregated",
    ):
        block = _extract_rule_block(text, rule_name)
        assert "envs/select.yml" in block, f"{rule_name} missing conda env"


def _extract_rule_block(text: str, rule_name: str) -> str:
    """Return the source of one rule block (rule_name + indented body)."""
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
