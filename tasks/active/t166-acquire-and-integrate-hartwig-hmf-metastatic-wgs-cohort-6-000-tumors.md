---
id: t166
project: ''
title: Acquire and integrate Hartwig HMF metastatic WGS cohort (~6,000 tumors)
type: ''
aspects:
- computational-analysis
priority: P3
status: blocked
blocked_by: []
related:
- hypothesis:0001-non-tumor-signal-contamination
- hypothesis:0002-cross-study-ranking-divergence-is-structured
- hypothesis:0005-healthy-somatic-background-atlas
- question:0009-sbs1-lrr-bias-as-normal-contamination-flag
- topic:signature-decomposition-unmatched-normal
- topic:targeted-panel-sequencing-bias
parent: ''
group: dataset-acquisition
artifacts: []
findings: []
created: '2026-04-28'
completed: null
---

Hartwig Medical Foundation database is a research-access metastatic WGS cohort, ~6000 tumors with matched normals, deeply called and uniformly processed. Adding it would unblock several lines simultaneously. (1) q009 SBS1 LRR-bias diagnostic was deferred (interpretation:0007-t126-sbs1-lrr-bias-per-study) under a pre-registered termination rule because MSK-IMPACT panel coverage of constitutive late-replicating bins is structurally insufficient (~20.7 kb across the panel; n_sbs1_pooled = 176 vs 500-floor; CI half-width 0.194 vs 0.10 ceiling). Hartwig WGS bypasses this entirely — every constitutive LRR bin is fully sampled. (2) h02 panel-vs-WES ascertainment work (t154) currently relies on TCGA MC3 as the WES comparator, which is matched-normal but primary-tumor; Hartwig adds a matched-normal metastatic comparator for stage-effect deconfounding. (3) h05 cross-tissue background atlas: Hartwig matched normals provide a clean cross-tissue normal sample distribution covering ~25 cancer-relevant tissues. (4) Replication-timing residual regression at full WGS scale (t163) becomes possible without panel-coverage caveats. Access: DUA via hartwigmedicalfoundation.nl/applying-for-data, typically 3-6 months. Pipeline integration scope: ingest as a single pseudo-study (parallel to tcga_mc3 MC3 path, code/scripts/process_mc3.py), add it to the matched_normal_studies config list, validate WES-vs-WGS callable-region denominators in build_panel_callable_sizes. Acceptance: data/hartwig_v6/ populated; convert_to_feather pipeline ingests; per-study mutation feathers exist for ≥20 cancer types; one rerun of the t126 SBS1 LRR-bias test on the Hartwig subset reaching a non-deferred verdict.
