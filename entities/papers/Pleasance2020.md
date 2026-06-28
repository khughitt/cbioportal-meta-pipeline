---
type: paper
title: Pan-cancer analysis of advanced patient tumors reveals interactions between
  therapy and genomic landscapes
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: paper:Pleasance2020
ontology_terms:
- mutational signatures
- somatic mutation
- pan-cancer
- tumor mutational burden
- immune microenvironment
- DNA damage response
- treatment-associated mutagenesis
datasets: []
source_refs:
- cite:Pleasance2020
related: []
---

# Pan-cancer analysis of advanced patient tumors reveals interactions between therapy and genomic landscapes

- **Authors:** Erin Pleasance, Emma Titmuss, Laura Williamson, Harwood Kwan, Luka Culibrk, Eric Y. Zhao, et al. (Marco A. Marra, corresponding)
- **Year:** 2020
- **Journal:** Nature Cancer
- **DOI/URL:** https://doi.org/10.1038/s43018-020-0050-6
- **BibTeX key:** Pleasance2020
- **Source:** PDF

## Key Contribution

This paper describes the POG570 cohort — 570 advanced and metastatic tumors profiled by whole-genome sequencing (WGS), transcriptome sequencing, and comprehensive clinical/treatment annotation through the BC Cancer Personalized OncoGenomics program. The central contribution is a systematic pan-cancer analysis demonstrating that prior therapy leaves distinct mutational footprints on tumor genomes: platinum-based chemotherapy elevates signatures SBS31 and DBS5, combined platinum + DNA-synthesis inhibitor therapy elevates SBS17b, and DNA-damage-inducing genotoxic therapy broadly increases TMB — with error-prone polymerases POLQ and Polζ mediating part of this effect. The study additionally links mutation signatures and immune expression clusters to overall survival and immunotherapy response, providing a resource specifically designed for the clinically important but data-sparse post-treatment metastatic setting [@Pleasance2020].

## Methods

**Cohort.** 570 patients with advanced/metastatic cancer across 25 histologies biopsied from 18 organ groups, enrolled at BC Cancer (July 2012–August 2017, NCT02155621). 82% received systemic therapy before biopsy; 110 different drugs were administered, with median treatment durations ranging from days to >4 years [@Pleasance2020].

**Sequencing.** WGS to ~80× tumor / ~40× germline; RNA-seq targeting 150–200 million 75-base paired-end reads. Libraries prepared from biopsied/resected specimens; peripheral blood used as normal. Data deposited at EGA (EGAS00001001159) [@Pleasance2020].

**Somatic alteration discovery.** SNVs, IDs, CNVs, LOH, SVs called from paired tumor–normal WGS (BurrowsWheeler Aligner, multiple callers). MSI via MSIsensor; HRD scores via HRDtools. Microbial detection via BioBloomTools.

**Mutation signatures.** De novo NMF-based decomposition from 6,181,180 somatic SBSs, 974,629 IDs, 54,042 DBSs using a published framework. Signatures matched to COSMIC v3 (May 2019) by cosine similarity (≥0.6 for match). Temporal ordering of SBS signatures via SignIT on clonal subpopulations. Final analysis retained 482 patients in 12 completed SBS cohorts [@Pleasance2020].

**Drug–signature associations.** Wilcoxon signed-rank tests comparing signature exposures across three groups: unexposed, short treatment (<median days), long treatment (≥median days). Twenty most common chemotherapy drugs examined for seven DNA-damaging drug classes. Multiple testing correction via Bonferroni.

**Gene expression.** RNA-seq aligned with STAR; quantified using RSEM; batch effects minimized by ComBat. Clustering and CIBERSORT deconvolution of immune cell types.

**Immune microenvironment.** CIBERSORT deconvolution of all 22 leukocyte cell types; ConsensusClusterPlus identified 8 immune clusters. TCR repertoire analysis via MiXCR on 372 non-lymphoid samples (dominance and Shannon diversity). ICI cohort: 76 patients receiving ICIs post-biopsy [@Pleasance2020].

**Subclonal / heterogeneity analysis.** EXPANDS to identify subpopulations; Shannon diversity index for ITH.

**Statistical.** All tests two-sided; R and Python; no pre-determined sample sizes; multiple testing via FDR or Bonferroni as appropriate.

## Key Findings

### Cohort and genomic landscape
- 7,441,311 somatic substitutions and 701,166 small indels detected; mutation burden ranged from <0.1 to 159 mutations/Mb.
- Most frequently altered oncogenes/suppressors: TP53, NF1, RB1, KRAS, CDKN2A/B, MYC (consistent with TCGA PCAWG).
- ESR1 mutation frequency 12.9% POG570 vs 1.2% PCAWG (all subtypes); PTEN elevated in metastatic ovarian serous cystadenocarcinoma (15% vs 0% PCAWG). FGFR1 amplification 17% vs 11% TCGA.
- 4% of cases had detectable viral/microbial sequences (Fusobacterium, herpesvirus, HPV).
- 1.1% of mutations were in noncoding regions (42% intronic, 56% intergenic); three regulatory region hotspots in ≥2% of patients: TERT promoter, ADGRG6 enhancer, PLEKHS1 promoter.

### Therapy-associated mutagenesis
- **Elevated TMB:** Patients with genotoxic therapy for >1 year had significantly higher TMB than untreated (P=0.00018); on average a twofold increase (4,304 additional somatic mutations) in long-treated vs untreated patients.
- **Error-prone polymerases:** POLQ mutations associated with elevated TMB in genotoxic-treated patients (P=0.00066); Polζ (REV3L/POLD3) mutations associated with elevated TMB after genotoxic therapy (P=0.0016), both independently of tumor type.
- **Platinum → SBS31 + DBS5:** SBS31 elevated in all platinum-treated patients (P=3.4×10⁻¹⁰); DBS5 elevated with platinum exposure (P=5.8×10⁻¹³); expanded tumor type coverage to include cholangiocarcinoma and sarcomas.
- **Platinum + DNA-synthesis inhibitors → SBS17b:** SBS17b biased toward late clonal timing; combination platinum + DNA-synthesis inhibitor therapy (capecitabine, gemcitabine, 5-FU) significantly elevated SBS17b (P=0.0020 for combination vs either alone in BRCA). Proposed to arise from replication stress.
- **Radiation → ID8:** Identified in breast and sarcoma, elevated in irradiated vs non-irradiated tumors (P=5×10⁻³); characterized by >5-bp deletions enriched for microhomology — consistent with non-homologous end joining of radiation-induced DSBs.
- **Tamoxifen → SBS2 (APOBEC):** SBS2 correlated with tamoxifen exposure duration in BRCA (P=0.011); APOBEC3A expression elevated in long-tamoxifen-treated tumors (P=0.052), consistent with APOBEC-mediated mutagenesis contributing to acquired tamoxifen resistance.

### De novo mutation signatures
- 15 COSMIC-matched SBS signatures, 6 DBS, 9 ID identified.
- Six additional novel SBS (MSBS1–MSBS6) and seven novel ID (MID1–MID7) identified.
- MSBS1: predominantly early-arising; matches SBS1B. MSBS2: most similar to APOBEC SBS2 and SBS13 (cosine 0.67 and 0.63). MSBS6 (late): similar to SBS7c (cosine 0.66) — a melanoma-specific UV-independent signature. MSBS3 (late): similar to SBS9 and SBS17b; pancreatic and stomach cancers.
- Signature network (Spearman correlations): tobacco cluster (SBS4, DBS2, ID3); UV cluster (SBS7a, MSBS6); APOBEC cluster (SBS2, SBS13, DBS11); HRD/platinum cluster (SBS3, SBS8, SBS31, DBS5, ID6, SBS17b).

### DDR mutations and genomic instability
- 181 DDR gene pathways surveyed; 357 patients had somatic DDR mutations. Most frequent: TP53 (36%), ATM (2.6%), BRCA2 (2.3%).
- DDR mutations → significantly higher TMB even excluding hypermutators (P<2.2×10⁻¹⁶); also increased structural instability (HRD score).
- 13.5% of patients carried pathogenic germline variants in 98 cancer predisposition genes (17 cancer types, 27 CPGs); prevalence comparable to estimates in similar advanced cohorts (12.2–17.8%). 39% of germline carriers had a second somatic hit consistent with Knudson two-hit model.

### Tumor heterogeneity and survival
- ITH positively correlated with TMB (r=0.58, P<2.2×10⁻¹⁶).
- High TMB associated with poorer overall survival (HR=1.52, P=7.03×10⁻⁵), but ITH did not independently contribute to prognosis (HR=1.05, P=0.68).

### Immune microenvironment and ICI response
- Eight immune clusters identified (independent of tumor type and biopsy site). Cluster 5 (B-cell + T-cell enriched) had highest overall survival (P=0.00011); HR=0.4 relative to BRCA reference (P=0.001) — consistent with tertiary lymphoid structure.
- TCR diversity positively correlated with T-cell signatures (r=0.76); high diversity negatively correlated with dominant clonotype (r=−0.46).
- In ICI-treated patients (n=76), combined high exonic TMB + high T-cell signature predicted longest duration of ICI therapy (P=0.0055; HR=0.18 accounting for tumor type).

### Treatment-associated resistance markers
- ESR1 and EGFR resistance mutations enriched in treated vs untreated in BRCA and LUNG respectively.
- FGFR1 amplification (17q) associated with aromatase inhibitor resistance in BRCA (P=0.022).
- CTNNB1 (β-catenin) mutations co-occurred with EGFR resistance mutations in long-treated EGFR-inhibitor cases.
- VEGFA expression elevated in bevacizumab-treated colorectal patients (P=0.00058) — possible compensatory mechanism.
- DPYD expression reduced in >90-day 5-FU-treated colorectal patients (P=0.0084); somatic DPYD loss consistent with acquired 5-FU sensitivity.

## Relevance

**hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and — agnostic covariate↔signature-exposure association:**

This paper is among the most directly relevant studies for hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and. It delivers several positive-control anchors:

1. **Treatment duration → specific signatures:** SBS31/DBS5 increasing with platinum duration (P=3.4×10⁻¹⁰), SBS17b with platinum+DNA-synthesis inhibitor combination, ID8 with radiation, SBS2 with tamoxifen — all within a multi-histology cohort with rich treatment covariates. These are exactly the kind of covariate↔exposure associations the project hypothesis proposes to recover agnostically from cross-study data.

2. **APOBEC3 expression as mediator:** The tamoxifen→SBS2 association with concomitant APOBEC3A mRNA elevation is a concrete example of the expression-module → signature link that the expression-module design aims to recover systematically.

3. **Within-tissue vs pan-cancer confounding:** The paper shows associations that hold after accounting for tumor type (linear regression covariates); the project hypothesis specifically asks whether conditioning on tissue reverses sign. Pleasance et al. [@Pleasance2020] provide the empirical baseline — many therapy effects survive within-tissue conditioning.

4. **Immune clusters predict ICI response in combination with TMB:** The TMB × T-cell signature interaction (P=0.0055) directly motivates the hypothesis that immune/inflammation expression modules will associate with signatures beyond what clinical labels alone capture. The immune cluster finding also warns of a reverse-causation scenario (immunoediting on burden, the hypothesis's alternative R3).

5. **Novel signatures MSBS6 (UV-independent melanoma) and MSBS3:** Illustrate that a subset of signatures in advanced/treated cohorts may lack a clear COSMIC aetiology — precisely the targets for the hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and discovery prong.

**Cross-study meta-analysis relevance:** POG570 is a post-treatment advanced-cancer cohort distinct from TCGA primaries. The elevated SBS31/DBS5/SBS17b in treated patients is a key confound for any cross-study somatic mutation frequency analysis that mixes treated and untreated tumors. The pipeline's `matched_normal_studies` list and hypermutator annotation pipeline (AGENTS.md) should ideally flag therapy-induced hypermutation distinct from intrinsic DDR-deficiency or MSI hypermutation — this paper provides the signature-level evidence for that distinction.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| SBS31 / DBS5 (platinum-associated) | Therapy-induced signature | Confound in cross-study aggregation of treated cohorts |
| SBS17b (platinum + DNA-synthesis inhibitor) | Therapy-induced signature | Late-arising; combination-therapy specific |
| ID8 (radiation) | Therapy-induced signature | Deletions >5 bp with microhomology |
| SBS2/APOBEC + APOBEC3A expression | Expression-module → signature | Mediator-level association for hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and |
| ITH (Shannon diversity via EXPANDS) | Intratumor heterogeneity | Correlated with TMB; independent of prognosis |
| Immune clusters (CIBERSORT) | Immune expression modules | Eight clusters; cluster 5 = best survival |
| ICI response: TMB × T-cell score | Combined biomarker | Motivates hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and expression × signature interaction |
| POLQ / Polζ mutations + genotoxic therapy | DDR pathway mutagenesis | Distinct from MSI/POLE hypermutation |
| POG570 cohort | External reference dataset | BC Cancer WGS + RNA-seq; 570 advanced cancers |

## Limitations

- **Post-treatment bias:** 82% of patients had prior therapy. Disentangling intrinsic vs therapy-induced signatures relies on untreated subgroups that may be systematically different (earlier-stage, different histology). Causal attribution of signature elevations to specific drugs remains correlational.
- **Mixed histologies with small per-type N:** Many tumor type subgroups have n<30, limiting within-type power. Signature analyses restricted to cohorts with sufficient patients (≥10% mutations timed).
- **No matched longitudinal samples:** Biopsy is a single post-treatment snapshot; temporal inference of signature ordering relies on clonal subpopulation modeling (SignIT), not serial biopsies — SPECULATION for many individual cases.
- **Single institution:** BC Cancer (Vancouver); treatment patterns, drug formulary, and patient selection may not generalize to other centers or jurisdictions.
- **Treatment reconstruction from pharmacy records:** Duration and dose approximations; cannot fully account for drug holidays, dose reductions, or prior treatments outside BC Cancer system.
- **Transcriptome available for only a subset:** Expression-based analyses may have different sample composition than somatic analyses.
- **ICI cohort is small (n=76):** TMB × T-cell response prediction is hypothesis-generating, not definitively powered.

## Model / Tool Availability

- Full mutation catalog and gene expression TPMs available at http://bcgsc.ca/downloads/POG570/
- Sequence data at EGA under EGAS00001001159
- cBioPortal instance: https://www.personalizedoncogenomics.org/cbioportal/
- SignIT (temporal signature ordering): https://github.com/eyzhao/SignIT
- No standalone tool released; all analysis uses open-source packages listed in Methods (R, Python)

## Follow-up

- **Alexandrov et al. 2020** (COSMIC v3 signatures repertoire) — companion reference for the COSMIC matching; hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and positive-control arms build on that catalog.
- **Degasperi et al. 2022** (Signature Fit Multi-Step) — improved signature refitting methodology relevant to per-sample assignment on cBioPortal data.
- **Kucab et al. 2019** — mutational signatures of environmental agents; complement to the therapy-associated signatures here.
- The therapy-associated signatures (SBS31, SBS17b, ID8, DBS5) should be checked as potential confounders in the `is_hypermutator` annotation pipeline (task t081); long-treated patients may exceed TMB thresholds not due to DDR/MSI but due to chemotherapy-induced mutagenesis.
- MSBS6 (UV-independent melanoma), MSBS3 (pancreatic/stomach), and MSBS5 (T>G, T>C, unknown) are candidate targets for the hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and discovery prong: no COSMIC match → agnostic covariate scan.
