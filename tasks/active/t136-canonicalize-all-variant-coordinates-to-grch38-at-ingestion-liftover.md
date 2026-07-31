---
id: t136
project: ''
title: Canonicalize all variant coordinates to GRCh38 at ingestion (liftover from
  hg19)
type: ''
aspects:
- software-development
priority: P2
status: proposed
blocked_by: []
related:
- task:t131
- topic:mutation-rate-normalization
- discussion:0001-gene-length-bias-in-mutation-rankings-and-literature
parent: ''
group: pipeline
artifacts: []
findings: []
created: '2026-04-24'
completed: null
---

Add a liftover step in convert_to_feather.py that maps hg19-native study variants to GRCh38 using CrossMap or pyliftover with UCSC hg19ToHg38.over.chain.gz. Retain original chr/pos/build columns for audit. Single canonical build downstream unlocks dNdScv refdb selection, future GRCh38-only annotation sources (gnomAD v4, ClinVar, dbNSFP v4.x, AlphaMissense, latest COSMIC), and removes a class of silent-degradation bugs across the pipeline. Exonic SNV loss expected <0.1% (per UCSC chain coverage). This is the long-term destination flagged during t131 design — t131 itself uses cheaper per-study refdb routing as an interim. Out of scope for this task: re-running upstream tooling against the lifted coordinates (signature callers, replication-timing joins). Plan separately for those once the liftover artifact is in place.
