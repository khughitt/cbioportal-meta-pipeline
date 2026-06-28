---
type: question
title: Does neural-gene enrichment persist after excluding CNS/glioma studies from
  the aggregation?
status: active
created: '2026-06-06'
updated: '2026-06-06'
id: question:0033-neural-enrichment-cns-exclusion
ontology_terms:
- glioma
- central nervous system
- cohort composition
- neural genes
datasets: []
source_refs:
- paper:Fan2024
- paper:Lu2026
related:
- hypothesis:0012-neural-gene-enrichment-length-histology-artifact
- hypothesis:0001-non-tumor-signal-contamination
- question:0032-neural-gene-length-null
---

# Does neural-gene enrichment persist after excluding CNS/glioma studies from the aggregation?

## Summary

LSAMP, OPCML, and RBFOX1 are recurrently altered in glioma. If CNS/glioma studies are
over-represented in the aggregated cohort, they could drive the pan-cancer neural-gene signal.
This asks whether the enrichment survives removal of CNS cancer types — a direct CNS-artifact test
distinct from the gene-length null.

## Why It Matters

- Separates "real pan-cancer signal" from "CNS studies leaking into the pooled ranking."
- If enrichment vanishes on CNS removal, the observation is a cohort-composition artifact.
- Peripheral-cancer literature (`paper:Fan2024`, `paper:Lu2026`) shows neural biology is *not*
  CNS-exclusive, so a surviving signal would still be interesting (but not necessarily mutational).

## Current Evidence

- `paper:Lu2026`: LSAMP/OPCML are brain-expressed, frequently mutated in glioma, and *not*
  cited as perineural-invasion actors — suggesting CNS over-representation rather than PNI biology.
- Peripheral cancers (PDAC, prostate, gastric) carry deep neural biology per Fan2024/Cortese2020.

## Thoughts

- Best current interpretation: CNS studies contribute materially; combined with length this
  may fully account for the top candidates.
- Major uncertainty: residual enrichment in specific peripheral cancer types (prostate, PDAC).

## Connections to Project

- Related hypotheses: `hypothesis:0012-neural-gene-enrichment-length-histology-artifact` (P2),
  `hypothesis:0001-non-tumor-signal-contamination`
- Required data or analyses: re-run cross-study aggregation with CNS cancer types excluded
  (OncoTree/cancer_type filter); compare neural-label enrichment and per-gene ranks; stratify
  contribution by study.
- Priority level: P2

## Related

- Topic notes: topic:cancer-neuroscience-neural-regulation
- Article notes: paper:Fan2024, paper:Lu2026
- Methods/Datasets: cross-study aggregation; cancer_type / oncotree_code metadata
