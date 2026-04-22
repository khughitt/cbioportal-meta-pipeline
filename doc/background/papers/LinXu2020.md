---
id: "paper:LinXu2020"
type: "paper"
title: "Arcsine-based transformations for meta-analysis of proportions: Pros, cons, and alternatives"
status: "active"
ontology_terms: []
datasets: []
source_refs:
  - "paper:LinXu2020"
related:
  - "paper:Barendregt2013"
  - "paper:Stijnen2010"
  - "paper:Nyaga2014"
  - "topic:cross-study-meta-analysis-cancer-genomics"
created: "2026-04-13"
updated: "2026-04-13"
---

# Arcsine-based transformations for meta-analysis of proportions: Pros, cons, and alternatives

- **Authors:** Lin L, Xu C
- **Year:** 2020
- **Journal:** Health Science Reports
- **DOI:** 10.1002/hsr2.178
- **OpenAlex:** W3044366033
- **BibTeX key:** LinXu2020
- **Source:** OpenAlex (verified)

## Key Contribution

Systematic critique of Freeman-Tukey double-arcsine (FTT) and related arcsine-based
transformations for meta-analysis of proportions (Barendregt 2013). Argues that the standard
arcsine-pooling recipe is statistically unsound in common scenarios and recommends
**generalized linear mixed models (GLMMs) with logit link** or **Bayesian hierarchical models**
as the current-generation default.

## Methods

Analytic + numerical-illustration review comparing four proportion-pooling approaches on
representative datasets:

1. Untransformed proportions with fixed- or random-effects.
2. Logit transform with normal-approximate within-study variance.
3. Freeman-Tukey double-arcsine (Barendregt 2013 recipe).
4. GLMM with logit link (Stijnen 2010) / Bayesian hierarchical alternative.

## Key Findings

- **FTT's back-transformation is ill-defined** when the pooled arcsine value is near the
  boundary — the resulting pooled proportion can differ markedly from the estimate on the
  original scale, especially for proportions near 0 or 1 (exactly the rare-gene regime in
  cancer meta-analysis).
- **Arcsine stabilisation of the variance is exact only at the true proportion** — weights
  depend on the unknown true rate, which the method pretends is observed.
- **Logit transforms** are better behaved for moderate proportions but fail badly at 0%/100%.
- **GLMMs with logit link** (i.e. random-intercept binomial regression) handle zeros natively,
  do not require a continuity correction, and produce a pooled estimate on the logit scale
  that back-transforms unambiguously.
- **Bayesian hierarchical models** (e.g. Stan / brms random-intercept binomial) give the same
  asymptotic behaviour as GLMMs but provide posterior credible intervals and easily
  accommodate study-level covariates (panel, cohort, matched-normal status).

## Relevance

Directly shapes the cbioportal pipeline's choice of pooling transform. The project is exactly
in the rare-event / boundary regime where FTT fails: many genes have 0 or 1 mutated sample in
some studies. The paper's recommendation to use **GLMM with logit link** maps cleanly onto
`metafor::rma.glmm(measure="PLO")` (R) or `brms::brm(mutated | trials(sequenced) ~ 1 + (1 |
study), family = binomial)` (Bayesian alternative).

## Project Framework Mapping

| Paper concept | Project concept | Notes |
|---|---|---|
| Per-study proportion (p_k) | per-(gene, cancer, study) mutation ratio | `mutated_samples / total_samples`. |
| Proportion near 0/1 | Rare or near-universal mutated gene | TP53 in LUSC near the upper boundary; most long-tail genes near 0. |
| FTT back-transformation ambiguity | The pooled ratio artefact when we average arcsine values across studies | Primary reason to avoid naive FTT in the pipeline. |
| GLMM logit link | `rma.glmm(measure="PLO")` in metafor / `brms` random-intercept binomial | Recommended default. |

## Limitations

- Review paper — no new simulation framework; relies on illustrative examples.
- Does not specifically address panel-composition heterogeneity (gene-level coverage varies
  across studies), which is a cbioportal-specific wrinkle on top of the general
  meta-analysis-of-proportions problem.

## Model / Tool Availability

- **R:** `metafor::rma.glmm(measure="PLO", ...)`, `meta::metaprop(..., method="GLMM")`.
- **Python:** no first-class GLMM meta-analysis library; bespoke `statsmodels` BinomialBayesMixedGLM
  or hand-rolled PyMC random-intercept binomial.
- **Stan / brms (R):** `brms::brm(k | trials(n) ~ 1 + (1 | study), family = binomial)`.

## Follow-up

- **Stijnen 2010** — GLMM-based pooling methods foundation.
- **Nyaga 2014** — single-proportion meta-analysis recipe (Stata metaprop, R equivalent).
- **Barendregt 2013** — the arcsine approach this paper critiques; context read only.
- For this project: adopt GLMM-logit as the default pooling transform; retain FTT as a
  disclosed-alternative sensitivity analysis only.
