---
id: t112
project: ''
title: Integrate Lee-Six 2018 blood (or Xu 2025 dbGaP) as second normal-tissue source
  for t111 outputs
type: ''
aspects:
- software-development
priority: P3
status: proposed
blocked_by: []
related:
- task:t111
- topic:signature-decomposition-unmatched-normal
- question:0006-ch-priority-gene-completeness
- question:0008-signature-decomposition-tissue-background-subtraction
- paper:LeeSix2018
- paper:Xu2025
parent: ''
group: pipeline
artifacts: []
findings: []
created: '2026-04-18'
completed: null
---

Follow-up to t111 (which was reduced to Li2021-only by the 2026-04-19 data-access gate because Xu2025 per-variant data is dbGaP-controlled). Add a second open-access normal-tissue source to enrich data/normal_tissue_spectra.tsv and data/normal_tissue_burden.tsv. Preferred source: Lee-Six 2018 (Nature, DOI 10.1038/s41586-018-0497-0) — single-donor ~140 HSC WGS colonies — complements Li2021's solid-tissue bias with blood where CH matters for q006/q008. Second-choice source: Xu2025 via dbGaP DAR (weeks of calendar time; only worth pursuing if a user has existing GTEx access). This task refactors code/scripts/extract_normal_tissue_spectra.py into the plugin-style adapters/ pattern planned in t111's scope brainstorming (option C: 'start hard-coded to 2 sources, plugin-ize when 3rd arrives').
