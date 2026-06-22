---
type: dataset
title: Allen Brain Cell Atlas
status: proposed
created: '2026-06-07'
updated: '2026-06-07'
id: dataset:allen-brain-cell-atlas
source_class: observational
source_refs:
- paper:Hwang2025a
- paper:Keough2022
related:
- question:0035-label-free-neural-gene-definition
- topic:cancer-neuroscience-neural-regulation
---

# Allen Brain Cell Atlas

## Summary

Single-cell reference transcriptomes for CNS cell types (neuronal subtypes, OPCs, astrocytes,
microglia, oligodendrocytes). Provides **cell-type marker gene sets** for a label-free neural-gene
definition — notably the OPC/NPC programs that the cancer-neuroscience literature links to
malignant glioma states (`paper:Keough2022`, Neftel2019/Filbin2018). Used to score genes by neural
cell-type specificity without GO labels.

## Access and Scope

- Source URL: https://portal.brain-map.org/ (Allen Brain Cell Atlas)
- Organism/population: Homo sapiens / Mus musculus (brain)
- Modality: single-cell / single-nucleus RNA-seq; cell-type taxonomies
- Role: cell-type marker reference for neural-enrichment scoring

## Connections to Project

- Required by: `question:0035`; second view alongside GTEx/HPA tissue specificity.
- Related: `topic:cancer-neuroscience-neural-regulation`.
- Acquisition: tracked as a search/acquire task in `tasks/active.md`.
