---
id: "dataset:tcga-pancanatlas"
type: "dataset"
title: "TCGA PanCanAtlas"
status: "active"
source_class: "derived"
derived_kind: "aggregate"
source_refs:
  - "paper:Bailey2018"
  - "paper:Hoadley2018"
  - "paper:Kandoth2013"
  - "paper:SanchezVega2018"
related:
  - "hypothesis:h08-agnostic-covariate-association-recovers-known-signature-aetiologies-and"
consumed_by:
  - "plan:2026-05-31-t199-h08-association-core"
created: "2026-05-30"
updated: "2026-05-31"
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

## Connections to Project

- Referenced by: `paper:Bailey2018`, `paper:Hoadley2018`, `paper:Kandoth2013`, `paper:SanchezVega2018`
- Role: external dataset cited in the project literature; see referencing papers for usage.
