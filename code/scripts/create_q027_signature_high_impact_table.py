# science:code
# status: workflow-owned
# science:end
"""Aggregate q027 signature-high frequency views into impact summaries."""

from pathlib import Path

import click
import pandas as pd


COHORT_VIEWS = (
    "all_samples",
    "signature_evaluable",
    "therapy_signature_high",
    "therapy_signature_high_excluded_primary",
    "therapy_signature_high_excluded_sensitivity_20",
    "therapy_signature_high_excluded_sensitivity_fraction_10",
    "signature_evaluable_high_excluded_primary",
    "signature_evaluable_high_excluded_sensitivity_20",
    "signature_evaluable_high_excluded_sensitivity_fraction_10",
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
    "signature_evaluable": "mean_signature_evaluable",
    "therapy_signature_high": "mean_therapy_signature_high",
    "therapy_signature_high_excluded_primary": "mean_therapy_signature_high_excluded_primary",
    "therapy_signature_high_excluded_sensitivity_20": "mean_therapy_signature_high_excluded_sensitivity_20",
    "therapy_signature_high_excluded_sensitivity_fraction_10": (
        "mean_therapy_signature_high_excluded_sensitivity_fraction_10"
    ),
    "signature_evaluable_high_excluded_primary": "mean_signature_evaluable_high_excluded_primary",
    "signature_evaluable_high_excluded_sensitivity_20": (
        "mean_signature_evaluable_high_excluded_sensitivity_20"
    ),
    "signature_evaluable_high_excluded_sensitivity_fraction_10": (
        "mean_signature_evaluable_high_excluded_sensitivity_fraction_10"
    ),
}

RANK_COLUMNS = {
    "all_samples": "rank_all_samples",
    "signature_evaluable": "rank_signature_evaluable",
    "therapy_signature_high_excluded_primary": "rank_signature_high_excluded_primary",
    "therapy_signature_high_excluded_sensitivity_20": "rank_signature_high_excluded_sensitivity_20",
    "therapy_signature_high_excluded_sensitivity_fraction_10": (
        "rank_signature_high_excluded_sensitivity_fraction_10"
    ),
    "signature_evaluable_high_excluded_primary": (
        "rank_signature_evaluable_high_excluded_primary"
    ),
    "signature_evaluable_high_excluded_sensitivity_20": (
        "rank_signature_evaluable_high_excluded_sensitivity_20"
    ),
    "signature_evaluable_high_excluded_sensitivity_fraction_10": (
        "rank_signature_evaluable_high_excluded_sensitivity_fraction_10"
    ),
}

CONTRASTS = {
    "signature_high_excluded_primary": {
        "baseline_view": "all_samples",
        "view": "therapy_signature_high_excluded_primary",
        "delta": "delta_signature_high_excluded_primary",
        "delta_hypermutator_excluded": "delta_signature_high_excluded_primary_hypermutator_excluded",
        "rank_delta": "rank_delta_signature_high_excluded_primary",
        "rank_delta_hypermutator_excluded": (
            "rank_delta_signature_high_excluded_primary_hypermutator_excluded"
        ),
        "power": "power_status_signature_high_excluded_primary",
        "power_hypermutator_excluded": (
            "power_status_signature_high_excluded_primary_hypermutator_excluded"
        ),
    },
    "signature_high_excluded_sensitivity_20": {
        "baseline_view": "all_samples",
        "view": "therapy_signature_high_excluded_sensitivity_20",
        "delta": "delta_signature_high_excluded_sensitivity_20",
        "delta_hypermutator_excluded": "delta_signature_high_excluded_sensitivity_20_hypermutator_excluded",
        "rank_delta": "rank_delta_signature_high_excluded_sensitivity_20",
        "rank_delta_hypermutator_excluded": (
            "rank_delta_signature_high_excluded_sensitivity_20_hypermutator_excluded"
        ),
        "power": "power_status_signature_high_excluded_sensitivity_20",
        "power_hypermutator_excluded": (
            "power_status_signature_high_excluded_sensitivity_20_hypermutator_excluded"
        ),
    },
    "signature_high_excluded_sensitivity_fraction_10": {
        "baseline_view": "all_samples",
        "view": "therapy_signature_high_excluded_sensitivity_fraction_10",
        "delta": "delta_signature_high_excluded_sensitivity_fraction_10",
        "delta_hypermutator_excluded": (
            "delta_signature_high_excluded_sensitivity_fraction_10_hypermutator_excluded"
        ),
        "rank_delta": "rank_delta_signature_high_excluded_sensitivity_fraction_10",
        "rank_delta_hypermutator_excluded": (
            "rank_delta_signature_high_excluded_sensitivity_fraction_10_hypermutator_excluded"
        ),
        "power": "power_status_signature_high_excluded_sensitivity_fraction_10",
        "power_hypermutator_excluded": (
            "power_status_signature_high_excluded_sensitivity_fraction_10_hypermutator_excluded"
        ),
    },
    "signature_evaluable_high_excluded_primary": {
        "baseline_view": "signature_evaluable",
        "view": "signature_evaluable_high_excluded_primary",
        "delta": "delta_signature_evaluable_high_excluded_primary",
        "delta_hypermutator_excluded": "delta_signature_evaluable_high_excluded_primary_hypermutator_excluded",
        "rank_delta": "rank_delta_signature_evaluable_high_excluded_primary",
        "rank_delta_hypermutator_excluded": (
            "rank_delta_signature_evaluable_high_excluded_primary_hypermutator_excluded"
        ),
        "power": "power_status_signature_evaluable_high_excluded_primary",
        "power_hypermutator_excluded": (
            "power_status_signature_evaluable_high_excluded_primary_hypermutator_excluded"
        ),
    },
    "signature_evaluable_high_excluded_sensitivity_20": {
        "baseline_view": "signature_evaluable",
        "view": "signature_evaluable_high_excluded_sensitivity_20",
        "delta": "delta_signature_evaluable_high_excluded_sensitivity_20",
        "delta_hypermutator_excluded": (
            "delta_signature_evaluable_high_excluded_sensitivity_20_hypermutator_excluded"
        ),
        "rank_delta": "rank_delta_signature_evaluable_high_excluded_sensitivity_20",
        "rank_delta_hypermutator_excluded": (
            "rank_delta_signature_evaluable_high_excluded_sensitivity_20_hypermutator_excluded"
        ),
        "power": "power_status_signature_evaluable_high_excluded_sensitivity_20",
        "power_hypermutator_excluded": (
            "power_status_signature_evaluable_high_excluded_sensitivity_20_hypermutator_excluded"
        ),
    },
    "signature_evaluable_high_excluded_sensitivity_fraction_10": {
        "baseline_view": "signature_evaluable",
        "view": "signature_evaluable_high_excluded_sensitivity_fraction_10",
        "delta": "delta_signature_evaluable_high_excluded_sensitivity_fraction_10",
        "delta_hypermutator_excluded": (
            "delta_signature_evaluable_high_excluded_sensitivity_fraction_10_hypermutator_excluded"
        ),
        "rank_delta": "rank_delta_signature_evaluable_high_excluded_sensitivity_fraction_10",
        "rank_delta_hypermutator_excluded": (
            "rank_delta_signature_evaluable_high_excluded_sensitivity_fraction_10_hypermutator_excluded"
        ),
        "power": "power_status_signature_evaluable_high_excluded_sensitivity_fraction_10",
        "power_hypermutator_excluded": (
            "power_status_signature_evaluable_high_excluded_sensitivity_fraction_10_hypermutator_excluded"
        ),
    },
}

HYPERMUTATOR_MEAN_COLUMNS = {
    view: f"{mean_column}_hypermutator_excluded"
    for view, mean_column in MEAN_COLUMNS.items()
}

HYPERMUTATOR_RANK_COLUMNS = {
    view: f"{rank_column}_hypermutator_excluded"
    for view, rank_column in RANK_COLUMNS.items()
}


def compute_q027_signature_high_impact_table(
    per_study_frames: list[tuple[str, pd.DataFrame]],
) -> pd.DataFrame:
    """Build a q027 gene-cancer signature-high impact summary."""
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
        _require_columns(
            frame, REQUIRED_COLUMNS, f"q027 signature-high views for {study_id}"
        )
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
                f"duplicate q027 signature-high view rows: {dup_rows.to_dict('records')}"
            )
        frames.append(out)
    if not frames:
        return pd.DataFrame(columns=[*REQUIRED_COLUMNS, "study_id"])
    combined = pd.concat(frames, ignore_index=True)
    unexpected = sorted(set(combined["cohort_view"]) - set(COHORT_VIEWS))
    if unexpected:
        raise ValueError(f"unexpected q027 cohort_view values: {unexpected}")
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
        raise ValueError(
            f"incomplete q027 signature-high view grid: {missing_examples}"
        )


def _validate_denominator_nesting(combined: pd.DataFrame) -> None:
    counts = combined.pivot(
        index=["study_id", *KEY_COLUMNS],
        columns="cohort_view",
        values=["n_samples", "num"],
    )
    all_values = counts[("n_samples", "all_samples")]
    for view in COHORT_VIEWS:
        if view == "all_samples":
            continue
        invalid = counts[("n_samples", view)] > all_values
        if invalid.any():
            bad_key = invalid[invalid].index[0]
            raise ValueError(
                f"{view} has n_samples greater than all_samples for {bad_key}"
            )


def _aggregate_view_stats(combined: pd.DataFrame) -> pd.DataFrame:
    grouped = combined.groupby([*KEY_COLUMNS, "cohort_view"], observed=True)
    return grouped.agg(
        mean_ratio=("ratio", "mean"),
        mean_ratio_hypermutator_excluded=("ratio_hypermutator_excluded", "mean"),
        n_studies=("n_samples", lambda values: int((values > 0).sum())),
        n_studies_hypermutator_excluded=(
            "n_samples_hypermutator_excluded",
            lambda values: int((values > 0).sum()),
        ),
        n_samples=("n_samples", "sum"),
        n_samples_hypermutator_excluded=("n_samples_hypermutator_excluded", "sum"),
        num=("num", "sum"),
        num_hypermutator_excluded=("num_hypermutator_excluded", "sum"),
    ).reset_index()


def _wide_summary(view_stats: pd.DataFrame) -> pd.DataFrame:
    base = (
        view_stats.loc[view_stats["cohort_view"] == "all_samples", KEY_COLUMNS]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    out = base.copy()
    metric_targets = {
        "mean_ratio": lambda view: MEAN_COLUMNS[view],
        "mean_ratio_hypermutator_excluded": lambda view: HYPERMUTATOR_MEAN_COLUMNS[
            view
        ],
        "n_studies": lambda view: f"n_studies_{view}",
        "n_studies_hypermutator_excluded": (
            lambda view: f"n_studies_hypermutator_excluded_{view}"
        ),
        "n_samples": lambda view: f"n_samples_{view}",
        "n_samples_hypermutator_excluded": (
            lambda view: f"n_samples_hypermutator_excluded_{view}"
        ),
        "num": lambda view: f"num_{view}",
        "num_hypermutator_excluded": (lambda view: f"num_hypermutator_excluded_{view}"),
    }
    for metric, target_for_view in metric_targets.items():
        wide = view_stats.pivot(index=KEY_COLUMNS, columns="cohort_view", values=metric)
        for view in COHORT_VIEWS:
            target = target_for_view(view)
            values = wide[view] if view in wide.columns else pd.Series(dtype=float)
            out = out.merge(
                values.rename(target).reset_index(), on=KEY_COLUMNS, how="left"
            )
            if not metric.startswith("mean_ratio"):
                out[target] = out[target].fillna(0).astype(int)
    return out


def _add_deltas(out: pd.DataFrame) -> pd.DataFrame:
    additions: dict[str, pd.Series] = {}
    for contrast_name, contrast in CONTRASTS.items():
        baseline_view = contrast["baseline_view"]
        view = contrast["view"]
        additions[contrast["delta"]] = (
            out[MEAN_COLUMNS[baseline_view]] - out[MEAN_COLUMNS[view]]
        )
        additions[contrast["delta_hypermutator_excluded"]] = (
            out[HYPERMUTATOR_MEAN_COLUMNS[baseline_view]]
            - out[HYPERMUTATOR_MEAN_COLUMNS[view]]
        )
        additions[f"n_samples_removed_{contrast_name}"] = (
            out[f"n_samples_{baseline_view}"] - out[f"n_samples_{view}"]
        )
        additions[f"num_removed_{contrast_name}"] = (
            out[f"num_{baseline_view}"] - out[f"num_{view}"]
        )
        additions[f"n_samples_removed_{contrast_name}_hypermutator_excluded"] = (
            out[f"n_samples_hypermutator_excluded_{baseline_view}"]
            - out[f"n_samples_hypermutator_excluded_{view}"]
        )
        additions[f"num_removed_{contrast_name}_hypermutator_excluded"] = (
            out[f"num_hypermutator_excluded_{baseline_view}"]
            - out[f"num_hypermutator_excluded_{view}"]
        )
    return pd.concat([out, pd.DataFrame(additions, index=out.index)], axis=1)


def _add_ranks(out: pd.DataFrame) -> pd.DataFrame:
    rank_additions: dict[str, pd.Series] = {}
    for view, rank_column in RANK_COLUMNS.items():
        rank_additions[rank_column] = out.groupby("cancer_type", observed=True)[
            MEAN_COLUMNS[view]
        ].rank(
            ascending=False,
            method="min",
        )
    for view, rank_column in HYPERMUTATOR_RANK_COLUMNS.items():
        rank_additions[rank_column] = out.groupby("cancer_type", observed=True)[
            HYPERMUTATOR_MEAN_COLUMNS[view]
        ].rank(
            ascending=False,
            method="min",
        )
    out = pd.concat([out, pd.DataFrame(rank_additions, index=out.index)], axis=1)
    delta_additions: dict[str, pd.Series] = {}
    for contrast in CONTRASTS.values():
        baseline_view = contrast["baseline_view"]
        view = contrast["view"]
        delta_additions[contrast["rank_delta"]] = (
            out[RANK_COLUMNS[baseline_view]] - out[RANK_COLUMNS[view]]
        )
        delta_additions[contrast["rank_delta_hypermutator_excluded"]] = (
            out[HYPERMUTATOR_RANK_COLUMNS[baseline_view]]
            - out[HYPERMUTATOR_RANK_COLUMNS[view]]
        )
    return pd.concat([out, pd.DataFrame(delta_additions, index=out.index)], axis=1)


def _add_power_statuses(out: pd.DataFrame) -> pd.DataFrame:
    additions: dict[str, list[str]] = {}
    for contrast_name, contrast in CONTRASTS.items():
        view = contrast["view"]
        additions[contrast["power"]] = [
            _power_status(
                removed_samples=removed_samples,
                comparator_samples=comparator_samples,
                comparator_studies=comparator_studies,
            )
            for removed_samples, comparator_samples, comparator_studies in zip(
                out[f"n_samples_removed_{contrast_name}"],
                out[f"n_samples_{view}"],
                out[f"n_studies_{view}"],
            )
        ]
        additions[contrast["power_hypermutator_excluded"]] = [
            _power_status(
                removed_samples=removed_samples,
                comparator_samples=comparator_samples,
                comparator_studies=comparator_studies,
            )
            for removed_samples, comparator_samples, comparator_studies in zip(
                out[f"n_samples_removed_{contrast_name}_hypermutator_excluded"],
                out[f"n_samples_hypermutator_excluded_{view}"],
                out[f"n_studies_hypermutator_excluded_{view}"],
            )
        ]
    return pd.concat([out, pd.DataFrame(additions, index=out.index)], axis=1)


def _power_status(
    *, removed_samples: int, comparator_samples: int, comparator_studies: int
) -> str:
    if removed_samples == 0:
        return "no_contrast"
    if comparator_samples == 0:
        return "no_comparator"
    if comparator_studies < 2:
        return "underpowered_non_arbitrating"
    return "interpretable"


def _output_columns() -> list[str]:
    columns = [*KEY_COLUMNS]
    for view in COHORT_VIEWS:
        columns.append(MEAN_COLUMNS[view])
        columns.append(HYPERMUTATOR_MEAN_COLUMNS[view])
        columns.append(f"n_studies_{view}")
        columns.append(f"n_studies_hypermutator_excluded_{view}")
        columns.append(f"n_samples_{view}")
        columns.append(f"n_samples_hypermutator_excluded_{view}")
        columns.append(f"num_{view}")
        columns.append(f"num_hypermutator_excluded_{view}")
    for contrast in CONTRASTS.values():
        columns.extend(
            [
                contrast["delta"],
                contrast["delta_hypermutator_excluded"],
                contrast["rank_delta"],
                contrast["rank_delta_hypermutator_excluded"],
                contrast["power"],
                contrast["power_hypermutator_excluded"],
            ]
        )
    for contrast_name in CONTRASTS:
        columns.extend(
            [
                f"n_samples_removed_{contrast_name}",
                f"num_removed_{contrast_name}",
                f"n_samples_removed_{contrast_name}_hypermutator_excluded",
                f"num_removed_{contrast_name}_hypermutator_excluded",
            ]
        )
    columns.extend(RANK_COLUMNS.values())
    columns.extend(HYPERMUTATOR_RANK_COLUMNS.values())
    return columns


def _empty_output() -> pd.DataFrame:
    return pd.DataFrame(columns=_output_columns())


def _require_columns(frame: pd.DataFrame, required: set[str], label: str) -> None:
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"{label} missing required columns: {missing}")


def _run_via_snakemake() -> None:
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821
    frames = [
        (study_id, pd.read_feather(path))
        for study_id, path in zip(snek.params.study_ids, snek.input.per_study)
    ]
    impact = compute_q027_signature_high_impact_table(frames)
    Path(snek.output.impact).parent.mkdir(parents=True, exist_ok=True)
    make_count_audit_table(impact).to_feather(snek.output.impact)
    impact.to_feather(snek.output.ratio)


@click.command()
@click.option("--output-impact", type=click.Path(path_type=Path), required=True)
@click.option("--output-ratio", type=click.Path(path_type=Path), required=True)
@click.argument(
    "per_study_paths", nargs=-1, type=click.Path(path_type=Path, exists=True)
)
def main(
    output_impact: Path, output_ratio: Path, per_study_paths: tuple[Path, ...]
) -> None:
    frames = [
        (path.parent.parent.parent.parent.name, pd.read_feather(path))
        for path in per_study_paths
    ]
    impact = compute_q027_signature_high_impact_table(frames)
    output_impact.parent.mkdir(parents=True, exist_ok=True)
    make_count_audit_table(impact).to_feather(output_impact)
    impact.to_feather(output_ratio)
    click.echo(f"Wrote {len(impact)} q027 signature-high impact rows to {output_ratio}")


if "snakemake" in globals():
    _run_via_snakemake()
elif __name__ == "__main__":
    main()
