---
id: t108
project: ''
title: Investigate is_hypermutator_relative reporting ~45% for BRCA (Samstein top-20%
  should cap at ~20%)
type: ''
aspects:
- software-development
priority: P2
status: proposed
blocked_by: []
related:
- task:t097
- task:t100
- paper:Samstein2019
- interpretation:0001-poc-run
parent: ''
group: pipeline
artifacts: []
findings: []
created: '2026-04-17'
completed: null
---

Surfaced by t100 PoC 2026-04-17: is_hypermutator_relative reports 45.5% for brca_tcga_pan_can_atlas_2018 and 36.4% for skcm_tcga_pan_can_atlas_2018 (from doc/interpretations/2026-04-17-poc-run.md Finding 4). The Samstein 2019 definition is 'top-20%% TMB within the sample's histology' — which should yield at most ~20%% hypermutators per cancer type (slightly more with ties at the boundary). 45%% / 36%% far exceed this. Likely causes: (a) tied-sample promotion at the 80th-percentile cut without explicit tiebreak policy, (b) the per-histology grouping key is cancer_type but the TCGA 'cancer_type' labels collapse many distinct histologies into one bucket (e.g. 'Breast Cancer'), so a large fraction of samples tie at a low TMB boundary, or (c) an off-by-one in the quantile cut logic. Inspect _relative_top_quintile_flag in code/scripts/annotate_hypermutators.py (line 200 area).
