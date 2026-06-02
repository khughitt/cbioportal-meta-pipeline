---
id: "interpretation:2026-05-31-t197-mc3-7strata-sbs-refit"
type: "interpretation"
status: "active"
source_refs:
  - "task:t197"
title: "t197 full-MC3 per-sample SBS refit across the 7 h08 arm strata (COSMIC v3.4, t178/t179-hardened)"
date: "2026-05-31"
related:
  - "task:t197"
  - "hypothesis:h08-agnostic-covariate-association-recovers-known-signature-aetiologies-and"
  - "question:q018-can-mutational-signature-decomposition-be-added-downstream-of-the-cross"
---
# t197 — full-MC3 per-sample SBS refit across the 7 h08 arm strata

Date: 2026-05-31

## Question

Can the t178/t179-hardened restricted-SigProfiler refit produce per-sample SBS exposures `H`
across all seven `pre-registration:h08-positive-control` arm strata (SKCM, LUAD, LUSC, BLCA,
BRCA, CESC, HNSC) on the MC3 WES substrate, reproducing the pre-registered §1b sample counts
and recovering the textbook positive-control signatures as a wiring check?

This is check 2 of `plan:2026-05-31-h08-positive-control-scan` and a near-term unblocker for the
H08a association core (`task:t199`). The verifiable record lives here because `results/` is
gitignored.

## Inputs and Provenance

- Substrate: `tcga_mc3` only (MC3 v0.2.8 PUBLIC PASS MAF, Ellrott 2018 — WES, 7-caller
  consensus, matched-normal by construction). Panels are excluded from per-sample `H` per the
  `question:q018` feasibility verdict.
- Config: `code/config/config-signature-h08-arms.yml` (COSMIC **v3.4** pinned per the locked
  pre-reg; 5 restriction families `melanoma / lung / bladder / breast / head_neck` covering the
  7 arm strata; matched-normal count floor 100; de-novo threshold n≥200).
- Rule: `run_restricted_sigprofiler_assignment_per_sample` (SigProfilerAssignment 1.1.3,
  SigProfilerMatrixGenerator GRCh37). The validated MC3 ingestion intermediates
  (`mut/table/mut.feather`, `metadata/samples.feather`) were reused byte-identically from the
  `signature-brca-2026-04-22` pilot run — deterministic products of `process_mc3` — so only the
  refit step was executed.
- Outputs (run dir `results/signature-h08-arms-2026-05-31/studies/tcga_mc3/mut/signatures/`,
  gitignored): `restricted_assignment_per_sample.feather` (md5 prefix `8f3c31a42c6e4b44`; 34,163
  rows, 3,457 arm samples × restricted signatures + 80-sample UVM rider — see below), plus the
  `*.signature_audit.feather` (t178) and `*.denovo_decision.feather` (t179) sidecars.

## Pre-flight QA (data-genomics-somatic-mutation-qa)

PASS-bearing sample counts reproduce the pre-reg §1b independently-verified lower bound
**exactly** for all seven strata (one MC3 `Tumor_Sample_Barcode` per case; GRCh37; PASS-only):

| Stratum | Computed | Pre-reg §1b | Median SBS/sample | `passes_count_floor` (≥100) |
|---|---|---|---|---|
| SKCM | 466 | 466 | 474 | 0.839 |
| LUAD | 513 | 513 | 251 | 0.774 |
| LUSC | 480 | 480 | 305 | 0.962 |
| BLCA | 411 | 411 | 241 | 0.844 |
| BRCA | 791 | 791 | 52  | 0.225 |
| CESC | 289 | 289 | 151 | 0.671 |
| HNSC | 507 | 507 | 142 | 0.702 |

All seven match. Across the seven arms, 67.3% of samples clear the matched-normal count floor of
100 SBS; per-sample reconstruction quality is sound (cosine similarity median 0.909, 53.8% of
samples ≥0.90, 5th-percentile 0.661 — the low tail tracks the low-count samples, as expected).

## Positive-control wiring sanity

The known aetiology signatures dominate their tissues exactly as expected (mean within-sample
exposure fraction), confirming the refit is correctly wired before any covariate is tested:

- **Arm A — SKCM**: SBS7a 0.48 + SBS7b 0.35 ≈ **0.83** (UV).
- **Arm B — lung**: SBS4 (smoking) 0.36 LUAD / 0.28 LUSC.
- **Arm C — APOBEC SBS2+SBS13**: BLCA 0.57, CESC 0.54, HNSC 0.26, BRCA 0.21.

The lookup restriction holds: the melanoma family carries no SBS4; lung/head_neck carry SBS4;
the APOBEC families carry SBS2/13.

## Sidecars

- **t178 signature-presence audit**: 122 rows, **every** requested + positive-control signature
  present in the loaded COSMIC v3.4 reference — none absorbed by nearest neighbours.
- **t179 de-novo-vs-refit decision**: all seven arm strata recommend `de_novo` (n≥200 AND
  caller-consensus True); UVM (n=80) recommends `refit`. The decision is **recorded only** — the
  executed `H` is refit/assignment against the pinned reference, the conservative instrument the
  pre-reg locked. No de-novo extractor was run.

## Caveats carried forward

- **UVM rider.** The `melanoma` lookup family also pulls in 80 UVM samples (median 15 SBS/sample,
  1.2% pass the count floor). UVM is **not** one of the seven arms; `task:t199` reads only the
  seven named strata, so these rows are inert. They are retained, not dropped (loud missingness).
- **BRCA sub-floor fraction.** Only 22.5% of BRCA samples clear the matched-normal floor of 100
  (median 52 SBS/sample — consistent with the WES median cited in `question:q018`). Samples are
  flagged (`passes_count_floor=False`), never silently dropped. The H08a association layer
  (t199) must read the count-floor flag and the pre-reg active-signature ≥5%-of-stratum rule when
  it fills the §1b post-join completeness table; the gate is not read until that table is filled.

## Implications

`task:t197` (analysis-plan check 2) is complete: the per-sample `H` substrate for all seven arm
strata exists, validated, with provenance and trust columns intact. Combined with the resolved
`question:q018` (check 1), both near-term unblockers for the H08a scan are closed. Remaining:
`task:t198` (PanCanAtlas RNA-seq + NMF expression modules) and `task:t199` (the within-tissue
covariate↔H association core, which consumes this table).
