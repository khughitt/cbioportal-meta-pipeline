---
id: t142
project: ''
title: Speed up create_correlation_matrices.py for large studies
type: ''
aspects:
- software-development
priority: P3
status: proposed
blocked_by: []
related:
- task:t131
parent: ''
group: pipeline
artifacts: []
findings: []
created: '2026-04-26'
completed: null
---

**Bottleneck.** `create_correlation_matrices.py` is O(n_genes²) per study and dominates upstream wall time for large cohorts. In the full pan-cancer-dndscv run 2026-04-25, `pancan_pcawg_2020` (~18,500 genes) took 2h 30min for one (cancer_cor.feather, gene_cor.feather) pair; output was 1.33 GB. There are 13 studies in the canonical pan-cancer config; `msk_met_2021` and `genie` are even larger.

**Optimization angles** (in priority order):
1. **`numpy.corrcoef` on the dense matrix** instead of pandas-level pairwise. Order of magnitude.
2. **Pre-filter genes with < K mutations** before correlating — most pairs are noise. Even K=3 should drop 50-80% of genes for most studies.
3. **Sparse representation** for the underlying gene × sample mutation matrix.
4. Per-study parallelism via `-j` already works; per-cell intra-rule multiprocessing could push further.

**Acceptance**: `create_correlation_matrices` for `msk_met_2021` finishes in under 30 minutes on a single core.

**Cross-references**: identified during the t131 full pan-cancer-dndscv run 2026-04-25.
