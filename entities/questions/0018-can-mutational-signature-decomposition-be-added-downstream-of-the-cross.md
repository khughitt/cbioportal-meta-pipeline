---
type: question
title: Can mutational-signature decomposition be added downstream of the cross-study
  aggregation, and is panel data adequate for reliable signature inference?
status: resolved
created: '2026-05-30'
updated: '2026-05-31'
id: question:0018-can-mutational-signature-decomposition-be-added-downstream-of-the-cross
ontology_terms:
- mutational signatures
- somatic mutation
- tumor mutational burden
datasets:
- TCGA MC3 (tcga_mc3)
- cBioPortal (~300 studies)
source_refs:
- paper:Islam2022
- paper:Medo2024
- paper:Jiang2025a
- paper:DiazGay2023
related:
- topic:mutational-signatures
- topic:signature-extraction-fitting-methods
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
- method:h08-agnostic-association-model
- pre-registration:0003-h08-positive-control-agnostic-association-must-recover-known-signature
- question:0020-minimum-sample-size-and-caller-provenance-for
- task:t178
- task:t179
- task:t197
- discussion:0004-common-mutational-signatures-known-vs-learned-immune-causes-and
---
# Can mutational-signature decomposition be added downstream of the cross-study aggregation, and is panel data adequate for reliable signature inference?

## Summary

**Resolved (two parts).**
Signature decomposition *can* be added downstream of the cross-study aggregation, and it already is: `code/scripts/run_restricted_sigprofiler_assignment.py` performs restricted COSMIC SBS *refit/assignment* (not de novo extraction) on per-study spectra, hardened against reference and provenance artefacts by `task:t178` / `task:t179`.
Panel data is **not** adequate for reliable *per-sample* signature inference.
The resolving rule is therefore: **per-sample exposures `H` are admissible only on WES/WGS substrates (`tcga_mc3`); panel and small studies enter cohort-pooled and refit-only, never per-sample.**
This is the activation gate that `pre-registration:0003-h08-positive-control-agnostic-association-must-recover-known-signature` conditions on, and the substrate boundary that `method:h08-agnostic-association-model` already assumes.

## Why It Matters

- **Decision affected:** which studies/strata may contribute per-sample `H` to the h08 covariate scan, and whether de novo extraction is attempted at all (it is not — the scan is refit-based, with de novo only *flagged* as warranted per `task:t179`).
- **Risk if unanswered:** assigning a 96-channel COSMIC spectrum from a handful of panel mutations yields unstable, noise-dominated exposures that would enter the H08a positive-control scan as false signal, defeating the recovery logic before any covariate is tested.

## Current Evidence

- **Empirical panel-vs-WES sparsity (decisive).** In the existing brca-2026-04-22 pilot refit, MSK-IMPACT panel samples carried a **median of 3 SBS per sample** (IQR 2–5, max 41), against a **median of 52** for the WES substrate (`tcga_mc3`) — a >15× gap, with panels falling far below any usable per-sample floor.
- **Literature floors.** SigProfilerExtractor [@Islam2022] and the tool comparison of [@Medo2024] bound the per-sample counts and cohort sizes at which extraction/fitting is reliable; flat signatures (SBS3/5/40) are the least separable at low counts. `task:t179` operationalises this as a per-sample SBS-count floor (~383 WES, ~100 matched-normal) — panel medians near 3 sit two orders of magnitude below it.
- **Caller provenance.** Consensus calling (≥2 callers) is essential for artefact-free de novo extraction; single callers inject reproducible spurious signatures [@Jiang2025]. `tcga_mc3` is a 7-caller consensus MAF — the clean substrate — whereas heterogeneous per-study cBioPortal MAFs are not (`task:t178` carries a per-study `caller_consensus` flag, default *unknown*).
- **Refit is the right instrument here.** SigProfilerAssignment [@DiazGay2023] is the assignment/refit fallback when de novo is underpowered; the h08 scan uses refit against a pinned COSMIC v3.4 reference (`task:t178`), not de novo, so it does not require the larger cohorts de novo extraction would.

## Thoughts

- **Best current interpretation:** feasibility is settled in the affirmative for the *WES/WGS refit* path and in the negative for the *panel per-sample* path. The H08a scan runs on `tcga_mc3` per-sample exposures only; the EHR-covariate / panel track (GENIE BPC, MSK-CHORD) — if pursued — must use cohort-pooled signatures under a separate registration.
- **Major remaining uncertainty (deferred, not blocking):** the exact per-cancer-type sample-size floor for any *de novo* extraction, and how completely a per-study caller-consensus flag can be reconstructed from cBioPortal metadata. Both belong to `question:0020` and do not gate the refit-based H08a scan, which sidesteps de novo entirely.

## Connections to Project

- Related hypotheses: `hypothesis:0007` (per-sample `H` is its outcome variable); this verdict is one of the two activation gates (`task:t177` is the other) named by `pre-registration:0003-h08-positive-control-agnostic-association-must-recover-known-signature`.
- Required data or analyses: the full-MC3 per-sample refit across the seven h08 arm strata (`task:t197`) executes under this rule.
- Priority level: resolved; the open de novo / caller-census tail lives in `question:0020`.

## Related

- Topic notes: `topic:mutational-signatures`, `topic:signature-extraction-fitting-methods`
- Article notes: [@Islam2022], [@Medo2024], [@Jiang2025], [@DiazGay2023]
- Methods/Datasets: `method:h08-agnostic-association-model`; analysis plan `doc/plans/2026-05-31-h08-positive-control-scan-analysis-plan.md`; `tcga_mc3`
