---
id: "paper:Sorensen2023"
type: "paper"
title: "Pan-cancer association of DNA repair deficiencies with whole-genome mutational patterns"
status: "active"
ontology_terms:
  - mutational signatures
  - DNA damage response
  - loss-of-function
  - whole-genome sequencing
  - LASSO regression
  - homologous recombination deficiency
datasets:
  - "PCAWG (n=2568 WGS, 32 cancer types)"
  - "Hartwig Medical Foundation HMF (n=3497 WGS, 32 cancer types)"
source_refs:
  - "cite:Sorensen2023"
related:
  - "hypothesis:h08-agnostic-covariate-association-recovers-known-signature-aetiologies-and"
created: "2026-05-31"
updated: "2026-05-31"
---

# Pan-cancer association of DNA repair deficiencies with whole-genome mutational patterns

- **Authors:** Simon Grund Sørensen, Amruta Shrikhande, Gustav Alexander Poulsgaard, Mikkel Hovden Christensen, Johanna Bertl, Britt Elmedal Laursen, Eva R Hoffmann, Jakob Skou Pedersen
- **Year:** 2023
- **Journal:** eLife (12:e81224)
- **DOI/URL:** https://doi.org/10.7554/eLife.81224
- **BibTeX key:** Sorensen2023
- **Source:** PDF

## Key Contribution

This paper presents a pan-cancer, systematic screen of 736 DNA damage response (DDR) gene loss-of-function (LOF) events (both mono- and biallelic) across 6,065 whole-cancer genomes from PCAWG and the Hartwig Medical Foundation, using LASSO regression models trained on genome-wide mutational summary statistics (SBS signatures, indels, and structural variants) to predict DDR gene deficiency. The analysis identifies 24 DDR genes — including expected associations (BRCA1/2, MSH3/6, TP53, CDK12) plus novel ones (ATRX, IDH1, HERC2, CDKN2A, PTEN, SMARCA4) — whose deficiency can be predicted from whole-genome mutational patterns with good accuracy (AUROC up to 0.97 for CDK12 in prostate cancer). This provides a proof-of-concept catalogue linking repair-pathway failure to specific mutational scars, enabling genotype-agnostic identification of DDR-deficient tumours from sequencing data alone.

## Methods

**Data:** 6,065 WGS genomes from two independent cohorts — PCAWG (n=2,568; primary tumours from ICGC/TCGA) and Hartwig Medical Foundation (n=3,497; predominantly metastatic). Thirty-two cancer types covered. For 77 HMF tumours the primary site was unknown (annotated separately).

**DDR gene set:** 736 genes curated from three prior DDR gene lists (Knijnenburg 2018, Pearl 2015, Olivieri 2020). Variants were filtered from VCFs (GRCH37/hg19 coordinates), requiring PASS status, ≥2 PCAWG callers, absent in >200 samples (SNP exclusion), VAF ≥0.2, gnomAD germline frequency ≤0.5%.

**LOF annotation:** Pathogenicity assigned by CADD phred ≥25 (ClinVar supplemented). LOH was inferred from copy-number profiles (minor allele CN <0.2); deep deletion when total CN <0.3. Biallelic LOF defined as pathogenic variant + LOH, pathogenic variant + deep deletion, or two pathogenic variants. Monoallelic LOF = single pathogenic event. Variants of unknown significance (VUS, CADD 10–25) were excluded from training sets but their tumours are tracked.

**Mutational summary features:** Signature Tools Lib (Degasperi 2020) was used to assign organ-specific SBS signature exposures (converted to COSMIC SBS1–30; SBS1 excluded as age-proxy). Indels were counted by context (microhomology, repetitive, other). Structural variants were categorised by type (deletion, inversion, tandem duplication, translocation), size (1–10 kb, 10–100 kb, 100 kb–1 Mb, 1–10 Mb, >10 Mb), and clustered vs non-clustered.

**Modelling:** For each of 535 DDR-gene × cancer-type combinations (>5 biallelic or >10 monoallelic events in either cohort), a weighted LASSO logistic regression model (R `glmnet` v4.0) was trained. Per-sample weights balanced class imbalance; lambda selected 1 SD from minimum binomial deviance; k-fold cross-validation (k = number of LOF events, ≤ features capped at 1 per 10 mutated tumours). Performance evaluated by precision-recall AUC enrichment over the true-positive rate (PR-AUC-E). Monte Carlo permutation null (10,000–30,000 permutations per model) tested significance; Benjamini–Hochberg FDR <0.05 and PR-AUC-E >0.2 were the shortlisting thresholds. Final shortlist: 48 models across 24 DDR genes.

**Survival analysis:** Cox regression on overall survival for shortlisted models, evaluated in both cohorts.

## Key Findings

**Overall shortlist:** 48 predictive models for 24 DDR genes, spanning known and novel associations.

**BRCA1/2 (positive controls):** Biallelic BRCA2-d models in breast (AUROC=0.93, PR-AUC-E=0.29), ovary, prostate, and pancreas. All BRCA2-d models driven by deletions at microhomology sites (HRD scar), consistent with published HRDetect features. BRCA1-d in ovary driven exclusively by clustered + non-clustered tandem duplications (1–10 kb). Models generalise across HMF and PCAWG.

**TP53 (positive control):** 11 monoallelic predictive models across breast, skin, ovary, uterus, biliary gland, head and neck, pancreas, CNS, and neuro-endocrine cancers. TP53-d consistently associated with increased numbers of structural variants (SVs) genome-wide (except skin), PR-AUC-E 0.21–0.48.

**MMR / MSI (positive controls):** In HMF colorectal cancers, eight monoallelic models (MSH3, SMC2, SMC6, BMPR2, CLASP2, SRCAP, UBR5, UVRAG) all driven by deletions in repetitive DNA (MSI phenotype). However, 20–33% of the mutated tumours in these models co-mutate MSH3, and the authors judge reverse causality likely: the MSH3-driven MSI phenotype generated spurious LOF calls in the other genes, not vice versa. MSH3 itself (biallelic, prostate) is a genuine positive control (PR-AUC-E=0.25, AUROC=0.98).

**CDK12 (high-accuracy novel model):** Biallelic CDK12-d in HMF prostate cancers (n=10 LOF / 283 WT) predicted by large non-clustered tandem duplications (100 kb–10 Mb), AUROC=0.97, PR-AUC-E=0.73. The prostate-trained model also detects CDK12-d in breast and ovarian cancers at lower power (AUROC=0.72, PR-AUC-E=0.19). CDK12 is associated with CHK1/PARP inhibitor sensitivity; this is the first published predictive algorithm for CDK12 from WGS patterns.

**Novel associations:**
- *ATRX-d (CNS):* Biallelic (PR-AUC-E=0.21, AUROC=0.76) and monoallelic (PR-AUC-E=0.23, AUROC=0.71) models, both predicted by decreased SBS8 (BRCAness/late-replication). Co-mutated with IDH1 in 7/11 cases (28-fold enrichment).
- *IDH1-d (CNS):* Monoallelic model (PR-AUC-E=0.24, AUROC=0.82), likewise driven by reduced SBS8. IDH1 and ATRX co-loss may define a CNS subgroup with altered repair.
- *SMARCA4-d (cancers of unknown primary):* Biallelic model (PR-AUC-E=0.44, AUROC=0.85) driven by enrichment of SBS27 (highly correlated with SBS4, the smoking signature; Pearson r=0.96 in this cohort). SMARCA4 biallelic LOF tumours show significantly lower SMARCA4 mRNA expression vs WT. Model uses SBS4 as near-equivalent predictor.
- *CDKN2A-d (skin):* Monoallelic model (PR-AUC-E=0.28, AUROC=0.82) driven by deletions at microhomology sites + non-clustered inversions 100 kb–1 Mb + SBS7 (UV). Consistent with melanoma predisposition role.
- *HERC2-d (skin):* Biallelic (PR-AUC-E=0.24, AUROC=0.73) and monoallelic (PR-AUC-E=0.23, AUROC=0.66) models, driven by deletions in non-microhomologous, non-repetitive regions. HERC2 modulates P53 activity; 7/9 biallelic HERC2-d tumours also carry monoallelic TP53-d (8-fold enrichment).
- *PTEN-d (CNS and uterus):* Multiple models in both HMF and PCAWG for monoallelic (PR-AUC-E 0.22–0.37) and biallelic (PR-AUC-E 0.37) PTEN-d, primarily driven by depletion of various SV categories (non-clustered inversions, tandem duplications, deletions). Generalises across cohorts.
- *ARID1A-d (prostate):* Monoallelic model (PR-AUC-E=0.208, AUROC=0.72) driven by depletion of SBS8, independent of BRCA1/2 status.
- *MEN1-d (neuro-endocrine):* Biallelic model (PR-AUC-E=0.22, AUROC=0.82) driven by fewer SBS16 mutations (hyperactivity of POLH).
- *BAP1-d (skin):* Biallelic model (PR-AUC-E=0.26, AUROC=0.80) via decreased SBS7 + increased SBS30 (base excision repair deficiency).
- *RB1-d (urinary tract):* Biallelic model (PR-AUC-E=0.47, AUROC=0.84) driven by increased SBS7 mutations (UV aetiology in non-UV-exposed tissue — authors note this does not necessarily imply UV causality).

**Survival:** Nominally significant (p<0.05, univariate Cox) differences observed for BRCA2 and TP53 LOF in multiple cancer types and UVRAG in colorectal. BRCA1/2 LOF associated with improved survival in metastatic ovarian but decreased survival in breast (reflecting platinum treatment differences).

## Relevance

This paper is directly relevant to **h08** on two levels:

**H08a positive-control recovery:** The study provides strong empirical confirmation that signature-to-DDR-gene associations are recoverable from WGS-scale mutational patterns in an unbiased, data-driven manner. The methods here are analogous to the h08 positive-control design (UV↔SBS7, smoking↔SBS4, MMR-loss↔MSI signatures), demonstrating that the mapping can be made with acceptable statistical power at n~dozens of LOF events per gene-cancer stratum. The authors' explicit recovery of BRCA1/2 (SBS3/HRD), MSH3/MSH6 (SBS-MMR/MSI), TP53 (elevated SVs), and CDK12 (tandem duplication phenotype) validates the general principle underlying h08a.

**H08b discovery / novel associations:** The novel links (ATRX/IDH1→SBS8 depletion in CNS; SMARCA4→SBS4/27 in cancers of unknown primary; PTEN→SV depletion) demonstrate that beyond the known canonical map, systematic association scans surface biologically plausible, clinically actionable new signature aetiologies. This is the key h08b promise.

**Methodological relevance for cbioportal pipeline:** The paper uses LASSO regression on mutational summary statistics (SBS exposures + indel counts + SV counts) as features, which maps cleanly onto the outputs already generated by the cbioportal pipeline (`gene_cancer_study_ratio_annotated.feather` and the TMB/signature annotation layers). The feature engineering (organ-specific SBS assignments via Signature Tools Lib, SV categorisation by type + size + clustering) is a reference implementation for the types of covariates the h08 association layer should expose. The PR-AUC enrichment metric (PR-AUC-E = PR-AUC − baseline) is a useful benchmark for the within-cancer-type association design.

**Reverse-causation warning:** The colorectal MMR-driven spurious LOF models illustrate a key pitfall for the cbioportal pipeline's h08 scan: when a high-TMB / hypermutator phenotype (MSH3-driven MSI) generates apparent LOF calls elsewhere via passenger mutations, association models can capture MSH3's effect but attribute it to co-mutated genes. The h08 design guard (hypermutator exclusion / stratification) directly addresses this.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| SBS signature exposures (Signature Tools Lib, organ-specific then converted to COSMIC) | `run_restricted_sigprofiler_assignment.py` output | Different tool (SigProfiler vs SigTools) but same COSMIC SBS framework |
| LASSO regression model per DDR-gene × cancer stratum | h08 association layer (to be built) | Paper uses DDR-LOF status as outcome; h08 uses signature exposure as outcome with covariates as predictors — transpose of the same design |
| PR-AUC enrichment (PR-AUC-E) as performance metric | Not yet defined in project | Adopt for h08 within-tissue benchmarking |
| Biallelic vs monoallelic LOF stratification | Not in current pipeline (mutation presence/absence only) | Potential extension for DDR-specific analyses |
| SV categorisation (type × size × clustering) | Not currently in pipeline | Would require WGS-level SV calls; cBioPortal studies are predominantly panel/WES |
| Reverse causality check via co-mutation fraction | hypermutator flag + `ch_priority_gene` stratification | Partial overlap; direct co-mutation check is an extension |

## Limitations

- Restricted to WGS cohorts (PCAWG + HMF): panel and WES tumours excluded by design, limiting applicability to the cBioPortal panel-sequencing majority.
- Monoallelic LOF models in colorectal cancer are likely confounded by reverse causality (MSH3-driven hypermutator phenotype generates spurious LOF calls genome-wide). Authors discuss this but do not fully resolve it.
- No expression or methylation data integrated (SMARCA4 expression analysed post-hoc only); transcriptional silencing of DDR genes is a known LOF mechanism not captured.
- VUS excluded from training (CADD 10–25), potentially leaving some true LOF events unmodelled.
- Sample sizes for rare biallelic events are small (as few as 7–10 events per model), limiting power and increasing permutation uncertainty.
- Cohort-specificity: some models are significant only in HMF (metastatic) or only in PCAWG (primary), and the biological cause of cross-cohort differences is not always resolvable.
- SBS signature assignment uses organ-specific reference signatures (cohort-tailored via Degasperi 2020), which may not transfer directly to panel sequencing data at cBioPortal scale.

## Model / Tool Availability

- Code: https://github.com/SimonGrund/DDR_Predict (archived at swh:1:rev:c4daf1b7a9526ea411ad763c05d0c9317b45d42e)
- Includes preprocessing, 535 LASSO model fits, and ≥10,000 permutation null models per model.
- R-based pipeline (glmnet v4.0, Signature Tools Lib for feature generation).

## Follow-up

- How does the SBS signature feature engineering (Signature Tools Lib organ-specific assignments converted to COSMIC) compare with the SigProfiler-based assignment used in the cbioportal pipeline? Are the resulting exposures interchangeable for association modelling?
- The SMARCA4↔SBS27/SBS4 link in cancers of unknown primary is intriguing: SBS27 is flagged as a possible sequencing artefact in COSMIC. Can the cBioPortal data (which includes many lung/unknown-primary studies) corroborate the SMARCA4↔smoking signal using SBS4 directly?
- The PTEN-d↔SV-depletion signal (CNS and uterus) is unexpected — PTEN is not typically considered a structural repair gene. Are there prior WGS studies of PTEN-deficient organoids that could clarify mechanism?
- The CDK12 tandem-duplication classifier (AUROC=0.97 in prostate) is a plausible clinical tool. Does cBioPortal's PRAD cohort have sufficient panel-SV annotations to test a simplified version?
- Papers to read: Davies et al. 2017 (HRDetect); Nguyen et al. 2020 (CDK12 tandem-dup phenotype); Degasperi et al. 2020 (Signature Tools Lib organ-specific signatures); Nik-Zainal et al. 2016 (SV clustering definition).
