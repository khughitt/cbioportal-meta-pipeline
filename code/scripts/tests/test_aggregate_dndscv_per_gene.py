"""Tests for ``aggregate_dndscv_per_gene.aggregate_dndscv_per_gene``.

Per-gene pan-cancer rollup of dNdScv outputs (t131). Covers:
  - empty / all-sentinel inputs (regression for the bug surfaced 2026-04-25:
    `RuntimeError: groupby+apply produced unexpected schema ([])` when every
    per-cancer cohort hit failed_qc / below_threshold)
  - happy path: min-q across cancer types, per-gene counts, best_cancer_type
  - mixed real + sentinel rows (per-cancer reconcile emits one sentinel row per
    cancer cohort that produced no real per-gene results)
"""

import pandas as pd

from aggregate_dndscv_per_gene import POOLED_SCHEMA, aggregate_dndscv_per_gene


def _per_cancer_frame(
    rows: list[tuple[str | None, str, float | None]],
) -> pd.DataFrame:
    """Rows are ``(symbol, cancer_type, dndscv_qglobal_cv)``.

    A row with ``symbol=None`` is a sentinel (the per-cancer reconcile emits
    one when a cohort produced no real per-gene results).
    """
    return pd.DataFrame.from_records(
        [
            {
                "symbol": sym,
                "cancer_type": ct,
                "dndscv_qglobal_cv": q,
            }
            for sym, ct, q in rows
        ],
        columns=["symbol", "cancer_type", "dndscv_qglobal_cv"],
    )


def test_empty_input_list_returns_empty_with_schema() -> None:
    out = aggregate_dndscv_per_gene([])
    assert out.empty
    assert list(out.columns) == POOLED_SCHEMA


def test_all_empty_frames_returns_empty_with_schema() -> None:
    out = aggregate_dndscv_per_gene([_per_cancer_frame([]).iloc[:0], _per_cancer_frame([]).iloc[:0]])
    assert out.empty
    assert list(out.columns) == POOLED_SCHEMA


def test_all_sentinel_frames_returns_empty_with_schema() -> None:
    """Regression: every per-cancer cohort hit failed_qc or below_threshold,
    so the only rows are sentinels with symbol=NA. Previously crashed with
    `RuntimeError: groupby+apply produced unexpected schema ([])`."""
    out = aggregate_dndscv_per_gene(
        [
            _per_cancer_frame([(None, "Salivary Cancer", None)]),
            _per_cancer_frame([(None, "Breast Cancer", None)]),
            _per_cancer_frame([(None, "NSCLC", None)]),
        ]
    )
    assert out.empty
    assert list(out.columns) == POOLED_SCHEMA


def test_min_q_across_cancer_types() -> None:
    out = aggregate_dndscv_per_gene(
        [
            _per_cancer_frame([("TP53", "Breast Cancer", 0.001)]),
            _per_cancer_frame([("TP53", "NSCLC", 0.0001)]),
            _per_cancer_frame([("TP53", "Salivary Cancer", 0.5)]),
        ]
    )
    assert len(out) == 1
    row = out.iloc[0]
    assert row["symbol"] == "TP53"
    assert row["min_qglobal"] == 0.0001
    assert row["best_cancer_type"] == "NSCLC"
    assert row["n_cancers_significant_q05"] == 2  # 0.001 and 0.0001 are < 0.05
    assert row["n_cancers_significant_q01"] == 2  # both are < 0.01
    assert row["n_cancers_tested"] == 3


def test_q01_count_strict() -> None:
    """q < 0.01 should be strictly less than 0.01, not <=."""
    out = aggregate_dndscv_per_gene(
        [
            _per_cancer_frame([("FOO", "A", 0.01)]),
            _per_cancer_frame([("FOO", "B", 0.009)]),
        ]
    )
    row = out.iloc[0]
    assert row["n_cancers_significant_q05"] == 2
    assert row["n_cancers_significant_q01"] == 1  # only 0.009 is strictly < 0.01


def test_gene_with_all_nan_q_emitted_with_null_min() -> None:
    """A gene observed in per-cancer outputs but with no usable q gets a row
    with null min_qglobal, zero significance counts, NA best_cancer_type."""
    out = aggregate_dndscv_per_gene(
        [
            _per_cancer_frame([("GHOST", "A", None), ("GHOST", "B", None)]),
        ]
    )
    assert len(out) == 1
    row = out.iloc[0]
    assert row["symbol"] == "GHOST"
    assert pd.isna(row["min_qglobal"])
    assert row["n_cancers_significant_q05"] == 0
    assert row["n_cancers_tested"] == 2
    assert pd.isna(row["best_cancer_type"])


def test_mixed_real_and_sentinel_rows_filters_sentinels() -> None:
    """Per-cancer reconcile emits one sentinel row per cohort with no real
    per-gene results. Real per-gene rows from successful cohorts must still
    contribute; sentinels must be filtered."""
    out = aggregate_dndscv_per_gene(
        [
            _per_cancer_frame([("KRAS", "Pancreatic", 0.0001)]),
            _per_cancer_frame([(None, "Breast Cancer", None)]),  # sentinel
            _per_cancer_frame([("KRAS", "Lung Cancer", 0.01)]),
        ]
    )
    assert len(out) == 1
    row = out.iloc[0]
    assert row["symbol"] == "KRAS"
    assert row["min_qglobal"] == 0.0001
    assert row["best_cancer_type"] == "Pancreatic"
    assert row["n_cancers_tested"] == 2  # sentinels are NOT counted


def test_output_sorted_by_min_qglobal() -> None:
    """Most-significant genes appear first; nulls last."""
    out = aggregate_dndscv_per_gene(
        [
            _per_cancer_frame(
                [
                    ("MID", "A", 0.05),
                    ("BEST", "A", 0.0001),
                    ("WORST", "A", 0.5),
                    ("UNKNOWN", "A", None),
                ]
            )
        ]
    )
    assert list(out["symbol"]) == ["BEST", "MID", "WORST", "UNKNOWN"]
