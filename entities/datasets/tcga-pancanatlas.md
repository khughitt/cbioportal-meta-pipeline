---
type: dataset
title: TCGA PanCanAtlas
status: active
created: '2026-05-30'
updated: '2026-06-27'
id: dataset:tcga-pancanatlas
source_class: derived
derived_kind: aggregate
tier: use-now
license: custom
update_cadence: static
accessions:
- GDC PanCanAtlas publication portal
- cBioPortal TCGA PanCanAtlas 2018 study directories
access:
  level: public
  availability: available
  available_after: ''
  verified: true
  verification_method: retrieved
  last_reviewed: '2026-06-01'
  verified_by: codex (t201)
  source_url: https://gdc.cancer.gov/about-data/publications/pancanatlas
  credentials_required: ''
  exception:
    mode: ''
    decision_date: ''
    followup_task: ''
    superseded_by_dataset: ''
    rationale: ''
local_path: /data/raw/cbioportal
source_refs:
- paper:Bailey2018
- paper:Hoadley2018
- paper:Kandoth2013
- paper:SanchezVega2018
related:
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
consumed_by:
- plan:0007-t199-h08-association-core
---

# TCGA PanCanAtlas

## Summary

The PanCanAtlas harmonized re-analysis of the full TCGA cohort — uniformly processed MC3 mutations, copy number, expression, and the Bailey 2018 / Sanchez-Vega 2018 / Hoadley 2018 / Kandoth 2013 pan-cancer driver and pathway consensus products.

## Access and Scope

- Accessions: GDC PanCanAtlas (https://gdc.cancer.gov/about-data/publications/pancanatlas)
- Source URL: https://gdc.cancer.gov/about-data/publications/pancanatlas
- Organism/population: Homo sapiens
- Modality: harmonized multi-omics consensus
- Sample size: ~10,000 samples, 33 cancer types

## Access verification log

- 2026-06-01 (codex, t201): verified the PanCanAtlas study directories needed by h08 expression
  substrates are present under `/data/raw/cbioportal/`, including RSEM files for the h08 arms, and
  that the child clinical dataset `dataset:tcga-pancanatlas-clinical` was downloaded and verified by
  t199 WP0.

## Connections to Project

- Referenced by: `paper:Bailey2018`, `paper:Hoadley2018`, `paper:Kandoth2013`, `paper:SanchezVega2018`
- Role: external dataset cited in the project literature; see referencing papers for usage.
