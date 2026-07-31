---
id: t131
project: ''
title: Opt dNdScv into rule all via config-pan-cancer-dndscv.yml + three-way ranking
  comparison
type: ''
aspects:
- computational-analysis
- software-development
priority: P2
status: proposed
blocked_by: []
related:
- topic:mutation-rate-normalization
- discussion:0001-gene-length-bias-in-mutation-rankings-and-literature
- question:0011-gene-length-as-literature-attention-confounder
- paper:Martincorena2017
parent: ''
group: pipeline
artifacts: []
findings: []
created: '2026-04-24'
completed: null
---

Add a side config code/config/config-pan-cancer-dndscv.yml that includes the per-study dNdScv outputs (studies/{id}/mut/dndscv/genes.feather) in rule all. Then write a comparison report: raw vs length-adjusted vs dNdScv-selection rankings, Spearman + Jaccard@10/50/100/500, and per-list correlation with PubTator gene-mention counts. Closes the 'length-only is below the 2013 methodology bar' finding from the bias audit and topic:mutation-rate-normalization. CONSTRAINT (per memory:r-reproducibility): the dNdScv rule must use a conda/mamba env YAML or Docker image — never assume system R.
