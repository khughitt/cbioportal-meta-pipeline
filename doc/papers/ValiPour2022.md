---
id: "paper:ValiPour2022"
type: "paper"
title: "The impact of rare germline variants on human somatic mutation processes"
status: "active"
ontology_terms: []
datasets: []
source_refs:
  - "cite:ValiPour2022"
related: []
created: "2026-05-31"
updated: "2026-05-31"
---

# The impact of rare germline variants on human somatic mutation processes

- **Authors:** Mischan Vali-Pour, Solip Park, Jose Espinosa-Carrasco, Daniel Ortiz-Martínez, Ben Lehner, Fran Supek
- **Year:** 2022
- **Journal:** Nature Communications
- **DOI/URL:** https://doi.org/10.1038/s41467-022-31483-1
- **BibTeX key:** ValiPour2022
- **Source:** PDF

## Key Contribution

Vali-Pour et al. perform the largest gene-based rare-variant association study (RVAS) to date linking inherited rare putative loss-of-function (pLoF) germline variants to somatic mutational processes in human tumors. Testing 891 candidate genes across ~11,000 individuals (TCGA discovery; PCAWG + Hartwig validation), they identify 207 replicated associations spanning 42 genes and 15 somatic mutational phenotypes at a 1% FDR. The study demonstrates that rare germline variation in a diverse, networked set of DNA repair and chromatin-modifying genes — many beyond well-known cancer predisposition genes — substantially shapes the somatic mutation landscape.

## Methods

**Data.** Somatic mutations were extracted from ~9,300 WES (TCGA; discovery) and ~5,500 WGS (PCAWG + Hartwig; validation) European-ancestry cancer genomes. 56 somatic mutational features were quantified per tumor, covering SBS signatures (organ-specific, via SigProfilerMatrixGenerator), DBS signatures, insertion/deletion signatures, copy-number signatures, transcription strand bias, replication strand bias, chromatin features (H3K36me3, DNase I, CTCF-binding sites), replication timing, expression levels, X-chromosomal hypermutation, and mitochondrial genome mutations.

**Dimensionality reduction.** Two complementary methods were applied to derive 29 orthogonal mutational components: independent component analysis (ICA; 15 components) and a variational autoencoder (VAE; 14 components). These components reduce feature correlation and serve as the association phenotypes; components were named by their strongest input feature correlate.

**Germline variant prioritisation.** Rare (MAF < 0.1%) pLoF variants were defined under five schemes: (i) PTVs only, (ii) PTVs + missense CADD ≥ 25, (iii) PTVs + missense CADD ≥ 15, (iv) missense with MTR ≤ 25th percentile, (v) missense in constrained coding regions (CCR ≥ 90th percentile). Testing used three inheritance models (dominant, additive, recessive), yielding 15 models tested per gene.

**Statistical testing.** Gene-based testing used SKAT-O, a combined burden + variance-component (SKAT) test on 891 candidate genes (DNA repair, replication, chromatin modifiers). Empirical FDR was estimated by randomisation. Discovery hits in TCGA were re-tested in the matched cancer type from the validation cohort (PCAWG + Hartwig). 594,462 total tests were run in the discovery phase.

**Network analysis.** Physical protein–protein interactions from STRING (combined score ≥ 80%) and HumanNet were used to validate the functional clustering of identified genes.

## Key Findings

1. **Scale and replication.** 207 associations replicated at 1% FDR, covering 42 genes, 15 mutational components, 46 unique gene–cancer-type pairs, and 65 unique gene–cancer-type–component combinations. An additional 149 associations replicated at a more permissive 2% FDR.

2. **dHR (deficient homologous recombination).** 57% of replicated hits (117/207) involved *BRCA1*, *BRCA2*, or *PALB2* with multiple dHR-related components (deletions at microhomology-flanked sites, SNV SBS3). Beyond these known genes, skin-cancer associations were found for *PAXIP1*, *EXO1*, and *RIF1* with dHR-linked components.

3. **dMMR (deficient mismatch repair).** *MLH1* and *MSH2* associated with classical dMMR components (small indels at microsatellites, SBS MMR1), consistent with Lynch syndrome. *MSH3* specifically associated with a distinct dMMR phenotype enriched in ≥2 nt indels — a MSH3-specific form not involving a large increase in SNV rates.

4. **MTOR and chromatin modifiers.** *MTOR* associated with dMMR components in multiple cancers via a proposed mechanism of MSH2 destabilisation. *SETD2* associated with dMMR at 2% FDR in colorectal cancer. *TRAAP* (ovarian) and *SETD1A* (breast) also implicated.

5. **APEX1 / APOBEC.** *APEX1* variants associated with three mutational components including an APOBEC mutagenesis component (APOBEC_VAE2), implicating the AP endonuclease in APOBEC-signature accumulation via error-prone translesion synthesis past unrepaired abasic sites.

6. **Variant pathogenicity inflation.** Most hits replicated via the SKAT variance component (ρ < 0.5), indicating that in silico pathogenicity predictors include non-causal variants; the variance test partially compensates for predictor inaccuracy.

7. **Network enrichment.** Identified genes were significantly more physically interconnected than random gene sets of the same size (p = 0.002 for FDR 1% genes), supporting a network view of mutational process control.

8. **Population prevalence.** Damaging variants in the discovered genes are about as prevalent in cancer patients as in the general gnomAD population, suggesting broad population-level relevance.

## Relevance

**Direct relevance to h08 (agnostic covariate↔signature-exposure association).**

This paper is a germline-RVAS analogue of h08's agnostic-association concept. Where h08 targets somatic covariates (expression modules, clinical fields) vs. signature exposures, Vali-Pour et al. target *germline* rare pLoF variants vs. somatic mutational components. Several connections matter:

- **Positive-control concordance.** The study recovers known exposure→signature links — dHR ↔ SBS3/microhomology deletions, dMMR ↔ MMR1/indels, APOBEC exposure ↔ SBS13 — using an agnostic multi-phenotype scan. This is exactly the type of positive-control recovery h08 proposes to validate before trusting novel hits. The success of the germline scan strengthens the argument that the same signal is detectable in somatic data.

- **APOBEC3 / APEX1 axis.** The finding that *APEX1* germline variants associate with APOBEC signature components supports the mechanistic chain between base-excision repair efficiency and APOBEC mutagenesis. For h08, this implies that APOBEC3A/B *expression* levels (targeted in h08 Prediction 2) have a plausible upstream mechanism — APEX1 activity modulates the abasic-site substrate that APOBEC acts on.

- **MSH3-specific dMMR phenotype.** The two-form MMR distinction (MSH2/MLH1 → SNV+indel; MSH3 → indel-only) provides a refined mutational-component taxonomy for h08: the project's dMMR signature extraction should resolve these two subtypes, and the h08 scan should find that within-cancer expression of *MSH3* vs *MSH2* differentially tracks these components.

- **Methodological parallels.** The paper's use of dimensionality reduction (ICA + VAE) to construct orthogonal mutational phenotypes, followed by multi-model testing with FDR control, closely parallels the planned h08 association pipeline. Their demonstration that ICA and VAE are complementary (different genes discovered by each) motivates using both in h08.

- **Network/pathway signal.** The enrichment of hits within PPI networks implies that germline mutations in support genes (regulators of BRCA1, MSH2, etc.) alter the same signatures as the canonical drivers. For h08, this suggests that expression modules of these networks (not just the canonical mutator genes) may serve as robust signature predictors.

**Relevance to cross-study somatic mutation meta-analysis.** The paper uses TCGA WES (consistent with the cbioportal pipeline's primary input) and identifies that the power to detect these associations is sensitive even to small reductions in sample size. This motivates aggregating across cBioPortal studies — the larger the effective N per cancer type, the more of this signature-germline (and by extension signature-somatic-covariate) landscape becomes statistically accessible.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Somatic mutational components (ICA / VAE derived) | Signature exposures (SigProfiler refitting output `H`) | Paper extracts de-novo components from mutation features; h08 uses pre-defined COSMIC reference |
| dHR components (dHR_ICA, dHR_VAE) | SBS3 / ID6 signature exposures | Microhomology-deletion enrichment is the key dHR feature |
| dMMR components (dMMR_ICA, dMMR_VAE) | SBS6/15/26/MMR1 + ID1/2 | Small indels at microsatellites are the key dMMR feature |
| APOBEC_VAE2 component | SBS2 / SBS13 exposure | C>G at non-CpG sites as APOBEC signature 13 proxy |
| SKAT-O gene-based burden+variance test | (not currently in pipeline) | h08 uses sample-level covariates; different association layer |
| 15 mutational models (3 inheritance × 5 variant sets) | Not applicable (somatic covariates, not germline) | Analogy: multiple pLoF models ↔ multiple covariate types |
| FDR by randomisation of somatic component matrix | Planned FDR-controlled association for h08 | Same principle — permute the outcome label |

## Limitations

- **European ancestry only.** The analysis was restricted to individuals of European ancestry, limiting generalisation to populations with different germline variant landscapes.
- **WES discovery.** TCGA WES samples cover only ~2% of the genome; features requiring whole-genome context (replicative strand asymmetry, CTCF enrichments) had reduced power in the discovery cohort.
- **Low recessive-model power.** Only 4% of tests used the recessive model because biallelic pLoF events are rare; many haplo-insufficient DNA repair genes are under-detected.
- **Variant pathogenicity predictors.** Most validated hits depended on the variance component of SKAT-O, reflecting substantial non-causal contamination in the missense pLoF sets. Better predictors would increase power and allow burden-test recovery.
- **Germline ≠ somatic covariate.** The identified germline determinants explain inter-individual variation, but within-individual somatic signature levels also reflect stochastic and environmental processes not captured here.
- **No non-European ancestry.** Multi-ancestry analyses would increase power and allow generalisation across populations.

## Model / Tool Availability

- Code for the association analysis: https://github.com/lehner-lab/RDGVassociation
- Interactive data visualisation: https://mischanvhu.shinyapps.io/rare_association_shiny/
- Data: TCGA WES from dbGaP (phs000178); PCAWG/Hartwig from ICGC DACO / Hartwig Medical Foundation (restricted access)

## Follow-up

- **For h08:** replicate the APOBEC3A/B expression → SBS2/13 recovery in the cBioPortal pipeline; use the paper's ICA/VAE component definitions as a reference for what "APOBEC" and "dMMR" signatures should look like in agnostic extraction.
- **MSH3 phenotype:** check whether the pipeline's dMMR extraction resolves the MSH3-specific ≥2 nt indel component from the MLH1/MSH2 SNV+indel component.
- **APEX1 mechanism:** the paper motivates adding *APEX1* expression as a candidate covariate in the h08 scan alongside APOBEC3A/B expression.
- **Network view of signatures:** consider whether PPI-network modules (e.g. HR network, MMR network) can be used as composite covariate features for h08, rather than single-gene expression levels.
- Papers to read: Levatic 2022 (mutational signatures as drug-sensitivity markers, already in `doc/papers/`); Park et al. 2023 on germline cancer predisposition (already in `doc/papers/`).
