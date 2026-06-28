---
type: paper
title: Mutational signature SBS8 predominantly arises due to late replication errors
  in cancer
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: paper:Singh2020
ontology_terms:
- mutational signatures
- SBS8
- DNA replication
- epigenomics
- heterochromatin
- cancer genomics
datasets: []
source_refs:
- cite:Singh2020
related: []
---

# Mutational signature SBS8 predominantly arises due to late replication errors in cancer

- **Authors:** Vinod Kumar Singh, Arnav Rastogi, Xiaoju Hu, Yaqun Wang, Subhajyoti De
- **Year:** 2020
- **Journal:** Communications Biology, 3:421
- **DOI/URL:** https://doi.org/10.1038/s42003-020-01119-5
- **BibTeX key:** Singh2020
- **Source:** PDF

## Key Contribution

SBS8 — a common but mechanistically unresolved COSMIC mutational signature — is shown through systematic epigenomic and replication-timing analysis to arise predominantly from uncorrected replication errors in late-replicating heterochromatin domains during cancer progression. The authors develop a genome-wide Hidden Markov Model-based "mutagenesis-related epigenomic" (MRE) composite context framework that integrates chromatin state, nuclear localization, and replication timing, and use it to show that SBS8 burden rises monotonically with both replication lateness and speed in tumor genomes across 18 ICGC cancer cohorts. SBS8 is nearly absent from germline de novo mutations and non-malignant somatic tissues, accumulates with pathological stage, and is elevated in tumors with checkpoint defects (low CHEK1/CHEK2, high ATR expression pattern) — reconciling competing prior hypotheses linking SBS8 to HRD and NER defects.

## Methods

**Data:** Somatic point mutations from 18 ICGC WGS cancer cohorts (20–569 samples/cohort, median 145; samples with <500 mutations excluded). De novo germline mutations from 250 Dutch parent-offspring trios (11,020 mutations). Structural variation and RNA-seq expression data for a subset of cohorts [@Singh2020].

**Epigenomic context framework:** Genome segmented into (i) genomic contexts (exons, whole genes, repeats, telomere), (ii) chromatin contexts (strong heterochromatin → strong euchromatin), and (iii) nuclear localization contexts (lamina-proximal / nuclear interior). Tissue-invariant chromatin and lamina data from Smith et al. 2017; tissue-specific ENCODE data for selected cancer types.

**MRE composite context (HMM):** A multivariate Hidden Markov Model trained with the Baum-Welch algorithm jointly annotates combinations of genomic + epigenomic + cellular-process features into a compact set of "mutagenesis-related epigenomic" (MRE) states. A 20-state model was used for downstream analyses, with 10- and 30-state models confirming robustness. ENCODE cell lines used: lung (IMR90), breast (MCF7), liver (HepG2), neuronal (SK-N-SH), hematopoietic (GM12878, K562).

**Replication analysis:** Repli-seq data from multiple human cell types; replication timing, fork direction, and fork speed inferred from the smoothed Repli-seq gradient along chromosomes. Late vs early and fast vs slow contexts compared for SBS8 proportion.

**Signature decomposition:** `deconstructSigs` applied per-sample within each genomic/epigenomic context; proportions compared across contexts (not confounded by context length or overall mutation burden). COSMIC SBS v3 (49 signatures). `SigProfiler` used for de novo extraction within early/late replication strata as a check.

**Checkpoint analysis:** Tumors stratified by purity-adjusted ATR, CHEK1, CHEK2 expression.

**Cosine similarity:** BG signature from CHEK2−/− clonal cell lines compared to COSMIC SBS8 (cosine similarity = 0.663) [@Singh2020].

**Statistics:** R v3.4.0; Wilcoxon rank-sum, Spearman correlation, Fisher's combined p-values; rank-biserial correlation for effect sizes; FDR correction where appropriate.

## Key Findings

1. **Heterochromatin and nuclear periphery enrichment:** SBS8 is depleted in exons and euchromatin, and significantly over-represented in heterochromatin and lamina-proximal nuclear periphery across all 18 cancer cohorts (combined p < 1e-05 for both comparisons). This is the most consistent genomic/epigenomic pattern across tissue types.

2. **MRE composite context preference:** SBS8 is preferentially found in MRE states E6, E17, E18, E19, and E20 — all characterized by late-replicating heterochromatin. Early-replicating euchromatic MRE states consistently show depletion of SBS8.

3. **Replication timing drives SBS8:** Late-replicating genomic regions show significantly higher SBS8 weight than early-replicating regions across breast cancer (BRCA-EU), ovarian cancer (OV-AU), and lymphoma (MALY-DE) cohorts, and in tissue-invariant analyses of all 18 cohorts (combined p < 1e-05). SBS8 shows highest effect size in discriminating early vs late replication among all COSMIC signatures with >5% presence in these cohorts.

4. **Fast late replication amplifies SBS8:** Within late-replicating regions, higher replication speed is independently associated with greater SBS8 burden (combined p = 3.45e-09 across three cohorts). Replication speed is higher during late S-phase genome-wide (consistent with known low-origin-density, higher-speed late replication). No strand-direction (left/right fork) bias is observed for SBS8.

5. **Checkpoint defects promote SBS8:** Tumors with high ATR and low CHEK1 or CHEK2 expression have the highest SBS8 proportions in late-replicating domains. CHEK2−/− clonal cell lines accumulate a "background genome maintenance" (BG) signature with cosine similarity 0.663 to SBS8 — the highest similarity among tested signatures.

6. **SBS8 is tumor-specific and stage-progressive:** SBS8 is nearly absent from de novo germline mutations (mean weight 0.014 in late vs 0.011 in early replication; p > 0.05) and non-malignant somatic tissues, unlike clock-like SBS1 and SBS5. In tumor cohorts, SBS8 weight in late-replicating regions increases with pathological stage.

7. **Crosstalk with SBS40:** In epigenomic-context PCA, SBS8 clusters with SBS40 (both broad-spectrum, unknown aetiology, preferring late replication). SBS1, SBS3, and SBS5 are all depleted in late-replication contexts — directly contrasting SBS8. SBS12 (NER, T>C) also shows late-replication preference but is spectrally distinct from SBS8.

8. **Context-dependent co-occurrence with HRD and NER signatures:** In breast/ovarian cancer, SBS8 in late-replication contexts correlates with SBS3 and SBS1 in early-replication contexts, consistent with tissue-specific BRCA1/2 deficiency; but no single complementary signature generalises across all cancers.

9. **No enrichment in fragile sites:** Common and early replicating fragile sites are not enriched for SBS8 compared to late-replicating regions generally — replication fork collapse does not appear to be the primary SBS8 source.

## Relevance

**Direct relevance to hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and (agnostic covariate-signature association):**

This paper provides strong prior evidence for what the hypothesis:0007 positive-control recovery experiment should find for SBS8. Specifically:

- **SBS8 aetiology is replication-timing-driven, not exposure-driven.** SBS8 does not map to any known exogenous mutagen or specific transcriptional strand bias — it emerges from endogenous replication machinery operating in late-replicating heterochromatin. This is precisely the class of "endogenous, process-linked" signatures that an agnostic covariate scan should be able to surface via genomic covariates (replication timing, chromatin context) rather than clinical exposures.

- **Positive control scope:** The hypothesis:0007 pre-registration targets UV→SBS7, smoking→SBS4, and APOBEC3-expr→SBS2/13 as the three recovery arms. SBS8 is explicitly not among the positive-control signatures, but this paper documents the *kind* of evidence a successful association looks like — a strong, reproducible, within-tissue, context-dependent signature-covariate link that holds across multiple independent cohorts.

- **SBS40 parallel:** Singh et al. note that SBS40 and SBS8 share late-replication preference and unknown aetiology. Hypothesis:0007 discovery lists SBS40 as a target for novel covariate association. The epigenomic similarity described here implies that any latent expression module found to associate with SBS8 should be tested on SBS40 simultaneously (a free prediction).

- **Checkpoint expression as a covariate:** The paper demonstrates that ATR / CHEK1 / CHEK2 expression covaries with SBS8 in late-replicating regions. This is an existence proof that the type of mRNA-expression covariate association targeted by hypothesis:0007 (expression modules vs signature exposures) can recover mechanistically informative links for a signature of unknown or debated aetiology.

- **Cross-study replication:** The analysis spans 18 ICGC WGS cohorts with diverse tissue-of-origin, exactly the multi-cohort context available in the cBioPortal meta-analysis. The consistency of SBS8's late-replication enrichment across cohorts (combined p < 1e-05) supports that replication-timing-linked covariates will be detectable even at cBioPortal-scale panel data if the within-tissue design is maintained.

- **Non-malignant tissue contrast:** The observation that SBS8 is near-absent in normal tissues and accumulates with stage informs the design of the hypothesis:0007 control arm: analyses restricted to tumor genomes will see a clearer SBS8 signal than mixed tumor/normal analyses, consistent with the pipeline's tumor-only input data.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| SBS8 signature weight per epigenomic context | Per-sample signature exposure `H[SBS8, sample]` from NMF | The paper uses `deconstructSigs` within contexts; hypothesis:0007 uses `SigProfiler` restricted assignment |
| MRE state (HMM composite context) | Potential covariate in the agnostic association layer | Replication timing is a derived feature; not yet in cBioPortal clinical tables but derivable for TCGA MC3 |
| Late vs early replicating regions | Genomic annotation covariate (replication timing) | Repli-seq not in standard cBioPortal data; indirect via histone-state proxies |
| ATR / CHEK1 / CHEK2 expression | mRNA expression covariate module | Directly computable from TCGA expression data via `export_study_expression.py` |
| Pathological stage | `stage` clinical column (already ingested) | Stage-SBS8 association is a direct hypothesis:0007 test |
| SBS40 (similar to SBS8) | Co-discovery target in hypothesis:0007 | Both are broad-spectrum, unknown-aetiology signatures with late-replication preference |

## Limitations

- **Correlation, not causation:** The paper's main inference chain (late replication → replication errors → SBS8) is correlative; the checkpoint expression data are also correlational and the authors acknowledge that current tumor expression is a poor proxy for expression at the time mutations were generated.
- **WGS-only analysis:** All 18 ICGC cohorts are whole-genome sequencing, providing the coverage needed to stratify mutations by chromatin context. The cBioPortal meta-analysis is predominantly panel/exome data, which cannot directly reproduce context-stratified analyses of heterochromatin (most panel genes fall in euchromatin). The per-sample SBS8 decomposition from panels will be noisier.
- **18 cancer types, but fixed set:** The cohorts are ICGC release 28; newer TCGA MC3 or pan-cancer analyses might find different or additional patterns.
- **MRE state annotation is cell-line-based:** Tissue-specific MRE states use ENCODE cell lines (MCF7, HepG2, etc.) as proxies for tumor epigenomes; primary tumor epigenomes may differ.
- **SBS8 vs SBS3/SBS5 deconvolution:** The authors acknowledge that separating broad-spectrum signatures computationally is challenging; `deconstructSigs` assignments within narrow contexts may be noisy.
- **Checkpoint gene expression directionality:** High ATR / low CHEK1/CHEK2 may reflect post-mutation selection rather than pre-existing checkpoint capacity; the causal direction is not resolved.
- **SBS40 hypothesis is speculative:** The proposed relationship between SBS8 and SBS40 is based on pattern similarity; no functional evidence is provided.

## Model / Tool Availability

- **mutSigTools R package:** Analysis code available at https://github.com/sjdlabgroup/MutSigTools; scripts for processing mutation data in genomic/epigenomic contexts.
- **MRE state annotations:** Composite epigenomic state (MRE) genomic coordinates provided as Supplementary Data 3.
- No pre-trained model weights distributed beyond the supplement.

## Follow-up

- **Papers to read next:**
  - Morganella et al. 2016 (Nat Commun) — topography of mutational processes in breast cancer; original breast-cancer SBS8 context analysis cited multiple times here.
  - Tomkova et al. 2018 (Genome Biol) — mutational signature distribution with replication timing and strand asymmetry; cited for no strand bias in SBS8.
  - Poti et al. 2019 (Genome Biol) — CHEK2−/− clonal mutation catalog (the BG signature source); cited for cosine similarity to SBS8.
  - Liu et al. 2013 (Nat Commun) — replication timing and mutation landscapes; foundational for this paper's framework.
  - Smith et al. 2017 (Nat Struct Mol Biol) — nuclear topology and mutational landscapes; source of tissue-invariant lamina/chromatin data used here.

- **Questions this raises for the project:**
  - In the cBioPortal pipeline's restricted SigProfiler output, does SBS8 weight per sample correlate with any available clinical stage, MSI status, or TMB variable? (Test the stage-SBS8 link with available data, as a low-cost check of the paper's finding using panel data.)
  - Can ATR/CHEK1/CHEK2 expression be included as a candidate covariate in the hypothesis:0007 agnostic scan for TCGA MC3 samples with paired expression data?
  - Does SBS40 show the same stage-progression pattern as SBS8, as would be predicted from their epigenomic similarity?
  - The paper notes SBS8 is depleted in exons — since cBioPortal panels predominantly capture coding regions, does this mean SBS8 is systematically under-estimated in panel-based decompositions relative to WGS?
