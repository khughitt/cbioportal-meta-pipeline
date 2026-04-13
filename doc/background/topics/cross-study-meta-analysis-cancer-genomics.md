---
id: "topic:cross-study-meta-analysis-cancer-genomics"
type: "topic"
title: "Cross-study meta-analysis methods (cancer genomics)"
status: "active"
ontology_terms: []
source_refs:
  - "cite:DerSimonian1986"
  - "cite:Viechtbauer2010"
  - "cite:Langan2018"
  - "cite:Stijnen2010"
  - "cite:LinXu2020"
  - "cite:Barendregt2013"
  - "cite:Nyaga2014"
  - "cite:Higgins2002"
  - "cite:IntHout2016"
  - "cite:MartinezJimenez2020"
related:
  - "topic:cross-study-harmonization"
  - "topic:targeted-panel-sequencing-bias"
  - "topic:cohort-selection-bias-representativeness"
  - "article:Bailey2018"
  - "article:Pugh2022"
  - "article:DerSimonian1986"
  - "article:Viechtbauer2010"
  - "article:Langan2018"
  - "article:Stijnen2010"
  - "article:LinXu2020"
  - "article:Nyaga2014"
  - "article:MartinezJimenez2020"
  - "search:2026-04-13-cross-study-meta-analysis-stats"
created: "2026-04-13"
updated: "2026-04-13"
---

# Cross-study meta-analysis methods for cancer genomics

## Summary

Statistical machinery for combining evidence across independent cancer-genomics studies:
fixed- vs random-effects, effect-size combination (SumZ, Stouffer), study-level covariate
adjustment for panel composition / cohort stage / annotation version. Distinct from
`topic:cross-study-harmonization` (which is about *what biases need correcting*); this topic
is about *which statistical machinery should do the combining once the biases are known*.

## Key Concepts

- **Effect-size combination.** Per-study per-gene effect sizes (e.g., mutation rates relative
  to per-study background) combined via random-effects models with study-level covariates,
  rather than naive count pooling.
- **Random vs fixed effects.** Random-effects appropriate when study-level mutation rates are
  expected to vary (different panels, cohorts, technologies); fixed-effects only for narrow
  homogeneous comparisons.
- **Heterogeneity diagnostics.** I² and Q-statistic to quantify how much per-study estimates
  deviate from the pooled estimate. High heterogeneity invalidates simple combination.
- **Stratified pooling.** Combine within strata (panel-class × cohort-stage), then combine
  across strata with weights. Avoids strata-confounded pooled estimates.

## Current State of Knowledge

This is the **largest methodology gap in cross-study panel-based cancer genomics.** Published
consortia papers (AACR GENIE 2017, Pugh 2022, Bandlamudi 2026, Nguyen 2022) generally aggregate
counts across cohorts without explicit meta-analytic statistics. Where harmonization is
attempted (Pugh 2022's TMB harmonization model; the Bailey 2018 26-tool consensus voting), it's
rarely accompanied by published variance estimates / heterogeneity statistics.

The non-cancer meta-analytic literature (medical / behavioral / genomic — e.g.,
random-effects models per DerSimonian & Laird, REML, Bayesian hierarchical alternatives) is
mature but has not been systematically adapted to cancer-genomics cross-cohort effect sizes.

This is a documented gap — see `tasks` t027 (focused search) and t057 (develop topic on
meta-analytic stats specifically).

## Controversies & Open Questions

- **Is per-study mutation rate / ratio the right effect size, or should we use log-OR vs a
  per-study background?** Different choices give different variance estimators and different
  weights.
- **How to weight panel-of-origin?** Per-cohort sample size is the obvious weight, but small
  panels with high recurrence in their narrow gene set can produce extreme per-gene rates that
  dominate naive pooling.
- **What's the right reference background for per-study effect sizes?** Per-cohort whole-coding
  rate? Per-cancer-type expected rate? Per-gene-context expected rate (Lawrence 2014 / dNdScv
  approach)? Each gives different biological interpretation.

## Relevance to This Project

Our pipeline currently produces per-(gene, cancer, study) raw counts and ratios in long-format
tables (`summary/mut/table/*_study.feather`). The natural extension is:
1. Compute per-study per-gene effect sizes (rate / ratio with reference baseline).
2. Combine via random-effects model with study-level covariates (panel, stage).
3. Report pooled effect with heterogeneity diagnostics alongside the pooled estimate.

Step 1 is mostly there; steps 2–3 are not implemented. Adding them would put our outputs above
the 2013 methodology bar (Kandoth covariate-aware SMG) and into modern meta-analytic territory.

## Key References

Populated by the 2026-04-13 focused search
(`search:2026-04-13-cross-study-meta-analysis-stats`).

**General meta-analysis methodology (Core now):**

- **DerSimonian & Laird 1986** (`cite:DerSimonian1986`) — seminal random-effects estimator.
- **Viechtbauer 2010** (`cite:Viechtbauer2010`) — `metafor` R package, tool-of-record.
- **Langan et al. 2018** (`cite:Langan2018`) — simulation comparison of τ² estimators;
  recommends REML + HKSJ as modern default.
- **Stijnen, Hamza & Özdemir 2010** (`cite:Stijnen2010`) — GLMM framework for sparse-data
  meta-analysis; methodological foundation for pooling (events, n) counts directly.
- **Nyaga, Arbyn & Aerts 2014** (`cite:Nyaga2014`) — single-proportion meta-analysis
  (Stata `metaprop`); matches our per-study single-proportion framing.
- **Lin & Xu 2020** (`cite:LinXu2020`) — modern critique of Freeman-Tukey arcsine for
  proportions; recommends GLMM / Bayesian hierarchical alternatives.
- **Barendregt et al. 2013** (`cite:Barendregt2013`) — canonical Freeman-Tukey double-arcsine
  paper; context read for Lin & Xu 2020 critique.
- **Higgins & Thompson 2002** (`cite:Higgins2002`) — I² heterogeneity statistic.
- **IntHout et al. 2016** (`cite:IntHout2016`) — prediction intervals + HKSJ practical
  guidance.

**Cancer-genomics-native aggregation (Core now):**

- **Martínez-Jiménez et al. 2020** (`cite:MartinezJimenez2020`) — IntOGen compendium; cancer-
  genomics-native consensus-voting pipeline. Sits between naive pooling and random-effects
  meta-analysis (consensus voting rather than effect-size combination). Primary cross-reference
  when contrasting what cancer-genomics pipelines currently do vs. what random-effects pooling
  would add.

**Rare-event and sparse-data methods (Relevant next):**

- **Tsujimoto et al. 2024** (`cite:Tsujimoto2024`) — 2024 meta-epidemiological reassessment
  of continuity corrections for zero-event trials.
- **Efthimiou et al. 2019** (`cite:Efthimiou2019`) — Mantel-Haenszel network meta-analysis
  for rare events.
- **Piaget-Rossel & Taffé 2019** (`cite:PiagetRossel2019`) — homogeneous-effect framework
  for rare-event meta-analysis (contrast with random-effects).

## Recommended default for this project

Based on the 2026-04-13 search: **GLMM with logit link** on per-study (mutated-samples,
total-samples) counts (Stijnen 2010; Lin & Xu 2020; Nyaga 2014) — implemented via
`metafor::rma.glmm(measure = "PLO", method = "ML")` in R, or equivalent
`brms::brm(k | trials(n) ~ 1 + (1 | study), family = binomial)` for the Bayesian
alternative. Report pooled estimate with 95% CI (HKSJ-adjusted when K < 30), I², τ², and
a 95% prediction interval (IntHout 2016) alongside the existing naive sample-weighted
ratio. See `search:2026-04-13-cross-study-meta-analysis-stats` §Recommended Next Actions
for the full rationale.

## Known gaps (from 2026-04-13 search)

- No cancer-genomics paper found that runs per-gene-per-cancer random-effects meta-analysis.
  The IntOGen consensus-voting approach is the closest analogue. **This represents a novel
  contribution opportunity for this project.**
- HKSJ primary sources (Hartung 2001, Sidik 2005) and Paule-Mandel 1982 not individually
  retrieved; covered indirectly by Langan 2018 and IntHout 2016.
- No dedicated Bayesian-hierarchical cancer-mutation-frequency-pooling paper found; cite
  Stijnen 2010 as methods foundation and Williams/Rast/Bürkner `brms` tutorials (not
  retrieved) for implementation patterns.
