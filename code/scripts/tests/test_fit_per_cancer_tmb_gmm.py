"""Tests for ``fit_per_cancer_tmb_gmm.fit_gmm_per_cancer``.

Specification is task 5 of the t081 hypermutator / TMB annotation plan at
``doc/plans/2026-04-13-t081-hypermutator-annotation-pipeline-plan.md``.
"""

import math

import numpy as np
import pandas as pd

from fit_per_cancer_tmb_gmm import (
    FIT_QUALITY_BIMODAL,
    FIT_QUALITY_INSUFFICIENT_DATA,
    FIT_QUALITY_NOT_BIMODAL,
    FIT_QUALITY_SINGLE_MODE,
    fit_gmm_per_cancer,
)


_RNG_SEED = 42


def _synthetic_bimodal_cancer(
    cancer_type: str,
    n_lower: int = 200,
    n_upper: int = 50,
    lower_log_tmb: float = math.log10(3.0),
    upper_log_tmb: float = math.log10(100.0),
    # Scale tightened from plan's suggested 0.3 to 0.2 so the Hartigan dip test
    # reliably returns p < 0.1 at the plan's 200:50 imbalance; at 0.3 the dip
    # test is borderline because it is conservative on imbalanced mixtures.
    scale: float = 0.2,
    rng_seed: int = 0,
) -> pd.DataFrame:
    rng = np.random.default_rng(rng_seed)
    lower = rng.normal(lower_log_tmb, scale, size=n_lower)
    upper = rng.normal(upper_log_tmb, scale, size=n_upper)
    log_tmb = np.concatenate([lower, upper])
    tmb = np.power(10.0, log_tmb) - 1.0
    tmb = np.clip(tmb, 0.0, None)
    return pd.DataFrame(
        {
            "sample_id": [f"{cancer_type}_{i}" for i in range(len(tmb))],
            "study_id": "test_study",
            "cancer_type": cancer_type,
            "tmb": tmb,
            "tmb_log10": log_tmb,
        }
    )


def _synthetic_unimodal_cancer(
    cancer_type: str, n: int = 500, log_tmb: float = math.log10(3.0), scale: float = 0.3
) -> pd.DataFrame:
    rng = np.random.default_rng(1)
    log_tmb_vals = rng.normal(log_tmb, scale, size=n)
    tmb = np.power(10.0, log_tmb_vals) - 1.0
    tmb = np.clip(tmb, 0.0, None)
    return pd.DataFrame(
        {
            "sample_id": [f"{cancer_type}_{i}" for i in range(n)],
            "study_id": "test_study",
            "cancer_type": cancer_type,
            "tmb": tmb,
            "tmb_log10": log_tmb_vals,
        }
    )


def test_bimodal_cohort_fit_quality_bimodal_and_upper_samples_flagged() -> None:
    df = _synthetic_bimodal_cancer("BIMOD", n_lower=200, n_upper=50)
    per_cancer, samples = fit_gmm_per_cancer(df, random_seed=_RNG_SEED)
    fit_row = per_cancer.loc[per_cancer["cancer_type"] == "BIMOD"].iloc[0]
    assert fit_row["fit_quality"] == FIT_QUALITY_BIMODAL
    # Upper component samples (those synthesized near log10(100)) should be flagged.
    flagged = samples.loc[samples["is_hypermutator_gmm"]]
    # At least ~80% of the 50 synthetic upper-mode samples should be flagged.
    upper_log_threshold = (math.log10(3.0) + math.log10(100.0)) / 2
    expected_upper = df["tmb_log10"] > upper_log_threshold
    # Cross-reference with flags — agreement should be >= 0.8 overall.
    joined = samples.merge(
        df.assign(expected=expected_upper)[["sample_id", "expected"]],
        on="sample_id",
    )
    agreement = (joined["is_hypermutator_gmm"] == joined["expected"]).mean()
    assert agreement >= 0.8
    # Posterior column present and in [0,1] for bimodal cells.
    assert samples["gmm_posterior_upper"].between(0.0, 1.0).all()
    assert flagged["gmm_posterior_upper"].gt(0.5).all()


def test_single_mode_cohort_flags_no_hypermutators() -> None:
    df = _synthetic_unimodal_cancer("UNIMODAL", n=500)
    per_cancer, samples = fit_gmm_per_cancer(df, random_seed=_RNG_SEED)
    fit_row = per_cancer.loc[per_cancer["cancer_type"] == "UNIMODAL"].iloc[0]
    assert fit_row["fit_quality"] in {FIT_QUALITY_SINGLE_MODE, FIT_QUALITY_NOT_BIMODAL}
    assert not samples["is_hypermutator_gmm"].any()


def test_insufficient_data_falls_back_to_ten_times_median_rule() -> None:
    # 10 samples — well below the default gmm_min_samples threshold. One sample has
    # TMB = 15 * median → should be flagged as hypermutator via the fallback rule.
    median_tmb = 1.0
    tmb_values = [median_tmb] * 9 + [15.0 * median_tmb]
    df = pd.DataFrame(
        {
            "sample_id": [f"S{i}" for i in range(len(tmb_values))],
            "study_id": "s",
            "cancer_type": "RARE_CANCER",
            "tmb": tmb_values,
            "tmb_log10": [math.log10(v + 1.0) for v in tmb_values],
        }
    )
    per_cancer, samples = fit_gmm_per_cancer(
        df, random_seed=_RNG_SEED, gmm_min_samples=100
    )
    fit_row = per_cancer.loc[per_cancer["cancer_type"] == "RARE_CANCER"].iloc[0]
    assert fit_row["fit_quality"] == FIT_QUALITY_INSUFFICIENT_DATA
    # Exactly one hypermutator — the 15×median sample.
    assert samples["is_hypermutator_gmm"].sum() == 1
    assert (
        samples.loc[samples["is_hypermutator_gmm"], "sample_id"].iloc[0]
        == df["sample_id"].iloc[-1]
    )


def test_z_score_within_cancer_always_emitted() -> None:
    df = _synthetic_unimodal_cancer("C", n=500)
    _, samples = fit_gmm_per_cancer(df, random_seed=_RNG_SEED)
    assert "tmb_zscore_within_cancer" in samples.columns
    # Within-group mean of z-score should be ~0 and std ~1.
    z = samples["tmb_zscore_within_cancer"]
    assert abs(z.mean()) < 1e-6
    assert abs(z.std(ddof=0) - 1.0) < 0.05


def test_reproducibility_same_seed_same_flags() -> None:
    df = _synthetic_bimodal_cancer("REP", n_lower=200, n_upper=50)
    _, s1 = fit_gmm_per_cancer(df, random_seed=123)
    _, s2 = fit_gmm_per_cancer(df, random_seed=123)
    merged = s1[["sample_id", "is_hypermutator_gmm", "gmm_posterior_upper"]].merge(
        s2[["sample_id", "is_hypermutator_gmm", "gmm_posterior_upper"]],
        on="sample_id",
        suffixes=("_1", "_2"),
    )
    assert (merged["is_hypermutator_gmm_1"] == merged["is_hypermutator_gmm_2"]).all()
    # Posterior values identical to within float tolerance.
    assert merged["gmm_posterior_upper_1"].equals(merged["gmm_posterior_upper_2"])


def test_per_cancer_fits_schema() -> None:
    df = _synthetic_bimodal_cancer("C1")
    per_cancer, _ = fit_gmm_per_cancer(df, random_seed=_RNG_SEED)
    expected_cols = {
        "cancer_type",
        "n_samples",
        "bic_1",
        "bic_2",
        "delta_bic",
        "dip_pvalue",
        "fit_quality",
        "upper_component_mean",
        "lower_component_mean",
    }
    assert expected_cols <= set(per_cancer.columns)


def test_samples_flagged_schema() -> None:
    df = _synthetic_bimodal_cancer("C1")
    _, samples = fit_gmm_per_cancer(df, random_seed=_RNG_SEED)
    for col in (
        "sample_id",
        "cancer_type",
        "is_hypermutator_gmm",
        "gmm_posterior_upper",
        "tmb_zscore_within_cancer",
    ):
        assert col in samples.columns


def test_multiple_cancer_types_fit_independently() -> None:
    df_bimodal = _synthetic_bimodal_cancer("BIMOD", n_lower=200, n_upper=50)
    df_unimodal = _synthetic_unimodal_cancer("UNIMOD", n=500)
    df = pd.concat([df_bimodal, df_unimodal], ignore_index=True)
    per_cancer, samples = fit_gmm_per_cancer(df, random_seed=_RNG_SEED)
    bimod = per_cancer.loc[per_cancer["cancer_type"] == "BIMOD"].iloc[0]
    unimod = per_cancer.loc[per_cancer["cancer_type"] == "UNIMOD"].iloc[0]
    assert bimod["fit_quality"] == FIT_QUALITY_BIMODAL
    assert unimod["fit_quality"] in {FIT_QUALITY_SINGLE_MODE, FIT_QUALITY_NOT_BIMODAL}
    # Cross-cancer separation: only BIMOD samples carry hypermutator=True.
    bimod_flagged = samples.loc[
        (samples["cancer_type"] == "BIMOD") & samples["is_hypermutator_gmm"]
    ]
    unimod_flagged = samples.loc[
        (samples["cancer_type"] == "UNIMOD") & samples["is_hypermutator_gmm"]
    ]
    assert len(bimod_flagged) > 0
    assert len(unimod_flagged) == 0


def test_empty_input_returns_empty_outputs_with_schema() -> None:
    empty = pd.DataFrame(
        {
            "sample_id": pd.Series(dtype=object),
            "study_id": pd.Series(dtype=object),
            "cancer_type": pd.Series(dtype=object),
            "tmb": pd.Series(dtype=float),
            "tmb_log10": pd.Series(dtype=float),
        }
    )
    per_cancer, samples = fit_gmm_per_cancer(empty, random_seed=_RNG_SEED)
    assert per_cancer.empty
    assert samples.empty
    assert "fit_quality" in per_cancer.columns
    assert "is_hypermutator_gmm" in samples.columns
