# science:code
# status: library
# science:end
"""Tests for workflow-visible QA checks on canonical mutation artifacts."""

from __future__ import annotations

import pandas as pd
import pytest

from validate_mutation_pipeline_artifacts import (
    validate_gene_cancer_annotated,
    validate_gene_cancer_pooled_bundle,
    validate_gene_cancer_pooled_input,
    validate_per_study_mutation_substrates,
    validate_samples_annotated,
)


def test_validate_per_study_mutation_substrates_accepts_clean_mutation_and_sample_tables() -> (
    None
):
    mutations = pd.DataFrame(
        {
            "symbol": ["TP53", "KRAS"],
            "sample_id_tumor": ["S1", "S2"],
            "variant_class": ["Missense_Mutation", "Nonsense_Mutation"],
            "variant_type": ["SNP", "SNP"],
        }
    )
    samples = pd.DataFrame(
        {
            "sample_id": ["S1", "S2"],
            "patient_id": ["P1", "P2"],
            "cancer_type": ["BRCA", "LUAD"],
            "cancer_type_detailed": ["Breast", "Lung"],
            "oncotree_code": ["BRCA", "LUAD"],
        }
    )

    report = validate_per_study_mutation_substrates(mutations, samples)

    assert report.failures == []
    assert any("mutation sample ids resolve" in check.name for check in report.checks)


def test_validate_per_study_mutation_substrates_rejects_unresolved_mutation_samples() -> (
    None
):
    mutations = pd.DataFrame(
        {
            "symbol": ["TP53"],
            "sample_id_tumor": ["UNKNOWN"],
            "variant_class": ["Missense_Mutation"],
            "variant_type": ["SNP"],
        }
    )
    samples = pd.DataFrame(
        {
            "sample_id": ["S1"],
            "patient_id": ["P1"],
            "cancer_type": ["BRCA"],
        }
    )

    report = validate_per_study_mutation_substrates(mutations, samples)

    assert "mutation sample ids resolve to samples.sample_id" in report.failures


def test_validate_per_study_mutation_substrates_tolerates_null_cancer_type_but_not_null_identifier() -> (
    None
):
    mutations = pd.DataFrame(
        {
            "symbol": ["TP53", "KRAS"],
            "sample_id_tumor": ["S1", "S2"],
            "variant_class": ["Missense_Mutation", "Nonsense_Mutation"],
            "variant_type": ["SNP", "SNP"],
        }
    )
    samples = pd.DataFrame(
        {
            "sample_id": ["S1", "S2"],
            "patient_id": ["P1", "P2"],
            "cancer_type": ["BRCA", None],
        }
    )

    # A null cancer_type is reported, not failed (classification label, not an identifier).
    report = validate_per_study_mutation_substrates(mutations, samples)
    assert report.failures == []
    reported = next(
        c for c in report.checks if c.name.startswith("cancer_type populated")
    )
    assert "missing cancer_type: 1 / 2" in reported.details

    # A null true identifier still fails hard.
    bad = samples.copy()
    bad.loc[1, "patient_id"] = None
    assert (
        "sample ids and patient ids are populated"
        in validate_per_study_mutation_substrates(mutations, bad).failures
    )


def test_validate_samples_annotated_checks_hypermutator_reason_vocabulary() -> None:
    samples = pd.DataFrame(
        {
            "study_id": ["study_a", "study_a"],
            "sample_id": ["S1", "S2"],
            "cancer_type": ["BRCA", "BRCA"],
            "tmb": [12.0, None],
            "hypermutation_score": [1.0, None],
            "is_hypermutator": [True, False],
            "hypermutator_reason": ["pole_hotspot", "tmb_unavailable"],
            "is_hypermutator_absolute": [True, False],
            "is_hypermutator_ultra": [False, False],
            "is_hypermutator_relative": [True, False],
        }
    )

    assert validate_samples_annotated(samples).failures == []

    bad = samples.copy()
    bad.loc[1, "hypermutator_reason"] = "silent_default"

    report = validate_samples_annotated(bad)

    assert "hypermutator_reason uses canonical vocabulary" in report.failures


def test_validate_samples_annotated_tolerates_null_cancer_type_but_not_null_identifier() -> (
    None
):
    samples = pd.DataFrame(
        {
            "study_id": ["study_a", "study_a"],
            "sample_id": ["S1", "S2"],
            "cancer_type": ["BRCA", None],
            "tmb": [12.0, None],
            "hypermutation_score": [1.0, None],
            "is_hypermutator": [True, False],
            "hypermutator_reason": ["pole_hotspot", "tmb_unavailable"],
            "is_hypermutator_absolute": [True, False],
            "is_hypermutator_ultra": [False, False],
            "is_hypermutator_relative": [True, False],
        }
    )

    # A null cancer_type is reported, not failed (classification label, not an identifier).
    report = validate_samples_annotated(samples)
    assert report.failures == []
    reported = next(
        c for c in report.checks if c.name.startswith("cancer_type populated")
    )
    assert "missing cancer_type: 1 / 2" in reported.details

    # A null true identifier still fails hard.
    bad = samples.copy()
    bad.loc[1, "sample_id"] = None
    assert (
        "samples_annotated identifiers are populated"
        in validate_samples_annotated(bad).failures
    )


def test_validate_gene_cancer_pooled_input_checks_counts_denominators_and_panel_class() -> (
    None
):
    pooled_input = pd.DataFrame(
        {
            "study_id": ["study_a"],
            "cancer_type": ["BRCA"],
            "symbol": ["TP53"],
            "y_inclusive": [2],
            "y_exclusive": [1],
            "n_inclusive": [10],
            "n_exclusive": [8],
            "panel_class": ["WES"],
            "matched_normal": [True],
        }
    )

    assert validate_gene_cancer_pooled_input(pooled_input).failures == []

    bad = pooled_input.copy()
    bad.loc[0, "y_exclusive"] = 9

    report = validate_gene_cancer_pooled_input(bad)

    assert "pooled input counts stay within denominators" in report.failures


def test_validate_gene_cancer_pooled_bundle_checks_result_views_and_rates() -> None:
    pooled = pd.DataFrame(
        {
            "cancer_type": ["BRCA", "BRCA"],
            "symbol": ["TP53", "TP53"],
            "analysis_view": ["exclusive", "inclusive"],
            "pooled_logit": [0.1, 0.2],
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
    diagnostics = pooled[
        [
            "cancer_type",
            "symbol",
            "analysis_view",
            "status",
            "k_studies",
            "n_total",
            "y_total",
        ]
    ].copy()
    diagnostics["method_used"] = "glmm"
    diagnostics["fallback_used"] = False
    diagnostics["glmm_error"] = ""
    diagnostics["reml_error"] = ""
    diagnostics["heterogeneity_state"] = "low"
    diagnostics["high_i2_threshold"] = 75.0
    diagnostics["leave_one_out_candidate"] = False

    report = validate_gene_cancer_pooled_bundle(
        pooled=pooled,
        diagnostics=diagnostics,
        leave_one_out=pd.DataFrame(),
        panel_sensitivity=pd.DataFrame(),
        placebo=pd.DataFrame(),
    )

    assert report.failures == []

    bad = pooled.copy()
    bad.loc[0, "analysis_view"] = "all_samples"

    report = validate_gene_cancer_pooled_bundle(
        pooled=bad,
        diagnostics=diagnostics,
        leave_one_out=pd.DataFrame(),
        panel_sensitivity=pd.DataFrame(),
        placebo=pd.DataFrame(),
    )

    assert (
        "pooled analysis_view uses paired inclusive/exclusive vocabulary"
        in report.failures
    )


def test_validate_gene_cancer_annotated_checks_canonical_ratio_consumer_contract() -> (
    None
):
    ratio = pd.DataFrame(
        {
            "cancer_type": ["BRCA"],
            "symbol": ["TP53"],
            "mean_inclusive": [0.20],
            "mean_exclusive": [0.18],
            "bailey2018_driver": [True],
            "cgc_tier_1": [True],
            "cgc_tier_2": [False],
            "sanchez_vega_pathway": ["p53"],
            "ch_priority_gene": [True],
            "mean_matched": [0.19],
            "mean_unmatched": [0.21],
            "n_matched_studies": [1],
            "n_unmatched_studies": [2],
            "pooled_rate_inclusive": [0.20],
            "pooled_rate_exclusive": [0.18],
            "status_inclusive": ["ok"],
            "status_exclusive": ["skipped_k"],
        }
    )

    assert validate_gene_cancer_annotated(ratio, ratio_table=True).failures == []

    bad = ratio.copy()
    bad.loc[0, "pooled_rate_exclusive"] = 1.5

    report = validate_gene_cancer_annotated(bad, ratio_table=True)

    assert "ratio-valued columns stay in [0, 1]" in report.failures


def test_validate_gene_cancer_annotated_rejects_duplicate_keys() -> None:
    table = pd.DataFrame(
        {
            "cancer_type": ["BRCA", "BRCA"],
            "symbol": ["TP53", "TP53"],
            "bailey2018_driver": [True, True],
            "cgc_tier_1": [True, True],
            "cgc_tier_2": [False, False],
            "sanchez_vega_pathway": ["p53", "p53"],
        }
    )

    report = validate_gene_cancer_annotated(table, ratio_table=False)

    assert "gene-cancer table is unique on (cancer_type, symbol)" in report.failures


def test_markdown_report_raises_when_requested() -> None:
    samples = pd.DataFrame({"sample_id": ["S1"]})
    report = validate_samples_annotated(samples)

    with pytest.raises(
        ValueError, match="samples_annotated schema has required columns"
    ):
        report.raise_for_failures()
