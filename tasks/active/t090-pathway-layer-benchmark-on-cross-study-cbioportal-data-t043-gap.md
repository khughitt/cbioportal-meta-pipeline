---
id: t090
project: ''
title: Pathway-layer benchmark on cross-study cBioPortal data (t043 gap)
type: ''
aspects:
- computational-analysis
priority: P2
status: proposed
blocked_by: []
related:
- search:0005-pathway-level-pan-cancer-methods
- paper:Reyna2020Pathway
- paper:Iorio2018SLAPenrich
- paper:Paczkowska2020
- task:t043
- task:t077
- task:t079
parent: ''
group: meta-analysis
artifacts: []
findings: []
created: '2026-04-14'
completed: null
---

Surfaced as a real gap in t043: no pan-cancer benchmark at the pathway rollup level currently exists (Wu 2022 Brief Bioinform benchmark is gene-level only). Run SLAPenrich vs ActivePathways vs HotNet2 on the pipeline's gene_cancer_study output using a shared pathway database (start with Reactome + Sanchez-Vega-10; KEGG and MSigDB Hallmarks as comparators) across multiple cBioPortal cohorts and report method concordance. Natural methodological contribution. Pre-register pathway database + primary method choice before running (ties to t079 pooling pre-registration).
