---
id: question:026-cancer-types-with-multiple-independent-cbioportal
type: question
title: Which cancer types have >=2 independent cBioPortal/MC3 studies with adequate
  depth to test cross-study signature-exposure replication?
status: active
ontology_terms: []
datasets: []
source_refs:
- paper:Medo2024
- paper:Jiang2025
related:
- hypothesis:h09-cross-study-signature-exposure-reproducibility
- topic:signature-extraction-fitting-methods
created: '2026-05-31'
updated: '2026-05-31'
---

# Which cancer types have >=2 independent cBioPortal/MC3 studies with adequate depth to test cross-study signature-exposure replication?

## Summary

`hypothesis:h09` needs cancer types covered by multiple independent studies at adequate depth. This question is that census: per cancer type, how many independent cBioPortal/MC3 studies exist, their assay class (panel/WES/WGS), caller provenance, and treatment-exposed fraction.

## Why It Matters

- Decision: which cancer types are admissible into the h09 replication analysis, and the batch covariates available per type.
- Risk: replication attempted on underpowered or technically-confounded type×study combos, conflating batch with biology.

## Current Evidence

- `paper:Medo2024`/`paper:Jiang2025` define the depth and caller-consensus thresholds for 'adequate'.
- The project already aggregates ~300 cBioPortal studies + MC3; this is a metadata pass.

## Thoughts

- Likely a handful of common types (breast, lung, CRC, melanoma) have many independent studies; rarer types may have only one and fall out of scope.
- Uncertainty: reconstructing caller provenance from study metadata (links q020).

## Connections to Project

- Hypotheses: `hypothesis:h09-...`.
- Analyses: study-metadata census (assay/caller/treatment/n) per cancer type.
- Priority: P2 (gates h09).

## Related

- Hypotheses: `hypothesis:h09-cross-study-signature-exposure-reproducibility`
- Topics: `topic:signature-extraction-fitting-methods`
- Questions: `question:q020-...`
