---
id: "paper:Stijnen2010"
type: "paper"
title: "Random effects meta-analysis of event outcome in the framework of the generalized linear mixed model with applications in sparse data"
status: "active"
ontology_terms: []
datasets: []
source_refs:
  - "cite:Stijnen2010"
related:
  - "paper:LinXu2020"
  - "paper:Nyaga2014"
  - "paper:Viechtbauer2010"
  - "topic:cross-study-meta-analysis-cancer-genomics"
created: "2026-04-13"
updated: "2026-04-13"
---

# Random effects meta-analysis of event outcome in the framework of the generalized linear mixed model with applications in sparse data

- **Authors:** Stijnen T, Hamza TH, Özdemir P
- **Year:** 2010
- **Journal:** Statistics in Medicine
- **DOI:** 10.1002/sim.4040
- **OpenAlex:** W2148361291
- **BibTeX key:** Stijnen2010
- **Source:** OpenAlex (verified)

## Key Contribution

Frames random-effects meta-analysis of binary-event data as a **generalized linear mixed
model (GLMM)** with the exact binomial within-study likelihood plus a normal random effect
across studies. Avoids the two failures of the classical "transform-then-pool" approach:
(1) the normal-approximate within-study variance breaking down at small counts / zeros, and
(2) continuity corrections biasing the pooled estimate.

## Methods

- **Single-arm meta-analysis (proportion pooling):** random-intercept binomial GLM,
  `logit(p_k) = μ + u_k, u_k ~ N(0, τ²)`, with exact binomial likelihood for
  observed `(x_k, n_k)`.
- **Two-arm meta-analysis (OR / RR pooling):** random-intercept / random-slope binomial
  GLMM with a treatment dummy — fixed-intercept or random-intercept depending on design.
- **Beta-binomial extension:** replaces the normal-on-logit mixing distribution with a
  beta mixing distribution on the proportion scale — closed-form binomial moments,
  useful when the normal-logit assumption is itself problematic.
- Estimation: maximum likelihood via Gauss-Hermite quadrature or adaptive quadrature,
  available in SAS `NLMIXED`, Stata `meqrlogit` / `melogit`, and R `lme4::glmer` (with
  caveats) or `metafor::rma.glmm`.

## Key Findings

- **GLMM handles zero-event studies natively** — no continuity correction required, no
  study dropped.
- **Pooled estimates differ from transform-then-pool** (FTT, logit-with-Wald-variance) most
  at the extremes of the proportion range (p near 0 or 1) — i.e., exactly where cancer-genomics
  rare-gene pooling operates.
- **τ² is identifiable in one-stage GLMM** even when some studies have zero events, which
  is not true for two-stage transform-then-pool approaches that require a finite within-study
  variance estimate.
- **Beta-binomial model gives similar results** to normal-logit random-effects in most
  scenarios, but becomes meaningfully different under strong skew.

## Relevance

This is the **methodological foundation** for GLMM-based pooling of per-study
(mutated-samples, total-sequenced-samples) counts — the exact structure this project's
`gene_cancer_study.feather` produces. The Lin & Xu 2020 critique of arcsine transforms
explicitly points here as the recommended alternative. For the cbioportal pipeline, the
default per-gene-per-cancer pooling model should be:

```
rma.glmm(measure = "PLO",
         xi = mutated_samples, ni = total_samples,
         data = per_study_rows, method = "ML")
```

## Project Framework Mapping

| Paper concept | Project concept | Notes |
|---|---|---|
| Study-level event count (x_k) | `mutated_samples` per (gene, cancer, study) | Direct. |
| Study-level denominator (n_k) | `total_samples` per (gene, cancer, study) | Post gene-coverage filter. |
| Random-intercept binomial (μ + u_k) | Per-study log-odds of gene mutation | Pooled μ = overall log-odds; τ² = cross-study heterogeneity. |
| Beta-binomial mixing | Alternative pooling when normal-logit suspect | Use as sensitivity analysis. |

## Limitations

- GLMM estimation is computationally heavier than closed-form DL/REML on transformed
  proportions. For ~20k genes × ~40 cancer types × ~100 studies this matters at scale —
  parallelize across gene-cancer pairs.
- Does **not** include study-level covariate adjustment directly in the paper (panel,
  matched-normal). Natural extension: add covariates to the fixed part of the GLMM.
- Empirical Bayes prediction of study-level random effects (u_k) not discussed at length —
  useful for per-study shrinkage estimates.

## Model / Tool Availability

- **R:** `metafor::rma.glmm(measure = "PLO" | "OR" | "RR")`, `meta::metaprop(method = "GLMM")`,
  `lme4::glmer` (with `family = binomial`).
- **SAS:** `PROC NLMIXED` (the paper's reference implementation).
- **Stan / brms:** `brms::brm(k | trials(n) ~ 1 + (1 | study), family = binomial)`.
- **Stata:** `metaprop` (Nyaga 2014) with `random` and `ftt`/`logit`/`glmm` options.

## Follow-up

- **Lin & Xu 2020** — contemporary review that cites this as the recommended pooling method.
- **Nyaga 2014** — Stata wrapper that operationalises Stijnen's GLMM for single-proportion
  meta-analysis.
- For this project: Stijnen's paper is the citation anchor for the planned
  `gene_cancer_study_pooled.feather` output. Add a `random-intercept binomial GLMM` code
  path to the pipeline alongside the existing naive sample-weighted sum.
