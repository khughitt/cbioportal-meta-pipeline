---
id: t152
project: ''
title: Replicate Vocht 2026 LUAD MHN demo and run simulation calibration
type: ''
aspects:
- computational-analysis
priority: P2
status: proposed
blocked_by: []
related:
- hypothesis:0004-mhn-pathway-ordering
- question:0012-mutation-ordering-cross-sectional-inference
- task:t135
- paper:Vocht2026
- paper:Schill2024
parent: ''
group: validation
artifacts: []
findings: []
created: '2026-04-28'
completed: null
---

Install `mhn` via `uv add mhn`, reproduce the Vocht 2026 GENIE LUAD demonstration as closely as possible on the project's GENIE release, and benchmark runtime / active-event limits. Then generate synthetic tumors from a known MHN, subsample to project-like panel and cohort-size distributions, and test whether the observation-event MHN recovers >=70% of injected pathway-level edges.

Acceptance: `doc/interpretations/<date>-mhn-luad-demo-and-simulation-calibration.md`; explicit decision on whether `h04` can be promoted or remains candidate.

Implementation plan: `doc/plans/2026-05-02-t135-t152-ordering-validation-plan.md`.
