---
type: interpretation
title: "t173 dNdScv LOSO second broad contrast \u2014 additional broad holdout confirming\
  \ structured perturbation"
status: active
created: '2026-04-30'
updated: '2026-04-30'
id: interpretation:0019-t173-dndscv-loso-second-broad-contrast
source_refs:
- task:t173
date: '2026-04-30'
related:
- task:t173
- hypothesis:0002-cross-study-ranking-divergence-is-structured
- question:0013-cross-study-replication-rate
---
# t173 dNdScv LOSO second broad contrast

Date: 2026-04-30

## Question

Does a second broad non-GENIE holdout reproduce the high top-100 stability seen for
`msk_met_2021`, or was that first contrast unusually stable?

## Run

The third completed holdout excluded `pog570_bcgsc_2020` and retained both GENIE and
`msk_met_2021`:

```bash
uv run --frozen snakemake \
  -s code/workflows/Snakefile \
  --configfile code/config/config-pan-cancer-dndscv.yml \
  --use-conda \
  -j 4 \
  aggregate_dndscv_per_gene \
  --config out_dir=/data/packages/cbioportal/pan-cancer-dndscv-loso/exclude_pog570_bcgsc_2020 \
  studies='["acc_2019","aml_ohsu_2018","aml_ohsu_2022","brain_cptac_2020","genie","msk_met_2021","metastatic_solid_tumors_mich_2017","mixed_allen_2018","mixed_pipseq_2017","pancan_pcawg_2020","pediatric_dkfz_2017","pptc_2019"]'
```

The Snakemake dry-run resolved the isolated DAG. The real run completed all 330 dynamic steps,
combined 2,877,087 mutation rows from 12 non-empty studies, wrote 148 cancer/build groups
(78 below threshold), aggregated 146 per-cancer outputs, and produced:

`/data/packages/cbioportal/pan-cancer-dndscv-loso/exclude_pog570_bcgsc_2020/summary/mut/table/dndscv_pooled.feather`

The pooled holdout table contains 20,091 genes with non-null `min_qglobal`.

## Result

The comparison script now includes three completed holdouts: `genie`, `msk_met_2021`, and
`pog570_bcgsc_2020`.

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
| pog570_bcgsc_2020 | 10 | 9 | 0.818 | 0.90 | 0.90 |
| pog570_bcgsc_2020 | 25 | 25 | 1.000 | 1.00 | 1.00 |
| pog570_bcgsc_2020 | 50 | 46 | 0.852 | 0.92 | 0.92 |
| pog570_bcgsc_2020 | 100 | 96 | 0.923 | 0.96 | 0.96 |

The second broad non-GENIE contrast strengthens the GENIE-specific disruption interpretation.
Both broad non-GENIE holdouts land well above the pre-registered `>= 0.60` support threshold:

- `msk_met_2021`: Jaccard@100 = 0.852.
- `pog570_bcgsc_2020`: Jaccard@100 = 0.923.
- `genie`: Jaccard@100 = 0.429.

The three-holdout summary is still not a full LOSO distribution. Its median Jaccard@100 is
0.852, and the minimum remains 0.429 because GENIE is the only low-overlap holdout.

## Rank changes for `pog570_bcgsc_2020`

Base top 20:

`TP53, KRAS, NRAS, PIK3CA, TTN, CDKN2A.p16INK4a, FBXW7, KMT2D, PTEN, RB1, TET2, ARID1A, ARID2, DNMT3A, BRAF, SETD2, NF1, KDM6A, EP300, FAT1`

Exclude-POG top 20:

`TP53, KRAS, NRAS, PIK3CA, CDKN2A.p16INK4a, FBXW7, KMT2D, PTEN, RB1, TET2, TTN, ARID1A, ARID2, DNMT3A, BRAF, SETD2, NF1, FAT1, JAK2, EP300`

Genes lost from the base top 100 after excluding `pog570_bcgsc_2020`:

`BRCA1, CIC, PTCH1, TCF3`

Genes gained in the exclude-POG top 100:

`ABL1, BCL6, HIST1H1C, MYCN`

## Interpretation

The result now rejects the generic single-study sensitivity explanation more strongly than the
single MSK contrast did. Two broad non-GENIE holdouts preserve the canonical dNdScv top-100
ranking, while GENIE removal substantially reshuffles it.

This still does not close all of P2, because only three holdouts have been run. It is enough to
change the next best use of compute: stop the blind broad-holdout fan-out for now and investigate
the GENIE-specific mechanism. The next analysis should identify which GENIE cancer/build groups
or high-weight cancer labels drive the genes lost and gained in the `exclude_genie` top 100.

Postscript: t174 has now resolved the CDKN2A isoform-symbol overlay issue. Use
`doc/interpretations/2026-04-30-t173-dndscv-loso-synthesis.md` for the final post-t174
Bailey/CGC recovery values. The Jaccard contrast and GENIE-specific conclusion did not depend on
those reference overlays.
