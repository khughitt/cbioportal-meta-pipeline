---
type: paper
title: Mutational impact of APOBEC3A and APOBEC3B in a human cell line and comparisons
  to breast cancer
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: paper:Carpenter2023
ontology_terms:
- APOBEC3A
- APOBEC3B
- mutational signatures
- SBS2
- SBS13
- cytosine deamination
- breast cancer
- single base substitution
- kataegis
- trinucleotide context
datasets: []
source_refs:
- cite:Carpenter2023
related: []
---

# Mutational impact of APOBEC3A and APOBEC3B in a human cell line and comparisons to breast cancer

- **Authors:** Michael A. Carpenter, Nuri A. Temiz, Mahmoud A. Ibrahim, Matthew C. Jarvis, Margaret R. Brown, Prokopios P. Argyris, William L. Brown, Gabriel J. Starrett, Douglas Yee, Reuben S. Harris
- **Year:** 2023
- **Journal:** PLOS Genetics
- **DOI/URL:** https://doi.org/10.1371/journal.pgen.1011043
- **BibTeX key:** Carpenter2023
- **Source:** PDF

## Key Contribution

This paper provides the first direct, controlled comparison of the mutagenic activity of APOBEC3A (A3A) and APOBEC3B (A3B) — the two leading candidates for the APOBEC3 mutational signature in human cancer — using a human cell line system with a selectable reporter. The central finding is that both A3A and A3B individually generate the canonical APOBEC3 signature (SBS2 + SBS13) at genome scale, but they do so with distinct tetranucleotide preferences: A3A strongly prefers YTCW motifs (~70%), while A3B shows only a weak YTCW preference (~50%), with a slight enrichment for RTCW. Because most primary breast tumors exhibit intermediate YTCW percentages (50–70%), the data support a model in which both enzymes contribute combinatorially to the observed composite signature in cancer [@Carpenter2023].

## Methods

**Experimental system.** The near-diploid human haploid cell line HAP1 was engineered to carry a single genomic copy of the HSV-1 thymidine kinase (*TK*) gene (HAP1-TK-M9), which confers sensitivity to ganciclovir. Cells that acquire inactivating *TK* mutations survive ganciclovir selection (Gan^R clones), enabling quantification of mutation frequency and direct Sanger sequencing of mutational spectra in the reporter gene.

**A3 expression.** MLV-based retroviral constructs driving A3A, A3B, A3H (haplotypes I and II), and catalytic-inactive derivatives (A3A-E72A, A3B-E255A, A3H-II-E56A) under a synthetic MND promoter were transduced into HAP1-TK-M9 cells. Single-copy integration was confirmed by low-MOI transduction and WGS-based site mapping.

**Whole-genome sequencing (WGS).** Independent clonal granddaughter lines were expanded ~1 month post-transduction and subjected to 30x Illumina WGS (NovaSeq 6000, 150×2 bp). Somatic single base substitutions (SBS) were called relative to the HAP1-TK-M9 mother clone's sequence using GATK3 + Mutect2. Signature analysis used COSMIC v3 references, deconstructSigs R package, NMF, and pentanucleotide enrichment scoring. Hairpin substrate biochemistry used purified recombinant A3A and A3B in single-hit kinetic assays on SDHB and NUP93 oligonucleotide substrates [@Carpenter2023].

**Tumor comparison.** 784 ICGC primary breast tumor WGS datasets were clustered based on pentanucleotide C→T/G mutation profiles and compared to the cell-line profiles to assign likely enzymatic sources [@Carpenter2023].

**A3 mRNA.** RNA-seq was used to compare exogenous A3 expression levels in granddaughter clones vs. TCGA breast tumors, CCLE cell lines, and published breast cancer datasets.

## Key Findings

1. **Both A3A and A3B generate genome-wide APOBEC3 signatures.** All 6/6 A3A-expressing granddaughter clones and 4/5 A3B-expressing clones showed significant APOBEC3 signature enrichment; neither catalytic mutant controls nor A3H (haplotypes I or II) did. NMF extracted a "Signature A" resembling SBS2/SBS13 only from A3A- and A3B-expressing clones.

2. **A3A generates ~4-fold more APOBEC3 signature mutations than A3B** over identical month-long experiments (6,070 vs. 1,528 unique SBSs from 6 and 5 clones, respectively). Part of this difference is attributed to the A3A expression level being ~5-fold higher than in breast tumors or cell lines (MND promoter effect), plus the higher intrinsic enzymatic activity of A3A.

3. **Distinct -2 position preferences.** A3A strongly prefers a pyrimidine (C or T) at the -2 position relative to the mutated cytosine — YTCW motifs in 72.7% of TC-context mutations. A3B shows only a weak YTCW preference (47.2% YTCW) and a corresponding enrichment for RTCW (52.8%). These preferences are consistent with yeast-based and murine model data for A3A, and contrast with published A3B-driven murine tumor data (~53% YTCW in mice vs. 47% here).

4. **Breast tumor clustering.** Unsupervised pentanucleotide clustering of 784 ICGC breast tumor WGS profiles against the HAP1-TK-M9 clonal profiles revealed three groups: (i) A3A-like (significant APOBEC3 signature, YTCW-biased), (ii) A3B-like (significant APOBEC3 signature, RTCW-biased), and (iii) no significant APOBEC3 signature. Most A3A-like breast tumors had YTCW percentages below the ~72.7% seen in HAP1-TK-M9 A3A clones, and most A3B-like tumors had YTCW fractions above the ~47.2% seen in A3B clones, consistent with combinatorial contributions of both enzymes in individual tumors.

5. **Mutations are genome-wide and mostly dispersed.** APOBEC3 SBS events were distributed throughout all chromosomes with no enrichment at top-100 cruciform/hairpin-prone genomic loci. However, both A3A and A3B showed elevated APOBEC3 signature mutation frequencies in predicted ssDNA loop regions of hairpin structures relative to non-catalytic controls (A3B significant at P=0.0367; A3A approaches significance at P=0.0655, limited by small clone number).

6. **Both enzymes cause kataegis.** Clear APOBEC3 kataegis events (≥2 APOBEC3 SBSs within 10 kbp) were observed in genomic DNA of both A3A and A3B-expressing clones; frequency did not differ significantly between the two (A3A: 4 events; A3B: 1 event; p=0.14).

7. **A3H dismissed as major contributor.** A3H-I and A3H-II (haplotype III / ΔAsn15 in this cell line background) failed to increase Gan^R mutation frequency or generate detectable APOBEC3 signature mutations in WGS of two A3H-I expressing clones.

8. **Hairpin biochemistry.** Purified A3A and A3B both deaminate ssDNA loop regions of SDHB and NUP93 hairpin substrates; A3A shows uniformly higher deamination rates. On NUP93, A3B deaminates the linear control efficiently but the hairpin only at low efficiency — suggesting substrate-specific differential hairpin usage between the two enzymes.

9. **Indel landscape unaffected.** Genome-wide insertion/deletion profiles (cosine similarity >0.96 across all conditions) were indistinguishable between A3A/A3B-expressing and control clones, consistent with SBS being the primary output of APOBEC3 activity.

## Relevance

This paper is directly relevant to **hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and** (agnostic covariate↔signature-exposure association; positive-control recovery of APOBEC3 aetiology):

- **H08a positive control, APOBEC3 arm.** H08a requires that an agnostic covariate association recovers APOBEC3 expression↔SBS2/13 within-tissue without being told the link. This study provides the gold-standard mechanistic warrant that A3A and A3B expression are genuine causal drivers of SBS2/SBS13, not mere correlates. It calibrates what "signal" to expect: A3A expression is a stronger per-unit predictor of YTCW-biased APOBEC3 mutations than A3B, while both contribute to the composite signal in real tumors. The H08a arm must therefore either test *A3A* and *A3B* mRNA jointly or use a combined APOBEC3A/B expression score to avoid underpowering on A3B alone.

- **Sub-signature resolution.** The YTCW vs. RTCW distinction between A3A and A3B means that the composite SBS2+SBS13 bucket in COSMIC is a mixture of (at least) two enzymatic sources. Any attempt in this project to attribute SBS2/13 exposure to a single covariate should account for this composite nature; pentanucleotide or YTCW/RTCW fractionation provides finer resolution.

- **A3A expression level caveat.** The study notes that exogenous A3A in HAP1-TK-M9 is ~5-fold over breast-tumor physiological levels; A3B expression approximates in vivo levels. For the hypothesis:0007 expression↔signature association, the relevant predictor is endogenous mRNA expression in the tumor being decomposed — the mechanistic dose-response established here justifies using endogenous A3A/B mRNA, while cautioning that in the model system A3A's apparent mutagenic potency may be inflated relative to in vivo conditions.

- **Cross-study mutation meta-analysis context.** In the cbioportal pipeline, per-study APOBEC3 mutation loads (TCW-context C→T/G ratios) are aggregated across studies. The finding that most breast tumors carry intermediate YTCW percentages attributable to combinatorial A3A+A3B activity means that study-level APOBEC3 signal will reflect whichever enzyme(s) are active in the dominant clones captured at sequencing — a source of inter-study variance not captured by a single COSMIC SBS2 or SBS13 attribution.

- **Kataegis as a qualitative APOBEC3 marker.** Both A3A and A3B produce kataegis in human cells; this supports using kataegis frequency or local mutation clustering as a supplementary APOBEC3 indicator alongside overall SBS2/13 burden in downstream analyses.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| SBS2 (C→T in TCW) | APOBEC3 signature — transition arm | COSMIC SBS2 |
| SBS13 (C→G in TCW) | APOBEC3 signature — transversion arm | COSMIC SBS13 |
| YTCW enrichment score | Sub-signature APOBEC3A proxy | ~72% in A3A clones; intermediate in tumors |
| RTCW enrichment score | Sub-signature APOBEC3B proxy | ~53% in A3B clones; intermediate in tumors |
| HAP1-TK-M9 granddaughter clones | Reference WGS (mechanistic positive control) | Not in cBioPortal; used for signature calibration |
| ICGC breast tumor WGS | Cross-study mutation data | Overlaps with cBioPortal breast cancer studies |
| Ganciclovir Gan^R frequency | Per-gene mutation rate reporter | Not used in pipeline; analogous to TMB in miniature |
| Kataegis events | Locally clustered mutations | Pipeline currently does not compute kataegis; relevant to hypermutator annotation |

## Limitations

- **A3A overexpression.** The MND promoter drives A3A at ~5-fold above physiological levels in breast tumors, which may inflate A3A's apparent mutagenic yield relative to A3B and complicate direct comparisons. A3B levels in the clones approximate tumor levels.
- **Near-diploid but aneuploid cell line.** HAP1-TK-M9 carries a reciprocal 9:22 translocation and lacks the Y chromosome; some chromosomal context effects may not generalize.
- **Small WGS clone number.** A3A WGS from n=6 clones, A3B from n=5, limits statistical power for hairpin-enrichment and kataegis comparisons.
- **Selection pressure on TK.** The ganciclovir-selected granddaughter clone analysis may enrich for rare APOBEC3 mutations at TC-rich positions within TK, overrepresenting hotspots relative to unselected genome-wide events — as the authors acknowledge by analogy to PIK3CA hotspots.
- **A3H dismissed but not excluded.** A3H haplotype I and II could not be rigorously tested because their expression in HAP1-TK-M9 is below the level needed to drive detectable DNA damage; the sole A3H allele in this cell line is the unstable ΔAsn15 haplotype III. A3H remains incompletely characterized.
- **No matched normal for HAP1.** Somatic mutations are called relative to the mother clone, not a germline normal; pre-existing somatic variation in HAP1 is excluded by design but constitutional HAP1 variants are not fully removed.
- **Breast cancer focus.** The tumor comparison is limited to ICGC breast cancer WGS; the generalizability of the YTCW/RTCW fractionation to other APOBEC3-enriched cancer types (bladder, cervix, lung, head/neck) is not directly tested.

## Model / Tool Availability

- All WGS data: NCBI BioProject PRJNA832427 (FASTQ and BAM)
- S2 Table: MAF file with all SBS mutations from the WGS described
- HAP1-TK-M9 cell line: available by contacting RSH (rsh@uthscsa.edu)
- MLV-A3 plasmid constructs (pRH9977–9986): available by contacting RSH
- Anti-A3A rabbit monoclonal antibody UMN-13: available by contacting RSH
- No standalone software tool released; analysis used MutationalPatterns, deconstructSigs, ggseqlogo, katdetectr, SigProfilerClusters (all standard R/Bioconductor packages)

## Follow-up

- **Read next:** Chan et al. 2015 (Nat Genet) on distinguishing A3A vs. A3B hypermutation signatures; Buisson et al. 2019 (Science) on APOBEC3A and mesoscale genomic features (passenger hotspots, hairpin loops); Petljak et al. 2022 (Nature) on CRISPR knockout mechanisms of APOBEC3 mutagenesis in cancer cell lines.
- **Questions for this project:**
  - Can the YTCW/RTCW pentanucleotide fractionation be computed from cBioPortal panel-sequencing data, or is it only reliable for WGS/WES-scale mutation counts?
  - Does stratifying APOBEC3 SBS2 vs. SBS13 attribution by YTCW fraction improve the expression↔signature association test in H08a?
  - The episodic vs. continuous APOBEC3 mutagenesis debate (Petljak 2019, Cell): do study-level cBioPortal mutation frequencies reflect a snapshot of an episodic process, inflating cross-study variance?
