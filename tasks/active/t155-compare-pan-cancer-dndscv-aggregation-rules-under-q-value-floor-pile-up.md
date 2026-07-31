---
id: t155
project: ''
title: Compare pan-cancer dNdScv aggregation rules under q-value floor pile-up
type: ''
aspects:
- computational-analysis
priority: P3
status: proposed
blocked_by: []
related:
- question:0015-pan-cancer-aggregator-choice
- hypothesis:0002-cross-study-ranking-divergence-is-structured
- task:t144
- task:t146
- task:t148
parent: ''
group: meta-analysis
artifacts: []
findings: []
created: '2026-04-28'
completed: null
---

Evaluate candidate per-gene pan-cancer dNdScv aggregators on the existing per-cancer dNdScv outputs: current lexicographic `(min_q, n_cancers_significant_q05)`, Stouffer/Fisher-style combined evidence, rank pooling, and cancer-count weighted variants. Compare Bailey recovery, IntOGen / Martincorena agreement, and leave-one-cancer-out stability.

Acceptance: `doc/interpretations/<date>-q015-dndscv-aggregator-choice.md` and a pre-registered default aggregator recommendation for production outputs.
