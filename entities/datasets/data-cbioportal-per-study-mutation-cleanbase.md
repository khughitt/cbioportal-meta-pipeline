---
type: dataset
title: Generated cBioPortal per-study mutation clean-base substrates
status: active
created: '2026-05-31'
updated: '2026-06-27'
id: dataset:data-cbioportal-per-study-mutation-cleanbase
source_class: derived
dataset_class: deposit
derived_kind: transform
local_path: /data/packages/cbioportal/pan-cancer/studies
related:
- dataset:cbioportal
- dataset:tcga-mc3
- dataset:gene-cancer-study-ratio-annotated-product
---

# Generated cBioPortal per-study mutation clean-base substrates

This dataset entity describes the reusable per-study clean feathers emitted by the mutation ingest
workflow, not the raw cBioPortal downloads.
Each configured study gets a local manifest at
`results/.../studies/{study_id}/datapackage.json` from
`rule package_per_study_mutation_substrates`.

## Package Contents

Each package records the generated mutation table, sample table, patient table, study metadata,
genome-build token, and mutation-substrate QA report.
The manifest records byte sizes and SHA-256 hashes for these generated files.

## Access

The source data are public cBioPortal study downloads when the upstream study permits public
redistribution, but the generated package remains a local workflow artifact.
Do not treat the manifest as a license grant; follow the source study terms and cBioPortal terms
for redistribution.

## Scope

These packages are intended as reusable clean-base substrates for downstream mutation-frequency,
signature, and selection analyses.
They exclude project-specific aggregate products, exploratory branches, and ad hoc notebook
outputs.
Their main project-level dataset links are `dataset:cbioportal`, `dataset:tcga-mc3`, and
`dataset:gene-cancer-study-ratio-annotated-product`.
