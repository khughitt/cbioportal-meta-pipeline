# science:code
# status: exploratory
# science:end
"""Build isolated Snakemake commands for t173 dNdScv LOSO reruns."""

from __future__ import annotations

import json
import shlex
from pathlib import Path
from typing import Any

import click
import pandas as pd
import yaml

DEFAULT_SNAKEFILE = Path("code/workflows/Snakefile")
DEFAULT_TARGET = "aggregate_dndscv_per_gene"


def load_studies_from_config(config_path: Path) -> list[str]:
    """Read the study list from a Snakemake YAML config."""
    config = yaml.safe_load(config_path.read_text())
    if not isinstance(config, dict):
        raise ValueError(f"{config_path} did not parse to a YAML mapping")
    studies = config.get("studies")
    if not isinstance(studies, list) or not all(
        isinstance(study, str) for study in studies
    ):
        raise ValueError(f"{config_path} must define studies as a list of strings")
    return studies


def build_loso_manifest(
    studies: list[str],
    config_path: Path,
    out_root: Path,
    pilot_study: str | None = None,
    snakefile: Path = DEFAULT_SNAKEFILE,
    target: str = DEFAULT_TARGET,
    jobs: int = 1,
) -> pd.DataFrame:
    """Return one isolated dNdScv rerun command per requested holdout."""
    holdouts = [pilot_study] if pilot_study is not None else list(studies)
    unknown = sorted(set(holdouts) - set(studies))
    if unknown:
        raise ValueError(
            f"pilot/holdout studies not present in config study list: {', '.join(unknown)}"
        )

    rows: list[dict[str, Any]] = []
    for excluded_study in holdouts:
        included_studies = [study for study in studies if study != excluded_study]
        included_studies_json = json.dumps(included_studies, separators=(",", ":"))
        out_dir = out_root / f"exclude_{excluded_study}"
        command = _snakemake_command(
            config_path=config_path,
            out_dir=out_dir,
            studies_json=included_studies_json,
            snakefile=snakefile,
            target=target,
            jobs=jobs,
            dry_run=False,
        )
        dry_run_command = _snakemake_command(
            config_path=config_path,
            out_dir=out_dir,
            studies_json=included_studies_json,
            snakefile=snakefile,
            target=target,
            jobs=jobs,
            dry_run=True,
        )
        rows.append(
            {
                "excluded_study_id": excluded_study,
                "n_included_studies": len(included_studies),
                "included_studies_json": included_studies_json,
                "out_dir": str(out_dir),
                "command": command,
                "dry_run_command": dry_run_command,
            }
        )
    return pd.DataFrame(rows)


def _snakemake_command(
    config_path: Path,
    out_dir: Path,
    studies_json: str,
    snakefile: Path,
    target: str,
    jobs: int,
    dry_run: bool,
) -> str:
    args = [
        "uv",
        "run",
        "--frozen",
        "snakemake",
        "-s",
        str(snakefile),
        "--configfile",
        str(config_path),
        "--use-conda",
        "-j",
        str(jobs),
    ]
    if dry_run:
        args.append("-n")
    args.append(target)
    command_parts = [shlex.quote(arg) for arg in args]
    command_parts.append("--config")
    command_parts.append(shlex.quote(f"out_dir={out_dir}"))
    command_parts.append(f"studies={shlex.quote(studies_json)}")
    return " ".join(command_parts)


@click.command()
@click.option(
    "--config",
    "config_path",
    type=Path,
    required=True,
    help="Base dNdScv Snakemake config",
)
@click.option(
    "--out-root",
    type=Path,
    required=True,
    help="Root for isolated exclude_<study> runs",
)
@click.option(
    "--pilot-study", type=str, default=None, help="Emit only this holdout study"
)
@click.option(
    "--manifest-out", type=Path, required=True, help="TSV path for the run manifest"
)
@click.option(
    "--jobs", type=int, default=1, show_default=True, help="Snakemake -j value to embed"
)
def main(
    config_path: Path,
    out_root: Path,
    pilot_study: str | None,
    manifest_out: Path,
    jobs: int,
) -> None:
    studies = load_studies_from_config(config_path)
    manifest = build_loso_manifest(
        studies=studies,
        config_path=config_path,
        out_root=out_root,
        pilot_study=pilot_study,
        jobs=jobs,
    )
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    manifest.to_csv(manifest_out, sep="\t", index=False)
    click.echo(f"wrote {len(manifest):,} dNdScv LOSO command(s): {manifest_out}")


if __name__ == "__main__":
    main()
