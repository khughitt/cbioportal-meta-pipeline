# science:code
# status: library
# science:end
"""Tests for compare_stage_stratified_gene_rates.

Pre-registered tests from doc/plans/2026-04-24-t052-cohort-stage-descriptor-design.md
(v2 §Testing): one stratum-rate fixture + four verdict outcomes.
"""

from __future__ import annotations

import pandas as pd

import compare_stage_stratified_gene_rates as mod


# ---------------------------------------------------------------------------
# Stratum rate computation (1 test)
# ---------------------------------------------------------------------------


def test_compute_stratum_rate_protein_altering_filter_only() -> None:
    samples = pd.DataFrame({"sample_id": ["s1", "s2", "s3", "s4"]})
    mutations = pd.DataFrame(
        [
            {
                "sample_id_tumor": "s1",
                "symbol": "AR",
                "variant_class": "Missense_Mutation",
                "hgvsp_short": "p.X1Y",
            },
            {
                "sample_id_tumor": "s1",
                "symbol": "AR",
                "variant_class": "Silent",
                "hgvsp_short": "p.X1Y",
            },  # filtered
            {
                "sample_id_tumor": "s2",
                "symbol": "AR",
                "variant_class": "Frame_Shift_Del",
                "hgvsp_short": "",
            },
            {
                "sample_id_tumor": "s3",
                "symbol": "TP53",
                "variant_class": "Missense_Mutation",
                "hgvsp_short": "",
            },  # wrong gene
        ]
    )
    n_in_stratum, n_panel_covers, n_mutated, rate = mod.compute_stratum_rate(
        stratum_samples=samples,
        mutations_df=mutations,
        gene="AR",
        target_variant="",
        panel_covered_sample_ids=None,
    )
    assert n_in_stratum == 4
    assert n_panel_covers == 4
    assert n_mutated == 2
    assert rate == 0.5


# ---------------------------------------------------------------------------
# Verdict logic (4 tests, one per outcome)
# ---------------------------------------------------------------------------


def test_verdict_reproduces_when_both_rates_within_3pp_of_published() -> None:
    v = mod.apply_verdict(
        observed_met=0.18,
        observed_pri=0.02,
        expected_met=0.18,
        expected_pri=0.01,
        n_met_panel=400,
        n_pri_panel=400,
    )
    assert v == "reproduces"


def test_verdict_partial_when_direction_correct_but_magnitude_off() -> None:
    v = mod.apply_verdict(
        observed_met=0.30,
        observed_pri=0.01,  # 12 pp above expected metastatic
        expected_met=0.18,
        expected_pri=0.01,
        n_met_panel=400,
        n_pri_panel=400,
    )
    assert v == "partial"


def test_verdict_fails_when_direction_wrong() -> None:
    v = mod.apply_verdict(
        observed_met=0.05,
        observed_pri=0.18,
        expected_met=0.18,
        expected_pri=0.01,
        n_met_panel=400,
        n_pri_panel=400,
    )
    assert v == "fails"


def test_verdict_underpowered_when_either_stratum_below_min_n() -> None:
    v = mod.apply_verdict(
        observed_met=0.18,
        observed_pri=0.01,
        expected_met=0.18,
        expected_pri=0.01,
        n_met_panel=10,
        n_pri_panel=400,  # below min_n=20
    )
    assert v == "underpowered"


# ---------------------------------------------------------------------------
# Closure-state aggregation (folded into the same suite, 0 extra tests beyond the 5)
# ---------------------------------------------------------------------------


def test_closure_state_validated_when_at_least_one_reproduces_or_partial_and_no_fails() -> (
    None
):
    assert (
        mod.apply_closure_state(["reproduces", "underpowered"])
        == "descriptor validated"
    )
    assert mod.apply_closure_state(["partial", "partial"]) == "descriptor validated"


def test_closure_state_needs_investigation_when_any_fails() -> None:
    assert (
        mod.apply_closure_state(["reproduces", "fails"])
        == "descriptor needs investigation"
    )


def test_closure_state_insufficient_evidence_when_all_underpowered() -> None:
    assert (
        mod.apply_closure_state(["underpowered", "underpowered"])
        == "insufficient evidence"
    )
