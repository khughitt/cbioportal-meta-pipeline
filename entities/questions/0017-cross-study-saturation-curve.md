---
type: question
title: "How does top-N gene-cancer ranking stability scale with the number of contributing\
  \ studies \u2014 is there a saturation point?"
status: active
created: '2026-04-27'
updated: '2026-04-28'
id: question:0017-cross-study-saturation-curve
ontology_terms:
- learning curve
- sample-size saturation
- meta-analysis power
datasets:
- cBioPortal per-study feathers
- AACR GENIE composite
source_refs: []
related:
- hypothesis:0002-cross-study-ranking-divergence-is-structured
- question:0013-cross-study-replication-rate
- task:t072
- task:t158
---

# Cross-study saturation curve: how many studies are enough?

## Summary

The project aggregates ~50–100 cBioPortal studies plus AACR GENIE into pan-cancer rankings.
The implicit assumption is that more studies are always better; the empirical question
is *how many studies are needed before the top-N ranking stabilizes*. A k-study ablation —
randomly subsample k of the available studies, recompute top-N, repeat — produces a
saturation curve per cancer-type and pan-cancer.

Possible regimes:
- **Early saturation:** top-25 stabilizes by k = 5–10; further studies add noise more than
  signal. Implies the project should publish per-cancer rankings only for cancer-types
  where ≥5 studies exist, and treat additional studies as robustness checks.
- **Slow saturation:** top-25 still moving at k = 50; aggregating more is genuinely
  informative. Implies external cohorts (HMF, PCAWG follow-on) are worth ingesting.
- **Cancer-type-dependent:** breast / lung / colon saturate early; rare cancers (cholangio,
  ampullary, mesothelioma) never saturate within available data. Reporting strategy must
  distinguish.

## Why It Matters

- Informs the cost-benefit of adding new studies to the pipeline. If saturation is early,
  `t-add-tcga-mc3` (already done) was the last needed bulk add for major cancer types.
- Directly relates to `h02` — the rank-stability claim depends on having enough studies for
  LOO to be meaningful. If `k_eff` < 3 for many cancer-types, LOO is statistically weak.
- Adjacent to audit F10 (cancer saturation status, tracked as `t072`), but at the
  meta-analytic level (number of studies) rather than the per-cancer-cohort level (number
  of samples).

## Current Evidence

- The pipeline runs over a fixed study set; no k-study ablation has been performed.
- t072 (saturation-aware per-cancer interpretation context column) tracks per-cancer
  cohort N saturation — but does not address the *number of studies* axis.
- The 26-tool consensus from [@Bailey2018] required combining many tools across the same TCGA
  cohorts; the analogue here would be many studies with the same tool (dNdScv).

## Thoughts

- Cheapest version: randomly subsample k from the full study set (k = 1, 2, 3, 5, 10, 20,
  all), recompute top-25 by each ranking scheme, report variance across 100 random subsets
  per k. Plot variance as a function of k. The "knee" of the curve is the saturation
  point.
- Per-cancer-type vs pan-cancer: pan-cancer is dominated by large cancers (breast, lung,
  colon) that have many studies; the saturation curve may look different per cancer-type
  for rare cancers.
- The saturation curve is a *project-level* quality metric and should be reported
  alongside any pan-cancer ranking output.

## Connections to Project

- Related hypotheses: `h02` (the saturation-curve numbers feed directly into LOO
  power / interpretability).
- Related questions: `q013` (LOO replication — same family of cross-study stability
  questions, different lens).
- Required data or analyses: existing pipeline + a k-study subsampling wrapper. Compute
  cost is moderate (need many runs); enabled by `t141` parallelization.
- Tracking task: `t158`.
- Priority level: P3. Run after `t141` parallelization lands; informs reporting strategy
  for any pan-cancer headline output.

## Related

- Topic notes: `topic:mutation-rate-normalization`.
- Article notes: meta-analysis power literature; learning-curve literature in ML.
- Methods/Datasets: existing per-study feathers; a subsampling notebook.
