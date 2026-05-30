# science:code
# status: library
# science:end
"""Tests for joining pooled t077 outputs onto the canonical ratio table."""

from __future__ import annotations

import pandas as pd
import pytest

from join_gene_cancer_meta import join_pooled_meta_annotations


def test_join_pooled_meta_annotations_adds_paired_columns_without_reordering_rows() -> None:
    ratio_annotated = pd.DataFrame(
        {
            "cancer_type": ["BRCA", "LUAD"],
            "symbol": ["TP53", "EGFR"],
            "mean_inclusive": [0.20, 0.12],
            "mean_exclusive": [0.18, 0.10],
            "study_a": [0.22, 0.11],
            "study_a_exclusive": [0.20, 0.09],
            "bailey2018_driver": [True, False],
        }
    )
    pooled = pd.DataFrame(
        {
            "cancer_type": ["BRCA", "BRCA"],
            "symbol": ["TP53", "TP53"],
            "analysis_view": ["exclusive", "inclusive"],
            "pooled_logit": [0.10, 0.20],
            "pooled_rate": [0.18, 0.21],
            "pooled_ci_lo": [0.15, 0.18],
            "pooled_ci_hi": [0.21, 0.24],
            "tau2": [0.01, 0.02],
            "i2": [20.0, 25.0],
            "pi_lo": [0.10, 0.12],
            "pi_hi": [0.30, 0.35],
            "k_studies": [4, 4],
            "n_total": [300, 330],
            "y_total": [54, 69],
            "converged": [True, True],
            "status": ["ok", "ok"],
        }
    )

    out = join_pooled_meta_annotations(ratio_annotated, pooled)

    assert out["cancer_type"].tolist() == ["BRCA", "LUAD"]
    assert out["symbol"].tolist() == ["TP53", "EGFR"]
    assert list(out.columns) == [
        "cancer_type",
        "symbol",
        "mean_inclusive",
        "mean_exclusive",
        "study_a",
        "study_a_exclusive",
        "bailey2018_driver",
        "pooled_logit_inclusive",
        "pooled_logit_exclusive",
        "pooled_rate_inclusive",
        "pooled_rate_exclusive",
        "pooled_ci_lo_inclusive",
        "pooled_ci_lo_exclusive",
        "pooled_ci_hi_inclusive",
        "pooled_ci_hi_exclusive",
        "tau2_inclusive",
        "tau2_exclusive",
        "i2_inclusive",
        "i2_exclusive",
        "pi_lo_inclusive",
        "pi_lo_exclusive",
        "pi_hi_inclusive",
        "pi_hi_exclusive",
        "k_studies_inclusive",
        "k_studies_exclusive",
        "n_total_inclusive",
        "n_total_exclusive",
        "y_total_inclusive",
        "y_total_exclusive",
        "converged_inclusive",
        "converged_exclusive",
        "status_inclusive",
        "status_exclusive",
    ]

    tp53 = out.iloc[0]
    egfr = out.iloc[1]

    assert tp53["pooled_rate_inclusive"] == pytest.approx(0.21)
    assert tp53["pooled_rate_exclusive"] == pytest.approx(0.18)
    assert tp53["k_studies_inclusive"] == 4
    assert tp53["status_exclusive"] == "ok"
    assert bool(tp53["converged_inclusive"]) is True

    assert pd.isna(egfr["pooled_rate_inclusive"])
    assert pd.isna(egfr["status_exclusive"])


def test_join_pooled_meta_annotations_rejects_duplicate_view_rows() -> None:
    ratio_annotated = pd.DataFrame(
        {
            "cancer_type": ["BRCA"],
            "symbol": ["TP53"],
        }
    )
    pooled = pd.DataFrame(
        {
            "cancer_type": ["BRCA", "BRCA"],
            "symbol": ["TP53", "TP53"],
            "analysis_view": ["inclusive", "inclusive"],
            "pooled_logit": [0.10, 0.20],
            "pooled_rate": [0.18, 0.21],
            "pooled_ci_lo": [0.15, 0.18],
            "pooled_ci_hi": [0.21, 0.24],
            "tau2": [0.01, 0.02],
            "i2": [20.0, 25.0],
            "pi_lo": [0.10, 0.12],
            "pi_hi": [0.30, 0.35],
            "k_studies": [4, 4],
            "n_total": [300, 330],
            "y_total": [54, 69],
            "converged": [True, True],
            "status": ["ok", "ok"],
        }
    )

    with pytest.raises(ValueError, match="Duplicate pooled meta rows"):
        join_pooled_meta_annotations(ratio_annotated, pooled)
