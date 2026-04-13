---
id: "article:Viechtbauer2010"
type: "article"
title: "Conducting Meta-Analyses in R with the metafor Package"
status: "active"
ontology_terms: []
datasets: []
source_refs:
  - "cite:Viechtbauer2010"
related:
  - "article:Langan2018"
  - "article:DerSimonian1986"
  - "article:Stijnen2010"
  - "topic:cross-study-meta-analysis-cancer-genomics"
created: "2026-04-13"
updated: "2026-04-13"
---

# Conducting Meta-Analyses in R with the metafor Package

- **Authors:** Viechtbauer W
- **Year:** 2010
- **Journal:** Journal of Statistical Software (Vol. 36, Issue 3)
- **DOI:** 10.18637/jss.v036.i03
- **OpenAlex:** W2139168999
- **BibTeX key:** Viechtbauer2010
- **Source:** OpenAlex (verified)

## Key Contribution

Defines the canonical R interface for meta-analysis — the `metafor` package — which has
become the de-facto tool-of-record for applied meta-analytic work. One API for fixed-effects,
random-effects, GLMM, and Mantel-Haenszel meta-analyses; a side-by-side implementation of
seven between-study-variance estimators; and built-in meta-regression, forest / funnel
plotting, and moderator analysis. 17,712+ citations.

## Methods

Software paper. Describes:

- `escalc()` — compute effect-size and variance pairs from study-level input (risk
  differences, log-OR, log-RR, mean differences, correlations, raw proportions, transformed
  proportions).
- `rma()` — the workhorse random-effects regression function. Supports DL, REML, PM, SJ, HE,
  ML, EB τ² estimators; fixed- and random-intercept moderator models; HKSJ variance
  adjustment via `test = "knha"`.
- `rma.mh()` — Mantel-Haenszel pooled effect for binary data.
- `rma.peto()` — Peto one-step OR pooling (rare events).
- `rma.glmm()` — generalised linear mixed-model meta-analysis (Stijnen 2010 approach),
  with measure arguments including `"PLO"` (pooled logit proportion), `"PR"`, `"OR"`, `"RR"`.
- Diagnostic and plotting functions: `forest()`, `funnel()`, `trimfill()`,
  `regtest()`, `ranktest()`, `predict()` (including prediction intervals).

## Key Findings (tooling-centric)

- Unified API across measure types — the same `rma()` call handles binary, continuous,
  correlation, and proportion effect sizes with measure-specific variance computation.
- All major heterogeneity estimators (DL, REML, PM, SJ, HE, ML, EB) available via a single
  argument — critical for sensitivity analysis.
- Built-in HKSJ variance adjustment (`test = "knha"`) — the modern practical default
  recommended by Langan 2018 and IntHout 2016.
- GLMM-based pooling via `rma.glmm()` directly operationalises Stijnen 2010 for
  single-proportion and two-arm binary meta-analyses.
- Meta-regression via the standard R formula interface — easy to add study-level covariates
  (panel class, cohort stage, matched-normal status) as moderators.

## Relevance

`metafor` is the specific R tool this project should adopt if meta-analytic pooling is added
to the Snakemake pipeline. All four of the anchor methods required (DL, REML, HKSJ, GLMM on
proportions) are first-class operations in one package. The paper is the citation obligation
if `metafor` appears in the pipeline's `environment.yml` and the `run_meta_analysis.R`
script's library calls.

## Project Framework Mapping

| Paper concept | Project concept | Notes |
|---|---|---|
| `escalc(measure = "PLO", xi, ni)` | Compute per-study logit proportion + variance from mutation-ratio counts | Preprocessing step before pooling. |
| `rma(yi, vi, method = "REML", test = "knha")` | Random-effects pooled estimate with HKSJ variance adjustment | Recommended default per Langan 2018. |
| `rma.glmm(measure = "PLO", xi, ni, method = "ML")` | GLMM-based pooling directly from counts, no transform needed | Recommended per Lin & Xu 2020 / Stijnen 2010. |
| `predict(rma_fit, level = 95)` | 95% prediction interval for the pooled gene-cancer rate | Per IntHout 2016 recommendation. |
| `forest()`, `funnel()` | Per-gene-per-cancer study-level plots | Optional diagnostic output. |

## Limitations

- Paper is 2010; the package has evolved substantially (multilevel models via `rma.mv`,
  location-scale models in Viechtbauer & López-López 2022). Treat the original paper as
  the citation anchor and the current [metafor documentation](https://www.metafor-project.org/)
  as the functional reference.
- R-only — not natively available in Python. If the pipeline is kept Python-only, use
  `rpy2` bridges or port to `statsmodels.meta` / Stan / PyMC equivalents (all less complete).

## Model / Tool Availability

- **R CRAN:** `install.packages("metafor")`.
- **License:** GPL-2 / GPL-3.
- **Docs:** <https://www.metafor-project.org/>.

## Follow-up

- **Langan 2018** — which τ² estimator to use.
- **Stijnen 2010** — methodological paper behind `rma.glmm`.
- **IntHout 2016** — prediction intervals and HKSJ practical guidance.
- For this project: add `metafor` to `environment.yml`; add a `code/scripts/meta_analyze_gene_cancer.R`
  that runs `rma.glmm(measure = "PLO")` per (gene, cancer) across studies.
