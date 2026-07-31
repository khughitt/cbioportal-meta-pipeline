---
id: t113
project: ''
title: Close t111 assembly range-check TODO — verify chrom/pos against declared assembly
type: ''
aspects:
- software-development
priority: P3
status: proposed
blocked_by: []
related:
- task:t111
- interpretation:0003-t111-normal-tissue-spectra-pipeline
parent: ''
group: pipeline
artifacts: []
findings: []
created: '2026-04-19'
completed: null
---

Current validate_input_contract accepts the assembly parameter but does not range-check chrom/pos against per-chromosome lengths (marked TODO(t111-followup) at code/scripts/extract_normal_tissue_spectra.py:96-100). A caller who declares wrong assembly gets silent acceptance. Fix: encode GRCh37/GRCh38 max-chromosome-lengths as module constants and validate df['pos'].max() <= length_dict[chrom] for each chromosome. Becomes load-bearing when t112 introduces GRCh38 sources. ~30 min + one test.
