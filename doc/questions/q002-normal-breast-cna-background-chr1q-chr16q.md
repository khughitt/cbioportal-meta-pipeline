---
id: "question:q002-normal-breast-cna-background-chr1q-chr16q"
type: "question"
title: "Do chr1q gains and chr16q losses in cBioPortal breast cancer studies partly reflect contaminating normal aneuploid epithelial clones?"
status: "active"
ontology_terms: []
datasets: []
source_refs:
  - "cite:Lin2024"
related:
  - "question:q001-normal-epithelial-clone-contamination-in-esophageal-studies"
  - "article:Lin2024"
  - "article:Yoshida2026"
  - "topic:pan-cancer-mutation-landscape"
created: "2026-04-18"
updated: "2026-04-18"
---

# Do chr1q gains and chr16q losses in cBioPortal breast cancer studies partly reflect contaminating normal aneuploid epithelial clones?

## Summary

Lin et al. 2024 (Nature) showed that histologically normal breast epithelium from healthy women contains a median 3.19% aneuploid cells, 82% of which form expanded clones bearing cancer-associated CNAs — most prominently chr1q gain and chr16q loss (the hallmarks of the der(1;16) rearrangement typical of luminal A/B breast cancer). These normal-tissue clones expand with age, are enriched in luminal lineages, and are undetectable by standard histopathology. This raises the question: do CNA frequencies reported in cBioPortal breast cancer studies for chr1q and chr16q include a measurable contribution from contaminating normal-epithelial aneuploid clones, particularly in studies with lower average tumour purity?

## Why It Matters

- Inflation of chr1q gain and chr16q loss rates in breast studies would overestimate their utility as tumour-specific driver events in cross-study aggregation outputs.
- A future CNA annotation layer in the pipeline must treat 1q/16q as high-background normal-tissue events requiring tumour-purity adjustment for breast cancer studies.
- Older patient cohorts (which have higher aneuploid cell burdens, P < 0.05 in Lin 2024) would show the largest inflation; cohort age-distribution differences across cBioPortal studies could therefore masquerade as biological heterogeneity in 1q/16q frequencies.
- The question has direct downstream implications for any study clustering breast cancer studies by CNA profile similarity.

## Current Evidence

- Lin et al. 2024 establishes the baseline: median 3.19% aneuploid cells / 82% in expanded clones in normal breast; chr1q gain at 15.11% frequency among aneuploid cells, chr16q loss ~8%. These frequencies are from reduction mammoplasty (presumably low-risk) cohort.
- No published calibration study exists quantifying normal-breast CNA misattribution in standard WES or panel-based breast cancer genomics datasets, in contrast to the well-characterised 5–25% CH misattribution rates in unmatched blood-based panels (Coombs 2017, Ptashkin 2018).
- Lin 2024 explicitly does not demonstrate that detected aneuploid clones are on a transformation trajectory — they may be stably tolerated. This weakens the contamination concern for individual events but does not resolve the rate inflation question.
- The current cbioportal pipeline focuses on somatic SNV mutation frequencies; CNA features are not yet integrated. The question therefore remains theoretical until a CNA layer is added.

## Thoughts

- The most direct empirical check would require tumour-purity metadata for cBioPortal breast cancer studies (e.g., ABSOLUTE estimates, where available) and stratification of 1q/16q frequencies by purity decile. A purity-dependent frequency gradient would be evidence for normal-tissue clone contamination.
- An alternative indirect check: compare 1q/16q frequencies in matched-normal breast studies (where contaminating germline and normal-tissue variants are subtracted during somatic calling) vs. tumour-only studies. MSK-IMPACT breast cancer data (largely matched-normal) is in cBioPortal and would serve as a clean comparison.
- The issue is breast-specific: Lin 2024 did not detect MYC (chr8q), ERBB2 (chr17q), or RB1/BRCA2 (chr13) alterations in normal tissue, suggesting those CNAs are not subject to the same contamination concern.

## Connections to Project

- Related hypotheses: none yet filed; this question could motivate a hypothesis about purity-dependent CNA rate inflation in breast studies.
- Required data or analyses: tumour purity metadata for cBioPortal breast studies; 1q/16q frequency table stratified by purity and study collection method; matched vs. unmatched normal comparison for breast-subset studies.
- Priority level: low for the current pipeline (SNV-focused, CNA not integrated); medium if a CNA annotation layer is added in future.

## Related

- Topic notes: `topic:pan-cancer-mutation-landscape`, `topic:mutation-rate-normalization`
- Article notes: `article:Lin2024`, `article:Yoshida2026`
- Related question: `question:q001` (same conceptual issue for esophageal NOTCH1/TP53 inversion)
- Methods/Datasets: cBioPortal breast cancer study list; MSK-IMPACT breast subset (matched normal); TCGA BRCA (matched normal via MC3); ABSOLUTE/FACETS purity estimates where available
