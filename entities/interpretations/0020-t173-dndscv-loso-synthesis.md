---
type: interpretation
title: "t173 dNdScv LOSO synthesis \u2014 dNdScv ranking is LOSO-stable; GENIE removal\
  \ is a structured, not generic, perturbation"
status: active
created: '2026-04-30'
updated: '2026-06-28'
id: interpretation:0020-t173-dndscv-loso-synthesis
source_refs:
- task:t173
date: '2026-04-30'
related:
- task:t173
- hypothesis:0002-cross-study-ranking-divergence-is-structured
- question:0013-cross-study-replication-rate
- question:0015-pan-cancer-aggregator-choice
---
# t173 dNdScv LOSO synthesis

Project links: this synthesis interpretation is part of `task:t173` and connects
`question:0013-cross-study-replication-rate` to `question:0015-pan-cancer-aggregator-choice`.

Date: 2026-04-30

## Question

Does the pan-cancer dNdScv top-gene ranking show generic single-study instability, or is the
observed instability specifically driven by GENIE?

## Inputs

This synthesis closes the t173 sequence using three completed dNdScv holdouts and the GENIE
influence attribution analysis:

- `exclude_genie`: `/data/packages/cbioportal/pan-cancer-dndscv-loso/exclude_genie/summary/mut/table/dndscv_pooled.feather`
- `exclude_msk_met_2021`: `/data/packages/cbioportal/pan-cancer-dndscv-loso/exclude_msk_met_2021/summary/mut/table/dndscv_pooled.feather`
- `exclude_pog570_bcgsc_2020`: `/data/packages/cbioportal/pan-cancer-dndscv-loso/exclude_pog570_bcgsc_2020/summary/mut/table/dndscv_pooled.feather`
- comparison outputs: `/data/packages/cbioportal/pan-cancer/summary/dndscv_loso/`
- GENIE attribution outputs: `/data/packages/cbioportal/pan-cancer/summary/dndscv_loso/genie_influence/`

The LOSO comparison outputs were refreshed after t174, so Bailey/CGC recovery values now expand
bare driver symbols to dNdScv isoform symbols such as `CDKN2A.p16INK4a` and `CDKN2A.p14arf`.
Raw dNdScv symbols are still preserved in the ranked tables.

## Final Result

Top-K overlap between the full pan-cancer dNdScv ranking and each completed holdout:

| excluded study | K=10 Jaccard | K=25 Jaccard | K=50 Jaccard | K=100 Jaccard | top-100 lost/gained |
|---|---:|---:|---:|---:|---:|
| `genie` | 0.429 | 0.471 | 0.449 | 0.429 | 40 / 40 |
| `msk_met_2021` | 1.000 | 0.923 | 0.786 | 0.852 | 8 / 8 |
| `pog570_bcgsc_2020` | 0.818 | 1.000 | 0.852 | 0.923 | 4 / 4 |

The `pog570_bcgsc_2020` K=50 value is lower than its K=25 and K=100 values because each K is a
separate prefix comparison. Adding ranks 26-50 can introduce transient disagreements before
ranks 51-100 restore more overlap; the K=50 value is still well above the contrast threshold.

Reference recovery after the t174 overlay fix:

| excluded study | base Bailey@100 | holdout Bailey@100 | base CGC tier 1/2 @100 | holdout CGC tier 1/2 @100 |
|---|---:|---:|---:|---:|
| `genie` | 0.62 | 0.70 | 0.91 | 0.88 |
| `msk_met_2021` | 0.62 | 0.62 | 0.91 | 0.91 |
| `pog570_bcgsc_2020` | 0.62 | 0.61 | 0.91 | 0.90 |

The original pilot fan-out gate was Jaccard@100 >= 0.5, recorded in
`doc/interpretations/2026-04-29-t173-dndscv-loso-protocol.md`. The GENIE holdout failed that
gate with Jaccard@100 = 0.429. The `>= 0.60` contrast threshold for a GENIE-specific disruption
reading was recorded in `doc/interpretations/2026-04-29-t173-dndscv-loso-pilot.md` before the
second holdout was run. Both broad non-GENIE controls were above that threshold.

## Interpretation

t173 supports a GENIE-specific rank-shaping effect, not generic single-study sensitivity.

Removing GENIE changes 40 of the full-cohort top-100 genes. Removing two broad non-GENIE cohorts
while retaining GENIE changes only 8 and 4 top-100 genes. The contrast is large enough that the
simplest "any large study removal causes the same instability" explanation is no longer
credible for the current dNdScv ranking.

The GENIE effect is not a collapse of driver signal. In the GENIE holdout, Bailey recovery at
K=100 increases from 0.62 to 0.70, the opposite direction from a degraded-driver explanation,
while CGC tier-1-or-2 recovery only decreases from 0.91 to 0.88. The result is a reshuffling
among driver-supported genes and candidate driver-like genes, not replacement of drivers by
obvious passenger noise.

## Mechanism

The follow-up attribution analysis did not identify a single narrow GENIE-only cancer/build group
as the dominant cause. The stronger mechanism is a broad evidence-strength and sample-mix shift
across high-sample shared `hg19` labels, with an additional tail of labels that become
below-threshold or missing after GENIE removal.

The largest summed-rank attribution labels were broad shared labels: bladder, colorectal,
endometrial, non-small cell lung, breast, pancreatic, and head/neck cancers. This summed-rank
view reflects where sample-weighted rank movement is concentrated. Lost-significance counts
instead reflect where base-cohort signals disappear or weaken below the q-evidence threshold;
that view points more specifically to soft tissue sarcoma, glioma, renal cell carcinoma,
mesothelioma, esophagogastric cancer, anal cancer, hepatobiliary cancer, mature B-cell
neoplasms, small bowel cancer, and appendiceal cancer.

The negative controls share some of these broad labels, but their perturbation magnitude is much
smaller: max supported rank delta was 27,531 for `exclude_genie`, versus 2,684 for
`exclude_msk_met_2021` and 1,951 for `exclude_pog570_bcgsc_2020`. Here max supported rank delta
is the largest cancer/build value of `sum_abs_rank_delta_supported`: the sum, over affected
diagnostic genes supported in that label, of absolute full-vs-holdout pan-cancer rank changes.
The attribution schema is specified in
`doc/plans/2026-04-30-t173-genie-dndscv-influence-plan.md`.

## Decision

Stop the blind broad-holdout fan-out. The expensive full LOSO distribution is no longer the
highest-value next step for `hypothesis:0002-cross-study-ranking-divergence-is-structured`. Three real reruns are enough to establish the directional
contrast that matters for the current decision: GENIE is the unusual perturbation, and the
mechanism is structured.

Close t173 as resolved for the dNdScv LOSO decision. Future work should not spend compute on
more broad holdouts unless a reviewer specifically requires a complete LOSO distribution.

## Limitations

This is not a full LOSO distribution. It is a targeted pilot plus two broad negative controls.
The conclusion is therefore about the current decision point, not about the complete empirical
distribution of all possible study holdouts.

The influence score is descriptive. It identifies where rank movement is concentrated, but it
does not by itself distinguish label granularity, assay/callability, sample-count dominance, and
true cohort biology. A focused audit of the highest-impact GENIE-supported labels is the right
mechanistic follow-up if that level of detail becomes necessary.

## Follow-Up

The next project step should move out of the t173 holdout loop. The strongest candidates are:

- t171: integrate independent IntOGen and DepMap validation for the dNdScv ranking.
- t155/t165: compare alternative aggregators for the q=0 dNdScv floor regime.
- a narrow GENIE-label audit only if the synthesis needs a deeper mechanism appendix.
