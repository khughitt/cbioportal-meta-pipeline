# science:code
# status: workflow-owned
# science:end
"""Annotate samples with the H10 treatment-denominator labels.

This is the WP1/WP2 substrate for task:t207. It keeps broad treatment-history
labels, primary mutagenic-treatment labels, PDX/sensitivity labels, confirmed
naive evidence, and unknown metadata as separate booleans so downstream H10
cohort views can choose the right denominator explicitly.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import click
import pandas as pd
import yaml


H10_CONFIG_KEY = "h10_treatment_denominator"

LABEL_COLUMNS = (
    "treatment_exposed_broad",
    "mutagenic_treatment_signal",
    "mutagenic_treatment_signal_sensitivity_only",
    "positive_naive_or_pretreatment",
    "treatment_metadata_unknown",
    "no_detected_treatment_signal",
)

SAMPLE_LEVEL_TARGETS = {
    "treatment_exposed_broad",
    "mutagenic_treatment_signal",
    "mutagenic_treatment_signal_sensitivity_only",
    "positive_naive_or_pretreatment",
    "treatment_metadata_unknown",
}


@dataclass(frozen=True)
class SampleLevelRule:
    rule_id: str
    study_id: str
    target: str
    clinical_sample_file: str
    sample_id_column: str
    positive_columns: Mapping[str, frozenset[str]]


@dataclass(frozen=True)
class TreatmentConfig:
    broad_treatment_exposed_studies: frozenset[str]
    mutagenic_treatment_signal_studies: frozenset[str]
    mutagenic_treatment_signal_sensitivity_only_studies: frozenset[str]
    positive_naive_or_pretreatment_studies: frozenset[str]
    unknown_treatment_metadata_studies: frozenset[str]
    sample_level_rules: Mapping[str, SampleLevelRule]


def load_treatment_config(config: Mapping[str, Any]) -> TreatmentConfig:
    """Parse and validate the top-level ``h10_treatment_denominator`` block."""
    block = config.get(H10_CONFIG_KEY)
    if not isinstance(block, Mapping):
        raise ValueError(f"config must define a mapping at {H10_CONFIG_KEY!r}")

    cfg = TreatmentConfig(
        broad_treatment_exposed_studies=_as_frozenset(
            block, "broad_treatment_exposed_studies"
        ),
        mutagenic_treatment_signal_studies=_as_frozenset(
            block, "mutagenic_treatment_signal_studies"
        ),
        mutagenic_treatment_signal_sensitivity_only_studies=_as_frozenset(
            block, "mutagenic_treatment_signal_sensitivity_only_studies"
        ),
        positive_naive_or_pretreatment_studies=_as_frozenset(
            block, "positive_naive_or_pretreatment_studies"
        ),
        unknown_treatment_metadata_studies=_as_frozenset(
            block, "unknown_treatment_metadata_studies"
        ),
        sample_level_rules=_parse_sample_level_rules(
            block.get("sample_level_rules", {})
        ),
    )
    _validate_treatment_config(cfg)
    return cfg


def annotate_treatment_exposure(
    samples_annotated: pd.DataFrame,
    cfg: TreatmentConfig,
    data_dir: Path,
) -> pd.DataFrame:
    """Return one H10 treatment-label row per canonical sample."""
    _require_columns(samples_annotated, {"study_id", "sample_id"}, "samples_annotated")
    if samples_annotated.duplicated(["study_id", "sample_id"]).any():
        raise ValueError("samples_annotated must be unique on (study_id, sample_id)")

    out = samples_annotated.copy()
    out["study_id"] = out["study_id"].astype(str)
    out["sample_id"] = out["sample_id"].astype(str)
    for column in LABEL_COLUMNS:
        out[column] = False
    out["treatment_label_source"] = ""
    out["treatment_rule_id"] = ""

    _apply_study_level_labels(out, cfg)
    for rule in cfg.sample_level_rules.values():
        _apply_sample_level_rule(out, rule, data_dir=data_dir)

    out["no_detected_treatment_signal"] = ~out[
        [
            "treatment_exposed_broad",
            "mutagenic_treatment_signal",
            "mutagenic_treatment_signal_sensitivity_only",
            "treatment_metadata_unknown",
        ]
    ].any(axis=1)
    no_source = out["no_detected_treatment_signal"] & (
        out["treatment_label_source"] == ""
    )
    out.loc[no_source, "treatment_label_source"] = "no-detected-signal"
    out.loc[no_source, "treatment_rule_id"] = "no_detected_treatment_signal"

    return out


def write_label_counts(annotated: pd.DataFrame, output_path: Path) -> None:
    """Write per-study treatment-label counts for QA and interpretation notes."""
    _require_columns(
        annotated, {"study_id", *LABEL_COLUMNS}, "samples_treatment_exposure"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    grouped = annotated.groupby("study_id", sort=True, observed=True)
    counts = grouped.size().rename("n_samples").to_frame()
    for column in LABEL_COLUMNS:
        counts[f"n_{column}"] = grouped[column].sum().astype(int)
    counts.reset_index().to_csv(output_path, sep="\t", index=False)


def _as_frozenset(block: Mapping[str, Any], key: str) -> frozenset[str]:
    raw = block.get(key, [])
    if raw is None:
        raw = []
    if not isinstance(raw, list):
        raise ValueError(f"{H10_CONFIG_KEY}.{key} must be a list")
    return frozenset(str(value) for value in raw)


def _parse_sample_level_rules(raw: Any) -> dict[str, SampleLevelRule]:
    if raw is None:
        raw = {}
    if not isinstance(raw, Mapping):
        raise ValueError(f"{H10_CONFIG_KEY}.sample_level_rules must be a mapping")

    rules: dict[str, SampleLevelRule] = {}
    for rule_id, rule_raw in raw.items():
        if not isinstance(rule_raw, Mapping):
            raise ValueError(f"sample_level_rules[{rule_id!r}] must be a mapping")
        rule_key = str(rule_id)
        target = _required_str(rule_raw, "target", rule_key)
        if target not in SAMPLE_LEVEL_TARGETS:
            allowed = ", ".join(sorted(SAMPLE_LEVEL_TARGETS))
            raise ValueError(
                f"sample_level_rules[{rule_key!r}].target must be one of {allowed}"
            )
        positive_columns = _parse_positive_columns(
            rule_raw.get("positive_columns"), rule_key
        )
        rules[rule_key] = SampleLevelRule(
            rule_id=rule_key,
            study_id=_required_str(rule_raw, "study_id", rule_key),
            target=target,
            clinical_sample_file=str(
                rule_raw.get("clinical_sample_file", "data_clinical_sample.txt")
            ),
            sample_id_column=str(rule_raw.get("sample_id_column", "SAMPLE_ID")),
            positive_columns=positive_columns,
        )
    return rules


def _parse_positive_columns(raw: Any, rule_id: str) -> dict[str, frozenset[str]]:
    if not isinstance(raw, Mapping) or not raw:
        raise ValueError(
            f"sample_level_rules[{rule_id!r}].positive_columns must be a non-empty mapping"
        )
    parsed: dict[str, frozenset[str]] = {}
    for column, values in raw.items():
        if not isinstance(values, list) or not values:
            raise ValueError(
                f"sample_level_rules[{rule_id!r}].positive_columns[{column!r}] "
                "must be a non-empty list"
            )
        parsed[str(column)] = frozenset(str(value) for value in values)
    return parsed


def _required_str(rule_raw: Mapping[str, Any], key: str, rule_id: str) -> str:
    value = rule_raw.get(key)
    if value is None or str(value) == "":
        raise ValueError(f"sample_level_rules[{rule_id!r}].{key} is required")
    return str(value)


def _validate_treatment_config(cfg: TreatmentConfig) -> None:
    overlap = (
        cfg.mutagenic_treatment_signal_studies
        & cfg.positive_naive_or_pretreatment_studies
    )
    if overlap:
        raise ValueError(
            "studies cannot be both primary mutagenic and positive-naive: "
            f"{sorted(overlap)}"
        )
    pdx_overlap = (
        cfg.mutagenic_treatment_signal_studies
        & cfg.mutagenic_treatment_signal_sensitivity_only_studies
    )
    if pdx_overlap:
        raise ValueError(
            "studies cannot be both primary mutagenic and sensitivity-only: "
            f"{sorted(pdx_overlap)}"
        )
    for rule in cfg.sample_level_rules.values():
        if (
            rule.target == "mutagenic_treatment_signal"
            and rule.study_id in cfg.mutagenic_treatment_signal_sensitivity_only_studies
        ):
            raise ValueError(
                f"sample-level rule {rule.rule_id!r} targets primary mutagenic treatment "
                f"for sensitivity-only study {rule.study_id!r}"
            )


def _apply_study_level_labels(out: pd.DataFrame, cfg: TreatmentConfig) -> None:
    assignments = [
        (
            cfg.broad_treatment_exposed_studies,
            "treatment_exposed_broad",
            "study-level:broad",
            "broad_treatment_exposed_studies",
        ),
        (
            cfg.mutagenic_treatment_signal_studies,
            "mutagenic_treatment_signal",
            "study-level:mutagenic-primary",
            "mutagenic_treatment_signal_studies",
        ),
        (
            cfg.mutagenic_treatment_signal_sensitivity_only_studies,
            "mutagenic_treatment_signal_sensitivity_only",
            "sensitivity-only",
            "mutagenic_treatment_signal_sensitivity_only_studies",
        ),
        (
            cfg.positive_naive_or_pretreatment_studies,
            "positive_naive_or_pretreatment",
            "positive-naive",
            "positive_naive_or_pretreatment_studies",
        ),
        (
            cfg.unknown_treatment_metadata_studies,
            "treatment_metadata_unknown",
            "unknown",
            "unknown_treatment_metadata_studies",
        ),
    ]
    for studies, column, source, rule_id in assignments:
        mask = out["study_id"].isin(studies)
        out.loc[mask, column] = True
        _append_label_detail(out, mask, source, rule_id)


def _apply_sample_level_rule(
    out: pd.DataFrame, rule: SampleLevelRule, data_dir: Path
) -> None:
    clinical_path = data_dir / rule.study_id / rule.clinical_sample_file
    if not clinical_path.exists():
        raise FileNotFoundError(
            f"sample-level rule {rule.rule_id!r} missing {clinical_path}"
        )

    clinical = pd.read_csv(clinical_path, sep="\t", dtype=str, comment="#").fillna("")
    required = {rule.sample_id_column, *rule.positive_columns.keys()}
    _require_columns(clinical, required, f"clinical sample file for {rule.rule_id}")
    if clinical[rule.sample_id_column].duplicated().any():
        duplicates = sorted(
            clinical.loc[
                clinical[rule.sample_id_column].duplicated(keep=False),
                rule.sample_id_column,
            ].unique()
        )
        raise ValueError(
            f"sample-level rule {rule.rule_id!r} has duplicate raw SAMPLE_ID values: {duplicates}"
        )

    study_mask = out["study_id"] == rule.study_id
    canonical_ids = set(out.loc[study_mask, "sample_id"])
    raw_ids = set(clinical[rule.sample_id_column].astype(str))
    unmatched = sorted(raw_ids - canonical_ids)
    if unmatched:
        raise ValueError(
            f"sample-level rule {rule.rule_id!r} raw SAMPLE_ID values not present "
            f"in canonical samples_annotated: {unmatched[:10]}"
        )

    positive = pd.Series(False, index=clinical.index)
    for column, values in rule.positive_columns.items():
        positive |= clinical[column].astype(str).isin(values)

    positive_ids = set(clinical.loc[positive, rule.sample_id_column].astype(str))
    mask = study_mask & out["sample_id"].isin(positive_ids)
    out.loc[mask, rule.target] = True
    if rule.target in {
        "mutagenic_treatment_signal",
        "mutagenic_treatment_signal_sensitivity_only",
    }:
        out.loc[mask, "treatment_exposed_broad"] = True
    _append_label_detail(out, mask, "sample-level", rule.rule_id)


def _append_label_detail(
    out: pd.DataFrame,
    mask: pd.Series,
    source: str,
    rule_id: str,
) -> None:
    if not mask.any():
        return
    for column, value in (
        ("treatment_label_source", source),
        ("treatment_rule_id", rule_id),
    ):
        current = out.loc[mask, column].astype(str)
        out.loc[mask, column] = current.mask(current == "", value).mask(
            current != "", current + ";" + value
        )


def _require_columns(df: pd.DataFrame, required: set[str], label: str) -> None:
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"{label} missing required clinical columns: {missing}")


@click.command()
@click.option(
    "--config",
    "config_path",
    type=click.Path(path_type=Path, exists=True),
    required=True,
    help="Pipeline config containing h10_treatment_denominator.",
)
@click.option(
    "--samples-annotated",
    type=click.Path(path_type=Path, exists=True),
    required=True,
    help="Canonical metadata/samples_annotated.feather input.",
)
@click.option(
    "--data-dir",
    type=click.Path(path_type=Path, exists=True, file_okay=False),
    required=True,
    help="Raw cBioPortal data directory containing per-study clinical sample files.",
)
@click.option(
    "--output",
    "output_path",
    type=click.Path(path_type=Path),
    required=True,
    help="Output metadata/samples_treatment_exposure.feather path.",
)
@click.option(
    "--counts",
    "counts_path",
    type=click.Path(path_type=Path),
    required=True,
    help="Output TSV sidecar with per-study treatment label counts.",
)
def main(
    config_path: Path,
    samples_annotated: Path,
    data_dir: Path,
    output_path: Path,
    counts_path: Path,
) -> None:
    cfg = load_treatment_config(
        yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    )
    samples = pd.read_feather(samples_annotated)
    out = annotate_treatment_exposure(samples, cfg, data_dir=data_dir)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_feather(output_path)
    write_label_counts(out, counts_path)
    click.echo(
        f"Wrote H10 treatment exposure labels for {len(out)} samples "
        f"across {out['study_id'].nunique()} studies to {output_path}"
    )


if __name__ == "__main__":
    main()
