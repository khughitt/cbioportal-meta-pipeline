"""Tests for ``annotate_hypermutators.annotate_hypermutators``.

Specification is task 6 of the t081 hypermutator / TMB annotation plan at
``doc/plans/2026-04-13-t081-hypermutator-annotation-pipeline-plan.md``
(the canonical 8-row decision table; F4 fix). Also covers the dual
absolute/relative/ultra hypermutator flags introduced by task t089.
"""

import math

import numpy as np
import pandas as pd

from annotate_hypermutators import annotate_hypermutators


def _samples_tmb(rows: list[dict]) -> pd.DataFrame:
    defaults = {
        "study_id": "s",
        "cancer_type": "Test Cancer",
        "tmb": 5.0,
        "tmb_log10": math.log10(6.0),
        "panel_callable_mb": 1.0,
        "tmb_source": "bed_sum",
        "msi_type": pd.NA,
        "msi_score": np.nan,
        "pole_hotspot_detected": False,
        "pold1_hotspot_detected": False,
    }
    return pd.DataFrame([{**defaults, **r} for r in rows])


def _samples_gmm(rows: list[dict]) -> pd.DataFrame:
    defaults = {
        "cancer_type": "Test Cancer",
        "tmb_log10": math.log10(6.0),
        "tmb_zscore_within_cancer": 0.0,
        "gmm_posterior_upper": np.nan,
        "is_hypermutator_gmm": False,
    }
    return pd.DataFrame([{**defaults, **r} for r in rows])


def _per_cancer(rows: list[dict]) -> pd.DataFrame:
    defaults = {
        "n_samples": 500,
        "bic_1": 0.0,
        "bic_2": 0.0,
        "delta_bic": 0.0,
        "dip_pvalue": 0.5,
        "fit_quality": "single_mode",
        # log10(20) = 1.30 — well above the default composite floor of log10(10) = 1.0,
        # so any test that wants its bimodal cancer-type to pass the upper-mode gate can
        # rely on this default. Tests that want the gate to fail set this explicitly.
        "upper_component_mean": math.log10(20.0),
        "lower_component_mean": math.log10(1.0),
    }
    return pd.DataFrame([{**defaults, **r} for r in rows])


# --- 8-row decision table ----------------------------------------------------


def test_row1_pole_hotspot_forces_true_regardless_of_tmb() -> None:
    # Even a sample with tmb = 1.0 and no other signal is a hypermutator if POLE hotspot fires.
    out = annotate_hypermutators(
        samples_tmb_combined=_samples_tmb(
            [{"sample_id": "S1", "tmb": 1.0, "pole_hotspot_detected": True}]
        ),
        samples_gmm_flagged=_samples_gmm([{"sample_id": "S1"}]),
        per_cancer_gmm_fits=_per_cancer([{"cancer_type": "Test Cancer"}]),
    )
    row = out.loc[out["sample_id"] == "S1"].iloc[0]
    assert row["is_hypermutator"]
    assert row["hypermutation_score"] == 1.0
    assert row["hypermutator_reason"] == "pole_hotspot"


def test_row2_pold1_hotspot_forces_true() -> None:
    out = annotate_hypermutators(
        samples_tmb_combined=_samples_tmb(
            [{"sample_id": "S1", "tmb": 1.0, "pold1_hotspot_detected": True}]
        ),
        samples_gmm_flagged=_samples_gmm([{"sample_id": "S1"}]),
        per_cancer_gmm_fits=_per_cancer([{"cancer_type": "Test Cancer"}]),
    )
    row = out.loc[out["sample_id"] == "S1"].iloc[0]
    assert row["is_hypermutator"]
    assert row["hypermutation_score"] == 1.0
    assert row["hypermutator_reason"] == "pold1_hotspot"


def test_row3_msi_h_forces_true() -> None:
    out = annotate_hypermutators(
        samples_tmb_combined=_samples_tmb(
            [{"sample_id": "S1", "tmb": 1.0, "msi_type": "MSI-H"}]
        ),
        samples_gmm_flagged=_samples_gmm([{"sample_id": "S1"}]),
        per_cancer_gmm_fits=_per_cancer([{"cancer_type": "Test Cancer"}]),
    )
    row = out.loc[out["sample_id"] == "S1"].iloc[0]
    assert row["is_hypermutator"]
    assert row["hypermutator_reason"] == "msi_h"


def test_row4_gmm_bimodal_upper_posterior_flags_true() -> None:
    # Sample tmb 15 mut/Mb (>= floor) and the default upper_component_mean log10(20)
    # (>= floor); both gates pass.
    out = annotate_hypermutators(
        samples_tmb_combined=_samples_tmb([{"sample_id": "S1", "tmb": 15.0}]),
        samples_gmm_flagged=_samples_gmm(
            [{"sample_id": "S1", "gmm_posterior_upper": 0.92}]
        ),
        per_cancer_gmm_fits=_per_cancer(
            [{"cancer_type": "Test Cancer", "fit_quality": "bimodal"}]
        ),
    )
    row = out.loc[out["sample_id"] == "S1"].iloc[0]
    assert row["is_hypermutator"]
    assert row["hypermutation_score"] == 0.92
    assert row["hypermutator_reason"] == "gmm_upper_mode"


def test_row5_gmm_bimodal_lower_posterior_flags_false() -> None:
    out = annotate_hypermutators(
        samples_tmb_combined=_samples_tmb([{"sample_id": "S1"}]),
        samples_gmm_flagged=_samples_gmm(
            [{"sample_id": "S1", "gmm_posterior_upper": 0.2}]
        ),
        per_cancer_gmm_fits=_per_cancer(
            [{"cancer_type": "Test Cancer", "fit_quality": "bimodal"}]
        ),
    )
    row = out.loc[out["sample_id"] == "S1"].iloc[0]
    assert not row["is_hypermutator"]
    assert row["hypermutation_score"] == 0.2
    assert row["hypermutator_reason"] == "gmm_lower_mode"


def test_row6_gmm_unavailable_high_zscore_flags_true_with_piecewise_score() -> None:
    # zscore = 3.0 -> score = min(1.0, (3.0 - 1.5)/1.5 + 0.5) = min(1.0, 1.5) = 1.0
    out = annotate_hypermutators(
        samples_tmb_combined=_samples_tmb([{"sample_id": "S1"}]),
        samples_gmm_flagged=_samples_gmm(
            [{"sample_id": "S1", "tmb_zscore_within_cancer": 3.0}]
        ),
        per_cancer_gmm_fits=_per_cancer(
            [{"cancer_type": "Test Cancer", "fit_quality": "single_mode"}]
        ),
    )
    row = out.loc[out["sample_id"] == "S1"].iloc[0]
    assert row["is_hypermutator"]
    assert row["hypermutation_score"] == 1.0
    assert row["hypermutator_reason"] == "zscore_fallback_high"


def test_row6_gmm_unavailable_mid_high_zscore_piecewise() -> None:
    # zscore = 1.8 -> score = (1.8 - 1.5)/1.5 + 0.5 = 0.2 + 0.5 = 0.7
    out = annotate_hypermutators(
        samples_tmb_combined=_samples_tmb([{"sample_id": "S1"}]),
        samples_gmm_flagged=_samples_gmm(
            [{"sample_id": "S1", "tmb_zscore_within_cancer": 1.8}]
        ),
        per_cancer_gmm_fits=_per_cancer(
            [{"cancer_type": "Test Cancer", "fit_quality": "not_bimodal"}]
        ),
    )
    row = out.loc[out["sample_id"] == "S1"].iloc[0]
    assert row["is_hypermutator"]
    assert row["hypermutation_score"] == pytest_approx(0.7)
    assert row["hypermutator_reason"] == "zscore_fallback_high"


def test_row7_gmm_unavailable_low_zscore_flags_false() -> None:
    # zscore = 0.6 -> score = max(0.0, 0.6/3.0) = 0.2
    out = annotate_hypermutators(
        samples_tmb_combined=_samples_tmb([{"sample_id": "S1"}]),
        samples_gmm_flagged=_samples_gmm(
            [{"sample_id": "S1", "tmb_zscore_within_cancer": 0.6}]
        ),
        per_cancer_gmm_fits=_per_cancer(
            [{"cancer_type": "Test Cancer", "fit_quality": "insufficient_data"}]
        ),
    )
    row = out.loc[out["sample_id"] == "S1"].iloc[0]
    assert not row["is_hypermutator"]
    assert row["hypermutation_score"] == pytest_approx(0.2)
    assert row["hypermutator_reason"] == "zscore_fallback_low"


def test_row7_gmm_unavailable_negative_zscore_score_clamps_to_zero() -> None:
    out = annotate_hypermutators(
        samples_tmb_combined=_samples_tmb([{"sample_id": "S1"}]),
        samples_gmm_flagged=_samples_gmm(
            [{"sample_id": "S1", "tmb_zscore_within_cancer": -2.0}]
        ),
        per_cancer_gmm_fits=_per_cancer(
            [{"cancer_type": "Test Cancer", "fit_quality": "single_mode"}]
        ),
    )
    row = out.loc[out["sample_id"] == "S1"].iloc[0]
    assert not row["is_hypermutator"]
    assert row["hypermutation_score"] == 0.0
    assert row["hypermutator_reason"] == "zscore_fallback_low"


def test_row8_tmb_nan_flags_false_with_nan_score() -> None:
    out = annotate_hypermutators(
        samples_tmb_combined=_samples_tmb(
            [{"sample_id": "S1", "tmb": np.nan, "tmb_log10": np.nan}]
        ),
        samples_gmm_flagged=_samples_gmm([{"sample_id": "S1"}]),
        per_cancer_gmm_fits=_per_cancer([{"cancer_type": "Test Cancer"}]),
    )
    row = out.loc[out["sample_id"] == "S1"].iloc[0]
    assert not row["is_hypermutator"]
    assert pd.isna(row["hypermutation_score"])
    assert row["hypermutator_reason"] == "tmb_unavailable"


# --- t105: composite-min-absolute-tmb gates on row 4 ------------------------


def test_row4_demoted_when_upper_component_mean_below_floor() -> None:
    """BRCA-like case: GMM finds bimodality but the upper mode mean is well below
    the absolute hypermutator floor. Row 4 must demote to ``gmm_upper_mode_below_floor``
    (False) regardless of how high the per-sample TMB is.
    """
    out = annotate_hypermutators(
        samples_tmb_combined=_samples_tmb([{"sample_id": "S1", "tmb": 50.0}]),
        samples_gmm_flagged=_samples_gmm(
            [{"sample_id": "S1", "gmm_posterior_upper": 0.95}]
        ),
        per_cancer_gmm_fits=_per_cancer(
            [
                {
                    "cancer_type": "Test Cancer",
                    "fit_quality": "bimodal",
                    # log10(2.5) = 0.40, below default floor of log10(10) = 1.0
                    "upper_component_mean": math.log10(2.5),
                }
            ]
        ),
    )
    row = out.loc[out["sample_id"] == "S1"].iloc[0]
    assert not row["is_hypermutator"]
    assert row["hypermutator_reason"] == "gmm_upper_mode_below_floor"
    # Score still reports the GMM posterior so downstream consumers can see why.
    assert row["hypermutation_score"] == 0.95


def test_row4_demoted_when_sample_tmb_below_floor_even_if_mode_passes() -> None:
    """SKCM-like case: the cohort's upper-mode mean is high enough to pass the
    per-mode gate, but THIS sample's own TMB is below the absolute floor — so
    even though it sits in the upper-posterior bucket, it isn't biologically
    a hypermutator. Demote.
    """
    out = annotate_hypermutators(
        samples_tmb_combined=_samples_tmb([{"sample_id": "S1", "tmb": 4.0}]),
        samples_gmm_flagged=_samples_gmm(
            [{"sample_id": "S1", "gmm_posterior_upper": 0.85}]
        ),
        per_cancer_gmm_fits=_per_cancer(
            [
                {
                    "cancer_type": "Test Cancer",
                    "fit_quality": "bimodal",
                    "upper_component_mean": math.log10(15.0),
                }
            ]
        ),
    )
    row = out.loc[out["sample_id"] == "S1"].iloc[0]
    assert not row["is_hypermutator"]
    assert row["hypermutator_reason"] == "gmm_upper_mode_below_floor"


def test_row4_promoted_when_both_gates_pass() -> None:
    """UCEC-like case: upper-mode mean high (24 mut/Mb) AND sample TMB high
    (50 mut/Mb). Both gates pass; sample is composite-True.
    """
    out = annotate_hypermutators(
        samples_tmb_combined=_samples_tmb([{"sample_id": "S1", "tmb": 50.0}]),
        samples_gmm_flagged=_samples_gmm(
            [{"sample_id": "S1", "gmm_posterior_upper": 0.92}]
        ),
        per_cancer_gmm_fits=_per_cancer(
            [
                {
                    "cancer_type": "Test Cancer",
                    "fit_quality": "bimodal",
                    "upper_component_mean": math.log10(24.0),
                }
            ]
        ),
    )
    row = out.loc[out["sample_id"] == "S1"].iloc[0]
    assert row["is_hypermutator"]
    assert row["hypermutator_reason"] == "gmm_upper_mode"


def test_composite_min_absolute_tmb_is_configurable() -> None:
    """A run with a stricter floor (50 mut/Mb) demotes a sample at 15 mut/Mb
    that the default floor (10 mut/Mb) would have promoted.
    """
    out_default = annotate_hypermutators(
        samples_tmb_combined=_samples_tmb([{"sample_id": "S1", "tmb": 15.0}]),
        samples_gmm_flagged=_samples_gmm(
            [{"sample_id": "S1", "gmm_posterior_upper": 0.92}]
        ),
        per_cancer_gmm_fits=_per_cancer(
            [
                {
                    "cancer_type": "Test Cancer",
                    "fit_quality": "bimodal",
                    "upper_component_mean": math.log10(20.0),
                }
            ]
        ),
    )
    out_strict = annotate_hypermutators(
        samples_tmb_combined=_samples_tmb([{"sample_id": "S1", "tmb": 15.0}]),
        samples_gmm_flagged=_samples_gmm(
            [{"sample_id": "S1", "gmm_posterior_upper": 0.92}]
        ),
        per_cancer_gmm_fits=_per_cancer(
            [
                {
                    "cancer_type": "Test Cancer",
                    "fit_quality": "bimodal",
                    "upper_component_mean": math.log10(20.0),
                }
            ]
        ),
        composite_min_absolute_tmb=50.0,
    )
    assert out_default.iloc[0]["is_hypermutator"]
    assert out_default.iloc[0]["hypermutator_reason"] == "gmm_upper_mode"
    assert not out_strict.iloc[0]["is_hypermutator"]
    assert out_strict.iloc[0]["hypermutator_reason"] == "gmm_upper_mode_below_floor"


def test_clinical_rules_pole_pold1_msi_unaffected_by_floor() -> None:
    """Rows 1-3 (POLE / POLD1 / MSI-H) take precedence regardless of TMB floor."""
    out = annotate_hypermutators(
        samples_tmb_combined=_samples_tmb(
            [
                {"sample_id": "POLE", "tmb": 1.0, "pole_hotspot_detected": True},
                {"sample_id": "POLD1", "tmb": 1.0, "pold1_hotspot_detected": True},
                {"sample_id": "MSI", "tmb": 1.0, "msi_type": "MSI-H"},
            ]
        ),
        samples_gmm_flagged=_samples_gmm(
            [{"sample_id": "POLE"}, {"sample_id": "POLD1"}, {"sample_id": "MSI"}]
        ),
        per_cancer_gmm_fits=_per_cancer([{"cancer_type": "Test Cancer"}]),
        composite_min_absolute_tmb=1000.0,
    )
    by_id = out.set_index("sample_id")
    assert bool(by_id.loc["POLE", "is_hypermutator"])
    assert by_id.loc["POLE", "hypermutator_reason"] == "pole_hotspot"
    assert bool(by_id.loc["POLD1", "is_hypermutator"])
    assert by_id.loc["POLD1", "hypermutator_reason"] == "pold1_hotspot"
    assert bool(by_id.loc["MSI", "is_hypermutator"])
    assert by_id.loc["MSI", "hypermutator_reason"] == "msi_h"


# --- priority enforcement ---------------------------------------------------


def test_pole_priority_over_pold1() -> None:
    out = annotate_hypermutators(
        samples_tmb_combined=_samples_tmb(
            [
                {
                    "sample_id": "S1",
                    "pole_hotspot_detected": True,
                    "pold1_hotspot_detected": True,
                }
            ]
        ),
        samples_gmm_flagged=_samples_gmm([{"sample_id": "S1"}]),
        per_cancer_gmm_fits=_per_cancer([{"cancer_type": "Test Cancer"}]),
    )
    row = out.loc[out["sample_id"] == "S1"].iloc[0]
    assert row["hypermutator_reason"] == "pole_hotspot"


def test_pold1_priority_over_msi_h() -> None:
    out = annotate_hypermutators(
        samples_tmb_combined=_samples_tmb(
            [
                {
                    "sample_id": "S1",
                    "pold1_hotspot_detected": True,
                    "msi_type": "MSI-H",
                }
            ]
        ),
        samples_gmm_flagged=_samples_gmm([{"sample_id": "S1"}]),
        per_cancer_gmm_fits=_per_cancer([{"cancer_type": "Test Cancer"}]),
    )
    row = out.loc[out["sample_id"] == "S1"].iloc[0]
    assert row["hypermutator_reason"] == "pold1_hotspot"


def test_msi_h_priority_over_gmm() -> None:
    out = annotate_hypermutators(
        samples_tmb_combined=_samples_tmb([{"sample_id": "S1", "msi_type": "MSI-H"}]),
        samples_gmm_flagged=_samples_gmm(
            [{"sample_id": "S1", "gmm_posterior_upper": 0.1}]
        ),
        per_cancer_gmm_fits=_per_cancer(
            [{"cancer_type": "Test Cancer", "fit_quality": "bimodal"}]
        ),
    )
    row = out.loc[out["sample_id"] == "S1"].iloc[0]
    # MSI-H wins despite low GMM posterior.
    assert row["is_hypermutator"]
    assert row["hypermutator_reason"] == "msi_h"


# --- dual flags (t089) ------------------------------------------------------


def test_absolute_flag_uses_campbell_2017_ten_mut_per_mb_cutoff() -> None:
    out = annotate_hypermutators(
        samples_tmb_combined=_samples_tmb(
            [
                {"sample_id": "BELOW", "tmb": 9.99},
                {"sample_id": "AT", "tmb": 10.0},
                {"sample_id": "ABOVE", "tmb": 12.0},
            ]
        ),
        samples_gmm_flagged=_samples_gmm(
            [
                {"sample_id": "BELOW"},
                {"sample_id": "AT"},
                {"sample_id": "ABOVE"},
            ]
        ),
        per_cancer_gmm_fits=_per_cancer([{"cancer_type": "Test Cancer"}]),
    )
    flags = dict(zip(out["sample_id"], out["is_hypermutator_absolute"]))
    assert flags == {"BELOW": False, "AT": True, "ABOVE": True}


def test_ultra_flag_uses_campbell_2017_hundred_mut_per_mb_cutoff() -> None:
    out = annotate_hypermutators(
        samples_tmb_combined=_samples_tmb(
            [
                {"sample_id": "BELOW", "tmb": 99.0},
                {"sample_id": "AT", "tmb": 100.0},
                {"sample_id": "ABOVE", "tmb": 500.0},
            ]
        ),
        samples_gmm_flagged=_samples_gmm(
            [
                {"sample_id": "BELOW"},
                {"sample_id": "AT"},
                {"sample_id": "ABOVE"},
            ]
        ),
        per_cancer_gmm_fits=_per_cancer([{"cancer_type": "Test Cancer"}]),
    )
    flags = dict(zip(out["sample_id"], out["is_hypermutator_ultra"]))
    assert flags == {"BELOW": False, "AT": True, "ABOVE": True}


def test_relative_flag_uses_per_histology_top_20_percent() -> None:
    # 20 samples in one cancer type — top 20% = 4 highest-TMB samples.
    rows_tmb = [
        {"sample_id": f"S{i:02d}", "cancer_type": "C1", "tmb": float(i)}
        for i in range(20)
    ]
    out = annotate_hypermutators(
        samples_tmb_combined=_samples_tmb(rows_tmb),
        samples_gmm_flagged=_samples_gmm(
            [{"sample_id": f"S{i:02d}", "cancer_type": "C1"} for i in range(20)]
        ),
        per_cancer_gmm_fits=_per_cancer([{"cancer_type": "C1"}]),
    )
    relative = out.loc[out["is_hypermutator_relative"], "sample_id"].tolist()
    # Top-4 by TMB are S19, S18, S17, S16.
    assert set(relative) == {"S16", "S17", "S18", "S19"}


def test_relative_flag_is_per_cancer_type_not_pan_cancer() -> None:
    # Two cancer types, 10 samples each. Top 20% = 2 per cancer type.
    rows = []
    for cancer in ["C1", "C2"]:
        for i in range(10):
            rows.append(
                {
                    "sample_id": f"{cancer}_S{i:02d}",
                    "cancer_type": cancer,
                    "tmb": float(i),
                }
            )
    out = annotate_hypermutators(
        samples_tmb_combined=_samples_tmb(rows),
        samples_gmm_flagged=_samples_gmm(
            [
                {"sample_id": r["sample_id"], "cancer_type": r["cancer_type"]}
                for r in rows
            ]
        ),
        per_cancer_gmm_fits=_per_cancer([{"cancer_type": "C1"}, {"cancer_type": "C2"}]),
    )
    relative = out.loc[out["is_hypermutator_relative"]]
    c1_flagged = set(relative.loc[relative["cancer_type"] == "C1", "sample_id"])
    c2_flagged = set(relative.loc[relative["cancer_type"] == "C2", "sample_id"])
    assert c1_flagged == {"C1_S08", "C1_S09"}
    assert c2_flagged == {"C2_S08", "C2_S09"}


# --- schema / preservation --------------------------------------------------


def test_output_preserves_sample_level_columns_from_input() -> None:
    out = annotate_hypermutators(
        samples_tmb_combined=_samples_tmb([{"sample_id": "S1"}]),
        samples_gmm_flagged=_samples_gmm([{"sample_id": "S1"}]),
        per_cancer_gmm_fits=_per_cancer([{"cancer_type": "Test Cancer"}]),
    )
    for col in (
        "study_id",
        "sample_id",
        "cancer_type",
        "tmb",
        "tmb_log10",
        "panel_callable_mb",
        "msi_type",
        "pole_hotspot_detected",
        "pold1_hotspot_detected",
    ):
        assert col in out.columns, f"missing input column {col!r}"


def test_output_has_expected_new_columns() -> None:
    out = annotate_hypermutators(
        samples_tmb_combined=_samples_tmb([{"sample_id": "S1"}]),
        samples_gmm_flagged=_samples_gmm([{"sample_id": "S1"}]),
        per_cancer_gmm_fits=_per_cancer([{"cancer_type": "Test Cancer"}]),
    )
    for col in (
        "hypermutation_score",
        "is_hypermutator",
        "hypermutator_reason",
        "is_hypermutator_absolute",
        "is_hypermutator_ultra",
        "is_hypermutator_relative",
        "gmm_posterior_upper",
        "tmb_zscore_within_cancer",
    ):
        assert col in out.columns, f"missing output column {col!r}"


def test_one_row_per_input_sample() -> None:
    out = annotate_hypermutators(
        samples_tmb_combined=_samples_tmb(
            [
                {"sample_id": "S1"},
                {"sample_id": "S2"},
                {"sample_id": "S3"},
            ]
        ),
        samples_gmm_flagged=_samples_gmm(
            [{"sample_id": "S1"}, {"sample_id": "S2"}, {"sample_id": "S3"}]
        ),
        per_cancer_gmm_fits=_per_cancer([{"cancer_type": "Test Cancer"}]),
    )
    assert len(out) == 3
    assert len(set(out["sample_id"])) == 3


# --- helpers ----------------------------------------------------------------


def pytest_approx(expected: float, rel: float = 1e-6) -> object:
    """Tiny shim so the above tests don't need to import pytest just for approx."""
    import pytest

    return pytest.approx(expected, rel=rel)


# --- Regression: missing msi_type column ---------------------------------- #
#
# Caught in t131 full pan-cancer-dndscv run 2026-04-25: not every cBioPortal
# study carries an MSI-H call (older studies pre-date routine MSI testing).
# annotate_hypermutators previously hard-keyed on samples["msi_type"] and
# raised KeyError when the column was absent. Fix: treat absence as no MSI-H
# (msi_h all False).

def test_missing_msi_type_column_treats_as_no_msi_h() -> None:
    samples_tmb = _samples_tmb([{"sample_id": "S1", "tmb": 5.0}])
    samples_tmb = samples_tmb.drop(columns=["msi_type", "msi_score"])  # cBioPortal-old shape
    out = annotate_hypermutators(
        samples_tmb_combined=samples_tmb,
        samples_gmm_flagged=_samples_gmm([{"sample_id": "S1"}]),
        per_cancer_gmm_fits=_per_cancer([{"cancer_type": "Test Cancer"}]),
    )
    row = out.loc[out["sample_id"] == "S1"].iloc[0]
    # No POLE/POLD1 hotspot, no MSI-H, no GMM trigger → NOT a hypermutator.
    assert not row["is_hypermutator"]
    assert "msi_h" not in str(row.get("hypermutator_reason", ""))
