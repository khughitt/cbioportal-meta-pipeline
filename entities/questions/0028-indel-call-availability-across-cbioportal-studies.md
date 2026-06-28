---
type: question
title: What fraction of cBioPortal/MC3 studies carry indel calls at sufficient depth
  for joint SBS+ID signature decomposition?
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: question:0028-indel-call-availability-across-cbioportal-studies
ontology_terms: []
datasets: []
source_refs:
- paper:Koh2025
- paper:FerrerTorres2025
related:
- hypothesis:0010-joint-indel-sbs-improves-aetiology-discrimination
- topic:signature-extraction-fitting-methods
- question:0020-minimum-sample-size-and-caller-provenance-for
---

# What fraction of cBioPortal/MC3 studies carry indel calls at sufficient depth for joint SBS+ID signature decomposition?

## Summary

`hypothesis:0010` is gated by indel-call availability. This question quantifies, across the corpus, which studies report indels at usable depth for joint SBS+ID decomposition (expected: WGS/MC3 yes, most panels no).

## Why It Matters

- Decision: realistic scope of any joint SBS+ID analysis and whether
  `hypothesis:0010-joint-indel-sbs-improves-aetiology-discrimination` can be tested beyond MC3/PCAWG.
- Risk: effort on a modality only a few studies support.

## Current Evidence

- `paper:Koh2025` (indel taxonomy) and `paper:FerrerTorres2025` (multimodal SBS+ID) define what adequate indel data enables.
- MC3 is consensus + indel-bearing; panels under-call indels.

## Thoughts

- Feasibility likely binary by assay class.
- Uncertainty: indel call-quality heterogeneity within the WES tier.

## Connections to Project

- Hypotheses: `hypothesis:0010-joint-indel-sbs-improves-aetiology-discrimination`.
- Analyses: per-study indel-count/depth census; ties
  `question:0020-minimum-sample-size-and-caller-provenance-for`.
- Priority: P3.

## Related

- Hypotheses: `hypothesis:0010-joint-indel-sbs-improves-aetiology-discrimination`
- Topics: `topic:signature-extraction-fitting-methods`
- Questions: `question:0020-minimum-sample-size-and-caller-provenance-for`
