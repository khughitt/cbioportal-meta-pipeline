---
id: t129
project: ''
title: Length × PubMed-mention regression pipeline step (q011)
type: ''
aspects:
- computational-analysis
priority: P2
status: proposed
blocked_by: []
related:
- question:0011-gene-length-as-literature-attention-confounder
- topic:mutation-rate-normalization
- discussion:0001-gene-length-bias-in-mutation-rankings-and-literature
- task:t082
parent: ''
group: meta-analysis
artifacts: []
findings: []
created: '2026-04-24'
completed: null
---

Implement the regression spec'd in q011: log(mention_count+1) ~ log(protein_length) + log(mutation_count+1) over protein-coding genes (PubTator 2026-01-16 + UniProt + cBioPortal aggregate counts). Report marginal vs partial length slope with bootstrap CIs. Subgroup by Bailey 2018 driver list. Sensitivity: dNdScv-corrected counts, disease-co-mention covariate, non-cancer placebo slice. Output: doc/interpretations/<date>-q011-length-attention-regression.md plus a length-residualized 'attention prior' feather under models/. Requires HGNC alias mapping (t082) for the PubTator↔UniProt join.
