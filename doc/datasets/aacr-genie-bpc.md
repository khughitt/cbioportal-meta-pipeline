---
id: dataset:aacr-genie-bpc
type: dataset
origin: external
title: 'AACR Project GENIE BPC (Biopharma Collaborative, PRISSMM)'
summary: Deeply phenotyped subset of AACR GENIE — targeted-panel mutations linked to
  PRISSMM-curated EHR data (treatment regimens, ICD-O histology, RECIST imaging/path/med-onc
  timelines, outcomes, vital status). The closest public EHR-adjacent substrate for agnostic
  signature-aetiology association.
tier: evaluate-next
access:
  level: controlled
  source_url: https://www.synapse.org/Synapse:syn21226493
  credentials_required: true
  verified: false
  last_reviewed: ''
accessions:
- syn21226493
license: CC-BY-NC-4.0
formats:
- maf
- tsv
- bed
size_estimate: unknown
update_cadence: versioned-releases
ontology_terms:
- MONDO:0004992
- MONDO:0005233
- MONDO:0005575
- MONDO:0007254
related:
- dataset:aacr-genie
- dataset:msk-chord
- hypothesis:h07-agnostic-covariate-association-recovers-known-signature-aetiologies-and
- topic:signature-decomposition-unmatched-normal
- topic:panel-induced-ascertainment
source_refs:
- paper:AACRGENIEConsortium2017
created: '2026-05-30'
updated: '2026-05-30'
---

# AACR Project GENIE BPC (Biopharma Collaborative, PRISSMM)

## Summary

GENIE BPC is the deeply phenotyped subset of AACR Project GENIE: a defined set of cohort
"sponsor projects" (NSCLC, CRC, breast, pancreas, bladder, prostate, …) for which the panel
mutation data of the main GENIE registry (`dataset:aacr-genie`) is augmented with
**PRISSMM-curated clinical data abstracted from the electronic health record** — treatment
regimens and lines, ICD-O histology/site coding, RECIST + imaging/pathology/med-onc event
timelines, and outcomes/vital status.

For `hypothesis:h07` it is the **EHR-covariate track**: the richest *public* source of
EHR-like, coded clinical terms co-measured with somatic mutations. Its limitation is that the
mutations are **targeted-panel** (tens of mutations/sample), so signatures can only be derived
**cohort-pooled / refit**, never per-sample (the binding mutation-count constraint, `q018`).
It is the natural complement to the **signature-grade track** (`dataset:tcga-mc3` +
`dataset:tcga-pancanatlas`), which gives per-sample WES signatures + co-measured expression
but only structured (non-EHR) clinical metadata.

## Provenance

Curated by the AACR Project GENIE Biopharma Collaborative. Clinical data follow the PRISSMM
phenomic data model (Pathology, Radiology/Imaging, Signs/Symptoms, Medical oncology, Medical
notes). Mutations inherit GENIE main-registry calling (multi-institution clinical-grade
targeted panels). Peer-reviewed origin: AACR GENIE Consortium 2017 (`paper:AACRGENIEConsortium2017`)
for the registry; the BPC cohort releases are documented per-cohort on Synapse. **[UNVERIFIED]**
exact per-cohort sample counts and the precise top-level Synapse accession (`syn21226493`
recorded as the BPC project landing — confirm at verification time).

## Access

Synapse account + AACR GENIE BPC Data Use Agreement (controlled). Released as versioned
per-cohort data files. License CC-BY-NC-4.0 (inherited from GENIE). Not auto-fetchable; must be
downloaded manually after DUA acceptance, like the main GENIE prerequisite already documented in
`AGENTS.md`.

## Variables

- **Genomic:** panel mutations (MAF), per-assay coverage BEDs (shared lineage with
  `dataset:aacr-genie`).
- **EHR-like clinical (the value for h07):** treatment regimen + line of therapy, drug names,
  ICD-O histology + primary site codes, stage, RECIST/imaging-derived response, sites of
  progression/metastasis, overall + progression-free survival, vital status.
- **Demographic:** age, sex, race (as in main GENIE).

## Integration Notes

- Join key: GENIE sample/patient IDs; mutation calling already compatible with the pipeline's
  GENIE ingest path (`process_genie_panel_coverage.py`).
- For h07, the covariate side is the PRISSMM clinical tables; signatures must be **pooled** at
  cohort level (panel footprint too small for per-sample de-novo).
- Coded terms (ICD-O, drug/regimen vocabularies) are the realistic stand-in for the user's
  "ICD-10 / words / bigrams" wish; free-text notes are *not* released (only curated phenomic
  abstractions).
- Confirm which BPC cohorts have releasable signature-usable variant calls vs coverage-only.

## Related

- Sibling / parent: `dataset:aacr-genie` (main registry; BPC is its deeply-phenotyped subset),
  `dataset:msk-chord` (the other NLP/EHR-derived substrate).
- Signature-grade complement: `dataset:tcga-mc3`, `dataset:tcga-pancanatlas`.
- Drives: `hypothesis:h07-agnostic-covariate-association-recovers-known-signature-aetiologies-and`,
  `search:2026-05-30-ehr-rich-substrates-for-agnostic-signature-association`.
- Constraint: `question:q018-can-mutational-signature-decomposition-be-added-downstream-of-the-cross`.
