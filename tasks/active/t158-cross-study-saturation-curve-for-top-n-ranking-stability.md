---
id: t158
project: ''
title: Cross-study saturation curve for top-N ranking stability
type: ''
aspects:
- computational-analysis
priority: P3
status: proposed
blocked_by: []
related:
- question:0017-cross-study-saturation-curve
- question:0013-cross-study-replication-rate
- hypothesis:0002-cross-study-ranking-divergence-is-structured
- task:t072
- task:t149
parent: ''
group: validation
artifacts: []
findings: []
created: '2026-04-28'
completed: null
---

Run k-study subsampling ablations for evaluable cancer types and pan-cancer rankings. For k in a pre-registered grid (e.g. 1, 2, 3, 5, 10, 20, all), repeatedly sample k studies, recompute top-N rankings, and estimate variance / Jaccard / Spearman to the full-study reference. Identify the saturation point or mark cancers as unsaturated.

Acceptance: `doc/interpretations/<date>-q017-cross-study-saturation-curve.md` with per-cancer saturation status and recommendations for reporting thresholds.
