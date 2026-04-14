---
id: "topic:cohort-selection-bias-representativeness"
type: "topic"
title: "Cohort selection bias and population representativeness"
status: "active"
ontology_terms: []
source_refs: []
related:
  - "article:Zehir2017"
  - "article:Pugh2022"
  - "article:Nguyen2022"
  - "article:Bandlamudi2026"
  - "article:AACRGENIEConsortium2017"
  - "topic:targeted-panel-sequencing-bias"
  - "topic:cross-study-harmonization"
created: "2026-04-13"
updated: "2026-04-13"
---

# Cohort selection bias and population representativeness

## Summary

Clinical-sequencing cohorts (GENIE, MSK-IMPACT) over-represent advanced / metastatic /
pre-treated disease at tertiary referral centers. TCGA over-represents treatment-naive resected
primary tumors. Neither is a faithful sample of the underlying cancer population. Cross-study
aggregation that pools these without stratification produces gene-frequency estimates that
reflect *cohort composition* as much as biology.

## Key Concepts

- **Clinical-sequencing referral bias.** GENIE / MSK-IMPACT samples are ordered for therapy
  decisions, biasing toward patients with treatment options under consideration — typically
  advanced or refractory disease.
- **Treatment-history confounding.** Resistance-associated alterations are elevated by orders
  of magnitude in pretreated cohorts:
  - **AR mutations 18% in MSK metastatic prostate vs 1% in TCGA primary** (Zehir 2017)
  - **ESR1 mutations 11% in MSK metastatic breast vs 4% in TCGA primary** (Zehir 2017)
  - **EGFR T790M 11.3% of GENIE EGFR mutations vs 2.2% of TCGA EGFR mutations** (AACR GENIE 2017)
- **Demographic representation gaps.** Pugh 2022 GENIE v9.1: 72% White, 14% race unknown / not
  collected, 6% Black, 5% Asian. Geographic distribution skewed to US academic centers.
- **Specimen-state heterogeneity.** Primary vs metastatic biopsy; FFPE vs frozen; tumor-purity
  varies (PAAD ~33% in MC3, LAML ~44% — Ellrott 2018 — well below most TCGA cohorts).
- **Selective biopsy of metastatic sites.** Nguyen 2022 MSK-MET: lymph node 2,305, liver 2,289,
  lung 982, bone 726 are most-sampled met sites — clinically accessible / actionable sites
  over-represented.

## Current State of Knowledge

The literature **acknowledges these biases as first-order interpretive concerns but does not
publish portable corrections**. Most papers stratify analyses (primary vs metastatic; treated
vs naive) where stage is a covariate of interest, but cross-study aggregations (including ours)
typically pool without stratification.

Concretely:
- **TCGA-vs-GENIE concordance metric exists** (Pugh 2022: median weighted RMSD 0.32 across
  cancer types) but no per-gene correction recipe.
- **Per-cohort age / treatment / specimen-state metadata is in cBioPortal clinical sample
  tables** but inconsistently formatted across studies.

## Controversies & Open Questions

- **When (if ever) is it appropriate to combine primary-tumor and metastatic-tumor cohorts in
  a cross-study ratio?** Defensible for cancer types where primary and metastatic genomes are
  highly concordant (most carcinomas at gene-level); less defensible for cancers with clear
  primary-vs-metastatic divergence (e.g., AR mutations in prostate).
- **Should we report cohort-stratified ratios alongside pooled ratios?** Discordance between
  the two would itself be informative, but doubles the output dimensionality.

## Relevance to This Project

Our `summary/mut/table/gene_cancer_study.feather` and downstream rolls aggregate across
heterogeneous cohorts with no cohort-stage stratification. For genes whose mutation rate
genuinely changes with disease stage (AR, ESR1, MET, ERBB2-T798I, etc.), our pooled rates are
biased upward by clinical-sequencing-cohort dominance.

Concrete addition planned (task t052): per-study cohort-stage descriptor ingested from
cBioPortal study definitions (primary-naive / metastatic / pre-treated). Stratified analyses
where stage matters, plus a cohort-composition descriptor alongside every per-(gene, cancer)
ratio.

## Key References

Zehir2017 (cleanest quantification of advanced-disease bias); AACR GENIE 2017 (referral bias
in EGFR T790M); Pugh2022 (demographic gaps); Nguyen2022 (metastatic-site sampling bias);
Bandlamudi2026 (advanced-disease selection in 50k cohort).
