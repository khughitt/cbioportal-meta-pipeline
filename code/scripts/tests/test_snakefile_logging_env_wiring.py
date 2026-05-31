# science:code
# status: library
# science:end
"""Verify active Snakemake rules declare logs and execution environments."""

from __future__ import annotations

import re
from pathlib import Path

SNAKEFILE = Path(__file__).resolve().parents[3] / "code" / "workflows" / "Snakefile"
PROJECT_ENV = Path(__file__).resolve().parents[2] / "envs" / "project-python.yml"


SPECIALIZED_ENVS = {
    "../envs/dndscv.yml",
    "../envs/r-meta.yml",
    "../envs/select.yml",
}


def test_shared_project_python_env_exists() -> None:
    text = PROJECT_ENV.read_text()

    assert "python" in text
    assert "pandas" in text
    assert "snakemake" in text


def test_executable_rules_have_log_directives() -> None:
    missing = []
    for name, block in _rule_blocks(SNAKEFILE.read_text()):
        if _is_executable_rule(block) and "log:" not in block:
            missing.append(name)

    assert missing == []


def test_executable_rules_declare_conda_envs() -> None:
    missing = []
    for name, block in _rule_blocks(SNAKEFILE.read_text()):
        if _is_executable_rule(block) and "conda:" not in block:
            missing.append(name)

    assert missing == []


def test_python_script_rules_use_shared_project_env() -> None:
    wrong_env = []
    for name, block in _rule_blocks(SNAKEFILE.read_text()):
        if '.py"' not in block:
            continue
        env = _extract_conda_env(block)
        if env != "../envs/project-python.yml":
            wrong_env.append((name, env))

    assert wrong_env == []


def test_specialized_r_envs_are_preserved() -> None:
    text = SNAKEFILE.read_text()

    for env in SPECIALIZED_ENVS:
        assert env in text


def _is_executable_rule(block: str) -> bool:
    return "script:" in block or "shell:" in block


def _extract_conda_env(block: str) -> str | None:
    match = re.search(r'conda:\n\s+"([^"]+)"', block)
    return match.group(1) if match else None


def _rule_blocks(text: str) -> list[tuple[str, str]]:
    lines = text.splitlines()
    blocks: list[tuple[str, str]] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        match = re.match(r"^(\s*)rule\s+([A-Za-z0-9_]+):", line)
        if match:
            indent = len(match.group(1))
            start = index
            index += 1
            while index < len(lines):
                next_line = lines[index]
                if next_line.strip() and _indent(next_line) <= indent:
                    break
                index += 1
            blocks.append((match.group(2), "\n".join(lines[start:index])))
            continue
        index += 1
    return blocks


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip())
