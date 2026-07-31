---
id: t104
project: ''
title: 'Optimize create_correlation_matrices.py: gene x gene corr scales O(n_genes^2)
  and stalls on whole-exome studies'
type: ''
aspects:
- software-development
priority: P2
status: proposed
blocked_by: []
related:
- task:t100
parent: ''
group: pipeline
artifacts: []
findings: []
created: '2026-04-17'
completed: null
---

Surfaced by t100 PoC run 2026-04-17: create_correlation_matrices for brca_tcga_pan_can_atlas_2018 (~1090 samples x ~20k genes) took ~55 min; same expected for ucec_tcga and skcm_tcga. Panel studies (MSK-IMPACT ~341 genes) are fast. Script computes patient_mut.T.corr() which is O(n_genes^2) in both time and memory. Options: (a) use numpy.corrcoef on float32 matrix (typically 5-10x faster than pandas corr), (b) restrict to the top-K variance genes before correlation (add config key max_genes_for_corr default 5000), (c) sparse-aware correlation via sklearn.metrics.pairwise when count matrix is sparse (>95% zeros typical for mutation count matrices). Recommend starting with (a)+(b) and only falling back to (c) if still too slow. Ref: code/scripts/create_correlation_matrices.py:27 (patient_mut.T.corr()).
