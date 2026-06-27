---
type: dataset
title: GENIE panel coverage and callable-size registry
status: active
created: '2026-05-31'
updated: '2026-06-27'
id: dataset:data-genie-panel-callable-registry
source_class: derived
derived_kind: transform
local_path: /data/packages/cbioportal/pan-cancer/metadata
related:
- dataset:aacr-genie
- dataset:gene-cancer-study-ratio-annotated-product
---

# GENIE Panel Coverage And Callable-Size Registry

This dataset entity covers the generated GENIE panel coverage feather and the derived callable-Mb
registry consumed by TMB and cross-study mutation-frequency rules.
The local package is written at
`results/.../metadata/genie_panel_registry/datapackage.json` by
`rule package_genie_panel_registry`.

## Package Contents

The package records the processed `genie_panel_coverage.feather` table and
`panel_callable_mb.tsv` registry with byte sizes and SHA-256 hashes.
The callable registry combines BED-derived coding coverage, configured authoritative overrides,
and WES defaults according to the active workflow configuration.

## Access

The GENIE upstream release requires a Synapse account and GENIE Data Use Agreement.
The generated registry is a local workflow artifact and should not be redistributed in a way that
violates the upstream GENIE terms.
