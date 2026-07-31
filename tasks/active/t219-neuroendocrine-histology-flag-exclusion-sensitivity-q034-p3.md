---
id: t219
project: ''
title: Neuroendocrine-histology flag + exclusion sensitivity (q034, P3)
type: ''
aspects:
- computational-analysis
- software-development
priority: P2
status: proposed
blocked_by: []
related:
- question:0034-neuroendocrine-histology-confound
- topic:neuroendocrine-neoplasm-lineage-confound
parent: ''
group: neural-gene-meta-analysis
artifacts: []
findings: []
created: '2026-06-06'
completed: null
---

Enumerate NET/NEC OncoTree codes present in pipeline studies; add is_neuroendocrine_histology flag; recompute ranks with NEN excluded. MEN1 rank is the positive-control canary; watch ATRX/NF1 as dual CNS+NEN confounds.

### Notes

- 2026-06-08: Downgrade (t218, 2026-06-08): the plan gated NET exclusion on a residual surviving CNS exclusion. t218 shows no residual survives (the candidate enrichment is fully genomic-span/CFS + one WGS cohort's whole-locus reach; not CNS, not panel, not hypermutator, not selection). Keep t219 only as a quick MEN1-canary NET-exclusion sanity check, not as a residual-explaining step. See interpretation:0042-t218-cns-exclusion-wes-panel.
