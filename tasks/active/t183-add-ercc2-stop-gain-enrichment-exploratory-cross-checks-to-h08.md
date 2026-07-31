---
id: t183
project: ''
title: Add ERCC2 + stop-gain-enrichment exploratory cross-checks to h08
type: ''
aspects:
- computational-analysis
priority: P3
status: proposed
blocked_by: []
related:
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
- method:h08-agnostic-association-model
- question:0021-positive-control-signature-set-expansion-sbs9
parent: ''
group: hypothesis-h08
artifacts: []
findings: []
created: '2026-05-31'
completed: null
---

Two exploratory secondary checks: (1) ERCC2 somatic-mutation status as a bladder/urothelial
positive-control covariate targeting SBS5 (paper:Kim2016 ground truth); (2) after any confirmed
SBS4/SBS13 hit, verify elevated nonsense burden in the Adler2023 protein-truncation gene set via
the existing Bailey2018 driver overlay. Sources: paper:Kim2016, paper:Adler2023.
