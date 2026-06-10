---
type: topic
title: 'Normal-tissue somatic-mutation atlas: cross-tissue, cross-age background as
  positive knowledge'
status: active
created: '2026-04-27'
updated: '2026-04-28'
id: topic:normal-tissue-mutation-atlas
ontology_terms:
- somatic mutation
- normal tissue
- clonal hematopoiesis
- clonal expansion
- aging
- cross-species mutation rate
datasets:
- dataset:li2021-normal-wgs
- dataset:gtex
source_refs:
- paper:Martincorena2018
- paper:LeeSix2018
- paper:Li2021
- paper:Yaacov2023
- paper:Yoshida2026
related:
- hypothesis:0005-healthy-somatic-background-atlas
- hypothesis:0001-non-tumor-signal-contamination
- question:0007-cross-tissue-somatic-mutation-rate-variation-as-null-model
- task:t150
- task:t151
- topic:clonal-hematopoiesis-contamination
- topic:signature-decomposition-unmatched-normal
---

# Normal-tissue somatic-mutation atlas

## Summary

The cancer-genomics field has invested heavily in cataloging mutations in tumors and
relatively little in characterizing the somatic-mutation **background** in apparently-
healthy individuals across tissues and ages. This topic frames the broader research
direction — that healthy somatic-mutation backgrounds are themselves a substantively
under-specified object — and the case that consolidating it into a unified atlas would be
both novel and project-relevant. From an evolutionary perspective, somatic-driven clonal
expansions appear to be the rule, not the exception, in the adult population: the canonical
"cancer" phenotype may be the small-N tail of a broader continuum of clonal somatic genomic
instability, with most clonal expansions producing milder or sub-clinical consequences.

## Key Concepts

- **Somatic mutation rate per cell per year.** Per-tissue rate, derivable from cell-by-cell
  phylogenies (Lee-Six 2018, 2019). Varies by tissue; scales roughly with stem-cell
  turnover (Tomasetti & Vogelstein 2015 framework).
- **Clonal expansion.** A somatic mutation in a stem cell that confers replicative
  advantage produces a clonal patch in the tissue. Detectable in normal tissue WGS as
  elevated VAF for the clone-marker mutation.
- **Driver-mutation-positive clones.** Clones carrying mutations in canonical driver genes
  (TP53, NOTCH1, KRAS, APC, …) detected in apparently-healthy tissue. Clinically silent in
  most cases but molecularly equivalent to the early mutations of cancer.
- **Clonal hematopoiesis (CH).** The blood-specific name for the same phenomenon: clonal
  expansion of hematopoietic stem cells carrying mutations in DNMT3A, TET2, ASXL1, JAK2,
  TP53, PPM1D, … with prevalence of ~10% by age 70 (Jaiswal 2014, Genovese 2014).
- **Cross-species mutation rate scaling.** Cagan 2022 showed mammalian per-cell-per-year
  somatic mutation rate scales inversely with lifespan; informs which between-tissue
  variation is mechanistically grounded.

## Current State of Knowledge

**Well-established:**
- Multiple tissues carry driver-mutation-positive clones at high prevalence in
  apparently-healthy adults (Martincorena 2015 skin; 2018 esophagus; Yokoyama 2019
  esophagus; Lee-Six 2018 colon; Moore 2020 endometrium; Brunner 2019 liver; Yoshida 2020
  lung).
- CH prevalence rises sharply with age, exceeding 10% by age 70 in blood (Jaiswal 2014,
  Genovese 2014, Coombs 2017, Bolton 2020).
- Per-cell-per-year somatic mutation rate accumulates roughly linearly through life
  (Lee-Six 2019); inter-tissue rate variation spans ~1–2 orders of magnitude across the
  tissues that have been measured.
- Driver-clone landscape in normal tissue partially overlaps the cancer driver landscape —
  with characteristic exceptions (NOTCH1 dominates normal esophagus more than EAC; TP53
  is rare in normal but common in cancer).

**Emerging / less established:**
- A unified cross-tissue, cross-age normal somatic-mutation atlas does not exist in
  consolidated form. Each published cohort is one tissue; harmonization is the unsolved
  problem.
- Quantitative comparison between population-level driver-clone prevalence and
  population-level cancer incidence — i.e., "is your tissue more clonally diverse than
  the cancer rate would suggest?" — is mostly anecdotal.
- The functional consequences of sub-clinical clonal expansions (immune dysfunction,
  metabolic cost, senescent-cell load) are largely speculative outside CH.

## Controversies & Open Questions

- **Are most clonal expansions consequential?** CH is associated with cardiovascular risk
  and AML transition, but the quantitative attribution is debated. Other tissue clonal
  expansions (esophageal NOTCH1, skin sun-damage drivers) have weaker outcome links.
- **What's the right denominator for "more common than cancer"?** Comparing biopsy-level
  clonal coverage to population-level cancer incidence is not apples-to-apples; the
  right framing is per-individual lifetime risk of a clinically-relevant clone vs lifetime
  cancer risk for the same tissue.
- **How much of the "normal" mutation rate is exposure-driven vs intrinsic?** UV / smoking
  / alcohol modify rates substantially in their target tissues; the intrinsic baseline is
  observable only in unexposed tissues (heart muscle, neurons).
- **Identifiability of "true normal" vs "subclinical pre-malignant".** A 70-year-old with a
  TP53-positive clone in liver tissue is not unambiguously "healthy"; the atlas must
  acknowledge the continuum, not reify a binary.

## Relevance to This Project

- **Direct support for `hypothesis:0005`** (cross-tissue normal background atlas + the
  null-substitution claim).
- **Sibling support for `hypothesis:0001`** (within-sample non-tumor signal contamination
  — the *atlas* is the calibrated population-level form of the *correction* h01 applies
  per sample).
- **Question:** `q007` (Li 2021 as null model) is the precursor; this topic generalizes
  q007 to a meta-analytic cross-tissue null.
- **Big-version research direction:** "cancer is the small-N tail of a continuum of
  clonal somatic genomic instability." If the atlas confirms driver-clone prevalence
  exceeding cancer rates in multiple tissues, the project-level framing of cBioPortal
  contamination work shifts from "fix the noise" to "the noise is a measurement of a
  separate biology that the field has under-counted."
- **Out-of-scope for direct project work but relevant to interpretation:** the clinical
  and epidemiological consequences of widespread sub-clinical clonal expansion. Does not
  require new analyses; informs how the project frames its cancer-genomics findings.

## Key References

- **Martincorena 2018** *Science* 362:911 — NOTCH1 in normal esophagus; the canonical
  "normal tissue is full of driver-positive clones" paper.
- **Lee-Six 2019** *Nature* 561:473 — colon-crypt phylogenies; per-cell-per-year mutation
  rate.
- **Li 2021** — multi-tissue body-map of somatic mutation rates; the closest existing
  cross-tissue reference in the project library.
- **Cagan 2022** *Nature* 604:517 — cross-species mutation rate scaling with lifespan.
- **Jaiswal 2014** *NEJM* 371:2488 — clonal hematopoiesis at population scale; the
  blood-specific anchor.

## Datasets referenced

Studies/resources discussed in this topic (not yet first-class `dataset:` entities):

- "Martincorena 2015 (skin)"
- "Martincorena 2018 (esophagus)"
- "Yokoyama 2019 (esophagus)"
- "Lee-Six 2018 (colon)"
- "Lee-Six 2019 (blood, hematopoietic phylogeny)"
- "Moore 2020 (endometrium)"
- "Brunner 2019 (liver)"
- "Yoshida 2020 (lung)"
- "Cagan 2022 (cross-species mutation rate scaling)"
- "Park 2024 (somatic mutation as biological clocks)"
- "HMF / Hartwig (potential normal-cohort component)"
