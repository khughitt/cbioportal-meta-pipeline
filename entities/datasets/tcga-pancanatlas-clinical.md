---
type: dataset
title: TCGA PanCanAtlas clinical-with-followup (smoking / pack-years)
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: dataset:tcga-pancanatlas-clinical
source_class: observational
origin: external
tier: use-now
license: custom
update_cadence: static
ontology_terms: []
accessions:
- GDC file UUID 0fc78496-818b-4896-bd83-52db1f533c5c (clinical_PANCAN_patient_with_followup.tsv)
access:
  level: public
  availability: available
  available_after: ''
  verified: true
  verification_method: retrieved
  last_reviewed: '2026-05-31'
  verified_by: claude (t199 WP0)
  source_url: https://api.gdc.cancer.gov/data/0fc78496-818b-4896-bd83-52db1f533c5c
  credentials_required: ''
  exception:
    mode: ''
    decision_date: ''
    followup_task: ''
    superseded_by_dataset: ''
    rationale: ''
parent_dataset: dataset:tcga-pancanatlas
siblings: []
local_path: data/pancanatlas_clinical_with_followup.tsv
consumed_by:
- plan:0007-t199-h08-association-core
source_refs:
- cite:Liu2018TCGACDR
related:
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
- dataset:tcga-pancanatlas
- task:t199
---

# TCGA PanCanAtlas clinical-with-followup (smoking / pack-years)

## Summary

The PanCanAtlas pan-cancer clinical table `clinical_PANCAN_patient_with_followup.tsv` — one row per
TCGA patient (10,956 patients × 746 fields), keyed on the 12-char `bcr_patient_barcode`, with cancer
type in the `acronym` column. It is the **only** TCGA source of `tobacco_smoking_history` and
`number_pack_years_smoked`; the per-study cBioPortal PanCanAtlas clinical (`data_clinical_patient.txt`)
does **not** carry a smoking field. It is therefore the substrate for the h08 **Arm B** smoking
covariate (`pre-registration:0003-h08-positive-control-agnostic-association-must-recover-known-signature`).

## Access and Scope

- **Open-access, no authentication.** Served from the GDC data endpoint at file UUID
  `0fc78496-818b-4896-bd83-52db1f533c5c`. (The GDC `/files` *metadata* index does not carry this
  legacy supplement object, but the `/data` *download* route serves it without auth — an earlier
  t199 review draft mis-stated it as Synapse-gated; corrected. A Synapse copy and the GerkeLab GitHub
  mirror exist as fallbacks only.)
- Modality: de-identified patient-level clinical / exposure / follow-up.
- This dataset is consistent with the standing no-gated-access constraint (it is *un-built locally*,
  not *access-controlled*).

## Access verification log

- 2026-05-31 (claude, t199 WP0): downloaded via `code/scripts/fetch_pancanatlas_clinical.py` to
  `data/pancanatlas_clinical_with_followup.tsv`. **`verified: true`** — all WP0 checks pass:
  - size = **18,633,685 B** (exact match to the GDC listing);
  - md5 = `ffcb35edda305dd8d615497f9214eb92`;
  - `tobacco_smoking_history` + `number_pack_years_smoked` columns present; `acronym` +
    `bcr_patient_barcode` present; 10,956 × 746.
  - Arm-B completeness (the §1b feed): **LUAD** n=522 — pack-years 358 (69%), smoking-history 508
    (97%); **LUSC** n=504 — pack-years 427 (85%), smoking-history 492 (98%). The lung arm is
    well-powered on the smoking-history field; pack-years is the noisier continuous covariate.
  - Encoding is latin-1 (TCGA biotab convention), not utf-8.

## Granularity at this access level

Patient-level (12-char barcode). The h08 join is patient-level for Arm B (smoking) and for ancestry;
sample-level covariates come from the per-study cBioPortal clinical and the MC3 substrate. The
realized Arm-B join n is the MC3∩(this table)∩(smoking non-missing) intersection, computed at WP1.

## Connections to Project

- Consumed by: `plan:0007-t199-h08-association-core` (WP0 → WP1 covariate join), `task:t199`.
- Variables used: `number_pack_years_smoked` (continuous), `tobacco_smoking_history` (ordinal
  indicator) — the Arm-B covariate against SBS4 within LUAD+LUSC.

## Related

- Parent: `dataset:tcga-pancanatlas`. Survival/clinical curation per `paper:Liu2018TCGACDR`.
