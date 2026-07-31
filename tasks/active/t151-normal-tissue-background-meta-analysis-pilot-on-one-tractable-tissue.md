---
id: t151
project: ''
title: Normal-tissue background meta-analysis pilot on one tractable tissue
type: ''
aspects:
- computational-analysis
priority: P2
status: proposed
blocked_by: []
related:
- task:t150
- hypothesis:0005-healthy-somatic-background-atlas
- hypothesis:0001-non-tumor-signal-contamination
- question:0007-cross-tissue-somatic-mutation-rate-variation-as-null-model
parent: ''
group: meta-analysis
artifacts: []
findings: []
created: '2026-04-28'
completed: null
---

After `t150`, run a scoped pilot on the most tractable tissue (likely esophagus or colon). Estimate an age-stratified normal-tissue mutation background and substitute it into the relevant `h01` contamination test (e.g. q001 NOTCH1 in esophagus). Report whether the cross-tissue normal null improves matched-vs-unmatched correction over the current within-pipeline null.

Acceptance: one tissue-specific interpretation document with effect size, uncertainty, and a recommendation on whether to scale the atlas work.
