---
id: "dataset:tcga-mc3"
type: "dataset"
title: "TCGA MC3 unified MAF"
status: "active"
source_class: "derived"
derived_kind: "aggregate"
source_refs:
  - "paper:Ellrott2018"
related:
  - "hypothesis:h08-agnostic-covariate-association-recovers-known-signature-aetiologies-and"
consumed_by:
  - "plan:2026-05-31-t199-h08-association-core"
created: "2026-05-30"
updated: "2026-05-31"
---

# TCGA MC3 unified MAF

## Summary

Ellrott 2018 Multi-Center Mutation Calling in Multiple Cancers (MC3) — a single 7-caller consensus somatic MAF across the TCGA cohort (~3.6M variants / ~10,000 samples), ingested by this pipeline as the pseudo-study `tcga_mc3`.

## Access and Scope

- Accessions: syn7214402 (Synapse); GDC mc3.v0.2.8.PUBLIC.maf.gz
- Source URL: https://gdc.cancer.gov/about-data/publications/mc3-2017
- Organism/population: Homo sapiens
- Modality: consensus somatic MAF (WES)
- Sample size: ~3.6M variants, ~10,000 samples, 33 cancer types

## Connections to Project

- Referenced by: `paper:Ellrott2018`
- Role: external dataset cited in the project literature; see referencing papers for usage.
- Generated clean-base package: when `tcga_mc3` is present in a run config,
  `rule package_per_study_mutation_substrates` writes
  `results/.../studies/tcga_mc3/datapackage.json`.
