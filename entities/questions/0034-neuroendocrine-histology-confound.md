---
type: question
title: Do neuroendocrine-neoplasm histologies (OncoTree-flagged) inflate neuroendocrine/neural
  gene ranks, and does excluding them change the result?
status: active
created: '2026-06-06'
updated: '2026-06-28'
id: question:0034-neuroendocrine-histology-confound
ontology_terms:
- neuroendocrine neoplasm
- oncotree
- lineage marker
- cohort composition
datasets: []
source_refs:
- paper:Tan2024
- paper:Ahmed2020
- paper:Kulke2012
related:
- hypothesis:0012-neural-gene-enrichment-length-histology-artifact
- question:0033-neural-enrichment-cns-exclusion
- topic:neuroendocrine-neoplasm-lineage-confound
---

# Do neuroendocrine-neoplasm histologies inflate neuroendocrine/neural gene ranks, and does excluding them change the result?

## Summary

Neuroendocrine neoplasms (NET/NEC) are tumors *of* neuroendocrine cells and constitutively
express a neural/neuroendocrine program (CHGA, SYP, NCAM1/CD56, INSM1, ENO2) with distinct
drivers (MEN1, DAXX, ATRX; TP53/RB1 in NEC). If cBioPortal studies pool NEN histologies with
adenocarcinomas, they could mimic a "neural gene" signal. This asks whether OncoTree-based NEN
flagging and exclusion materially changes the top-mutated ranking.

## Why It Matters

- A second, distinct histology confound (separate from CNS in `question:0033`).
- MEN1 in a top-mutated list is a near-definitive marker of NEN contamination; ATRX/NF1 are
  dual CNS+NEN confounds.
- Enables a clean sensitivity stratum rather than silent contamination.

## Current Evidence

- `paper:Tan2024`: PNET drivers MEN1 (40–56%), DAXX (~25%), ATRX (~17.6%), mTOR pathway; NEC
  defined by TP53+RB1; lineage markers CHGA/SYP/NCAM1/INSM1.
- `paper:Ahmed2020`, `paper:Kulke2012`: NEN classification and lineage markers; rising incidence.

## Thoughts

- Best current interpretation: NEN inclusion inflates MEN1/DAXX/ATRX and lineage genes; its
  effect on the *specific* candidate list (LSAMP/OPCML/etc.) is probably smaller than CNS+length.
- Major uncertainty: how many pipeline studies actually contain NEN-coded samples.

## Connections to Project

- Related hypotheses: `hypothesis:0012-neural-gene-enrichment-length-histology-artifact` (P3);
  follows the CNS-exclusion check in `question:0033-neural-enrichment-cns-exclusion`.
- Required data or analyses: enumerate OncoTree codes for NET/NEC (PNET, GINET, SINET, NEC,
  PHEO, MCC, MTC, ACC, etc.) present in pipeline studies; add `is_neuroendocrine_histology`
  flag; recompute ranks with NEN excluded; check MEN1 as positive control.
- Priority level: P2

## Related

- Topic notes: topic:neuroendocrine-neoplasm-lineage-confound
- Article notes: paper:Tan2024, paper:Ahmed2020, paper:Kulke2012
- Methods/Datasets: convert_to_feather oncotree handling; cancer_type metadata
