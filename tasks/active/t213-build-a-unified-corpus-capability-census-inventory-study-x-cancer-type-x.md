---
id: t213
project: ''
title: Build a unified corpus-capability census inventory (study x cancer_type x assay
  x matched_normal x n_samples x treatment_flag x indel_depth x caller_provenance)
type: ''
aspects:
- computational-analysis
priority: P2
status: proposed
blocked_by: []
related:
- question:0026-cancer-types-with-multiple-independent-cbioportal
- question:0028-indel-call-availability-across-cbioportal-studies
- question:0017-cross-study-saturation-curve
- question:0024-treatment-exposed-cohort-chemotherapy-signature
- theme:0001-assay-regime-panel-wes-wgs-as-a-master-technical-confounder-spanning
- hypothesis:0008-cross-study-signature-exposure-reproducibility
parent: ''
group: corpus-capability-census
artifacts: []
findings: []
created: '2026-06-02'
completed: null
---

One inventory feather that multiple hypotheses are independently re-deriving. h10 found only 1 adequate treatment cohort in 198 studies; q026/q028/q017 each separately enumerate corpus capacity. Consolidate into a single per-study capability table so replication-depth questions (per cancer x condition) are answered from one source. Powers q026 (>=2 studies/cancer), q028 (indel depth), q024/q027 (treatment cohorts), q017 (saturation), and the assay-regime theme.
