---
type: dataset
title: Processed driver and pathway overlay registry
status: active
created: '2026-05-31'
updated: '2026-06-27'
id: dataset:data-driver-overlay-registry
source_class: derived
derived_kind: transform
local_path: /data/packages/cbioportal/pan-cancer/metadata
source_refs:
- paper:Bailey2018
- paper:SanchezVega2018
- paper:Tate2019
related:
- dataset:cosmic
- dataset:gene-cancer-study-ratio-annotated-product
---

# Processed Driver And Pathway Overlay Registry

This dataset entity covers the reusable processed overlay feathers used to annotate the canonical
gene-cancer outputs.
The local package is written at
`results/.../metadata/driver_overlays/datapackage.json` by
`rule package_driver_overlay_registry`.

## Package Contents

The package contains the processed Bailey et al. [@Bailey2018] driver roster, COSMIC Cancer Gene Census gene
registry, and TCGA pathway templates [@SanchezVega2018].
The manifest records resource paths, byte sizes, and SHA-256 hashes so downstream projects can
verify that the annotation layer matches the source snapshot.

## Access

The upstream sources have mixed access and redistribution terms.
Bailey et al. [@Bailey2018] and the TCGA pathway templates [@SanchezVega2018] derive from article
supplements; COSMIC CGC requires a COSMIC account and is not a general redistribution asset.
Generated local overlays should therefore be shared only where the corresponding upstream terms
permit it.
