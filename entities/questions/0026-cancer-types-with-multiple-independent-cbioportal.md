---
type: question
title: Which cancer types have >=2 independent cBioPortal/MC3 studies with adequate
  depth to test cross-study signature-exposure replication?
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: question:0026-cancer-types-with-multiple-independent-cbioportal
ontology_terms: []
datasets: []
source_refs:
- paper:Medo2024
- paper:Jiang2025a
related:
- hypothesis:0008-cross-study-signature-exposure-reproducibility
- topic:signature-extraction-fitting-methods
---

# Which cancer types have >=2 independent cBioPortal/MC3 studies with adequate depth to test cross-study signature-exposure replication?

## Summary

`hypothesis:0008` needs cancer types covered by multiple independent studies at adequate depth. This question is that census: per cancer type, how many independent cBioPortal/MC3 studies exist, their assay class (panel/WES/WGS), caller provenance, and treatment-exposed fraction.

## Why It Matters

- Decision: which cancer types are admissible into the
  `hypothesis:0008-cross-study-signature-exposure-reproducibility` replication analysis, and the batch covariates available per type.
- Risk: replication attempted on underpowered or technically-confounded type×study combos, conflating batch with biology.

## Current Evidence

- `paper:Medo2024`/`paper:Jiang2025a` define the depth and caller-consensus thresholds for 'adequate'.
- The project already aggregates ~300 cBioPortal studies + MC3; this is a metadata pass.

## Thoughts

- Likely a handful of common types (breast, lung, CRC, melanoma) have many independent studies; rarer types may have only one and fall out of scope.
- Uncertainty: reconstructing caller provenance from study metadata (links
  `question:0020-minimum-sample-size-and-caller-provenance-for`).

## Connections to Project

- Hypotheses: `hypothesis:0008-cross-study-signature-exposure-reproducibility`.
- Analyses: study-metadata census (assay/caller/treatment/n) per cancer type.
- Priority: P2 (gates `hypothesis:0008-cross-study-signature-exposure-reproducibility`).

## Related

- Hypotheses: `hypothesis:0008-cross-study-signature-exposure-reproducibility`
- Topics: `topic:signature-extraction-fitting-methods`
- Questions: `question:0020-minimum-sample-size-and-caller-provenance-for`
