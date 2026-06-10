---
type: pre-registration
title: "h08 smoking-arm repair \u2014 repaired smoking covariate must recover SBS4\
  \ without rereading the locked H08a verdict"
status: committed
created: '2026-06-01'
updated: '2026-06-01'
id: pre-registration:0004-h08-smoking-arm-repair-repaired-smoking-covariate-must-recover-sbs4
committed: '2026-06-01'
spec: doc/methods/h08-agnostic-association-model.md
related:
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
- method:h08-agnostic-association-model
- pre-registration:0003-h08-positive-control-agnostic-association-must-recover-known-signature
- plan:0006-h08-within-tissue-diagnostics
- task:t199
- task:t200
- task:t201
- task:t202
commits_to:
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
---

# Pre-registration: h08 smoking-arm repair

**Target class: mixed, with limited epistemic weight.**

The operational target is a repaired Arm-B production rerun that uses the fixed smoking covariates from `task:t201` before inspecting any new production-rerun output.
The epistemic target is narrower than the original H08a gate: does the repaired smoking covariate recover the known smoking→SBS4 association under the h08 within-tissue model?

This is **not** an amendment that rereads the frozen `pre-registration:0003-h08-positive-control-agnostic-association-must-recover-known-signature` result.
The 2026-05-31 H08a verdict remains `[?]` because the locked Arm-B covariate was `pack_years`, and the registered 2-of-3 gate was already read in `doc/interpretations/2026-05-31-t199-h08-association-verdict.md`.

This pre-registration is also **not cleanly pre-data**.
The t200 diagnostic already observed a stronger `ever_smoker_derived`→SBS4 association on the same MC3/PanCanAtlas substrate.
Therefore, a repaired production rerun can support the claim that the original Arm-B miss was an operationalization artifact and can justify a future repaired gate, but it cannot by itself promote H08a or unlock H08b as a confirmatory discovery program.

## Hypotheses Under Test

This repair bears on the positive-control prong of
`hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and`.
The tested proposition is local:
the h08 within-tissue association model can recover smoking→SBS4 in lung when the smoking exposure is encoded as a valid binary ever-smoker covariate rather than as missing-prone continuous pack-years.

## Feasibility

The relevant substrate already exists:

| Component | Status |
|---|---|
| Signature outcome | SBS4 exposure from the frozen MC3 COSMIC SBS v3.4 refit used by `task:t199`. |
| Stratum | LUAD + LUSC pooled, with LUAD-only and LUSC-only as sensitivity strata. |
| Repaired smoking covariates | `task:t201` maps raw PanCanAtlas `tobacco_smoking_history` labels to `ever_smoker` and emits `pack_years_zero_never`. |
| Prior diagnostic evidence | `task:t200` fit the same repaired smoking definitions diagnostically without changing the frozen H08a verdict. |

The t200 diagnostic support set gives the practical floor for the rerun:

| Stratum | Covariate | n | coef | p |
|---|---|---:|---:|---:|
| LUAD+LUSC | `ever_smoker_derived` | 839 | +0.267 | 0.00032 |
| LUAD+LUSC | `pack_years_zero_never` | 734 | +0.193 | 0.016 |
| LUAD+LUSC | `pack_years` | 703 | +0.107 | 0.182 |
| LUAD | `ever_smoker_derived` | 388 | +0.393 | 0.00015 |
| LUSC | `ever_smoker_derived` | 451 | +0.139 | 0.208 |

The observed label map is finite and explicit:
lifelong non-smoker maps to 0; current smoker and all current-reformed smoker labels map to 1; missing, unknown, not-available, and discrepancy labels stay missing.
No unrecognized smoking label may be silently coerced to either 0 or 1.

## Expected Outcomes

The primary expectation is that `ever_smoker` will recover SBS4 in the pooled LUAD+LUSC stratum with a positive coefficient and a stronger signal than `pack_years_zero_never`.
This expectation is based on the t200 diagnostic and on the known missingness pattern: lifelong non-smokers often carry missing pack-years, so a continuous pack-year-only model drops much of the never-smoker contrast.

The expected tissue pattern is asymmetric.
LUAD should carry most of the binary contrast because never-smoker LUAD is common enough to separate never from ever smokers.
LUSC may remain weak or null because nearly all LUSC cases are smoking-associated, leaving little binary contrast.

## Expectations

```yaml
- parameter: "rank/significance of repaired ever_smoker vs SBS4 in pooled LUAD+LUSC"
  scope: confirmatory
  expected:
    central: "rank <= 3, positive coefficient, q < 0.05"
    range: "rank [1, 3]"
    direction: positive
  evidence_tier: hint
  provenance:
    - source: "t200 diagnostic"
      calibration_source: pilot_fit
      estimate: "n=839, coef=+0.267, p=0.00032 for ever_smoker_derived vs SBS4 in LUAD+LUSC"
      ref: "doc/interpretations/2026-06-01-h08-within-tissue-diagnostics.md"
      notes: "Same substrate and post-hoc diagnostic; useful for repair design, not independent confirmation."
  unknowns:
    - "whether the production repaired scan reproduces the diagnostic fit once the repaired covariate is inserted into the formal rank denominator"
    - "whether adding or replacing smoking covariates in the denominator changes rank behavior relative to the diagnostic three-proxy comparison"
    - "whether the pooled signal is dominated enough by LUAD that the pooled Arm-B interpretation should be described as LUAD-weighted"
  gate_use: "Primary repaired Arm-B pass criterion; limited evidential weight because t200 has already observed the same signal on the same substrate."

- parameter: "rank/significance of pack_years_zero_never vs SBS4 in pooled LUAD+LUSC"
  scope: sensitivity
  expected:
    central: "positive coefficient, weaker than ever_smoker"
    range: "positive but may or may not meet q < 0.05 after full denominator refit"
    direction: positive
  evidence_tier: hint
  provenance:
    - source: "t200 diagnostic"
      calibration_source: pilot_fit
      estimate: "n=734, coef=+0.193, p=0.016 for pack_years_zero_never vs SBS4 in LUAD+LUSC"
      ref: "doc/interpretations/2026-06-01-h08-within-tissue-diagnostics.md"
      notes: "Supports missing-zero artifact, but remains less direct than binary ever-smoker."
  unknowns:
    - "whether zero-filled pack-years behaves as a biologically interpretable dose proxy rather than a hybrid binary/continuous proxy"
    - "whether pack-year missingness among ever-smokers still biases the fitted coefficient"
  gate_use: "Sensitivity only; cannot rescue the primary repaired Arm-B verdict if ever_smoker fails."
```

## Decision Criteria

The repaired Arm-B primary analysis replaces the original smoking covariate slot with **`ever_smoker`**.
The analysis must use the same SBS4 outcome, LUAD+LUSC pooled stratum, CLR machinery, adjustment set, active-signature rule, and denominator-freezing discipline as the original h08 association scan unless an explicit amendment is recorded before the rerun.

A repaired Arm-B **primary pass** requires all of the following:

| Criterion | Requirement |
|---|---|
| Covariate | `ever_smoker`, derived by the explicit `SMOKING_LABEL_MAP` in `build_h08_covariates.py`. |
| Direction | Positive standardized coefficient against SBS4. |
| Multiplicity | BH-FDR q < 0.05 within the repaired scan family. |
| Rank | Rank ≤ 3 among the testable lung ranked scalar covariates after replacing the original Arm-B smoking slot with `ever_smoker`. |
| Sample support | Production model-frame n must be reported; if n falls below 700 for pooled LUAD+LUSC, the result is `[?]` regardless of coefficient or q-value. |

Sensitivity analyses are fixed in advance:

| Sensitivity | Interpretation |
|---|---|
| `pack_years_zero_never` replacing the smoking slot | Tests whether the missing-zero artifact explains the failure under a dose-like encoding. |
| Original `pack_years` | Reproduces the frozen Arm-B miss and confirms the comparison anchor. |
| LUAD-only and LUSC-only | Localizes the pooled result; neither is an alternative pass route. |
| Including all three smoking proxies simultaneously | Exploratory only, because correlated smoking encodings would make the rank denominator harder to interpret. |

Verdict mapping for this repair only:

| Result | Repair verdict | Meaning |
|---|---|---|
| Primary pass | `[+]` for repaired Arm-B recovery | Supports the claim that the frozen smoking miss was a covariate operationalization artifact. Does **not** change H08a `[?]`. |
| Positive coefficient but q ≥ 0.05 or rank > 3 | `[?]` | Direction is compatible with repair but production evidence is too weak under the locked repaired criterion. |
| Non-positive coefficient, model failure, or model-frame n < 700 | `[-]` | Weakens the t200 artifact explanation and argues against rerunning a repaired H08a gate on this substrate. |

## Null Result Plan

A null repaired result does not dispute the smoking→SBS4 biology.
It would instead mean that the t200 diagnostic result did not survive formal production insertion into the h08 rank denominator, or that the same-substrate repair is too fragile to support a gate repair.

If the primary repaired result is `[?]` or `[-]`, do not open H08b on the basis of the smoking repair.
The next move would be either to seek an independent lung substrate with valid smoking covariates or to leave H08a at `[?]` and label any H08b work exploratory.

## Suspicious/Unexpected Result Plan

Treat any of the following as suspicious until checked:

| Pattern | Required check |
|---|---|
| `ever_smoker` is all-missing or constant in lung | Re-audit raw label mapping and the non-lung nulling logic. |
| Production n differs from the t200 diagnostic n by more than 10% | Compare model-frame dropna columns and adjustment typing between `fit_cell` and the repaired production fit. |
| `ever_smoker` ranks first with an implausibly large coefficient or separation warning | Check label leakage, tissue coding, and whether sample IDs duplicated across LUAD/LUSC. |
| LUSC drives the entire pooled signal despite weak t200 LUSC diagnostic fit | Inspect per-histology fits before accepting the pooled reading. |

## Exploratory vs Confirmatory

Confirmatory scope is only the repaired `ever_smoker` primary pass in pooled LUAD+LUSC under the criteria above.
`pack_years_zero_never`, original `pack_years`, per-histology LUAD/LUSC fits, simultaneous multi-proxy smoking models, and burden-conditioned variants are exploratory or sensitivity analyses.

This repair does not authorize a post-hoc replacement of the original H08a verdict.
A future full repaired H08a gate would need its own pre-registration that decides whether to rerun all arms, replace only Arm B, add a better UV substrate, and define what evidence would be sufficient to unlock H08b.
