---
id: "dataset:human-protein-atlas"
type: "dataset"
title: "Human Protein Atlas (tissue specificity)"
status: "proposed"
source_class: "observational"
source_refs:
  - "paper:Keough2022"
related:
  - "question:q035-label-free-neural-gene-definition"
  - "topic:cancer-neuroscience-neural-regulation"
created: "2026-06-07"
updated: "2026-06-07"
---

# Human Protein Atlas (tissue specificity)

## Summary

Multi-tissue RNA + protein expression resource with per-gene **tissue-specificity** classifications
(tissue-enriched / -enhanced / group-enriched) and consensus RNA expression. Used here to build a
**label-free brain/nerve-enrichment score** for genes (a continuous neural-enrichment covariate)
without relying on GO/human labels, and to partition CNS vs PNS vs neuroendocrine expression.

## Access and Scope

- Source URL: https://www.proteinatlas.org/
- Organism/population: Homo sapiens
- Modality: bulk + single-cell RNA, immunohistochemistry; tissue-specificity scores
- Role: tissue-specificity reference for the data-driven neural-gene definition

## Connections to Project

- Required by: `question:q035`; consumed by `method:length-aware-geneset-enrichment` (gene set `S`).
- Related: complements `dataset:gtex`; `topic:cancer-neuroscience-neural-regulation`.
- Acquisition: tracked as a search/acquire task in `tasks/active.md`.
