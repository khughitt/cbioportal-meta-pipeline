# science:code
# status: exploratory
# science:end
"""Compare full-cohort vs leave-one-study-out dNdScv gene rankings.

Task t173 requires real dNdScv reruns per holdout because the canonical
per-cancer dNdScv outputs do not retain enough study identity to subtract a
study analytically. This script analyzes completed holdout runs, each of which
contains its own ``summary/mut/table/dndscv_pooled.feather``.
"""

from __future__ import annotations

from pathlib import Path

import click
import pandas as pd

from symbol_normalization import expand_reference_symbols_to_universe

K_VALUES = (10, 25, 50, 100)
BASE_OVERLAP_COLUMNS = [
    "excluded_study_id",
    "k",
    "base_size",
    "holdout_size",
    "intersection",
    "jaccard",
    "base_recovery",
    "holdout_recovery",
]


def rank_dndscv_genes(pooled: pd.DataFrame) -> pd.DataFrame:
    """Return pooled dNdScv genes in canonical t144 ranking order."""
    ranked = (
        pooled.copy()
        .sort_values(
            by=["min_qglobal", "n_cancers_significant_q05"],
            ascending=[True, False],
            na_position="last",
        )
        .reset_index(drop=True)
    )
    ranked["dndscv_rank"] = range(1, len(ranked) + 1)
    return ranked


def extract_reference_sets(
    annotated: pd.DataFrame, universe: set[str]
) -> dict[str, set[str]]:
    """Extract driver reference sets restricted to ranked genes.

    ``cgc_tier1`` is tier-1-only. ``cgc_tier1_or_2`` is the inclusive CGC set.
    """
    cgc_tier_1 = _symbols_where(annotated, "cgc_tier_1", universe)
    cgc_tier_2 = _symbols_where(annotated, "cgc_tier_2", universe)
    return {
        "bailey2018": _symbols_where(annotated, "bailey2018_driver", universe),
        "cgc_tier1": cgc_tier_1,
        "cgc_tier1_or_2": cgc_tier_1 | cgc_tier_2,
    }


def compare_loso_rankings(
    base: pd.DataFrame,
    loo_frames: dict[str, pd.DataFrame],
    annotated: pd.DataFrame,
    k_values: tuple[int, ...] = K_VALUES,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Compare base dNdScv ranking to each completed LOO dNdScv ranking."""
    base_ranked = rank_dndscv_genes(base)
    universe = set(base_ranked["symbol"].dropna().astype(str))
    for holdout in loo_frames.values():
        universe |= set(holdout["symbol"].dropna().astype(str))
    references = extract_reference_sets(annotated, universe)

    rows: list[dict[str, float | int | str]] = []
    for excluded_study, holdout in sorted(loo_frames.items()):
        holdout_ranked = rank_dndscv_genes(holdout)
        for k in k_values:
            base_set = _top_symbols(base_ranked, k)
            holdout_set = _top_symbols(holdout_ranked, k)
            row: dict[str, float | int | str] = {
                "excluded_study_id": excluded_study,
                "k": k,
                **_overlap_metrics(base_set, holdout_set),
            }
            for reference_name, reference_set in references.items():
                row[f"base_{reference_name}_recovery_in_top"] = _top_reference_recovery(
                    base_set, reference_set
                )
                row[f"holdout_{reference_name}_recovery_in_top"] = (
                    _top_reference_recovery(holdout_set, reference_set)
                )
            rows.append(row)

    overlap = pd.DataFrame(rows, columns=_overlap_columns(tuple(references)))
    summary = summarize_loso_overlap(overlap)
    return overlap, summary


def summarize_loso_overlap(overlap: pd.DataFrame) -> pd.DataFrame:
    """Summarize dNdScv LOSO stability across completed holdout iterations."""
    if overlap.empty:
        return pd.DataFrame(
            columns=[
                "k",
                "n_iterations",
                "jaccard_median",
                "jaccard_min",
                "base_recovery_median",
                "base_recovery_min",
                "holdout_recovery_median",
                "holdout_recovery_min",
            ]
        )
    return (
        overlap.groupby("k", as_index=False)
        .agg(
            n_iterations=("excluded_study_id", "nunique"),
            jaccard_median=("jaccard", "median"),
            jaccard_min=("jaccard", "min"),
            base_recovery_median=("base_recovery", "median"),
            base_recovery_min=("base_recovery", "min"),
            holdout_recovery_median=("holdout_recovery", "median"),
            holdout_recovery_min=("holdout_recovery", "min"),
        )
        .reset_index(drop=True)
    )


def discover_loso_frames(loo_root: Path) -> dict[str, pd.DataFrame]:
    """Load completed holdout ``dndscv_pooled.feather`` files below a root."""
    frames: dict[str, pd.DataFrame] = {}
    for pooled_path in sorted(
        loo_root.glob("exclude_*/summary/mut/table/dndscv_pooled.feather")
    ):
        excluded_study = pooled_path.parts[-5].removeprefix("exclude_")
        frames[excluded_study] = pd.read_feather(pooled_path)
    return frames


def _symbols_where(
    annotated: pd.DataFrame, flag_col: str, universe: set[str]
) -> set[str]:
    if flag_col not in annotated.columns:
        return set()
    flags = annotated[flag_col].fillna(False).astype(bool)
    reference_symbols = annotated.loc[flags, "symbol"].dropna().astype(str)
    return expand_reference_symbols_to_universe(reference_symbols, universe)


def _top_symbols(ranked: pd.DataFrame, k: int) -> set[str]:
    return set(ranked.head(k)["symbol"].dropna().astype(str))


def _overlap_metrics(
    base_set: set[str], holdout_set: set[str]
) -> dict[str, float | int]:
    intersection = base_set & holdout_set
    union = base_set | holdout_set
    return {
        "base_size": len(base_set),
        "holdout_size": len(holdout_set),
        "intersection": len(intersection),
        "jaccard": len(intersection) / len(union) if union else float("nan"),
        "base_recovery": len(intersection) / len(base_set)
        if base_set
        else float("nan"),
        "holdout_recovery": len(intersection) / len(holdout_set)
        if holdout_set
        else float("nan"),
    }


def _top_reference_recovery(top_set: set[str], reference_set: set[str]) -> float:
    return len(top_set & reference_set) / len(top_set) if top_set else float("nan")


def _overlap_columns(reference_names: tuple[str, ...]) -> list[str]:
    reference_columns = [
        column
        for reference_name in reference_names
        for column in (
            f"base_{reference_name}_recovery_in_top",
            f"holdout_{reference_name}_recovery_in_top",
        )
    ]
    return [*BASE_OVERLAP_COLUMNS, *reference_columns]


@click.command()
@click.option(
    "--base",
    "base_path",
    type=Path,
    required=True,
    help="Full-cohort dndscv_pooled.feather",
)
@click.option(
    "--annotated",
    "annotated_path",
    type=Path,
    required=True,
    help="gene_cancer_study_ratio_annotated_dndscv.feather",
)
@click.option(
    "--loo-root",
    type=Path,
    required=True,
    help="Root containing exclude_*/summary/mut/table outputs",
)
@click.option("--out-dir", type=Path, required=True, help="Output directory")
def main(base_path: Path, annotated_path: Path, loo_root: Path, out_dir: Path) -> None:
    base = pd.read_feather(base_path)
    annotated = pd.read_feather(annotated_path)
    loo_frames = discover_loso_frames(loo_root)
    overlap, summary = compare_loso_rankings(base, loo_frames, annotated)

    out_dir.mkdir(parents=True, exist_ok=True)
    overlap_path = out_dir / "dndscv_loso_topk_overlap.feather"
    summary_path = out_dir / "dndscv_loso_summary.feather"
    overlap.to_feather(overlap_path)
    summary.to_feather(summary_path)

    click.echo(f"loaded {len(loo_frames):,} completed holdout dNdScv runs")
    click.echo(f"wrote: {overlap_path}")
    click.echo(f"wrote: {summary_path}")
    if not summary.empty:
        with pd.option_context("display.max_rows", None, "display.width", 160):
            click.echo(summary.to_string(index=False))


if __name__ == "__main__":
    main()
