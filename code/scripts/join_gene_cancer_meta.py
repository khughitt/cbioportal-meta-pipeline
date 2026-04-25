"""Join pooled t077 meta-analysis outputs onto the canonical ratio table."""

from pathlib import Path

import pandas as pd


KEY_COLUMNS = ["cancer_type", "symbol"]
ANALYSIS_VIEWS = ["inclusive", "exclusive"]
META_COLUMNS = [
    "pooled_logit",
    "pooled_rate",
    "pooled_ci_lo",
    "pooled_ci_hi",
    "tau2",
    "i2",
    "pi_lo",
    "pi_hi",
    "k_studies",
    "n_total",
    "y_total",
    "converged",
    "status",
]


def join_pooled_meta_annotations(
    ratio_annotated: pd.DataFrame,
    pooled_meta: pd.DataFrame,
) -> pd.DataFrame:
    """Return ``ratio_annotated`` with paired inclusive/exclusive pooled columns added."""
    _validate_ratio_annotated(ratio_annotated)
    _validate_pooled_meta(pooled_meta)

    wide = _pivot_pooled_meta(pooled_meta)
    return ratio_annotated.merge(wide, on=KEY_COLUMNS, how="left", sort=False, validate="one_to_one")


def _validate_ratio_annotated(ratio_annotated: pd.DataFrame) -> None:
    missing = [col for col in KEY_COLUMNS if col not in ratio_annotated.columns]
    if missing:
        raise ValueError(
            "Ratio annotated table is missing required columns: " + ", ".join(missing)
        )
    if ratio_annotated.duplicated(KEY_COLUMNS).any():
        raise ValueError("Ratio annotated table must be unique on (cancer_type, symbol).")


def _validate_pooled_meta(pooled_meta: pd.DataFrame) -> None:
    required = [*KEY_COLUMNS, "analysis_view", *META_COLUMNS]
    missing = [col for col in required if col not in pooled_meta.columns]
    if missing:
        raise ValueError("Pooled meta table is missing required columns: " + ", ".join(missing))

    duplicate_mask = pooled_meta.duplicated([*KEY_COLUMNS, "analysis_view"])
    if duplicate_mask.any():
        duplicates = pooled_meta.loc[duplicate_mask, [*KEY_COLUMNS, "analysis_view"]]
        first = duplicates.iloc[0]
        raise ValueError(
            "Duplicate pooled meta rows for "
            f"({first['cancer_type']}, {first['symbol']}, {first['analysis_view']})."
        )

    views = set(pooled_meta["analysis_view"].dropna().astype(str))
    unexpected = sorted(views.difference(ANALYSIS_VIEWS))
    if unexpected:
        raise ValueError(
            "Pooled meta table has unexpected analysis_view values: " + ", ".join(unexpected)
        )


def _pivot_pooled_meta(pooled_meta: pd.DataFrame) -> pd.DataFrame:
    if pooled_meta.empty:
        return pd.DataFrame(columns=[*KEY_COLUMNS, *_output_columns()])

    metric_frames: list[pd.DataFrame] = []
    for column in META_COLUMNS:
        metric = pooled_meta.pivot(
            index=KEY_COLUMNS,
            columns="analysis_view",
            values=column,
        ).reindex(columns=ANALYSIS_VIEWS)
        metric.columns = [f"{column}_{view}" for view in ANALYSIS_VIEWS]
        metric_frames.append(metric)

    wide = pd.concat(metric_frames, axis=1).reset_index()
    return wide[[*KEY_COLUMNS, *_output_columns()]]


def _output_columns() -> list[str]:
    return [f"{column}_{view}" for column in META_COLUMNS for view in ANALYSIS_VIEWS]


def _run_via_snakemake() -> None:
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821
    ratio_annotated = pd.read_feather(snek.input.ratio)
    pooled_meta = pd.read_feather(snek.input.pooled)
    out = join_pooled_meta_annotations(ratio_annotated, pooled_meta)
    Path(snek.output[0]).parent.mkdir(parents=True, exist_ok=True)
    out.to_feather(snek.output[0])


if "snakemake" in globals():
    _run_via_snakemake()
