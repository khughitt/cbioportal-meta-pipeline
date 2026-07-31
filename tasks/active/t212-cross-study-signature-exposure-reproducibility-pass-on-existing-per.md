---
id: t212
project: ''
title: Cross-study signature-exposure reproducibility pass on existing per-study SBS
  assignments
type: ''
aspects:
- computational-analysis
priority: P2
status: proposed
blocked_by: []
related:
- hypothesis:0008-cross-study-signature-exposure-reproducibility
- method:h08-agnostic-association-model
- question:0018-can-mutational-signature-decomposition-be-added-downstream-of-the-cross
parent: ''
group: hypothesis-h09
artifacts: []
findings: []
created: '2026-06-01'
completed: null
---

First concrete, data-unblocked test of h09: using per-sample SBS exposures already on disk (run_restricted_sigprofiler_assignment outputs), compare per-cancer-type signature-exposure profiles across independent cBioPortal studies and quantify whether divergences track technical batch (caller/panel/treatment per t178/t179 provenance flags) vs biology. h09 currently has zero tracked tasks (surfaced by 2026-06-01 backlog review). Deliverable: doc/interpretations/<date>-h09-cross-study-exposure-reproducibility.md with a per-cancer reproducibility metric and a batch-vs-biology attribution.
