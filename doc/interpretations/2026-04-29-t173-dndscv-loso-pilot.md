---
id: "interpretation:2026-04-29-t173-dndscv-loso-pilot"
type: "interpretation"
status: "active"
source_refs:
  - "task:t173"
title: "t173 dNdScv LOSO pilot — first leave-one-study-out holdout result on the dNdScv ranking"
date: "2026-04-29"
related:
  - "task:t173"
  - "hypothesis:h02-cross-study-ranking-divergence-is-structured"
  - "question:q013-cross-study-replication-rate"
---
# t173 dNdScv LOSO pilot result

Date: 2026-04-29

## Question

Does the first leave-one-study-out dNdScv rerun preserve the pan-cancer driver ranking strongly
enough to justify launching the full holdout fan-out?

## Pilot run

The pilot excluded `genie`, the study that was most disruptive in the t149 pooled-rate LOSO
analysis. The rerun used the direct pooled dNdScv target rather than the broader
`all_with_dndscv` target:

```bash
uv run --frozen snakemake \
  -s code/workflows/Snakefile \
  --configfile code/config/config-pan-cancer-dndscv.yml \
  --use-conda \
  -j 4 \
  aggregate_dndscv_per_gene \
  --config out_dir=/data/packages/cbioportal/pan-cancer-dndscv-loso/exclude_genie \
  studies='["acc_2019","aml_ohsu_2018","aml_ohsu_2022","brain_cptac_2020","msk_met_2021","metastatic_solid_tumors_mich_2017","mixed_allen_2018","mixed_pipseq_2017","pancan_pcawg_2020","pediatric_dkfz_2017","pog570_bcgsc_2020","pptc_2019"]'
```

Snakemake completed successfully. The run combined 8,157,844 mutation rows from 12 non-empty
studies, wrote 98 cancer/build groups, aggregated 96 per-cancer dNdScv outputs, and produced:

`/data/packages/cbioportal/pan-cancer-dndscv-loso/exclude_genie/summary/mut/table/dndscv_pooled.feather`

The pooled holdout table contains 20,091 genes with non-null `min_qglobal`.

## Stability result

The comparison script wrote real, non-placeholder outputs:

- `/data/packages/cbioportal/pan-cancer/summary/dndscv_loso/dndscv_loso_topk_overlap.feather`
- `/data/packages/cbioportal/pan-cancer/summary/dndscv_loso/dndscv_loso_summary.feather`

These are one-iteration pilot outputs. They do not estimate a LOSO distribution; the median and
minimum in `dndscv_loso_summary.feather` are identical by construction because only `genie` has
completed. The table below should therefore be read as the behavior of the `genie` holdout, not
as the overall behavior of dNdScv LOSO.

Top-K overlap for the `genie` holdout:

| K | intersection | Jaccard | base recovery | holdout recovery |
|---:|---:|---:|---:|---:|
| 10 | 6 | 0.429 | 0.60 | 0.60 |
| 25 | 16 | 0.471 | 0.64 | 0.64 |
| 50 | 31 | 0.449 | 0.62 | 0.62 |
| 100 | 60 | 0.429 | 0.60 | 0.60 |

The planned P1 fan-out gate was Jaccard@100 >= 0.5. The `exclude_genie` pilot produced
Jaccard@100 = 0.429, so the gate is not met.

This is not simply a loss of recognizable driver signal. Bailey recovery at K=100 increased in
the holdout top 100 (0.68) relative to the base top 100 (0.61), while CGC tier-1-or-2 recovery
decreased modestly from 0.90 to 0.86. GENIE removal therefore appears to change which
driver-supported genes rank highly, rather than just replacing drivers with non-drivers.

Postscript: t174 has now resolved the CDKN2A isoform-symbol overlay issue. This historical pilot
note keeps the original pilot table for traceability; use
`doc/interpretations/2026-04-30-t173-dndscv-loso-synthesis.md` for the final post-t174
Bailey/CGC recovery values. The rank-overlap/Jaccard gate and the relative conclusion from this
pilot did not depend on the reference overlays.

## Rank changes

Base top 20:

`TP53, KRAS, NRAS, PIK3CA, TTN, CDKN2A.p16INK4a, FBXW7, KMT2D, PTEN, RB1, TET2, ARID1A, ARID2, DNMT3A, BRAF, SETD2, NF1, KDM6A, EP300, FAT1`

Exclude-GENIE top 20:

`TP53, PIK3CA, KRAS, PTEN, ARID1A, ATM, CREBBP, KMT2D, RB1, ARID2, NRAS, FBXW7, BRAF, CDKN2A.p16INK4a, EP300, MGA, NOTCH1, SETD2, APC, ASXL1`

Genes lost from the base top 100 after excluding GENIE:

`AXL, B2M, BLM, BRCA2, CBL, CHEK2, CIC, CSF3R, ESR1, ETV6, EZH2, FANCA, FGFR4, FLT3, HRAS, IL7R, JAK2, MLH1, MPL, MSH2, MSH6, MUTYH, NOTCH2, NTRK1, OBSCN, PARK2, PDGFRB, PPM1D, PRDM1, PTCH1, RECQL4, RUNX1, SH2B3, SLX4, SMARCB1, SUZ12, TCF3, TTN, U2AF1, WT1`

Genes gained in the exclude-GENIE top 100:

`ARID1B, ASXL2, ATR, AXIN1, AXIN2, BAP1, CDK12, CDKN2A.p14arf, DOT1L, EGFR, GLI1, GNAS, HGF, IKZF1, JAK1, KDM5C, KDR, KMT2A, KMT2B, LATS1, MDC1, MTOR, NFE2L2, NOTCH4, PIK3CG, POLE, PREX2, PTPRD, PTPRS, PTPRT, RAD50, RASA1, RET, RNF43, RPS6KA4, SMAD4, SMARCA4, STK11, TET1, TGFBR2`

## Interpretation

The pilot fails the pre-specified fan-out gate. Do not launch the remaining multi-hour dNdScv
holdouts as a blind fan-out from this state.

The result supports the directional claim that GENIE is strongly rank-shaping even under dNdScv,
not only under pooled-rate ranking. It does not yet distinguish a GENIE-specific effect from
generic single-study sensitivity, because `n_iterations = 1`.

Before any second holdout run, pre-register the next contrast as `msk_met_2021`, a broad
non-GENIE cohort. Interpret its Jaccard@100 as follows:

- `>= 0.60`: supports a GENIE-specific disruption reading.
- `0.50` to `< 0.60`: ambiguous; continue with at least one additional contrastive holdout.
- `0.40` to `< 0.50`: supports generic single-study sensitivity rather than a GENIE-specific
  effect.
- `< 0.40`: supports generic sensitivity at least as severe as the GENIE pilot.

The contrast has now been run; see
`doc/interpretations/2026-04-29-t173-dndscv-loso-contrast.md`. Full P2 adjudication remains open,
but the `msk_met_2021` result supports the GENIE-specific disruption reading over generic
single-study sensitivity.
