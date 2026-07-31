---
id: t164
project: ''
title: 'Draft candidate hypothesis h07: signature/topography-based contamination QC
  (absorbs q009)'
type: ''
aspects:
- computational-analysis
priority: P2
status: proposed
blocked_by: []
related:
- question:0009-sbs1-lrr-bias-as-normal-contamination-flag
- hypothesis:0001-non-tumor-signal-contamination
- interpretation:0006-t123-rt-brca-sbs1-proxy-pilot
- interpretation:0007-t126-sbs1-lrr-bias-per-study
parent: ''
group: hypothesis-spine
artifacts: []
findings: []
created: '2026-04-28'
completed: null
---

Run /science:add-hypothesis to formalize a candidate sub-hypothesis (proposed id h07) absorbing q009, t123, and t126. Working frame: 'a well-powered WGS-based topographic or signature-based diagnostic can directly flag studies with excess normal-tissue contamination, independently of tumor-purity proxies'. Distinguished from h01 because h01 targets correction whereas h07 targets *detection* — a per-study quality flag with a pre-registered threshold (e.g. SBS1 LRR-bias delta, or SBS1 fraction excess vs the matched-cohort pool). Promotion gate: any one WGS cohort added (Hartwig HMF or PCAWG follow-on). Acceptance: specs/hypotheses/h07-*.md with phase: candidate, status: proposed, source_refs to Tomkova 2018 / Sherman 2024, and the three promotion criteria stated.
