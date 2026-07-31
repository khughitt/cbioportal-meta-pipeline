---
id: t148
project: ''
title: Replace single-cancer best_cancer_type with multi-cancer set field in per-gene
  rollup
type: ''
aspects:
- software-development
priority: P3
status: proposed
blocked_by: []
related:
- task:t131
- task:t144
- interpretation:0009-t131-full-pan-cancer-dndscv-run
parent: ''
group: pipeline
artifacts: []
findings: []
created: '2026-04-26'
completed: null
---

The current `best_cancer_type` column in `dndscv_pooled.feather` and `three_way_ranking_comparison.feather` reports a single cancer type as "best", chosen by `idxmin(min_q)`. At full pan-cancer scale this is dominated by alphabetical-tie artifacts (Ampullary Cancer appears as "best" for TP53, KRAS, PIK3CA, ARID1A, ARID2 — purely because of alphabetical tiebreaking among many cancers all hitting q=0). t144 will partially fix this for the top hits, but the underlying single-cancer field is information-lossy when many cancers tie.

**Replace** `best_cancer_type` with one or more of:
- `cancers_with_significant_q05` (sorted list / count) — already partially captured as `n_cancers_significant_q05`; expose the cancer names too.
- `most_significant_cancer_by_n_samples` (cohort-power-weighted; tie-broken by larger cohort).

**Acceptance**: per-gene rollup carries enough information to identify *which* cancer types contribute to a gene's q-significance, not just one alphabetically-arbitrary "best".
