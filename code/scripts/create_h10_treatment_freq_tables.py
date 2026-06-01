# science:code
# status: workflow-owned
# science:end
"""Create H10 treatment-aware per-study gene-cancer frequency views."""

import logging
from pathlib import Path

import click
import pandas as pd

from create_freq_tables import compute_freq_tables


logger = logging.getLogger("create_h10_treatment_freq_tables")

COHORT_VIEWS = (
    "all_samples",
    "no_detected_treatment_signal",
    "confirmed_naive_or_pretreatment",
    "broad_treatment_excluded",
    "mutagenic_treatment_excluded_primary",
    "mutagenic_treatment_excluded_with_pdx_sensitivity",
)

TREATMENT_FLAG_COLUMNS = (
    "treatment_exposed_broad",
    "mutagenic_treatment_signal",
    "mutagenic_treatment_signal_sensitivity_only",
    "positive_naive_or_pretreatment",
    "treatment_metadata_unknown",
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


def compute_h10_treatment_freq_table(
    mutations: pd.DataFrame,
    samples: pd.DataFrame,
    treatment_annotations: pd.DataFrame,
    panel_coverage: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Compute long H10 treatment-aware ``(cancer_type, symbol, cohort_view)`` rows."""
    samples_meta = _prepare_samples(samples)
    treatment = _prepare_treatment_annotations(treatment_annotations, samples_meta)
    mut = _prepare_mutations(mutations)

    _validate_panel_coverage(samples_meta, panel_coverage)

    _, _, _, canonical_gene_cancer = compute_freq_tables(
        mut.rename(columns={"sample_id": "sample_id_tumor"}),
        samples_meta,
        treatment[["sample_id", "is_hypermutator"]],
        panel_coverage=panel_coverage,
    )
    all_samples = _canonical_all_samples_view(canonical_gene_cancer)
    base_keys = all_samples[["cancer_type", "symbol"]].drop_duplicates()

    treatment_join_keys = (
        ["study_id", "sample_id"]
        if "study_id" in samples_meta.columns and "study_id" in treatment.columns
        else ["sample_id"]
    )
    samples_with_treatment = samples_meta.merge(
        treatment, on=treatment_join_keys, how="inner"
    )
    view_frames = [all_samples]
    for cohort_view, mask in _cohort_masks(samples_with_treatment).items():
        if cohort_view == "all_samples":
            continue
        view_samples = samples_with_treatment.loc[mask].copy()
        view_frames.append(
            _build_view_for_keys(
                cohort_view=cohort_view,
                base_keys=base_keys,
                mut=mut,
                view_samples=view_samples,
                panel_coverage=panel_coverage,
            )
        )

    if not view_frames:
        return pd.DataFrame(columns=OUTPUT_COLUMNS)
    out = pd.concat(view_frames, ignore_index=True)
    out = out.loc[:, OUTPUT_COLUMNS]
    return out.sort_values(["cancer_type", "symbol", "cohort_view"]).reset_index(
        drop=True
    )


def _prepare_samples(samples: pd.DataFrame) -> pd.DataFrame:
    required = {"sample_id", "cancer_type", "cancer_type_detailed"}
    _require_columns(samples, required, "samples")
    sample_cols = ["sample_id", "cancer_type", "cancer_type_detailed"]
    if "study_id" in samples.columns:
        sample_cols.insert(0, "study_id")
    if "panel_id" in samples.columns:
        sample_cols.append("panel_id")
    out = samples[sample_cols].copy()
    out["sample_id"] = out["sample_id"].astype(str)
    if "study_id" in out.columns:
        out["study_id"] = out["study_id"].astype(str)
    if out["sample_id"].duplicated().any():
        duplicates = sorted(
            out.loc[out["sample_id"].duplicated(keep=False), "sample_id"].unique()
        )
        raise ValueError(
            f"samples must be unique on sample_id; duplicates: {duplicates[:10]}"
        )
    return out


def _ensure_study_id(samples: pd.DataFrame, study_id: str) -> pd.DataFrame:
    out = samples.copy()
    if "study_id" not in out.columns:
        out.insert(0, "study_id", str(study_id))
    return out


def _prepare_treatment_annotations(
    treatment_annotations: pd.DataFrame, samples_meta: pd.DataFrame
) -> pd.DataFrame:
    required = {"sample_id", "is_hypermutator", *TREATMENT_FLAG_COLUMNS}
    _require_columns(treatment_annotations, required, "samples_treatment_exposure")
    treatment_cols = list(required)
    if (
        "study_id" in treatment_annotations.columns
        and "study_id" in samples_meta.columns
    ):
        treatment_cols.append("study_id")
    out = treatment_annotations[treatment_cols].copy()
    out["sample_id"] = out["sample_id"].astype(str)
    if "study_id" in out.columns:
        out["study_id"] = out["study_id"].astype(str)
        study_ids = set(samples_meta["study_id"].astype(str))
        out = out.loc[out["study_id"].isin(study_ids)].copy()
        uniqueness_key = ["study_id", "sample_id"]
    else:
        uniqueness_key = ["sample_id"]
    if out.duplicated(uniqueness_key).any():
        duplicates = sorted(
            out.loc[out.duplicated(uniqueness_key, keep=False), "sample_id"].unique()
        )
        raise ValueError(
            "samples_treatment_exposure must be unique on "
            f"{uniqueness_key}; duplicates: {duplicates[:10]}"
        )

    missing = sorted(set(samples_meta["sample_id"]) - set(out["sample_id"]))
    if missing:
        raise ValueError(
            f"samples_treatment_exposure missing treatment annotations for samples: {missing[:10]}"
        )

    for column in ("is_hypermutator", *TREATMENT_FLAG_COLUMNS):
        out[column] = out[column].fillna(False).astype(bool)
    return out


def _prepare_mutations(mutations: pd.DataFrame) -> pd.DataFrame:
    _require_columns(mutations, {"symbol", "sample_id_tumor"}, "mutations")
    out = (
        mutations[["symbol", "sample_id_tumor"]]
        .rename(columns={"sample_id_tumor": "sample_id"})
        .copy()
    )
    out["sample_id"] = out["sample_id"].astype(str)
    return out


def _validate_panel_coverage(
    samples_meta: pd.DataFrame, panel_coverage: pd.DataFrame | None
) -> None:
    if panel_coverage is None or "panel_id" not in samples_meta.columns:
        return
    _require_columns(panel_coverage, {"panel_id", "gene"}, "panel_coverage")
    panels_in_samples = set(samples_meta["panel_id"].dropna().unique())
    panels_in_coverage = set(panel_coverage["panel_id"].unique())
    missing = sorted(panels_in_samples - panels_in_coverage)
    if missing:
        raise ValueError(
            f"panel_coverage is missing entries for panel(s): {', '.join(missing)}"
        )


def _canonical_all_samples_view(canonical_gene_cancer: pd.DataFrame) -> pd.DataFrame:
    out = canonical_gene_cancer[
        [
            "cancer_type",
            "symbol",
            "num_inclusive",
            "n_samples_inclusive",
            "ratio_inclusive",
            "n_samples_exclusive",
            "num_exclusive",
            "ratio_exclusive",
        ]
    ].rename(
        columns={
            "num_inclusive": "num",
            "n_samples_inclusive": "n_samples",
            "ratio_inclusive": "ratio",
            "n_samples_exclusive": "n_samples_hypermutator_excluded",
            "num_exclusive": "num_hypermutator_excluded",
            "ratio_exclusive": "ratio_hypermutator_excluded",
        }
    )
    out.insert(2, "cohort_view", "all_samples")
    return out


def _cohort_masks(samples_with_treatment: pd.DataFrame) -> dict[str, pd.Series]:
    no_detected = ~samples_with_treatment[
        [
            "treatment_exposed_broad",
            "mutagenic_treatment_signal",
            "mutagenic_treatment_signal_sensitivity_only",
            "treatment_metadata_unknown",
        ]
    ].any(axis=1)
    return {
        "all_samples": pd.Series(True, index=samples_with_treatment.index),
        "no_detected_treatment_signal": no_detected,
        "confirmed_naive_or_pretreatment": samples_with_treatment[
            "positive_naive_or_pretreatment"
        ],
        "broad_treatment_excluded": ~samples_with_treatment["treatment_exposed_broad"],
        "mutagenic_treatment_excluded_primary": ~samples_with_treatment[
            "mutagenic_treatment_signal"
        ],
        "mutagenic_treatment_excluded_with_pdx_sensitivity": ~(
            samples_with_treatment["mutagenic_treatment_signal"]
            | samples_with_treatment["mutagenic_treatment_signal_sensitivity_only"]
        ),
    }


def _build_view_for_keys(
    cohort_view: str,
    base_keys: pd.DataFrame,
    mut: pd.DataFrame,
    view_samples: pd.DataFrame,
    panel_coverage: pd.DataFrame | None,
) -> pd.DataFrame:
    base = base_keys.copy()
    base["cohort_view"] = cohort_view

    if view_samples.empty:
        return _with_counts(base, {}, {}, {}, {})

    sample_ids = set(view_samples["sample_id"])
    mut_view = mut.loc[mut["sample_id"].isin(sample_ids)].merge(
        view_samples[["sample_id", "cancer_type", "is_hypermutator"]],
        on="sample_id",
        how="inner",
    )
    num = mut_view.groupby(["cancer_type", "symbol"], observed=True)[
        "sample_id"
    ].nunique()
    num_hypermutator_excluded = (
        mut_view.loc[~mut_view["is_hypermutator"]]
        .groupby(["cancer_type", "symbol"], observed=True)["sample_id"]
        .nunique()
    )
    n_samples, n_samples_hypermutator_excluded = _view_denominators(
        view_samples, panel_coverage
    )
    return _with_counts(
        base, num, n_samples, num_hypermutator_excluded, n_samples_hypermutator_excluded
    )


def _view_denominators(
    view_samples: pd.DataFrame,
    panel_coverage: pd.DataFrame | None,
) -> tuple[pd.Series, pd.Series]:
    use_panel_path = (
        panel_coverage is not None
        and "panel_id" in view_samples.columns
        and not view_samples["panel_id"].isna().all()
    )
    if use_panel_path:
        assert panel_coverage is not None
        callable_pairs = (
            panel_coverage[["panel_id", "gene"]]
            .drop_duplicates()
            .rename(columns={"gene": "symbol"})
        )
        panel_gene_samples = view_samples.merge(callable_pairs, on="panel_id")
        n_samples = panel_gene_samples.groupby(
            ["cancer_type", "symbol"], observed=True
        )["sample_id"].nunique()
        n_samples_hypermutator_excluded = (
            panel_gene_samples.loc[~panel_gene_samples["is_hypermutator"]]
            .groupby(["cancer_type", "symbol"], observed=True)["sample_id"]
            .nunique()
        )
        return n_samples, n_samples_hypermutator_excluded

    n_samples = view_samples.groupby("cancer_type", observed=True)[
        "sample_id"
    ].nunique()
    n_samples_hypermutator_excluded = (
        view_samples.loc[~view_samples["is_hypermutator"]]
        .groupby("cancer_type", observed=True)["sample_id"]
        .nunique()
    )
    return n_samples, n_samples_hypermutator_excluded


def _with_counts(
    base: pd.DataFrame,
    num: pd.Series | dict[object, int],
    n_samples: pd.Series | dict[object, int],
    num_hypermutator_excluded: pd.Series | dict[object, int],
    n_samples_hypermutator_excluded: pd.Series | dict[object, int],
) -> pd.DataFrame:
    key_index = pd.MultiIndex.from_frame(base[["cancer_type", "symbol"]])
    out = base.copy()
    if isinstance(n_samples, pd.Series) and isinstance(n_samples.index, pd.MultiIndex):
        out["n_samples"] = key_index.map(n_samples).fillna(0).astype(int)
        out["n_samples_hypermutator_excluded"] = (
            key_index.map(n_samples_hypermutator_excluded).fillna(0).astype(int)
        )
    else:
        out["n_samples"] = out["cancer_type"].map(n_samples).fillna(0).astype(int)
        out["n_samples_hypermutator_excluded"] = (
            out["cancer_type"]
            .map(n_samples_hypermutator_excluded)
            .fillna(0)
            .astype(int)
        )
    out["num"] = key_index.map(num).fillna(0).astype(int)
    out["num_hypermutator_excluded"] = (
        key_index.map(num_hypermutator_excluded).fillna(0).astype(int)
    )
    out["ratio"] = _safe_ratio(out["num"], out["n_samples"])
    out["ratio_hypermutator_excluded"] = _safe_ratio(
        out["num_hypermutator_excluded"], out["n_samples_hypermutator_excluded"]
    )
    return out


def _safe_ratio(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    return numerator.astype(float) / denominator.astype(float).replace(
        0.0, float("nan")
    )


def _require_columns(df: pd.DataFrame, required: set[str], label: str) -> None:
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"{label} missing required columns: {missing}")


def _run_via_snakemake() -> None:
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821
    mutations = pd.read_feather(snek.input.mutations)
    samples = _ensure_study_id(pd.read_feather(snek.input.samples), snek.wildcards.id)
    treatment_annotations = pd.read_feather(snek.input.treatment_annotations)

    panel_coverage_path = getattr(snek.input, "panel_coverage", None)
    panel_coverage = (
        pd.read_feather(panel_coverage_path) if panel_coverage_path else None
    )

    out = compute_h10_treatment_freq_table(
        mutations,
        samples,
        treatment_annotations,
        panel_coverage=panel_coverage,
    )
    out.to_feather(snek.output[0])


@click.command()
@click.option(
    "--mutations", type=click.Path(path_type=Path, exists=True), required=True
)
@click.option("--samples", type=click.Path(path_type=Path, exists=True), required=True)
@click.option(
    "--treatment-annotations",
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
    treatment_annotations: Path,
    output_path: Path,
    panel_coverage: Path | None,
) -> None:
    panel_coverage_df = pd.read_feather(panel_coverage) if panel_coverage else None
    out = compute_h10_treatment_freq_table(
        pd.read_feather(mutations),
        pd.read_feather(samples),
        pd.read_feather(treatment_annotations),
        panel_coverage=panel_coverage_df,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_feather(output_path)
    click.echo(f"Wrote {len(out)} H10 treatment frequency rows to {output_path}")


if "snakemake" in globals():
    _run_via_snakemake()
elif __name__ == "__main__":
    main()
