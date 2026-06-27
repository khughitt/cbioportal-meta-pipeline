---
type: question
title: What is the leave-one-study-out replication rate of top-N gene-cancer associations
  across cBioPortal?
status: active
created: '2026-04-27'
updated: '2026-04-28'
id: question:0013-cross-study-replication-rate
ontology_terms: []
datasets:
- cBioPortal per-study gene_cancer_study feathers
- AACR GENIE per-panel mutation data
- Bailey et al. [@Bailey2018] 299-driver list (validation oracle)
source_refs:
- paper:Bailey2018
related:
- hypothesis:0002-cross-study-ranking-divergence-is-structured
- interpretation:0009-t131-full-pan-cancer-dndscv-run
- task:t149
---

# What is the leave-one-study-out replication rate of top-N gene-cancer associations?

## Summary

The project's flagship research question is *"which gene-cancer associations recur across
independent cBioPortal studies?"* — but no analysis to date has explicitly asked the prior
question: *do they recur, at what rate, and for which gene strata?* This question proposes
a leave-one-study-out (LOO) cross-validation protocol on the cross-study aggregation: hold
out study `s`, recompute the top-N gene-cancer table on the remaining `S\{s}` studies,
measure rank stability vs both the all-studies-included reference and the held-out study's
own ranking where powered. Repeat for each `s`. Report per-cancer-type and pan-cancer
rank-±5 stability for canonical drivers and long-tail candidates separately.

## Why It Matters

- Tests the project's central premise empirically. Currently presumed (the project produces
  a cross-study ranking; its value is implicitly the assumption that aggregation is
  worthwhile), not measured.
- Directly informs `hypothesis:0002` — the structured-divergence claim depends on a
  measured replication rate, not just a single-run output.
- Identifies which cancer types have stable enough cross-study agreement to support
  confident reporting and which require per-study attribution.
- Provides a quality metric for any future study added to the pipeline: does adding study X
  change the top-N more or less than dropping a randomly-chosen existing study?

## Current Evidence

- No project run has performed LOO yet. The closest is the t131 PoC-vs-full-run shifts in
  PubTator correlations (raw +0.127 → +0.002; dNdScv +0.055 → +0.184), which are large and
  suggestive of regime instability.
- Bailey et al. [@Bailey2018] 26-tool consensus gives an external rank-stability anchor: drivers that
  multiple tools agree on are by construction more replicable.
- Cross-study Spearman correlation of per-gene per-cancer rates is computed in the
  pipeline but not reported as a quality metric.

## Thoughts

- Compute cost is bounded — it's the existing pipeline run × number of studies. With t141
  parallelization, a full LOO sweep should be tractable.
- The partition between "canonical driver" and "long-tail candidate" is itself a choice
  that may bias the result; pre-register the partition (Bailey et al. [@Bailey2018] ∪ CGC tier 1, vs
  everything else) before running.
- Per-cancer-type LOO is more interpretable than pan-cancer LOO; pan-cancer mixes
  cancer-specific signals.
- Do not count a cancer type as evaluable unless it has at least 3 contributing studies
  after assay/matched-normal stratification. Otherwise LOO becomes a single-study influence
  diagnostic, not a replication-rate estimate.

## Connections to Project

- Related hypotheses: `hypothesis:0002-cross-study-ranking-divergence-is-structured` (this question
  provides the empirical replication-rate measurement that hypothesis depends on).
- Required data or analyses: existing pipeline (post-t141), LOO wrapper, Bailey driver
  list join.
- Tracking task: `t149`.
- Priority level: P2. Should run after t141 lands and before t146 external validation —
  a *project-internal* validation that is cheaper than the external comparison and
  informative for it.

## Related

- Topic notes: `topic:mutation-rate-normalization`.
- Article notes: Bailey et al. [@Bailey2018]; Lawrence et al. [@Lawrence2014] (long-gene-passenger pattern as the canonical
  failure of un-replicated raw rankings).
- Methods/Datasets: same per-study feathers used for the main aggregation; no new data
  required.
