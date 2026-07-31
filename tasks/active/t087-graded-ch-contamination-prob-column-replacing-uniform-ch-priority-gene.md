---
id: t087
project: ''
title: Graded ch_contamination_prob column replacing uniform ch_priority_gene boolean
type: ''
aspects:
- software-development
priority: P2
status: proposed
blocked_by: []
related:
- search:0004-asxl1-tet2-ch-disambiguation
- topic:clonal-hematopoiesis-contamination
- paper:Coombs2018
- task:t059
parent: ''
group: pipeline
artifacts: []
findings: []
created: '2026-04-14'
completed: null
---

Replace the uniform ch_priority_gene boolean emitted by annotate_ch.py with a graded ch_contamination_prob column sourced from Coombs 2018 Table 2 (per-gene variant-level CH confirmation rate in paired-tumor/blood cohort). Anchor values: DNMT3A ~64%, TP53 ~4%, overall across the 9-gene CH panel ~8%. ASXL1 and TET2 intermediate — read Coombs 2018 Table 2 for the precise numbers. Keep the boolean as a backward-compatible column (computed by thresholding the graded prob at 0.5) until downstream consumers migrate. Closes the open question surfaced in t059: uniform CH flagging over-masks bona fide solid-tumor ASXL1 biology (MSI-CRC polyG-indel, CRPC, HNSCC per Katoh 2013).
