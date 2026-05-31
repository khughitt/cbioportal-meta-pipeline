---
id: question:q020-minimum-sample-size-and-caller-provenance-for
type: question
title: What minimum per-cancer-type sample size and variant-caller provenance does
  the cross-study cohort need for reliable signature extraction/fitting?
status: active
ontology_terms: []
datasets: []
source_refs:
- paper:Jiang2025
- paper:Islam2022
- paper:Medo2024
- paper:DiazGay2023
related:
- hypothesis:h08-agnostic-covariate-association-recovers-known-signature-aetiologies-and
- method:h08-agnostic-association-model
- topic:signature-extraction-fitting-methods
- question:q018-can-mutational-signature-decomposition-be-added-downstream-of-the-cross
- question:q019-does-de-novo-extraction-on-the-aggregated-cohort-surface-factors-not-in
created: '2026-05-31'
updated: '2026-05-31'
---

# What minimum per-cancer-type sample size and variant-caller provenance does the cross-study cohort need for reliable signature extraction/fitting?

## Summary

The cross-study aggregation mixes studies of widely varying size and variant-calling provenance. Before per-sample signature exposures `H` can drive the h08 covariate scan, we need a defensible per-cancer-type sample-size floor for de novo extraction and a rule for handling single-caller (non-consensus) studies that are known to inject artefactual signatures.

## Why It Matters

- Decision affected: which studies/strata are admissible into the h08 signature-decomposition rule, and whether de novo extraction is attempted at all vs. refit-only.
- Risk if unanswered: spurious de novo signatures from single-caller studies (`paper:Jiang2025`) and unstable exposures from undersized strata would propagate into the covariate scan as false positives, defeating the positive-control logic.

## Current Evidence

- `paper:Jiang2025` shows consensus calling (>=2 callers) is essential for artefact-free de novo SBS extraction; single callers inject reproducible spurious signatures.
- `paper:Islam2022` (SigProfilerExtractor) and `paper:Medo2024` (tool comparison) bound the per-sample mutation counts and cohort sizes at which extraction/fitting is reliable; flat signatures (SBS3/5/40) are the least separable.
- `paper:DiazGay2023` (SigProfilerAssignment) is the refit fallback when de novo is underpowered.
- The project already ingests the consensus MC3 MAF (`tcga_mc3`) as a clean substrate; heterogeneous per-study cBioPortal TCGA MAFs are the contrast case.

## Thoughts

- Best current interpretation: refit-only against a restricted COSMIC reference for panel/small studies; reserve de novo extraction for consensus-called, adequately-sized strata (MC3-grade).
- Major uncertainty: the exact per-cancer-type n floor and whether a per-study caller-consensus flag can be reconstructed from cBioPortal metadata at all.

## Connections to Project

- Related hypotheses: `hypothesis:h08-...` (signature exposures are its outcome variable).
- Required data or analyses: per-study caller provenance audit; per-cancer-type sample-size census; extraction-vs-refit decision rule.
- Priority level: P2 (gates the feasibility confirmation in `question:q018`).

## Related

- Topic notes: `topic:signature-extraction-fitting-methods`
- Article notes: `paper:Jiang2025`, `paper:Islam2022`, `paper:Medo2024`, `paper:DiazGay2023`, `paper:Pancotti2023`
- Methods/Datasets: `method:h08-agnostic-association-model`; `question:q018`, `question:q019`
