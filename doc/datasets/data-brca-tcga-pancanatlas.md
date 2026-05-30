---
id: dataset:brca-tcga-pancanatlas
overlay_of: dataset:brca-tcga-pancanatlas
pin_version: "1.0.0"
source_refs:
- cite:Koboldt2012
- cite:Liu2018TCGACDR
related: []
source: results/brca-cmag/studies/brca_tcga_pan_can_atlas_2018/expression/datapackage.json
---
# TCGA-BRCA (PanCancer Atlas) — mRNA expression + clinical

## Summary

The cBioPortal study `brca_tcga_pan_can_atlas_2018`: TCGA breast invasive carcinoma,
PanCancer Atlas freeze. This entity covers the **mRNA expression + clinical** modality
surfaced by the `export_study_expression` rule (the mutation modality is covered by the
generic pipeline). Tidy products: **20,511 genes × 1,082 samples** (RNA-seq RSEM,
`data_mrna_seq_v2_rsem.txt`; 0 missing cells) and a merged sample-level clinical table
(1,084 rows, 57 fields incl. `OS_MONTHS`/`OS_STATUS`, `DSS_*`, `AGE`,
`AJCC_PATHOLOGIC_TUMOR_STAGE`, PAM50 `SUBTYPE`). PAM50 luminal A n = 499. The paired
`datapackage.json` records both parquet resources with byte sizes, SHA-256 hashes, and
shapes.

## Access verification log

- 2026-05-30 (claude, t046): exported from the cached cBioPortal tarball already staged
  under `/data/raw/cbioportal/brca_tcga_pan_can_atlas_2018`; products + datapackage
  written by `all_expression`. `verified: true` — files materialized and hashed.

## Granularity at this access level

mRNA expression matrix (genes × samples) + merged sample-level clinical/survival. TCGA
open-access tier (de-identified). Survival fields follow the Liu 2018 TCGA-CDR curation.

## Connections to Project

- Questions/hypotheses it can inform: the health-cycles tumor-CMag prognostic validation
  (`task:t046`, `question:77-tumor-cmag-prognostic-validation-breast-cancer`).
- Variables likely available: mRNA RSEM expression; OS/DSS survival; age; AJCC stage;
  PAM50 subtype.
- Planned usage: luminal-A reproduction cohort — CYCLOPS ordering → CMag → 5-yr-death
  logistic model.

## Related

- Source: `cite:Koboldt2012` (TCGA-BRCA), `cite:Liu2018TCGACDR` (survival curation).
