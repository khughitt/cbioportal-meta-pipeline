---
type: dataset
title: PanglaoDB cell-type marker database
status: candidate
created: '2026-06-07'
updated: '2026-06-27'
id: dataset:panglaodb
source_class: reference
source_refs:
- paper:Hwang2025a
- paper:Wu2025a
related:
- question:0035-label-free-neural-gene-definition
- method:length-aware-geneset-enrichment
---

# PanglaoDB cell-type marker database

## Summary

Curated single-cell marker gene sets across cell types, including neurons, glial subtypes
(astrocytes, oligodendrocytes, OPCs, Schwann cells), and neuroendocrine cells. Provides ready
**marker panels** for a label-free neural / neuroendocrine partition of genes, and a convenient
source of cell-type gene sets to test with the length-aware enrichment guard. Curated (not raw
observational), so used as a comparator/marker source rather than a primary expression atlas.

## Access and Scope

- Source URL: https://panglaodb.se/
- Organism/population: Homo sapiens / Mus musculus
- Modality: curated single-cell marker gene sets
- Role: marker panels for neural / glial / neuroendocrine cell types

## Connections to Project

- Required by: `question:0035`; gene-set source for `method:length-aware-geneset-enrichment`.
- Note: marker membership is label-adjacent — use as a comparator to the expression-derived
  score, not as the sole definition (avoids annotation circularity per q035).
- Acquisition: tracked as a search/acquire task in `tasks/active.md`.
