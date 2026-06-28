---
type: paper
title: Genome-wide mutational signatures of immunological diversification in normal
  lymphocytes
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: paper:Machado2021
ontology_terms: []
datasets: []
source_refs:
- cite:Machado2021
related: []
---

# Genome-wide mutational signatures of immunological diversification in normal lymphocytes

- **Authors:** Heather E Machado, Emily Mitchell, Nina F Øbro, Kirsten Kübler, Megan Davies, Francesco Maura, Daniel Leongamornlert, Mathijs A Sanders, Alex Cagan, Craig McDonald, Miriam Belmonte, Mairi S Shepherd, Robert J Osborne, Krishnaa Mahbubani, Iñigo Martincorena, Elisa Laurenti, Anthony R Green, Gad Getz, Paz Polak, Kourosh Saeb-Parsy, Daniel J Hodson, David Kent, Peter J Campbell
- **Year:** 2021
- **Journal:** bioRxiv (preprint, posted 2021-04-30)
- **DOI/URL:** https://doi.org/10.1101/2021.04.29.441939
- **BibTeX key:** Machado2021
- **Source:** PDF

## Key Contribution

This study provides the first comprehensive whole-genome mutational landscape of normal human lymphocytes, sequencing 717 single-cell-expanded naive and memory B and T lymphocytes alongside hematopoietic stem/progenitor cells (HSPCs) from six donors. It demonstrates that lymphocytes accumulate substantially more somatic mutations than stem cells, with distinct signatures reflecting both programmed immune diversification (RAG, AID, somatic hypermutation) and exogenous exposures (UV radiation, unknown mutagenic microenvironments). Memory B cells acquire on average 18 off-target genome-wide mutations for every one on-target IGV mutation during the germinal center reaction, and ~15% of off-target structural variants genome-wide bear RAG recombination signal sequence (RSS) motifs, implicating RAG off-target activity as a major source of lymphocyte structural variation [@Machado2021].

## Methods

**Experimental design.** Single naive and memory B and T lymphocytes (plus HSPCs) were flow-sorted from peripheral blood, spleen, bone marrow, tonsil, and cord blood of six donors aged 0–81 years. Cells were expanded in vitro to colonies of 30–2,000+ cells, then subjected to whole-genome sequencing at ~20x depth. The final dataset comprised 717 whole genomes representing eight cell subsets (naive B, memory B, CD4+ naive T, CD4+ memory T, CD8+ naive T, CD8+ memory T, T-regulatory cells, HSPC) [@Machado2021].

**Mutation calling.** Somatic SNVs, indels, and structural variants (SVs) were identified using standard benchmarked bioinformatics pipelines. Average telomere lengths were estimated from sequencing data.

**Signature extraction.** Mutational signatures were extracted and attributed per genome using `hdp` (hierarchical Dirichlet process) and `sigprofiler`, with per-genome attribution refined by `sigfit`. Signatures with a 90% CI lower bound <1% were excluded from per-genome plots [@Machado2021].

**Genomic distribution modeling.** General additive models (GAMs) regressed SBS9 burden against 36 genomic features (gene density, chromatin marks, replication timing) across 10 kb bins. Random Forest regression modeled the match of each genome's mutation distribution to 149 epigenomes representing 48 blood cell types and differentiation stages [@Machado2021].

**Structural variant analysis.** SVs were called across 635 lymphocytes; RAG recombination signal sequence (RSS) motifs were looked for within 50 bp of breakpoints using genomic background correction [@Machado2021].

**Malignancy comparison.** Normal lymphocyte mutation burdens and signature proportions were compared against published WGS data from seven blood cancers: Burkitt lymphoma, follicular lymphoma, DLBC lymphoma, multiple myeloma, mutated and unmutated CLL, and myeloid-AML.

## Key Findings

**Mutation burden.**
- Lymphocytes carry more SNVs than HSPCs; naive B and T cells have ~110 and ~59 extra SNVs respectively (above HSPC age-adjusted baseline); memory B and T cells carry ~1,034 and ~277 extra SNVs.
- T cells accumulate mutations faster per year than B cells: naive T: 22 mut/cell/year; memory T: 25 mut/cell/year versus naive B: 15 and memory B: 17 mut/cell/year; HSPCs: ~16 mut/cell/year.
- Variance in mutation burden increases dramatically with lymphocyte differentiation (SD in HSPCs: 70 SNVs/cell; memory B: 820 SNVs/cell; memory T: 592 SNVs/cell; p<10⁻¹⁶).

**Mutational signatures in lymphocytes.**
- Naive B and T cells (and HSPCs) are dominated by two endogenous signatures: SBS1 (spontaneous deamination of methylated cytosines, clock-like) and SBSblood (a novel blood-specific endogenous signature; clock-like, correlates with age).
- Memory B cells additionally carry SBS9 (42% of mutations on average, mean 780 mut/cell), SBS8, and sporadic SBS7a/SBS17b.
- Memory T cells carry SBS7a (UV, >10% in 9/100 cells; mean 757 mut/cell in those cells) and SBS17b [@Machado2021].

**SBS7 as a record of skin residency.** SBS7a matches the canonical UV signature; 9/100 circulating memory T cells showed SBS7 contributions >10%, with shorter telomeres than SBS7-low cells (p=0.01, indicative of greater proliferative history). UVB penetrates only 10–50 µm into skin, so these cells must have been skin-resident at some stage. This implies skin-resident T cells represent a large, dynamically recirculating population [@Machado2021].

**SBS17b as evidence of gastrointestinal microenvironmental exposure.** SBS17 (characterized by T>G in TpT context) appeared in 3/74 memory B cells and 1/100 memory T cells (>4 SD above mean), independent of any treatment history. Its known occurrence in gastric and esophageal cancers suggests tissue residency in gastric/esophageal mucosa as an additional source [@Machado2021].

**SBS9 and the germinal center reaction.**
- SBS9 (A:T base-pair mutations, especially T>G in TpW context) accounts for 42% of memory B cell mutations (mean 780 mut/cell), sometimes tripling the baseline mutation burden.
- SBS9 mutations per genome correlated strongly (R²=0.57, p=4×10⁻⁹) with the fraction of IGHV mutated in the productive V(D)J rearrangement—the canonical proxy for germinal center activity. Density at IGHV was 270,000-fold higher than genome-wide SBS9 density.
- Every 1 on-target IGV mutation is accompanied by an average of 18 off-target SBS9 mutations elsewhere in the genome.
- Telomere lengths in memory B cells correlated with SBS9 burden (R²=0.37, p=3×10⁻⁸), consistent with telomerase activation in germinal centers.
- SBS9 enrichment in late-replicating, gene-poor, inactive chromatin regions (replication timing explains 17% of genomic SBS9 variance individually; R²=0.20 in full GAM with 18 features); distribution matches germinal center B cell epigenomes best (p=1.1×10⁻⁵).
- SBS9 spectrum differs from on-target somatic hypermutation (SHM): AID-induced SHM targets active chromatin, whereas SBS9 accumulates in inactive regions, arguing against direct AID causation. Authors propose a replicative-stress model: polymerase-eta bypass of background DNA lesions induced by replicative/oxidative stress in germinal center B cells, where mismatch repair is less active in late-replicating regions.

**Structural variation.**
- 1,037 SVs found across 635 lymphocytes; 85% were in Ig/TCR gene regions.
- 103/609 (17%) lymphocytes carried at least one off-target SV (vs. 1/82 HSPCs; p=9×10⁻⁵).
- ~15% of off-target (non-Ig/TCR) deletions carry an RSS (RAG) motif within 50 bp of the breakpoint (vs. genomic background), attributing ~12% of all non-Ig/TCR SVs to RAG off-target activity.
- CSR (via AID at switch regions) accounts for the remaining Ig SVs; CSR motifs are absent from non-Ig/TCR SVs, indicating CSR is exquisitely targeted.
- Occasional chromoplexy and templated insertions were observed.

**Epigenome-based timing of mutational processes.**
- Clock-like SBSblood mutations in naive B cells best correlate with HSPC epigenomes (confirming pre-differentiation acquisition); in memory B cells they correlate with memory B cell epigenomes (prolonged memory residence).
- SBSblood in naive T cells correlates with epigenomes of long-lived CCR7⁺CD45RO⁻CD25⁻ naive T cells, consistent with thymic origin and long naive T cell lifespan.
- SBS9 mutations correlate best with germinal center B cell epigenomes, providing independent evidence of germinal center acquisition.
- SBS7 in memory T cells correlates with differentiated (not naive) T cell epigenomes, supporting accumulation during tissue-resident memory phase.

**Comparison with lymphoid malignancies.**
- SNV burdens of Burkitt lymphoma, mutated/unmutated CLL, and AML overlap with normal memory B cell range; follicular lymphoma, DLBC lymphoma, and multiple myeloma have higher SNV burdens than normal lymphocytes.
- The mutational signature composition of B-cell malignancies is broadly similar to that of normal memory B cells—elevated SBS9, SBS8, SHM signatures—suggesting that cancer mutations derive from amplification of the same processes active in normal cells, not acquisition of cancer-specific processes (in contrast to colorectal/breast cancer).
- Off-target RAG-mediated SV proportions in lymphoid malignancies (except ALL) are comparable to normal lymphocytes; ALL shows specifically elevated RAG-SV proportions.

## Relevance

**Relevance to hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and (covariate–signature-exposure association; positive-control recovery of UV/smoking/APOBEC/MMR).**

This paper is directly germane to hypothesis:0007 in several ways:

1. **Positive-control signature recovery.** The clean recovery of SBS7 (UV) in circulating memory T cells demonstrates that exogenous-exposure signatures can be detected and attributed in non-cancer, non-skin WGS data when cell types are appropriate. This validates signature-based inference of environmental history as a biological reality and not purely a cancer-tissue artifact.

2. **Signature-to-covariate linkage.** SBS9 exposure is correlated with a biological covariate (IGHV mutation rate, a proxy for germinal center activity) with R²=0.57. SBS7 is correlated with UV/skin-residency; SBS17b correlates with GI tract residency. This is a model system for hypothesis:0007-style covariate<->signature-exposure association—the covariate here is cell-type-specific differentiation history rather than a clinical/demographic variable, but the conceptual structure is identical.

3. **Normal-tissue baseline for lymphocyte-derived tumors.** For the cbioportal cross-study meta-analysis, lymphoid malignancy studies (DLBC, CLL, ALL, MM) carry SBS9 and SBS8 as the dominant excess signatures. Understanding that these signatures originate in normal germinal center activity—and that their intensities reflect the degree of germinal center transit—contextualizes inter-study variation in lymphoid cancer mutation burdens. Studies dominated by post-GC malignancies will show elevated SBS9; studies with more naive-B-derived malignancies will not.

4. **Off-target immunological editing as a confounder.** In any pan-cancer study including lymphoid tumors, RAG/AID off-target activity (SBS8, SBS9, SHM signature) constitutes a tissue-of-origin confound. A covariate capturing lymphoid versus non-lymphoid tissue-of-origin would be expected to associate strongly with SBS9 exposure—this paper's data provide the normal-cell mechanistic anchor for that association.

5. **Structural variant awareness.** The 16-fold higher SV burden in lymphocytes versus HSPCs, and ~15% off-target RAG-mediated SVs, is relevant to any study incorporating SV-level data from lymphoid tumors.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| SBSblood (endogenous HSPC/naive lymphocyte signature) | Clock-like background signature | Baseline for mutation burden comparisons in lymphoid cancers in cbioportal |
| SBS9 (germinal center off-target AID/Pol-eta) | Lymphoid-specific signature | Dominant excess signature in post-GC B-cell malignancies; tissue-of-origin covariate |
| SBS7a (UV, skin residency) | Exogenous exposure signature | Positive control for hypothesis:0007 covariate–signature recovery |
| SBS17b (GI microenvironment) | Exogenous exposure signature | Sporadic; tissue-residency covariate candidate |
| Off-target RAG SVs | Structural variant confound | ~15% of non-Ig/TCR deletions in normal lymphocytes |
| Germinal center reaction | Cell-type differentiation event | Biological covariate explaining SBS9 exposure variance |

## Limitations

- Preprint (2021-04-30); peer-reviewed publication status should be rechecked before treating
  the findings as final.
- Small cohort (N=6 donors, ages 0–81); tissue availability varied by donor, limiting subgroup analyses.
- WGS at ~20x depth may underdetect low-frequency somatic variants; single-cell colony expansion avoids amplification artifacts but introduces potential selection bias during in vitro culture.
- SBS9 mechanistic model (polymerase-eta bypass in late-replicating regions) is a hypothesis consistent with the data but not directly proven; alternative contributions from AID or other mechanisms cannot be fully excluded [SPECULATION by authors].
- SBS17b aetiology in memory lymphocytes is unknown; the gastrointestinal microenvironment hypothesis is speculative [SPECULATION by authors].
- Donors were selected for hematopoietic normality, limiting generalizability to populations with clonal hematopoiesis or immunosenescence.
- No germline controls per-donor for the SV analysis; RAG-motif enrichment estimation relies on a genomic background model.

## Model / Tool Availability

- Analysis code: https://github.com/machadoheather/lymphocyte_somatic_mutation

## Follow-up

- Seek a published version of this preprint for peer-reviewed confirmation of findings.
- Compare SBS9 exposure levels across cbioportal lymphoid malignancy studies as a potential covariate proxy for germinal center transit.
- LeeSix2018 (HSPC WGS) provides the baseline HSPC mutation rate (~16 mut/cell/year) that this paper references and extends into lymphocyte subsets.
- Papers to read: the B lymphocyte single-cell WGS across lifespan paper cited as ref 13; the mutational signatures repertoire paper [@Alexandrov2020]; and the practical guide to signature analysis in hematological malignancies [@Maura2019].
