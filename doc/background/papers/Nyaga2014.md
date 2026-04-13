---
id: "article:Nyaga2014"
type: "article"
title: "Metaprop: a Stata command to perform meta-analysis of binomial data"
status: "active"
ontology_terms: []
datasets: []
source_refs:
  - "cite:Nyaga2014"
related:
  - "article:Stijnen2010"
  - "article:LinXu2020"
  - "article:Barendregt2013"
  - "topic:cross-study-meta-analysis-cancer-genomics"
created: "2026-04-13"
updated: "2026-04-13"
---

# Metaprop: a Stata command to perform meta-analysis of binomial data

- **Authors:** Nyaga VN, Arbyn M, Aerts M
- **Year:** 2014
- **Journal:** Archives of Public Health (Vol. 72, Issue 39)
- **DOI:** 10.1186/2049-3258-72-39
- **OpenAlex:** W2133564174
- **BibTeX key:** Nyaga2014
- **Source:** OpenAlex (verified)

## Key Contribution

Describes `metaprop`, the Stata command that operationalises **meta-analysis of single
proportions** (no control arm per study) as a first-class procedure. Synthesises
Freeman-Tukey arcsine, logit, and GLMM approaches into one tool with proper CIs at the
study and pooled levels. This is the specific methodological problem the cbioportal project
actually has: per-study mutation ratios are single proportions, not two-arm comparisons.

## Methods

- **Input:** per-study `(events, n)` binomial counts.
- **Within-study CI options:** Wald, Wilson score, Agresti-Coull, exact (Clopper-Pearson) —
  critical for small n where Wald fails.
- **Transformation options:** raw proportion, logit (Hamza et al. 2008), double-arcsine
  (Freeman-Tukey, Barendregt 2013), or GLMM with logit link (Stijnen 2010).
- **Heterogeneity:** DL, REML, SJ, PM for τ²; Q, I², H statistics; HKSJ variance adjustment.
- **Output:** pooled proportion with CI back-transformed to the original scale, forest plot,
  per-study CIs.

## Key Findings

- **Default Wald CIs for per-study proportions are wrong** for small n or extreme p; Wilson
  / exact should be default.
- **Freeman-Tukey double-arcsine** (Barendregt 2013) produces spuriously tight pooled CIs
  near the 0/1 boundaries — consistent with Lin & Xu 2020's later critique.
- **GLMM logit-link pooling** (Stijnen 2010) is the most statistically principled of the
  four transforms but is also the slowest and can fail to converge with sparse data.
- **Logit transform with random-effects** is a reasonable middle-ground default: handles
  moderate proportions well, faster than GLMM, less biased than FTT at extremes.

## Relevance

This is the **most direct methodological peer** for what we need: a recipe for pooling
per-study single proportions (mutated-samples / total-samples) across many studies, with
proper heterogeneity statistics and choices of transform. The `metaprop` feature set
maps 1:1 onto what the cbioportal pipeline's meta-analysis output should report:

1. Per-study exact CI on the mutation ratio.
2. Pooled rate via GLMM-logit (primary) and FTT (disclosed sensitivity).
3. τ², I², Q heterogeneity statistics.
4. HKSJ-adjusted pooled CI for K < 30 studies.
5. Forest plot of per-study rates and the pooled estimate.

R equivalent: `meta::metaprop(event, n, method = "GLMM", sm = "PLOGIT")`.

## Project Framework Mapping

| Paper concept | Project concept | Notes |
|---|---|---|
| `metaprop events n` | Input row: per-(gene, cancer, study) (mutated, total) | Direct map. |
| `random` option | Random-effects (vs fixed) | Default for cross-study pooling. |
| `ftt` | Freeman-Tukey double-arcsine | Sensitivity only (per Lin & Xu 2020). |
| `logit` | Logit-link random-effects | Reasonable middle-ground default. |
| `glmm` / `mm` | GLMM logit link (Stijnen 2010) | Recommended primary. |
| `cimethod(wilson)` | Per-study Wilson CI | Default; Wald fails at small n. |

## Limitations

- Stata-only tool. R analogues: `meta::metaprop` (same author concept, different codebase),
  `metafor::rma.glmm(measure = "PLO")`. For this project we would use the R equivalents.
- Single proportions only — no two-arm comparisons. That matches the cbioportal use case
  exactly; flag if the project later adds case-control comparisons.
- Does not adjust for study-level covariates by default — extend via meta-regression on the
  logit-transform scale if needed.

## Model / Tool Availability

- **Stata:** `ssc install metaprop`.
- **R (equivalent):** `meta::metaprop(event, n, method = "Inverse" | "GLMM",
  sm = "PFT" | "PLOGIT" | "PAS" | "PRAW")`.
- **Python:** no direct equivalent; roll via `statsmodels.BinomialBayesMixedGLM` or port
  to Stan / PyMC.

## Follow-up

- **Stijnen 2010** — GLMM methodology behind the `metaprop` `glmm` option.
- **Lin & Xu 2020** — critique of the `ftt` option; recommends `glmm` as the modern default.
- **Barendregt 2013** — the FTT recipe that `ftt` operationalises.
- For this project: use R `meta::metaprop` or `metafor::rma.glmm` as the direct analogue.
  The Nyaga 2014 paper should be cited whenever we describe the single-proportion meta-analysis
  framing.
