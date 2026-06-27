---
type: dataset
title: Hartwig Medical Foundation (HMF) metastatic pan-cancer WGS
status: candidate
created: '2026-05-31'
updated: '2026-06-27'
id: dataset:hartwig-hmf
source_class: observational
origin: external
tier: evaluate-next
license: custom
update_cadence: versioned-releases
ontology_terms: []
accessions:
- Hartwig Medical Foundation DR-series (https://www.hartwigmedicalfoundation.nl/en/data/data-access-request/)
access:
  level: controlled
  availability: available
  available_after: ''
  verified: false
  verification_method: ''
  last_reviewed: '2026-05-31'
  verified_by: ''
  source_url: https://www.hartwigmedicalfoundation.nl/en/data/data-access-request/
  credentials_required: Data Access Request + Data Use Agreement (academic/commercial
    tiers); not downloadable without approval
  exception:
    mode: ''
    decision_date: ''
    followup_task: ''
    superseded_by_dataset: ''
    rationale: ''
siblings: []
consumed_by: []
source_refs:
- paper:Pleasance2020
related:
- hypothesis:0009-treatment-induced-signature-frequency-contamination
- topic:clinical-translational-signatures
- dataset:pcawg
---

# Hartwig Medical Foundation (HMF) metastatic pan-cancer WGS

## Summary

Whole-genome sequencing of ~5,000+ metastatic tumours with **harmonised consensus somatic calls and
linked treatment history** — the largest uniformly-processed *treatment-annotated* metastatic WGS
cohort. Its distinguishing feature for this project is the systematic prior-therapy metadata, which
makes it the ideal substrate for the treatment-induced-signature-contamination hypothesis.

## Why it matters for the project

- **Primary substrate for `hypothesis:0009`.** Treatment annotation + WGS depth lets us directly
  observe therapy signatures (SBS11/31/35/87) and quantify their burden inflation against
  treatment-naive cohorts — the contamination mechanism h10 proposes for the gene × cancer frequency
  tables.
- **WGS contrast to panel cBioPortal.** Complements `dataset:pcawg` (treatment-naive-leaning primary
  WGS) with the metastatic/treated end of the spectrum — useful for `hypothesis:0008` cross-study
  reproducibility batch modelling (assay + treatment axes).

## Access and Scope

- Access: **controlled** — requires a Hartwig Data Access Request and signed DUA; cannot be committed
  or redistributed. Treat like AACR GENIE for data-sensitivity purposes.
- Modality: whole-genome sequencing, consensus somatic SNV/indel/SV/CNV.
- Sample size: ~5,000+ metastatic tumours across many cancer types (version-dependent).
- Source: https://www.hartwigmedicalfoundation.nl/en/data/data-access-request/

## Evaluation Notes

- **Tier: evaluate-next.** High value for h10, but controlled access + DUA is a real cost; evaluate
  whether the treatment-contamination question can first be scoped on already-held treated cohorts
  (MSK-MET, relapsed cBioPortal studies) before committing to the DUA process.
- Data sensitivity: never commit HMF files to git (same posture as GENIE).

## Related

- Hypotheses: `hypothesis:0009-treatment-induced-signature-frequency-contamination`,
  `hypothesis:0008-cross-study-signature-exposure-reproducibility`
- Topics: `topic:clinical-translational-signatures`
- Datasets: `dataset:pcawg` (WGS contrast)
- Papers: `paper:Pleasance2020`
