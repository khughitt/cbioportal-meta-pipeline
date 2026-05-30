# science:code
# status: library
# science:end
"""Unit tests for the biological positive-control regression check."""

import pandas as pd

import check_known_biology as mod


def test_empty_headline_yields_all_skips():
    empty = pd.DataFrame(
        columns=[
            "gene_i",
            "gene_j",
            "cancer_type",
            "cohort",
            "b_n_samples",
            "b_q_wMI_within_stratum",
            "b_direction",
        ]
    )
    failures = mod.check(empty)
    assert failures == 0  # all skipped, none failed


def test_perfect_synthetic_headline_passes():
    rows = []
    for c in mod.CONTROLS:
        rows.append(
            {
                "gene_i": c.gene_a,
                "gene_j": c.gene_b,
                "cancer_type": c.cancer_type,
                "cohort": "exclusive",
                "b_n_samples": 100,
                "b_q_wMI_within_stratum": 0.001,
                "b_direction": c.expected_direction,
            }
        )
    df = pd.DataFrame(rows)
    failures = mod.check(df)
    assert failures == 0


def test_synthetic_headline_with_direction_flip_fails():
    c0 = mod.CONTROLS[0]
    rows = [
        {
            "gene_i": c0.gene_a,
            "gene_j": c0.gene_b,
            "cancer_type": c0.cancer_type,
            "cohort": "exclusive",
            "b_n_samples": 100,
            "b_q_wMI_within_stratum": 0.001,
            "b_direction": "CO" if c0.expected_direction == "ME" else "ME",
        }
    ]
    df = pd.DataFrame(rows)
    failures = mod.check(df)
    assert failures == 1
