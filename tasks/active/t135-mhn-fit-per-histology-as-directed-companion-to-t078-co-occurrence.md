---
id: t135
project: ''
title: MHN fit per histology as directed companion to t078 co-occurrence results
type: ''
aspects:
- computational-analysis
priority: P3
status: proposed
blocked_by: []
related:
- question:0012-mutation-ordering-cross-sectional-inference
- hypothesis:0004-mhn-pathway-ordering
- paper:Schill2024
- paper:Vocht2026
- task:t078
- task:t081
- task:t111
- task:t152
parent: ''
group: meta-analysis
artifacts: []
findings: []
created: '2026-04-24'
completed: null
---

t078 co-occurrence/mutual-exclusivity landed 2026-04-25 (no longer blocking). Add observation-event Mutual Hazard Network fit (Schill 2024 / Vocht 2026), using the same sample-specific-background-rate null and per-sample callability mask. Report primary results at Sanchez-Vega 10-pathway level; gene-level as drill-down. Stratify per histology and per hypermutator class (t081). Calibrate against PCAWG Gerstung 2020 pan-cancer chronology Table 1 before reporting any novel edges. Do not report classical cMHN-only edges as biological ordering evidence; cMHN is a baseline for bias comparison only.

Implementation plan: `doc/plans/2026-05-02-t135-t152-ordering-validation-plan.md`.
