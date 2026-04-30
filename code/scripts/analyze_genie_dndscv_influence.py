"""Attribute GENIE-driven dNdScv ranking shifts from completed LOSO artifacts."""

from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import TypedDict

import click
import numpy as np
import pandas as pd

from analyze_dndscv_loso import rank_dndscv_genes

TESTED_STATUSES = {"tested_significant", "tested_not_significant"}
NON_TESTED_STATUSES = {"below_threshold", "failed_qc", "not_run", "missing"}
LABEL_PRESENCE_SUPPORT_CLASSES = {"full_only_tested", "holdout_only_tested"}
SIGNAL_SHIFT_SUPPORT_CLASSES = {"lost_significance", "gained_significance"}

RANKED_VALUE_COLUMNS = [
    "rank",
    "min_qglobal",
    "n_cancers_significant_q05",
    "n_cancers_significant_q01",
    "n_cancers_tested",
    "best_cancer_type",
]
PER_CANCER_REQUIRED_COLUMNS = {
    "symbol",
    "cancer_type",
    "dndscv_qglobal_cv",
    "dndscv_significant_q05",
    "dndscv_input_status",
    "dndscv_input_modality",
    "dndscv_panel_only",
    "dndscv_n_samples",
    "dndscv_n_variants",
    "dndscv_split_build",
    "dndscv_refdb",
}
PER_CANCER_PREFIX_COLUMNS = {
    "dndscv_qglobal_cv": "qglobal",
    "dndscv_significant_q05": "significant_q05",
    "dndscv_input_status": "input_status",
    "dndscv_input_modality": "input_modality",
    "dndscv_panel_only": "panel_only",
    "dndscv_n_samples": "n_samples",
    "dndscv_n_variants": "n_variants",
    "dndscv_split_build": "split_build",
    "dndscv_refdb": "refdb",
}
COHORT_META_REQUIRED_COLUMNS = {
    "cancer_type",
    "build",
    "slug",
    "n_samples",
    "n_variants",
    "modality",
    "panel_only",
    "below_threshold",
    "min_samples_threshold",
    "min_variants_threshold",
}
ALIGNED_COHORT_META_REQUIRED_COLUMNS = {
    "cancer_type",
    "build",
    "base_n_samples",
    "holdout_n_samples",
    "base_n_variants",
    "holdout_n_variants",
    "base_modality",
    "holdout_modality",
    "base_panel_only",
    "holdout_panel_only",
    "base_below_threshold",
    "holdout_below_threshold",
    "base_min_samples_threshold",
    "holdout_min_samples_threshold",
    "base_min_variants_threshold",
    "holdout_min_variants_threshold",
}
INFLUENCE_EVIDENCE_REQUIRED_COLUMNS = {
    "symbol",
    "cancer_type",
    "topk_status",
    "rank_delta",
    "base_significant_q05",
    "holdout_significant_q05",
    "support_class",
    "delta_neg_log10_q",
}


class ContrastResult(TypedDict):
    rank_delta: pd.DataFrame
    evidence: pd.DataFrame
    influence: pd.DataFrame
    counts: dict[str, int | float]
    base_pooled: pd.DataFrame
    holdout_pooled: pd.DataFrame
    base_per_cancer: pd.DataFrame
    holdout_per_cancer: pd.DataFrame
    cohort_meta: pd.DataFrame


class ThresholdMismatchError(ValueError):
    """Raised when full and holdout dNdScv threshold settings differ."""


def rank_pooled_dndscv(pooled: pd.DataFrame) -> pd.DataFrame:
    """Rank pooled dNdScv output using the published t173 ordering."""
    return rank_dndscv_genes(pooled)


def classify_topk_status(
    base_rank: int | None, holdout_rank: int | None, top_k: int
) -> str:
    """Classify whether a gene is lost, gained, stable, or outside the top-k set."""
    in_base_topk = base_rank is not None and base_rank <= top_k
    in_holdout_topk = holdout_rank is not None and holdout_rank <= top_k
    if in_base_topk and in_holdout_topk:
        return "stable"
    if in_base_topk:
        return "lost"
    if in_holdout_topk:
        return "gained"
    return "outside_top100"


def build_gene_rank_delta(
    base: pd.DataFrame,
    holdout: pd.DataFrame,
    *,
    top_k: int,
    diagnostic_top_n: int,
) -> pd.DataFrame:
    """Build one row per gene in the base/holdout diagnostic rank union."""
    base_ranked = _ranked_for_join(rank_pooled_dndscv(base), "base")
    holdout_ranked = _ranked_for_join(rank_pooled_dndscv(holdout), "holdout")
    symbols = _diagnostic_symbols(base_ranked, holdout_ranked, diagnostic_top_n)

    rows: list[dict[str, float | int | str | None]] = []
    base_by_symbol = base_ranked.set_index("symbol", drop=False)
    holdout_by_symbol = holdout_ranked.set_index("symbol", drop=False)
    for symbol in symbols:
        base_row = (
            base_by_symbol.loc[symbol] if symbol in base_by_symbol.index else None
        )
        holdout_row = (
            holdout_by_symbol.loc[symbol] if symbol in holdout_by_symbol.index else None
        )
        row: dict[str, float | int | str | None] = {"symbol": symbol}
        row.update(_prefixed_values(base_row, "base"))
        row.update(_prefixed_values(holdout_row, "holdout"))
        base_rank = _optional_int(row["base_rank"])
        holdout_rank = _optional_int(row["holdout_rank"])
        row["rank_delta"] = (
            holdout_rank - base_rank
            if base_rank is not None and holdout_rank is not None
            else None
        )
        row["topk_status"] = classify_topk_status(base_rank, holdout_rank, top_k)
        rows.append(row)

    return pd.DataFrame(rows)


def load_per_cancer_genes(root: Path) -> pd.DataFrame:
    """Load reconciled per-cancer dNdScv gene tables from a run root."""
    per_cancer_root = root
    if root.name != "per_cancer":
        per_cancer_root = root / "summary/mut/dndscv/per_cancer"
    paths = sorted(per_cancer_root.glob("*/genes.feather"))
    if not paths:
        raise FileNotFoundError(
            f"no per-cancer dNdScv genes.feather files found under {per_cancer_root}"
        )
    frames = [pd.read_feather(path) for path in paths]
    out = pd.concat(frames, ignore_index=True)
    _require_columns(out, PER_CANCER_REQUIRED_COLUMNS, "per-cancer dNdScv table")
    return out


def load_cohort_meta(root: Path) -> pd.DataFrame:
    """Load dNdScv cohort metadata from a run root."""
    meta_root = root
    if root.name != "dndscv_input":
        meta_root = root / "summary/mut/dndscv_input"
    paths = sorted(meta_root.glob("*/cohort_meta.feather"))
    if not paths:
        raise FileNotFoundError(
            f"no dNdScv cohort_meta.feather files found under {meta_root}"
        )
    frames = [pd.read_feather(path) for path in paths]
    out = pd.concat(frames, ignore_index=True)
    _require_columns(out, COHORT_META_REQUIRED_COLUMNS, "dNdScv cohort metadata")
    return out


def compare_gene_cancer_evidence(
    base: pd.DataFrame,
    holdout: pd.DataFrame,
    affected: pd.DataFrame,
    *,
    q_floor: float = 1e-300,
) -> pd.DataFrame:
    """Compare per-cancer dNdScv evidence for affected genes."""
    _require_columns(base, PER_CANCER_REQUIRED_COLUMNS, "base per-cancer dNdScv table")
    _require_columns(
        holdout, PER_CANCER_REQUIRED_COLUMNS, "holdout per-cancer dNdScv table"
    )
    _require_columns(
        affected, {"symbol", "topk_status", "rank_delta"}, "affected gene table"
    )

    affected_meta = affected[["symbol", "topk_status", "rank_delta"]].drop_duplicates(
        "symbol"
    )
    symbols = set(affected_meta["symbol"].dropna().astype(str))
    base_prepared = _prepare_per_cancer_for_merge(base, "base", symbols)
    holdout_prepared = _prepare_per_cancer_for_merge(holdout, "holdout", symbols)
    evidence = base_prepared.merge(
        holdout_prepared, on=["symbol", "cancer_type"], how="outer"
    )
    evidence = evidence.merge(affected_meta, on="symbol", how="inner")
    evidence["base_input_status"] = evidence["base_input_status"].fillna("missing")
    evidence["holdout_input_status"] = evidence["holdout_input_status"].fillna(
        "missing"
    )
    evidence["base_neg_log10_q"] = neg_log10_q(evidence["base_qglobal"], floor=q_floor)
    evidence["holdout_neg_log10_q"] = neg_log10_q(
        evidence["holdout_qglobal"], floor=q_floor
    )
    evidence["delta_neg_log10_q"] = (
        evidence["holdout_neg_log10_q"] - evidence["base_neg_log10_q"]
    )
    evidence["support_class"] = evidence.apply(_classify_support_row, axis=1)
    return evidence.reset_index(drop=True)


def neg_log10_q(q: pd.Series, *, floor: float = 1e-300) -> pd.Series:
    """Return floored -log10(q) values without infinities for q=0."""
    values = pd.to_numeric(q, errors="coerce").clip(lower=floor)
    return pd.Series(-np.log10(values), index=q.index)


def score_cancer_build_influence(
    evidence: pd.DataFrame,
    cohort_meta: pd.DataFrame,
    *,
    q_shift_threshold: float = 2.0,
) -> pd.DataFrame:
    """Aggregate gene-cancer evidence into transparent cancer/build influence scores."""
    _require_columns(
        evidence, INFLUENCE_EVIDENCE_REQUIRED_COLUMNS, "gene-cancer evidence"
    )
    _require_columns(
        cohort_meta, ALIGNED_COHORT_META_REQUIRED_COLUMNS, "aligned cohort metadata"
    )
    _assert_threshold_parity(cohort_meta)

    rows: list[dict[str, object]] = []
    for meta_row in cohort_meta.itertuples(index=False):
        cancer_type = str(meta_row.cancer_type)
        group = evidence.loc[evidence["cancer_type"].astype(str) == cancer_type]
        if group.empty:
            continue
        explanatory = group.loc[_explanatory_support_mask(group, q_shift_threshold)]
        support_classes = explanatory["support_class"].dropna().astype(str).tolist()
        delta_values = explanatory["delta_neg_log10_q"].tolist()
        threshold_transition = _threshold_transition(
            bool(meta_row.base_below_threshold),
            bool(meta_row.holdout_below_threshold),
            base_missing=bool(getattr(meta_row, "base_missing", False)),
            holdout_missing=bool(getattr(meta_row, "holdout_missing", False)),
        )
        rows.append(
            {
                "cancer_type": cancer_type,
                "build": str(meta_row.build),
                "n_affected_genes": int(explanatory["symbol"].nunique()),
                "n_lost_top100_supported_full": _count_lost_supported_full(explanatory),
                "n_lost_top100_lost_significance": int(
                    (
                        (explanatory["topk_status"] == "lost")
                        & (explanatory["support_class"] == "lost_significance")
                    ).sum()
                ),
                "n_gained_top100_supported_holdout": _count_gained_supported_holdout(
                    explanatory
                ),
                "sum_abs_rank_delta_supported": float(
                    pd.to_numeric(explanatory["rank_delta"], errors="coerce")
                    .abs()
                    .sum()
                ),
                "median_delta_neg_log10_q": float(
                    pd.to_numeric(
                        explanatory["delta_neg_log10_q"], errors="coerce"
                    ).median()
                ),
                "delta_n_samples": int(meta_row.base_n_samples)
                - int(meta_row.holdout_n_samples),
                "delta_n_variants": int(meta_row.base_n_variants)
                - int(meta_row.holdout_n_variants),
                "full_modality": meta_row.base_modality,
                "holdout_modality": meta_row.holdout_modality,
                "full_panel_only": bool(meta_row.base_panel_only),
                "holdout_panel_only": bool(meta_row.holdout_panel_only),
                "threshold_transition": threshold_transition,
                "mechanism_class": assign_mechanism_class(
                    support_classes,
                    delta_values,
                    q_shift_threshold=q_shift_threshold,
                    threshold_transition=threshold_transition,
                ),
            }
        )
    return (
        pd.DataFrame(rows)
        .sort_values(
            by=[
                "sum_abs_rank_delta_supported",
                "n_affected_genes",
                "cancer_type",
                "build",
            ],
            ascending=[False, False, True, True],
        )
        .reset_index(drop=True)
    )


def assign_mechanism_class(
    support_classes: Iterable[str],
    delta_neg_log10_q: Iterable[float | int | None],
    *,
    q_shift_threshold: float,
    threshold_transition: str = "tested_to_tested",
) -> str:
    """Assign the dominant mechanism label for an affected cancer/build group."""
    classes = set(support_classes)
    has_label_event = (
        bool(classes & LABEL_PRESENCE_SUPPORT_CLASSES)
        or threshold_transition != "tested_to_tested"
    )
    has_shift_event = bool(classes & SIGNAL_SHIFT_SUPPORT_CLASSES) or any(
        _is_meaningful_delta(delta, q_shift_threshold) for delta in delta_neg_log10_q
    )
    if has_label_event and has_shift_event:
        return "mixed"
    if has_label_event:
        return "genie_only_label"
    if has_shift_event:
        return "shared_label_shift"
    return "weak_or_unclear"


def align_cohort_meta(
    base_meta: pd.DataFrame, holdout_meta: pd.DataFrame
) -> pd.DataFrame:
    """Align full and holdout cohort metadata by cancer type and build."""
    _require_columns(base_meta, COHORT_META_REQUIRED_COLUMNS, "base cohort metadata")
    _require_columns(
        holdout_meta, COHORT_META_REQUIRED_COLUMNS, "holdout cohort metadata"
    )
    base = _prefix_cohort_meta(base_meta, "base")
    holdout = _prefix_cohort_meta(holdout_meta, "holdout")
    aligned = base.merge(holdout, on=["cancer_type", "build"], how="outer")
    aligned["base_missing"] = aligned["base_n_samples"].isna()
    aligned["holdout_missing"] = aligned["holdout_n_samples"].isna()
    for prefix in ("base", "holdout"):
        other = "holdout" if prefix == "base" else "base"
        aligned[f"{prefix}_n_samples"] = (
            aligned[f"{prefix}_n_samples"].fillna(0).astype(int)
        )
        aligned[f"{prefix}_n_variants"] = (
            aligned[f"{prefix}_n_variants"].fillna(0).astype(int)
        )
        aligned[f"{prefix}_modality"] = aligned[f"{prefix}_modality"].fillna("missing")
        aligned[f"{prefix}_panel_only"] = (
            aligned[f"{prefix}_panel_only"].fillna(False).astype(bool)
        )
        aligned[f"{prefix}_below_threshold"] = (
            aligned[f"{prefix}_below_threshold"].fillna(True).astype(bool)
        )
        for threshold in ("min_samples_threshold", "min_variants_threshold"):
            column = f"{prefix}_{threshold}"
            other_column = f"{other}_{threshold}"
            aligned[column] = aligned[column].fillna(aligned[other_column]).astype(int)
    return aligned.reset_index(drop=True)


def run_contrast(
    *,
    base_root: Path,
    holdout_root: Path,
    top_k: int,
    diagnostic_top_n: int,
    q_floor: float,
    q_shift_threshold: float,
) -> ContrastResult:
    """Run rank, evidence, and influence attribution for one contrast."""
    base_pooled = _load_pooled(base_root)
    holdout_pooled = _load_pooled(holdout_root)
    rank_delta = build_gene_rank_delta(
        base_pooled,
        holdout_pooled,
        top_k=top_k,
        diagnostic_top_n=diagnostic_top_n,
    )
    base_per_cancer = load_per_cancer_genes(base_root)
    holdout_per_cancer = load_per_cancer_genes(holdout_root)
    evidence = compare_gene_cancer_evidence(
        base_per_cancer,
        holdout_per_cancer,
        rank_delta,
        q_floor=q_floor,
    )
    cohort_meta = align_cohort_meta(
        load_cohort_meta(base_root), load_cohort_meta(holdout_root)
    )
    influence = score_cancer_build_influence(
        evidence, cohort_meta, q_shift_threshold=q_shift_threshold
    )
    counts: dict[str, int | float] = {
        "base_pooled_rows": int(len(base_pooled)),
        "holdout_pooled_rows": int(len(holdout_pooled)),
        "base_per_cancer_rows": int(len(base_per_cancer)),
        "holdout_per_cancer_rows": int(len(holdout_per_cancer)),
        "cohort_meta_rows": int(len(cohort_meta)),
        "cancer_labels": int(evidence["cancer_type"].nunique()),
        "build_strata": int(
            cohort_meta[["cancer_type", "build"]].drop_duplicates().shape[0]
        ),
        "diagnostic_genes": int(rank_delta["symbol"].nunique()),
    }
    return {
        "rank_delta": rank_delta,
        "evidence": evidence,
        "influence": influence,
        "counts": counts,
        "base_pooled": base_pooled,
        "holdout_pooled": holdout_pooled,
        "base_per_cancer": base_per_cancer,
        "holdout_per_cancer": holdout_per_cancer,
        "cohort_meta": cohort_meta,
    }


@click.command()
@click.option("--base-root", type=Path, required=True)
@click.option("--loo-root", type=Path, required=True)
@click.option("--holdout", required=True)
@click.option("--negative-control", multiple=True)
@click.option("--out-dir", type=Path, required=True)
@click.option("--top-k", type=int, default=100, show_default=True)
@click.option("--diagnostic-top-n", type=int, default=200, show_default=True)
@click.option("--q-floor", type=float, default=1e-300, show_default=True)
@click.option("--q-shift-threshold", type=float, default=2.0, show_default=True)
@click.option("--q-floor-sensitivity", type=float, multiple=True)
@click.option("--q-shift-threshold-sensitivity", type=float, multiple=True)
def main(
    base_root: Path,
    loo_root: Path,
    holdout: str,
    negative_control: tuple[str, ...],
    out_dir: Path,
    top_k: int,
    diagnostic_top_n: int,
    q_floor: float,
    q_shift_threshold: float,
    q_floor_sensitivity: tuple[float, ...],
    q_shift_threshold_sensitivity: tuple[float, ...],
) -> None:
    """Write GENIE dNdScv influence attribution outputs."""
    out_dir.mkdir(parents=True, exist_ok=True)
    primary = run_contrast(
        base_root=base_root,
        holdout_root=loo_root / holdout,
        top_k=top_k,
        diagnostic_top_n=diagnostic_top_n,
        q_floor=q_floor,
        q_shift_threshold=q_shift_threshold,
    )
    primary["rank_delta"].to_feather(out_dir / "genie_gene_rank_delta.feather")
    primary["evidence"].to_feather(out_dir / "genie_gene_cancer_evidence.feather")
    primary["influence"].to_feather(out_dir / "genie_cancer_build_influence.feather")

    negative_results: dict[str, ContrastResult] = {}
    for contrast in negative_control:
        result = run_contrast(
            base_root=base_root,
            holdout_root=loo_root / contrast,
            top_k=top_k,
            diagnostic_top_n=diagnostic_top_n,
            q_floor=q_floor,
            q_shift_threshold=q_shift_threshold,
        )
        result["influence"].to_feather(
            out_dir / f"negative_control_cancer_build_influence_{contrast}.feather"
        )
        negative_results[contrast] = result

    summary = _summary_json(
        holdout=holdout,
        negative_controls=negative_control,
        top_k=top_k,
        diagnostic_top_n=diagnostic_top_n,
        q_floor=q_floor,
        q_shift_threshold=q_shift_threshold,
        q_floor_sensitivity=q_floor_sensitivity,
        q_shift_threshold_sensitivity=q_shift_threshold_sensitivity,
        primary=primary,
        negative_results=negative_results,
    )
    (out_dir / "genie_influence_summary.json").write_text(
        json.dumps(_json_safe(summary), indent=2) + "\n"
    )
    click.echo(f"wrote GENIE influence outputs to {out_dir}")


def _ranked_for_join(ranked: pd.DataFrame, prefix: str) -> pd.DataFrame:
    out = ranked.rename(columns={"dndscv_rank": "rank"}).copy()
    missing = {"symbol", *RANKED_VALUE_COLUMNS} - set(out.columns)
    if missing:
        raise ValueError(
            f"{prefix} pooled dNdScv table missing columns: {sorted(missing)}"
        )
    return out[["symbol", *RANKED_VALUE_COLUMNS]]


def _diagnostic_symbols(
    base_ranked: pd.DataFrame, holdout_ranked: pd.DataFrame, diagnostic_top_n: int
) -> list[str]:
    return list(
        dict.fromkeys(
            [
                *_top_ranked_symbols(base_ranked, diagnostic_top_n),
                *_top_ranked_symbols(holdout_ranked, diagnostic_top_n),
            ]
        )
    )


def _top_ranked_symbols(ranked: pd.DataFrame, n: int) -> Iterable[str]:
    return ranked.head(n)["symbol"].dropna().astype(str)


def _prefixed_values(
    row: pd.Series | None, prefix: str
) -> dict[str, float | int | str | None]:
    if row is None:
        return {f"{prefix}_{column}": None for column in RANKED_VALUE_COLUMNS}
    return {f"{prefix}_{column}": row[column] for column in RANKED_VALUE_COLUMNS}


def _require_columns(df: pd.DataFrame, required: set[str], label: str) -> None:
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{label} missing required columns: {sorted(missing)}")


def _prepare_per_cancer_for_merge(
    df: pd.DataFrame, prefix: str, symbols: set[str]
) -> pd.DataFrame:
    filtered = df.loc[
        df["symbol"].astype(str).isin(symbols),
        ["symbol", "cancer_type", *PER_CANCER_PREFIX_COLUMNS],
    ]
    rename = {
        column: f"{prefix}_{name}" for column, name in PER_CANCER_PREFIX_COLUMNS.items()
    }
    return filtered.rename(columns=rename)


def _classify_support_row(row: pd.Series) -> str:
    base_tested = row["base_input_status"] in TESTED_STATUSES
    holdout_tested = row["holdout_input_status"] in TESTED_STATUSES
    if base_tested and not holdout_tested:
        return "full_only_tested"
    if holdout_tested and not base_tested:
        return "holdout_only_tested"

    base_significant = _truthy(row["base_significant_q05"])
    holdout_significant = _truthy(row["holdout_significant_q05"])
    if base_significant and not holdout_significant:
        return "lost_significance"
    if not base_significant and holdout_significant:
        return "gained_significance"
    if base_significant and holdout_significant:
        return "stable_significant"
    return "stable_not_significant"


def _truthy(value: object) -> bool:
    return False if pd.isna(value) else bool(value)


def _optional_int(value: object) -> int | None:
    if pd.isna(value):
        return None
    if isinstance(value, int | float | np.integer | np.floating):
        return int(value)
    raise TypeError(f"expected numeric rank value, got {type(value).__name__}")


def _is_meaningful_delta(value: float | int | None, threshold: float) -> bool:
    return value is not None and pd.notna(value) and abs(float(value)) >= threshold


def _assert_threshold_parity(cohort_meta: pd.DataFrame) -> None:
    for row in cohort_meta.itertuples(index=False):
        if int(row.base_min_samples_threshold) != int(
            row.holdout_min_samples_threshold
        ):
            raise ThresholdMismatchError(
                f"threshold mismatch for {row.cancer_type} {row.build}: "
                f"base min_samples={row.base_min_samples_threshold}, "
                f"holdout min_samples={row.holdout_min_samples_threshold}"
            )
        if int(row.base_min_variants_threshold) != int(
            row.holdout_min_variants_threshold
        ):
            raise ThresholdMismatchError(
                f"threshold mismatch for {row.cancer_type} {row.build}: "
                f"base min_variants={row.base_min_variants_threshold}, "
                f"holdout min_variants={row.holdout_min_variants_threshold}"
            )


def _threshold_transition(
    base_below_threshold: bool,
    holdout_below_threshold: bool,
    *,
    base_missing: bool = False,
    holdout_missing: bool = False,
) -> str:
    if base_missing or holdout_missing:
        return "missing"
    if not base_below_threshold and holdout_below_threshold:
        return "tested_to_below_threshold"
    if base_below_threshold and not holdout_below_threshold:
        return "below_threshold_to_tested"
    return "tested_to_tested"


def _count_lost_supported_full(group: pd.DataFrame) -> int:
    supported = {"full_only_tested", "lost_significance", "stable_significant"}
    return int(
        (
            (group["topk_status"] == "lost") & group["support_class"].isin(supported)
        ).sum()
    )


def _count_gained_supported_holdout(group: pd.DataFrame) -> int:
    supported = {"holdout_only_tested", "gained_significance", "stable_significant"}
    return int(
        (
            (group["topk_status"] == "gained") & group["support_class"].isin(supported)
        ).sum()
    )


def _explanatory_support_mask(
    group: pd.DataFrame, q_shift_threshold: float
) -> pd.Series:
    deltas = pd.to_numeric(group["delta_neg_log10_q"], errors="coerce").abs()
    return (
        group["support_class"].isin(
            {"lost_significance", "gained_significance", "stable_significant"}
        )
        | (
            (group["support_class"] == "full_only_tested")
            & group["base_significant_q05"].fillna(False).astype(bool)
        )
        | (
            (group["support_class"] == "holdout_only_tested")
            & group["holdout_significant_q05"].fillna(False).astype(bool)
        )
        | (deltas >= q_shift_threshold)
    )


def _prefix_cohort_meta(meta: pd.DataFrame, prefix: str) -> pd.DataFrame:
    keep = [
        "cancer_type",
        "build",
        "n_samples",
        "n_variants",
        "modality",
        "panel_only",
        "below_threshold",
        "min_samples_threshold",
        "min_variants_threshold",
    ]
    rename = {
        column: f"{prefix}_{column}"
        for column in keep
        if column not in {"cancer_type", "build"}
    }
    return meta[keep].rename(columns=rename)


def _load_pooled(root: Path) -> pd.DataFrame:
    path = root / "summary/mut/table/dndscv_pooled.feather"
    if not path.exists():
        raise FileNotFoundError(f"missing pooled dNdScv table: {path}")
    return pd.read_feather(path)


def _top_symbols_from_rank_delta(
    rank_delta: pd.DataFrame, rank_column: str, top_k: int
) -> set[str]:
    ranks = pd.to_numeric(rank_delta[rank_column], errors="coerce")
    return set(rank_delta.loc[ranks <= top_k, "symbol"].dropna().astype(str))


def _jaccard_at_top_k(rank_delta: pd.DataFrame, top_k: int) -> float:
    base = _top_symbols_from_rank_delta(rank_delta, "base_rank", top_k)
    holdout = _top_symbols_from_rank_delta(rank_delta, "holdout_rank", top_k)
    union = base | holdout
    return len(base & holdout) / len(union) if union else float("nan")


def _summary_json(
    *,
    holdout: str,
    negative_controls: tuple[str, ...],
    top_k: int,
    diagnostic_top_n: int,
    q_floor: float,
    q_shift_threshold: float,
    q_floor_sensitivity: tuple[float, ...],
    q_shift_threshold_sensitivity: tuple[float, ...],
    primary: ContrastResult,
    negative_results: dict[str, ContrastResult],
) -> dict[str, object]:
    primary_influence = primary["influence"]
    top_genie_keys = set(
        zip(
            primary_influence.head(10)["cancer_type"].astype(str),
            primary_influence.head(10)["build"].astype(str),
            strict=False,
        )
    )
    return {
        "parameters": {
            "holdout": holdout,
            "negative_controls": list(negative_controls),
            "top_k": top_k,
            "diagnostic_top_n": diagnostic_top_n,
            "q_floor": q_floor,
            "q_shift_threshold": q_shift_threshold,
            "q_floor_sensitivity": list(q_floor_sensitivity),
            "q_shift_threshold_sensitivity": list(q_shift_threshold_sensitivity),
        },
        "loaded_counts": {
            holdout: primary["counts"],
            **{name: result["counts"] for name, result in negative_results.items()},
        },
        "topk_gene_counts": {
            holdout: _topk_gene_counts(primary["rank_delta"]),
            **{
                name: _topk_gene_counts(result["rank_delta"])
                for name, result in negative_results.items()
            },
        },
        "top_cancer_build_attributions": _top_influence_rows(primary_influence),
        "negative_control_comparison": {
            name: _negative_control_summary(
                result["rank_delta"],
                result["influence"],
                top_k,
                top_genie_keys,
            )
            for name, result in negative_results.items()
        },
        "sensitivity": _sensitivity_summary(
            primary=primary,
            q_floor_sensitivity=q_floor_sensitivity,
            q_shift_threshold_sensitivity=q_shift_threshold_sensitivity,
        ),
    }


def _topk_gene_counts(rank_delta: pd.DataFrame) -> dict[str, int]:
    counts = rank_delta["topk_status"].value_counts().to_dict()
    return {
        status: int(counts.get(status, 0))
        for status in ("lost", "gained", "stable", "outside_top100")
    }


def _top_influence_rows(
    influence: pd.DataFrame, n: int = 10
) -> list[dict[str, object]]:
    if influence.empty:
        return []
    columns = [
        "cancer_type",
        "build",
        "mechanism_class",
        "n_affected_genes",
        "n_lost_top100_supported_full",
        "n_gained_top100_supported_holdout",
        "sum_abs_rank_delta_supported",
        "delta_n_samples",
        "delta_n_variants",
        "threshold_transition",
    ]
    return influence.head(n)[columns].to_dict(orient="records")


def _negative_control_summary(
    rank_delta: pd.DataFrame,
    influence: pd.DataFrame,
    top_k: int,
    top_genie_keys: set[tuple[str, str]],
) -> dict[str, object]:
    control_keys = set(
        zip(
            influence.head(10)["cancer_type"].astype(str),
            influence.head(10)["build"].astype(str),
            strict=False,
        )
    )
    return {
        "jaccard_at_top_k": _jaccard_at_top_k(rank_delta, top_k),
        "lost_topk_count": int((rank_delta["topk_status"] == "lost").sum()),
        "gained_topk_count": int((rank_delta["topk_status"] == "gained").sum()),
        "stable_topk_count": int((rank_delta["topk_status"] == "stable").sum()),
        "top_cancer_build_rows": _top_influence_rows(influence),
        "top_genie_overlap_count": len(top_genie_keys & control_keys),
        "max_sum_abs_rank_delta_supported": float(
            influence["sum_abs_rank_delta_supported"].max()
        )
        if not influence.empty
        else 0.0,
        "median_sum_abs_rank_delta_supported": float(
            influence["sum_abs_rank_delta_supported"].median()
        )
        if not influence.empty
        else 0.0,
    }


def _sensitivity_summary(
    *,
    primary: ContrastResult,
    q_floor_sensitivity: tuple[float, ...],
    q_shift_threshold_sensitivity: tuple[float, ...],
) -> dict[str, object]:
    base_per_cancer = primary["base_per_cancer"]
    holdout_per_cancer = primary["holdout_per_cancer"]
    rank_delta = primary["rank_delta"]
    cohort_meta = primary["cohort_meta"]
    by_q_floor = {}
    for floor in q_floor_sensitivity:
        evidence = compare_gene_cancer_evidence(
            base_per_cancer, holdout_per_cancer, rank_delta, q_floor=floor
        )
        by_q_floor[str(floor)] = (
            evidence["support_class"].value_counts().astype(int).to_dict()
        )
    by_q_shift_threshold = {}
    evidence = primary["evidence"]
    for threshold in q_shift_threshold_sensitivity:
        influence = score_cancer_build_influence(
            evidence, cohort_meta, q_shift_threshold=threshold
        )
        by_q_shift_threshold[str(threshold)] = (
            influence["mechanism_class"].value_counts().astype(int).to_dict()
        )
    return {"q_floor": by_q_floor, "q_shift_threshold": by_q_shift_threshold}


def _json_safe(value: object) -> object:
    if isinstance(value, dict):
        return {str(key): _json_safe(inner) for key, inner in value.items()}
    if isinstance(value, list):
        return [_json_safe(inner) for inner in value]
    if isinstance(value, tuple):
        return [_json_safe(inner) for inner in value]
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return None if np.isnan(value) else float(value)
    if isinstance(value, float):
        return None if np.isnan(value) else value
    if pd.isna(value):
        return None
    return value


if __name__ == "__main__":
    main()
