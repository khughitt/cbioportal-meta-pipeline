---
id: t134
project: ''
title: 'Pipeline addition: retain VAF (t_alt_count, t_ref_count, tumor_f) in per-study
  variant feathers'
type: ''
aspects:
- software-development
priority: P3
status: proposed
blocked_by:
- Audit VAF availability across cBioPortal/GENIE studies
related:
- question:0012-mutation-ordering-cross-sectional-inference
parent: ''
group: pipeline
artifacts: []
findings: []
created: '2026-04-24'
completed: null
---

Extend convert_to_feather.py to retain per-variant allele-count columns alongside gene/sample presence calls. Unblocks clonality-based ordering (MHN validation companion), CCF estimation, per-sample signature deconvolution at variant level, and general driver-evolution work. Contingent on VAF-availability audit confirming retention is worthwhile.
