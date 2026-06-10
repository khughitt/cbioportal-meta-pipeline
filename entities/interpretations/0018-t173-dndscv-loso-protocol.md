---
type: interpretation
title: "t173 dNdScv LOSO protocol status \u2014 harness and holdout design for the\
  \ decisive replication test"
status: active
created: '2026-04-29'
updated: '2026-04-29'
id: interpretation:0018-t173-dndscv-loso-protocol
source_refs:
- task:t173
date: '2026-04-29'
related:
- task:t173
- hypothesis:0002-cross-study-ranking-divergence-is-structured
- question:0013-cross-study-replication-rate
---
# t173 dNdScv LOSO protocol status

Date: 2026-04-29

## Question

Does the dNdScv pan-cancer driver ranking remain stable under leave-one-study-out reruns, and do
specialty studies disrupt the ranking more than broad generalist studies?

## Current status

The protocol harness exists, and the first pilot holdout has now produced a real dNdScv pooled
table. The decisive full t173 test still requires fresh dNdScv reruns for each holdout because
the canonical per-cancer dNdScv outputs do not retain enough study identity to subtract one study
analytically.

The protocol and analysis harness now exist:

- Plan: `doc/plans/2026-04-29-t173-dndscv-loso-plan.md`
- Manifest builder: `code/scripts/build_dndscv_loso_manifest.py`
- Comparison script: `code/scripts/analyze_dndscv_loso.py`
- Pilot manifest:
  `/data/packages/cbioportal/pan-cancer/summary/dndscv_loso/dndscv_loso_run_manifest.tsv`
- Pilot result: `doc/interpretations/2026-04-29-t173-dndscv-loso-pilot.md`
- Contrast result: `doc/interpretations/2026-04-29-t173-dndscv-loso-contrast.md`
- Second broad contrast:
  `doc/interpretations/2026-04-30-t173-dndscv-loso-second-broad-contrast.md`

## Pilot holdout

The first pilot holdout is `genie`, because t149 identified GENIE as unexpectedly disruptive in
the pooled-rate LOSO analysis. The generated command writes into an isolated directory:

`/data/packages/cbioportal/pan-cancer-dndscv-loso/exclude_genie`

A Snakemake run of the direct dNdScv pooled target (`aggregate_dndscv_per_gene`) completed
successfully and did not touch the canonical pan-cancer dNdScv output directory. The broader
`all_with_dndscv` target is intentionally not used for LOSO pilots because it also triggers
sample-panel/SELECT outputs that are not needed for t173.

## Interpretation rule once outputs exist

Use `code/scripts/analyze_dndscv_loso.py` after one or more holdout runs complete. The decisive
P1 criterion is whether canonical-driver Jaccard at K=100 is stable across LOSO at >=0.5. P2 is
supported only if specialty-study holdouts disrupt top-K overlap more than generalist-study
holdouts after comparing the same dNdScv ranking metric.

t173 is now closed by `doc/interpretations/2026-04-30-t173-dndscv-loso-synthesis.md`. The
`exclude_genie` pilot plus two broad non-GENIE contrasts (`msk_met_2021`,
`pog570_bcgsc_2020`) are complete. Both broad contrasts support a GENIE-specific disruption
reading, and the follow-up GENIE influence attribution explains the mechanism sufficiently for
the current decision point.
