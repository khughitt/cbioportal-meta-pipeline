---
id: t055
project: ''
title: 'Pipeline addition: M/C-class descriptor (mutation-vs-CNA hyperbola)'
type: ''
aspects:
- software-development
priority: P3
status: deferred
blocked_by: []
related: []
parent: ''
group: pipeline
artifacts: []
findings: []
created: '2026-04-13'
completed: null
---

Compute per-tumor and per-cancer mutation-count vs SCNA-burden axis (Ciriello2013 cancer genome hyperbola). Cheap secondary descriptor. Blocked: requires CNA data ingestion which our pipeline does not currently have.

Blocked on CNA ingestion — no CNA scripts in code/scripts/, no rule in Snakefile, and CNA is outside current specs/research-question.md scope. Revisit when / if CNA modality is added.
