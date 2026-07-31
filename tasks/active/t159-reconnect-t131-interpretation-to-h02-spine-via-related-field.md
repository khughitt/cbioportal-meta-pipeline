---
id: t159
project: ''
title: 'Reconnect t131 interpretation to h02 spine via related: field'
type: ''
aspects:
- computational-analysis
priority: P2
status: proposed
blocked_by: []
related:
- interpretation:0009-t131-full-pan-cancer-dndscv-run
- hypothesis:0002-cross-study-ranking-divergence-is-structured
parent: ''
group: spine-hygiene
artifacts: []
findings: []
created: '2026-04-28'
completed: null
---

Big-picture validator flagged t131 as orphan because its frontmatter cites question:0011 in source_refs but not in related:. Add hypothesis:0002-cross-study-ranking-divergence-is-structured to the related: list so the resolver picks it up. Pure metadata fix, no analysis change. Acceptance: validator no longer reports t131 as orphan.
