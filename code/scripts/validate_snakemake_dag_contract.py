# science:code
# status: workflow-owned
# science:end
"""Validate static and dry-run contracts for the Snakemake workflow DAG."""

import argparse
import ast
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


PATHLIKE_SUFFIXES = (
    ".bed",
    ".csv",
    ".feather",
    ".gz",
    ".html",
    ".json",
    ".md",
    ".parquet",
    ".staged",
    ".tar.gz",
    ".tsv",
    ".txt",
    ".xlsx",
)
READ_FUNCTIONS = {"read_csv", "read_excel", "read_feather", "read_parquet", "open"}
REGISTERED_INTERNAL_INPUTS = {
    # SELECT opt-in branch: these substrates are intentionally pre-staged by
    # upstream exploratory runs today. t193/t194 can promote them into produced
    # datapackages/rules before SELECT becomes part of the default interpretation
    # surface.
    "{out_dir}/metadata/bailey_alteration_class.feather",
    "{out_dir}/summary/mut/table/gene_sample_long.feather",
}


@dataclass(frozen=True)
class RuleContract:
    name: str
    inputs: set[str]
    outputs: set[str]
    script: Path | None


@dataclass(frozen=True)
class LiteralRead:
    path: str
    line: int


@dataclass(frozen=True)
class DagFinding:
    check: str
    path: str
    rule: str
    details: str


@dataclass(frozen=True)
class DryRunResult:
    configfile: Path
    passed: bool
    stdout_tail: str
    stderr_tail: str


def parse_rule_contracts(
    snakefile_text: str, *, workflow_dir: Path
) -> list[RuleContract]:
    """Extract a conservative static contract for each Snakemake rule block."""
    rules: list[RuleContract] = []
    for name, block in _rule_blocks(snakefile_text):
        script = _extract_script(block, workflow_dir=workflow_dir)
        rules.append(
            RuleContract(
                name=name,
                inputs=_extract_section_paths(block, "input"),
                outputs=_extract_section_paths(block, "output"),
                script=script,
            )
        )
    return rules


def detect_duplicate_outputs(rules: list[RuleContract]) -> list[DagFinding]:
    """Return one finding per output path owned by multiple rules."""
    owners: dict[str, list[str]] = {}
    for rule in rules:
        for output in rule.outputs:
            owners.setdefault(output, []).append(rule.name)
    findings: list[DagFinding] = []
    for output, rule_names in sorted(owners.items()):
        if len(rule_names) > 1:
            findings.append(
                DagFinding(
                    check="single-writer output ownership",
                    path=output,
                    rule=", ".join(sorted(rule_names)),
                    details=f"output is produced by {len(rule_names)} rules: {', '.join(sorted(rule_names))}",
                )
            )
    return findings


def detect_orphan_internal_inputs(rules: list[RuleContract]) -> list[DagFinding]:
    """Return internal out_dir inputs that no rule declares as an output."""
    outputs = {output for rule in rules for output in rule.outputs}
    findings: list[DagFinding] = []
    for rule in rules:
        for input_path in sorted(rule.inputs):
            if not _is_internal_path(input_path):
                continue
            if input_path in REGISTERED_INTERNAL_INPUTS:
                continue
            if _produced_by_any(input_path, outputs):
                continue
            findings.append(
                DagFinding(
                    check="internal input has producer",
                    path=input_path,
                    rule=rule.name,
                    details="declared input is under out_dir but no rule declares the same output pattern",
                )
            )
    return findings


def scan_literal_project_reads(script_path: Path) -> list[LiteralRead]:
    """Find literal project-relative file reads in a Python script."""
    try:
        tree = ast.parse(script_path.read_text())
    except SyntaxError as exc:
        return [LiteralRead(path=f"<syntax-error: {exc.msg}>", line=exc.lineno or 0)]

    reads: list[LiteralRead] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not _is_read_call(node):
            continue
        if not node.args:
            continue
        first_arg = node.args[0]
        if isinstance(first_arg, ast.Constant) and isinstance(first_arg.value, str):
            path = _normalize_path(first_arg.value)
            if _is_project_relative_path(path):
                reads.append(LiteralRead(path=path, line=node.lineno))
    return sorted(reads, key=lambda read: (read.path, read.line))


def detect_hardcoded_project_reads(rules: list[RuleContract]) -> list[DagFinding]:
    """Return script reads of project files that are not declared as rule inputs."""
    findings: list[DagFinding] = []
    for rule in rules:
        if (
            rule.script is None
            or not rule.script.exists()
            or rule.script.suffix != ".py"
        ):
            continue
        for read in scan_literal_project_reads(rule.script):
            if read.path.startswith("<syntax-error:"):
                findings.append(
                    DagFinding(
                        check="script parseable for DAG input audit",
                        path=str(rule.script),
                        rule=rule.name,
                        details=read.path,
                    )
                )
                continue
            if read.path in rule.inputs:
                continue
            findings.append(
                DagFinding(
                    check="declared-input completeness for script reads",
                    path=read.path,
                    rule=rule.name,
                    details=f"{rule.script}:{read.line} reads a project file literal not declared as a rule input",
                )
            )
    return findings


def run_dry_runs(
    *,
    snakefile: Path,
    configfiles: list[Path],
    repo_root: Path,
    target: str = "all",
    timeout_seconds: int = 180,
) -> list[DryRunResult]:
    """Run Snakemake dry-runs for the configured shipped configs."""
    results: list[DryRunResult] = []
    for configfile in configfiles:
        cache_root = Path("/tmp/cbioportal-snakemake-cache")
        cache_root.mkdir(parents=True, exist_ok=True)
        env = os.environ.copy()
        env["XDG_CACHE_HOME"] = str(cache_root)
        cmd = [
            "uv",
            "run",
            "--frozen",
            "snakemake",
            "-s",
            str(snakefile),
            "--configfile",
            str(configfile),
            "--config",
            f"out_dir=/tmp/cbioportal-dag-dryrun/{configfile.stem}",
            "-n",
            target,
            "--quiet",
        ]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=repo_root,
            env=env,
            timeout=timeout_seconds,
            check=False,
        )
        results.append(
            DryRunResult(
                configfile=configfile,
                passed=result.returncode == 0,
                stdout_tail=_tail(result.stdout),
                stderr_tail=_tail(result.stderr),
            )
        )
    return results


def validate_contract(
    *,
    snakefile: Path,
    repo_root: Path,
    configfiles: list[Path],
    run_dry_run_checks: bool,
    target: str = "all",
) -> tuple[list[RuleContract], list[DagFinding], list[DryRunResult]]:
    workflow_dir = snakefile.parent
    rules = parse_rule_contracts(snakefile.read_text(), workflow_dir=workflow_dir)
    findings = [
        *detect_duplicate_outputs(rules),
        *detect_orphan_internal_inputs(rules),
        *detect_hardcoded_project_reads(rules),
    ]
    dry_runs = (
        run_dry_runs(
            snakefile=snakefile,
            configfiles=configfiles,
            repo_root=repo_root,
            target=target,
        )
        if run_dry_run_checks
        else []
    )
    return rules, findings, dry_runs


def render_markdown(
    *,
    rules: list[RuleContract],
    findings: list[DagFinding],
    dry_runs: list[DryRunResult],
) -> str:
    dry_run_failed = [result for result in dry_runs if not result.passed]
    status = "PASS" if not findings and not dry_run_failed else "FAIL"
    lines = [
        "# QA report: Snakemake DAG contract",
        "",
        f"Status: {status}",
        "",
        f"Rules checked: {len(rules)}",
        f"Static findings: {len(findings)}",
        f"Dry-runs checked: {len(dry_runs)}",
        "",
        "## Static Findings",
        "",
    ]
    if findings:
        lines.extend(["| Check | Rule | Path | Details |", "| --- | --- | --- | --- |"])
        for finding in findings:
            lines.append(
                "| "
                + " | ".join(
                    [
                        finding.check,
                        finding.rule,
                        finding.path,
                        finding.details.replace("|", "\\|").replace("\n", " "),
                    ]
                )
                + " |"
            )
    else:
        lines.append("No static DAG contract findings.")
    lines.extend(["", "## Dry-Runs", ""])
    if dry_runs:
        lines.extend(["| Config | Status | Output tail |", "| --- | --- | --- |"])
        for result in dry_runs:
            tail = (
                (result.stderr_tail or result.stdout_tail)
                .replace("|", "\\|")
                .replace("\n", "<br>")
            )
            lines.append(
                f"| {result.configfile} | {'PASS' if result.passed else 'FAIL'} | {tail} |"
            )
    else:
        lines.append("Dry-run checks were not requested.")
    lines.append("")
    return "\n".join(lines)


def _rule_blocks(text: str) -> list[tuple[str, str]]:
    lines = text.splitlines()
    blocks: list[tuple[str, str]] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.lstrip()
        match = re.match(
            r"(?:rule|checkpoint)\s+([A-Za-z_][A-Za-z0-9_]*)\s*:", stripped
        )
        if not match:
            i += 1
            continue
        rule_indent = len(line) - len(stripped)
        name = match.group(1)
        block_lines = [line]
        i += 1
        while i < len(lines):
            next_line = lines[i]
            next_stripped = next_line.lstrip()
            next_indent = len(next_line) - len(next_stripped)
            if (
                next_stripped
                and not next_stripped.startswith("#")
                and next_indent <= rule_indent
            ):
                break
            block_lines.append(next_line)
            i += 1
        blocks.append((name, "\n".join(block_lines)))
    return blocks


def _extract_section_paths(block: str, section: str) -> set[str]:
    section_text = _section_text(block, section)
    if section_text is None:
        return set()
    return _extract_paths(section_text)


def _section_text(block: str, section: str) -> str | None:
    lines = block.splitlines()
    out: list[str] = []
    in_section = False
    section_indent = 0
    for line in lines:
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        if re.match(rf"{section}\s*:", stripped):
            in_section = True
            section_indent = indent
            tail = stripped.split(":", 1)[1]
            if tail.strip():
                out.append(tail)
            continue
        if not in_section:
            continue
        if stripped and not stripped.startswith("#") and indent <= section_indent:
            break
        out.append(line)
    if not in_section:
        return None
    return "\n".join(out)


def _extract_paths(text: str) -> set[str]:
    paths: set[str] = set()
    joinpath_spans: list[tuple[int, int]] = []
    for prefix, marker in (("{out_dir}", "out_dir"), ("{data_dir}", "data_dir")):
        for match in re.finditer(
            rf"{marker}\.joinpath\(\s*f?[\"']([^\"']+)[\"']", text
        ):
            paths.add(_normalize_path(f"{prefix}/{match.group(1)}"))
            joinpath_spans.append(match.span(1))
    for match in re.finditer(r"(?<![A-Za-z0-9_])f?[\"']([^\"']+)[\"']", text):
        literal = match.group(1)
        if _span_inside(match.span(1), joinpath_spans):
            continue
        if _is_pathlike_literal(literal):
            paths.add(_normalize_path(literal))
    return paths


def _extract_script(block: str, *, workflow_dir: Path) -> Path | None:
    script_text = _section_text(block, "script")
    if script_text is None:
        return None
    match = re.search(r"[\"']([^\"']+)[\"']", script_text)
    if not match:
        return None
    return (workflow_dir / match.group(1)).resolve().relative_to(Path.cwd())


def _span_inside(span: tuple[int, int], containers: list[tuple[int, int]]) -> bool:
    return any(start <= span[0] and span[1] <= end for start, end in containers)


def _is_read_call(node: ast.Call) -> bool:
    func = node.func
    if isinstance(func, ast.Name):
        return func.id in READ_FUNCTIONS
    if isinstance(func, ast.Attribute):
        return func.attr in READ_FUNCTIONS
    return False


def _is_pathlike_literal(value: str) -> bool:
    normalized = _normalize_path(value)
    return "/" in normalized and (
        normalized.startswith(("data/", "results/", "code/", "doc/", "../scripts/"))
        or normalized.endswith(PATHLIKE_SUFFIXES)
    )


def _is_project_relative_path(value: str) -> bool:
    return value.startswith(("data/", "results/", "code/", "doc/"))


def _is_internal_path(path: str) -> bool:
    return path.startswith("{out_dir}/")


def _produced_by_any(input_path: str, outputs: set[str]) -> bool:
    return any(_pattern_covers(output, input_path) for output in outputs)


def _pattern_covers(output_pattern: str, input_path: str) -> bool:
    if output_pattern == input_path:
        return True
    output_regex = _wildcard_pattern_to_regex(output_pattern)
    if re.fullmatch(output_regex, input_path):
        return True
    input_regex = _wildcard_pattern_to_regex(input_path)
    if re.fullmatch(input_regex, output_pattern):
        return True
    output_prefix = output_pattern.rstrip("/") + "/"
    return input_path.startswith(output_prefix)


def _wildcard_pattern_to_regex(pattern: str) -> str:
    escaped = re.escape(pattern)
    return re.sub(r"\\\{[^{}]+\\\}", r"[^/]+", escaped)


def _normalize_path(path: str) -> str:
    return path.replace("{{", "{").replace("}}", "}").replace("//", "/")


def _tail(text: str, n: int = 12) -> str:
    return "\n".join(text.splitlines()[-n:])


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--snakefile", type=Path, default=Path("code/workflows/Snakefile")
    )
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--configfile", type=Path, action="append", default=[])
    parser.add_argument("--target", default="all")
    parser.add_argument("--skip-dry-runs", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    repo_root = args.repo_root.resolve()
    snakefile = args.snakefile
    configfiles = args.configfile
    rules, findings, dry_runs = validate_contract(
        snakefile=snakefile,
        repo_root=repo_root,
        configfiles=configfiles,
        run_dry_run_checks=not args.skip_dry_runs,
        target=args.target,
    )
    report = render_markdown(rules=rules, findings=findings, dry_runs=dry_runs)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report)
    if findings or any(not result.passed for result in dry_runs):
        raise SystemExit(1)


def _run_via_snakemake() -> None:
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821
    snakefile = Path(str(snek.input.snakefile))
    configfiles = [Path(str(path)) for path in snek.input.configfiles]
    output = Path(str(snek.output[0]))
    rules, findings, dry_runs = validate_contract(
        snakefile=snakefile,
        repo_root=Path.cwd(),
        configfiles=configfiles,
        run_dry_run_checks=True,
        target=str(snek.params.get("target", "all")),
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        render_markdown(rules=rules, findings=findings, dry_runs=dry_runs)
    )
    if findings or any(not result.passed for result in dry_runs):
        raise SystemExit(1)


if "snakemake" in globals():
    _run_via_snakemake()
elif __name__ == "__main__":
    main()
