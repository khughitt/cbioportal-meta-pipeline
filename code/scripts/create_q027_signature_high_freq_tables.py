# science:code
# status: workflow-owned
# science:end
"""Create q027 therapy-signature-high per-study gene-cancer frequency views."""

from pathlib import Path

import click
import pandas as pd

from create_freq_tables import compute_freq_tables
from create_h10_treatment_freq_tables import (
    _build_view_for_keys,
    _canonical_all_samples_view,
    _ensure_study_id,
    _prepare_mutations,
    _prepare_samples,
    _validate_panel_coverage,
)


COHORT_VIEWS = (
    "all_samples",
    "signature_evaluable",
    "therapy_signature_high",
    "therapy_signature_high_excluded_primary",
    "therapy_signature_high_excluded_sensitivity_20",
    "therapy_signature_high_excluded_sensitivity_fraction_10",
)

SIGNATURE_LABEL_COLUMNS = (
    "passes_count_floor",
    "therapy_signature_high",
    "therapy_signature_high_sensitivity_20",
    "therapy_signature_high_sensitivity_fraction_10",
)

OUTPUT_COLUMNS = (
    "cancer_type",
    "symbol",
    "cohort_view",
    "num",
    "n_samples",
    "ratio",
    "n_samples_hypermutator_excluded",
    "num_hypermutator_excluded",
    "ratio_hypermutator_excluded",
)


def compute_q027_signature_high_freq_table(
    mutations: pd.DataFrame,
    samples: pd.DataFrame,
    signature_labels: pd.DataFrame,
    hypermutator_annotations: pd.DataFrame,
    panel_coverage: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Compute long q027 ``(cancer_type, symbol, cohort_view)`` frequency rows."""
    samples_meta = _prepare_samples(samples)
    labels = _prepare_signature_labels(signature_labels, samples_meta)
    hyper = _prepare_hypermutator_annotations(hypermutator_annotations, samples_meta)
    mut = _prepare_mutations(mutations)
    _validate_panel_coverage(samples_meta, panel_coverage)

    sample_hyper = hyper[["sample_id", "is_hypermutator"]]
    if "study_id" in hyper.columns and "study_id" in samples_meta.columns:
        sample_hyper = hyper[["study_id", "sample_id", "is_hypermutator"]]

    _, _, _, canonical_gene_cancer = compute_freq_tables(
        mut.rename(columns={"sample_id": "sample_id_tumor"}),
        samples_meta,
        sample_hyper,
        panel_coverage=panel_coverage,
    )
    all_samples = _canonical_all_samples_view(canonical_gene_cancer)
    base_keys = all_samples[["cancer_type", "symbol"]].drop_duplicates()

    join_keys = (
        ["study_id", "sample_id"]
        if "study_id" in samples_meta.columns and "study_id" in labels.columns
        else ["sample_id"]
    )
    samples_with_labels = (
        samples_meta.merge(labels, on=join_keys, how="inner")
        .merge(hyper, on=join_keys, how="inner")
        .copy()
    )
    view_frames = [all_samples]
    for cohort_view, mask in _cohort_masks(samples_with_labels).items():
        if cohort_view == "all_samples":
            continue
        view_frames.append(
            _build_view_for_keys(
                cohort_view=cohort_view,
                base_keys=base_keys,
                mut=mut,
                view_samples=samples_with_labels.loc[mask].copy(),
                panel_coverage=panel_coverage,
            )
        )

    out = pd.concat(view_frames, ignore_index=True)
    return (
        out.loc[:, OUTPUT_COLUMNS]
        .sort_values(["cancer_type", "symbol", "cohort_view"])
        .reset_index(drop=True)
    )


def _prepare_signature_labels(
    signature_labels: pd.DataFrame, samples_meta: pd.DataFrame
) -> pd.DataFrame:
    required = {"sample_id", *SIGNATURE_LABEL_COLUMNS}
    _require_columns(signature_labels, required, "samples_q027_signature_high")
    cols = ["sample_id", *SIGNATURE_LABEL_COLUMNS]
    if "study_id" in signature_labels.columns and "study_id" in samples_meta.columns:
        cols.insert(0, "study_id")
    out = signature_labels[cols].copy()
    out["sample_id"] = out["sample_id"].astype(str)
    if "study_id" in out.columns:
        out["study_id"] = out["study_id"].astype(str)
        out = out.loc[
            out["study_id"].isin(set(samples_meta["study_id"].astype(str)))
        ].copy()
        key = ["study_id", "sample_id"]
    else:
        key = ["sample_id"]
    _require_unique(out, key, "samples_q027_signature_high")
    _require_coverage(
        samples_meta=samples_meta,
        annotations=out,
        key=key,
        label="missing q027 signature labels",
    )
    for column in SIGNATURE_LABEL_COLUMNS:
        out[column] = out[column].fillna(False).astype(bool)
    return out


def _prepare_hypermutator_annotations(
    hypermutator_annotations: pd.DataFrame, samples_meta: pd.DataFrame
) -> pd.DataFrame:
    required = {"sample_id", "is_hypermutator"}
    _require_columns(hypermutator_annotations, required, "samples_annotated")
    cols = ["sample_id", "is_hypermutator"]
    if (
        "study_id" in hypermutator_annotations.columns
        and "study_id" in samples_meta.columns
    ):
        cols.insert(0, "study_id")
    out = hypermutator_annotations[cols].copy()
    out["sample_id"] = out["sample_id"].astype(str)
    if "study_id" in out.columns:
        out["study_id"] = out["study_id"].astype(str)
        out = out.loc[
            out["study_id"].isin(set(samples_meta["study_id"].astype(str)))
        ].copy()
        key = ["study_id", "sample_id"]
    else:
        key = ["sample_id"]
    _require_unique(out, key, "samples_annotated")
    _require_coverage(
        samples_meta=samples_meta,
        annotations=out,
        key=key,
        label="missing hypermutator annotations",
    )
    out["is_hypermutator"] = out["is_hypermutator"].fillna(False).astype(bool)
    return out


def _cohort_masks(samples_with_labels: pd.DataFrame) -> dict[str, pd.Series]:
    return {
        "all_samples": pd.Series(True, index=samples_with_labels.index),
        "signature_evaluable": samples_with_labels["passes_count_floor"],
        "therapy_signature_high": samples_with_labels["therapy_signature_high"],
        "therapy_signature_high_excluded_primary": ~samples_with_labels[
            "therapy_signature_high"
        ],
        "therapy_signature_high_excluded_sensitivity_20": ~samples_with_labels[
            "therapy_signature_high_sensitivity_20"
        ],
        "therapy_signature_high_excluded_sensitivity_fraction_10": ~samples_with_labels[
            "therapy_signature_high_sensitivity_fraction_10"
        ],
    }


def _require_unique(frame: pd.DataFrame, key: list[str], label: str) -> None:
    if frame.duplicated(key).any():
        duplicates = frame.loc[frame.duplicated(key, keep=False), key].head(5)
        raise ValueError(
            f"{label} must be unique on {key}; duplicates: {duplicates.to_dict('records')}"
        )


def _require_coverage(
    *,
    samples_meta: pd.DataFrame,
    annotations: pd.DataFrame,
    key: list[str],
    label: str,
) -> None:
    sample_keys = set(map(tuple, samples_meta[key].astype(str).to_numpy()))
    annotation_keys = set(map(tuple, annotations[key].astype(str).to_numpy()))
    missing = sorted(sample_keys - annotation_keys)
    if missing:
        raise ValueError(f"{label} for samples: {missing[:10]}")


def _require_columns(frame: pd.DataFrame, required: set[str], label: str) -> None:
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"{label} missing required columns: {missing}")


def _run_via_snakemake() -> None:
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821
    panel_coverage_path = getattr(snek.input, "panel_coverage", None)
    panel_coverage = (
        pd.read_feather(panel_coverage_path) if panel_coverage_path else None
    )
    out = compute_q027_signature_high_freq_table(
        pd.read_feather(snek.input.mutations),
        _ensure_study_id(pd.read_feather(snek.input.samples), snek.wildcards.id),
        pd.read_feather(snek.input.signature_labels),
        pd.read_feather(snek.input.hypermutator_annotations),
        panel_coverage=panel_coverage,
    )
    out.to_feather(snek.output[0])


@click.command()
@click.option(
    "--mutations", type=click.Path(path_type=Path, exists=True), required=True
)
@click.option("--samples", type=click.Path(path_type=Path, exists=True), required=True)
@click.option(
    "--signature-labels", type=click.Path(path_type=Path, exists=True), required=True
)
@click.option(
    "--hypermutator-annotations",
    type=click.Path(path_type=Path, exists=True),
    required=True,
)
@click.option("--output", "output_path", type=click.Path(path_type=Path), required=True)
@click.option(
    "--panel-coverage", type=click.Path(path_type=Path, exists=True), default=None
)
def main(
    mutations: Path,
    samples: Path,
    signature_labels: Path,
    hypermutator_annotations: Path,
    output_path: Path,
    panel_coverage: Path | None,
) -> None:
    panel_coverage_df = pd.read_feather(panel_coverage) if panel_coverage else None
    out = compute_q027_signature_high_freq_table(
        pd.read_feather(mutations),
        pd.read_feather(samples),
        pd.read_feather(signature_labels),
        pd.read_feather(hypermutator_annotations),
        panel_coverage=panel_coverage_df,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_feather(output_path)
    click.echo(f"Wrote {len(out)} q027 signature-high frequency rows to {output_path}")


if "snakemake" in globals():
    _run_via_snakemake()
elif __name__ == "__main__":
    main()
