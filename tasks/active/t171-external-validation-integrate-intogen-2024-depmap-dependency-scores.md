---
id: t171
project: ''
title: 'External validation: integrate IntOGen 2024 + DepMap dependency scores'
type: ''
aspects:
- computational-analysis
priority: P1
status: proposed
blocked_by: []
related:
- hypothesis:0002-cross-study-ranking-divergence-is-structured
- task:t146
- question:0013-cross-study-replication-rate
parent: ''
group: dataset-acquisition
artifacts: []
findings: []
created: '2026-04-28'
completed: null
---

t146 (external validation of pan-cancer dNdScv ranking against IntOGen / Martincorena 2017) is the bias-mitigation step for the Bailey-circularity caveat: Bailey 2018 was used to build the project's driver overlay, so reporting Bailey recovery as the headline external-validation number is partially circular. Two independently-constructed external benchmarks resolve this. (1) IntOGen 2024: their 2024 release uses a different driver-detection ensemble (OncodriveFML, OncodriveCLUSTL, MutPanning, etc.) on a different cohort union; recovery against IntOGen is the cleanest 'does the project's rank match independent driver discovery' test. (2) DepMap CRISPR essentiality: orthogonal axis entirely — does the project's top-N pan-cancer driver list intersect more strongly with DepMap-essential genes than chance? This is the biology-not-statistics validation. Both are free public downloads (intogen.org/download; depmap.org/portal). Pipeline integration scope: a code/scripts/build_external_driver_benchmarks.py that pulls IntOGen 2024 driver list (per cancer type and pan-cancer) and DepMap 23Q4+ gene-essentiality scores (mean + cancer-type-stratified), emits external_driver_benchmarks.feather. t146 then computes Spearman, Jaccard@K, and odds-ratio for the project's dNdScv top-N vs each. Acceptance: external_driver_benchmarks.feather exists; t146 produces doc/interpretations/<date>-t146-external-validation.md with three numbers (vs IntOGen, vs Martincorena 2017, vs DepMap) plus interpretation.
