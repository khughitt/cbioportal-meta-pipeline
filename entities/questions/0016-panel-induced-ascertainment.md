---
type: question
title: Does panel-induced ascertainment confound both mutation-frequency rankings
  and literature-attention measures, creating a rich-get-richer loop?
status: active
created: '2026-04-27'
updated: '2026-06-28'
id: question:0016-panel-induced-ascertainment
ontology_terms:
- panel sequencing
- ascertainment bias
- selection bias
datasets:
- AACR GENIE panel BED files
- MSK-IMPACT (341/410/468) panel definitions
- cBioPortal per-study mutation data
- PubTator gene-mention counts
source_refs:
- paper:Bailey2018
related:
- hypothesis:0003-gene-length-confounds-literature-attention
- discussion:0001-gene-length-bias-in-mutation-rankings-and-literature
- task:t086
- task:t154
---

# Does panel-induced ascertainment confound both mutation-frequency rankings and literature attention?

Project links: this question tests a panel/callability branch of
`hypothesis:0003-gene-length-confounds-literature-attention`, drawing on
`discussion:0001-gene-length-bias-in-mutation-rankings-and-literature` and motivating `task:t086`
and `task:t154`.

## Summary

Targeted sequencing panels (MSK-IMPACT 341/410/468, FoundationOne, GENIE composite) are
designed around already-known cancer genes. A gene that is well-studied in 2010 is more
likely to be on a 2015 panel; a gene on a panel is more likely to be reported as mutated
in 2020 papers; the 2020 papers feed forward to the 2025 panel design. This is a
*rich-get-richer* loop where panel-induced ascertainment couples the mutation-frequency
ranking and literature-attention axes.

The question asks whether this loop produces a measurable confound: do panel-only studies
systematically over-represent the well-studied tail of the gene distribution relative to
WES studies of the same cancer-type, and does the gap between panel and WES top-N
correlate with the literature-attention residual identified in `h03`?

## Why It Matters

- Identifies a confounder that is *upstream* of both mutation-count and literature-attention
  axes in `h03` — without addressing it, the partial slope of length on attention is
  partially explainable as panel-induced loop, not direct length effect.
- Directly affects how panel data (~half of cBioPortal mutation samples) should be weighted
  in cross-study aggregation. If panel-only top-N is systematically narrower than WES
  top-N, panel data inflate the perceived agreement of canonical drivers.
- Has a methodological fix path: panel-coverage-aware denominator, panel-vs-WES stratified
  aggregation. The pipeline already has `build_panel_callable_sizes`; it does not yet stratify
  the rollup output by panel-vs-WES.

## Current Evidence

- AACR GENIE provides per-panel BED files; the panel target sets are known and
  enumerable.
- MSK-IMPACT panel evolution (341 → 410 → 468) targets known cancer genes; the panel
  expansions are documented and traceable to known-driver discoveries.
- The pipeline currently treats panel and WES studies symmetrically in the per-cancer
  meta-analysis (with callability correction), but the stratified analysis (panel-only
  rollup vs WES-only rollup vs combined) has not been reported.

## Thoughts

- The first analytical cut: per-cancer-type, compute the top-50 from panel-only studies
  vs the top-50 from WES-only studies (where both exist). Report Jaccard, rank-rank
  Spearman, and the gene-set difference; characterize what's in panel-only-top vs WES-only-
  top.
- Expectation: panel-only-top is enriched for the canonical set from [@Bailey2018] and Moseley/
  IMPACT panel-design genes; WES-only-top includes long-gene passengers + CFS loci that
  panels exclude. The asymmetry will quantify the panel-induced ascertainment effect.
- Connection to `h03`: compare `β_length` separately in panel-only, WES-only, and
  combined rankings. A direction or magnitude change would identify panel selection as a
  required control in the literature-attention regression, rather than treating the direct
  length effect as assay-independent.

## Connections to Project

- Related hypotheses: `h03` (panel-induced ascertainment is a candidate alternative
  explanation for the direct-length-effect claim); `h01` (panel coverage is one of the
  documented stratifiers in the contamination correction).
- Required data or analyses: per-cancer panel-vs-WES rollup; existing per-study feathers
  + GENIE panel BED files.
- Tracking task: `t154`.
- Priority level: P2 if `h03`'s formal regression goes ahead — needs to be controlled for
  in the partial-slope test. P3 otherwise.

## Related

- Topic notes: `topic:mutation-rate-normalization`.
- Article notes: [@Bailey2018] (consensus drivers — heavily panel-influenced via MSK-IMPACT
  participation); GENIE consortium documentation.
- Methods/Datasets: GENIE panel BED files; existing pipeline build_panel_callable_sizes.
