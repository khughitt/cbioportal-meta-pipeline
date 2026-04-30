from __future__ import annotations

import pandas as pd

from compare_three_way_rankings import build_three_way_comparison


def test_dndscv_isoform_inherits_bare_driver_overlay_in_three_way_comparison() -> None:
    annotated = pd.DataFrame(
        {
            "symbol": ["CDKN2A", "TP53"],
            "cancer_type": ["Cancer A", "Cancer A"],
            "mean_inclusive": [0.10, 0.20],
            "mean_adj": [0.001, 0.002],
            "bailey2018_driver": [True, True],
            "cgc_tier_1": [True, True],
            "ch_priority_gene": [False, True],
        }
    )
    pooled = pd.DataFrame(
        {
            "symbol": ["CDKN2A.p16INK4a", "TP53"],
            "min_qglobal": [0.0, 1e-12],
            "n_cancers_significant_q05": [2, 1],
            "best_cancer_type": ["Cancer A", "Cancer A"],
        }
    )
    lengths = pd.DataFrame(
        {
            "symbol": ["CDKN2A", "TP53"],
            "length": [156, 393],
        }
    )

    out = build_three_way_comparison(
        annotated=annotated, pooled=pooled, lengths=lengths
    )
    by_symbol = out.set_index("symbol")

    assert "CDKN2A.p16INK4a" in by_symbol.index
    assert bool(by_symbol.loc["CDKN2A.p16INK4a", "bailey_driver"]) is True
    assert bool(by_symbol.loc["CDKN2A.p16INK4a", "cgc_tier_1"]) is True
    assert by_symbol.loc["CDKN2A.p16INK4a", "rank_dndscv"] == 1
    assert by_symbol.loc["CDKN2A.p16INK4a", "best_cancer_type"] == "Cancer A"
