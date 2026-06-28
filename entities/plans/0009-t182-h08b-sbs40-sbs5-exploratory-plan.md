---
type: plan
title: t182 h08b exploratory SBS40-vs-SBS5 expression-module prototype
status: ready-with-caveats
created: '2026-06-01'
updated: '2026-06-01'
id: plan:0009-t182-h08b-sbs40-sbs5-exploratory-plan
related:
- task:t182
- task:t205
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
- question:0023-sbs40-vs-sbs5-clocklike-expression-module
- question:0025-causal-direction-guard-for-expression-signature
- method:h08-agnostic-association-model
- discussion:0005-h08b-gate-handling
source_refs:
- paper:Hakobyan2024
- paper:Luo2023a
- paper:Spisak2025
---

# t182 h08b exploratory SBS40-vs-SBS5 expression-module prototype

## Analysis Question

Can the existing `hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and` expression-module substrate produce a coherent exploratory separation between SBS40 and SBS5 within tissue after conditioning on age?

This is not a confirmatory discovery-prong analysis.
Per `discussion:0005-h08b-gate-handling`, the positive-control prong remains `[?]`, the repaired smoking-arm read remains `[?]`, and discovery-prong output cannot promote the hypothesis.

## Related Hypotheses / Questions / Tasks

This plan executes `task:t182`.
It bears on `question:0023-sbs40-vs-sbs5-clocklike-expression-module` and must obey the causal-direction guard in `question:0025-causal-direction-guard-for-expression-signature`.

The result should be read as feasibility evidence for the future discovery-prong design space, not as evidence that an expression module causes SBS40 or SBS5.

## Data Inputs and Provenance

Inputs are all from the existing association run bundle under `results/signature-h08-arms-2026-05-31/`.

- `association/h08_covariates.feather`: MC3-overlapping clinical and molecular covariates, including per-arm NMF module loadings.
- `association/covariate_denominator.json`: active-signature and ranked-covariate manifest.
- `studies/tcga_mc3/mut/signatures/restricted_assignment_per_sample.feather`: per-sample restricted SBS exposures with t178/t179 audit columns.
- `expression_modules/<ARM>/nmf_sample_loadings.feather`: frozen per-arm NMF loadings, already copied into `h08_covariates.feather`.
- `data_dir / h08_arm_studies["LUAD"] / data_mrna_seq_v2_rsem.txt`: LUAD RSEM matrix for the `REV3L` / `POLZ` targeted check.

Pre-run inspection found `REV3L` in LUAD RSEM and did not find `POLZ`.
The implementation should report `POLZ` as `not_evaluable_missing_expression_row` rather than imputing, aliasing, or silently skipping it.

## Required Input Inspection

Before fitting, the script must report:

- per tissue: total MC3 samples, count-floor-passing samples, matched module-loading samples, and final model-frame n after age/ancestry/treatment dropna;
- which SBS40 components are active by manifest in each tissue;
- whether SBS5 and at least one SBS40 component are active in each tissue;
- `REV3L` / `POLZ` availability in LUAD RSEM;
- denominator SHA256 for `covariate_denominator.json`.

Strata lacking SBS5 or any active SBS40 component should be recorded as `not_evaluable`, not dropped without trace.

## Preprocessing / Normalization Checks

SBS40 should be collapsed within each stratum as the sum of active SBS40 components in that stratum's manifest.
SBS5 remains its own component.

The primary outcome is the age-conditioned compositional contrast:

```text
clr_SBS40_minus_SBS5 = clr(SBS40_collapsed) - clr(SBS5)
```

The CLR basis is the stratum's manifest active-signature composition after the active-signature collapse rules and the existing pseudocount convention.
This contrast is a log-ratio-scale separation read rather than an absolute-burden claim.

Secondary descriptive outcomes are `clr_SBS40` and `clr_SBS5` fit separately.
These help distinguish a true differential contrast from a broad clock-like module that tracks both components.

Module covariates are the existing non-negative NMF sample loadings.
Each fitted covariate is z-scored in the model frame.
Age is z-scored and treated as a required numeric adjustment, not a ranked target.

## Independent Unit and Denominator

The independent unit is one MC3 tumor sample with trusted SBS exposure and co-measured expression-module loading.
Samples are restricted to `passes_count_floor == True`.

The screening denominator is not the H08a confirmatory denominator.
It is the exploratory set of estimable `(tissue, module, outcome)` cells plus the separate LUAD targeted-gene cells.

## Estimand and Primary Metric

The estimand is the within-tissue adjusted association between an expression-module loading and the SBS40-vs-SBS5 CLR contrast.

The primary metric is the standardized coefficient for a module in:

```text
clr_SBS40_minus_SBS5 ~ z(module) + z(age) + C(ancestry) + treatment
```

The primary screen ranks module cells by BH-adjusted p value and absolute standardized coefficient.
There is no pass/fail promotion criterion.

## Model / Test Assumptions

The prototype uses ordinary least squares, matching the association-layer convention.
The model is descriptive and exploratory.

A cell is estimable only if:

- model-frame n is at least 100;
- the module or target-gene covariate has at least two distinct non-missing values;
- age is available after all-column dropna;
- the outcome is finite for all model-frame rows.

Adjustment terms are:

- `z(age)` as required clock-like confounder control;
- `C(ancestry)` when at least two levels remain after dropna;
- `treatment` when at least two values remain after dropna.

## Power Floor or Resolution Limit

The prototype has limited resolution because SBS40 components are sparse in several strata and median SBS40 exposure is often zero.
The CLR pseudocount stabilizes the contrast but also means low-burden strata can be pseudocount-sensitive.

The output must report final model-frame n per cell and should treat small-n or sparse-SBS40 hits as triage candidates only.
No finding from this prototype can be used as confirmatory evidence.

## Bias vs Variance Risks

The major bias risks are:

- reverse causation: signature-generating mutations may remodel expression modules;
- tissue collinearity: avoided by per-tissue fits, but not solved for subtypes within tissue;
- age confounding: handled by required age adjustment, but age is a noisy proxy for clock-like mutation opportunity;
- module non-commensurability: NMF bases differ by tissue, so pooled module effects are invalid;
- signature attribution uncertainty: SBS40 and SBS5 are flat, sparse, and partly confounded by assignment uncertainty.

The major variance risk is that per-tissue module screens have moderate n but many exploratory cells.
The plan reports BH q values as descriptive triage, not as discovery proof.

## Sensitivity Arbitration

The primary read is `clr_SBS40_minus_SBS5`.

Secondary reads are:

- separate `clr_SBS40` and `clr_SBS5` fits for the same module;
- LUAD `REV3L` targeted expression against `clr_SBS5` and the SBS40-vs-SBS5 contrast;
- `POLZ` targeted expression only if a valid RSEM row exists.

Interpretation rules:

- A module with low q on the contrast but similar-direction effects on both separate outcomes is a broad clock-like module, not SBS40/SBS5 separation.
- A module with low q on the contrast and divergent separate-outcome effects is a candidate-bearing exploratory signal.
- A LUAD `REV3L` signal is a mechanistic candidate only at the hypothesis-generating layer.
- Missing `POLZ` is a data limitation, not a negative biological result.

## Required Output Artifacts

Add one script:

- `code/scripts/run_h08b_sbs40_sbs5_prototype.py`

Write outputs under:

- `results/signature-h08-arms-2026-05-31/association/exploratory/h08b_sbs40_sbs5/`

Required files:

- `h08b_sbs40_sbs5_module_contrast.feather`
- `h08b_sbs40_sbs5_target_genes.feather`
- `h08b_sbs40_sbs5.meta.json`

Write one interpretation:

- `doc/interpretations/2026-06-01-t182-h08b-sbs40-sbs5-prototype.md`

The interpretation must lead with the exploratory-only constraint and must not update H08a or promote H08b.

## Validation

Add focused tests for:

- SBS40 component collapse uses only active manifest SBS40 parts;
- the primary outcome equals `clr_SBS40 - clr_SBS5`;
- age is included as a numeric adjustment and n is reported after all-column dropna;
- missing `POLZ` yields a `not_evaluable` row;
- BH q values are monotone.

Run:

```bash
uv run --frozen pytest code/scripts/tests/test_run_h08b_sbs40_sbs5_prototype.py
uv run --frozen ruff check code/scripts/run_h08b_sbs40_sbs5_prototype.py code/scripts/tests/test_run_h08b_sbs40_sbs5_prototype.py
uv run --frozen ruff format --check code/scripts/run_h08b_sbs40_sbs5_prototype.py code/scripts/tests/test_run_h08b_sbs40_sbs5_prototype.py
uv run --frozen science validate --verbose
```

## Readiness Decision

`ready-with-caveats`.

The required substrate exists and the analysis is executable without new data.
The caveat is epistemic: the result is an exploratory feasibility screen under a failed H08a gate.
It can rank candidates and expose whether SBS40/SBS5 module separation is even visible, but it cannot support an upstream-cause claim or H08b promotion.

## Feedback Reflection

The Science plan-analysis template asks for `type: analysis-plan`, but this project currently warns on `analysis-plan` as an unknown graph kind.
This document uses `type: plan` to avoid adding a new validation warning while preserving the analysis-readiness sections.
