# science:code
# status: library
# science:end
"""Verifies rule (0) is wired into the Snakefile correctly."""
from pathlib import Path

SNAKEFILE = Path(__file__).resolve().parents[3] / "code" / "workflows" / "Snakefile"


def test_snakefile_declares_preflight_rule():
    text = SNAKEFILE.read_text()
    assert "rule preflight_select_env:" in text


def test_preflight_rule_uses_select_conda_env():
    text = SNAKEFILE.read_text()
    block = _extract_rule_block(text, "preflight_select_env")
    # Snakefile `conda:` paths resolve relative to the Snakefile, so the
    # canonical reference is "../envs/select.yml" -- match the suffix.
    assert "envs/select.yml" in block, "must use the SELECT conda env (envs/select.yml)"


def test_preflight_rule_consumes_vendored_tarball():
    text = SNAKEFILE.read_text()
    block = _extract_rule_block(text, "preflight_select_env")
    assert "data/external/select_v1.6.4.tar.gz" in block


def test_preflight_rule_writes_token():
    text = SNAKEFILE.read_text()
    block = _extract_rule_block(text, "preflight_select_env")
    assert ".preflight_ok" in block


def _extract_rule_block(text: str, rule_name: str) -> str:
    """Return the source of one rule block (rule_name + its indented body).

    Tolerates rules that live inside an `if select_enabled:` block by latching
    onto the indentation of the `rule <name>:` line and capturing all subsequent
    lines that are blank or more deeply indented.
    """
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
