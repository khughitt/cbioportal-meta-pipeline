"""
annotate_hypermutators.py

Composite hypermutation score + final flag for the t081 annotation pipeline
(see ``doc/plans/2026-04-13-t081-hypermutator-annotation-pipeline-plan.md``
task 6). Closes the F4 inconsistency by applying a single canonical decision
table with documented priority.

Canonical decision table (first matching row wins, per plan):

| # | Condition | hypermutation_score                         | is_hypermutator | reason                |
|---|-----------|---------------------------------------------|-----------------|-----------------------|
| 1 | POLE hotspot                              | 1.0                                  | True            | ``pole_hotspot``       |
| 2 | POLD1 hotspot                             | 1.0                                  | True            | ``pold1_hotspot``      |
| 3 | msi_type == "MSI-H"                        | 1.0                                  | True            | ``msi_h``              |
| 4 | GMM bimodal & posterior > 0.5              | posterior                            | True            | ``gmm_upper_mode``     |
| 5 | GMM bimodal & posterior ≤ 0.5              | posterior                            | False           | ``gmm_lower_mode``     |
| 6 | GMM unavailable & zscore ≥ 1.5             | min(1.0, (z - 1.5)/1.5 + 0.5)        | True            | ``zscore_fallback_high`` |
| 7 | GMM unavailable & zscore < 1.5             | max(0.0, z/3.0)                      | False           | ``zscore_fallback_low`` |
| 8 | tmb is NaN                                 | NaN                                  | False           | ``tmb_unavailable``    |

Rows 1-3 are deterministic (clinical diagnostic categories override TMB). Row 8
is the NaN-safe default. "GMM unavailable" is any ``fit_quality`` other than
``"bimodal"`` (i.e., single_mode / not_bimodal / insufficient_data).

Dual flags (introduced by task t089):

- ``is_hypermutator_absolute``  — tmb ≥ 10 mut/Mb (Campbell 2017 hypermutator cutoff)
- ``is_hypermutator_ultra``     — tmb ≥ 100 mut/Mb (Campbell 2017 ultramutator cutoff)
- ``is_hypermutator_relative``  — top-20% TMB within the sample's cancer type
                                  (Samstein 2019 per-histology top-quintile rule)

Inputs
------
- ``snakemake.input.samples_tmb_combined`` : per-sample TMB + MSI + POLE/POLD1
  flags (from ``combine_samples_tmb``).
- ``snakemake.input.per_cancer_fits``      : per-cancer-type GMM fit quality
  (from ``fit_per_cancer_tmb_gmm``).
- ``snakemake.input.samples_flagged``      : per-sample GMM posteriors +
  ``tmb_zscore_within_cancer`` (from ``fit_per_cancer_tmb_gmm``).

Output
------
- ``snakemake.output[0]`` : ``out_dir/metadata/samples_annotated.feather``
  with the three composite columns + three dual-flag columns added.
"""


import logging

import numpy as np
import pandas as pd


logger = logging.getLogger("annotate_hypermutators")


REASON_POLE_HOTSPOT = "pole_hotspot"
REASON_POLD1_HOTSPOT = "pold1_hotspot"
REASON_MSI_H = "msi_h"
REASON_GMM_UPPER = "gmm_upper_mode"
REASON_GMM_LOWER = "gmm_lower_mode"
REASON_ZSCORE_HIGH = "zscore_fallback_high"
REASON_ZSCORE_LOW = "zscore_fallback_low"
REASON_TMB_UNAVAILABLE = "tmb_unavailable"


_GMM_POSTERIOR_FLAG_THRESHOLD = 0.5
_ZSCORE_HIGH_THRESHOLD = 1.5

_ABSOLUTE_HYPERMUTATOR_TMB = 10.0  # Campbell 2017
_ULTRA_HYPERMUTATOR_TMB = 100.0  # Campbell 2017
_RELATIVE_TOP_QUANTILE = 0.8  # Samstein 2019 top-20% per histology


def annotate_hypermutators(
    samples_tmb_combined: pd.DataFrame,
    samples_gmm_flagged: pd.DataFrame,
    per_cancer_gmm_fits: pd.DataFrame,
) -> pd.DataFrame:
    """Apply the canonical decision table + dual flags; return annotated samples."""
    samples = samples_tmb_combined.merge(
        samples_gmm_flagged[
            [
                "sample_id",
                "gmm_posterior_upper",
                "tmb_zscore_within_cancer",
            ]
        ],
        on="sample_id",
        how="left",
    )
    samples = samples.merge(
        per_cancer_gmm_fits[["cancer_type", "fit_quality"]],
        on="cancer_type",
        how="left",
    )

    scores, flags, reasons = _apply_decision_table(samples)
    samples["hypermutation_score"] = scores
    samples["is_hypermutator"] = flags
    samples["hypermutator_reason"] = reasons

    samples["is_hypermutator_absolute"] = (
        samples["tmb"].ge(_ABSOLUTE_HYPERMUTATOR_TMB).fillna(False).astype(bool)
    )
    samples["is_hypermutator_ultra"] = (
        samples["tmb"].ge(_ULTRA_HYPERMUTATOR_TMB).fillna(False).astype(bool)
    )
    samples["is_hypermutator_relative"] = _relative_top_quintile_flag(samples)

    return samples


def _apply_decision_table(
    samples: pd.DataFrame,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    n = len(samples)
    scores = np.full(n, np.nan, dtype=float)
    flags = np.zeros(n, dtype=bool)
    reasons = np.full(n, "", dtype=object)
    assigned = np.zeros(n, dtype=bool)

    tmb = samples["tmb"].to_numpy(dtype=float)
    pole = samples["pole_hotspot_detected"].fillna(False).to_numpy(dtype=bool)
    pold1 = samples["pold1_hotspot_detected"].fillna(False).to_numpy(dtype=bool)
    msi_h = (samples["msi_type"].fillna("").astype(str) == "MSI-H").to_numpy(dtype=bool)
    is_bimodal = (samples["fit_quality"].fillna("").astype(str) == "bimodal").to_numpy(
        dtype=bool
    )
    posterior = samples["gmm_posterior_upper"].to_numpy(dtype=float)
    zscore = samples["tmb_zscore_within_cancer"].to_numpy(dtype=float)

    _assign_rule(scores, flags, reasons, assigned, pole, 1.0, True, REASON_POLE_HOTSPOT)
    _assign_rule(
        scores, flags, reasons, assigned, pold1, 1.0, True, REASON_POLD1_HOTSPOT
    )
    _assign_rule(scores, flags, reasons, assigned, msi_h, 1.0, True, REASON_MSI_H)
    gmm_upper = is_bimodal & (posterior > _GMM_POSTERIOR_FLAG_THRESHOLD) & (~assigned)
    gmm_lower = is_bimodal & (posterior <= _GMM_POSTERIOR_FLAG_THRESHOLD) & (~assigned)
    scores[gmm_upper] = posterior[gmm_upper]
    flags[gmm_upper] = True
    reasons[gmm_upper] = REASON_GMM_UPPER
    assigned[gmm_upper] = True
    scores[gmm_lower] = posterior[gmm_lower]
    flags[gmm_lower] = False
    reasons[gmm_lower] = REASON_GMM_LOWER
    assigned[gmm_lower] = True

    # Row 8 pre-check: if tmb is NaN, we cannot interpret the zscore either — mark
    # tmb_unavailable before the zscore fallback considers the row.
    tmb_nan = np.isnan(tmb) & (~assigned)
    scores[tmb_nan] = np.nan
    flags[tmb_nan] = False
    reasons[tmb_nan] = REASON_TMB_UNAVAILABLE
    assigned[tmb_nan] = True

    z_high = (~assigned) & (zscore >= _ZSCORE_HIGH_THRESHOLD)
    scores[z_high] = np.minimum(
        1.0, (zscore[z_high] - _ZSCORE_HIGH_THRESHOLD) / 1.5 + 0.5
    )
    flags[z_high] = True
    reasons[z_high] = REASON_ZSCORE_HIGH
    assigned[z_high] = True

    z_low = (~assigned) & (zscore < _ZSCORE_HIGH_THRESHOLD)
    scores[z_low] = np.maximum(0.0, zscore[z_low] / 3.0)
    flags[z_low] = False
    reasons[z_low] = REASON_ZSCORE_LOW
    assigned[z_low] = True

    # Any still-unassigned rows (shouldn't happen with well-formed input) default to
    # tmb_unavailable so the contract never returns an empty-string reason.
    leftover = ~assigned
    scores[leftover] = np.nan
    flags[leftover] = False
    reasons[leftover] = REASON_TMB_UNAVAILABLE
    return scores, flags, reasons


def _assign_rule(
    scores: np.ndarray,
    flags: np.ndarray,
    reasons: np.ndarray,
    assigned: np.ndarray,
    condition: np.ndarray,
    score_value: float,
    flag_value: bool,
    reason: str,
) -> None:
    mask = condition & (~assigned)
    scores[mask] = score_value
    flags[mask] = flag_value
    reasons[mask] = reason
    assigned[mask] = True


def _relative_top_quintile_flag(samples: pd.DataFrame) -> pd.Series:
    """Per-histology top-20% hypermutator flag (Samstein 2019).

    ``pd.Series.rank(pct=True)`` with ``method="max"`` gives the maximum rank percentile
    per value; samples in the top ``(1 - _RELATIVE_TOP_QUANTILE)`` are flagged. Missing
    TMB values drop out (NaN percentile → False).
    """
    pct = samples.groupby("cancer_type", observed=True)["tmb"].rank(
        pct=True, method="max"
    )
    flag = pct > _RELATIVE_TOP_QUANTILE
    return flag.fillna(False).astype(bool)


def _run_via_snakemake() -> None:
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821
    samples_tmb_combined = pd.read_feather(snek.input.samples_tmb_combined)
    samples_gmm_flagged = pd.read_feather(snek.input.samples_flagged)
    per_cancer_gmm_fits = pd.read_feather(snek.input.per_cancer_fits)
    out = annotate_hypermutators(
        samples_tmb_combined, samples_gmm_flagged, per_cancer_gmm_fits
    )
    out.to_feather(snek.output[0])
    logger.info(
        "Annotated %d samples; %d flagged is_hypermutator (%d POLE, %d POLD1, "
        "%d MSI-H, %d GMM-upper, %d zscore-fallback-high).",
        len(out),
        int(out["is_hypermutator"].sum()),
        int((out["hypermutator_reason"] == REASON_POLE_HOTSPOT).sum()),
        int((out["hypermutator_reason"] == REASON_POLD1_HOTSPOT).sum()),
        int((out["hypermutator_reason"] == REASON_MSI_H).sum()),
        int((out["hypermutator_reason"] == REASON_GMM_UPPER).sum()),
        int((out["hypermutator_reason"] == REASON_ZSCORE_HIGH).sum()),
    )


if "snakemake" in globals():
    _run_via_snakemake()
