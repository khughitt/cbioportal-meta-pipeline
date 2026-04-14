"""
fit_per_cancer_tmb_gmm.py

Per-cancer-type Gaussian Mixture Model fit on log10 TMB for the t081 hypermutator
annotation pipeline (see ``doc/plans/2026-04-13-t081-hypermutator-annotation-
pipeline-plan.md`` task 5).

Reproducibility covenant — flags flip on borderline samples if seed drifts; see
review ``doc/plans/2026-04-13-t081-hypermutator-annotation-plan-review.md``
finding #1. Every ``sklearn.mixture.GaussianMixture(...)`` call must pass the
explicit ``random_seed`` from config.

Selection logic for bimodal vs single-mode:

- ``n_samples < gmm_min_samples`` → ``fit_quality = "insufficient_data"``;
  fallback is the simple ``tmb > 10 * median(tmb)`` rule (per plan).
- Else fit 1-component + 2-component GMM; compute Hartigan dip-test p-value on
  ``tmb_log10``.
- Select 2-component iff ``ΔBIC > 10`` AND ``dip_p_value < 0.1``
  (``fit_quality = "bimodal"``). Samples with posterior upper-component prob
  > 0.5 get ``is_hypermutator_gmm = True``.
- Else ``fit_quality = "single_mode"`` (BIC fails) or ``"not_bimodal"`` (dip
  test fails); no samples flagged in either case. The z-score column is still
  emitted for the downstream composite step (t097 rows 6 / 7).

``tmb_zscore_within_cancer = (tmb_log10 - group_mean) / group_std`` is ALWAYS
computed regardless of fit quality — it is the fallback signal consumed by the
composite flag.
"""

from __future__ import annotations

import logging

import diptest  # type: ignore[import-untyped]
import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture


logger = logging.getLogger("fit_per_cancer_tmb_gmm")


FIT_QUALITY_BIMODAL = "bimodal"
FIT_QUALITY_SINGLE_MODE = "single_mode"
FIT_QUALITY_NOT_BIMODAL = "not_bimodal"
FIT_QUALITY_INSUFFICIENT_DATA = "insufficient_data"


_DEFAULT_GMM_MIN_SAMPLES = 100
_DELTA_BIC_THRESHOLD = 10.0
_DIP_PVALUE_THRESHOLD = 0.1
_UPPER_POSTERIOR_FLAG_THRESHOLD = 0.5
_INSUFFICIENT_DATA_MEDIAN_MULTIPLE = 10.0


_PER_CANCER_FIT_COLUMNS = [
    "cancer_type",
    "n_samples",
    "bic_1",
    "bic_2",
    "delta_bic",
    "dip_pvalue",
    "fit_quality",
    "upper_component_mean",
    "lower_component_mean",
]

_SAMPLES_FLAGGED_COLUMNS = [
    "sample_id",
    "cancer_type",
    "tmb_log10",
    "tmb_zscore_within_cancer",
    "gmm_posterior_upper",
    "is_hypermutator_gmm",
]


def fit_gmm_per_cancer(
    samples_tmb: pd.DataFrame,
    random_seed: int,
    gmm_min_samples: int = _DEFAULT_GMM_MIN_SAMPLES,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Fit per-cancer-type GMM on log10 TMB; return (per_cancer_fits, samples_flagged).

    The input must have at least ``sample_id``, ``cancer_type``, ``tmb_log10``.
    """
    if samples_tmb.empty:
        return (
            pd.DataFrame(columns=_PER_CANCER_FIT_COLUMNS),
            pd.DataFrame(columns=_SAMPLES_FLAGGED_COLUMNS),
        )

    per_cancer_rows: list[dict[str, object]] = []
    samples_rows: list[pd.DataFrame] = []

    for cancer_type, group in samples_tmb.groupby("cancer_type", observed=True):
        fit_row, per_sample = _fit_one_cancer(
            cancer_type=str(cancer_type),
            group=group,
            random_seed=random_seed,
            gmm_min_samples=gmm_min_samples,
        )
        per_cancer_rows.append(fit_row)
        samples_rows.append(per_sample)

    per_cancer = (
        pd.DataFrame(per_cancer_rows)
        .reindex(columns=_PER_CANCER_FIT_COLUMNS)
        .reset_index(drop=True)
    )
    samples = (
        pd.concat(samples_rows, ignore_index=True)
        .reindex(columns=_SAMPLES_FLAGGED_COLUMNS)
        .reset_index(drop=True)
    )
    return per_cancer, samples


def _fit_one_cancer(
    cancer_type: str,
    group: pd.DataFrame,
    random_seed: int,
    gmm_min_samples: int,
) -> tuple[dict[str, object], pd.DataFrame]:
    n_samples = int(len(group))
    tmb_log10 = group["tmb_log10"].to_numpy(dtype=float)
    zscore = _within_group_zscore(tmb_log10)

    per_sample_base = pd.DataFrame(
        {
            "sample_id": group["sample_id"].to_numpy(),
            "cancer_type": cancer_type,
            "tmb_log10": tmb_log10,
            "tmb_zscore_within_cancer": zscore,
            "gmm_posterior_upper": np.nan,
            "is_hypermutator_gmm": False,
        }
    )

    if n_samples < gmm_min_samples:
        return _insufficient_data_fallback(
            cancer_type, group, n_samples, per_sample_base
        )

    bic1, mean1 = _fit_gmm_and_score(tmb_log10, n_components=1, random_seed=random_seed)
    bic2, means2, posteriors_upper = _fit_gmm_and_score_two_component(
        tmb_log10, random_seed=random_seed
    )
    delta_bic = bic1 - bic2  # positive means 2-component is preferred
    dip_statistic, dip_pvalue = diptest.diptest(tmb_log10)
    del dip_statistic  # unused; kept here to document the return tuple

    lower_mean, upper_mean = (min(means2), max(means2))

    if delta_bic > _DELTA_BIC_THRESHOLD and dip_pvalue < _DIP_PVALUE_THRESHOLD:
        fit_quality = FIT_QUALITY_BIMODAL
        per_sample_base["gmm_posterior_upper"] = posteriors_upper
        per_sample_base["is_hypermutator_gmm"] = (
            posteriors_upper > _UPPER_POSTERIOR_FLAG_THRESHOLD
        )
    elif delta_bic <= _DELTA_BIC_THRESHOLD:
        fit_quality = FIT_QUALITY_SINGLE_MODE
    else:
        fit_quality = FIT_QUALITY_NOT_BIMODAL

    fit_row = {
        "cancer_type": cancer_type,
        "n_samples": n_samples,
        "bic_1": float(bic1),
        "bic_2": float(bic2),
        "delta_bic": float(delta_bic),
        "dip_pvalue": float(dip_pvalue),
        "fit_quality": fit_quality,
        "upper_component_mean": float(upper_mean),
        "lower_component_mean": float(lower_mean),
    }
    del mean1
    return fit_row, per_sample_base


def _insufficient_data_fallback(
    cancer_type: str,
    group: pd.DataFrame,
    n_samples: int,
    per_sample_base: pd.DataFrame,
) -> tuple[dict[str, object], pd.DataFrame]:
    tmb = group["tmb"].to_numpy(dtype=float)
    if len(tmb) == 0:
        median_tmb = float("nan")
    else:
        median_tmb = float(np.median(tmb))
    threshold = _INSUFFICIENT_DATA_MEDIAN_MULTIPLE * median_tmb
    is_hyp = tmb > threshold if median_tmb > 0 else np.zeros(len(tmb), dtype=bool)
    per_sample = per_sample_base.copy()
    per_sample["is_hypermutator_gmm"] = is_hyp

    fit_row = {
        "cancer_type": cancer_type,
        "n_samples": n_samples,
        "bic_1": float("nan"),
        "bic_2": float("nan"),
        "delta_bic": float("nan"),
        "dip_pvalue": float("nan"),
        "fit_quality": FIT_QUALITY_INSUFFICIENT_DATA,
        "upper_component_mean": float("nan"),
        "lower_component_mean": float("nan"),
    }
    return fit_row, per_sample


def _fit_gmm_and_score(
    log_tmb: np.ndarray, n_components: int, random_seed: int
) -> tuple[float, np.ndarray]:
    x = log_tmb.reshape(-1, 1)
    gmm = GaussianMixture(
        n_components=n_components, random_state=random_seed, n_init=10
    )
    gmm.fit(x)
    return float(gmm.bic(x)), gmm.means_.ravel()


def _fit_gmm_and_score_two_component(
    log_tmb: np.ndarray, random_seed: int
) -> tuple[float, np.ndarray, np.ndarray]:
    x = log_tmb.reshape(-1, 1)
    gmm = GaussianMixture(n_components=2, random_state=random_seed, n_init=10)
    gmm.fit(x)
    means = gmm.means_.ravel()
    upper_idx = int(np.argmax(means))
    posteriors = gmm.predict_proba(x)[:, upper_idx]
    return float(gmm.bic(x)), means, posteriors


def _within_group_zscore(values: np.ndarray) -> np.ndarray:
    if len(values) == 0:
        return values
    mu = float(np.mean(values))
    sigma = float(np.std(values, ddof=0))
    if sigma == 0.0:
        return np.zeros_like(values)
    return (values - mu) / sigma


def _run_via_snakemake() -> None:
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821
    samples = pd.read_feather(snek.input.samples_tmb_combined)
    random_seed = int(snek.config.get("random_seed", 0))
    gmm_min_samples = int(snek.config.get("gmm_min_samples", _DEFAULT_GMM_MIN_SAMPLES))
    per_cancer, samples_flagged = fit_gmm_per_cancer(
        samples, random_seed=random_seed, gmm_min_samples=gmm_min_samples
    )
    per_cancer.to_feather(snek.output.per_cancer_fits)
    samples_flagged.to_feather(snek.output.samples_flagged)
    logger.info(
        "Fitted %d cancer-type GMMs; %d samples flagged as hypermutator.",
        len(per_cancer),
        int(samples_flagged["is_hypermutator_gmm"].sum()),
    )


if "snakemake" in globals():
    _run_via_snakemake()
