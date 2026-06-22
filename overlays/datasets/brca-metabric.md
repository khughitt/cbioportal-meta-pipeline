---
id: dataset:brca-metabric
overlay_of: dataset:brca-metabric
pin_version: "1.0.0"
source_refs:
- cite:Curtis2012
- cite:Pereira2016
related: []
source: results/brca-cmag/studies/brca_metabric/expression/datapackage.json
---
# METABRIC — mRNA expression + clinical

## Summary

The cBioPortal study `brca_metabric`: Molecular Taxonomy of Breast Cancer International
Consortium. This entity covers the **mRNA expression + clinical** modality surfaced by
the `export_study_expression` rule. Tidy products: **20,385 genes × 1,980 samples**
(Illumina HT-12 v3 microarray, `data_mrna_illumina_microarray.txt`; **16 missing cells
across 11 genes** — genuine source NAs, flagged for WP2 to resolve before Julia) and a
merged sample-level clinical table (2,509 rows — 1,980 with matched expression, 529
clinical-only — 37 fields incl. `OS_MONTHS`/`OS_STATUS`, `RFS_*`, `AGE_AT_DIAGNOSIS`,
`CLAUDIN_SUBTYPE`, `ER_STATUS`). PAM50/claudin luminal A n = 700; long follow-up
supports independent survival validation. The paired `datapackage.json` records both
parquet resources with byte sizes, SHA-256 hashes, shapes, and the missing-cell count.

## Access verification log

- 2026-05-30 (claude, t046): exported from the cached cBioPortal tarball already staged
  under `/data/raw/cbioportal/brca_metabric`; products + datapackage written by
  `all_expression`. `verified: true` — files materialized and hashed. Note the 11 genes
  with ≥1 missing expression value (genuine NAs in the source microarray matrix).

## Granularity at this access level

mRNA expression matrix (genes × samples) + merged sample-level clinical/survival.
Processed study publicly redistributed via cBioPortal; primary METABRIC data is
EGA-controlled.

## Connections to Project

- Questions/hypotheses it can inform: the health-cycles tumor-CMag prognostic validation
  (`task:t046`, `question:77-tumor-cmag-prognostic-validation-breast-cancer`).
- Variables likely available: Illumina microarray expression; OS/RFS survival; age;
  claudin/PAM50 subtype; ER status.
- Planned usage: **independent (platform-distinct) validation cohort** for CMag.

## Related

- Source: `cite:Curtis2012` (METABRIC discovery), `cite:Pereira2016` (expanded landscape).
