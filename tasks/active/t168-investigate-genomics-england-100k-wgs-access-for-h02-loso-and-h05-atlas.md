---
id: t168
project: ''
title: Investigate Genomics England 100K WGS access for h02 LOSO and h05 atlas
type: ''
aspects:
- computational-analysis
priority: P3
status: blocked
blocked_by: []
related:
- hypothesis:0002-cross-study-ranking-divergence-is-structured
- hypothesis:0005-healthy-somatic-background-atlas
- question:0013-cross-study-replication-rate
- question:0017-cross-study-saturation-curve
parent: ''
group: dataset-acquisition
artifacts: []
findings: []
created: '2026-04-28'
completed: null
---

Genomics England 100K Genomes Project: ~70,000 cancer WGS samples + matched germline, harmonized through the Cancer Programme pipeline. Largest single WGS cancer cohort in the world. Motivations: (1) h02 saturation curve (q017, t158): testing whether top-N ranking stability saturates at the WGS-scale becomes possible only with cohorts in the 50k+ range; cBioPortal+GENIE+Hartwig+PCAWG combined still does not reach this scale uniformly. (2) h05 healthy somatic background: GEL holds matched-germline WGS, which is the closest existing approximation to a population-level normal somatic-mutation reference at scale. Access barrier: UK-only DAC; non-UK researchers must collaborate with a UK-based institution (Genomics England Research Environment is a secure analysis platform — cannot extract raw data). This task is exploratory: file as 'investigate' rather than 'integrate', because the access friction is high and the pipeline would need to run inside the GE Research Environment rather than ingesting locally. Acceptance: a one-page memo at doc/feasibility/2026-XX-genomics-england-feasibility.md with go/no-go recommendation, contingent partnership candidates, and an estimate of integration cost.
