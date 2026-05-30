---
id: paper:Langan2018
type: paper
title: A comparison of heterogeneity variance estimators in simulated random-effects
  meta-analyses
status: active
ontology_terms: []
source_refs:
- paper:Langan2018
related:
- paper:Viechtbauer2010
- paper:DerSimonian1986
- paper:IntHout2016
- topic:cross-study-meta-analysis-cancer-genomics
created: '2026-04-13'
updated: '2026-04-13'
---

# A comparison of heterogeneity variance estimators in simulated random-effects meta-analyses

- **Authors:** Langan D, Higgins JPT, Jackson D, Bowden J, Veroniki AA, Kontopantelis E, Viechtbauer W, Simmonds M
- **Year:** 2018
- **Journal:** Research Synthesis Methods (Vol. 10, Issue 1, 83–98)
- **DOI:** 10.1002/jrsm.1316
- **OpenAlex:** W2885675882
- **BibTeX key:** Langan2018
- **Source:** OpenAlex (verified), PubMed cross-check [UNVERIFIED PMID]

## Key Contribution

Large simulation study comparing seven between-study variance (τ²) estimators used in
random-effects meta-analysis: DerSimonian-Laird (DL), REML, Paule-Mandel (PM), Sidik-Jonkman
(SJ), Hunter-Schmidt (HS), Hedges (HE), and maximum likelihood (ML). Provides the practical
guidance most modern meta-analysis workflows now follow.

## Methods

- Simulation across number of studies (K), within-study sample sizes, true τ² values,
  and effect-size distributions.
- Tracks bias, MSE, and coverage of the pooled-effect confidence interval (with and without
  the Hartung-Knapp-Sidik-Jonkman (HKSJ) variance adjustment).
- Effect measures simulated: standardized mean difference, log-OR, log-RR.

## Key Findings

- **DL (the historical default) is biased in small meta-analyses** and has poor CI coverage
  when τ² is non-trivial.
- **REML is generally preferred** — unbiased or near-unbiased across most scenarios,
  well-behaved MSE.
- **PM and SJ are reasonable alternatives**, especially when REML fails to converge.
- **HKSJ variance adjustment** restores nominal CI coverage for K < 30 studies under any
  τ² estimator and should be the default variance adjustment in small meta-analyses.
- The choice of τ² estimator matters more than any other single modelling decision for
  small K, and much less for large K.

## Relevance

Directly answers: **"Which random-effects method should the cbioportal pipeline use by
default?"** The paper's practical recommendation — **REML τ² estimation + HKSJ variance
adjustment** — is the current community-consensus default. For the cbioportal cross-study
pipeline the per-gene-per-cancer meta-analyses will often have K ~ 2–20 studies, exactly
the small-K regime where HKSJ matters most.

## Project Framework Mapping

| Paper concept | Project concept | Notes |
|---|---|---|
| Study (k) | cBioPortal / GENIE study (study_id) | One row per study in the per-gene long table. |
| Effect size (y_k) | Per-study logit mutation ratio (per-gene-per-cancer) | `log(p / (1-p))` with continuity correction if needed. |
| Within-study variance (σ²_k) | Binomial variance `p(1-p)/n` (after logit transform) | Delta-method variance. |
| Between-study variance (τ²) | Cross-study mutation-rate heterogeneity | Central unknown — what we currently implicitly assume is zero. |
| Random-effects estimator | `metafor::rma(..., method="REML", test="knha")` | Recommended default. |

## Limitations

- Does **not** evaluate binomial / GLMM-based pooling (Stijnen 2010) — the simulation
  framework uses normal-approximate within-study variances.
- Does not cover non-standard effect sizes (e.g., pooled prevalence on the arcsine scale).
- Bayesian alternatives not covered — see `brms` / `rstanarm` for those.

## Model / Tool Availability

All estimators evaluated are available in `metafor` (R) as arguments to `rma()`. HKSJ
variance adjustment: `test="knha"`. The simulation code accompanying the paper is
available in the published supplementary material.

## Follow-up

- **Viechtbauer 2010** — tool-of-record paper for `metafor`.
- **IntHout 2016** — HKSJ practical guidance + prediction intervals.
- **Stijnen 2010** — what to do when per-study counts are too sparse for normal-approximate
  within-study variances.
- For this project: add a `gene_cancer_study_pooled.feather` output that carries
  `rma(..., method="REML", test="knha")` pooled estimates, τ², I², and 95% prediction
  interval alongside the existing naive-sum ratio.
