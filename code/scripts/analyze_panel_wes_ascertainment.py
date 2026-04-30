"""Panel-vs-WES ascertainment analysis for t154.

This script compares mutation-frequency rankings across assay strata using the
callability-aware long table produced for the t077 pooled meta-analysis.
"""

from __future__ import annotations

from itertools import combinations
from pathlib import Path
from typing import Literal

import click
import numpy as np
import pandas as pd


type AssayStratum = Literal["panel", "wes", "combined"]

PANEL_CLASSES = {"large_hybrid_capture", "small_amplicon"}
WES_CLASSES = {"WES", "MC3"}
STRATUM_ORDER: tuple[AssayStratum, ...] = ("wes", "panel", "combined")


def panel_class_to_assay_stratum(panel_class: str) -> Literal["panel", "wes"]:
    """Collapse pipeline panel classes into the t154 two-stratum comparison."""
    if panel_class in PANEL_CLASSES:
        return "panel"
    if panel_class in WES_CLASSES:
        return "wes"
    raise ValueError(f"Unsupported panel_class {panel_class!r}")


def build_gene_cancer_rankings(
    pooled_input: pd.DataFrame,
    annotated: pd.DataFrame,
    *,
    analysis_view: Literal["inclusive", "exclusive"] = "inclusive",
) -> pd.DataFrame:
    """Build assay-stratified per-(cancer, gene) rankings from y/n counts."""
    y_col = f"y_{analysis_view}"
    n_col = f"n_{analysis_view}"
    required = {"study_id", "cancer_type", "symbol", y_col, n_col, "panel_class"}
    missing = required - set(pooled_input.columns)
    if missing:
        raise ValueError(f"pooled_input missing required columns: {sorted(missing)}")

    base = pooled_input.loc[pooled_input[n_col].notna()].copy()
    base["assay_stratum"] = base["panel_class"].map(panel_class_to_assay_stratum)
    base = base.loc[base[n_col].astype(float) > 0].copy()

    stratum_rows = _aggregate_counts(base, y_col=y_col, n_col=n_col)
    combined = base.copy()
    combined["assay_stratum"] = "combined"
    combined_rows = _aggregate_counts(combined, y_col=y_col, n_col=n_col)
    rankings = pd.concat([stratum_rows, combined_rows], ignore_index=True)
    rankings["analysis_view"] = analysis_view

    overlay_cols = ["cancer_type", "symbol"]
    optional = [
        col for col in ("bailey2018_driver", "cgc_tier_1") if col in annotated.columns
    ]
    if optional:
        overlay = (
            annotated[overlay_cols + optional]
            .drop_duplicates(subset=overlay_cols)
            .copy()
        )
        rankings = rankings.merge(overlay, on=overlay_cols, how="left")
        for col in optional:
            rankings[col] = rankings[col].fillna(False).astype(bool)

    return rankings.sort_values(
        ["assay_stratum", "rank", "cancer_type", "symbol"]
    ).reset_index(drop=True)


def build_cancer_type_eligibility(pooled_input: pd.DataFrame) -> pd.DataFrame:
    """Return cancer types with study counts by assay stratum."""
    base = (
        pooled_input[["study_id", "cancer_type", "panel_class"]]
        .drop_duplicates()
        .copy()
    )
    base["assay_stratum"] = base["panel_class"].map(panel_class_to_assay_stratum)
    counts = (
        base.groupby(["cancer_type", "assay_stratum"], as_index=False)["study_id"]
        .nunique()
        .pivot(index="cancer_type", columns="assay_stratum", values="study_id")
        .fillna(0)
        .astype(int)
        .reset_index()
    )
    for col in ("panel", "wes"):
        if col not in counts.columns:
            counts[col] = 0
    counts = counts.rename(columns={"panel": "n_panel_studies", "wes": "n_wes_studies"})
    counts["has_panel_and_wes"] = (counts["n_panel_studies"] > 0) & (
        counts["n_wes_studies"] > 0
    )
    return counts[
        ["cancer_type", "n_panel_studies", "n_wes_studies", "has_panel_and_wes"]
    ]


def compare_topk_rankings(
    rankings: pd.DataFrame, *, k_values: tuple[int, ...]
) -> pd.DataFrame:
    """Compare top-K ranked pair sets between assay strata."""
    rows: list[dict[str, float | int | str]] = []
    present = set(rankings["assay_stratum"].dropna().unique().tolist())
    strata = [stratum for stratum in STRATUM_ORDER if stratum in present]
    for left, right in combinations(strata, 2):
        left_df = rankings.loc[rankings["assay_stratum"] == left]
        right_df = rankings.loc[rankings["assay_stratum"] == right]
        for k in k_values:
            left_top = _topk(left_df, k)
            right_top = _topk(right_df, k)
            left_set = _pair_set(left_top)
            right_set = _pair_set(right_top)
            intersection = left_set & right_set
            union = left_set | right_set
            rows.append(
                {
                    "left_stratum": left,
                    "right_stratum": right,
                    "k": k,
                    "left_size": len(left_set),
                    "right_size": len(right_set),
                    "intersection": len(intersection),
                    "jaccard": len(intersection) / len(union)
                    if union
                    else float("nan"),
                    "left_recovery": len(intersection) / len(left_set)
                    if left_set
                    else float("nan"),
                    "right_recovery": len(intersection) / len(right_set)
                    if right_set
                    else float("nan"),
                    "left_bailey_recovery": _flag_fraction(
                        left_top, "bailey2018_driver"
                    ),
                    "right_bailey_recovery": _flag_fraction(
                        right_top, "bailey2018_driver"
                    ),
                    "left_cgc_tier1_recovery": _flag_fraction(left_top, "cgc_tier_1"),
                    "right_cgc_tier1_recovery": _flag_fraction(right_top, "cgc_tier_1"),
                    "shared_rank_spearman": _shared_rank_spearman(left_df, right_df),
                }
            )
    return pd.DataFrame(rows)


def build_attention_regression(
    rankings: pd.DataFrame, gene_features: pd.DataFrame
) -> pd.DataFrame:
    """Fit log10 PubTator attention against log10 length and stratum mutation rate."""
    required_features = {"symbol", "length", "pubtator_mention_count"}
    missing = required_features - set(gene_features.columns)
    if missing:
        raise ValueError(f"gene_features missing required columns: {sorted(missing)}")

    gene_rates = (
        rankings.loc[rankings["assay_stratum"].isin(["wes", "panel", "combined"])]
        .groupby(["assay_stratum", "symbol"], as_index=False)
        .agg(
            mean_rate=("rate", "mean"),
            max_rate=("rate", "max"),
            n_gene_cancer_pairs=("cancer_type", "nunique")
            if "cancer_type" in rankings.columns
            else ("rate", "size"),
        )
    )
    features = gene_features[
        ["symbol", "length", "pubtator_mention_count"]
    ].drop_duplicates("symbol")
    merged = gene_rates.merge(features, on="symbol", how="inner")
    merged = merged.loc[
        (merged["length"].astype(float) > 0)
        & merged["pubtator_mention_count"].notna()
        & (merged["mean_rate"].astype(float) > 0)
    ].copy()
    merged["log_attention"] = np.log10(
        merged["pubtator_mention_count"].astype(float) + 1.0
    )
    merged["log_length"] = np.log10(merged["length"].astype(float))
    merged["log_rate"] = np.log10(merged["mean_rate"].astype(float))

    rows: list[dict[str, float | int | str]] = []
    for stratum, sub in merged.groupby("assay_stratum", sort=True):
        beta_log_length, beta_log_rate, intercept = _least_squares_coefficients(sub)
        rows.append(
            {
                "assay_stratum": str(stratum),
                "n_genes": int(len(sub)),
                "intercept": intercept,
                "beta_log_length": beta_log_length,
                "beta_log_rate": beta_log_rate,
                "spearman_attention_length": _spearman(
                    sub["log_attention"], sub["log_length"]
                ),
                "spearman_attention_rate": _spearman(
                    sub["log_attention"], sub["log_rate"]
                ),
            }
        )
    return pd.DataFrame(rows)


def _aggregate_counts(base: pd.DataFrame, *, y_col: str, n_col: str) -> pd.DataFrame:
    grouped = base.groupby(
        ["assay_stratum", "cancer_type", "symbol"], as_index=False
    ).agg(
        y_total=(y_col, "sum"),
        n_total=(n_col, "sum"),
        n_studies=("study_id", "nunique"),
    )
    grouped["rate"] = grouped["y_total"].astype(float) / grouped["n_total"].astype(
        float
    )
    grouped = grouped.sort_values(
        ["assay_stratum", "rate", "n_total", "cancer_type", "symbol"],
        ascending=[True, False, False, True, True],
        kind="mergesort",
    )
    grouped["rank"] = grouped.groupby("assay_stratum").cumcount() + 1
    return grouped


def _topk(df: pd.DataFrame, k: int) -> pd.DataFrame:
    return df.sort_values(["rank", "cancer_type", "symbol"], kind="mergesort").head(k)


def _pair_set(df: pd.DataFrame) -> set[tuple[str, str]]:
    return set(
        zip(df["cancer_type"].astype(str), df["symbol"].astype(str), strict=True)
    )


def _flag_fraction(df: pd.DataFrame, col: str) -> float:
    if df.empty or col not in df.columns:
        return float("nan")
    return float(df[col].fillna(False).astype(bool).mean())


def _shared_rank_spearman(left_df: pd.DataFrame, right_df: pd.DataFrame) -> float:
    left = left_df[["cancer_type", "symbol", "rank"]].rename(
        columns={"rank": "left_rank"}
    )
    right = right_df[["cancer_type", "symbol", "rank"]].rename(
        columns={"rank": "right_rank"}
    )
    shared = left.merge(right, on=["cancer_type", "symbol"], how="inner")
    if len(shared) < 2:
        return float("nan")
    return _spearman(shared["left_rank"], shared["right_rank"])


def _spearman(left: pd.Series, right: pd.Series) -> float:
    if len(left) < 2 or len(right) < 2:
        return float("nan")
    return float(left.rank(method="average").corr(right.rank(method="average")))


def _least_squares_coefficients(sub: pd.DataFrame) -> tuple[float, float, float]:
    if sub.empty:
        return float("nan"), float("nan"), float("nan")
    x = np.column_stack(
        [
            np.ones(len(sub), dtype=float),
            sub["log_length"].to_numpy(dtype=float),
            sub["log_rate"].to_numpy(dtype=float),
        ]
    )
    y = sub["log_attention"].to_numpy(dtype=float)
    beta, *_ = np.linalg.lstsq(x, y, rcond=None)
    return float(beta[1]), float(beta[2]), float(beta[0])


@click.command()
@click.option("--pooled-input", "pooled_input_path", type=Path, required=True)
@click.option("--annotated", "annotated_path", type=Path, required=True)
@click.option("--three-way", "three_way_path", type=Path, required=True)
@click.option("--out-dir", "out_dir", type=Path, required=True)
@click.option(
    "--k", "k_values", type=int, multiple=True, default=(10, 25, 50, 100, 250, 500)
)
def main(
    pooled_input_path: Path,
    annotated_path: Path,
    three_way_path: Path,
    out_dir: Path,
    k_values: tuple[int, ...],
) -> None:
    """Run the t154 panel-vs-WES ascertainment analysis."""
    pooled_input = pd.read_feather(pooled_input_path)
    annotated = pd.read_feather(annotated_path)
    three_way = pd.read_feather(three_way_path)
    out_dir.mkdir(parents=True, exist_ok=True)

    eligibility = build_cancer_type_eligibility(pooled_input)
    eligible_cancers = set(
        eligibility.loc[eligibility["has_panel_and_wes"], "cancer_type"]
    )
    eligible_input = pooled_input.loc[
        pooled_input["cancer_type"].isin(eligible_cancers)
    ].copy()

    rankings = build_gene_cancer_rankings(
        eligible_input, annotated, analysis_view="inclusive"
    )
    overlap = compare_topk_rankings(rankings, k_values=tuple(k_values))
    regression = build_attention_regression(rankings, three_way)

    eligibility.to_feather(out_dir / "cancer_type_eligibility.feather")
    rankings.to_feather(out_dir / "stratum_gene_cancer_rankings.feather")
    overlap.to_feather(out_dir / "topk_overlap.feather")
    regression.to_feather(out_dir / "attention_regression.feather")

    print(f"wrote: {out_dir / 'cancer_type_eligibility.feather'}")
    print(f"wrote: {out_dir / 'stratum_gene_cancer_rankings.feather'}")
    print(f"wrote: {out_dir / 'topk_overlap.feather'}")
    print(f"wrote: {out_dir / 'attention_regression.feather'}")
    print(f"eligible mixed cancer types: {len(eligible_cancers)}")


if __name__ == "__main__":
    main()
