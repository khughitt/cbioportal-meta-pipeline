---
id: t139
project: ''
title: Promote t077 meta-analysis to canonical cross-study aggregation
type: ''
aspects:
- computational-analysis
- software-development
priority: P2
status: proposed
blocked_by: []
related:
- task:t077
- task:t131
- task:t086
parent: ''
group: pipeline
artifacts: []
findings: []
created: '2026-04-25'
completed: null
---

The simple sample-weighted aggregation in `create_combined_gene_cancer_freq_table.py` bakes in the assumption that all studies measure all cancers identically, which fails for mixed-panel cohorts (e.g., metastatic_solid_tumors_mich_2017, pog570_bcgsc_2020 contributing 4-8 samples to cancer types where another study contributes hundreds). The current guardrail (the `ValueError: Per-cancer cohort-size recovery assumption violated` at line 346) hard-fails the rule rather than computing a biased aggregate.

The project's t077 meta-analysis pipeline (`run_gene_cancer_meta_analysis.R`) is the right long-term home for cross-study aggregation: each study is treated as an independent stratum, between-study heterogeneity is absorbed into variance components, and per-(study, cancer) cohort-size differences are handled correctly without requiring the homogeneity assumption.

**Goal**: promote `gene_cancer_pooled.feather` (t077 output) to the canonical cross-study aggregation. Demote the simple sample-weighted aggregation to "exploratory descriptive only" (or remove if no consumer remains). Have downstream rules — including `join_dndscv_into_annotated` (t131) — source from the meta-analysis output.

**Why dndscv first**: the t131 dNdScv chain's per-gene min_qglobal rollup is itself a meta-analysis-style aggregation. Sourcing its annotation feather from a meta-analysis-based aggregation is more philosophically consistent than sourcing from the naive sample-weighted sum.

**Effects**:
- Removes the load-bearing role of the cohort-size validation in create_combined_gene_cancer_freq_table — that validation can either be retired or moved to a separate diagnostic rule.
- Unblocks future run configs with mixed-panel-cohort studies without requiring per-(study, cancer) exclusion lists.
- Keeps the existing gene_cancer_study.feather long-format output intact (per the t131 review interim split) — this task only changes which AGGREGATION is canonical, not what's available.

**Cross-references**: this task is the long-term destination; a short-term split was applied 2026-04-25 to unblock t131 (see commit history).
