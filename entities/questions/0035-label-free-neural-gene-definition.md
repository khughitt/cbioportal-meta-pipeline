---
type: question
title: Can 'neural genes' be defined purely from data (tissue/developmental expression
  enrichment) rather than human/AI labels, and is that data-driven set enriched among
  top-mutated genes beyond gene length?
status: active
created: '2026-06-06'
updated: '2026-06-06'
id: question:0035-label-free-neural-gene-definition
ontology_terms:
- tissue specificity
- expression atlas
- neural genes
- gene set enrichment
- label-free
datasets: []
source_refs:
- paper:Hwang2025a
- paper:Keough2022
- paper:Cortese2020
related:
- hypothesis:0012-neural-gene-enrichment-length-histology-artifact
- question:0032-neural-gene-length-null
- question:0036-oncofetal-fetal-vs-adult-neural-expression
---

# Can 'neural genes' be defined purely from data, and is that data-driven set enriched among top-mutated genes beyond gene length?

## Summary

The whole question of "neural-gene enrichment" depends on what counts as a neural gene. To
avoid circular reliance on curated GO/human labels, this asks whether we can define neural
genes **empirically** from tissue and cell-type expression atlases (a continuous
brain/nerve-enrichment score), then test whether high-neural-score genes are over-represented
among top-mutated genes *after* controlling for gene length and histology.

## Why It Matters

- Human/AI labels are a hint, not evidence; a data-driven definition makes the enrichment test
  falsifiable and removes annotation circularity.
- Lets us distinguish CNS-only from PNS-expressed genes (`paper:Cortese2020`), and adult- from
  fetal-neural (feeds `question:0036`).
- Produces a reusable per-gene neural-enrichment covariate for the pipeline.

## Current Evidence

- No batch paper provides a computational set, but recommendations converge: GTEx (brain +
  tibial nerve), Human Protein Atlas tissue-specificity, Allen Brain Cell Atlas, PanglaoDB /
  CellMarker markers, Neftel2019/Filbin2018 glioma OPC/NPC signatures (`paper:Keough2022`,
  `paper:Hwang2025a`).
- Project already ingests GTEx-style references in other topics (`dataset:gtex`).

## Thoughts

- Best current approach: compute a per-gene neural-enrichment z-score from GTEx/HPA (tau or
  max-tissue-Z over brain regions + nerve), validate against the canonical-effector positive
  controls, then run length+histology-adjusted enrichment of high-score genes among
  top-mutated genes. Compare to a GO-label set as sensitivity only.
- Major uncertainty: choice of atlas/threshold; CNS-structural vs PNS vs neuroendocrine
  partitions may behave differently.

## Connections to Project

- Related hypotheses: h12 (label-free commitment; P1/P4)
- Required data or analyses: build neural-enrichment score; logistic/Poisson enrichment of
  top-mutated membership ~ neural_score + log(length) + histology; ROC of score vs canonical
  effectors.
- Priority level: P2

## Related

- Topic notes: topic:cancer-neuroscience-neural-regulation, topic:oncofetal-developmental-reprogramming
- Article notes: paper:Hwang2025a, paper:Keough2022, paper:Cortese2020
- Methods/Datasets: GTEx, Human Protein Atlas, Allen Brain Cell Atlas, PanglaoDB
