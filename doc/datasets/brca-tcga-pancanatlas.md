---
id: "dataset:brca-tcga-pancanatlas"
type: "dataset"
title: "TCGA-BRCA (PanCancer Atlas) — expression + clinical"
status: "active"
source_class: "observational"
source_refs: []
related: []
created: "2026-05-30"
updated: "2026-05-30"
---

# TCGA-BRCA (PanCancer Atlas) — expression + clinical

## Summary

The cBioPortal study `brca_tcga_pan_can_atlas_2018`: TCGA breast invasive carcinoma,
PanCancer Atlas freeze. This entity covers the **mRNA expression + clinical** modality
surfaced by the `export_study_expression` rule (the mutation modality is covered by the
generic pipeline). Tidy products: **20,511 genes × 1,082 samples** (RNA-seq RSEM,
`data_mrna_seq_v2_rsem.txt`) and a merged sample-level clinical table (1,084 rows, 57
fields incl. `OS_MONTHS`/`OS_STATUS`, `DSS_*`, `AGE`, `AJCC_PATHOLOGIC_TUMOR_STAGE`,
PAM50 `SUBTYPE`). PAM50 luminal A n = 499.

## Access and Scope

- Accession: cBioPortal `brca_tcga_pan_can_atlas_2018` (datahub tarball)
- Source URL: https://www.cbioportal.org/study/summary?id=brca_tcga_pan_can_atlas_2018
- Underlying: TCGA BRCA (Koboldt 2012 Nature; survival fields per Liu 2018 TCGA-CDR)
- Organism/population: Homo sapiens
- Modality (this entity): mRNA expression (RSEM) + clinical/survival
- License: TCGA open-access tier (de-identified, no restrictions on the open data)

## Products

- `results/brca-cmag/studies/brca_tcga_pan_can_atlas_2018/expression/expression.parquet`
- `results/brca-cmag/studies/brca_tcga_pan_can_atlas_2018/expression/clinical.parquet`
  (regenerable via `all_expression` + `config-brca-cmag.yml`; `results/` is gitignored)

## Connections to Project

- Surfaced for the health-cycles tumor-CMag prognostic validation (`task:t046`,
  `dataset:tcga-brca-pancanatlas` consumer). Luminal-A reproduction cohort.
