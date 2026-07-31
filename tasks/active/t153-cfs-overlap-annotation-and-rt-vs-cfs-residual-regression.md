---
id: t153
project: ''
title: CFS overlap annotation and RT-vs-CFS residual regression
type: ''
aspects:
- computational-analysis
- software-development
priority: P2
status: proposed
blocked_by: []
related:
- question:0014-cfs-as-distinct-confounder-class
- question:0003-replication-timing-as-gene-level-mutation-rate-confounder
- hypothesis:0001-non-tumor-signal-contamination
- hypothesis:0002-cross-study-ranking-divergence-is-structured
- task:t121
parent: ''
group: meta-analysis
artifacts: []
findings: []
created: '2026-04-28'
completed: null
---

Build a per-gene common-fragile-site overlap annotation from published CFS catalogues and join it to the existing gene-level replication-timing map. Regress per-gene mutation-rate residuals on both RT-late status and CFS overlap. If CFS carries a non-zero coefficient after RT adjustment, treat CFS as a distinct correction channel.

Acceptance: CFS annotation artifact under `data/` or `models/`, plus `doc/interpretations/<date>-q014-cfs-vs-rt.md` with coefficient estimates and a correction recommendation.
