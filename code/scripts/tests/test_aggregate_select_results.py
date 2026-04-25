"""Unit tests for aggregate_select_results."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

import pytest

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


def _per_cell_a(study: str, p: float, direction: str, n: int = 100) -> dict:
    return {
        "gene_i": "TP53",
        "gene_j": "KRAS",
        "select_score": 0.0,
        "p_wMI": p,
        "p_ME": p,
        "direction": direction,
        "n_samples": n,
        "n_i_only": 10,
        "n_j_only": 10,
        "n_both": 5,
        "n_neither": n - 25,
        "cancer_type": "luad",
        "tier": "A",
        "study": study,
        "cohort": "exclusive",
        "skip_reason": pd.NA,
    }


def test_a_tier_stouffer_aggregates_by_pair(tmp_path: Path):
    rows = [
        _per_cell_a("st1", 0.01, "ME"),
        _per_cell_a("st2", 0.05, "ME"),
        _per_cell_a("st3", 0.02, "ME"),
    ]
    df_a = pd.DataFrame(rows)
    out = mod.compute_a_tier_stouffer(df_a)
    assert len(out) == 1
    row = out.iloc[0]
    assert row["a_k_studies_contributing"] == 3
    assert row["a_k_studies_attempted"] == 3
    np.testing.assert_allclose(row["a_direction_consensus_frac"], 1.0)
    assert row["a_stouffer_p_wMI"] < 0.05


def test_a_tier_stouffer_handles_mixed_directions(tmp_path: Path):
    rows = [
        _per_cell_a("st1", 0.001, "ME"),
        _per_cell_a("st2", 0.001, "CO"),
        _per_cell_a("st3", 0.001, "ME"),
    ]
    df_a = pd.DataFrame(rows)
    out = mod.compute_a_tier_stouffer(df_a)
    row = out.iloc[0]
    np.testing.assert_allclose(row["a_direction_consensus_frac"], 2 / 3)
    rows_all_aligned = [_per_cell_a(f"st{i}", 0.001, "ME") for i in range(3)]
    aligned = mod.compute_a_tier_stouffer(pd.DataFrame(rows_all_aligned))
    assert abs(row["a_stouffer_z_wMI"]) < abs(aligned.iloc[0]["a_stouffer_z_wMI"])


def test_a_tier_counts_attempted_includes_sentinels(tmp_path: Path):
    rows = [
        _per_cell_a("st1", 0.01, "ME"),
        # Sentinel row from a small-N A-tier study cell.
        {
            "gene_i": pd.NA,
            "gene_j": pd.NA,
            "select_score": np.nan,
            "p_wMI": np.nan,
            "p_ME": np.nan,
            "direction": pd.NA,
            "n_samples": pd.NA,
            "n_i_only": pd.NA,
            "n_j_only": pd.NA,
            "n_both": pd.NA,
            "n_neither": pd.NA,
            "cancer_type": "luad",
            "tier": "A",
            "study": "st_small",
            "cohort": "exclusive",
            "skip_reason": "n_samples_below_threshold",
        },
    ]
    df_a = pd.DataFrame(rows)
    out = mod.compute_a_tier_stouffer(df_a)
    row = out.iloc[0]
    assert row["a_k_studies_contributing"] == 1
    assert row["a_k_studies_attempted"] == 2


def test_union_join_preserves_a_only_b_absent(tmp_path: Path):
    df_b = pd.DataFrame(
        [
            {
                "gene_i": "TP53",
                "gene_j": "KRAS",
                "cancer_type": "luad",
                "cohort": "exclusive",
                "b_n_samples": 100,
                "b_n_i_only": 10,
                "b_n_j_only": 10,
                "b_n_both": 5,
                "b_n_neither": 75,
                "b_select_score": 0.5,
                "b_p_wMI": 0.001,
                "b_p_ME": 0.002,
                "b_direction": "ME",
                "b_q_wMI_within_stratum": 0.005,
                "b_skip_reason": pd.NA,
            }
        ]
    )
    df_a = pd.DataFrame(
        [
            {
                "gene_i": "EGFR",
                "gene_j": "MYC",  # not in B-tier
                "cancer_type": "luad",
                "cohort": "exclusive",
                "a_stouffer_z_wMI": 3.0,
                "a_stouffer_p_wMI": 0.003,
                "a_q_wMI_within_stratum": 0.01,
                "a_k_studies_contributing": 3,
                "a_k_studies_attempted": 3,
                "a_direction_consensus_frac": 1.0,
                "a_skip_reason": pd.NA,
            }
        ]
    )
    out = mod.union_join(df_b, df_a)
    assert len(out) == 2
    egfr_myc = out[(out["gene_i"] == "EGFR") & (out["gene_j"] == "MYC")].iloc[0]
    assert pd.isna(egfr_myc["b_p_wMI"])
    assert egfr_myc["a_q_wMI_within_stratum"] == pytest.approx(0.01)


@pytest.mark.parametrize(
    "scenario,expected",
    [
        # (b_q, a_q, b_dir, a_z, k, consensus) -> expected
        ((0.05, 0.05, "ME", -3.0, 3, 1.0), "concordant"),
        ((0.05, 0.05, "ME", +3.0, 3, 0.5), "direction_conflict"),
        ((0.05, 0.5, "ME", -3.0, 3, 1.0), "b_only"),
        ((0.5, 0.05, "ME", +3.0, 3, 1.0), "a_only_b_present"),
        ((np.nan, 0.05, np.nan, +3.0, 3, 1.0), "a_only_b_absent"),
        ((0.05, 0.5, "ME", +3.0, 1, 1.0), "insufficient_a_studies"),
        ((np.nan, np.nan, np.nan, np.nan, 0, np.nan), "untested"),
    ],
)
def test_concordance_flag_categories(scenario, expected):
    b_q, a_q, b_dir, a_z, k, cons = scenario
    out = mod.compute_concordance_flag(
        pd.Series(
            {
                "b_q_wMI_within_stratum": b_q,
                "a_q_wMI_within_stratum": a_q,
                "b_direction": b_dir,
                "a_stouffer_z_wMI": a_z,
                "a_direction_consensus_frac": cons,
                "a_k_studies_contributing": k,
            }
        )
    )
    assert out == expected


def test_pathway_rollup_groups_by_pathway_pair(tmp_path: Path):
    """Stouffer over gene-pairs grouped by their pathway membership."""
    headline = pd.DataFrame(
        [
            {
                "gene_i": "TP53",
                "gene_j": "KRAS",
                "cancer_type": "luad",
                "cohort": "exclusive",
                "b_p_wMI": 0.01,
                "b_direction": "ME",
                "b_n_samples": 100,
            },
            {
                "gene_i": "TP53",
                "gene_j": "BRAF",
                "cancer_type": "luad",
                "cohort": "exclusive",
                "b_p_wMI": 0.05,
                "b_direction": "ME",
                "b_n_samples": 100,
            },
            {
                "gene_i": "EGFR",
                "gene_j": "BRAF",
                "cancer_type": "luad",
                "cohort": "exclusive",
                "b_p_wMI": 0.01,
                "b_direction": "CO",
                "b_n_samples": 100,
            },
        ]
    )
    pathway_membership = pd.DataFrame(
        {
            "symbol": ["TP53", "KRAS", "BRAF", "EGFR"],
            "pathway": ["P53", "RTK_RAS", "RTK_RAS", "RTK_RAS"],
        }
    )
    out = mod.pathway_rollup(headline, pathway_membership)
    rolled = out.set_index(["pathway_i", "pathway_j", "cancer_type", "cohort"])
    assert ("P53", "RTK_RAS", "luad", "exclusive") in rolled.index
    assert (
        rolled.loc[("P53", "RTK_RAS", "luad", "exclusive"), "n_constituent_pairs"] == 2
    )


def test_sibling_annotation_counts_partners(tmp_path: Path):
    headline = pd.DataFrame(
        [
            {
                "gene_i": "TP53",
                "gene_j": "KRAS",
                "cancer_type": "luad",
                "cohort": "exclusive",
                "b_q_wMI_within_stratum": 0.005,
                "b_a_concordance": "concordant",
            },
            {
                "gene_i": "TP53",
                "gene_j": "EGFR",
                "cancer_type": "luad",
                "cohort": "exclusive",
                "b_q_wMI_within_stratum": 0.05,
                "b_a_concordance": "b_only",
            },
            {
                "gene_i": "TP53",
                "gene_j": "BRAF",
                "cancer_type": "luad",
                "cohort": "exclusive",
                "b_q_wMI_within_stratum": 0.5,
                "b_a_concordance": "untested",
            },
        ]
    )
    out = mod.build_sibling_annotation(headline)
    tp53_luad = out[(out["symbol"] == "TP53") & (out["cancer_type"] == "luad")].iloc[0]
    assert tp53_luad["n_significant_select_partners_q01"] == 2
    assert tp53_luad["n_significant_select_partners_q01_concordant"] == 1


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
