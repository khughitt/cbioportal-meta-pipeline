---
id: "dataset:data-driver-overlay-registry"
type: "dataset"
title: "Processed driver and pathway overlay registry"
status: "active"
source_class: "derived"
derived_kind: "transform"
source_refs:
  - "paper:Bailey2018"
  - "paper:SanchezVega2018"
  - "paper:Tate2019"
related:
  - "dataset:cosmic"
  - "dataset:gene-cancer-study-ratio-annotated-product"
created: "2026-05-31"
updated: "2026-05-31"
---

# Processed Driver And Pathway Overlay Registry

This dataset entity covers the reusable processed overlay feathers used to annotate the canonical
gene-cancer outputs.
The local package is written at
`results/.../metadata/driver_overlays/datapackage.json` by
`rule package_driver_overlay_registry`.

## Package Contents

The package contains the processed Bailey 2018 driver roster, COSMIC Cancer Gene Census gene
registry, and Sanchez-Vega 2018 pathway templates.
The manifest records resource paths, byte sizes, and SHA-256 hashes so downstream projects can
verify that the annotation layer matches the source snapshot.

## Access

The upstream sources have mixed access and redistribution terms.
Bailey 2018 and Sanchez-Vega 2018 derive from article supplements; COSMIC CGC requires a COSMIC
account and is not a general redistribution asset.
Generated local overlays should therefore be shared only where the corresponding upstream terms
permit it.
