from __future__ import annotations

import pandas as pd
import pytest

import analyze_dndscv_loso
from analyze_dndscv_loso import (
    compare_loso_rankings,
    extract_reference_sets,
    rank_dndscv_genes,
)


def _pooled(rows: list[tuple[str, float | None, int]]) -> pd.DataFrame:
    return pd.DataFrame(
        rows,
        columns=["symbol", "min_qglobal", "n_cancers_significant_q05"],
    ).assign(
        n_cancers_significant_q01=0,
        n_cancers_tested=1,
        best_cancer_type="Cancer",
    )


def test_rank_dndscv_genes_uses_canonical_t144_order() -> None:
    ranked = rank_dndscv_genes(
        _pooled(
            [
                ("ALPHA", 0.0, 1),
                ("TP53", 0.0, 4),
                ("KRAS", 0.001, 3),
                ("UNKNOWN", None, 0),
            ]
        )
    )

    assert list(ranked["symbol"]) == ["TP53", "ALPHA", "KRAS", "UNKNOWN"]
    assert list(ranked["dndscv_rank"]) == [1, 2, 3, 4]


def test_extract_reference_sets_uses_unique_symbols_in_universe() -> None:
    annotated = pd.DataFrame(
        {
            "symbol": ["TP53", "TP53", "KRAS", "APC", "NOT_IN_DNDSCV"],
            "bailey2018_driver": [True, True, False, True, True],
            "cgc_tier_1": [True, True, False, False, False],
            "cgc_tier_2": [False, False, True, True, True],
        }
    )

    refs = extract_reference_sets(annotated, universe={"TP53", "KRAS", "APC"})

    assert refs["bailey2018"] == {"TP53", "APC"}
    assert refs["cgc_tier1"] == {"TP53"}
    assert refs["cgc_tier1_or_2"] == {"TP53", "KRAS", "APC"}


def test_extract_reference_sets_maps_cdkn2a_isoform_symbols_to_bare_reference() -> None:
    annotated = pd.DataFrame(
        {
            "symbol": ["CDKN2A", "TP53"],
            "bailey2018_driver": [True, True],
            "cgc_tier_1": [True, True],
            "cgc_tier_2": [False, False],
        }
    )

    refs = extract_reference_sets(
        annotated, universe={"CDKN2A.p16INK4a", "CDKN2A.p14arf", "TP53", "CDKN2AIP"}
    )

    assert refs["bailey2018"] == {"CDKN2A.p16INK4a", "CDKN2A.p14arf", "TP53"}
    assert refs["cgc_tier1"] == {"CDKN2A.p16INK4a", "CDKN2A.p14arf", "TP53"}


def test_compare_loso_rankings_reports_topk_overlap_and_reference_recovery() -> None:
    base = _pooled(
        [
            ("TP53", 0.0, 5),
            ("KRAS", 0.0, 4),
            ("BRAF", 0.001, 2),
            ("TTN", 0.01, 1),
        ]
    )
    loo = {
        "genie": _pooled(
            [
                ("TP53", 0.0, 4),
                ("BRAF", 0.001, 2),
                ("PIK3CA", 0.002, 2),
                ("TTN", 0.02, 1),
            ]
        )
    }
    annotated = pd.DataFrame(
        {
            "symbol": ["TP53", "KRAS", "BRAF", "TTN", "PIK3CA"],
            "bailey2018_driver": [True, True, True, False, True],
            "cgc_tier_1": [True, True, True, False, True],
            "cgc_tier_2": [False, False, False, False, False],
        }
    )

    overlap, summary = compare_loso_rankings(base, loo, annotated, k_values=(3,))

    row = overlap.iloc[0]
    assert row["excluded_study_id"] == "genie"
    assert row["k"] == 3
    assert row["base_size"] == 3
    assert row["holdout_size"] == 3
    assert row["intersection"] == 2
    assert row["jaccard"] == 0.5
    assert row["base_recovery"] == 2 / 3
    assert row["holdout_recovery"] == 2 / 3
    assert row["base_bailey2018_recovery_in_top"] == 1.0
    assert row["holdout_bailey2018_recovery_in_top"] == 1.0

    summary_row = summary.iloc[0]
    assert summary_row["k"] == 3
    assert summary_row["n_iterations"] == 1
    assert summary_row["jaccard_median"] == 0.5
    assert summary_row["base_recovery_median"] == 2 / 3


def test_compare_loso_rankings_preserves_new_reference_columns(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_reference_sets(
        annotated: pd.DataFrame, universe: set[str]
    ) -> dict[str, set[str]]:
        return {"intogen2024": {"TP53"}}

    monkeypatch.setattr(
        analyze_dndscv_loso, "extract_reference_sets", fake_reference_sets
    )

    overlap, _summary = compare_loso_rankings(
        base=_pooled([("TP53", 0.0, 2), ("KRAS", 0.01, 1)]),
        loo_frames={"genie": _pooled([("TP53", 0.0, 1), ("BRAF", 0.02, 1)])},
        annotated=pd.DataFrame({"symbol": ["TP53"]}),
        k_values=(1,),
    )

    assert "base_intogen2024_recovery_in_top" in overlap.columns
    assert "holdout_intogen2024_recovery_in_top" in overlap.columns
    assert overlap.loc[0, "base_intogen2024_recovery_in_top"] == 1.0
