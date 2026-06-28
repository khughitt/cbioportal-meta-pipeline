---
type: question
title: Can a tissue-of-origin classifier (CUPLR or cosine-similarity heuristic) flag
  cBioPortal study samples whose signature profiles are abnormally consistent with
  normal-tissue background?
status: active
created: '2026-04-18'
updated: '2026-06-28'
id: question:0010-cuplr-style-tof-classifier-for-suspect-normal-samples
ontology_terms:
- tissue-of-origin
- mutational signatures
- tumor purity
- cancer of unknown primary
- cosine similarity
datasets:
- cBioPortal (~300 studies)
- PCAWG
source_refs:
- paper:Nguyen2022CUPLR
- paper:Alexandrov2020
- paper:Li2021
related:
- topic:signature-decomposition-unmatched-normal
- paper:Li2021
- paper:Xu2025
- question:0008-signature-decomposition-tissue-background-subtraction
---

# Can a tissue-of-origin classifier (CUPLR or cosine-similarity heuristic) flag cBioPortal study samples whose signature profiles are abnormally consistent with normal-tissue background?

## Summary

Tissue-of-origin (TOO) classifiers trained to distinguish cancer types from each other (e.g., CUPLR) use mutational signatures, regional mutation density, and driver mutation presence as features. These same features distinguish cancer profiles from normal-tissue profiles. The question is whether an existing TOO classifier — or a simpler cosine-similarity heuristic based on published normal-tissue reference spectra — can flag cBioPortal study samples (or entire studies) whose 96-trinucleotide mutation spectra are unusually similar to normal-tissue background, suggesting excess normal-cell admixture.

## Why It Matters

- Flagging "normal-like" studies enables stratified analysis: comparisons between studies can be conditioned on contamination risk rather than treating all studies as equivalent.
- A practical screen does not require tumor purity estimation, which is often unavailable or unreliable for panel-sequenced studies.
- Even a coarse binary flag (high contamination risk vs low) would allow adding a covariate to downstream frequency analyses.

## Current Evidence

- CUPLR (Nguyen et al., Nature Communications 2022): classifies 35 cancer subtypes with ~90% precision/recall from WGS features. Key features: SBS signatures, RMD (regional mutation density, correlated with chromatin/RT), and structural variant classes. Published for CUP diagnosis but could be repurposed.
- CUPLR requires WGS — not applicable directly to panel/WES-based cBioPortal studies. The RMD feature alone requires coverage across the entire genome at 1 Mb resolution.
- Cosine-similarity heuristic: compute the cosine similarity between a sample's (or study's aggregate) 96-trinucleotide profile and: (a) the known cancer-type PCAWG reference spectrum; (b) the published normal-tissue spectrum for the corresponding organ (from Li 2021 or Xu 2025). Studies with similarity(b) > similarity(a) are candidates for flagging.
- Per-tissue reference spectra for normal tissue: available from Li 2021 (7 signatures extracted across 9 organs) and Xu 2025 (96-context spectra for 46 GTEx tissues). These are the best available references for the heuristic.

## Thoughts

- The cosine similarity approach is feasible immediately using the pipeline's existing per-study 96-trinucleotide profile outputs, if those are available, or can be computed from per-study mutation calls.
- The key challenge is defining "normal" spectra that are appropriate for comparison against cancer panel data: normal tissues are profiled by LCM-WES or WGS (Li 2021, Xu 2025), whereas cBioPortal studies use cancer-panel targeted sequencing. The trinucleotide context coverage differs between these.
- A computationally tractable first step: restrict the cosine similarity calculation to the subset of the 96 trinucleotide contexts that are represented in both the panel target bed and the normal-tissue reference data.
- An alternative heuristic that avoids the reference-spectrum coverage mismatch: compute the per-study SBS1+SBS5+SBS18 fraction of total mutations (using SigProfilerAssignment outputs). Studies where this combined aging-clock fraction exceeds a tissue-type-specific threshold (derived from PCAWG per-cancer reference) would be flagged as potentially contaminated.

## Connections to Project

- Related hypotheses: none filed.
- Required data or analyses:
  1. Extract per-tissue 96-trinucleotide reference spectra from Li 2021 and/or Xu 2025 supplemental tables.
  2. Compute per-study aggregate 96-trinucleotide profiles from pipeline mutation call files.
  3. Compute cosine similarity to (a) PCAWG cancer-type reference and (b) normal-tissue reference; flag studies where similarity(b) >= similarity(a).
  4. Validate against known matched-normal (clean) vs tumor-only (potentially contaminated) study pairs for the same cancer type.
- Priority level: medium — feasibility depends on whether per-tissue normal reference spectra can be extracted in accessible form from Li 2021 / Xu 2025. If spectra are in supplemental tables, this is a 2–3 day engineering task. If they require re-processing raw data, it is a multi-week project.

## Related

- Topic notes: `topic:signature-decomposition-unmatched-normal`
- Article notes: `paper:Li2021`, `paper:Xu2025`
- Related questions: `question:0008-signature-decomposition-tissue-background-subtraction`
  (contamination magnitude), `question:0009` (SBS1 LRR flag)
- Methods/Datasets: CUPLR (GitHub: UMCUGenetics/cuplr); SigProfilerAssignment; Li 2021 EGA data; Xu 2025 dbGaP data
