from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest
from click.testing import CliRunner

from analyze_dndscv_loso import rank_dndscv_genes
from analyze_genie_dndscv_influence import (
    TESTED_STATUSES,
    ThresholdMismatchError,
    assign_mechanism_class,
    build_gene_rank_delta,
    compare_gene_cancer_evidence,
    main,
    neg_log10_q,
    rank_pooled_dndscv,
    score_cancer_build_influence,
)


def _pooled(rows: list[tuple[str, float | None, int, str]]) -> pd.DataFrame:
    return pd.DataFrame(
        rows,
        columns=[
            "symbol",
            "min_qglobal",
            "n_cancers_significant_q05",
            "best_cancer_type",
        ],
    ).assign(
        n_cancers_significant_q01=0,
        n_cancers_tested=1,
    )


def test_rank_pooled_dndscv_matches_t173_rank_helper_for_ties() -> None:
    pooled = _pooled(
        [
            ("BETA", 0.001, 2, "Cancer B"),
            ("ALPHA", 0.001, 2, "Cancer A"),
            ("TP53", 0.001, 4, "Cancer T"),
            ("KRAS", 0.01, 1, "Cancer K"),
        ]
    )

    ranked = rank_pooled_dndscv(pooled)
    expected = rank_dndscv_genes(pooled)

    assert list(ranked["symbol"]) == ["TP53", "BETA", "ALPHA", "KRAS"]
    pd.testing.assert_frame_equal(ranked, expected)


def test_build_gene_rank_delta_classifies_topk_status_and_missing_ranks() -> None:
    base = _pooled(
        [
            ("TP53", 0.0, 5, "Lung Cancer"),
            ("KRAS", 0.001, 4, "Pancreatic Cancer"),
            ("BRAF", 0.002, 3, "Melanoma"),
            ("APC", 0.003, 2, "Colorectal Cancer"),
        ]
    )
    holdout = _pooled(
        [
            ("TP53", 0.0, 5, "Lung Cancer"),
            ("BRAF", 0.0005, 4, "Melanoma"),
            ("PIK3CA", 0.004, 2, "Breast Cancer"),
            ("APC", 0.005, 1, "Colorectal Cancer"),
        ]
    )

    delta = build_gene_rank_delta(base, holdout, top_k=2, diagnostic_top_n=4)
    by_symbol = delta.set_index("symbol")

    assert by_symbol.loc["TP53", "topk_status"] == "stable"
    assert by_symbol.loc["KRAS", "topk_status"] == "lost"
    assert by_symbol.loc["BRAF", "topk_status"] == "gained"
    assert by_symbol.loc["APC", "topk_status"] == "outside_top100"
    assert by_symbol.loc["TP53", "rank_delta"] == 0
    assert pd.isna(by_symbol.loc["KRAS", "holdout_rank"])
    assert pd.isna(by_symbol.loc["KRAS", "rank_delta"])
    assert pd.isna(by_symbol.loc["PIK3CA", "base_rank"])
    assert pd.isna(by_symbol.loc["PIK3CA", "rank_delta"])
    assert by_symbol.loc["BRAF", "rank_delta"] == -1
    assert by_symbol.loc["BRAF", "base_best_cancer_type"] == "Melanoma"
    assert by_symbol.loc["BRAF", "holdout_best_cancer_type"] == "Melanoma"


def test_compare_gene_cancer_evidence_classifies_support_and_missing_rows() -> None:
    base = pd.DataFrame(
        {
            "symbol": ["TP53", "BRAF", "APC", "KRAS", "NRAS"],
            "cancer_type": ["lung", "melanoma", "colon", "pancreas", "thyroid"],
            "dndscv_qglobal_cv": [0.001, 0.2, 0.01, 0.02, 0.7],
            "dndscv_significant_q05": [True, False, True, True, False],
            "dndscv_input_status": [
                "tested_significant",
                "tested_not_significant",
                "tested_significant",
                "tested_significant",
                "tested_not_significant",
            ],
            "dndscv_input_modality": ["wes"] * 5,
            "dndscv_panel_only": [False] * 5,
            "dndscv_n_samples": [100, 90, 80, 70, 60],
            "dndscv_n_variants": [1000, 900, 800, 700, 600],
            "dndscv_split_build": [False] * 5,
            "dndscv_refdb": ["hg19"] * 5,
        }
    )
    holdout = pd.DataFrame(
        {
            "symbol": ["TP53", "BRAF", "APC", "PIK3CA", "NRAS"],
            "cancer_type": ["lung", "melanoma", "colon", "breast", "thyroid"],
            "dndscv_qglobal_cv": [0.2, 0.01, 0.02, 0.001, 0.8],
            "dndscv_significant_q05": [False, True, True, True, False],
            "dndscv_input_status": [
                "tested_not_significant",
                "tested_significant",
                "tested_significant",
                "tested_significant",
                "tested_not_significant",
            ],
            "dndscv_input_modality": ["wes"] * 5,
            "dndscv_panel_only": [False] * 5,
            "dndscv_n_samples": [90, 80, 70, 50, 55],
            "dndscv_n_variants": [900, 800, 700, 500, 550],
            "dndscv_split_build": [False] * 5,
            "dndscv_refdb": ["hg19"] * 5,
        }
    )
    affected = pd.DataFrame(
        {
            "symbol": ["TP53", "BRAF", "APC", "KRAS", "PIK3CA", "NRAS"],
            "topk_status": [
                "lost",
                "gained",
                "stable",
                "lost",
                "gained",
                "outside_top100",
            ],
            "rank_delta": [10, -5, 0, None, None, 1],
        }
    )

    evidence = compare_gene_cancer_evidence(base, holdout, affected)
    support = evidence.set_index(["symbol", "cancer_type"])["support_class"]

    assert support.loc[("TP53", "lung")] == "lost_significance"
    assert support.loc[("BRAF", "melanoma")] == "gained_significance"
    assert support.loc[("APC", "colon")] == "stable_significant"
    assert support.loc[("KRAS", "pancreas")] == "full_only_tested"
    assert support.loc[("PIK3CA", "breast")] == "holdout_only_tested"
    assert support.loc[("NRAS", "thyroid")] == "stable_not_significant"
    assert {"tested_significant", "tested_not_significant"} <= TESTED_STATUSES


def test_neg_log10_q_uses_floor_for_zero_values() -> None:
    scores = neg_log10_q(pd.Series([0.0, 1e-2]), floor=1e-100)

    assert scores.tolist() == pytest.approx([100.0, 2.0])


def test_score_cancer_build_influence_counts_rank_delta_and_mechanism_classes() -> None:
    evidence = pd.DataFrame(
        {
            "symbol": ["TP53", "KRAS", "BRAF", "NRAS"],
            "cancer_type": ["lung", "lung", "melanoma", "thyroid"],
            "topk_status": ["lost", "lost", "gained", "lost"],
            "rank_delta": [10, None, -5, 1],
            "base_significant_q05": [True, True, False, False],
            "holdout_significant_q05": [False, False, True, False],
            "support_class": [
                "full_only_tested",
                "lost_significance",
                "gained_significance",
                "stable_not_significant",
            ],
            "delta_neg_log10_q": [None, -3.0, 3.0, 0.5],
        }
    )
    cohort_meta = pd.DataFrame(
        {
            "cancer_type": ["lung", "melanoma", "thyroid"],
            "build": ["hg19", "hg38", "hg19"],
            "base_n_samples": [100, 80, 60],
            "holdout_n_samples": [70, 80, 55],
            "base_n_variants": [1000, 800, 600],
            "holdout_n_variants": [600, 780, 590],
            "base_modality": ["mixed", "wes", "panel"],
            "holdout_modality": ["wes", "wes", "panel"],
            "base_panel_only": [False, False, True],
            "holdout_panel_only": [False, False, True],
            "base_below_threshold": [False, False, False],
            "holdout_below_threshold": [True, False, False],
            "base_min_samples_threshold": [30, 30, 30],
            "holdout_min_samples_threshold": [30, 30, 30],
            "base_min_variants_threshold": [50, 50, 50],
            "holdout_min_variants_threshold": [50, 50, 50],
        }
    )

    influence = score_cancer_build_influence(
        evidence, cohort_meta, q_shift_threshold=2.0
    )
    rows = influence.set_index(["cancer_type", "build"])

    assert rows.loc[("lung", "hg19"), "n_lost_top100_supported_full"] == 2
    assert rows.loc[("lung", "hg19"), "n_lost_top100_lost_significance"] == 1
    assert rows.loc[("lung", "hg19"), "sum_abs_rank_delta_supported"] == 10
    assert rows.loc[("lung", "hg19"), "delta_n_samples"] == 30
    assert rows.loc[("lung", "hg19"), "delta_n_variants"] == 400
    assert rows.loc[("lung", "hg19"), "mechanism_class"] == "mixed"
    assert rows.loc[("melanoma", "hg38"), "n_gained_top100_supported_holdout"] == 1
    assert rows.loc[("melanoma", "hg38"), "mechanism_class"] == "shared_label_shift"
    assert rows.loc[("thyroid", "hg19"), "n_affected_genes"] == 0
    assert rows.loc[("thyroid", "hg19"), "sum_abs_rank_delta_supported"] == 0
    assert rows.loc[("thyroid", "hg19"), "mechanism_class"] == "weak_or_unclear"


def test_score_cancer_build_influence_fails_on_threshold_mismatch() -> None:
    evidence = pd.DataFrame(
        {
            "symbol": ["TP53"],
            "cancer_type": ["lung"],
            "topk_status": ["lost"],
            "rank_delta": [10],
            "base_significant_q05": [True],
            "holdout_significant_q05": [False],
            "support_class": ["full_only_tested"],
            "delta_neg_log10_q": [None],
        }
    )
    cohort_meta = pd.DataFrame(
        {
            "cancer_type": ["lung"],
            "build": ["hg19"],
            "base_n_samples": [100],
            "holdout_n_samples": [70],
            "base_n_variants": [1000],
            "holdout_n_variants": [600],
            "base_modality": ["mixed"],
            "holdout_modality": ["wes"],
            "base_panel_only": [False],
            "holdout_panel_only": [False],
            "base_below_threshold": [False],
            "holdout_below_threshold": [True],
            "base_min_samples_threshold": [30],
            "holdout_min_samples_threshold": [40],
            "base_min_variants_threshold": [50],
            "holdout_min_variants_threshold": [50],
        }
    )

    with pytest.raises(ThresholdMismatchError, match="lung.*hg19"):
        score_cancer_build_influence(evidence, cohort_meta)


def test_score_cancer_build_influence_ignores_tested_only_non_significant_rows() -> (
    None
):
    evidence = pd.DataFrame(
        {
            "symbol": ["TP53", "KRAS"],
            "cancer_type": ["lung", "lung"],
            "topk_status": ["lost", "lost"],
            "rank_delta": [10, 8],
            "base_significant_q05": [True, False],
            "holdout_significant_q05": [False, False],
            "support_class": ["full_only_tested", "full_only_tested"],
            "delta_neg_log10_q": [None, None],
        }
    )
    cohort_meta = pd.DataFrame(
        {
            "cancer_type": ["lung"],
            "build": ["hg19"],
            "base_n_samples": [100],
            "holdout_n_samples": [70],
            "base_n_variants": [1000],
            "holdout_n_variants": [600],
            "base_modality": ["mixed"],
            "holdout_modality": ["wes"],
            "base_panel_only": [False],
            "holdout_panel_only": [False],
            "base_below_threshold": [False],
            "holdout_below_threshold": [True],
            "base_min_samples_threshold": [30],
            "holdout_min_samples_threshold": [30],
            "base_min_variants_threshold": [50],
            "holdout_min_variants_threshold": [50],
        }
    )

    influence = score_cancer_build_influence(evidence, cohort_meta)
    row = influence.iloc[0]

    assert row["n_affected_genes"] == 1
    assert row["sum_abs_rank_delta_supported"] == 10


@pytest.mark.parametrize(
    ("classes", "deltas", "expected"),
    [
        (["full_only_tested"], [None], "genie_only_label"),
        (["lost_significance"], [-3.0], "shared_label_shift"),
        (["full_only_tested", "lost_significance"], [None, -3.0], "mixed"),
        (["stable_not_significant"], [0.5], "weak_or_unclear"),
    ],
)
def test_assign_mechanism_class(
    classes: list[str], deltas: list[float | None], expected: str
) -> None:
    assert assign_mechanism_class(classes, deltas, q_shift_threshold=2.0) == expected


def test_cli_writes_primary_negative_control_and_summary_outputs(
    tmp_path: Path,
) -> None:
    base_root = tmp_path / "pan-cancer"
    loo_root = tmp_path / "pan-cancer-dndscv-loso"
    out_dir = tmp_path / "genie_influence"
    _write_run(
        base_root,
        pooled_rows=[
            ("TP53", 0.0, 5, "lung"),
            ("KRAS", 0.001, 4, "lung"),
            ("BRAF", 0.002, 3, "melanoma"),
        ],
        per_cancer_rows=[
            ("TP53", "lung", 0.001, True, "tested_significant"),
            ("KRAS", "lung", 0.001, True, "tested_significant"),
            ("BRAF", "melanoma", 0.2, False, "tested_not_significant"),
        ],
        meta_rows=[
            ("lung", "hg19", 100, 1000, False),
            ("melanoma", "hg19", 80, 800, False),
        ],
    )
    _write_run(
        loo_root / "exclude_genie",
        pooled_rows=[
            ("TP53", 0.0, 5, "lung"),
            ("BRAF", 0.0005, 4, "melanoma"),
            ("PIK3CA", 0.003, 2, "breast"),
        ],
        per_cancer_rows=[
            ("TP53", "lung", 0.2, False, "tested_not_significant"),
            ("BRAF", "melanoma", 0.001, True, "tested_significant"),
            ("PIK3CA", "breast", 0.001, True, "tested_significant"),
        ],
        meta_rows=[
            ("lung", "hg19", 60, 600, True),
            ("melanoma", "hg19", 80, 780, False),
            ("breast", "hg19", 50, 500, False),
        ],
    )
    _write_run(
        loo_root / "exclude_msk_met_2021",
        pooled_rows=[
            ("TP53", 0.0, 5, "lung"),
            ("KRAS", 0.001, 4, "lung"),
            ("BRAF", 0.002, 3, "melanoma"),
        ],
        per_cancer_rows=[
            ("TP53", "lung", 0.001, True, "tested_significant"),
            ("KRAS", "lung", 0.001, True, "tested_significant"),
            ("BRAF", "melanoma", 0.2, False, "tested_not_significant"),
        ],
        meta_rows=[
            ("lung", "hg19", 95, 950, False),
            ("melanoma", "hg19", 80, 790, False),
        ],
    )

    result = CliRunner().invoke(
        main,
        [
            "--base-root",
            str(base_root),
            "--loo-root",
            str(loo_root),
            "--holdout",
            "exclude_genie",
            "--negative-control",
            "exclude_msk_met_2021",
            "--out-dir",
            str(out_dir),
            "--top-k",
            "2",
            "--diagnostic-top-n",
            "3",
            "--q-floor",
            "1e-300",
            "--q-shift-threshold",
            "2.0",
            "--q-floor-sensitivity",
            "1e-100",
            "--q-shift-threshold-sensitivity",
            "1.0",
            "--q-shift-threshold-sensitivity",
            "3.0",
        ],
    )

    assert result.exit_code == 0, result.output
    assert (out_dir / "genie_gene_rank_delta.feather").exists()
    assert (out_dir / "genie_gene_cancer_evidence.feather").exists()
    assert (out_dir / "genie_cancer_build_influence.feather").exists()
    assert (
        out_dir / "negative_control_cancer_build_influence_exclude_msk_met_2021.feather"
    ).exists()
    summary = json.loads((out_dir / "genie_influence_summary.json").read_text())
    assert {
        "parameters",
        "loaded_counts",
        "topk_gene_counts",
        "top_cancer_build_attributions",
        "negative_control_comparison",
        "sensitivity",
    } <= set(summary)
    assert "exclude_msk_met_2021" in summary["negative_control_comparison"]


def _write_run(
    root: Path,
    *,
    pooled_rows: list[tuple[str, float | None, int, str]],
    per_cancer_rows: list[tuple[str, str, float, bool, str]],
    meta_rows: list[tuple[str, str, int, int, bool]],
) -> None:
    table_root = root / "summary/mut/table"
    table_root.mkdir(parents=True)
    _pooled(pooled_rows).to_feather(table_root / "dndscv_pooled.feather")

    for cancer_type, cancer_rows in pd.DataFrame(
        per_cancer_rows,
        columns=[
            "symbol",
            "cancer_type",
            "dndscv_qglobal_cv",
            "dndscv_significant_q05",
            "dndscv_input_status",
        ],
    ).groupby("cancer_type", sort=False):
        per_cancer_root = root / "summary/mut/dndscv/per_cancer" / cancer_type
        per_cancer_root.mkdir(parents=True)
        cancer_rows.assign(
            dndscv_input_modality="wes",
            dndscv_panel_only=False,
            dndscv_n_samples=50,
            dndscv_n_variants=500,
            dndscv_split_build=False,
            dndscv_refdb="hg19",
        ).reset_index(drop=True).to_feather(per_cancer_root / "genes.feather")

    for cancer_type, build, n_samples, n_variants, below_threshold in meta_rows:
        slug = f"{cancer_type}__{build}"
        meta_root = root / "summary/mut/dndscv_input" / slug
        meta_root.mkdir(parents=True)
        pd.DataFrame(
            [
                {
                    "cancer_type": cancer_type,
                    "build": build,
                    "slug": slug,
                    "n_samples": n_samples,
                    "n_variants": n_variants,
                    "modality": "wes",
                    "panel_only": False,
                    "below_threshold": below_threshold,
                    "min_samples_threshold": 30,
                    "min_variants_threshold": 50,
                }
            ]
        ).to_feather(meta_root / "cohort_meta.feather")
