---
id: "dataset:brca-metabric"
type: "dataset"
title: "METABRIC — expression + clinical"
status: "active"
source_class: "observational"
source_refs: []
related: []
created: "2026-05-30"
updated: "2026-05-30"
---

# METABRIC — expression + clinical

## Summary

The cBioPortal study `brca_metabric`: Molecular Taxonomy of Breast Cancer International
Consortium. This entity covers the **mRNA expression + clinical** modality surfaced by
the `export_study_expression` rule. Tidy products: **20,385 genes × 1,980 samples**
(Illumina microarray, `data_mrna_illumina_microarray.txt`) and a merged sample-level
clinical table (2,509 rows — 1,980 with matched expression, 529 clinical-only — 37
fields incl. `OS_MONTHS`/`OS_STATUS`, `RFS_*`, `AGE_AT_DIAGNOSIS`, `CLAUDIN_SUBTYPE`,
`ER_STATUS`). PAM50/claudin luminal A n = 700; long follow-up supports independent
survival validation.

## Access and Scope

- Accession: cBioPortal `brca_metabric` (datahub tarball)
- Source URL: https://www.cbioportal.org/study/summary?id=brca_metabric
- Underlying: Curtis 2012 Nature (10.1038/nature10983); Pereira 2016 Nat Commun
  (10.1038/ncomms11479)
- Organism/population: Homo sapiens
- Modality (this entity): mRNA expression (Illumina microarray) + clinical/survival
- License: data released for academic research via cBioPortal; primary access EGA-gated

## Products

- `results/brca-cmag/studies/brca_metabric/expression/expression.parquet`
- `results/brca-cmag/studies/brca_metabric/expression/clinical.parquet`
  (regenerable via `all_expression` + `config-brca-cmag.yml`; `results/` is gitignored)

## Connections to Project

- Surfaced for the health-cycles tumor-CMag prognostic validation (`task:t046`).
  Independent (platform-distinct) validation cohort.
