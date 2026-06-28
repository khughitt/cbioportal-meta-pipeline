---
type: interpretation
title: "t204 h08 smoking-arm repair production rerun \u2014 binary ever-smoker recovers\
  \ significant SBS4 association but misses top-3 gate"
status: active
created: '2026-06-01'
updated: '2026-06-28'
id: interpretation:0025-h08-smoking-repair
source_refs:
- task:t204
date: '2026-06-01'
related:
- task:t204
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
---
# t204 — hypothesis:0007 smoking-arm repair production rerun

Date: 2026-06-01

## Question

Under the committed smoking-arm repair pre-registration, does replacing the original Arm-B `pack_years` slot with the repaired production `ever_smoker` covariate recover smoking→SBS4 in pooled LUAD+LUSC?
This is the `task:t204` production read and remains scoped to
`hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and`.

This is a repaired positive-control read only.
It does **not** re-read the locked t199 H08a verdict, which remains `[?]` (see `doc/interpretations/2026-05-31-t199-h08-association-verdict.md`).

## Artifacts

Run bundle:
`results/signature-h08-arms-2026-05-31/association/repairs/smoking_arm/`

- `h08_smoking_repair_grid.feather`
- `h08_smoking_repair_sensitivity.feather`
- `h08_smoking_repair.meta.json`

The repaired run used the t201 production covariate table and derived its Arm-B denominator from the t199 denominator manifest without overwriting the original H08a artifacts.
The source denominator SHA256 recorded in repair metadata is
`72ed4159fdfad821f8c9dcc0be35d34e5e4ebba3d0c0abafa971760c923d280c`.

## Primary Read

The repaired primary family replaces `pack_years` with `ever_smoker` in the LUAD+LUSC Arm-B ranked scalar set and fits SBS4 against each testable covariate under the original agnostic-association CLR / count-floor / adjustment machinery.

| Covariate | n | coef | p | BH-q | Rank / denom |
|---|---:|---:|---:|---:|---:|
| `is_hypermutator` | 840 | +0.755 | 6.36e-26 | 5.09e-25 | 1 / 8 |
| `tmb_nonsynonymous` | 840 | +0.721 | 2.83e-23 | 1.13e-22 | 2 / 8 |
| `age` | 817 | −0.371 | 9.18e-07 | 2.45e-06 | 3 / 8 |
| `apobec3ab_joint` | 833 | −0.319 | 2.51e-04 | 5.03e-04 | 4 / 8 |
| `ever_smoker` | 839 | +0.267 | 3.19e-04 | 5.10e-04 | 5 / 8 |
| `stage_ordinal` | 836 | +0.108 | 0.146 | 0.195 | 6 / 8 |
| `msi_sensor_score` | 840 | −0.064 | 0.382 | 0.436 | 7 / 8 |
| `sex_male` | 838 | −0.056 | 0.464 | 0.464 | 8 / 8 |

The primary repaired smoking signal is real in the narrow association sense: the coefficient is positive, model-frame n is 839, and BH-q is 5.10e-04.
It fails the pre-registered repaired pass because rank is 5 / 8, not <= 3.

**Repair verdict: `[?]`.**
The result supports the t200 operationalization-artifact explanation directionally, but it does not meet the stricter repaired production gate.

## Sensitivities

| Family | Stratum | Covariate | n | coef | p | BH-q | Rank / denom |
|---|---|---|---:|---:|---:|---:|---:|
| pooled original | LUAD+LUSC | `pack_years` | 703 | +0.107 | 0.182 | 0.243 | 6 / 8 |
| pooled zero-never | LUAD+LUSC | `pack_years_zero_never` | 734 | +0.193 | 0.016 | 0.0257 | 5 / 8 |
| LUAD-only | LUAD | `ever_smoker` | 388 | +0.393 | 1.54e-04 | 6.66e-04 | 3 / 13 |
| LUSC-only | LUSC | `ever_smoker` | 451 | +0.139 | 0.208 | 0.289 | 9 / 13 |

The sensitivity pattern matches the t200 diagnostic.
Binary ever-smoker is stronger than continuous pack-years, and the signal is concentrated in LUAD rather than LUSC.
Zero-filled never-smoker pack-years improves over original pack-years but remains weaker than the binary covariate and is not a primary pass route.

## Interpretation

The repaired production run narrows the Arm-B story rather than fully repairing the gate.
The original t199 `pack_years` miss was not just random failure: when lifelong non-smokers are retained through `ever_smoker`, the SBS4 association becomes clearly positive and statistically significant.
However, under the pre-registered rank rule, smoking still does not outrank the burden-linked covariates or two additional lung covariates in the repaired production denominator.

That rank failure matters.
It means the repaired binary proxy is better than frozen pack-years, but still not strong enough to serve as a clean top-3 positive-control recovery on this substrate.
The burden dominance observed in t199 and t200 remains a feature of the lung SBS4 cell.

## Verdict and What It Licenses

The local repaired Arm-B verdict is `[?]`.
This supports a cautious statement:
the frozen Arm-B miss was partly an exposure-operationalization artifact, but the repaired production scan still does not produce a top-3 smoking positive control.

It does not change H08a `[?]`, and it does not unlock H08b as confirmatory work.
The next defensible choices are either to leave H08a inconclusive and label H08b exploratory, or to design a future repaired gate that also addresses Arm A / UV and the lung burden-dominance problem before any promotion decision.
