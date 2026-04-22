---
id: "paper:Yaacov2023"
type: "paper"
title: "Mutational signatures association with replication timing in normal cells reveals similarities and differences with matched cancer tissues"
status: "active"
ontology_terms: []
datasets:
  - SomaMutDB
  - PCAWG
source_refs:
  - "paper:Yaacov2023"
related:
  - "paper:Yoshida2026"
  - "topic:mutation-rate-normalization"
  - "topic:pan-cancer-mutation-landscape"
created: "2026-04-18"
updated: "2026-04-18"
---

# Mutational signatures association with replication timing in normal cells reveals similarities and differences with matched cancer tissues

- **Authors:** Adar Yaacov, Shai Rosenberg, Itamar Simon
- **Year:** 2023
- **Journal:** Scientific Reports
- **DOI:** 10.1038/s41598-023-34631-9
- **PMCID:** PMC10185532
- **BibTeX key:** Yaacov2023
- **Source:** Europe PMC full-text XML (retrieved via science-tool paper-fetch, status: ok)

## Key Contribution

The first comprehensive analysis of the association between mutational signatures and DNA replication timing (RT) specifically in non-cancerous tissues. Using 2.9 million somatic mutations from 25 published datasets spanning multiple normal tissue types, the authors show that most mutational processes have the same RT bias (early vs. late replicating region enrichment) in normal cells as in matched cancer samples — establishing that the relationship between mutagenesis and replication timing is largely conserved through carcinogenic transformation. The key exception is SBS1 (clock-like CpG deamination): SBS1 is preferentially enriched in late-replicating regions (LRR) in normal tissues but loses this bias in cancer, likely due to increased mutation burden and CpG island methylation changes during transformation.

## Methods

**Data:** Somatic mutations in non-cancerous cells drawn from two independent sources: (1) SomaMutDB (2.42 million SNVs from 24 published papers spanning 19 tissue types / 2838 single cells/clones/biopsies) and (2) Moore et al. (2022) pan-tissue WGS dataset from 389 patches of 29 histological structures. Cancer mutations from PCAWG (Pan-Cancer Analysis of Whole Genomes). Final cohort: 1,192 samples (Mixed cohort) + 176 samples (Moore et al.) passing QC.

**Replication timing regions:** Used constitutive RT regions — genomic regions (~40% of the genome; ~706 Mb early-replicating + 583 Mb late-replicating) showing consistent RT across 26 cell types. This minimizes confounding from cell-type variation in RT.

**Signatures:** Trinucleotide profiles extracted using SigProfilerMatrixGenerator; signatures extracted by NMF via SigProfilerExtractor (v1.14) and decomposed against COSMIC v3.2 SBS signatures. Minimum: 50 SBS events in each of ERR and LRR; cosine similarity ≥ 80% to reconstructed profile. Results cross-validated using deconstructSigs.

**RT bias metric:** Delta = relative signature contribution in early replicating regions (ERR) minus LRR. Positive = ERR-biased; negative = LRR-biased. Normalized absolute delta used for germline analysis. Two-sided Wilcoxon rank-sum test with FDR correction.

**Normal-vs-cancer comparison:** Four matched tissue-cancer pairs from PCAWG: colon/COAD, hepatocytes/HCC, lung/NSCLC, melanocytes/melanoma. Cancer samples processed identically to normal cells.

## Key Findings

### RT biases in normal cells (pan-tissue)

| Signature | RT bias | Etiology |
|---|---|---|
| SBS1 | LRR (late) | Clock-like CpG deamination (aging) |
| SBS5 | ERR (early) | Clock-like replication errors (aging) |
| SBS7b | ERR | UV exposure (C>T at TpC) |
| SBS16 | ERR (exclusively) | Unknown; appears only in ERR in hepatocytes |
| SBS40 | ERR | Unknown |
| SBS88 | ERR | Colibactin (E. coli pks+ genotoxin) — first reported RT bias for this signature |
| SBS4 | LRR (exclusively) | Tobacco smoking — appears only in LRR in lung/hepatocytes |
| SBS7a | LRR | UV exposure |
| SBS8 | LRR | Unknown |
| SBS18 | LRR | Reactive oxygen species (ROS) |

Additional tissue-specific findings: APOBEC-related SBS2 and SBS13 are ERR-biased in lung and urothelium; SBS9 and SBS84 are LRR-biased in blood cells and bone marrow respectively.

Concordance between the two independent cohorts (Mixed vs. Moore et al.) was high: R = 0.967 (P < 3×10⁻⁷). Cross-validation with deconstructSigs gave R = 0.974.

### Normal vs. cancer: mostly conserved, SBS1 as exception

For 4 matched tissue-cancer pairs, the RT bias direction was consistent between normal and cancer for SBS5, SBS40, SBS7a/b, SBS2/13, SBS4, SBS8, SBS16, and SBS18.

The single major exception: **SBS1 is LRR-biased in normal tissues but loses this bias in cancer** (both pan-tissue and in each of the 4 tissue-specific comparisons). The change is statistically significant in absolute terms (P < 2.2×10⁻¹⁶, Wilcoxon rank-sum), while SBS5's ERR bias is preserved (P = 0.23 for normal-vs-cancer delta difference).

Proposed mechanisms for the SBS1 RT bias loss in cancer:
1. Increased SBS1 mutations at CpG islands (which are ERR-enriched) in cancer cells — observed for liver and lung.
2. Impaired base excision repair (BER) in cancer during ERR replication (faster cycles → less functional TGD/MBD2 in ERR), eliminating the repair-efficiency gradient.
3. CEBPβ binding at G:T mismatches inhibiting repair (Yang et al. mechanism) — likely a minor contributor only, given few SBS1 mutations originate from CCAAT sites.

A milder secondary finding: SBS7b is slightly more ERR-biased in normal vs. cancer cells, suggesting additional lower-magnitude changes beyond SBS1.

### Germline cell comparison

Testis (germline-cell-enriched) samples from Moore et al. — only SBS1 and SBS5 found. Both show the same RT bias as somatic tissues (SBS1 → LRR; SBS5 → ERR), indicating the RT mutagenesis mechanisms predate and are independent of somatic evolutionary selection. Absolute-delta analysis confirms SBS1 is LRR-dominant (P = 0.0009 SBS1 vs. SBS5 comparison).

## Relevance

This paper has three layers of relevance to the cbioportal pipeline:

**1. Replication timing as a source of gene-level mutation rate variation (direct confound)**
Late-replicating regions accumulate more somatic mutations overall. Genes located in LRR will appear more frequently mutated in cross-study aggregation tables, independent of selection pressure. The pipeline aggregates mutation counts per gene but does not currently normalize for gene-level RT. Genes like TP53 (often in variable-RT regions) and KRAS (ERR) have intrinsically different background mutation rates partly attributable to RT. This paper provides the empirical signature-RT mapping needed to reason about which gene-cancer associations in our outputs could be inflated by LRR positioning rather than positive selection.

**2. SBS1 behavior provides a normal-tissue calibration signal**
SBS1 (clock-like, age-correlated) is LRR-biased in normal cells but not in cancer. Since our pipeline combines cBioPortal studies with variable tumor purity and mixed sequencing methods, any dataset with residual normal-cell contamination will show an SBS1 LRR bias that should be absent from pure tumor data. The loss of SBS1 LRR bias could serve as a computational purity indicator or contamination screen — studies showing SBS1 with a LRR skew may contain significant normal-tissue admixture.

**3. SBS88 (colibactin) exclusively ERR in normal colon — implications for colon cancer studies**
SBS88 appears exclusively in ERR in normal colorectal crypts. Since ERR regions are gene-dense and transcriptionally active, colibactin-induced mutations in normal cells preferentially hit genes in active chromatin. This is mechanistically relevant to interpreting colorectal cancer gene-frequency outputs: SBS88-attributable background mutations in the pipeline's CRC aggregations will have a non-random genomic distribution skewed toward gene-rich regions, potentially inflating apparent mutation rates for certain ERR-resident cancer genes in colibactin-exposed populations.

**Relationship to Yoshida2026:** Yoshida's review identifies SBS88 in normal colorectal crypts as a potential cancer risk factor; this paper provides the mechanistic detail that SBS88 is ERR-restricted, tying the environmental exposure to specific genomic targeting. Together they strengthen the case that colibactin-driven normal-cell mutation is not uniformly distributed and could confound CRC mutation-frequency tables in a gene-position-dependent way.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| ERR/LRR enrichment of signatures | Gene-level background mutation rate | Not currently in pipeline; RT annotation could be added as a per-gene covariate |
| SBS1 LRR bias in normal vs. no bias in cancer | Normal-cell contamination indicator | Detectable in aggregate if enough mutations; likely below resolution at individual study level |
| SBS4 exclusively LRR in lung | Tobacco-related CRC/lung background inflation | Genes in LRR will show tobacco-inflated rates in lung studies |
| SBS88 exclusively ERR in normal colon | Colibactin signal in CRC gene-frequency | Enriches mutation rates for ERR-resident genes specifically |
| Constitutive RT regions (40% genome) | Candidate normalization strata | If per-gene RT annotation added, these regions are more reliable than variable RT |
| Normal-vs-cancer signature conservation | Background model robustness | Most signatures preserve RT bias — supports using normal-tissue signature studies to inform cancer background models |

## Limitations

- Analysis restricted to ~40% of the genome (constitutive RT regions only); signatures in variable-RT regions, which may differ between tissue types, are excluded. This is methodologically conservative but means the results may not generalize to all genes.
- Sample counts for non-common tissues are small — tissue-specific RT biases (e.g., SBS9/SBS84 in blood/bone marrow) are based on limited samples. Only tissues with ≥15 samples are shown in the main heatmap.
- The comparison uses PCAWG whole-genome cancers but most cBioPortal studies are panel/WES — panel data will detect far fewer mutations per sample, reducing power to resolve RT biases per-study. The population-level finding (SBS1 LRR loss in cancer) is not actionable per-study in the pipeline without aggregating many samples.
- The paper does not provide quantitative per-gene RT annotations or effect sizes at gene resolution; it operates at the signatures-vs-broad-RT-region level. Applying these findings to specific genes in the pipeline would require linking gene chromosomal positions to the constitutive RT annotation used in this study.
- The proposed mechanisms for SBS1 RT bias loss (CpG island changes, BER impairment) are plausible but not definitively proven; the authors acknowledge the discrepancy with Moore et al. (2022) which found mostly LRR enrichment for all signatures, attributing it to methodological differences.

## Model / Tool Availability

- Data: SomaMutDB (https://compgenomics.weizmann.ac.il/SomaMutDB/) and PCAWG. Code and constitutive RT region annotations not described as a standalone release but methods reference Yaacov et al. 2022 (prior cancer-RT paper, ref [9]) for the RT region construction.
- No standalone software tool released with this paper.

## Follow-up

- Read Yaacov et al. 2022 (the companion cancer-only RT-signatures paper, ref [9] in this study) to understand the complete ERR/LRR signature map in cancer — this paper directly extends that prior work to normal cells.
- Read Moore et al. 2022 (ref [15]) — the pan-tissue WGS dataset underlying the Moore et al. cohort used here; their RT analysis methodology differs and may complement.
- Investigate whether gene-level constitutive RT annotations (from the ENCODE RT data used by Yaacov) could be added as a covariate to the pipeline's gene × cancer frequency tables — even a binary ERR/LRR flag per gene would allow post-hoc stratification.
- Assess whether the SBS1 LRR-bias metric could be computed per cBioPortal study as a quality/purity indicator; studies with residual normal-cell content (e.g., endoscopic biopsies) might show a detectable SBS1 LRR enrichment.
- Consider whether SBS88-attributable mutations in CRC studies (identifiable via trinucleotide profile) disproportionately affect specific ERR-resident driver candidates in the pipeline's colon outputs.
