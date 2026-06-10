---
type: paper
title: DNA mismatch repair promotes APOBEC3-mediated diffuse hypermutation in human
  cancers
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: paper:MasPonte2020
ontology_terms:
- APOBEC3
- mismatch repair
- mutational signatures
- kataegis
- hypermutation
- somatic mutation clustering
- single-stranded DNA
- cancer genomics
datasets: []
source_refs:
- cite:MasPonte2020
related:
- paper:MasPonte2022
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
---

# DNA mismatch repair promotes APOBEC3-mediated diffuse hypermutation in human cancers

- **Authors:** David Mas-Ponte, Fran Supek
- **Year:** 2020
- **Journal:** Nature Genetics, 52(9): 958-968
- **DOI/URL:** https://doi.org/10.1038/s41588-020-0674-6
- **BibTeX key:** MasPonte2020
- **Source:** PDF

## Key Contribution

This paper identifies a previously unrecognized mode of APOBEC3 (A3) mutagenesis in human
tumors called *omikli* (Greek: fog) — diffuse, non-recurrent hypermutation clusters of 2–4
mutations — mechanistically distinct from the well-known *kataegis* (thunderstorm) showers.
The central finding is that DNA mismatch repair (MMR) activity, not double-strand break
processing, drives omikli by generating single-stranded DNA (ssDNA) excision intermediates
that serve as A3 substrate. Because MMR is directed to early-replicating, gene-rich regions,
this coupling makes A3/MMR-linked mutations disproportionately likely to affect cancer driver
genes relative to common external mutagens (tobacco, UV).

## Methods

- **Cohort:** 699 TCGA tumor whole-genome sequences (WGS) across 22 cancer types (primary
  discovery); 2,304 Hartwig Medical Foundation WGS (validation); ~5,831 TCGA MC3 WES tumors
  for 16 cancer types (functional impact analysis).
- **Mutation clustering:** Custom tool **HyperClust** — a randomization-based FDR estimator
  (local FDR, *lfdr*) for mutation cluster detection. Randomizes mutations within 1 Mbp
  chromosomal windows preserving trinucleotide context; stratifies mutation pairs by base
  type and clonal fraction. Compared against prior approaches via simulated spiked-in
  cluster benchmarks.
- **Cluster classification:** Poisson mixture modelling (R *flexmix* package) on number of
  mutations per cluster distinguishes the two-component distribution: omikli (short; mean
  2.2 mutations) vs kataegis (long; mean 7.1 mutations); clusters with 2–4 mutations
  classified as omikli, ≥5 mutations as kataegis.
- **Genomic feature enrichment:** Negative binomial regression of cluster counts on
  replication timing bins (ENCODE RepliSeq), H3K36me3 marks (Roadmap Epigenomics), CpG
  density, and expression levels; conditioned on trinucleotide composition.
- **IMD analysis:** Inter-mutational distance (IMD) distributions modelled as gamma mixtures
  to infer underlying ssDNA tract lengths; compared to simulated IMD expected for 25 nt
  (RPA footprint), 200 nt (Okazaki fragment), and 800 nt (MMR excision tract) exposures.
- **MSI stratification:** 24 TCGA MSI vs matched MSS tumors; MSI labels from reference data;
  TMZ-treated samples excluded.
- **Functional impact density (FID):** Fraction of mutations from a given process landing in
  coding sequences of cancer genes (299 Cancer Gene Census genes); expressed as oncogenic
  mutations per thousand (OMPK).
- **Driver gene association:** Logistic regression of cancer-gene mutation status on omikli/
  kataegis burden (square-rooted), within A3 (TCW>K) context; 61 testable genes; FDR
  corrected with Benjamini-Hochberg.

## Key Findings

1. **Two distinct A3 cluster types.** HyperClust detects 108,401 clustered mutations in 699
   TCGA tumors (lfdr ≤ 20%); the cluster length distribution is better fit by a two-Poisson
   mixture than a single distribution. Omikli (mean 2.2 mut/cluster) and kataegis (mean 7.1
   mut/cluster) are the two components.

2. **Omikli is ubiquitous; kataegis is rare.** 76% of tumors carry ≥3 A3 omikli events
   (vs ~14% expected by chance); 48% carry ≥3 A3 kataegis events. Omikli and kataegis
   loads are only weakly correlated (R²=0.11), confirming independent mechanisms.

3. **Omikli enriches in early-replicating, MMR-active domains.** A3-context omikli clusters
   are 2.0–2.5-fold enriched in early-replicating regions (vs 0.54–0.72-fold for unclustered
   TCW and VCN controls). Enrichment follows the H3K36me3 histone mark gradient — a hallmark
   of MMR targeting — even after conditioning on replication timing and gene expression.

4. **MMR deficiency (MSI) depletes omikli.** MSI tumors show a 5.52-fold lower fraction of
   A3 omikli than MSS counterparts (p<0.001, Mann-Whitney; consistent across 3 cancer types,
   pooled p<0.001 Fisher's method). Absolute omikli counts are also lower in MSI (p<0.01),
   in contrast to the overall increase in mutation load — MMR normally protects against most
   mutations but paradoxically promotes A3 omikli when intact.

5. **IMD peak matches MMR excision tract length (~800 nt).** The global IMD peak for omikli
   is 355 nt, matching the simulated peak for 800 nt ssDNA segments (MMR excision length
   in vitro). Kataegis IMD shows no corresponding peak, disfavoring a shared mechanism.

6. **Omikli explains ~two-thirds of global A3 context mutations.** Regression-based
   decomposition: omikli process (A3-O) accounts for ~66.4% of TCW>K context mutations
   pan-cancer; kataegis (A3-K) ~0%; the remaining ~32.4% (A3-X) is unaccounted-for (likely
   lagging-strand synthesis or BER-processed lesions).

7. **A3 mutagenesis has higher functional impact than common external mutagens.** Oncogenic
   FID: A3-O = 0.47 OMPK; A3-K = 0.46 OMPK. By comparison: tobacco smoking = 0.24 OMPK;
   UV = 0.19 OMPK; stomach acid (Sig17) = 0.24 OMPK. The higher FID is not from positive
   selection but from MMR directing mutations to early-replicating, gene-rich (euchromatic)
   domains.

8. **A3 omikli preferentially affects chromatin modifier and tumor suppressor genes.** 22
   cancer genes are significantly associated with omikli burden at FDR<5%; 30 at FDR<10%
   (including KMT2A/C/D, NCOR1, SETD2, MECOM, PBRM1, ARID2). Genes linked to omikli are
   enriched for tumor suppressors (14 of 30 vs 5 oncogenes). No genes are significantly
   associated with kataegis.

9. **Strand bias of omikli matches post-replicative MMR, not leading-strand POLE.** The
   leading vs lagging strand ratio of omikli mutations closely matches MSI (MMR-deficient)
   tumors and differs from POLE-mutant strand bias, supporting MMR excision as the source.

10. **A3-context 5' tetranucleotide analysis suggests A3A drives omikli, A3B drives
    kataegis.** A3A-like (YTCA) context is enriched in omikli relative to kataegis across
    multiple cancer types; A3B-like (RTCA) context is relatively enriched in kataegis.

## Relevance

**Direct relevance to h08 (agnostic covariate→signature-exposure recovery):**

- **Positive control arm — APOBEC3 expression ↔ SBS2/13 (H08a Arm 3).** This paper
  provides the mechanistic foundation for why APOBEC3A/B expression should be the strongest
  molecular predictor of A3 signature exposure within a tissue: the omikli mechanism is
  expression-limited (Spearman rho = 0.31/0.45 for APOBEC3A/B mRNA with omikli burden;
  smaller for kataegis). If h08's agnostic covariate scan of mRNA expression recovers
  APOBEC3A/3B as the top hits for SBS2/SBS13 within relevant tissue types (lung, bladder,
  breast, cervical, HNSC), that is expected and interpretable mechanistically. Failure to
  recover this would falsify H08a.

- **Interpretation guide for the discovery prong (H08b).** The MMR→A3 coupling means that
  MSI status and MMR gene (MSH6, MSH2, EXO1) expression/copy-number should also correlate
  *negatively* with SBS2/13 exposures (omikli depleted in MSI). The h08 scan should see
  MMR pathway covariates associating with APOBEC signatures in an unexpected direction
  (higher MMR integrity → more SBS2/13, not less). This is a subtle, counterintuitive
  association that a purely covariate-blind scan might surface and that the literature
  supports.

- **Cross-study meta-analysis relevance.** The pipeline aggregates mutation counts across
  ~300 cBioPortal studies; A3 omikli comprises ~66% of all A3-context somatic mutations.
  Since omikli mutations are enriched in gene-dense, early-replicating domains, they will
  disproportionately appear in the pipeline's exome-derived data (which already selects
  coding regions). This inflates apparent A3-pathway mutation rates in panel/WES-based
  studies relative to WGS, creating a potential cross-study bias for cancer types with high
  A3 activity (lung, bladder, breast, cervical, head-and-neck).

- **Driver gene context.** Chromatin modifier genes (KMT2A/C/D, SETD2, ARID2, PBRM1,
  NCOR1) are disproportionately targeted by the omikli mechanism. These genes recur in the
  pipeline's cross-study mutation frequency tables. Their elevated rates in APOBEC-active
  cancers partly reflect mechanism (MMR directs A3 mutagenesis to gene-rich regions), not
  solely positive selection — relevant when interpreting the pipeline's mutation frequency
  rankings.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| omikli (A3-O process) | APOBEC signature component / SBS2+SBS13 | ~66% of TCW>K mutations genome-wide |
| kataegis (A3-K process) | Focal APOBEC hypermutation | Minor contributor to unclustered TCW>K |
| A3-X (residual TCW>K) | Unclustered APOBEC mutations, BER or replication origin | ~32% not explained by omikli/kataegis |
| MMR activity → omikli | MSI status covariate (pipeline clinical fields) | MMR-proficient (MSS) promotes omikli; MSI depletes it |
| Functional impact density (FID) | Mutation enrichment in cancer genes | Relevant for interpreting pipeline mutation frequency tables |
| HyperClust | Not in current pipeline | Whole-genome cluster calling tool; pipeline uses panel/WES data so direct application is limited |

## Limitations

- **WGS-centric:** The omikli/kataegis distinction requires WGS. The pipeline primarily
  ingests WES/panel data from cBioPortal; direct cluster detection is not feasible.
  However, the mechanism's covariate implications (MSI, A3 expression, replication timing)
  can still be tested at the study level.
- **TCGA dominant cohort:** Discovery cohort is 699 TCGA WGS tumors. Hartwig validation uses
  2,304 tumors but from a different patient selection context (metastatic). Pan-cancer
  generalizability beyond the 22 represented cancer types is inferred.
- **Causal interpretation of MMR-A3 link:** The strand-bias and IMD analyses are consistent
  with MMR-generated ssDNA as substrate, but do not rule out alternative explanations (e.g.,
  replication fork dynamics altered by MMR activity). Authors acknowledge ~one-third of A3
  mutations (A3-X) are not explained by omikli.
- **A3A vs A3B distinction is associative:** The tetranucleotide context analysis implicates
  A3A in omikli and A3B in kataegis but cannot directly measure individual paralog activity
  in tumor cells.
- **Skin cancer (SKCM) and B-cell lymphoma (DLBC) excluded** from cluster analysis due to
  overlapping UV signatures (SKCM) and somatic hypermutation (DLBC), limiting applicability
  to those cancer types.

## Follow-up

- **MasPonte2022** — companion review paper (already summarized) on the full spectrum of
  MMR failures in cancer genomics; provides broader context for the omikli mechanism.
- Alexandrov et al. 2020 (COSMIC v3) — for mapping omikli/kataegis to SBS2 and SBS13.
- Petljak et al. / Roberts & Gordenin — foundational kataegis papers (references 8, 10).
- Chan et al. 2015 / Buisson et al. — A3 expression in cancer, germline APOBEC3A/B
  deletion polymorphism.
- For h08: whether within-tissue APOBEC3A/3B mRNA expression rank-predicts SBS2/13
  exposure better than MSI status or other covariates is the key association test to run.
  The paper predicts expression is the primary limiting factor for omikli (not kataegis).
