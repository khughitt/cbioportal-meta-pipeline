---
id: t138
project: ''
title: Add canalization-collapse interpretive note to t081 hypermutator topic
type: ''
aspects:
- computational-analysis
priority: P3
status: proposed
blocked_by: []
related:
- task:t081
- paper:Bavisetty2025
- paper:Lu2023
- paper:Rashid2025
- paper:Jung2025
- synthesis:0002-canalization-in-gene-regulatory-networks-cross-paper-synthesis-for-the
- topic:tumor-mutational-burden
parent: ''
group: docs
artifacts: []
findings: []
created: '2026-04-25'
completed: null
---

Add a short interpretive section to the hypermutator/TMB topic note (or a new sub-note) framing 'is_hypermutator = True' tumors as cells in which canalization has collapsed, and the 8-category hypermutator_reason audit trail (pole_hotspot / pold1_hotspot / msi_h / gmm_upper_mode / gmm_lower_mode / zscore_fallback_high / zscore_fallback_low / tmb_unavailable) as different *modes* of canalization failure. Source: doc/papers/synthesis-2026-04-25-canalization-gene-regulatory-networks.md (Combined implications #2). Cheap, doc-only — no pipeline code change. Cross-link from the topic note back to the synthesis and to Bavisetty2025, Lu2023, Rashid2025, Jung2025.
