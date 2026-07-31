---
id: t175
project: ''
title: Integrate standalone analysis scripts into Snakemake when promoted to recurring
  outputs
type: ''
aspects:
- software-development
priority: P2
status: proposed
blocked_by: []
related:
- task:t154
- task:t163
- question:0016-panel-induced-ascertainment
- question:0003-replication-timing-as-gene-level-mutation-rate-confounder
parent: ''
group: pipeline
artifacts: []
findings: []
created: '2026-04-29'
completed: null
---

The t154 panel-vs-WES ascertainment and t163 RT residual analyses currently run as standalone
tested scripts that write outputs under `/data/packages/cbioportal/pan-cancer/summary/`. That is
appropriate for first-pass hypothesis testing, but if either analysis becomes a recurring
consumer-facing output it should be wired into `code/workflows/Snakefile` with explicit inputs,
outputs, and config-gated inclusion in `rule all` or a named analysis target.

Acceptance: add Snakemake rules for promoted standalone analyses, document their output locations
in `doc/guides/canonical-outputs.md` or the relevant modality guide, and keep one CLI smoke path for
ad-hoc reruns.
