# science:code
# status: workflow-owned
# science:end
"""Annotate q027 therapy-signature-high samples from per-sample SBS exposures."""

from pathlib import Path
from typing import Any, Mapping

import click
import pandas as pd
import yaml


THERAPY_SIGNATURES = ("SBS11", "SBS31", "SBS35", "SBS87")
PRIMARY_EXPOSURE_THRESHOLD = 50.0
SENSITIVITY_EXPOSURE_THRESHOLD = 20.0
SENSITIVITY_FRACTION_THRESHOLD = 0.10


def annotate_q027_signature_high(
    assignments: pd.DataFrame,
    *,
    target_signatures_by_study: Mapping[str, tuple[str, ...]],
    primary_exposure_threshold: float = PRIMARY_EXPOSURE_THRESHOLD,
    sensitivity_exposure_threshold: float = SENSITIVITY_EXPOSURE_THRESHOLD,
    sensitivity_fraction_threshold: float = SENSITIVITY_FRACTION_THRESHOLD,
) -> pd.DataFrame:
    """Return one q027 signature-high label row per per-sample assignment."""
    required = {
        "study_id",
        "cancer_type",
        "sample_name",
        "signature",
        "exposure",
        "total_sbs_count",
        "count_floor",
        "passes_count_floor",
    }
    _require_columns(assignments, required, "restricted_assignment_per_sample")
    if assignments.empty:
        return pd.DataFrame(columns=_output_columns())

    assignments = assignments.copy()
    assignments["study_id"] = assignments["study_id"].astype(str)
    assignments["sample_id"] = assignments["sample_name"].astype(str)
    _validate_target_mapping(assignments, target_signatures_by_study)

    base = (
        assignments[
            [
                "study_id",
                "sample_id",
                "cancer_type",
                "total_sbs_count",
                "count_floor",
                "passes_count_floor",
            ]
        ]
        .drop_duplicates(["study_id", "sample_id"])
        .copy()
    )
    exposures = (
        assignments.pivot_table(
            index=["study_id", "sample_id"],
            columns="signature",
            values="exposure",
            aggfunc="sum",
            fill_value=0.0,
        )
        .reset_index()
        .rename_axis(None, axis=1)
    )
    out = base.merge(
        exposures, on=["study_id", "sample_id"], how="left", validate="one_to_one"
    )
    for signature in THERAPY_SIGNATURES:
        if signature not in out.columns:
            out[signature] = 0.0
        out[f"{signature}_exposure"] = out[signature].astype(float)
        out[f"{signature}_fraction"] = _safe_fraction(
            out[f"{signature}_exposure"], out["total_sbs_count"]
        )

    out["therapy_signature_exposure"] = [
        float(row[list(target_signatures_by_study[row["study_id"]])].sum())
        for _, row in out.iterrows()
    ]
    out["therapy_signature_fraction"] = _safe_fraction(
        out["therapy_signature_exposure"], out["total_sbs_count"]
    )
    out["passes_count_floor"] = out["passes_count_floor"].fillna(False).astype(bool)
    out["therapy_signature_unevaluable"] = ~out["passes_count_floor"]
    out["therapy_signature_high"] = out["passes_count_floor"] & (
        out["therapy_signature_exposure"] >= primary_exposure_threshold
    )
    out["therapy_signature_high_sensitivity_20"] = out["passes_count_floor"] & (
        out["therapy_signature_exposure"] >= sensitivity_exposure_threshold
    )
    out["therapy_signature_high_sensitivity_fraction_10"] = out[
        "passes_count_floor"
    ] & (out["therapy_signature_fraction"] >= sensitivity_fraction_threshold)
    out["therapy_signature_high_sensitivity_any"] = out["passes_count_floor"] & (
        out["therapy_signature_exposure"] > 0
    )
    out["therapy_signature_label_reason"] = [
        _label_reason(
            passes_count_floor=passes,
            primary_high=primary,
            therapy_signature_exposure=exposure,
        )
        for passes, primary, exposure in zip(
            out["passes_count_floor"],
            out["therapy_signature_high"],
            out["therapy_signature_exposure"],
        )
    ]
    out["q027_target_signatures"] = [
        "|".join(target_signatures_by_study[study_id]) for study_id in out["study_id"]
    ]
    out = out.drop(
        columns=[
            signature for signature in THERAPY_SIGNATURES if signature in out.columns
        ]
    )
    return (
        out.loc[:, _output_columns()]
        .sort_values(["study_id", "sample_id"])
        .reset_index(drop=True)
    )


def load_target_signatures(config: Mapping[str, Any]) -> dict[str, tuple[str, ...]]:
    raw = config.get("q027_therapy_signature_targets")
    if not isinstance(raw, Mapping) or not raw:
        raise ValueError("config must define q027_therapy_signature_targets")
    out: dict[str, tuple[str, ...]] = {}
    for study_id, value in raw.items():
        if not isinstance(value, Mapping):
            raise ValueError(
                f"q027_therapy_signature_targets[{study_id!r}] must be a mapping"
            )
        signatures = value.get("target_signatures")
        if not isinstance(signatures, list) or not signatures:
            raise ValueError(
                f"q027_therapy_signature_targets[{study_id!r}].target_signatures must be a non-empty list"
            )
        unknown = sorted(set(signatures) - set(THERAPY_SIGNATURES))
        if unknown:
            raise ValueError(
                f"Unsupported q027 therapy signatures for {study_id}: {unknown}"
            )
        out[str(study_id)] = tuple(str(signature) for signature in signatures)
    return out


@click.command()
@click.option(
    "--config",
    "config_path",
    type=click.Path(path_type=Path, exists=True),
    required=True,
)
@click.option("--output", "output_path", type=click.Path(path_type=Path), required=True)
@click.argument(
    "assignment_paths", nargs=-1, type=click.Path(path_type=Path, exists=True)
)
def main(
    config_path: Path, output_path: Path, assignment_paths: tuple[Path, ...]
) -> None:
    config = yaml.safe_load(config_path.read_text())
    _write_annotations(
        config=config, assignment_paths=list(assignment_paths), output_path=output_path
    )


def _main_snakemake() -> None:
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821
    assignment_paths = [Path(path) for path in snek.input["assignments"]]
    _write_annotations(
        config=snek.config,
        assignment_paths=assignment_paths,
        output_path=Path(snek.output[0]),
    )


def _write_annotations(
    *,
    config: Mapping[str, Any],
    assignment_paths: list[Path],
    output_path: Path,
) -> None:
    if not assignment_paths:
        raise ValueError("At least one per-sample assignment path is required")
    frames = [pd.read_feather(path) for path in assignment_paths]
    assignments = pd.concat(frames, ignore_index=True)
    out = annotate_q027_signature_high(
        assignments, target_signatures_by_study=load_target_signatures(config)
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_feather(output_path)


def _label_reason(
    *,
    passes_count_floor: bool,
    primary_high: bool,
    therapy_signature_exposure: float,
) -> str:
    if not passes_count_floor:
        return "unevaluable_below_count_floor"
    if primary_high:
        return "primary_exposure_ge_50"
    if therapy_signature_exposure > 0:
        return "below_primary_threshold"
    return "no_target_signature_exposure"


def _validate_target_mapping(
    assignments: pd.DataFrame,
    target_signatures_by_study: Mapping[str, tuple[str, ...]],
) -> None:
    missing = sorted(
        set(assignments["study_id"].astype(str)) - set(target_signatures_by_study)
    )
    if missing:
        raise ValueError(f"Missing q027 target signatures for studies: {missing}")
    assignment_signatures = set(assignments["signature"].astype(str))
    for study_id, signatures in target_signatures_by_study.items():
        absent = sorted(set(signatures) - assignment_signatures)
        if absent:
            raise ValueError(
                f"Assignment table for {study_id} is missing target signatures: {absent}"
            )


def _safe_fraction(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    denominator = denominator.astype(float)
    return numerator.astype(float).where(denominator > 0, 0.0) / denominator.where(
        denominator > 0, 1.0
    )


def _output_columns() -> list[str]:
    return [
        "study_id",
        "sample_id",
        "cancer_type",
        "passes_count_floor",
        "therapy_signature_unevaluable",
        "total_sbs_count",
        "count_floor",
        "therapy_signature_exposure",
        "therapy_signature_fraction",
        "SBS11_exposure",
        "SBS11_fraction",
        "SBS31_exposure",
        "SBS31_fraction",
        "SBS35_exposure",
        "SBS35_fraction",
        "SBS87_exposure",
        "SBS87_fraction",
        "therapy_signature_high",
        "therapy_signature_high_sensitivity_20",
        "therapy_signature_high_sensitivity_fraction_10",
        "therapy_signature_high_sensitivity_any",
        "therapy_signature_label_reason",
        "q027_target_signatures",
    ]


def _require_columns(frame: pd.DataFrame, required: set[str], name: str) -> None:
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"{name} missing required columns: {sorted(missing)}")


if "snakemake" in globals():
    _main_snakemake()
elif __name__ == "__main__":
    main()
