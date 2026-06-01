# science:code
# status: library
# science:end
"""Tests for cross-study H10 treatment impact aggregation."""

from __future__ import annotations

import pandas as pd
import pytest

from create_h10_treatment_impact_table import (
    compute_h10_treatment_impact_table,
)


COHORT_VIEWS = (
    "all_samples",
    "no_detected_treatment_signal",
    "confirmed_naive_or_pretreatment",
    "broad_treatment_excluded",
    "mutagenic_treatment_excluded_primary",
    "mutagenic_treatment_excluded_with_pdx_sensitivity",
)


def test_impact_table_reports_means_deltas_ranks_and_contrast_specific_power() -> None:
    frames = [
        (
            "study_a_primary_treated",
            _frame(
                {
                    "TP53": {
                        "all_samples": (6, 10),
                        "no_detected_treatment_signal": (0, 0),
                        "confirmed_naive_or_pretreatment": (0, 0),
                        "broad_treatment_excluded": (0, 0),
                        "mutagenic_treatment_excluded_primary": (0, 0),
                        "mutagenic_treatment_excluded_with_pdx_sensitivity": (0, 0),
                    },
                    "ERCC2": {
                        "all_samples": (1, 10),
                        "no_detected_treatment_signal": (0, 0),
                        "confirmed_naive_or_pretreatment": (0, 0),
                        "broad_treatment_excluded": (0, 0),
                        "mutagenic_treatment_excluded_primary": (0, 0),
                        "mutagenic_treatment_excluded_with_pdx_sensitivity": (0, 0),
                    },
                }
            ),
        ),
        (
            "study_b_no_signal",
            _frame(
                {
                    "TP53": {
                        "all_samples": (1, 10),
                        "no_detected_treatment_signal": (1, 10),
                        "confirmed_naive_or_pretreatment": (0, 0),
                        "broad_treatment_excluded": (1, 10),
                        "mutagenic_treatment_excluded_primary": (1, 10),
                        "mutagenic_treatment_excluded_with_pdx_sensitivity": (1, 10),
                    },
                    "ERCC2": {
                        "all_samples": (4, 10),
                        "no_detected_treatment_signal": (4, 10),
                        "confirmed_naive_or_pretreatment": (0, 0),
                        "broad_treatment_excluded": (4, 10),
                        "mutagenic_treatment_excluded_primary": (4, 10),
                        "mutagenic_treatment_excluded_with_pdx_sensitivity": (4, 10),
                    },
                }
            ),
        ),
        (
            "study_c_confirmed_naive",
            _frame(
                {
                    "TP53": {
                        "all_samples": (2, 10),
                        "no_detected_treatment_signal": (2, 10),
                        "confirmed_naive_or_pretreatment": (2, 10),
                        "broad_treatment_excluded": (2, 10),
                        "mutagenic_treatment_excluded_primary": (2, 10),
                        "mutagenic_treatment_excluded_with_pdx_sensitivity": (2, 10),
                    },
                    "ERCC2": {
                        "all_samples": (3, 10),
                        "no_detected_treatment_signal": (3, 10),
                        "confirmed_naive_or_pretreatment": (3, 10),
                        "broad_treatment_excluded": (3, 10),
                        "mutagenic_treatment_excluded_primary": (3, 10),
                        "mutagenic_treatment_excluded_with_pdx_sensitivity": (3, 10),
                    },
                }
            ),
        ),
    ]

    out = compute_h10_treatment_impact_table(frames)

    tp53 = _row(out, "Bladder Cancer", "TP53")
    assert tp53["mean_all_samples"] == pytest.approx(0.3)
    assert tp53["mean_no_detected_treatment_signal"] == pytest.approx(0.15)
    assert tp53["delta_no_detected_contrast"] == pytest.approx(0.15)
    assert tp53["delta_mutagenic_primary"] == pytest.approx(0.15)
    assert tp53["rank_all_samples"] == 1
    assert tp53["rank_no_detected_treatment_signal"] == 2
    assert tp53["rank_delta_no_detected_contrast"] == -1
    assert tp53["power_status_no_detected_contrast"] == "interpretable"
    assert (
        tp53["power_status_confirmed_naive_contrast"] == "underpowered_non_arbitrating"
    )
    assert tp53["power_status_mutagenic_primary"] == "interpretable"
    assert tp53["n_studies_all_samples"] == 3
    assert tp53["n_studies_no_detected_treatment_signal"] == 2
    assert tp53["n_samples_all_samples"] == 30
    assert tp53["n_samples_no_detected_treatment_signal"] == 20
    assert tp53["n_samples_removed_no_detected_contrast"] == 10
    assert tp53["num_removed_no_detected_contrast"] == 6

    ercc2 = _row(out, "Bladder Cancer", "ERCC2")
    assert ercc2["rank_all_samples"] == 2
    assert ercc2["rank_no_detected_treatment_signal"] == 1
    assert ercc2["rank_delta_no_detected_contrast"] == 1
    assert ercc2["delta_no_detected_contrast"] < 0


def test_no_contrast_status_wins_when_samples_do_not_change() -> None:
    frames = [
        (
            "study_a",
            _frame(
                {
                    "TP53": {
                        "all_samples": (1, 10),
                        "no_detected_treatment_signal": (1, 10),
                        "confirmed_naive_or_pretreatment": (0, 0),
                        "broad_treatment_excluded": (1, 10),
                        "mutagenic_treatment_excluded_primary": (1, 10),
                        "mutagenic_treatment_excluded_with_pdx_sensitivity": (1, 10),
                    }
                }
            ),
        ),
        (
            "study_b",
            _frame(
                {
                    "TP53": {
                        "all_samples": (2, 10),
                        "no_detected_treatment_signal": (2, 10),
                        "confirmed_naive_or_pretreatment": (0, 0),
                        "broad_treatment_excluded": (2, 10),
                        "mutagenic_treatment_excluded_primary": (2, 10),
                        "mutagenic_treatment_excluded_with_pdx_sensitivity": (2, 10),
                    }
                }
            ),
        ),
    ]

    out = compute_h10_treatment_impact_table(frames)

    tp53 = _row(out, "Bladder Cancer", "TP53")
    assert tp53["power_status_no_detected_contrast"] == "no_contrast"
    assert tp53["power_status_confirmed_naive_contrast"] == "no_contrast"
    assert tp53["power_status_mutagenic_primary"] == "no_contrast"


def _frame(gene_counts: dict[str, dict[str, tuple[int, int]]]) -> pd.DataFrame:
    rows = []
    for symbol, view_counts in gene_counts.items():
        for cohort_view in COHORT_VIEWS:
            num, n_samples = view_counts[cohort_view]
            ratio = num / n_samples if n_samples else float("nan")
            rows.append(
                {
                    "cancer_type": "Bladder Cancer",
                    "symbol": symbol,
                    "cohort_view": cohort_view,
                    "num": num,
                    "n_samples": n_samples,
                    "ratio": ratio,
                    "n_samples_hypermutator_excluded": n_samples,
                    "num_hypermutator_excluded": num,
                    "ratio_hypermutator_excluded": ratio,
                }
            )
    return pd.DataFrame(rows)


def _row(df: pd.DataFrame, cancer_type: str, symbol: str) -> pd.Series:
    match = df.loc[(df["cancer_type"] == cancer_type) & (df["symbol"] == symbol)]
    assert len(match) == 1
    return match.iloc[0]
