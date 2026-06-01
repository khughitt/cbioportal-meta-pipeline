# science:code
# status: workflow-owned
# science:end
"""Aggregate per-study H10 treatment-view frequencies into impact summaries."""

from pathlib import Path

import click
import pandas as pd


COHORT_VIEWS = (
    "all_samples",
    "no_detected_treatment_signal",
    "confirmed_naive_or_pretreatment",
    "broad_treatment_excluded",
    "mutagenic_treatment_excluded_primary",
    "mutagenic_treatment_excluded_with_pdx_sensitivity",
)

REQUIRED_COLUMNS = {
    "cancer_type",
    "symbol",
    "cohort_view",
    "num",
    "n_samples",
    "ratio",
    "n_samples_hypermutator_excluded",
    "num_hypermutator_excluded",
    "ratio_hypermutator_excluded",
}

KEY_COLUMNS = ["cancer_type", "symbol"]

MEAN_COLUMNS = {
    "all_samples": "mean_all_samples",
    "no_detected_treatment_signal": "mean_no_detected_treatment_signal",
    "confirmed_naive_or_pretreatment": "mean_confirmed_naive_or_pretreatment",
    "broad_treatment_excluded": "mean_broad_treatment_excluded",
    "mutagenic_treatment_excluded_primary": "mean_mutagenic_treatment_excluded_primary",
    "mutagenic_treatment_excluded_with_pdx_sensitivity": (
        "mean_mutagenic_treatment_excluded_with_pdx_sensitivity"
    ),
}

RANK_COLUMNS = {
    "all_samples": "rank_all_samples",
    "no_detected_treatment_signal": "rank_no_detected_treatment_signal",
    "confirmed_naive_or_pretreatment": "rank_confirmed_naive_or_pretreatment",
    "broad_treatment_excluded": "rank_broad_treatment_excluded",
    "mutagenic_treatment_excluded_primary": "rank_mutagenic_primary",
}

CONTRASTS = {
    "no_detected_contrast": {
        "view": "no_detected_treatment_signal",
        "delta": "delta_no_detected_contrast",
        "rank_delta": "rank_delta_no_detected_contrast",
        "power": "power_status_no_detected_contrast",
    },
    "confirmed_naive_contrast": {
        "view": "confirmed_naive_or_pretreatment",
        "delta": "delta_confirmed_naive_contrast",
        "rank_delta": "rank_delta_confirmed_naive_contrast",
        "power": "power_status_confirmed_naive_contrast",
    },
    "broad": {
        "view": "broad_treatment_excluded",
        "delta": "delta_broad",
        "rank_delta": "rank_delta_broad",
        "power": "power_status_broad",
    },
    "mutagenic_primary": {
        "view": "mutagenic_treatment_excluded_primary",
        "delta": "delta_mutagenic_primary",
        "rank_delta": "rank_delta_mutagenic_primary",
        "power": "power_status_mutagenic_primary",
    },
}


def compute_h10_treatment_impact_table(
    per_study_frames: list[tuple[str, pd.DataFrame]],
) -> pd.DataFrame:
    """Build a gene-cancer treatment impact summary from per-study H10 view tables."""
    combined = _combine_per_study_frames(per_study_frames)
    if combined.empty:
        return _empty_output()

    _validate_complete_view_grid(combined)
    _validate_denominator_nesting(combined)

    view_stats = _aggregate_view_stats(combined)
    out = _wide_summary(view_stats)
    out = _add_deltas(out)
    out = _add_ranks(out)
    out = _add_power_statuses(out)
    return out.loc[:, _output_columns()].sort_values(KEY_COLUMNS).reset_index(drop=True)


def make_count_audit_table(impact_table: pd.DataFrame) -> pd.DataFrame:
    """Return count/audit fields for the non-ratio H10 impact output."""
    count_prefixes = ("n_studies_", "n_samples_", "num_")
    count_cols = [
        column
        for column in impact_table.columns
        if column.startswith(count_prefixes) or column.startswith("power_status_")
    ]
    return impact_table.loc[:, [*KEY_COLUMNS, *count_cols]].copy()


def _combine_per_study_frames(
    per_study_frames: list[tuple[str, pd.DataFrame]],
) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for study_id, frame in per_study_frames:
        _require_columns(frame, REQUIRED_COLUMNS, f"H10 treatment views for {study_id}")
        if frame.empty:
            continue
        out = frame.copy()
        out["study_id"] = str(study_id)
        duplicates = out.duplicated(
            ["study_id", "cancer_type", "symbol", "cohort_view"]
        )
        if duplicates.any():
            dup_rows = out.loc[
                duplicates, ["study_id", "cancer_type", "symbol", "cohort_view"]
            ].head(5)
            raise ValueError(
                f"duplicate H10 treatment view rows: {dup_rows.to_dict('records')}"
            )
        frames.append(out)
    if not frames:
        return pd.DataFrame(columns=[*REQUIRED_COLUMNS, "study_id"])
    combined = pd.concat(frames, ignore_index=True)
    unexpected = sorted(set(combined["cohort_view"]) - set(COHORT_VIEWS))
    if unexpected:
        raise ValueError(f"unexpected H10 treatment cohort_view values: {unexpected}")
    return combined


def _validate_complete_view_grid(combined: pd.DataFrame) -> None:
    expected = set(COHORT_VIEWS)
    missing_examples: list[dict[str, object]] = []
    for keys, frame in combined.groupby(["study_id", *KEY_COLUMNS], observed=True):
        missing = expected - set(frame["cohort_view"])
        if missing:
            study_id, cancer_type, symbol = keys
            missing_examples.append(
                {
                    "study_id": study_id,
                    "cancer_type": cancer_type,
                    "symbol": symbol,
                    "missing_views": sorted(missing),
                }
            )
        if len(missing_examples) >= 5:
            break
    if missing_examples:
        raise ValueError(f"incomplete H10 treatment view grid: {missing_examples}")


def _validate_denominator_nesting(combined: pd.DataFrame) -> None:
    counts = combined.pivot(
        index=["study_id", *KEY_COLUMNS],
        columns="cohort_view",
        values=["n_samples", "num"],
    )
    for metric in ("n_samples", "num"):
        all_values = counts[(metric, "all_samples")]
        for view in COHORT_VIEWS:
            if view == "all_samples":
                continue
            invalid = counts[(metric, view)] > all_values
            if invalid.any():
                bad_key = invalid[invalid].index[0]
                raise ValueError(
                    f"{view} has {metric} greater than all_samples for {bad_key}"
                )


def _aggregate_view_stats(combined: pd.DataFrame) -> pd.DataFrame:
    grouped = combined.groupby([*KEY_COLUMNS, "cohort_view"], observed=True)
    return grouped.agg(
        mean_ratio=("ratio", "mean"),
        n_studies=("n_samples", lambda values: int((values > 0).sum())),
        n_samples=("n_samples", "sum"),
        num=("num", "sum"),
    ).reset_index()


def _wide_summary(view_stats: pd.DataFrame) -> pd.DataFrame:
    base = (
        view_stats.loc[view_stats["cohort_view"] == "all_samples", KEY_COLUMNS]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    out = base.copy()
    for metric, prefix in (
        ("mean_ratio", "mean"),
        ("n_studies", "n_studies"),
        ("n_samples", "n_samples"),
        ("num", "num"),
    ):
        wide = view_stats.pivot(index=KEY_COLUMNS, columns="cohort_view", values=metric)
        for view in COHORT_VIEWS:
            target = (
                MEAN_COLUMNS[view] if metric == "mean_ratio" else f"{prefix}_{view}"
            )
            values = wide[view] if view in wide.columns else pd.Series(dtype=float)
            out = out.merge(
                values.rename(target).reset_index(),
                on=KEY_COLUMNS,
                how="left",
            )
            if metric != "mean_ratio":
                out[target] = out[target].fillna(0).astype(int)
    return out


def _add_deltas(out: pd.DataFrame) -> pd.DataFrame:
    for contrast_name, contrast in CONTRASTS.items():
        view = contrast["view"]
        out[contrast["delta"]] = out["mean_all_samples"] - out[MEAN_COLUMNS[view]]
        out[f"n_samples_removed_{contrast_name}"] = (
            out["n_samples_all_samples"] - out[f"n_samples_{view}"]
        )
        out[f"num_removed_{contrast_name}"] = (
            out["num_all_samples"] - out[f"num_{view}"]
        )
    return out


def _add_ranks(out: pd.DataFrame) -> pd.DataFrame:
    for view, rank_column in RANK_COLUMNS.items():
        mean_column = MEAN_COLUMNS[view]
        out[rank_column] = out.groupby("cancer_type", observed=True)[mean_column].rank(
            ascending=False,
            method="min",
        )
    for contrast in CONTRASTS.values():
        view = contrast["view"]
        rank_column = RANK_COLUMNS[view]
        out[contrast["rank_delta"]] = out["rank_all_samples"] - out[rank_column]
    return out


def _add_power_statuses(out: pd.DataFrame) -> pd.DataFrame:
    for contrast_name, contrast in CONTRASTS.items():
        view = contrast["view"]
        removed_column = f"n_samples_removed_{contrast_name}"
        view_samples_column = f"n_samples_{view}"
        view_studies_column = f"n_studies_{view}"
        out[contrast["power"]] = [
            _power_status(
                removed_samples=removed_samples,
                comparator_samples=comparator_samples,
                comparator_studies=comparator_studies,
            )
            for removed_samples, comparator_samples, comparator_studies in zip(
                out[removed_column],
                out[view_samples_column],
                out[view_studies_column],
                strict=True,
            )
        ]
    return out


def _power_status(
    *,
    removed_samples: int,
    comparator_samples: int,
    comparator_studies: int,
) -> str:
    if comparator_samples == 0 or removed_samples == 0:
        return "no_contrast"
    if comparator_studies < 2:
        return "underpowered_non_arbitrating"
    return "interpretable"


def _output_columns() -> list[str]:
    columns = [
        *KEY_COLUMNS,
        *MEAN_COLUMNS.values(),
        "delta_no_detected_contrast",
        "delta_confirmed_naive_contrast",
        "delta_broad",
        "delta_mutagenic_primary",
        "rank_all_samples",
        "rank_no_detected_treatment_signal",
        "rank_confirmed_naive_or_pretreatment",
        "rank_broad_treatment_excluded",
        "rank_mutagenic_primary",
        "rank_delta_no_detected_contrast",
        "rank_delta_confirmed_naive_contrast",
        "rank_delta_broad",
        "rank_delta_mutagenic_primary",
        "power_status_no_detected_contrast",
        "power_status_confirmed_naive_contrast",
        "power_status_broad",
        "power_status_mutagenic_primary",
    ]
    for metric in ("n_studies", "n_samples", "num"):
        columns.extend(f"{metric}_{view}" for view in COHORT_VIEWS)
    for contrast_name in CONTRASTS:
        columns.append(f"n_samples_removed_{contrast_name}")
        columns.append(f"num_removed_{contrast_name}")
    return columns


def _empty_output() -> pd.DataFrame:
    return pd.DataFrame(columns=_output_columns())


def _require_columns(df: pd.DataFrame, required: set[str], label: str) -> None:
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"{label} missing required columns: {missing}")


def _study_id_from_path(path: str | Path) -> str:
    p = Path(path)
    return p.parent.parent.parent.name


def _run_via_snakemake() -> None:
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821
    frames = [
        (_study_id_from_path(path), pd.read_feather(path))
        for path in list(snek.input.per_study)
    ]
    impact = compute_h10_treatment_impact_table(frames)
    count_audit = make_count_audit_table(impact)
    count_audit.to_feather(snek.output.impact)
    impact.to_feather(snek.output.ratio)


@click.command()
@click.option(
    "--per-study-table",
    "per_study_tables",
    type=click.Path(path_type=Path, exists=True),
    multiple=True,
    required=True,
)
@click.option("--study-id", "study_ids", multiple=True, required=True)
@click.option("--impact-output", type=click.Path(path_type=Path), required=True)
@click.option("--ratio-output", type=click.Path(path_type=Path), required=True)
def main(
    per_study_tables: tuple[Path, ...],
    study_ids: tuple[str, ...],
    impact_output: Path,
    ratio_output: Path,
) -> None:
    if len(per_study_tables) != len(study_ids):
        raise click.ClickException("--per-study-table and --study-id counts must match")
    frames = [
        (study_id, pd.read_feather(path))
        for study_id, path in zip(study_ids, per_study_tables, strict=True)
    ]
    impact = compute_h10_treatment_impact_table(frames)
    count_audit = make_count_audit_table(impact)
    impact_output.parent.mkdir(parents=True, exist_ok=True)
    ratio_output.parent.mkdir(parents=True, exist_ok=True)
    count_audit.to_feather(impact_output)
    impact.to_feather(ratio_output)
    click.echo(f"Wrote {len(impact)} H10 treatment impact rows to {ratio_output}")


if "snakemake" in globals():
    _run_via_snakemake()
elif __name__ == "__main__":
    main()
