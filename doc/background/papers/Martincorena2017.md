---
id: "paper:Martincorena2017"
type: "paper"
title: "Universal Patterns of Selection in Cancer and Somatic Tissues"
status: "read"
ontology_terms: []
datasets: []
source_refs: ["article:Martincorena2017"]
related: ["paper:Lawrence2014", "paper:Bailey2018", "topic:cancer-driver-genes"]
created: "2026-04-13"
updated: "2026-04-13"
---

# Universal Patterns of Selection in Cancer and Somatic Tissues

- **Authors:** Martincorena I, et al.
- **Year:** 2017
- **Journal:** Cell
- **PMID:** 29056346
- **DOI:** 10.1016/j.cell.2017.09.042
- **BibTeX key:** Martincorena2017

## Key Contribution

Introduces `dNdScv`, a maximum-likelihood dN/dS framework that detects positive selection by
comparing observed non-synonymous substitution counts against a neutral expectation derived from
synonymous mutations, corrected for trinucleotide context, gene length, and regional mutation-rate
covariates. The method's central methodological move is treating driver detection as a selection
problem (dN/dS >> 1) rather than a recurrence problem, which makes it sensitive to genes whose
drivers are spread across many distinct positions rather than concentrated in hotspots.

## Methods

The substitution model uses 192 rate classes (6 base changes x 16 trinucleotide contexts x 2
transcriptional strands) fit per cohort from synonymous sites. Per-gene expected mutation counts
are computed by summing these rates across each gene's coding sequence, giving a sequence-context
and length-aware neutral baseline. Four selection coefficients are estimated per gene: `wmis`
(missense), `wnon` (nonsense), `wspl` (essential splice), and `wind` (indels, fit via a separate
negative binomial regression). Gene-wise regional rate variation is captured by a negative-binomial
model whose prior is informed by 20 principal components of 169 epigenomic marks from RoadMap
Epigenomics; this constrains per-gene rates via a Gamma prior and borrows strength between global
covariates and local synonymous counts. Significance is a likelihood-ratio test of w=1.
Cohort: 7,664 TCGA tumors across 29 cancer types, re-called in-house for 24 types to control
germline-leakage artifacts (samples with <50% concordance to public calls dropped). Hypermutators
(>3,000 coding mutations) are excluded from cohort fits; POLE/MMR tumors are handled with extended
pentanucleotide contexts and per-signature normalization to avoid inflated backgrounds.

## Key Findings

Across 7,664 tumors, dNdScv identifies **179 significant driver genes at 5% FDR** pan-cancer, of
which ~54% overlap the Cancer Gene Census. The estimated number of coding drivers per tumor varies
~10-fold by lineage: <1 in thyroid/testicular/sarcoma, 3-4 in breast/bladder, >10 in colorectal
and endometrial. Crucially, roughly **half of all positively-selected coding mutations fall outside
the existing ~369-gene reference set**, implying many drivers remain uncataloged. The
covariate-informed background model (vs. a local-only or uniform model) gives dNdScv better
sensitivity on small cohorts and better specificity on neutral simulations (dNdSunif produced 368
false positives at q<0.05). Novel candidates flagged via truncating-mutation enrichment despite
modest recurrence include `ZFP36L1/L2`, `KANSL1`, `BMPR2`, `MAP2K7`, and `NIPBL` — exactly the
regime where recurrence-based tests lose power. The other headline result: **dN/dS ~= 1 across
essentially all of the genome in both tumors and normal somatic tissues** (blood, skin, colon,
liver, small intestine, from cited companion studies), with <1 coding substitution per tumor
removed by negative selection. Purifying selection is detectable only in essential genes in
haploid regions (dN/dS = 0.66). Positive selection thus dominates somatic evolution, malignant or
not.

## Relevance

Introduces the dNdScv method — selection-based driver detection that uses the dN/dS ratio
(non-synonymous vs synonymous substitution rates) corrected for trinucleotide context and gene
length. Methodologically complementary to recurrence-based methods (Lawrence2014 MutSigCV,
Bailey2018 consensus): a gene can be under positive selection without being recurrently mutated
in a single hotspot, and vice versa. Useful comparison axis for our gene-frequency outputs.

## Limitations

- **Coding SNVs + small indels only.** Copy-number drivers, structural variants, and fusions are
  not scored — a dN/dS framework is undefined for these classes.
- **Non-coding drivers not captured.** The framework depends on the synonymous/non-synonymous
  contrast, so promoter, UTR, enhancer, and intronic drivers are out of scope in this paper.
- **Power floor for rare drivers.** Genes with very low driver-mutation frequency require large
  cohorts; in small cohorts the Gamma prior helps but does not fully rescue detection.
- **Germline contamination sensitivity.** Even 1-3% germline SNP leakage artifactually depresses
  dN/dS; five TCGA cancer types had to be reverted to public calls because in-house re-calls were
  too permissive.
- **Cohort-level, not patient-level.** `w` values are cohort averages; labeling an individual
  mutation as driver vs. passenger in one tumor needs additional per-sample signature modeling.
- **Negative selection largely undetectable,** which limits the method as a tool for finding
  essential or haploinsufficient genes in somatic data.

## Follow-up

- **Lawrence2014 (MutSigCV)** — the recurrence-plus-covariate predecessor dNdScv is implicitly
  benchmarked against.
- **Bailey2018** — PanCanAtlas consensus driver list that combined dNdScv with multiple other
  callers (MutSig2CV, OncodriveFML, 20/20+, etc.), used as the community-level driver catalog.
- **Martincorena2015 (skin)** and **Martincorena2018 (esophagus)** — companion studies applying
  dNdScv to normal epithelia, establishing the surprising result that driver-gene positive
  selection is detectable in physiologically normal tissue.
- **Successors / extensions:** `dndscv` has been extended with `sitednds` for site-level selection,
  and combined with hotspot methods in later pan-cancer analyses. R package at
  `github.com/im3sanger/dndscv`.
