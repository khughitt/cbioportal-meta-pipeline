---
id: t114
project: ''
title: Pre-register q007 null-model correction impact before rolling into frequency
  pipeline
type: ''
aspects:
- computational-analysis
priority: P2
status: proposed
blocked_by: []
related:
- task:t111
- question:0007-cross-tissue-somatic-mutation-rate-variation-as-null-model
- paper:Li2021
parent: ''
group: pipeline
artifacts: []
findings: []
created: '2026-04-19'
completed: null
---

Before applying the t111 per-tissue snvs_per_mb correction to gene_cancer_study_ratio_annotated.feather frequencies, pre-register: (1) expected number of gene-cancer rankings that shift and by how many positions; (2) head-to-head comparison against a Martincorena 2017 dN/dS-based null as a simpler baseline. If the two approaches rank genes identically, t111's value-add collapses. Prevents ships-before-thinks bias on whether the empirical null is actually discriminating versus a uniform-rate-per-gene-length null. Deliverable: doc/meta/pre-registration-q007-null-model-correction.md.
