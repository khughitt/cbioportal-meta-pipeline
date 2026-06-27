---
type: paper
title: 'MutationalPatterns: the one stop shop for the analysis of mutational processes'
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: paper:Manders2022
ontology_terms:
- mutational signatures
- somatic mutation
- NMF
- signature refitting
- indels
- double base substitutions
- lesion segregation
- R/Bioconductor
datasets: []
source_refs:
- cite:Manders2022
related: []
---

# MutationalPatterns: the one stop shop for the analysis of mutational processes

- **Authors:** Freek Manders, Arianne M. Brandsma, Jurrian de Kanter, Mark Verheul, Rurika Oka, Markus J. van Roosmalen, Bastiaan van der Roest, Arne van Hoeck, Edwin Cuppen, Ruben van Boxtel
- **Year:** 2022
- **Journal:** BMC Genomics, 23:134
- **DOI/URL:** https://doi.org/10.1186/s12864-022-08357-3
- **BibTeX key:** Manders2022
- **Source:** PDF

## Key Contribution

MutationalPatterns v3.4.0 is a near-complete rewrite of the R/Bioconductor MutationalPatterns package (previously v1.4.3), extending somatic mutation analysis from single base substitutions (SBSs) alone to also cover double base substitutions (DBSs), multi-base substitutions (MBSs), and indels — all parsed from a single VCF. Key technical additions are: (1) a `fit_to_signatures_strict` function using iterative backwards selection to reduce COSMIC signature overfitting; (2) bootstrapped refitting for confidence quantification; (3) regional mutation spectrum analysis tied to arbitrary genomic annotations (enhancers, replication timing, chromatin); (4) lesion segregation detection (strand-asymmetric inheritance); and (5) a signature-specific damaging-potential score based on predicted stop-gain/missense/synonymous/splice-site consequences.

## Methods

**Input.** Mutations are loaded from VCF files via `read_vcfs_as_granges`; the package handles SBS, DBS, MBS, and indel contexts in one pass. Context windows are fully configurable (not fixed at 1 bp each side), supporting arbitrary extended trinucleotide or wider contexts.

**Mutation profile construction.** Count matrices are built by `mut_matrix`, `mut_matrix_stranded`, `count_indel_contexts`, `count_dbs_contexts`, `count_mbs_contexts`. Matrices can be pooled across samples or split by annotated genomic region using `split_muts_region` and a GRanges/GRangesList object.

**De novo signature extraction.** Standard NMF plus a variational Bayesian (Bayes) NMF implementation (ccfindR) for optimal rank selection; extracted signatures renamed via cosine similarity to known catalogues using `rename_nmf_signatures`.

**Signature refitting (known signatures).** `fit_to_signatures` (original least-squares); `fit_to_signatures_strict` (new, iterative backwards selection — each iteration drops the lowest-contributing signature until cosine similarity change per step exceeds `max_delta`); `fit_to_signatures_bootstrapped` (repeated sampling to quantify contribution confidence). Bundled reference matrices include COSMIC v3.1+v3.2, SIGNAL v1, SparseSignatures v1 — loaded via `get_known_signatures`.

**Simulated benchmark.** 300 simulated matrices per condition (200/400/2000/4000 mutations per sample) drawing from the first 30 COSMIC SBS signatures at 4-signature blends, repeated 300 times. Strict refitting outperformed "regular" and "regular_10+" by precision while preserving sensitivity; AUC of 0.925 even at 50 mutations per signature.

**Regional analyses.** Mutations split into genomic annotation bins; mutation spectra compared per region via chi-squared test (Monte Carlo) with FDR correction. Unsupervised regional similarity assessed genome-wide using a sliding-window cosine similarity vs. the whole-genome profile (`determine_regional_similarity`).

**Lesion segregation.** Watson–Crick strand asymmetries per chromosome measured by `calculate_lesion_segregation`; rl20 statistic (value >5 indicates lesion segregation).

**Damaging potential.** `context_potential_damage_analysis` + `signature_potential_damage_analysis` score signatures for stop-gain/missense enrichment relative to a flat hypothetical signature.

**Validation dataset.** AHH-1 lymphoblastoid CRISPR-Cas9 bi-allelic knockouts of MSH2, UNG, XPC (individually and combined with HPRT) — WGS on clonally expanded subclones; somatic variants identified by subclone-vs-clone subtraction.

## Key Findings

**Extended context matters.** In 276 HMF melanoma samples, TT[C>T]CT is the dominant substitution (more common than any T[C>T]C context), demonstrating that the extended 5′ base has a large effect on SBS spectrum shape (Fig. 4a).

**Regional spectra are informative.** MSH2 and UNG knockout cells show significantly different mutation spectra in exons vs. the rest of the genome (FDR = 0.0012 for both; chi-squared, Monte Carlo) and between early-, intermediate- and late-replicating DNA (FDR = 0.0012 and 0.0012 respectively). These patterns disappear when downsampled to 227 mutations, underscoring statistical power dependence.

**Somatic hypermutation regions detectable.** In 217 pediatric B-ALL samples, the package identifies distinct mutational spectra at the VDJ regions on chromosomes 2 and 14, consistent with somatic hypermutation at immunoglobulin loci (Fig. 4c).

**Strict refitting reduces false positive signatures.** Compared to "regular" and "regular_10+" approaches, `fit_to_signatures_strict` achieves substantially higher precision with comparable recall across all simulated mutation loads. AUC = 0.925 at 50 mutations/signature — practical even for samples with limited mutation counts.

**Bootstrapping reveals signature confusion.** In UNG knockouts, SBS30 contribution was negatively correlated with SBS2 across bootstrap iterations (correlation = 0.46 cosine similarity), signalling that the algorithm struggles to disambiguate these two signatures — a finding only visible via bootstrapping.

**DNA repair knockout profiles recover expected COSMIC signatures.** MSH2 knockouts: SBS5, SBS20, SBS26, SBS44 (all MMR-associated). UNG knockouts: SBS30 (previously NTHL1/oxidative; here attributed to uracil-removal deficiency). XPC knockouts: SBS8 (nucleotide excision repair deficiency). Cosine similarity between original and reconstructed profiles ≥ 0.95 for all knockout types (strict refitting; Fig. 3e).

**MSH2 indel signature.** MSH2 knockout shows a markedly elevated indel burden vs. wild type; strict indel refitting assigns ID1, ID2, ID7 — consistent with polymerase slippage and defective mismatch repair (Fig. 5).

**Damaging potential of COSMIC signatures.** SBS10a (POLE) and SBS18 (oxidative stress) are 3.6× and 2.0× more likely than a flat signature to cause stop-gain mutations; SBS1 (clock-like aging) scores 0.81× — much lower damaging potential (Fig. not directly numbered but described p. 14).

**Performance.** `mut_matrix` and `mut_matrix_stranded` re-implemented with O(n) vectorized operations; 3.4× and 2.6× faster than v1.4.3; a 1-million-SBS matrix now computes in ~135 s on a laptop.

## Relevance

**hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and — Agnostic covariate–signature-exposure association (positive-control recovery of UV/smoking/APOBEC/MMR).**

This paper is directly relevant to the hypothesis:0007 positive-control prong (H08a). Several points of contact:

1. **Signature refitting is the core analytical primitive.** The hypothesis:0007 pipeline must assign per-sample COSMIC signature exposures before running any covariate association. MutationalPatterns v3.4.0's `fit_to_signatures_strict` with `max_delta` tuning is a concrete, benchmarked implementation that reduces the overfitting artifact (too many signatures assigned to a sample), which would otherwise generate spurious covariate hits.

2. **Bootstrapped refitting quantifies confidence in exposures.** The H08a positive-control arms (UV→SBS7, smoking→SBS4, APOBEC3-expression→SBS2/13) all require trustworthy per-sample exposure estimates. Bootstrapped contributions allow the association layer to weight samples by refitting confidence — a natural FDR guard.

3. **MMR/MSI positive control is illustrated here.** The MSH2 knockout results (SBS20/26/44 recovered, indel ID1/ID2/ID7 elevated) directly demonstrate the kind of positive-control recovery the H08a MMR arm requires: MMR-loss status as covariate, SBS6/15/26/44 exposures as outcome.

4. **Extended context and regional analyses.** The `split_muts_region` and regional spectrum tools could support the hypothesis:0007 covariate scan if any covariate (e.g. chromatin state) requires restricting to genomic subsets before fitting.

5. **Damaging potential scores.** A downstream application of the hypothesis:0007 discovery arm would be to assess whether novel covariate-associated signatures also show elevated damaging potential — MutationalPatterns provides this function directly.

**Cross-study meta-analysis relevance.** The package's ability to pool samples (`pool_mut_mat`) and support all mutation types from a single VCF is directly useful if the cBioPortal pipeline extends to indel or DBS signature analysis.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| `fit_to_signatures_strict` (backwards selection) | Signature refitting / per-sample exposure estimates | Core input to hypothesis:0007 covariate association |
| `fit_to_signatures_bootstrapped` | Confidence-weighted exposures | Natural weight for association layer |
| `get_known_signatures` (COSMIC v3.1/3.2, SIGNAL, SparseSignatures) | COSMIC reference catalogue | Same catalogues used by SigProfiler refitting in the pipeline |
| Lesion segregation (`calculate_lesion_segregation`, rl20) | (not currently in pipeline) | Detects unmatched-normal contamination confound |
| Regional mutation spectra (`split_muts_region`) | (not in current pipeline) | Could stratify by replication timing as a covariate |
| Signature damaging potential score | (not in pipeline) | Post-hoc prioritization of hypothesis:0007 novel hits |
| NMF / Bayes-NMF de novo extraction | De novo signature extraction | Complementary to SigProfiler |

## Limitations

- **R-only; no Python interface.** The cBioPortal pipeline is Python/Snakemake; MutationalPatterns is an R/Bioconductor package. Integration requires either an R subprocess wrapper or parallel re-implementation in Python.
- **Strict refitting AUC at low mutation counts.** AUC = 0.925 at 50 mutations/signature is good but not perfect; panel-sequenced tumors (common in cBioPortal) may fall below this threshold, limiting per-sample exposure reliability.
- **Damaging potential is context-only.** The score ignores chromatin state, tissue-specific expression of genes harboring the mutations, or 3D genome context.
- **Benchmarked against first 30 COSMIC SBS signatures only.** Performance on the full COSMIC v3.3 catalogue (>80 SBS signatures) or tissue-specific sub-catalogues is not assessed.
- **Regional analysis requires high mutation counts.** The paper notes that at 227 mutations (the minimum in their set), regional differences in the MSH2/UNG knockouts disappear — a practical floor for the analysis.
- **Artefact signatures excluded by default from `get_known_signatures`.** Downstream users must opt back in to inspect data quality, which may be important for unmatched-normal cBioPortal studies.

## Model / Tool Availability

- **Package name:** MutationalPatterns
- **Version described:** v3.4.0
- **Language:** R (≥ 4.1.0); R/Bioconductor
- **Repository:** https://github.com/ToolsVanBox/MutationalPatterns
- **Archived Bioconductor version:** https://bioconductor.org/packages/3.14/bioc/html/MutationalPatterns.html
- **License:** MIT
- **OS:** Linux, Windows, macOS
- **Data/scripts for paper figures:** https://github.com/ToolsVanBox/MutationalPatterns_manuscript2_data_scripts/
- **Bundled reference matrices:** COSMIC v3.1+v3.2, SIGNAL v1, SparseSignatures v1

## Follow-up

- **Related tools benchmarked in Table 1:** SigProfiler (Python, human/mouse/rat/yeast), SignatureAnalyzer (Python), deconstructSigs (R), sparseSignatures (R), signeR (R), somaicSignatures (R), Maftools (R), decompTumor2Sig (R) — consult for comparison when selecting a refitting back-end for hypothesis:0007.
- **Lesion segregation** could be a useful diagnostic for identifying cBioPortal studies using unmatched normals (where C>N and T>N strand asymmetry would accumulate from germline leakage rather than true somatic mutagenesis). Worth evaluating alongside the `topic:signature-decomposition-unmatched-normal` context.
- **Bootstrapped contribution output** (`fit_to_signatures_bootstrapped`) provides natural uncertainty estimates for hypothesis:0007's per-sample signature exposures. Consider as input weights in the association model rather than point estimates.
- The `determine_regional_similarity` sliding-window function could test whether VDJ-region somatic hypermutation creates a systematic artifact in B-cell malignancy studies in cBioPortal — relevant to the CH contamination audit.
