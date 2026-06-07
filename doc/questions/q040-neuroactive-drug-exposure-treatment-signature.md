---
id: "question:q040-neuroactive-drug-exposure-treatment-signature"
type: "question"
title: "Can neuro-active drug exposure (beta-blockers, anti-epileptics, SSRIs) be captured as a covariate or contaminant in treatment-signature analysis?"
status: "active"
ontology_terms:
  - drug exposure
  - treatment signature
  - beta-blocker
  - anti-epileptic
  - covariate
datasets: []
source_refs:
  - "paper:Magnon2023"
  - "paper:Fan2024"
  - "paper:Huang2025"
related:
  - "hypothesis:h10-treatment-induced-signature-frequency-contamination"
  - "question:q027-does-excluding-treatment-signature-high-samples"
  - "topic:clinical-translational-signatures"
  - "theme:cancer-neuroscience-in-a-mutation-only-pipeline"
created: "2026-06-07"
updated: "2026-06-07"
---

# Can neuro-active drug exposure be captured as a covariate or contaminant in treatment-signature analysis?

## Summary

The batch repeatedly flags neuro-active drugs as cancer-relevant: beta-blockers (propranolol,
carvedilol), anti-epileptics (valproate, lamotrigine), SSRIs/antidepressants, and anti-NGF
antibodies — several in oncology trials (`paper:Magnon2023`, `paper:Fan2024`, `paper:Huang2025`).
Two of these are independently mutagenic-adjacent or repair-relevant. This asks whether
neuro-active drug exposure can be represented in the project's treatment-signature framework
(h10) — either as a covariate of interest or as a contaminant to control.

## Why It Matters

- The project already models treatment-induced signature contamination (`hypothesis:h10`,
  t207); neuro-active drugs are a concrete, under-considered exposure class to fold in.
- Valproate (HDAC inhibitor) and chronic adrenergic modulation plausibly interact with the
  mutational/epigenetic layer; beta-blocker use is a candidate *inverse* proxy for adrenergic
  stress (links `question:q039`).
- Risk if unanswered: an exposure class that is neither modeled as covariate nor excluded.

## Current Evidence

- `paper:Magnon2023` Table 1: ~12 trials repurposing beta-blockers, antidepressants, valproate,
  anti-cholinergics, anti-NGF across cancer types.
- No mutational-signature data for these drugs in the batch; the temozolomide precedent
  (project Crisafulli2022) shows therapy *can* leave SBS/ID footprints.

## Thoughts

- Best current interpretation: most neuro-active drugs are unlikely to leave a strong direct
  mutational signature (unlike alkylators), but exposure is a useful covariate and a stress proxy.
- Major uncertainty: drug-exposure metadata is sparse in cBioPortal; needs an EHR-rich substrate.

## Connections to Project

- Related hypotheses: h10 (treatment-signature contamination), and q039 (stress proxy)
- Required data or analyses: enumerate neuro-active drug classes; check availability of exposure
  fields in MSK-CHORD / GENIE-BPC; add as covariate stratum in treatment-signature scans;
  beta-blocker use as inverse adrenergic-stress proxy.
- Priority level: P3 (substrate-gated)

## Related

- Topic notes: topic:clinical-translational-signatures
- Article notes: paper:Magnon2023, paper:Fan2024, paper:Huang2025
- Methods/Datasets: h10 treatment-signature pipeline; MSK-CHORD / GENIE-BPC exposure fields
