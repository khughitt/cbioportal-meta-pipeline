---
id: t161
project: ''
title: Absorb orphan questions q014/q016/q017 into hypothesis spine
type: ''
aspects:
- computational-analysis
priority: P2
status: proposed
blocked_by: []
related:
- hypothesis:0002-cross-study-ranking-divergence-is-structured
- hypothesis:0003-gene-length-confounds-literature-attention
- question:0014-cfs-as-distinct-confounder-class
- question:0016-panel-induced-ascertainment
- question:0017-cross-study-saturation-curve
parent: ''
group: spine-hygiene
artifacts: []
findings: []
created: '2026-04-28'
completed: null
---

Resolver currently treats q014/q016/q017 as orphan questions even though they substantively belong on the spine. Amend specs/hypotheses/h02-*.md related: to add q014 (CFS gene-level confounder refinement) and q017 (saturation curve). Amend specs/hypotheses/h03-*.md related: to add q016 (panel-induced ascertainment). Pure metadata change. Acceptance: resolve-questions output drops these three from the orphan set; emergent-threads regenerates with smaller orphan_question_count.
