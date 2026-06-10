---
id: "paper:Gourmet2024"
overlay_of: "paper:Gourmet2024"
status: active
relevance: "Direct prior art and external calibration target for h04 (hallmark/pathway ordering) and discussion:2026-06-07; validates clonality+selection (VAF/dN/dS), not patient age, as the ordering proxy, and flags the CH / hypermutator / TP53-dominance confounds the project must control before replicating hallmark-level ordering."
project_tags:
  - h04-pathway-ordering
  - hallmark-ordering-calibration
  - clonality-vaf-ordering
created: "2026-06-07"
updated: "2026-06-07"
---

Consumer overlay — the canonical cross-paper summary lives in `~/d/science-commons`
(`paper:Gourmet2024`). cBioPortal-specific relevance, framework mapping, and follow-up below.

## Relevance

This paper is the **direct prior art and external calibration target** for hypothesis `h04-mhn-pathway-ordering` and the primary empirical reference for `discussion:0007-hallmark-ordering-and-data-driven-modules`.

**(a) External calibration for h04's predicted ordering.**
h04 predicts that per-histology MHN fits will recover an "intrinsic mutators → lineage drivers → checkpoint/immune-late" order. Gourmet et al. provide exactly that at the hallmark grain: genome instability and immortality are first, immune evasion and inflammation are last, across 27/32 cancer types. This is the hallmark-level echo of h04's pathway-level prediction: the "intrinsic-instability-early → checkpoint/immune-late" ordering is confirmed in the largest cross-cancer VAF analysis to date.

**(b) Clonality + selection as the correct order proxy, validating the discussion's pushback on age.**
The paper uses VAF (clonality) and dN/dS (selective advantage) as the order proxy — precisely the combination that `discussion:2026-06-07` advocated and that q012 adopted as the methodological standard. Patient age is not used anywhere in the analysis. This is a direct methodological parallel: the project should use clonality-based ordering (via VAF/CCF or MHN), not patient age, as the primary ordering signal.

**(c) Trajectory clustering corresponds to the project's cancer-type clustering interest.**
The inter-tumor Pearson correlation heatmap (Fig. 2a) and patient-level k-means clustering (Fig. 3b-d) correspond to the project's interest in "clusters of cancer types with coherent ordering" (discussion). The melanoma exception (environmental disruption of common path) is particularly relevant: cBioPortal TCGA skin/uveal melanoma data would be expected to show the same deviation, providing a built-in falsification check for any ordering model.

**(d) Confounders the project faces that Gourmet et al. may not fully address:**

1. **Cross-sectional under-identification.** The VAF-ordering approach inherits the same fundamental limitation as MHN: a higher mean VAF is consistent with both "acquired earlier in the lineage" and "under stronger clonal selection regardless of order." The paper does not formally test these alternatives; it interprets VAF as a timing proxy without modeling the selection-vs-timing confound. The project's use of MHN (which explicitly models hazard rates) is methodologically stronger for directed ordering claims.

2. **Clonal hematopoiesis (CH) contamination.** In non-matched-normal TCGA studies, CH-contaminated mutations in DNMT3A, TP53, TET2, ASXL1, PPM1D would inflate VAF for genome instability and related hallmarks — potentially amplifying the "genomic instability first" signal artificially. The paper does not apply a CH filter. This is a direct concern for the cBioPortal pipeline's `t087` CH-aware annotation and `matched_normal_studies` config list.

3. **Panel callability.** GTEx uses RNA-seq-derived mutation calls; TCGA uses WES. The paper does not address panel callability corrections. For the project's mixed-panel GENIE data, the same callability mask required for t078 must be applied before hallmark-level ordering.

4. **Hypermutator tumors.** Hypermutator/MSI-H/POLE-driven tumors accumulate mutations throughout the genome at elevated rates. These tumors would have genome-instability-hallmark genes mutated at high VAF simply because of elevated mutation rate, not because GI was acquired early in a causal sense. The paper does not apply a hypermutator stratification filter (analogous to the project's t081). This is the most likely source of residual confounding in their GI-first result.

5. **TP53 dominance.** The paper's own sensitivity analysis shows that removing TP53 moves genome instability to last place. This raises the question of whether the "GI first" result reflects a genuine hallmark ordering or is driven by TP53's ubiquity and high clonality as a tumor suppressor loss-of-function event — which occurs across multiple hallmark categories (TP53 is listed in 8 of 10 hallmarks). The project's analysis would need to consider this carefully.

6. **Per-histology pooling.** The pan-cancer ordering pools all 32 cancer types before computing mean VAF. Type-specific findings (melanoma, thymoma exceptions) emerge only in the correlation heatmap. The project's per-histology approach avoids the Simpson's-paradox risk of pooling.

7. **CCF vs. VAF discordance.** Using CCF (ploidy-corrected) moves GI to a middle position, while VAF places it first. This discordance suggests that the GI-first result is sensitive to copy-number/ploidy status — a known source of technical confounding. The project should replicate both metrics when VAF data are available.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| VAF of nonsynonymous mutations as timing proxy | Clonality-based ordering (q012); t133 VAF audit | Same principle; project auditing VAF retention across cBioPortal studies |
| dN/dS (dNdScv) as selective advantage | Positive-selection annotation; Bailey 2018 driver overlay | dNdScv used in both; per-hallmark vs. per-gene grain |
| Hallmark gene sets from Zhang et al. 2020 (CHG) | Sanchez-Vega 2018 10-pathway annotation (current pipeline) | Different gene-set sources; project uses pathway layer, not hallmark layer directly |
| Common ordering in 27/32 cancer types | h04 prediction of intrinsic-mutator-early ordering | Direct calibration target; project would test at pathway grain per histology |
| Melanoma exception (UV mutagenesis) | Per-histology stratification; SBS7 signature group | Signature-stratified ordering (t111) expected to show same deviation |
| 2 patient clusters (early vs. late GI) | Cancer-type or patient clustering by mutation profile | Project interest in coherent ordering clusters across cancer types |
| Dichotomous GI position (ranked 1 or last) | TP53 clonality signal; CH contamination risk | TP53 dominant role; in non-matched-normal studies CH TP53 inflates GI rank |
| dN/dS > 1 in cancer, < 1 in healthy tissue | Positive selection in cancer vs. normal tissue | Validates hallmark gene sets as under genuine positive selection |
| ASCETIC algorithm (evolutionary trajectory inference) | MHN (h04); PLPM (RaphaelVandin2015) | ASCETIC is an alternative trajectory method; paper uses it as cross-validation |
| CCF (ploidy-corrected allele frequency) | VAF in pipeline; t133 VAF/CCF availability | CCF discordance with VAF is a methodological caution for the project |
| Healthy tissue (GTEx) negative control | Normal-tissue contamination concern (q001/q005) | Paper uses GTEx as external control; project removes contaminated samples |
| No hallmark ordering in healthy tissues | Cancer-specificity of driver ordering | Supports that any ordering recovered in TCGA/GENIE is tumor-biology signal |
| Randomization (pseudo-hallmark) control | Bootstrap / leave-one-study-out (h04 falsifiability) | Paper validates ordering is not a gene-set-size artifact; project would use leave-one-study-out |

## Follow-up

- **Use as calibration for h04.** When the project's per-histology MHN pathway ordering is computed (task t135), compare the recovered pathway-level ordering against the Gourmet et al. hallmark ordering by mapping Sanchez-Vega pathways to their corresponding hallmarks. The expected calibration check: MMR/POLE (genome instability pathway) orders early; immune checkpoint pathways order late. Deviation from this in ≥ 5 of the common cancer types would argue against h04 or flag a confound.

- **Replicate TP53 sensitivity analysis.** Before treating h04's predicted "intrinsic-instability-first" result as confirmed, replicate the paper's TP53-removal sensitivity test using cBioPortal data: does the GI pathway (or TP53 specifically) dominate the early ordering, and if so, does the ordering collapse when TP53 is excluded? This directly tests whether the GI-first result is a TP53-driven artifact vs. a genuine hallmark signal.

- **Apply hypermutator filter before any hallmark-level VAF analysis.** The project's t081 hypermutator annotation should be applied before any VAF-based hallmark ordering replication; the paper's omission of this filter is the most likely single confounder to address.

- **CH filter for non-matched-normal studies.** The project's `ch_priority_gene` flag (Bolton 2020 7-gene list) and `matched_normal_studies` config should be used to flag or exclude CH-contaminated mutations before hallmark-level VAF calculations, especially for TP53 (in GI) and DNMT3A/TET2 (which appear in metabolism/epigenetic hallmarks).

- **Obtain CHG gene sets (Zhang et al. 2020).** For a direct comparison between the paper's hallmark-level result and the project's Sanchez-Vega 10-pathway result, download the CHG database gene sets and cross-map them to the Sanchez-Vega pathways. This defines the hallmark-to-pathway bridge for calibration.

- **Examine ASCETIC as an alternative to MHN.** The ASCETIC algorithm (Fontana et al. 2023, Nat Commun 14:5982) is used in the paper as a cross-validation trajectory method operating on binary hallmark-presence matrices with CCF/VAF timing. It is an alternative to MHN for ordered progression inference and may be worth comparing against MHN for the project's module-ordering step (h04/q012). The ASCETIC GitHub is caravagnalab/ASCETIC.

- **Assess the 2-cluster patient stratification in cBioPortal data.** The paper's finding that early vs. late GI acquisition predicts prognosis is clinically actionable and directly testable in cBioPortal data. If VAF is available (t133 audit), compute per-patient hallmark VAF ranks and reproduce the 2-cluster PCA. A concordance check against the Gourmet et al. cluster assignments (using TCGA overlap samples) would validate both the method and the prognostic signal.
