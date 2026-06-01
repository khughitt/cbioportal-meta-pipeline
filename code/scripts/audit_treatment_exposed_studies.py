# science:code
# status: exploratory
# science:end
"""Audit cBioPortal study metadata for H10 treatment-exposure candidate cohorts.

This is a conservative scaffold for task:t206. It does not make final cohort labels from
signatures or downstream mutation burden; it only surfaces metadata/clinical-label evidence that a
study should be flagged or manually reviewed before the H10 frequency-table impact pass.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import click
import yaml


NEGATIVE_PATTERNS = (
    "treatment-naive",
    "treatment naive",
    "previously untreated",
    "untreated",
    "pre-treatment",
    "pretreatment",
)

EXPLICIT_TREATMENT_PATTERNS = (
    "pretreated",
    "pre-treated",
    "post-treatment",
    "post treatment",
    "post-chemotherapy",
    "post chemotherapy",
    "chemotherapy",
    "chemosensitive",
    "chemoresistant",
    "therapy-related",
    "prior therapy",
    "prior treatment",
    "refractory",
    "resistant",
    "platinum",
    "cisplatin",
    "temozolomide",
    "tmz",
    "thiopurine",
    "melphalan",
)

GENERIC_TREATMENT_PATTERNS = (
    "exposed",
    "treated",
)

ADVANCED_PATTERNS = (
    "metastatic",
    "advanced",
    "relapsed",
    "relapse",
    "recurrent",
    "castrate resistant",
    "castration resistant",
)

CLINICAL_COLUMN_PATTERNS = (
    "TREAT",
    "THERAP",
    "CHEMO",
    "PLATIN",
    "TMZ",
    "TEMOZOLOMIDE",
    "RELAP",
    "RECURRENT",
    "METAST",
)


@dataclass(frozen=True)
class StudyClassification:
    tier: str
    recommendation: str
    signals: tuple[str, ...]
    negative_signals: tuple[str, ...]


def parse_meta_study(path: Path) -> dict[str, str]:
    """Parse cBioPortal meta_study.txt key/value files, including CR-separated files."""
    text = path.read_text(encoding="utf-8", errors="replace").replace("\r", "\n")
    parsed: dict[str, str] = {}
    for line in text.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        parsed[key.strip()] = value.strip()
    return parsed


def classify_study_text(text: str) -> StudyClassification:
    lowered = " ".join(text.casefold().split())
    negative = _collect_patterns(lowered, NEGATIVE_PATTERNS)
    explicit = _collect_patterns(lowered, EXPLICIT_TREATMENT_PATTERNS)
    generic_explicit = (
        ()
        if negative or explicit
        else _collect_patterns(lowered, GENERIC_TREATMENT_PATTERNS)
    )
    advanced = _collect_patterns(lowered, ADVANCED_PATTERNS)
    treatment_signals = (*explicit, *generic_explicit)
    signals = (*advanced, *treatment_signals)

    if treatment_signals:
        return StudyClassification(
            tier="explicit_treatment_exposed",
            recommendation="flag_exposed",
            signals=signals,
            negative_signals=negative,
        )
    if advanced:
        return StudyClassification(
            tier="advanced_metastatic_enriched",
            recommendation="review_for_fraction",
            signals=signals,
            negative_signals=negative,
        )
    if negative:
        return StudyClassification(
            tier="treatment_naive_or_pretreatment",
            recommendation="do_not_flag",
            signals=signals,
            negative_signals=negative,
        )
    return StudyClassification(
        tier="no_metadata_signal",
        recommendation="do_not_flag",
        signals=signals,
        negative_signals=negative,
    )


def audit_study(study_id: str, data_dir: Path) -> dict[str, str] | None:
    """Return one audit row for a non-TCGA study, or None for skipped studies."""
    if _is_tcga_study(study_id):
        return None

    study_dir = data_dir / study_id
    meta_path = study_dir / "meta_study.txt"
    if not meta_path.exists():
        return {
            "study_id": study_id,
            "name": "",
            "description": "",
            "candidate_tier": "missing_metadata",
            "recommendation": "needs_manual_review",
            "signals": "",
            "negative_signals": "",
            "clinical_signal_columns": "",
        }

    meta = parse_meta_study(meta_path)
    name = meta.get("name", "")
    description = meta.get("description", "")
    classification = classify_study_text(f"{name} {description}")
    clinical_columns = find_clinical_signal_columns(study_dir)
    if classification.tier == "no_metadata_signal" and clinical_columns:
        classification = StudyClassification(
            tier="clinical_signal_present",
            recommendation="review_for_fraction",
            signals=classification.signals,
            negative_signals=classification.negative_signals,
        )
    return {
        "study_id": study_id,
        "name": name,
        "description": description,
        "candidate_tier": classification.tier,
        "recommendation": classification.recommendation,
        "signals": ";".join(classification.signals),
        "negative_signals": ";".join(classification.negative_signals),
        "clinical_signal_columns": ";".join(clinical_columns),
    }


def find_clinical_signal_columns(study_dir: Path) -> tuple[str, ...]:
    clinical_path = study_dir / "data_clinical_sample.txt"
    if not clinical_path.exists():
        return ()

    header = ""
    with clinical_path.open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            stripped = line.rstrip("\n\r")
            if stripped.startswith("PATIENT_ID") or stripped.startswith("SAMPLE_ID"):
                header = stripped
    if not header:
        return ()

    columns = header.split("\t")
    matched = [
        column
        for column in columns
        if any(pattern in column.upper() for pattern in CLINICAL_COLUMN_PATTERNS)
    ]
    return tuple(dict.fromkeys(matched))


def load_config_studies(path: Path) -> list[str]:
    config = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    studies = config.get("studies", [])
    if not isinstance(studies, list):
        raise ValueError(f"{path} must define 'studies' as a list")
    return [str(study) for study in studies]


def audit_config(config_path: Path, data_dir: Path) -> list[dict[str, str]]:
    rows = [
        row
        for study_id in load_config_studies(config_path)
        if (row := audit_study(study_id, data_dir)) is not None
    ]
    order = {
        "flag_exposed": 0,
        "review_for_fraction": 1,
        "needs_manual_review": 2,
        "do_not_flag": 3,
    }
    return sorted(
        rows,
        key=lambda row: (
            order.get(row["recommendation"], 9),
            row["candidate_tier"],
            row["study_id"],
        ),
    )


def write_audit_tsv(rows: list[dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "study_id",
        "name",
        "description",
        "candidate_tier",
        "recommendation",
        "signals",
        "negative_signals",
        "clinical_signal_columns",
    ]
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def _collect_patterns(text: str, patterns: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(pattern for pattern in patterns if pattern in text)


def _is_tcga_study(study_id: str) -> bool:
    lowered = study_id.casefold()
    return "_tcga" in lowered or lowered.startswith("tcga_") or lowered == "tcga_mc3"


@click.command()
@click.option(
    "--config",
    "config_path",
    type=click.Path(path_type=Path, exists=True),
    required=True,
    help="Pipeline config whose studies list defines the audit universe.",
)
@click.option(
    "--data-dir",
    type=click.Path(path_type=Path, exists=True, file_okay=False),
    required=True,
    help="cBioPortal raw data directory containing per-study meta_study.txt files.",
)
@click.option(
    "--output",
    "output_path",
    type=click.Path(path_type=Path),
    required=True,
    help="TSV audit output path.",
)
def main(config_path: Path, data_dir: Path, output_path: Path) -> None:
    """Write a conservative H10 treatment-exposure candidate audit table."""
    rows = audit_config(config_path, data_dir)
    write_audit_tsv(rows, output_path)
    click.echo(f"Wrote {len(rows)} non-TCGA study audit rows to {output_path}")


if __name__ == "__main__":
    main()
