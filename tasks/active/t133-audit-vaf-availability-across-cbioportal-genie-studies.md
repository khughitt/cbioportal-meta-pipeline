---
id: t133
project: ''
title: Audit VAF availability across cBioPortal/GENIE studies
type: ''
aspects:
- software-development
priority: P2
status: proposed
blocked_by: []
related:
- question:0012-mutation-ordering-cross-sectional-inference
- discussion:0002-mutation-ordering-and-path-dependency
parent: ''
group: audits
artifacts: []
findings: []
created: '2026-04-24'
completed: null
---

Hard gate on any clonality-based ordering work. For each study in code/config/config-full.yml, inspect pre-convert_to_feather MAF headers and tally which carry (a) tumor_f / VAF directly, (b) t_alt_count + t_ref_count (can compute VAF), (c) neither. Also record sequencing type (WES vs panel) and matched-normal status. Output: doc/audits/YYYY-MM-DD-vaf-availability-audit.md. Decision rule: if ≥50% of samples retain VAF, unlock pipeline change to preserve VAF; if not, restrict ordering work to CBN/MHN-style population-level inference only.
