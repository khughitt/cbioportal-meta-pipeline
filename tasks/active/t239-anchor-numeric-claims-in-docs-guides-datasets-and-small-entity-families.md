---
id: t239
project: ''
title: Anchor numeric claims in docs, guides, datasets, and small entity families
type: ''
aspects:
- computational-analysis
priority: P3
status: proposed
blocked_by: []
related:
- task:t233
- task:t234
parent: ''
group: science-strict-validation-cleanup
artifacts: []
findings: []
created: '2026-06-28'
completed: null
---

Cleanup batch for smaller numeric-anchor families after t234 upstream parser work. Current baseline after the upstream DOI/identifier fix and the first t235 exact-reference passes: doc/plans 34, doc/meta 9, doc/guides/modalities 2, entities/datasets 7, entities/pre-registrations 15, entities/questions 14, entities/synthesis 11, entities/hypotheses 4, entities/modality-guide 5, entities/discussions 1, and entities/topics 32. For real numeric claims, add nearby anchors or reduce unsupported precision.
