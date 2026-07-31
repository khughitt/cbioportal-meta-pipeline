---
id: t127
project: ''
title: 'First q008 quantitative pass: unmatched-normal contamination magnitude using
  t111 normal_tissue_spectra'
type: ''
aspects:
- computational-analysis
priority: P3
status: blocked
blocked_by:
- task:t166
related:
- question:0008-signature-decomposition-tissue-background-subtraction
- task:t111
- meta:0007-next-steps-and-gap-analysis-2026-04-24
parent: ''
group: meta-analysis
artifacts: []
findings: []
created: '2026-04-24'
completed: null
---

Produce a first numeric estimate of normal-tissue SBS1/SBS5 contamination
magnitude in unmatched-normal cBioPortal-style cohorts, using the Li2021
reference spectra landed by t111 + the existing t109/t110 SigProfiler
assignment surface. Closes the "built-but-unexploited" gap from
meta:0007-next-steps-and-gap-analysis-2026-04-24 gap 2 for question:0008.

Status: deferred 2026-04-28 — workable but materially weaker than originally
scoped. Plan + cohort survey landed; revival is cheap when a better
unmatched-WES cohort becomes available (Hartwig HMF when t166 unblocks is
the obvious candidate).

What landed
-----------
- doc/plans/2026-04-28-t127-q008-quantitative-pass-plan.md (revised plan,
  reuses run_restricted_sigprofiler_assignment.py; threshold pre-registration;
  no-go rules; 9-finding code-review pass).
- code/config/config-t127.yml (study list + signature config).
- tcga_mc3 ingested (commit 16d1a12): 9,104 samples / 32 TCGA project codes
  / GRCh37 in results/q008-quantitative-pass-2026-04-28/studies/tcga_mc3/.
- Cohort survey across 196 pipeline studies for matched/unmatched status.

Why deferred
------------
Original plan paired tcga_mc3 (matched WES) with msk_impact_2017 (assumed
unmatched panel). Survey discovered msk_impact_2017's public release is 98%
matched (MATCHED_STATUS column: 10,702 matched / 242 unmatched / 1 NaN).
Largest unmatched cancer-type stratum is NSCLC at n=24 — below the n=50
floor required for the planned per-cancer-type FDR table.

Best alternative cohort found in survey:
- sarcoma_msk_2022 (n=7,494, 100% unmatched, MSK-IMPACT panel) — pairs with
  MC3 SARC (n=236) for a single-cancer-type matched-vs-unmatched contrast.
  But: Li2021 covers 9 GI/respiratory tissues only — no soft-tissue / bone /
  sarcoma reference, so the subtraction arm of the original plan cannot run
  on this contrast.

GENIE (229,453 samples) does not publish MATCHED_STATUS; per-assay matching
policy curation would be required, out of scope for a pilot.

Revised pilot design (recorded for revival)
-------------------------------------------
Tripartite descriptive design that fits the available cohorts:

1. Primary Δ — sarcoma matched-vs-unmatched. MC3 SARC (n=236 matched WES)
   vs sarcoma_msk_2022 Soft Tissue Sarcoma (n=5,264 unmatched panel) on
   per-sample SBS1+SBS5 fraction. Single cancer type ⇒ no FDR table; verdict
   is descriptive. Confounders: WES vs panel callable territory, TCGA vs
   MSK caller pipeline.

2. Secondary Δ — within-MSK-IMPACT. matched (n=10,702) vs unmatched (n=242)
   pooled across cancer types. Strongest causal-attribution design (same
   assay/caller/cohort) but small unmatched n limits Δ precision.

3. Subtraction-model calibration on matched data. Apply Li2021 c-sweep to
   MC3 GI cancer types (LIHC, COAD/READ, ESCA, STAD, PAAD; n=940 total).
   Answers: how much SBS1+SBS5 mass does the subtraction remove from a
   known-matched cohort? Large removal ⇒ over-aggressive; small removal ⇒
   conservative.

Material weaknesses vs original plan: no per-cancer-type FDR table, no
Δ(c) gap-closing test, primary contrast confounds normal-status with
WES-vs-panel and caller pipeline.

What would unblock the strong design
------------------------------------
A multi-cancer-type unmatched-normal WGS or WES cohort, ideally with a
within-cohort matched comparator. Hartwig HMF (task t166, currently gated
on a 3-6 month DUA) is the leading candidate: WGS, mixed matched/unmatched,
35+ cancer types. When t166 lands, the t127 plan structure runs on that
cohort with minimal modification — the subtraction arm becomes feasible
(WGS removes the t126 panel-sparsity blocker on q009 too), and the
per-cancer-type FDR table comes back.

Cheaper revival paths if a better cohort surfaces unexpectedly:
- Curate a tumor-only subset of GENIE by joining seq_assay_id against the
  AACR Project GENIE matching-policy table (per-contributor metadata).
- Search for newer per-tissue Li2021-equivalent normal references (Moore
  2022 pan-tissue WGS; Xu2025 GTEx coding spectra at t111 follow-up).

To revive: re-read this description, the plan, and config-t127.yml; pick
up at Task 1 of the plan with the new cohort substituted into the
feasibility table.
