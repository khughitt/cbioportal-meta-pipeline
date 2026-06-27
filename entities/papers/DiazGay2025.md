---
type: paper
title: Geographic and age variations in mutational processes in colorectal cancer
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: paper:DiazGay2025
ontology_terms:
- mutational signatures
- colorectal cancer
- colibactin
- early-onset colorectal cancer
- mutational epidemiology
- SBS88
- ID18
- geographic variation
- whole-genome sequencing
datasets: []
source_refs:
- cite:DiazGay2025
related:
- paper:DiazGay2023
- paper:Alexandrov2020
---

# Geographic and age variations in mutational processes in colorectal cancer

- **Authors:** Marcos Díaz-Gay, Wellington dos Santos, Sarah Moody, Mariya Kazachkova, Ammal Abbasi, Christopher D. Steele, Raviteja Vangara, Sergey Senkin, Jingwei Wang, Stephen Fitzgerald, Erik N. Bergstrom, Azhar Khandekar, Burçak Otlu, Behnoush Abedi-Ardekani, and many others (Mutographs consortium); Paul Brennan, Michael R. Stratton, Ludmil B. Alexandrov (senior/corresponding)
- **Year:** 2025
- **Journal:** Nature
- **DOI/URL:** https://doi.org/10.1038/s41586-025-09025-8
- **BibTeX key:** DiazGay2025
- **Source:** PDF (Europe PMC XML full text)

## Key Contribution

This study applies whole-genome sequencing to 981 colorectal cancer genomes from 11 countries across 4 continents (the Mutographs cohort) to perform mutational epidemiology — linking geographic and age-related variation in colorectal cancer incidence to specific mutational signatures. The central finding is that colibactin-induced signatures SBS88 and ID18 (produced by pks-island-carrying bacteria such as E. coli) are enriched in early-onset colorectal cancer (3.3× more common in diagnoses before age 40 vs. over 70) and correlate with country-level colorectal cancer age-standardized incidence rates, implicating early-life microbial mutagenic exposure in the rising global incidence of early-onset colorectal cancer.

## Methods

- **Cohort:** 981 colorectal cancers (45.7% female; ages 18–95) from 11 countries: Argentina, Brazil, Canada, Colombia, Czech Republic, Iran, Japan, Poland, Russia, Serbia, Thailand. Countries classified as intermediate-incidence (ASR 13–20/100k) or high-incidence (ASR >24/100k).
- **Sequencing:** Whole-genome sequencing at median 53× (tumour) and 27× (normal) coverage, all matched tumour-normal pairs.
- **Molecular subtyping:** MSI/MSS status confirmed by ddPCR for 5 microsatellite markers. MSI cases (n=153, 15.6%), POLE/POLD1 ultra-hypermutated (n=13), HRD (n=7), and base excision repair-deficient (n=4) were identified but main analyses focused on 802 treatment-naive MSS cases.
- **Signature extraction:** De novo extraction using SigProfilerExtractor (500 NMF replicates, nndsvd_min initialization) for SBS, ID, DBS, CN, and SV variant types. An extended context (SBS-288, ID-83, CN-68, SV-38) leveraged WGS data. De novo signatures decomposed into COSMICv3.4 reference signatures using SigProfilerAssignment. Novel signatures SBS_O, ID_J, CN_F, SV_B, SV_D detected. Hierarchical Dirichlet process (mSigHdp) used as a complementary extraction method.
- **Association analyses:** Multivariable logistic/linear regression models adjusted for age, sex, country, tumour subsite, and tumour purity. Enrichments reported as odds ratios (OR) with Benjamini-Hochberg-adjusted q-values. Firth's bias-reduced logistic regression for complete/quasi-complete separation.
- **Timing analysis:** Mutations classified as early clonal, late clonal, or subclonal based on cancer cell fractions; signature contributions per timing category assessed.
- **Driver mutation analysis:** IntOGen framework identified 46 driver genes; probabilistic signature-to-mutation assignment used to attribute driver mutations to specific signatures.
- **Microbiome analysis:** pks island coverage from non-human-mapping sequencing reads used to detect active pks+ bacterial infection.
- **Genetic ancestry:** Principal component analysis on germline SNPs to assess population structure.

## Key Findings

**Molecular landscape (MSS CRC, n=802):**
- 16 SBS, 10 ID, 4 DBS, 6 CN, and 6 SV de novo signatures identified; the majority correspond to previously catalogued COSMIC v3.4 signatures.
- Known signatures include: SBS1/SBS5 (clock-like), SBS2/SBS13 (APOBEC), SBS3 (HRD), SBS18 (ROS), SBS88 (colibactin), and multiple unknown-aetiology signatures (SBS8, SBS17a, SBS17b, SBS34, SBS40a, SBS89, SBS93, SBS94).
- Novel SBS_O detected, representing a refined version of the previously reported SBS41.

**Geographic variation:**
- SBS89, DBS8, and ID_J enriched in Argentina (ORs: 28.0, 8.9, 9.6 respectively; q<0.001), with strong co-occurrence suggesting a shared unknown mutagenic exposure.
- SBS94, SBS_F, and DBS6 enriched in Colombia (ORs: 19.7, 10.7, 12.5); SBS94 and SBS_F co-occur.
- SBS2 (APOBEC) and SBS_H elevated in Russia; CN_F elevated in Brazil.
- DBS2 depleted in Thailand; DBS4 depleted in Colombia.

**Colibactin signatures and incidence rates:**
- SBS88 and ID18 positively associate with country-level colorectal cancer ASR (q<0.05), particularly for rectal cancer ASR (ID18: q=0.008).
- SBS1 and novel SBS_H also associate with increasing ASR, especially for colon cancer.

**Age-related enrichment of colibactin signatures:**
- SBS88 2.5× more common in CRC diagnosed before age 50 vs. after (q=0.006); ID18 4× more common (q=3.7×10⁻⁷).
- Colibactin exposure (SBS88 or ID18 present) found in 21.1% of MSS CRCs (169/802), and associated with earlier median age at diagnosis (62 vs. 67 years, P=1.6×10⁻⁸).
- Prevalence of colibactin signatures declines monotonically with age at diagnosis; 3.3× more common in patients <40 years vs. >70 years.
- Effect strongest in distal colon (median age 57 vs. 66 years, q=5.2×10⁻⁷) and rectum.
- Age-enrichment independent of country, genetic ancestry, and ethnicity.

**Colibactin as an early clonal event:**
- SBS88 and ID18 enriched in early clonal (vs. late clonal) mutations (q=4.2×10⁻⁴ and q=6.1×10⁻⁵), similar to clock-like SBS1/SBS5/ID1, consistent with mutagenesis occurring on normal colorectal epithelium early in life.
- No association between current pks+ bacterial presence (by microbiome sequencing) and SBS88/ID18 in tumour genome; cases with colibactin signatures but no pks+ bacteria have younger age at diagnosis, suggesting early-life exposure followed by microbiome turnover.

**Driver mutations:**
- 46 colorectal cancer driver genes identified; APC, TP53, KRAS, FBXW7, SMAD4, PIK3CA, TCF7L2, SOX9 mutated in >10% of cases.
- ID18 accounts for ~25% of APC indel driver mutations in colibactin-positive cases.
- SBS88 accounts for 64.3% of the colibactin-associated APC splicing variant c.835-8A>G.
- Colibactin signatures together account for 8.3% of all SBS/ID driver mutations and 15.5% of all APC driver mutations in colibactin-positive cases.
- More driver mutations observed in late-onset vs. early-onset CRC (FC=1.21, P=5.4×10⁻⁵); APC driver mutations enriched in late-onset.
- Country-enriched signatures SBS94/SBS_F (Colombia) and SBS89/ID_J (Argentina) also contribute elevated proportions of driver mutations in their respective countries.

## Relevance

**Connection to hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and (agnostic covariate-signature association):** This paper is a premier exemplar of the "mutational epidemiology" approach that hypothesis:0007 aims to operationalize: systematic, regression-based association of external covariates (geography, age at diagnosis, country-level incidence rates) with mutational signature exposures. Key connections:

- **Positive control recovery:** The study successfully recovers known causal exposures (colibactin → SBS88/ID18 enriched in younger patients with higher-incidence colorectal cancer) using multivariable regression adjusted for known confounders — exactly the validation strategy hypothesis:0007 requires for UV/smoking/APOBEC/MMR signatures.
- **Covariate adjustment strategy:** Geographic/demographic covariates (sex, country, tumour subsite, purity, age) are systematically included as adjustment variables in all regression models, illustrating how confounding can be controlled in multi-population covariate-signature association studies. This is directly relevant to the design of the agnostic covariate screen in hypothesis:0007.
- **Novel signature discovery via geography:** Multiple signatures of unknown aetiology (SBS89/DBS8/ID_J in Argentina; SBS94/SBS_F/DBS6 in Colombia) are identified through geographic enrichment analysis, showing that covariate-driven screens can implicate new mutational processes — a key motivation for hypothesis:0007.
- **Benchmark for APOBEC:** SBS2/SBS13 enrichment in Russia and expected age-associations of clock-like SBS1/SBS5 serve as positive controls demonstrating that known aetiology-exposure links are recoverable in this framework.
- **Cross-study meta-analysis relevance:** The study's aggregation of multiple country-cohorts into one unified signature analysis parallels the cross-study aggregation performed by this project (cBioPortal meta-analysis). It demonstrates that heterogeneous cohort-level covariates can be harmonized for joint signature-association analysis, suggesting that cross-study cancer-type and study-design covariates could be similarly leveraged.
- **Colibactin as case study:** The timing and driver-mutation analyses illustrate how signature exposures (early-life colibactin) propagate into driver gene mutations (APC indels), connecting signature biology to cancer gene mutation frequencies tracked by this project's pipeline.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Geographic signature variation (country-level) | Cross-study signature prevalence variation | Equivalent; country maps to study in our context |
| ASR (age-standardized incidence rate) as covariate | External covariate for signature association | Exactly the agnostic-covariate design in hypothesis:0007 |
| Multivariable logistic/linear regression per signature | Association test in hypothesis:0007 screen | BH-corrected, adjusted for confounders |
| SBS88 / ID18 (colibactin) as early-life imprint | Persistent signature exposure detectable in tumours | Relevant to normal-tissue mutation background (hypothesis:0005-healthy-somatic-background-atlas) |
| pks+ bacteria microbiome status | Environmental exposure proxy | Shows microbiome assay ≠ historical exposure |
| IntOGen driver gene detection | Driver gene identification (Bailey overlay [@Bailey2018]) | Partially overlapping gene sets |

## Limitations

- Study limited to 11 countries; countries with divergent incidence trends (e.g., USA) not directly included in the WGS cohort.
- No paired stool/microbiome samples from the same patients, preventing direct measurement of historical pks+ bacterial colonization; microbiome data inferred from tumour sequencing reads.
- BMI, diet, lifestyle, and other exposomal variables not systematically captured or analysed — explicitly flagged by authors as a study limitation.
- Genetic ancestry and self-reported ethnicity are confounded with country of origin (mostly homogenous within countries), precluding clean separation of environmental vs. genetic effects for country-enriched signatures.
- Causal interpretation of colibactin-early-onset association requires case-control studies of normal colorectal crypts, which are not yet available.
- MSI cases are under-powered for geographic/age analyses due to smaller n and domination of mismatch-repair signatures.
- Novel signatures SBS_O, ID_J, CN_F, SV_B, SV_D lack established aetiologies.

## Model / Tool Availability

- SigProfilerExtractor (de novo extraction): https://github.com/AlexandrovLab/SigProfilerExtractor
- SigProfilerAssignment (signature attribution): https://github.com/AlexandrovLab/SigProfilerAssignment
- mSigHdp (hierarchical Dirichlet process signature extraction): complementary method used for validation
- Data: raw sequencing data and derived mutation catalogues available from IARC/WHO; dbGaP/EGA accession not specified in this text

## Follow-up

- Read complementary normal-tissue colibactin study (referenced as Alexandrov et al. showing SBS88/ID18 in normal colorectal crypts).
- Examine SBS89's possible microbiome origin — the paper speculates it may be a second microbiome-derived mutagen with Argentina-specific exposure.
- Consider whether the cross-study cBioPortal meta-analysis can recover country-level SBS88 enrichment using publicly available genomic data, connecting the pipeline's aggregated mutation frequencies to epidemiological covariate screens (hypothesis:0007).
- Assess whether colibactin-associated APC indel enrichment is detectable in cBioPortal CRC studies through the ID18-signature mutation profile (T deletions in repetitive regions).
