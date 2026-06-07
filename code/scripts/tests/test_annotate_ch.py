# science:code
# status: library
# science:end
"""Tests for ``annotate_ch.per_study_columns`` and ``annotate_ch.annotate_ch``.

Regression guard: the saturation-context columns added upstream by
``create_combined_gene_cancer_freq_table`` (including the string
``cancer_saturation_status``) must not be treated as per-study rate columns —
a string slot otherwise breaks the matched/unmatched numeric mean.
"""

import math

import pandas as pd
import pytest

from annotate_ch import annotate_ch, per_study_columns


def test_per_study_columns_keeps_only_twinned_study_slots() -> None:
    df = pd.DataFrame(
        columns=[
            "cancer_type",
            "symbol",
            "study_a",
            "study_a_exclusive",
            "study_b",
            "study_b_exclusive",
            "mean",
            "mean_exclusive",
            "mean_inclusive",
            "n_studies_contributing",
            "n_total_samples_in_cancer_inclusive",
            "callable_sample_fraction_inclusive",
            "lawrence2014_required_n",
            "cancer_saturation_status",
        ]
    )
    assert per_study_columns(df) == ["study_a", "study_b"]


def test_annotate_ch_stratifies_and_ignores_string_metadata() -> None:
    ratio = pd.DataFrame(
        {
            "cancer_type": ["A", "A"],
            "symbol": ["TP53", "EGFR"],
            "study_a": [0.20, 0.10],
            "study_a_exclusive": [0.10, 0.05],
            "study_b": [0.40, 0.30],
            "study_b_exclusive": [0.20, 0.15],
            "cancer_saturation_status": ["saturated", "undersampled"],
        }
    )
    out = annotate_ch(ratio, matched_studies={"study_a"})

    # String metadata never enters the numeric mean (no TypeError raised).
    assert out.loc[0, "mean_matched"] == pytest.approx(0.20)  # study_a only
    assert out.loc[0, "mean_unmatched"] == pytest.approx(0.40)  # study_b only
    assert out.loc[0, "n_matched_studies"] == 1
    assert out.loc[0, "n_unmatched_studies"] == 1
    # CH-priority flag is by gene symbol.
    assert bool(out.loc[0, "ch_priority_gene"]) is True  # TP53
    assert bool(out.loc[1, "ch_priority_gene"]) is False  # EGFR


def test_annotate_ch_all_tumor_only_yields_nan_matched() -> None:
    ratio = pd.DataFrame(
        {
            "cancer_type": ["A"],
            "symbol": ["DNMT3A"],
            "study_a": [0.30],
            "study_a_exclusive": [0.15],
        }
    )
    out = annotate_ch(ratio, matched_studies=set())
    assert math.isnan(out.loc[0, "mean_matched"])
    assert out.loc[0, "n_matched_studies"] == 0
    assert out.loc[0, "mean_unmatched"] == pytest.approx(0.30)
