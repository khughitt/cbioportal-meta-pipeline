---
type: question
title: Can neuro-active drug exposure (beta-blockers, anti-epileptics, SSRIs) be captured
  as a covariate or contaminant in treatment-signature analysis?
status: active
created: '2026-06-07'
updated: '2026-06-28'
id: question:0040-neuroactive-drug-exposure-treatment-signature
ontology_terms:
- drug exposure
- treatment signature
- beta-blocker
- anti-epileptic
- covariate
datasets: []
source_refs:
- paper:Magnon2023
- paper:Fan2024
- paper:Huang2025a
related:
- hypothesis:0009-treatment-induced-signature-frequency-contamination
- question:0027-does-excluding-treatment-signature-high-samples
- topic:clinical-translational-signatures
- theme:0002-cancer-neuroscience-in-a-mutation-only-pipeline-expression-not-mutation
---

# Can neuro-active drug exposure be captured as a covariate or contaminant in treatment-signature analysis?

## Summary

The batch repeatedly flags neuro-active drugs as cancer-relevant: beta-blockers (propranolol,
carvedilol), anti-epileptics (valproate, lamotrigine), SSRIs/antidepressants, and anti-NGF
antibodies — several in oncology trials (`paper:Magnon2023`, `paper:Fan2024`, `paper:Huang2025a`).
Two of these are independently mutagenic-adjacent or repair-relevant. This asks whether
neuro-active drug exposure can be represented in the project's treatment-signature framework
(`hypothesis:0009-treatment-induced-signature-frequency-contamination`) — either as a covariate of interest or as a contaminant to control.

## Why It Matters

- The project already models treatment-induced signature contamination (`hypothesis:0009`,
  t207); neuro-active drugs are a concrete, under-considered exposure class to fold in.
- Valproate (HDAC inhibitor) and chronic adrenergic modulation plausibly interact with the
  mutational/epigenetic layer; beta-blocker use is a candidate *inverse* proxy for adrenergic
  stress (links `question:0039`).
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

- Related hypotheses: `hypothesis:0009-treatment-induced-signature-frequency-contamination` (treatment-signature contamination), and `question:0039-stress-hpa-adrenergic-mutational-footprint` (stress proxy)
- Therapy-signature exclusion companion:
  `question:0027-does-excluding-treatment-signature-high-samples`.
- Required data or analyses: enumerate neuro-active drug classes; check availability of exposure
  fields in MSK-CHORD / GENIE-BPC; add as covariate stratum in treatment-signature scans;
  beta-blocker use as inverse adrenergic-stress proxy.
- Priority level: P3 (substrate-gated)

## Related

- Topic notes: `topic:clinical-translational-signatures`,
  `theme:0002-cancer-neuroscience-in-a-mutation-only-pipeline-expression-not-mutation`
- Article notes: paper:Magnon2023, paper:Fan2024, paper:Huang2025a
- Methods/Datasets: `hypothesis:0009-treatment-induced-signature-frequency-contamination` treatment-signature pipeline; MSK-CHORD / GENIE-BPC exposure fields
