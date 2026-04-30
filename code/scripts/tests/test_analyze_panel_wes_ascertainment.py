import pandas as pd

from analyze_panel_wes_ascertainment import (
    build_attention_regression,
    build_gene_cancer_rankings,
    compare_topk_rankings,
    panel_class_to_assay_stratum,
)


def test_panel_class_to_assay_stratum_collapses_panel_classes() -> None:
    assert panel_class_to_assay_stratum("WES") == "wes"
    assert panel_class_to_assay_stratum("MC3") == "wes"
    assert panel_class_to_assay_stratum("large_hybrid_capture") == "panel"
    assert panel_class_to_assay_stratum("small_amplicon") == "panel"


def test_build_gene_cancer_rankings_uses_callability_denominators() -> None:
    pooled_input = pd.DataFrame(
        [
            {
                "study_id": "wes1",
                "cancer_type": "A",
                "symbol": "TP53",
                "y_inclusive": 10,
                "n_inclusive": 100,
                "panel_class": "WES",
            },
            {
                "study_id": "wes2",
                "cancer_type": "A",
                "symbol": "KRAS",
                "y_inclusive": 20,
                "n_inclusive": 100,
                "panel_class": "WES",
            },
            {
                "study_id": "pan1",
                "cancer_type": "A",
                "symbol": "TP53",
                "y_inclusive": 8,
                "n_inclusive": 10,
                "panel_class": "large_hybrid_capture",
            },
            {
                "study_id": "pan1",
                "cancer_type": "A",
                "symbol": "KRAS",
                "y_inclusive": 1,
                "n_inclusive": 10,
                "panel_class": "large_hybrid_capture",
            },
        ]
    )
    annotated = pd.DataFrame(
        [
            {
                "cancer_type": "A",
                "symbol": "TP53",
                "bailey2018_driver": True,
                "cgc_tier_1": True,
            },
            {
                "cancer_type": "A",
                "symbol": "KRAS",
                "bailey2018_driver": False,
                "cgc_tier_1": False,
            },
        ]
    )

    rankings = build_gene_cancer_rankings(
        pooled_input, annotated, analysis_view="inclusive"
    )

    wes_top = rankings[
        (rankings["assay_stratum"] == "wes") & (rankings["rank"] == 1)
    ].iloc[0]
    panel_top = rankings[
        (rankings["assay_stratum"] == "panel") & (rankings["rank"] == 1)
    ].iloc[0]
    combined_top = rankings[
        (rankings["assay_stratum"] == "combined") & (rankings["rank"] == 1)
    ].iloc[0]

    assert wes_top["symbol"] == "KRAS"
    assert wes_top["rate"] == 0.20
    assert panel_top["symbol"] == "TP53"
    assert panel_top["rate"] == 0.80
    assert combined_top["symbol"] == "KRAS"
    assert combined_top["n_total"] == 110


def test_compare_topk_rankings_reports_jaccard_and_driver_recovery() -> None:
    rankings = pd.DataFrame(
        [
            {
                "assay_stratum": "wes",
                "cancer_type": "A",
                "symbol": "TP53",
                "rank": 1,
                "bailey2018_driver": True,
                "cgc_tier_1": True,
            },
            {
                "assay_stratum": "wes",
                "cancer_type": "A",
                "symbol": "KRAS",
                "rank": 2,
                "bailey2018_driver": False,
                "cgc_tier_1": False,
            },
            {
                "assay_stratum": "panel",
                "cancer_type": "A",
                "symbol": "TP53",
                "rank": 1,
                "bailey2018_driver": True,
                "cgc_tier_1": True,
            },
            {
                "assay_stratum": "panel",
                "cancer_type": "A",
                "symbol": "BRAF",
                "rank": 2,
                "bailey2018_driver": True,
                "cgc_tier_1": True,
            },
        ]
    )

    summary = compare_topk_rankings(rankings, k_values=(2,))
    row = summary[
        (summary["left_stratum"] == "wes") & (summary["right_stratum"] == "panel")
    ].iloc[0]

    assert row["intersection"] == 1
    assert row["jaccard"] == 1 / 3
    assert row["left_bailey_recovery"] == 0.5
    assert row["right_bailey_recovery"] == 1.0


def test_build_attention_regression_reports_slope_per_stratum() -> None:
    rankings = pd.DataFrame(
        [
            {"assay_stratum": "wes", "symbol": "A", "rate": 0.01},
            {"assay_stratum": "wes", "symbol": "B", "rate": 0.10},
            {"assay_stratum": "panel", "symbol": "A", "rate": 0.20},
            {"assay_stratum": "panel", "symbol": "B", "rate": 0.02},
        ]
    )
    gene_features = pd.DataFrame(
        [
            {"symbol": "A", "length": 100.0, "pubtator_mention_count": 9.0},
            {"symbol": "B", "length": 1000.0, "pubtator_mention_count": 99.0},
        ]
    )

    out = build_attention_regression(rankings, gene_features)

    assert set(out["assay_stratum"]) == {"wes", "panel"}
    assert {"beta_log_length", "beta_log_rate", "n_genes"}.issubset(out.columns)
