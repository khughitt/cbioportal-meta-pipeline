---
id: "interpretation:2026-06-01-h08-within-tissue-diagnostics"
type: "interpretation"
status: "active"
source_refs:
  - "task:t200"
title: "t200 h08 within-tissue failure diagnostics — APOBEC arm robust; UV/smoking failures are proxy-quality, not method"
date: "2026-06-01"
related:
  - "task:t200"
  - "hypothesis:h08-agnostic-covariate-association-recovers-known-signature-aetiologies-and"
  - "question:q022-apobec-a3a-a3b-joint-expression-and-mmr-omikli"
---
# t200 — h08 within-tissue failure diagnostics

Date: 2026-06-01

## Question

Why did the h08 positive-control scan miss the UV→SBS7 and smoking→SBS4 within-tissue gates, and
does the APOBEC pass survive a direct proliferation-control probe?

This is a diagnostic layer over the frozen t199 artifacts.
It does **not** re-read the H08a verdict: the locked result remains H08a `[?]` (1/3 arms passing;
see `doc/interpretations/2026-05-31-t199-h08-association-verdict.md`).

## Artifacts

Run bundle:
`results/signature-h08-arms-2026-05-31/association/diagnostics/`

- `h08_within_tissue_baseline.feather`
- `h08_within_tissue_contrast.feather`
- `h08_smoking_operationalizations.feather`
- `h08_smoking_label_counts.feather`
- `h08_burden_conditioning.feather`
- `h08_apobec_proliferation.feather`
- `h08_within_tissue_diagnostics.meta.json`

The baseline guard reproduced the frozen WP2 target coefficients and n exactly:
A −0.0462 (n = 370), B +0.1066 (n = 703), C +0.4584 (n = 1,883).

## Readout

| Arm | Frozen target | Diagnostic read | Most-consistent failure mode |
|---|---|---|---|
| A | UV-site ordinal→SBS7 | UV-site remains null under burden conditioning; the non-saturated subset is only n = 9–10 at SBS7-fraction thresholds 0.80–0.95. | Weak proxy plus saturation / no residual room. |
| B | `pack_years`→SBS4 | Derived `ever_smoker` out-ranks both pack-year forms, especially in LUAD. | Thresholded smoking signal + missing-zero artefact in frozen pack-years. |
| C | APOBEC3A/B mRNA→SBS2/13 | APOBEC remains after TMB/hypermutator conditioning and after proliferation control. | Proliferation-robust in this substrate. |

## Test 1 — effective contrast

UV-site contrast in SKCM is ordinal and compressed into three tiers: 40 low, 119 mid, 211 high
among the 370 model-frame samples; entropy is 1.34 bits.
That is enough ordinal spread to fit a coefficient, but it is still a coarse anatomic-site proxy, not
a cumulative UV-dose measure.

Pack-years did **not** look range-restricted by SD alone on the effective fit frame: LUAD ratio =
0.94, LUSC ratio = 1.05 after tissue-mean centering.
This means the original smoking miss should not be attributed simply to low continuous variance.
The later smoking-operationalization test gives the sharper explanation.

APOBEC3A/B mRNA shows usable within-tissue spread across all six Arm-C tissues.
The tissue-centered range-restriction ratios span 0.82–1.21, supporting the idea that the molecular
covariate has enough within-tissue contrast for the model to recover it.

## Test 2 — smoking operationalization

The frozen `ever_smoker` artifact is unusable, as expected from the plan review: it is all-missing in
lung because textual smoking labels were passed through numeric coercion.
The diagnostic re-derived smoking from the raw PanCanAtlas labels and added
`pack_years_zero_never`, where lifelong non-smokers are set to 0 rather than silently dropped.

| Stratum | Covariate | n | coef | p |
|---|---|---:|---:|---:|
| LUAD+LUSC | `pack_years` | 703 | +0.107 | 0.182 |
| LUAD+LUSC | `pack_years_zero_never` | 734 | +0.193 | 0.016 |
| LUAD+LUSC | `ever_smoker_derived` | 839 | +0.267 | 0.00032 |
| LUAD | `pack_years` | 306 | +0.161 | 0.155 |
| LUAD | `pack_years_zero_never` | 325 | +0.316 | 0.0055 |
| LUAD | `ever_smoker_derived` | 388 | +0.393 | 0.00015 |
| LUSC | `pack_years` | 397 | +0.088 | 0.444 |
| LUSC | `pack_years_zero_never` | 409 | +0.134 | 0.245 |
| LUSC | `ever_smoker_derived` | 451 | +0.139 | 0.208 |

This shifts the Arm-B diagnosis.
The frozen pack-years miss is partly an operationalization artifact: never-smokers mostly have
missing pack-years rather than zero pack-years, so the frozen continuous model drops much of the
contrast that distinguishes never-smokers from ever-smokers.
The stronger binary result, concentrated in LUAD, is consistent with a thresholded smoking signal
rather than a clean linear pack-years dose-response.

This is still diagnostic only.
It does not promote Arm B to a primary pass because the registered, frozen target was
`pack_years`, not re-derived `ever_smoker`.

## Test 3 — burden-mediated / proximal conditioning

Conditioning on `tmb_nonsynonymous` and `is_hypermutator` gives the expected target-proximal read:
it asks whether the registered covariate has residual association after burden-linked consequences
are included, not whether the original exposure is causally independent of burden.

| Arm | Model | n | coef | p | Interpretation |
|---|---|---:|---:|---:|---|
| A | burden-conditioned | 370 | −0.066 | 0.135 | UV-site remains null. |
| A | non-saturated subset, SBS7 < 0.90 | 10 | −0.237 | 0.716 | Too few non-saturated SKCM samples to rescue signal. |
| B | burden-conditioned | 689 | +0.085 | 0.257 | Pack-years remains weak. |
| B | non-saturated subset | 398 | +0.049 | 0.653 | Smoking proxy has little residual signal after excluding hypermutators. |
| C | burden-conditioned | 1,883 | +0.447 | 3.6e-13 | APOBEC survives target-proximal controls. |
| C | non-saturated subset | 1,312 | +0.386 | 2.2e-08 | APOBEC remains in non-hypermutators. |

The Arm-A non-saturated result is mostly a sample-size warning: SBS7 dominates SKCM so strongly that
the pre-specified non-saturated subset is n = 9–10 across the 0.80–0.95 sweep.
That supports a saturation/no-residual-room interpretation, but it does not rescue the anatomic UV
proxy.

## Test 4 — APOBEC proliferation robustness

APOBEC3A/B mRNA was refit per Arm-C tissue with a proliferation score from full RSEM, using the
Venet meta-PCNA gene set as the primary control and a canonical cell-cycle marker set as sensitivity.
All six tissues retained all 30 meta-PCNA genes and all 16 canonical markers, with non-zero score
variance.

Primary meta-PCNA control:

| Tissue | n | baseline coef | proliferation-controlled coef | shrinkage bin |
|---|---:|---:|---:|---|
| BLCA | 343 | +0.302 | +0.289 | <25% |
| BRCA | 176 | −0.086 | +0.216 | <25% |
| CESC | 184 | +0.570 | +0.571 | <25% |
| HNSC | 347 | +0.655 | +0.655 | <25% |
| LUAD | 389 | +0.533 | +0.513 | <25% |
| LUSC | 444 | +0.328 | +0.335 | <25% |

The n-weighted absolute coefficient is essentially unchanged: 0.427 before control versus 0.434
after meta-PCNA control.
The canonical marker sensitivity gives the same qualitative result.

The Arm-C APOBEC pass is therefore **proliferation-robust in this substrate**.
BRCA remains the one per-tissue caveat: its baseline per-tissue coefficient is small and negative,
then positive after proliferation control, so the pooled Arm-C pass should not be described as
uniformly positive across every tissue.
The pooled result is nevertheless not explained away by a shared cell-cycle score.

## Conclusion

The t200 probe changes the *why*, not the verdict.

Arm A looks like weak measurement plus saturation: an anatomic UV-site ordinal cannot recover much
residual SBS7 variation once SKCM is already SBS7-dominated.
Arm B looks less like pure measurement noise and more like a frozen operationalization problem:
binary ever-smoker and zero-filled never-smoker pack-years recover a stronger SBS4 association than
the registered continuous pack-years variable.
Arm C remains the cleanest positive control because the covariate is molecular, variable within
tissue, and robust to both burden-linked and proliferation-linked controls.

The locked H08a verdict remains `[?]`.
The indicated follow-up is to fix the production `ever_smoker` derivation separately, then decide
whether a future pre-registered smoking-arm repair should use `ever_smoker` or a better smoking
biomarker rather than frozen pack-years alone.
