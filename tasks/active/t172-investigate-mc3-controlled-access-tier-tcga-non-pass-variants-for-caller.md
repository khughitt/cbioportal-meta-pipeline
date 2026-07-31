---
id: t172
project: ''
title: Investigate MC3 controlled-access tier (TCGA non-PASS variants) for caller-confidence
  stratification
type: ''
aspects:
- computational-analysis
priority: P3
status: blocked
blocked_by: []
related:
- hypothesis:0001-non-tumor-signal-contamination
- question:0008-signature-decomposition-tissue-background-subtraction
- task:t127
parent: ''
group: dataset-acquisition
artifacts: []
findings: []
created: '2026-04-28'
completed: null
---

The current ingest uses MC3 v0.2.8 PUBLIC (PASS-only). The controlled-access MC3 tier exposes the non-PASS variants and per-caller filter flags. Motivation specific to h01: when the q008 quantitative contamination-magnitude pass (t127) reports 'this gene shows X% excess SBS1 in unmatched cohorts', a likely critique is 'maybe that excess is low-confidence variants slipping through unmatched-normal filtering'. Having access to per-caller flags lets us stratify the contamination signal by caller-confidence and report which contamination claims are robust to PASS-only restriction. Lower priority because P3 — the public PASS tier should be sufficient for the first contamination magnitude estimate. Access: dbGaP phs000178 (TCGA controlled access), institutional DAR required. Pipeline integration scope: minimal — same MC3 ingest path with an extra column carrying the per-caller filter set. Acceptance: a feasibility memo at doc/feasibility/2026-XX-mc3-controlled-tier.md with go/no-go recommendation. Defer execution until t127 and t146 have produced public-tier results that justify the access friction.
