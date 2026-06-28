---
type: interpretation
title: "t173 dNdScv LOSO contrastive holdout \u2014 broad single-study removal contrast\
  \ for top-N replication"
status: active
created: '2026-04-29'
updated: '2026-06-28'
id: interpretation:0016-t173-dndscv-loso-contrast
source_refs:
- task:t173
- /data/packages/cbioportal/pan-cancer-dndscv-loso/exclude_msk_met_2021/summary/mut/table/dndscv_pooled.feather
- /data/packages/cbioportal/pan-cancer/summary/dndscv_loso/dndscv_loso_summary.feather
- /data/packages/cbioportal/pan-cancer/summary/dndscv_loso/dndscv_loso_topk_overlap.feather
date: '2026-04-29'
related:
- task:t173
- hypothesis:0002-cross-study-ranking-divergence-is-structured
- question:0013-cross-study-replication-rate
---
# t173 dNdScv LOSO contrastive holdout

Project links: this interpretation is part of `task:t173`, testing
`hypothesis:0002-cross-study-ranking-divergence-is-structured` through
`question:0013-cross-study-replication-rate`.

Date: 2026-04-29

## Question

Was the failed `exclude_genie` dNdScv LOSO pilot a sign of generic single-study sensitivity, or
was GENIE unusually rank-shaping?

## Pre-registered contrast

After the `exclude_genie` pilot produced Jaccard@100 = 0.429, the next contrast was
pre-registered as `msk_met_2021`, a broad non-GENIE cohort. The decision bands were set in
`task:t173`:

- Jaccard@100 `>= 0.60`: supports a GENIE-specific disruption reading.
- Jaccard@100 `0.50` to `< 0.60`: ambiguous; continue with at least one additional contrastive
  holdout.
- Jaccard@100 `0.40` to `< 0.50`: supports generic single-study sensitivity rather than a
  GENIE-specific effect.
- Jaccard@100 `< 0.40`: supports generic sensitivity at least as severe as the GENIE pilot.

## Run

The contrast excluded `msk_met_2021` and retained GENIE:

```bash
uv run --frozen snakemake \
  -s code/workflows/Snakefile \
  --configfile code/config/config-pan-cancer-dndscv.yml \
  --use-conda \
  -j 4 \
  aggregate_dndscv_per_gene \
  --config out_dir=/data/packages/cbioportal/pan-cancer-dndscv-loso/exclude_msk_met_2021 \
  studies='["acc_2019","aml_ohsu_2018","aml_ohsu_2022","brain_cptac_2020","genie","metastatic_solid_tumors_mich_2017","mixed_allen_2018","mixed_pipseq_2017","pancan_pcawg_2020","pediatric_dkfz_2017","pog570_bcgsc_2020","pptc_2019"]'
```

The Snakemake dry-run resolved the isolated DAG. The real run completed all 330 dynamic steps,
combined 9,916,430 mutation rows from 12 non-empty studies, wrote 148 cancer/build groups
(78 below threshold), aggregated 146 per-cancer outputs, and produced the pooled table at
`/data/packages/cbioportal/pan-cancer-dndscv-loso/exclude_msk_met_2021/summary/mut/table/dndscv_pooled.feather`.

The pooled holdout table contains 20,091 genes with non-null `min_qglobal`
(`/data/packages/cbioportal/pan-cancer-dndscv-loso/exclude_msk_met_2021/summary/mut/table/dndscv_pooled.feather`).

## Result

The comparison script now includes two completed holdouts: `genie` and `msk_met_2021`.

| excluded study | K | intersection | Jaccard | base recovery | holdout recovery |
|---|---:|---:|---:|---:|---:|
| genie | 10 | 6 | 0.429 | 0.60 | 0.60 |
| genie | 25 | 16 | 0.471 | 0.64 | 0.64 |
| genie | 50 | 31 | 0.449 | 0.62 | 0.62 |
| genie | 100 | 60 | 0.429 | 0.60 | 0.60 |
| msk_met_2021 | 10 | 10 | 1.000 | 1.00 | 1.00 |
| msk_met_2021 | 25 | 24 | 0.923 | 0.96 | 0.96 |
| msk_met_2021 | 50 | 44 | 0.786 | 0.88 | 0.88 |
| msk_met_2021 | 100 | 92 | 0.852 | 0.92 | 0.92 |

The pre-registered contrast result is decisive in direction: `msk_met_2021` Jaccard@100 was
0.852, which is above the `>= 0.60` threshold for a GENIE-specific disruption reading
(`/data/packages/cbioportal/pan-cancer/summary/dndscv_loso/dndscv_loso_topk_overlap.feather`).

The two-holdout summary is still not a full LOSO distribution. Its median values are useful as a
status check, but with `n_iterations = 2`, the scientific interpretation should focus on the
pre-registered contrast rather than over-reading distribution summaries.

## Rank changes for `msk_met_2021`

Base top 20:

`TP53, KRAS, NRAS, PIK3CA, TTN, CDKN2A.p16INK4a, FBXW7, KMT2D, PTEN, RB1, TET2, ARID1A, ARID2, DNMT3A, BRAF, SETD2, NF1, KDM6A, EP300, FAT1`

Exclude-MSK top 20:

`TP53, KRAS, NRAS, TTN, PIK3CA, CDKN2A.p16INK4a, FBXW7, KMT2D, PTEN, RB1, TET2, ARID1A, ARID2, DNMT3A, BRAF, SETD2, NF1, KIT, EP300, FAT1`

Genes lost from the base top 100 after excluding `msk_met_2021`
(`/data/packages/cbioportal/pan-cancer/summary/dndscv_loso/dndscv_loso_topk_overlap.feather`):

`ESR1, NTRK1, PTPN11, RECQL4, SUZ12, TCF3, U2AF1, WT1`

Genes gained in the exclude-MSK top 100
(`/data/packages/cbioportal/pan-cancer/summary/dndscv_loso/dndscv_loso_topk_overlap.feather`):

`ABL1, BCL6, BCORL1, EGFR, HLA-A, HNF1A, IKZF1, KMT2A`

## Interpretation

The contrast supports the GENIE-specific reading of the original pilot failure. Removing
`msk_met_2021`, while retaining GENIE, preserves the canonical dNdScv top-100 ranking much more
strongly than removing GENIE: Jaccard@100 is 0.852 for `msk_met_2021` versus 0.429 for GENIE
(`/data/packages/cbioportal/pan-cancer/summary/dndscv_loso/dndscv_loso_topk_overlap.feather`).

This does not close full P2, because it compares only one broad non-GENIE contrast against one
GENIE holdout. It is enough to reject the simplest "any single study removal causes the same
instability" explanation. The next useful step is either:

- run one additional non-GENIE broad holdout, such as `pog570_bcgsc_2020`, to check whether the
  high-overlap contrast generalizes; or
- stop the expensive fan-out and investigate which GENIE cancer/build groups drive the
  re-ranking.

Postscript: t174 has now resolved the CDKN2A isoform-symbol overlay issue. Use
`doc/interpretations/2026-04-30-t173-dndscv-loso-synthesis.md` for the final post-t174
Bailey/CGC recovery values. The Jaccard gate and contrastive conclusion did not depend on those
reference overlays.

Follow-up: the second broad non-GENIE contrast, `pog570_bcgsc_2020`, has now been run and also
supports the GENIE-specific disruption reading; see
`doc/interpretations/2026-04-30-t173-dndscv-loso-second-broad-contrast.md`.
