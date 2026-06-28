---
type: interpretation
title: "t173 GENIE dNdScv influence attribution \u2014 GENIE LOSO effect traces to\
  \ broad sample-mix shifts across shared hg19 labels"
status: active
created: '2026-04-30'
updated: '2026-06-28'
id: interpretation:0021-t173-genie-dndscv-influence
source_refs:
- task:t173
date: '2026-04-30'
related:
- task:t173
- hypothesis:0002-cross-study-ranking-divergence-is-structured
- question:0013-cross-study-replication-rate
---
# t173 GENIE dNdScv influence attribution

Project links: this interpretation is part of `task:t173`, testing
`hypothesis:0002-cross-study-ranking-divergence-is-structured` through
`question:0013-cross-study-replication-rate`.

Date: 2026-04-30

## Question

Which GENIE cancer/build groups and per-cancer dNdScv signals explain the `exclude_genie`
top-100 rank reshuffling seen in t173?

## Analysis

The attribution script used the completed full-cohort, `exclude_genie`,
`exclude_msk_met_2021`, and `exclude_pog570_bcgsc_2020` dNdScv outputs. It preserved the
published t173 ranking order from `analyze_dndscv_loso.py`: `min_qglobal` ascending, then
`n_cancers_significant_q05` descending, with stable input order for remaining ties.

Command:

```bash
uv run --frozen python code/scripts/analyze_genie_dndscv_influence.py \
  --base-root /data/packages/cbioportal/pan-cancer \
  --loo-root /data/packages/cbioportal/pan-cancer-dndscv-loso \
  --holdout exclude_genie \
  --negative-control exclude_msk_met_2021 \
  --negative-control exclude_pog570_bcgsc_2020 \
  --out-dir /data/packages/cbioportal/pan-cancer/summary/dndscv_loso/genie_influence \
  --top-k 100 \
  --diagnostic-top-n 200 \
  --q-floor 1e-300 \
  --q-shift-threshold 2.0 \
  --q-floor-sensitivity 1e-100 \
  --q-shift-threshold-sensitivity 1.0 \
  --q-shift-threshold-sensitivity 3.0
```

Outputs:

- `/data/packages/cbioportal/pan-cancer/summary/dndscv_loso/genie_influence/genie_gene_rank_delta.feather`
- `/data/packages/cbioportal/pan-cancer/summary/dndscv_loso/genie_influence/genie_gene_cancer_evidence.feather`
- `/data/packages/cbioportal/pan-cancer/summary/dndscv_loso/genie_influence/genie_cancer_build_influence.feather`
- `/data/packages/cbioportal/pan-cancer/summary/dndscv_loso/genie_influence/negative_control_cancer_build_influence_exclude_msk_met_2021.feather`
- `/data/packages/cbioportal/pan-cancer/summary/dndscv_loso/genie_influence/negative_control_cancer_build_influence_exclude_pog570_bcgsc_2020.feather`
- `/data/packages/cbioportal/pan-cancer/summary/dndscv_loso/genie_influence/genie_influence_summary.json`

The primary tables have these shapes:

| table | shape |
|---|---:|
| `genie_gene_rank_delta.feather` | 254 x 15 |
| `genie_gene_cancer_evidence.feather` | 17,272 x 26 |
| `genie_cancer_build_influence.feather` | 68 x 16 |

## Gene-Level Result

The `exclude_genie` contrast has the same top-100 instability reported in the LOSO note:

| contrast | lost top-100 | gained top-100 | stable top-100 |
|---|---:|---:|---:|
| `exclude_genie` | 40 | 40 | 60 |
| `exclude_msk_met_2021` | 8 | 8 | 92 |
| `exclude_pog570_bcgsc_2020` | 4 | 4 | 96 |

The largest lost-gene rank drops include `OBSCN` (+1035), `TTN` (+414), `SUZ12` (+226),
`MUTYH` (+222), `TCF3` (+206), `PARK2` (+178), `PPM1D` (+171), and `ETV6` (+164). The largest
gained-gene promotions include `PTPRS` (-264), `RPS6KA4` (-250), `PTPRT` (-234), `LATS1`
(-209), `GNAS` (-192), `TGFBR2` (-188), `HGF` (-179), and `NOTCH4` (-175).

## Cancer/Build Attribution

All top influence rows are `hg19`; this analysis did not identify a GRCh38-specific driver of
the rank reshuffling.

By summed supported rank delta, the largest groups are broad, high-sample cancer labels:

| cancer/build | mechanism | supported genes | lost support | gained support | sample delta | variant delta |
|---|---|---:|---:|---:|---:|---:|
| Bladder Cancer / hg19 | shared label shift | 254 | 40 | 40 | 5,967 | 88,533 |
| Colorectal Cancer / hg19 | shared label shift | 254 | 40 | 40 | 19,877 | 242,644 |
| Endometrial Cancer / hg19 | shared label shift | 254 | 40 | 40 | 7,171 | 171,402 |
| Non-Small Cell Lung Cancer / hg19 | shared label shift | 254 | 40 | 40 | 30,137 | 290,078 |
| Breast Cancer / hg19 | shared label shift | 253 | 40 | 40 | 17,470 | 114,655 |
| Pancreatic Cancer / hg19 | shared label shift | 252 | 40 | 39 | 9,302 | 60,332 |
| Head and Neck Cancer / hg19 | shared label shift | 252 | 40 | 35 | 2,428 | 24,686 |

By lost top-100 significance specifically, the leading labels are more informative about where
GENIE removal weakens base top-100 genes:

| cancer/build | lost-significance genes |
|---|---:|
| Soft Tissue Sarcoma / hg19 | 37 |
| Glioma / hg19 | 37 |
| Renal Cell Carcinoma / hg19 | 37 |
| Mesothelioma / hg19 | 36 |
| Esophagogastric Cancer / hg19 | 34 |
| Anal Cancer / hg19 | 34 |
| Hepatobiliary Cancer / hg19 | 31 |
| Mature B-Cell Neoplasms / hg19 | 31 |
| Small Bowel Cancer / hg19 | 29 |
| Appendiceal Cancer / hg19 | 24 |

Mechanism labels across the 68 cancer/build groups:

| mechanism | groups |
|---|---:|
| `shared_label_shift` | 35 |
| `genie_only_label` | 30 |
| `weak_or_unclear` | 3 |

Threshold/missingness is still substantial: 21 groups transition from tested to below-threshold
after excluding GENIE, and 9 groups are missing in the holdout. These are not the only mechanism,
but they explain many `genie_only_label` calls. Examples among high ranked rows include Cancer
of Unknown Primary, UNKNOWN, Mature T and NK Neoplasms, and several lower-count tumor labels.

## Negative Controls

The broad non-GENIE controls share some top high-sample labels with the GENIE attribution, but
their rank impact is much smaller:

| contrast | Jaccard@100 | lost/gained top-100 | top-GENIE-label overlap | max supported rank delta | median supported rank delta |
|---|---:|---:|---:|---:|---:|
| `exclude_genie` | 0.429 | 40 / 40 | reference | 27,531 | not used |
| `exclude_msk_met_2021` | 0.852 | 8 / 8 | 8 of top 10 | 2,684 | 683 |
| `exclude_pog570_bcgsc_2020` | 0.923 | 4 / 4 | 7 of top 10 | 1,951 | 506 |

This means the broad labels themselves are not GENIE-exclusive. The GENIE-specific part is the
magnitude of the perturbation: removing GENIE changes many more top-100 genes, and the same
broad labels carry much larger rank movement.

## Interpretation

The dominant mechanism is not a single narrow GENIE cancer/build group. It is a broad
sample-mix and evidence-strength shift across high-sample shared labels, with an additional
tail of labels that become below-threshold or missing when GENIE is removed.

The strongest reading is:

- GENIE is uniquely disruptive relative to the two broad controls.
- The disruption is structured, not random loss of driver signal.
- Most of the top supported rank movement occurs in shared `hg19` cancer labels, especially
  bladder, colorectal, endometrial, non-small cell lung, breast, pancreatic, and head/neck.
- The most gene-loss-specific labels include soft tissue sarcoma, glioma, renal cell carcinoma,
  mesothelioma, esophagogastric, anal, hepatobiliary, mature B-cell neoplasms, small bowel, and
  appendiceal cancer.
- Threshold/missingness explains a substantial minority of groups but is not the whole story.

The next best follow-up is not another broad holdout. It is a targeted audit of the high-impact
GENIE-supported labels above, especially where large sample deltas coincide with lost
significance. A useful next split would separate shared-label quantitative shifts from
tested-to-below-threshold label loss, then inspect whether the leading labels reflect GENIE label
granularity, assay/callability, or true sample-count dominance.

## Caveats

The influence score is descriptive, not causal. Broad labels that support nearly all diagnostic
genes can rank highly by total rank delta because they carry signal for many genes. The
lost-significance table is therefore the better lens for "which labels weaken base top-100
genes," while the summed-rank table is the better lens for "where the global rank movement is
concentrated."

t174 has now resolved the CDKN2A isoform-symbol caveat for external driver overlays. This
analysis uses dNdScv ranks and per-cancer dNdScv evidence directly, so the main attribution did
not depend on Bailey/CGC matching.
