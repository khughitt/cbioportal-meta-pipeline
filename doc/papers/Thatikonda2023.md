---
id: "paper:Thatikonda2023"
type: "paper"
title: "Comprehensive analysis of mutational signatures reveals distinct patterns and molecular processes across 27 pediatric cancers"
status: "active"
ontology_terms:
  - mutational signatures
  - SBS signatures
  - indel signatures
  - pediatric cancer
  - NMF
  - COSMIC v3
  - whole-genome sequencing
  - homologous recombination deficiency
datasets: []
source_refs:
  - "cite:Thatikonda2023"
related: []
created: "2026-05-31"
updated: "2026-05-31"
---

# Comprehensive analysis of mutational signatures reveals distinct patterns and molecular processes across 27 pediatric cancers

- **Authors:** Venu Thatikonda, S. M. Ashiqul Islam, Robert J. Autry, Barbara C. Jones, Susanne N. Grobner, Gregor Warsow, Barbara Hutter, Daniel Huebschmann, Stefan Frohling, Marcel Kool, Mirjam Blattner-Johnson, David T. W. Jones, Ludmil B. Alexandrov, Stefan M. Pfister, Natalie Jager
- **Year:** 2023
- **Journal:** Nature Cancer
- **DOI/URL:** https://doi.org/10.1038/s43018-022-00509-4
- **BibTeX key:** Thatikonda2023
- **Source:** PDF

## Key Contribution

This study provides the largest systematic COSMIC v.3 mutational-signature analysis of pediatric cancers to date, examining SBS and indel (ID) signatures across 785 whole-genome sequenced tumor-normal pairs from 27 molecularly defined childhood cancer subtypes. Pediatric tumors harbor far fewer active mutational processes than adult cancers, with clock-like signatures (SBS1, SBS5, ID1, ID2) dominating a large fraction of mutations across cancer types. A novel indel signature termed "IDN" was discovered exclusively in pediatric leukemias (B-ALL, AML, T-ALL), characterized by long insertions (>1 bp) outside repeat regions that preferentially affect intronic and intergenic regions but also exons of known cancer genes such as NOTCH1.

## Methods

- **Cohort:** 785 WGS tumor-normal pairs from the PedPanCan PPC-WGS cohort, spanning 27 molecularly defined pediatric cancer entities. Supplemented with 149 St. Jude Cloud samples and 5 INFORM whole-genome sequenced tumors with known BRCA1/2 germline mutations.
- **Mutation calling:** Consensus somatic variant calling using DKFZ in-house pipeline (updated BWA-MEM + SAMtools) plus mutect2; variants intersected ("bedtools intersect") to produce a consensus call set. SBS mutations called at 96 trinucleotide context; ID mutations at 83-context catalogs.
- **Signature extraction:** Three methods applied in parallel:
  1. SigProfilerExtractor (NMF-based, SBS96 and ID83 catalogs; k = 1 to 10, 500 random initializations per k; stability criterion ≥ 0.80);
  2. SignatureAnalyzer (Bayesian ARD-NMF; SBS1536 + ID83 composite COMPOSITE spectra);
  3. HDP (hierarchical Dirichlet process, non-NMF; applied specifically to leukemia cohort for ID signatures).
- De novo signatures decomposed into COSMIC v.3 reference set using NNLS (minimum cosine similarity 0.85 for SBS, 0.80 for ID). Signatures validated across two independent methods for robustness.
- **Association analyses:** Linear regression of signature activity against TP53 mutation status, chromothripsis, and age at diagnosis, with cancer type as covariate; Benjamini-Hochberg FDR correction. Spearman correlations for continuous covariates.
- **Strand asymmetry:** SigProfilerMatrixGenerator + SigProfilerTopography; transcription- and replication-strand asymmetries evaluated per signature per cancer type (100 simulations, Fisher exact test, BH adjusted p < 0.05).
- **HRD classification:** CHORD (v2.0; random-forest classifier trained on >5,000 WGS tumors) applied to PPC-WGS (n = 599) and INF-WGS (n = 5) cohorts.
- **Chromothripsis detection:** ShatterSeek (default parameters) for newly added tumors; Grobner et al. annotations reused for overlapping samples.
- **Germline:** 162 cancer-predisposition genes screened; stepwise filtering using dbSNP v.141, 1000 Genomes, gnomAD, ClinVar, CADD ≥ 15, MutationAssessor; TP53 and BRCA1/2 flagged for signature association.

## Key Findings

**Scale and signature repertoire:**
- 29 SBS signatures and 10 ID signatures identified across the 27 cancer types (vs. >40 SBS and 17 ID signatures found in adult pan-cancer analyses), confirming that pediatric tumors operate with a smaller active mutational process repertoire.
- SBS1 and SBS5 (clock-like) present in 98.2% and 96.6% of samples across the cohort, respectively. ID1 and ID2 (replication slippage/clock-like) most prevalent ID signatures.
- 41.7% of SBS mutations and 42.8% of ID mutations in non-hypermutated samples attributed to clock-like signatures; 87% and 100% of ID mutations in hypermutated samples attributed to clock-like processes.

**APOBEC (SBS2/SBS13):**
- Restricted in this cohort to adrenocortical carcinoma (ACC), Ewing sarcoma (ES), high-grade glioma (HGG K27M), and osteosarcoma. Activity significantly elevated in TPS53-mutated tumors compared with wildtype, consistent with p53 modulation of APOBEC3B expression.

**UV signatures (SBS7a/SBS7b):**
- Identified exclusively in hypodiploid B-cell acute lymphoblastic leukemia (B-ALL-HYPO). CC>TT doublet base substitutions significantly elevated. Mechanism unclear — may be genuine UV exposure or biochemical mimic.

**HR defect signatures (SBS3/ID6 = SBS3 in COSMIC v.2):**
- COSMIC v.3 SBS3 active in only 2.29% of tumors (vs. 54% with Signature.3 COSMIC v.2) — major reduction attributed to the "flattening" of v.3 signatures. SBS3 activity without complementing ID6 in most tumors. The single INF-WGS tumor with biallelic homozygous BRCA2 inactivation was the only one showing both SBS3 and ID6 activity. CHORD HRD probability high only for this tumor. Pediatric tumors have very few MH-associated long deletions overall compared with adult cancers.
- Signature.P1 (a pediatric-specific signature from prior COSMIC v.2 analysis) reinterpreted here as a mixture of SBS31 + SBS35 (both platinum treatment-associated; cosine similarity of reconstruction = 0.99), explaining its occurrence in treatment-naive relapsed tumor samples.

**Novel IDN indel signature:**
- Identified exclusively in pediatric leukemias (B-ALL subtypes, AML, T-ALL) using three independent methods (SigProfiler, SigAnalyzer, HDP) with high concordance (cosine similarities 0.81-0.98 between methods).
- Characterized by elevated insertions >1 bp at non-repeat regions. Strongly correlated with SBS1 (Spearman r = 0.77) and SBS40 (r = 0.38), suggesting clock-like behavior. Enriched in first introns, other introns, and distal intergenic regions (32.6%); also coding exons of known cancer genes (NOTCH1, PHF6). Not previously reported in COSMIC v.3.
- Confirmed not to be alignment/calling artifact by IGV inspection.

**ROS signature (SBS18):**
- Active in 17 of 27 cancer types; highest fractions in neuroblastoma (90%) and rhabdomyosarcoma (83.3%). No association found with MYCN amplification in neuroblastoma (contrary to some prior reports), possibly due to small sample size.

**Chromothripsis and SBS8/SBS40:**
- SBS8 activity significantly higher in chromothripsis-positive tumors. SBS40 highly correlated with structural variant count (Spearman r = 0.41, p = 1.7e-25), suggesting genomic rearrangement mechanisms contribute to both signatures.

**Strand asymmetries:**
- Transcriptional strand asymmetry observed for SBS5 (T>C enrichment on transcribed strand in multiple cancer types), SBS7a (C>T on untranscribed strand in B-ALL-HYPO), SBS31/SBS35 (T>C on transcribed strand), and SBS15 (C>T leading-strand enrichment in HGG). Replication strand asymmetry for SBS5 (lagging strand T>C), SBS15 (leading C>T in HGG), and SBS44 (leading strand in Group4 MB).

**SBS9 (polymerase eta):**
- Restricted to Burkitt lymphoma and DLBLNOS; activity correlated with IGHV mutation status, consistent with AID-driven somatic hypermutation context.

## Relevance

**h08 (agnostic covariate-signature exposure association; positive-control recovery):**

This paper is directly relevant as a positive-control reference catalog for h08. Key points:

1. **Age at diagnosis** is confirmed as a significant covariate for multiple signatures in pediatric cancers (SBS1, SBS5, SBS40 positively correlated with age; ID1, ID2, ID9 show clock-like age behavior). The linear regression framework used here (signature activity ~ exposure + cancer_type + age) is a worked example of within-cancer-type covariate association — structurally identical to the h08 agnostic association model.

2. **TP53 mutation status** associates with APOBEC signatures (SBS2 elevated in germline TP53 mutants; p_adj = 0.011) and SBS8 (chromothripsis-positive tumors enriched with SBS8). These represent clinical-genomic covariate associations analogous to what h08 aims to systematically recover.

3. **Chromothripsis** (a structural variant-derived binary covariate) associates with SBS8 and SBS40, demonstrating that derived molecular features beyond mutation counts can drive signature differences — exactly the type of signal h08 wants to surface agnostically.

4. **Known aetiologies (positive controls for h08):** UV (SBS7a/b) confined to B-ALL-HYPO; APOBEC (SBS2/13) in ACC/ES/HGG/OS; clock signatures (SBS1/5) universal; HR-defect (SBS3/ID6) requiring biallelic BRCA1/2 loss; platinum treatment (SBS31/SBS35). These provide ground-truth aetiology-covariate linkages that h08's agnostic scan should recover.

5. **Signature complexity in pediatric vs. adult cancer:** Fewer active signatures in pediatric tumors means that agnostic scans on pediatric cohorts (should any cBioPortal studies include pediatric cancer) would face a lower-dimensional signature space, potentially aiding covariate recovery but limiting power for rarer signatures.

6. **IDN leukemia-restricted signature** illustrates how a novel process can emerge from agnostic extraction without a COSMIC prior; its cancer-type restriction and correlation with known clock signatures (SBS1, SBS40) are the kind of structured pattern an association analysis would surface.

**Cross-study meta-analysis context:** The paper demonstrates that signature activity is highly correlated across independent extraction methods (NMF / Bayesian ARD-NMF / HDP), supporting robustness of signature decomposition. The finding that pediatric tumors carry very few MH-associated deletions relative to adult tumors is relevant for any cross-study pipeline comparing pediatric and mixed-age cBioPortal cohorts.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| SigProfilerExtractor NMF extraction | Signature decomposition step (downstream of cross-study aggregation) | q018/q019 ask whether to add this |
| SBS/ID signature activity per tumor | Per-sample signature exposure vector H | Outcome variable in h08 association model |
| TP53 mutation status, chromothripsis | Structured clinical/molecular covariate | Positive-control covariate for h08 agnostic scan |
| Age at diagnosis | Clinical covariate (age) | Already present as a cBioPortal field in the pipeline |
| COSMIC v.3 reference signatures | COSMIC v.3 reference catalog | Same reference; project uses same version |
| IDN (novel pediatric leukemia indel) | Novel de novo signature not in COSMIC | Example of what agnostic extraction might surface |
| Cancer type as regression covariate | within-cancer-type stratification | h08 applies within-tissue stratification to avoid confounding |
| Strand asymmetry analysis | Mechanistic validation | Not part of core pipeline, but relevant for signature interpretation |

## Limitations

- **Pediatric-only scope:** All 785 tumors are from children/adolescents (<25 years). Adult signatures (tobacco, UV in melanoma, microsatellite instability in colorectal) are absent or minor, limiting generalizability to adult-dominant cBioPortal studies. Cross-study translation of the IDN signature requires confirmation in adult leukemia cohorts.
- **WGS only, no exome-seq:** Signature decomposition requires trinucleotide context counts; exome-based studies in the cBioPortal pipeline cannot use these signatures directly without panel/exome normalization.
- **Low indel counts per tumor:** Very low ID mutation burden in most pediatric tumors limits statistical power for ID signature decomposition; the authors acknowledge that even longer IDN insertions (>5 bp) are likely missed by short-read WGS.
- **Hypothesis-driven associations only:** Association analyses were targeted to TP53, chromothripsis, and age — selected based on prior biological knowledge. An agnostic phenome-wide scan (as proposed in h08) was not performed.
- **SBS3 reclassification caveat:** The dramatic drop in SBS3 frequency from COSMIC v.2 to v.3 (54% to 2.29%) raises a method-sensitivity concern: flat background signatures (SBS5, SBS40) can absorb activity previously attributed to HR-defect signatures, making it difficult to confidently exclude HRD in tumors without biallelic BRCA1/2 hits.
- **No matched adult comparison cohort from the same variant-calling pipeline**, making comparisons to adult PCAWG data indirect.

## Model / Tool Availability

- **SigProfilerMatrixGenerator** (v1.2.4): https://github.com/AlexandrovLab/SigProfilerMatrixGenerator
- **SigProfilerExtractor** (v1.1.7): https://github.com/AlexandrovLab/SigProfilerExtractor
- **SignatureAnalyzer** (v0.0.8): https://github.com/getzlab/SignatureAnalyzer
- **deConstructSigs** (v1.9.0): https://github.com/raerose01/deconstructSigs
- **SigProfilerTopography** (v1.0.63): https://github.com/AlexandrovLab/SigProfilerTopography
- **CHORD** (v2.0): https://github.com/UMCU-Genetics/CHORD
- **ShatterSeek** (v1.1): https://github.com/parklab/ShatterSeek
- **Manuscript analysis code + tutorial:** https://github.com/KiTZ-Heidelberg/Signatures-Manuscript
- All analyses: Python 3.7.3 or R 4.0.5. Open Access (CC BY 4.0).

## Follow-up

- **IDN signature in adult leukemias:** Degasperi et al. 2022 (Sci. Adv.) studied UK Biobank adult cancers including CLL; no IDN equivalent reported. Brady et al. 2022 (Nat. Genet.) analyzed ALL genomic landscape without flagging IDN. Warrants checking whether IDN is truly pediatric-restricted or missed in adult studies due to indel calling limitations.
- **Signature.P1 / SBS31+SBS35 connection to ETMR:** This paper re-classifies the pediatric-specific Signature.P1 as cisplatin treatment artifacts — relevant for any pediatric cohort in cBioPortal that includes relapsed/treated tumors.
- **APOBEC-TP53 link:** Association between germline TP53 loss and elevated SBS2 is consistent with p53 suppressing APOBEC3B. In h08, TP53 mutation frequency (available in cBioPortal) could serve as a positive-control covariate for APOBEC signature recovery.
- **SBS40 and structural variants:** Strong correlation suggests that structural variant count (if computable from cBioPortal) could serve as a covariate predictor of SBS40 exposure in the h08 agnostic framework.
- Relevant companion paper: Grobner et al. 2018 (Nature 555, 321-327) — the initial PedPanCan landscape paper that established the PPC-WGS cohort.
