"""Rule (4): aggregate per-cell SELECT outputs into headline feathers.

This task implements the B-tier slice. Subsequent tasks add A-tier Stouffer,
union join + concordance flag, and pathway rollup + sibling annotation.
"""

from pathlib import Path

import numpy as np
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


def concat_a_tier(per_cell_paths: list[Path]) -> pd.DataFrame:
    """Concatenate all A-tier per-cell pair feathers (sentinels included)."""
    frames = []
    for p in per_cell_paths:
        df = pd.read_feather(p)
        df = df[df["tier"] == "A"]
        frames.append(df)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def compute_a_tier_stouffer(df_a: pd.DataFrame) -> pd.DataFrame:
    """Sign-aware weighted-Z aggregate over A-tier per-study cells.

    Returns one row per (gene_i, gene_j, cancer_type, cohort) appearing in df_a
    with non-sentinel rows. Sentinel rows count toward `a_k_studies_attempted`
    but not `a_k_studies_contributing`.
    """
    if df_a.empty:
        return pd.DataFrame()

    df = df_a.copy()
    df["is_sentinel"] = df["skip_reason"].notna()

    real = df[~df["is_sentinel"]].copy()
    if real.empty:
        return pd.DataFrame()

    sign_map = {"CO": +1, "ME": -1, "none": 0}
    real["sign"] = real["direction"].map(sign_map).fillna(0).astype(int)
    real["weight"] = np.sqrt(real["n_samples"].astype(float))

    out_rows: list[dict] = []
    for keys, sub in real.groupby(KEY_COLS, observed=True):
        z, p, n_used = lib.signed_stouffer(
            pvalues=sub["p_wMI"].to_numpy(dtype=float),
            signs=sub["sign"].to_numpy(dtype=float),
            weights=sub["weight"].to_numpy(dtype=float),
        )
        d_frac = lib.direction_consensus_frac(sub["direction"].astype(str).tolist())

        # Attempted count: contributing studies for this pair plus sentinel A-tier
        # studies in the same cancer_type x cohort.
        ct, ch = keys[2], keys[3]
        sentinel_studies = (
            df_a[
                (df_a["cancer_type"] == ct)
                & (df_a["cohort"] == ch)
                & df_a["skip_reason"].notna()
            ]["study"]
            .dropna()
            .unique()
        )
        attempted = n_used + len(set(sentinel_studies))

        out_rows.append(
            {
                "gene_i": keys[0],
                "gene_j": keys[1],
                "cancer_type": ct,
                "cohort": ch,
                "a_stouffer_z_wMI": z,
                "a_stouffer_p_wMI": p,
                "a_k_studies_contributing": int(n_used),
                "a_k_studies_attempted": int(attempted),
                "a_direction_consensus_frac": d_frac,
                "a_skip_reason": pd.NA,
            }
        )
    out = pd.DataFrame(out_rows)
    if out.empty:
        return out
    out["a_q_wMI_within_stratum"] = lib.bh_fdr_within_groups(
        out, group_cols=["cancer_type", "cohort"], pvalue_col="a_stouffer_p_wMI"
    )
    return out


if "snakemake" in globals():  # pragma: no cover  # set by Snakemake's script: directive
    raise NotImplementedError("Snakemake entry point lands in Task 17.")
