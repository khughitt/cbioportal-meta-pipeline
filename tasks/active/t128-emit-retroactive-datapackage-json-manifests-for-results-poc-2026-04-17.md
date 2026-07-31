---
id: t128
project: ''
title: Emit retroactive datapackage.json manifests for results/poc-2026-04-17/ and
  results/signature-brca-2026-04-22/
type: ''
aspects:
- software-development
priority: P2
status: proposed
blocked_by: []
related:
- task:t100
- meta:0007-next-steps-and-gap-analysis-2026-04-24
parent: ''
group: pipeline
artifacts: []
findings: []
created: '2026-04-24'
completed: null
---

Two workflow output directories currently sit on disk with no datapackage.json manifests: results/poc-2026-04-17/ (t100 PoC annotated artifact) and results/signature-brca-2026-04-22/ (t109/t110 signature-restriction outputs). Write Frictionless Data Package manifests retroactively so provenance is filesystem-readable rather than narrative-only. Recurring gap flagged on both 2026-04-22 and 2026-04-24.
