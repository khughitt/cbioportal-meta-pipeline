---
id: "dataset:tcga-mc3"
type: "dataset"
title: "TCGA MC3 unified MAF"
status: "active"
source_class: "derived"
derived_kind: "aggregate"
tier: "use-now"
license: "custom"
update_cadence: "static"
accessions:
  - "GDC mc3.v0.2.8.PUBLIC.maf.gz"
access:
  level: "public"
  availability: "available"
  available_after: ""
  verified: true
  verification_method: "retrieved"
  last_reviewed: "2026-06-01"
  verified_by: "codex (t201)"
  source_url: "https://gdc.cancer.gov/about-data/publications/mc3-2017"
  credentials_required: ""
  exception:
    mode: ""
    decision_date: ""
    followup_task: ""
    superseded_by_dataset: ""
    rationale: ""
local_path: "data/mc3.v0.2.8.PUBLIC.maf.gz"
source_refs:
  - "paper:Ellrott2018"
related:
  - "hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and"
consumed_by:
  - "plan:0007-t199-h08-association-core"
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

## Access verification log

- 2026-06-01 (codex, t201): verified the local prerequisite at
  `data/mc3.v0.2.8.PUBLIC.maf.gz` is present (719 MB) and that the h08 run consumed the derived
  `tcga_mc3` pseudo-study in `results/signature-h08-arms-2026-05-31/`.

## Connections to Project

- Referenced by: `paper:Ellrott2018`
- Role: external dataset cited in the project literature; see referencing papers for usage.
- Generated clean-base package: when `tcga_mc3` is present in a run config,
  `rule package_per_study_mutation_substrates` writes
  `results/.../studies/tcga_mc3/datapackage.json`.
