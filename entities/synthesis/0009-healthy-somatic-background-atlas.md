---
type: synthesis
title: 'Synthesis: h05-healthy-somatic-background-atlas'
status: active
created: '2026-06-02'
updated: '2026-06-02'
report_kind: hypothesis-synthesis
id: synthesis:0009-healthy-somatic-background-atlas
hypothesis: hypothesis:0005-healthy-somatic-background-atlas
generated_at: 2026-06-02 09:52:22+00:00
source_commit: 037f0ab2d3c84ecc56bebd843e361c1a9dfbfa66
provenance_coverage: thin
---

## State

`hypothesis:0005-healthy-somatic-background-atlas` is in `phase: candidate`, with no
interpretations yet recorded. The core claim rests on three propositions: cross-tissue somatic
mutation rates vary by more than two orders of magnitude (P1); driver-positive clonal expansions
in apparently-healthy tissue exceed per-tissue cancer-discovery rates at age 70+ for at least
three tissues (P2); and substituting a meta-analyzed cross-tissue normal null for the project's
current within-pipeline null produces calibrated, tissue-specific shifts in apparent driver
frequencies in unmatched-normal cBioPortal studies (P3).

The only directly resolved question in the bundle,
`question:0007-cross-tissue-somatic-mutation-rate-variation-as-null-model`, frames the Li 2021
body-map (9 tissues, liver highest, pancreas lowest mutation burden) as the closest existing
empirical anchor for P1. That question notes that the Li 2021 sample size is five donors and
that per-tissue rate estimates require clone-size corrections from VAF distributions — making
them uncertain. The question also flags a simpler dN/dS-based null as methodologically more
mature for near-term pipeline use, and records that no published adaptation of the Li 2021
body-map data as a quantitative null model for cancer-study frequency analysis existed as of
its filing date.

Data harmonization is the principal unresolved obstacle: published normal-tissue cohorts differ
in sequencing depth, variant-calling regime, and age range. For several cBioPortal-relevant
tissues (kidney, thyroid, pancreas), normal-mutation reference data are thin or absent, which
limits how broadly P1's >2-OoM range can be tested.

## Arc

Arc reconstruction is limited because no interpretations with `prior_interpretations` chains
have been filed for this hypothesis.

`hypothesis:0005-healthy-somatic-background-atlas` was registered on 2026-04-28 as a direct
generalization of the within-sample contamination frame in
`hypothesis:0001-non-tumor-signal-contamination`. The initial framing drew on
`question:0007-cross-tissue-somatic-mutation-rate-variation-as-null-model`, which had been
filed ten days earlier (2026-04-18) asking whether Li 2021 body-map rates could serve as a
null model for per-tissue background in the pipeline. That question reached a provisional
answer: the concept is sound but calibration obstacles — small donor count, clone-size
corrections, EGA data-access requirements — make direct pipeline integration a multi-week
project rather than a quick annotation step.

At hypothesis registration, three scoped tasks were issued to gate promotion: `t150`
(feasibility audit of available normal-tissue WGS cohorts), `t151` (single-tissue meta-analysis
pilot, likely esophagus), and `t114` (pre-registration of null-model correction impact before
rolling any correction into the frequency pipeline). Dataset-acquisition tasks `t166`, `t168`,
and `t169` were also filed but immediately blocked — `t169` was explicitly blocked on
2026-05-31 because the GTEx controlled-access somatic call sets require institutional
affiliation not currently available. The hypothesis has not advanced past the candidate framing
stage; no project-internal hypothesis test has been conducted.

## Research fronts

**Open tasks.**

- `t114` (proposed, P2): pre-register expected gene-cancer ranking shifts and a head-to-head
  comparison against a dN/dS-based null before applying any per-tissue SNVs/Mb correction to
  pipeline outputs; deliverable is `doc/meta/pre-registration-q007-null-model-correction.md`.
- `t150` (proposed, P2): feasibility audit — enumerate published normal-tissue WGS cohorts,
  map to cBioPortal cancer types, decide harmonization regime, and produce a promotion
  recommendation for `hypothesis:0005-healthy-somatic-background-atlas`.
- `t151` (proposed, P2, depends on t150): scoped pilot meta-analysis on the most tractable
  tissue (esophagus or colon); test whether the cross-tissue normal null improves
  matched-vs-unmatched correction over the current within-pipeline null; deliverable is a
  tissue-specific interpretation with effect size and scale-up recommendation.
- `t166` (blocked, P3): Hartwig HMF acquisition; ~6,000 matched-normal metastatic WGS samples
  covering ~25 cancer-relevant tissues, which would directly support P1 and P3 and bypass
  the panel-coverage gap that blocked the
  `question:0009-sbs1-lrr-bias-as-normal-contamination-flag` SBS1 LRR-bias test.
- `t168` (blocked, P3): Genomics England 100K feasibility memo; access requires UK-institution
  collaboration; exploratory only.
- `t169` (blocked, P3): GTEx v10 + Yizhak 2019 / Rockweiler 2023 somatic call sets; blocked on
  institutional affiliation for controlled-access tiers; revisit when affiliation is
  re-established.

**Live question.** `question:0007-cross-tissue-somatic-mutation-rate-variation-as-null-model`
remains the primary open question anchoring this hypothesis; resolution depends on `t150`
completing a cohort audit and `t151` delivering a single-tissue pilot result.

**Promotion gates.** All three conditions stated in the hypothesis spec must be met: feasibility
audit completes (t150), at least 6 cBioPortal-relevant tissues are covered at per-decade
age-stratification scale, and a scoped first analysis testing P3 on at least one tissue is
identified with a pre-registered effect-size target (t114 + t151 jointly fulfill this gate).
