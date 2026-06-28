---
type: question
title: How should multi-cancer dNdScv signals be aggregated into a per-gene pan-cancer
  ranking when BH-FDR floors out for hundreds of genes?
status: active
created: '2026-04-27'
updated: '2026-06-28'
id: question:0015-pan-cancer-aggregator-choice
ontology_terms:
- meta-analysis
- multiple-testing correction
- rank aggregation
datasets:
- cBioPortal per-cancer dNdScv feathers
- AACR GENIE pan-cancer dNdScv outputs
source_refs:
- paper:Martincorena2017
related:
- interpretation:0009-t131-full-pan-cancer-dndscv-run
- hypothesis:0002-cross-study-ranking-divergence-is-structured
- task:t144
- task:t155
---

# How should multi-cancer dNdScv signals be aggregated when BH-FDR floors out?

Project links: this question is tied to
`hypothesis:0002-cross-study-ranking-divergence-is-structured`,
`interpretation:0009-t131-full-pan-cancer-dndscv-run`, `task:t144`, and `task:t155`.

## Summary

At full pan-cancer scale, BH-FDR-adjusted q-values for hundreds of genes underflow to
exactly 0 (829 genes in the t131 run). The current per-gene rollup (`min_qglobal`) cannot
distinguish among them; the t144 fix added `n_cancers_significant_q05` as a tiebreaker and
recovered canonical drivers, but this is one choice among several plausible aggregators.
The question asks: which aggregator best discriminates among q=0 genes, is most stable
under leave-one-cancer-out, and is theoretically defensible?

Candidate aggregators include:
- `(min_qglobal ASC, n_cancers_significant_q05 DESC)` lexicographic (current t144 fix)
- Stouffer's combined log10(q) — sum of -log10(q) across cancers, with weight by sample size
- Inverse-variance-weighted mean log10(q) (Fisher / Stouffer family)
- Ordinal pooling — rank-of-min-rank across cancers (robust to scale differences)
- Maximum likelihood per-gene fit across cancers (one-step meta-analysis)
- Bayesian hierarchical fit per gene (random-effects across cancers)

## Why It Matters

- Determines what "the cross-study answer" *is* when the project reports a single pan-cancer
  driver list. Currently this choice is buried in `aggregate_dndscv_per_gene.py`; it
  deserves to be a pre-registered methodological choice with a defensible rationale.
- Directly affects `h02` (structured divergence) — different aggregators may disagree on
  which canonical drivers rank first vs which long-tail candidates survive.
- The 829-gene q=0 pile-up is a regime-specific phenomenon (large sample sizes) — at PoC
  scale, fewer genes hit the floor and the choice of aggregator matters less.

## Current Evidence

- t131 + t144: lexicographic `(min_q, -n_cancers)` recovered 14/15 canonical drivers in
  top-15 (vs 2/10 with alphabetical tiebreak). Direct evidence that aggregator choice
  matters.
- Standard meta-analysis literature (Stouffer, Fisher, inverse-variance) provides
  established alternatives with theoretical foundations.
- No published consensus on rollup choice for dNdScv pan-cancer aggregation specifically.

## Thoughts

- The first cut: cheap to evaluate. All candidate aggregators can be computed from the
  existing per-cancer dNdScv feather (`gene_cancer_pooled.feather`) — no re-run of the
  upstream R chain is needed.
- Pre-register the comparison protocol: rank-rank Spearman among aggregators, leave-one-
  cancer-out stability, recovery of drivers from [@Bailey2018], agreement with IntOGen pan-cancer.
- The right answer may be different at different N — for top-25 (canonical-driver regime),
  the aggregators may agree; for top-100+ (candidate regime), they may diverge.

## Connections to Project

- Related hypotheses: `h02-cross-study-ranking-divergence-is-structured` (the aggregator
  choice is itself a methodological factor in observed structured divergence).
- Required data or analyses: existing `gene_cancer_pooled.feather`; aggregator-comparison
  notebook (marimo).
- Tracking task: `t155`.
- Priority level: P3. Important for headline-quality output but not blocking; can run any
  time after t144 is in.

## Related

- Topic notes: `topic:mutation-rate-normalization`.
- Article notes: [@Martincorena2017] (dNdScv methodology — note the original is per-tissue,
  not pan-cancer); meta-analysis textbooks (Borenstein 2009 *Introduction to Meta-Analysis*).
- Methods/Datasets: `gene_cancer_pooled.feather`; per-cancer Bailey overlap as validation.
