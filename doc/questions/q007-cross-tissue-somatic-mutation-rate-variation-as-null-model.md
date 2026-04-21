---
id: "question:q007-cross-tissue-somatic-mutation-rate-variation-as-null-model"
type: "question"
title: "Can the Li 2021 body-map tissue-specific normal mutation rates serve as a null model for per-tissue background in our pipeline outputs?"
status: "active"
ontology_terms: []
datasets:
  - "EGA:EGAD00001007859"
source_refs:
  - "cite:Li2021"
related:
  - "paper:Li2021"
  - "paper:Yoshida2026"
  - "topic:mutation-rate-normalization"
  - "topic:pan-cancer-mutation-landscape"
  - "question:q001-normal-epithelial-clone-contamination-in-esophageal-studies"
created: "2026-04-18"
updated: "2026-04-18"
---

# Can the Li 2021 body-map tissue-specific normal mutation rates serve as a null model for per-tissue background in our pipeline outputs?

## Summary

Li et al. 2021 (Nature) established that somatic mutation accumulation in morphologically normal tissue varies substantially by organ type, with per-cell mutation burden highest in liver and lowest in pancreas, and that clonal driver gene composition is also organ-specific. If these per-tissue normal-tissue mutation rates could be extracted from the EGA dataset and expressed as exonic mutation-per-Mb estimates per tissue, they could serve as tissue-matched null models for interpreting whether a gene's apparent mutation frequency in our cross-cancer cBioPortal outputs exceeds neutral-background expectation. This is conceptually analogous to the dN/dS framework (Martincorena 2017) but parameterized from empirical normal-tissue data rather than assuming a uniform mutation rate scaled by coding sequence length.

## Why It Matters

- Our pipeline currently reports cross-study mutation frequency ratios without adjusting for baseline per-tissue mutation rates; tissues with high background (e.g., liver, colon/rectum) may inflate apparent driver gene frequencies relative to tissues with low background (e.g., pancreas).
- The body-map data provide the empirical per-tissue background against which to interpret whether observed cancer mutation frequencies represent enrichment above the normal-tissue floor or are merely elevated because the tissue has a high baseline mutation rate.
- If SBS1/SBS5 dominate all normal tissues but with different relative magnitudes per tissue, the effective per-gene background rate differs by tissue even for genes with no positive selection — a source of systematic variation in our frequency tables.

## Current Evidence

- Li 2021: liver highest, pancreas lowest mutation burden among 9 organs; macroscopic clonal drivers in esophagus/cardia; microscopic constrained clones in colon/rectum/duodenum.
- Yoshida 2026 review (Table 1): per-tissue SBSs/year confirmed for a broader set of tissues — colon ~43.6/year, esophagus ~41.5/year, blood ~14–17/year; these rates are from different studies and methods so cross-tissue comparison is approximate.
- Martincorena 2017 (Cell): dN/dS ≈ 1 for most genes in normal tissue across multiple organs, supporting near-neutral evolution of the vast majority of somatic mutations — the exception being specific driver hotspots.
- No published adaptation of the Li 2021 body-map data as a quantitative null model for cancer study frequency analysis exists in the literature (as of 2026-04-18).

## Thoughts

- The conceptual approach is sound but requires solving several calibration issues: (a) the Li 2021 data uses mini-bulk WES on ~600-cell microbiopsy units, not single-cell WGS, so per-cell mutation rates are estimated from VAF distributions and require clone-size correction; (b) the 5-donor sample size is very small — tissue-level rates have high uncertainty; (c) the reference cohort is healthy donors (presumably middle-aged Chinese adults), and direct applicability to cancer-affected tissues is unclear.
- A simpler proxy for current pipeline use: use per-tissue dN/dS models from Martincorena 2017 / IntOGen gene-level background to flag genes with apparent frequency enrichment above the neutral-evolution expectation. This is methodologically more mature than extracting absolute rates from the Li 2021 data.
- The EGA raw data (EGAD00001007859) could in principle be re-analyzed to derive exonic mutation spectra per tissue, but this requires EGA data access approval and substantial compute — a multi-week project if pursued.

## Connections to Project

- Related hypotheses: none yet filed; this question could motivate a hypothesis about tissue-specific background rate normalization as a pipeline enhancement.
- Required data or analyses: (1) per-tissue mutation-per-Mb estimates from the Li 2021 supplemental tables (if accessible in the published paper); (2) comparison of apparent mutation frequency ranks in our pipeline across high-background vs. low-background tissues; (3) optionally, EGA data access for re-analysis.
- Priority level: low — the pipeline currently addresses a different normalization (per-sample ratio by total mutations), and adding a per-tissue background model is a substantial methodological change. Medium if a future pipeline version adds absolute mutation rate outputs.

## Related

- Topic notes: `topic:mutation-rate-normalization`, `topic:pan-cancer-mutation-landscape`
- Article notes: `paper:Li2021`, `paper:Yoshida2026`, `paper:Martincorena2017`
- Related question: `question:q001` (normal-tissue clone contamination in esophageal studies)
- Methods/Datasets: EGA:EGAD00001007859 (raw WGS+WES from Li 2021); dN/dS framework from Martincorena 2017
