---
id: t167
project: ''
title: Acquire and integrate PCAWG / ICGC-25K WGS cohort
type: ''
aspects:
- computational-analysis
priority: P3
status: blocked
blocked_by: []
related:
- hypothesis:0001-non-tumor-signal-contamination
- hypothesis:0002-cross-study-ranking-divergence-is-structured
- hypothesis:0004-mhn-pathway-ordering
- question:0009-sbs1-lrr-bias-as-normal-contamination-flag
- question:0012-mutation-ordering-cross-sectional-inference
- paper:PCAWG2020
parent: ''
group: dataset-acquisition
artifacts: []
findings: []
created: '2026-04-28'
completed: null
---

PCAWG (~2,800 tumors, 38 cancer types, fully WGS, matched normals, harmonized PanCancer Analysis of Whole Genomes consortium calls) is the canonical WGS-tier comparator for any rank-stability or topographic claim. Three motivations specific to this project. (1) Cross-validation against Gerstung 2020: the PCAWG chronology paper provides per-cancer mutation-order benchmarks against which any h04 MHN result must be sanity-checked; we cannot run that benchmark without PCAWG-tier data in our pipeline. (2) Topographic / signature-bias diagnostics (q009, h07 if filed): same payoff as Hartwig but with broader cancer-type coverage and primary-tumor (vs metastatic) sample distribution. (3) h02 LOSO replication test (t149): adding PCAWG as one held-out cohort tests whether the 62/100 Bailey recovery in dNdScv survives leave-one-cohort-out at the WGS stratum level. Access: dbGaP phs001629 (PCAWG mutations) requires institutional DAR; ICGC DACO governs the broader release. Practical scope: ingest the consensus mutation calls TSV (parallel to the MC3 path) as one pseudo-study or per-project pseudo-studies; the difficult bit is CNA calls (not modeled by the pipeline yet, out-of-scope per AGENTS.md). Acceptance: data/pcawg_v2/ ingested; ≥30 cancer types appear in per-study feathers; one held-out LOSO iteration runs successfully; one Gerstung 2020 chronology comparison appended to t152 calibration if h04 has progressed.
