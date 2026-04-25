"""Unit tests for aggregate_select_results."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

import aggregate_select_results as mod


def _per_cell(rows: list[dict]) -> pd.DataFrame:
    base = {
        "gene_i": "TP53",
        "gene_j": "KRAS",
        "select_score": 0.0,
        "p_wMI": np.nan,
        "p_ME": np.nan,
        "direction": "none",
        "n_samples": 100,
        "n_i_only": 10,
        "n_j_only": 10,
        "n_both": 5,
        "n_neither": 75,
        "cancer_type": "luad",
        "tier": "B",
        "study": pd.NA,
        "cohort": "exclusive",
        "skip_reason": pd.NA,
    }
    return pd.DataFrame([{**base, **r} for r in rows])


def test_concat_b_tier_strips_sentinel_rows(tmp_path: Path):
    cell_a = _per_cell(
        [
            {"gene_i": "TP53", "gene_j": "KRAS", "p_wMI": 0.001, "direction": "ME"},
            {"gene_i": "TP53", "gene_j": "EGFR", "p_wMI": 0.5, "direction": "CO"},
        ]
    )
    cell_b_sentinel = _per_cell(
        [
            {
                "gene_i": pd.NA,
                "gene_j": pd.NA,
                "p_wMI": np.nan,
                "skip_reason": "n_samples_below_threshold",
            },
        ]
    )
    pa = tmp_path / "a.feather"
    cell_a.to_feather(pa)
    pb = tmp_path / "b.feather"
    cell_b_sentinel.to_feather(pb)
    out = mod.concat_b_tier([pa, pb])
    assert len(out) == 2  # sentinel dropped
    assert set(out["gene_j"]) == {"KRAS", "EGFR"}


def test_bh_fdr_within_stratum_applied(tmp_path: Path):
    df = _per_cell(
        [
            {"gene_i": "TP53", "gene_j": "KRAS", "p_wMI": 0.001, "direction": "ME"},
            {"gene_i": "TP53", "gene_j": "EGFR", "p_wMI": 0.5, "direction": "CO"},
            {"gene_i": "TP53", "gene_j": "BRAF", "p_wMI": 0.5, "direction": "CO"},
        ]
    )
    out = mod.compute_b_tier_qvalues(df)
    qs = out.set_index("gene_j")["b_q_wMI_within_stratum"].to_dict()
    np.testing.assert_allclose(qs["KRAS"], 0.003, rtol=1e-6)
    np.testing.assert_allclose(qs["EGFR"], 0.5, rtol=1e-6)
    np.testing.assert_allclose(qs["BRAF"], 0.5, rtol=1e-6)


def test_b_tier_columns_have_b_prefix(tmp_path: Path):
    df = _per_cell(
        [{"gene_i": "TP53", "gene_j": "KRAS", "p_wMI": 0.001, "direction": "ME"}]
    )
    out = mod.compute_b_tier_qvalues(df)
    expected_b_cols = {
        "b_n_samples",
        "b_n_i_only",
        "b_n_j_only",
        "b_n_both",
        "b_n_neither",
        "b_select_score",
        "b_p_wMI",
        "b_p_ME",
        "b_direction",
        "b_q_wMI_within_stratum",
        "b_skip_reason",
    }
    assert expected_b_cols.issubset(set(out.columns))
