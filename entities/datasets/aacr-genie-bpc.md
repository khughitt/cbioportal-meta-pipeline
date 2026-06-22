---
type: dataset
title: AACR Project GENIE BPC (Biopharma Collaborative, PRISSMM)
status: active
created: '2026-05-30'
updated: '2026-05-30'
id: dataset:aacr-genie-bpc
source_class: observational
source_refs:
- paper:AACRGENIEConsortium2017
related:
- dataset:aacr-genie
- dataset:msk-chord
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
- topic:signature-decomposition-unmatched-normal
---

# AACR Project GENIE BPC (Biopharma Collaborative, PRISSMM)

## Summary

GENIE BPC is the deeply phenotyped subset of AACR Project GENIE (`dataset:aacr-genie`): a defined
set of cohorts (NSCLC, CRC, breast, pancreas, bladder, prostate, …) whose panel mutation data is
augmented with **PRISSMM-curated clinical data abstracted from the electronic health record** —
treatment regimens/lines, ICD-O histology + site coding, RECIST + imaging/pathology/med-onc event
timelines, and outcomes/vital status. It is the richest *public* source of EHR-like coded clinical
terms co-measured with somatic mutations, and the **EHR-covariate track** for
`hypothesis:0007`. Limitation: mutations are **targeted-panel** (tens of mutations/sample), so
signatures can only be derived **cohort-pooled / refit**, never per-sample (the binding
mutation-count constraint, `question:0018`).

## Access and Scope

- Accessions: syn21226493 (Synapse BPC project landing) [UNVERIFIED — confirm at verification]
- Source URL: https://www.synapse.org/Synapse:syn21226493
- Access: controlled (Synapse account + AACR GENIE BPC Data Use Agreement); CC-BY-NC-4.0
- Organism/population: Homo sapiens
- Modality: multi-institution targeted-panel sequencing + PRISSMM-curated EHR clinical data
- Sample size: per-cohort releases; total [UNVERIFIED]

## Connections to Project

- Questions/hypotheses it can inform: `hypothesis:0007` (EHR-covariate track),
  `question:0018` (panel signature feasibility constraint).
- Variables likely available: panel mutations; treatment regimen/line, drug names, ICD-O
  histology + primary site, stage, RECIST response, sites of progression/metastasis, OS/PFS,
  vital status; age, sex, race.
- Planned usage: cohort-pooled signature exposures × rich EHR terms; the realistic stand-in for
  the "ICD-10 / coded clinical terms" wish (free-text notes are not released — only curated
  PRISSMM phenomic abstractions).

## Related

- Sibling/parent: `dataset:aacr-genie` (main registry; BPC is its deeply-phenotyped subset),
  `dataset:msk-chord` (the other NLP/EHR-derived substrate).
- Signature-grade complement: `dataset:tcga-mc3`, `dataset:tcga-pancanatlas`.
- Scan: `search:0007-ehr-rich-substrates-for-agnostic-signature-association`.
