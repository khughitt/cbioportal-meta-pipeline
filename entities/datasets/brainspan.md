---
type: dataset
title: BrainSpan Atlas of the Developing Human Brain
status: candidate
created: '2026-06-07'
updated: '2026-06-27'
id: dataset:brainspan
source_class: observational
source_refs:
- paper:Cao2023
related:
- question:0036-oncofetal-fetal-vs-adult-neural-expression
- question:0035-label-free-neural-gene-definition
- topic:oncofetal-developmental-reprogramming
---

# BrainSpan Atlas of the Developing Human Brain

## Summary

Transcriptomic atlas spanning human prenatal-to-adult brain development (~8 pcw through
adulthood, multiple regions). Provides the **fetal-vs-adult brain expression ratio** needed to
operationalize the oncofetal (H3) test: whether a residual neural-gene enrichment is fetal/
developmental rather than adult-neural. Also a developmental-stage axis for the label-free
neural-gene score (`question:0035`).

## Access and Scope

- Source URL: https://www.brainspan.org/
- Organism/population: Homo sapiens (developing brain)
- Modality: bulk RNA-seq + exon microarray across developmental stages and regions
- Role: developmental-stage expression reference (H3 discrimination)

## Connections to Project

- Required by: `question:0036` (fetal-vs-adult), `question:0035` (developmental axis)
- Related: `topic:oncofetal-developmental-reprogramming`; complements `dataset:gtex` (adult).
- Acquisition: tracked as a search/acquire task in `tasks/active.md` (group dataset-acquisition).
