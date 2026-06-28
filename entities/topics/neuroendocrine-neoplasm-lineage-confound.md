---
type: topic
title: Neuroendocrine neoplasms as a histology confound (distinct from neural regulation
  of cancer)
status: active
created: '2026-06-06'
updated: '2026-06-28'
id: topic:neuroendocrine-neoplasm-lineage-confound
ontology_terms:
- neuroendocrine neoplasm
- lineage marker
- oncotree
- MEN1
- cohort composition
source_refs:
- paper:Tan2024
- paper:Ahmed2020
- paper:Kulke2012
related:
- hypothesis:0012-neural-gene-enrichment-length-histology-artifact
- question:0034-neuroendocrine-histology-confound
- synthesis:0015-cancer-neuroscience-literature-batch-21-papers-does-it-explain-a-neural
---

# Neuroendocrine neoplasms as a histology confound

## Scope and the key distinction

Neuroendocrine neoplasms (NEN: well-differentiated NET, poorly-differentiated NEC) are tumors
**of** neuroendocrine cells — a **different disease class** from "neural regulation of cancer."
The user asked about the "relationship to neuroendocrines"; the answer relevant to a *mutation*
meta-analysis is that NENs are primarily a **confound**, not a mechanism. Sources:
`paper:Tan2024` (GEP-NEN epidemiology/genetics — most useful), `paper:Ahmed2020` (GI-NET),
`paper:Kulke2012` (NCCN guideline).

## Driver and lineage genes (the confound signature)

- **PNET drivers:** MEN1 (40–56%), DAXX (~25%), ATRX (~17.6%), mTOR pathway (TSC1/2, PTEN,
  PIK3CA, DEPDC5), VHL, NF1.
- **SiNET:** chromosomal (chr 11/18 loss), CDKN1B (~9%), APC.
- **NEC:** TP53 + RB1 (genetically near small-cell lung cancer).
- **Lineage IHC markers:** CHGA, SYP, NCAM1/CD56, INSM1, ENO2 — *constitutive* expression of a
  neuroendocrine program, reflecting cell-of-origin, not neural co-option.

## Why it matters for the project

If cBioPortal studies pool NEN histologies with adenocarcinomas, NEN-lineage genes inflate the
top-mutated ranking and could mimic a "neural gene" signal:

- **MEN1** in a top-mutated list is a near-definitive canary for NEN contamination.
- **ATRX** and **NF1** are *dual* confounds (NEN **and** glioma) — they will co-load with the
  CNS confound (`topic:perineural-invasion-axon-guidance-genes`, `question:0033`).
- **NCAM1/CD56** elevation is a strong NEN lineage signal in expression/CNA views.

## Action

`question:0034-neuroendocrine-histology-confound` / task t219: enumerate NET/NEC OncoTree codes in the pipeline studies, add an
`is_neuroendocrine_histology` flag, and recompute ranks with NEN excluded as a sensitivity
stratum. This is independent of, and additive to, the CNS exclusion and the gene-length null.

## Project Links

This topic is one confounder arm for
`hypothesis:0012-neural-gene-enrichment-length-histology-artifact` and is summarized in
`synthesis:0015-cancer-neuroscience-literature-batch-21-papers-does-it-explain-a-neural`.

## Summary

This topic note is currently a concise project-facing record; the existing sections above carry the substantive synthesis until a fuller rewrite is warranted.

## Key Concepts

The key concepts are defined in the existing prose above and in the linked project entities; this section is present to keep the topic aligned with the current Science topic template.

## Current State of Knowledge

The current project-facing state of knowledge is summarized in the existing prose above. No additional confidence upgrade is made by this structural section.

## Relevance to This Project

This topic is relevant through the linked questions, hypotheses, datasets, and source references in the frontmatter and in the note above.

## Key References

Key references are listed in `source_refs` and cited in the note above.
