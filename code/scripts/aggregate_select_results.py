"""Rule (4): aggregate per-cell SELECT outputs into headline feathers.

This task implements the B-tier slice. Subsequent tasks add A-tier Stouffer,
union join + concordance flag, and pathway rollup + sibling annotation.
"""

from pathlib import Path

import pandas as pd

import select_lib as lib


KEY_COLS = ["gene_i", "gene_j", "cancer_type", "cohort"]
B_RENAME = {
    "n_samples": "b_n_samples",
    "n_i_only": "b_n_i_only",
    "n_j_only": "b_n_j_only",
    "n_both": "b_n_both",
    "n_neither": "b_n_neither",
    "select_score": "b_select_score",
    "p_wMI": "b_p_wMI",
    "p_ME": "b_p_ME",
    "direction": "b_direction",
    "skip_reason": "b_skip_reason",
}


def concat_b_tier(per_cell_paths: list[Path]) -> pd.DataFrame:
    """Concatenate all B-tier per-cell pair feathers, dropping sentinel rows."""
    frames = []
    for p in per_cell_paths:
        df = pd.read_feather(p)
        df = df[df["tier"] == "B"]
        df = df[df["skip_reason"].isna()]  # drop sentinel rows
        frames.append(df)
    if not frames:
        return pd.DataFrame(columns=list(B_RENAME.keys()) + KEY_COLS)
    return pd.concat(frames, ignore_index=True)


def compute_b_tier_qvalues(df_b: pd.DataFrame) -> pd.DataFrame:
    """Add b_q_wMI_within_stratum via BH-FDR per (cancer_type, cohort)."""
    df = df_b.rename(columns=B_RENAME).copy()
    if df.empty:
        df["b_q_wMI_within_stratum"] = pd.Series(dtype="float64")
        return df
    df["b_q_wMI_within_stratum"] = lib.bh_fdr_within_groups(
        df, group_cols=["cancer_type", "cohort"], pvalue_col="b_p_wMI"
    )
    return df


if "snakemake" in globals():  # pragma: no cover  # set by Snakemake's script: directive
    raise NotImplementedError("Snakemake entry point lands in Task 17.")
