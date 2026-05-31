---
id: "dataset:pcawg"
type: "dataset"
title: "ICGC/TCGA PCAWG"
status: "active"
source_class: "observational"
tier: "evaluate-next"
source_refs:
  - "paper:PCAWG2020"
  - "paper:Yaacov2023"
  - "paper:Alexandrov2020"
related:
  - hypothesis:h08-agnostic-covariate-association-recovers-known-signature-aetiologies-and
  - hypothesis:h09-cross-study-signature-exposure-reproducibility
  - hypothesis:h11-joint-indel-sbs-improves-aetiology-discrimination
  - topic:pan-cancer-signature-catalogs
  - topic:signature-topography-genomic-features
created: "2026-05-30"
updated: "2026-05-31"
---

# ICGC/TCGA PCAWG

## Summary

Pan-Cancer Analysis of Whole Genomes — whole-genome sequencing of ~2,800 tumors across 38 cancer types with consensus somatic SNV/indel/SV/CNV calls; the reference WGS pan-cancer cohort for mutational signatures and non-coding drivers.

## Role for the signature thread (h08/h09/h11)

PCAWG is the **WGS signature gold standard** for the project: it is the substrate on which COSMIC v3
signatures were defined (`paper:Alexandrov2020`) and carries genome-wide SBS+indel+SV+CN calls at
depth the panel/WES cBioPortal corpus cannot reach. It is therefore the natural cross-validation
reference for (a) checking that panel/WES signature calls recover the WGS-defined map
(`hypothesis:h09`), (b) the high-depth arm of joint indel+SBS decomposition
(`hypothesis:h11`), and (c) genome-wide topography analysis
(`topic:signature-topography-genomic-features`). Access is controlled (ICGC DACO for protected
tiers); treat protected-tier files with the same data-sensitivity posture as GENIE.

## Access and Scope

- Accessions: ICGC/TCGA PCAWG (https://dcc.icgc.org/pcawg)
- Source URL: https://dcc.icgc.org/pcawg
- Organism/population: Homo sapiens
- Modality: whole-genome sequencing (consensus calls)
- Sample size: ~2,800 tumors, 38 cancer types

## Connections to Project

- Referenced by: `paper:PCAWG2020`, `paper:Yaacov2023`
- Role: external dataset cited in the project literature; see referencing papers for usage.
