---
id: "topic:neuroendocrine-neoplasm-lineage-confound"
type: "topic"
title: "Neuroendocrine neoplasms as a histology confound (distinct from neural regulation of cancer)"
status: "active"
ontology_terms:
  - neuroendocrine neoplasm
  - lineage marker
  - oncotree
  - MEN1
  - cohort composition
source_refs:
  - "paper:Tan2024"
  - "paper:Ahmed2020"
  - "paper:Kulke2012"
related:
  - "hypothesis:h12-neural-gene-enrichment-length-histology-artifact"
  - "question:q034-neuroendocrine-histology-confound"
  - "synthesis:2026-06-06-cancer-neuroscience"
created: "2026-06-06"
updated: "2026-06-06"
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
  CNS confound (`topic:perineural-invasion-axon-guidance-genes`, `question:q033`).
- **NCAM1/CD56** elevation is a strong NEN lineage signal in expression/CNA views.

## Action

`question:q034` / task t219: enumerate NET/NEC OncoTree codes in the pipeline studies, add an
`is_neuroendocrine_histology` flag, and recompute ranks with NEN excluded as a sensitivity
stratum. This is independent of, and additive to, the CNS exclusion and the gene-length null.
