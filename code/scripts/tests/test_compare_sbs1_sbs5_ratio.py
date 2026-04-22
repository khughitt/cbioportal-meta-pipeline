from pathlib import Path

import pandas as pd

import compare_sbs1_sbs5_ratio as ratio


def test_build_comparison_table_compares_matched_and_unmatched() -> None:
    per_sample = pd.DataFrame(
        {
            "study_id": ["tcga_mc3"] * 10 + ["msk_impact_2017"] * 10,
            "cancer_type": ["BRCA"] * 10 + ["Breast Cancer"] * 10,
            "lookup_key": ["breast"] * 20,
            "sample_name": [
                "T1",
                "T1",
                "T2",
                "T2",
                "T3",
                "T3",
                "T4",
                "T4",
                "T5",
                "T5",
                "M1",
                "M1",
                "M2",
                "M2",
                "M3",
                "M3",
                "M4",
                "M4",
                "M5",
                "M5",
            ],
            "signature": ["SBS1", "SBS5"] * 10,
            "exposure": [1.0, 5.0, 2.0, 6.0, 1.0, 4.0, 2.0, 5.0, 1.0, 4.0, 8.0, 1.0, 9.0, 2.0, 7.0, 1.0, 10.0, 2.0, 8.0, 1.0],
        }
    )

    comparison = ratio.build_comparison_table(
        per_sample,
        matched_normal_studies={"tcga_mc3"},
        min_samples_per_group=2,
        ratio_pseudocount=0.5,
    )

    assert comparison["lookup_key"].tolist() == ["breast"]
    row = comparison.iloc[0]
    assert row["matched_study_id"] == "tcga_mc3"
    assert row["unmatched_study_id"] == "msk_impact_2017"
    assert row["matched_n_samples"] == 5
    assert row["unmatched_n_samples"] == 5
    assert row["median_log10_ratio_shift"] > 0
    assert row["median_sbs1_shift"] > 0
    assert row["observed_sbs1_direction"] == "unmatched_higher"
    assert row["observed_log10_ratio_direction"] == "unmatched_higher"
    assert row["unmatched_gt_matched_sbs1_pvalue"] < 0.05
    assert row["unmatched_gt_matched_log10_ratio_pvalue"] < 0.05


def test_load_per_sample_assignments_concatenates_inputs(tmp_path: Path) -> None:
    first = tmp_path / "first.feather"
    second = tmp_path / "second.feather"
    pd.DataFrame({"study_id": ["a"], "signature": ["SBS1"], "sample_name": ["S1"], "exposure": [1.0]}).to_feather(first)
    pd.DataFrame({"study_id": ["b"], "signature": ["SBS5"], "sample_name": ["S2"], "exposure": [2.0]}).to_feather(second)

    out = ratio.load_per_sample_assignments([first, second])

    assert out["study_id"].tolist() == ["a", "b"]


def test_build_comparison_table_returns_empty_schema_when_no_pairs() -> None:
    per_sample = pd.DataFrame(
        {
            "study_id": ["tcga_mc3", "tcga_mc3"],
            "cancer_type": ["BRCA", "BRCA"],
            "lookup_key": ["breast", "breast"],
            "sample_name": ["T1", "T1"],
            "signature": ["SBS1", "SBS5"],
            "exposure": [1.0, 4.0],
        }
    )

    comparison = ratio.build_comparison_table(
        per_sample,
        matched_normal_studies={"tcga_mc3"},
        min_samples_per_group=2,
        ratio_pseudocount=0.5,
    )

    assert comparison.empty
    assert comparison.columns.tolist() == [
        "lookup_key",
        "matched_study_id",
        "unmatched_study_id",
        "matched_n_samples",
        "unmatched_n_samples",
        "matched_median_sbs1",
        "unmatched_median_sbs1",
        "matched_median_sbs5",
        "unmatched_median_sbs5",
        "matched_median_log10_ratio",
        "unmatched_median_log10_ratio",
        "median_sbs1_shift",
        "median_log10_ratio_shift",
        "observed_sbs1_direction",
        "observed_log10_ratio_direction",
        "unmatched_gt_matched_sbs1_pvalue",
        "unmatched_gt_matched_log10_ratio_pvalue",
        "sbs1_two_sided_pvalue",
        "log10_ratio_two_sided_pvalue",
    ]
