---
id: paper:Nagpal2022
type: paper
title: Canalization of the Polygenic Risk for Common Diseases and Traits in the UK
  Biobank Cohort
status: active
ontology_terms: []
source_refs:
- cite:Nagpal2022
related: []
created: '2026-04-25'
updated: '2026-04-25'
---

# Canalization of the Polygenic Risk for Common Diseases and Traits in the UK Biobank Cohort

- **Authors:** Sini Nagpal, Raghav Tandon, Greg Gibson
- **Year:** 2022
- **Journal:** Molecular Biology and Evolution, 39(4): msac053
- **DOI/URL:** https://doi.org/10.1093/molbev/msac053
- **PMCID:** PMC9004416
- **BibTeX key:** Nagpal2022
- **Source:** PDF

## Key Contribution

This paper provides the first large-scale empirical evidence that canalization — the evolutionary
buffering of genetic liability by regulatory network architecture — is widespread in the human
genome with respect to complex disease risk. Analyzing 10 traits and 151 environmental exposures
in 408,925 UK Biobank participants, the authors show that in approximately one-fifth of
gene-environment comparisons the deviation between prevalence-risk curves increases monotonically
with polygenic score (PGS) percentile, indicating that genetic and environmental influences
interact non-additively. Crucially, the direction is trait-specific: BMI shows predominantly
decanalization (unhealthy environments amplify genetic risk at the extremes), whereas
waist-to-hip ratio shows predominantly canalization (genetic effects are buffered across much of
the risk spectrum), implying that different evolutionary pressures have shaped the regulatory
architecture of these two closely related anthropometric traits.

## Methods

**Cohort:** 408,925 self-reported White British UK Biobank participants. Genotype imputation v3
(~96 M markers); bi-allelic variants with imputation score > 0.9, MAF > 1%, HWE P > 10⁻¹⁰,
< 5% missingness retained; 8,063,507 SNPs used for GWAS and PGS construction.

**Traits:** Seven binary disease phenotypes (obesity by BMI, WHR-obesity, CAD, T2D, depression,
college attainment, IBD + UC/CD subtypes) and three continuous traits (BMI, WHR, educational
attainment in years). ICD-10 codes plus self-report questionnaire data.

**PGS construction:** LD-pruned summary statistics ("–indep-pairwise" in PLINK, r² > 0.2 within
1 kb) at two thresholds (P < 5×10⁻⁸ genome-wide; P < 0.001). Scores computed via PLINK
`–score`. BMI additionally evaluated with PRS-CS Bayesian continuous shrinkage.

**Environmental exposures:** 151 UKB data fields dichotomized into high/low groups spanning diet,
lifestyle, socioeconomic, psychosocial, early-life, familial, and general health categories.

**Detection framework:** For each trait × exposure pair, prevalence-risk curves (observed
prevalence vs. PGS percentile bin) were generated for the high and low exposure groups. The
High-minus-Low (H-L) curve was required to be (1) monotonically increasing or decreasing
(derivative consistently signed) and (2) have a linear deviation greater than that seen in 100
random permutations of exposure labels. Conservative threshold: ≥ 2 SD above mean permutation
deviation; suggestive threshold: ≥ 1.3 SD.

**Continuous-trait modeling:** Four complementary approaches including (i) prevalence-threshold
equalization, (ii) regression of trait on PGS × Env interaction term, (iii) per-percentile-bin
mean with nonlinear least-squares fitting of `Trait = SP + MBL × exp(PGS/CF)`, and (iv)
inverse normal transformation of per-bin means. Canalization/decanalization inferred from the
departure of observed tail deviations from expected tail deviations under the null.

**Calibration factor (CF):** A parameter in the SP/MBL/CF model that scales the curvature of the
PGS-prevalence relationship; larger CF in the unhealthy environment implies decanalization
(genetic effects amplified at high risk), smaller CF implies canalization.

## Key Findings

1. **Scale of PGS×E interactions:** ~20% of the 151 exposure comparisons showed evidence of
   PGS×E interaction at the suggestive level for at least one of the 10 traits, with enrichment
   in lifestyle (exercise, smoking, drinking) and familial (parental/sibling illness) categories.
   An additional 10% showed additive environmental shifts independent of PGS.

2. **Decanalization predominates for metabolic traits and CAD:** BMI, T2D, and CAD show more
   decanalization than canalization across environmental categories. For BMI, 82 of 126
   contrasts had positive delta (decanalization direction), 32 significantly so after inverse
   normal transformation. Slow walk pace, daytime napping, and alcohol consumption were top
   decanalization exposures.

3. **Canalization predominates for WHR:** WHR had ~20 canalization versus 8 decanalization
   instances at the suggestive level — striking given BMI and WHR both measure adiposity,
   implying different evolutionary constraints on the genetic architectures of central versus
   overall adiposity.

4. **Familial illness as genetic confounder:** Having a father or sibling with diabetes
   decanalized T2D PGS curves, likely reflecting shared genetic variance not captured by the
   PRS; inversely, maternal stroke or sibling diabetes tended to suppress depression PGS curves
   (apparent canalization possibly via caretaking-related behavioral buffering).

5. **Educational attainment:** High Townsend deprivation index interacts with EA PGS to produce
   decanalization — individuals at low PGS are ~3% less likely to attain a college degree in
   high-deprivation areas, whereas those at the top of the PGS distribution are ~3% more likely
   regardless of deprivation, a canonical canalization-from-below / decanalization-from-above
   pattern.

6. **IBD:** Fewer PGS×E interactions than chronic metabolic traits; dietary patterns (whole grain
   bread preference protective, salt addition decanalizating for CD) and past tobacco smoking
   confirmed as amplifying IBD genetic risk.

7. **Mechanistic candidates:** Authors propose three non-exclusive mechanisms for canalization:
   (a) epistatic G×G interactions suppressing additive variance, (b) G×E interactions in
   perturbing environments reducing individual allelic effects, and (c) cryptic genetic variation
   at loci manifesting only in specific environments.

8. **PGS calibration artifact:** A portion of observed decanalization signal in binary traits is
   attributable to the liability-threshold model's dependence of odds-ratio effect sizes on
   prevalence (allelic effects appear smaller in high-prevalence environments), requiring CF
   correction. After calibration, decanalization signal persists for CAD, T2D, and obesity.

## Relevance

This paper connects to `spec:research-question` indirectly but importantly. The project asks
which gene-cancer associations are robust across independent studies — a question that is
fundamentally about **why some genetic signals replicate and others do not**. Canalization theory
offers a mechanistic lens: genes embedded in highly canalized (buffered) regulatory networks may
show *less* consistent somatic mutation enrichment across cBioPortal studies because the network
context varies across cancer types and study cohorts, whereas decanalized genes (those whose
mutation phenotype is exquisitely sensitive to cellular environment) may appear as strong
context-specific drivers in some studies but not others.

More concretely:

- **Driver-gene robustness:** The hypermutator annotation pipeline (tasks t081/t092–t099)
  classifies samples by mutational burden and reasons. Canalization predicts that driver genes
  in buffered network hubs should show stable mutation frequencies across the `_inclusive` vs.
  `_exclusive` hypermutator strata, while decanalized drivers should show amplified enrichment
  in hypermutator samples (analogous to the high-environmental-risk arm here).

- **Cross-study consistency as a canalization proxy:** In the cbioportal aggregation, the
  `k_studies` and `status` columns from the t077 pooled meta-analysis flag genes mutated
  consistently across studies. High `k_studies` with narrow inter-study variance is the somatic
  analogue of canalization — the gene's mutation phenotype is buffered against cohort/environment
  variation. Low `k_studies` or high inter-study variance is the decanalization analogue.

- **BMI/WHR dissociation as a template:** The paper's finding that two correlated phenotypes
  (BMI, WHR) can have opposing canalization architectures maps onto cBioPortal observations
  where closely related cancer types can have divergent driver-gene profiles — a reminder that
  histological proximity does not guarantee shared genetic buffering structure.

- **PGS×E as a model for somatic PRS×tumor-environment:** The calibration framework (SP, MBL,
  CF model; prevalence-risk curve shape analysis) is methodologically transferable to
  tumor-mutational-burden (TMB) × cancer-type analyses — evaluating whether high-TMB tumors
  (analogous to high-environmental-risk individuals) show amplified or buffered gene-specific
  mutation enrichment relative to low-TMB tumors.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Polygenic Score (PGS) | Per-sample mutation burden / TMB | Both rank individuals on cumulative genetic liability |
| Environmental exposure (high/low) | Cancer type / study cohort | Defines the context in which genetic liability is expressed |
| Prevalence-risk curve | Gene mutation ratio vs. TMB stratum | Canalization detectable as flattening at high-TMB extremes |
| Calibration factor (CF) | Study-level ratio normalization | Analogous CF correction needed before cross-study curve comparison |
| Decanalization (G×E amplification) | Driver enrichment in hypermutators | Genes whose somatic enrichment scales super-additively with TMB |
| Canalization (G×E buffering) | Stable driver frequency across cohorts | High `k_studies`, low inter-study variance in `gene_cancer_study_ratio_annotated.feather` |
| Familial illness as genetic confounder | Study-level panel/cohort composition bias | Shared genetic variance inflating apparent environmental effect |

## Limitations

- **Ancestry restriction:** Analysis limited to self-reported White British UKB participants
  (n = 408,925); PGS portability across ancestries is low (Chen 2015, Martin 2017 cited);
  findings may not generalize.
- **Healthy volunteer bias:** UKB has known healthy volunteer selection effects, particularly for
  behavioral traits, which could attenuate decanalization signal.
- **Reverse causation:** For several exposures, the disease may precede the environmental state
  (e.g., diabetics becoming sedentary), making causal interpretation of decanalization direction
  uncertain.
- **No independent validation cohort:** Authors note this as a key limitation; findings in
  specific traits (e.g., IBD dietary interactions) would benefit from replication.
- **Binary dichotomization of exposures:** Continuous environmental gradients collapsed to
  high/low, potentially losing signal and introducing threshold arbitrariness.
- **Calibration model assumptions:** The SP/MBL/CF framework assumes the liability threshold
  model holds and that the CF captures all non-additivity; more flexible nonlinear models might
  reveal additional structure.
- **Odds-ratio prevalence dependence:** A substantial fraction of apparent decanalization in
  binary traits is attributable to the statistical artifact that allelic ORs shrink as
  prevalence increases — requires careful CF correction that may over- or under-correct.

## Model / Tool Availability

- **Shiny app:** https://canalization-gibsonlab.shinyapps.io/rshiny/ — interactive exploration
  of all 151-exposure × 10-trait prevalence-risk curves and (de)canalization calls.
- **Code and data:** Available via UKB application number 17984; analysis performed in R using
  PLINK, `nls` (R base), and standard GWAS tools.

## Follow-up

- Read Gibson 2009 (decanalization concept) and Gibson & Wagner 2000 (canalization theory) as
  foundational references for the conceptual framework.
- Simons et al. 2018 (omnigenic model + stabilizing selection) is cited as the evolutionary
  context for why canalization might be expected genome-wide.
- Evaluate whether the cbioportal inter-study variance of `gene_cancer_study_ratio` (especially
  for known drivers vs. passengers) tracks the canalization vs. decanalization gradient predicted
  by this paper's framework.
- Consider whether the `pooled_ratio_{inclusive,exclusive}` columns from t077 could be used
  to construct a somatic analogue of the prevalence-risk curve shape test developed here.
