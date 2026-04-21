---
id: "paper:Alexandrov2020"
type: "paper"
title: "The repertoire of mutational signatures in human cancer"
status: "read"
ontology_terms: []
datasets: ["cosmic-signatures"]
source_refs: ["cite:Alexandrov2020"]
related: ["paper:Tate2019", "paper:PCAWG2020", "topic:mutational-signatures"]
created: "2026-04-13"
updated: "2026-04-12"
---

# The repertoire of mutational signatures in human cancer

- **Authors:** Alexandrov LB, et al.
- **Year:** 2020
- **Journal:** Nature
- **PMID:** 32025018
- **DOI:** 10.1038/s41586-020-1943-3
- **BibTeX key:** Alexandrov2020

## Key Contribution

Establishes the COSMIC v3 reference catalog of mutational signatures by re-analyzing
~24k tumors with the SigProfiler NMF pipeline, expanding beyond the SBS-only v2 catalog
(Alexandrov 2013) to include doublet-base substitutions (DBS) and small insertions/deletions
(ID), and providing curated etiological annotations for each signature.

## Methods

- **Cohort:** 23,829 samples — 2,780 PCAWG whole genomes, 1,865 additional WGS, and
  19,184 exomes — yielding ~79.8M SBSs, ~814k DBSs, and ~4.1M indels (~10x prior studies).
- **SBS framework:** primary classification uses 96 trinucleotide contexts (6 pyrimidine
  substitutions × 16 flanking 5'/3' base combinations); extended analyses use 1,536 classes
  (two flanking bases each side) and 192 classes (transcribed-strand bias).
- **DBS framework:** 78 doublet-base classes capturing paired-base substitution patterns.
- **ID framework:** 83 indel classes encoding insertion vs. deletion, single-base C/T calls,
  mononucleotide repeat tract length, repeat count, and microhomology length at deletion
  boundaries.
- **Signature extraction:** NMF (SigProfilerExtractor) factorizes the mutation-count matrix
  into signature profiles × per-sample exposures. A parallel SignatureAnalyzer (Bayesian
  NMF) pipeline cross-validates results. Extraction is run separately on hypermutated and
  low-burden strata; signatures are clustered, deduplicated, and curated against prior
  experimental evidence and DNA damage/repair literature.
- **Attribution:** per-sample exposures derived as part of NMF factorization, with a
  separate constrained refit that assigns each signature's mutation contribution while
  penalizing biologically implausible small contributions.

## Key Findings

- **Signature counts (v3 release):** 67 SBS signatures extracted (49 deemed biologically
  plausible after curation), 11 DBS signatures, 17 ID signatures, plus 4
  clustered-substitution signatures.
- **Backwards compatibility:** all v2 SBS signatures reproduced except SBS25 (a
  cell-line-only artifact). Several v2 signatures resolved into finer-grained
  constituents — e.g., SBS17 splits into SBS17a/SBS17b — reflecting better separation of
  partially correlated processes.
- **Validated etiologies:** signatures with strong mechanistic support include SBS1
  (5mC deamination/aging), SBS4 (tobacco smoking), SBS7a-d (UV), SBS2/SBS13 (APOBEC),
  SBS6/SBS15/SBS20/SBS26 (MMR deficiency), SBS3 (HRD), SBS10a/b (POLE), and several
  chemotherapy signatures (platinum, temozolomide, 5-FU).
- **Putative/unknown etiologies:** ~half of SBS signatures lack a confirmed cause; the
  authors flag "flat" featureless signatures as mathematically hard to deconvolute and
  potentially conflated with sequencing artifacts.
- **Novel discoveries:** new SBS signatures linked to tobacco-chewing, aristolochic acid
  exposure variants, additional chemotherapy agents, and several POLE/POLD1 subtypes;
  the DBS and ID catalogs are entirely new (e.g., DBS2 = tobacco, DBS5 = platinum,
  ID1/ID2 = polymerase slippage at mononucleotide tracts, ID6 = HRD-associated MH-mediated
  deletions, ID8 = NHEJ).
- **Per-cancer exposures:** signature activities are tabulated per cancer type, providing
  reference distributions (e.g., UV signatures dominate melanoma, smoking dominates
  lung adenocarcinoma, APOBEC active across bladder/cervical/breast).

## Limitations

- **NMF non-uniqueness:** mutation spectra in a given sample can be reconstructed by many
  signature combinations, especially when burden is low or many candidate signatures
  overlap; choice of rank (signature count) is not fully algorithmic.
- **Method discordance:** SigProfiler vs. SignatureAnalyzer disagree on hypermutator
  decomposition (13 vs. 25 SBS signatures), illustrating residual subjectivity.
- **Artifact contamination:** sequencing/calling differences themselves generate
  spurious signatures; curation against artifacts is manual.
- **Power requirement:** WGS provides "many-fold-greater" mutation counts, enabling
  separation of correlated signatures and detection of low-contribution processes —
  implying weaker performance on exome and especially panel data.
- **Etiology gaps:** many signatures remain idiopathic; experimental validation lags
  computational discovery.

## Relevance

Defines the COSMIC v3 catalog of mutational signatures (SBS, DBS, ID) — the field-standard
reference for decomposing tumor mutation spectra into reproducible processes (aging, smoking, UV,
APOBEC, MMR/HRD deficiency, chemotherapy). Out-of-scope for the current pipeline but foundational
background for any future signature-decomposition extension.

## Follow-up

- COSMIC v3.x point releases (v3.1, v3.2, v3.3) refine signatures and add new ones; check
  current Tate2019 / COSMIC release notes for the active catalog.
- Degasperi et al. 2022 (Science) extends signatures using 12k WGS from Genomics England
  100,000 Genomes Project — relevant if extending beyond PCAWG.
- Tool comparison: SigProfilerAssignment (refit) vs. lighter-weight per-sample fitters
  (deconstructSigs, sigfit, MutationalPatterns, YAPSA) for cBioPortal-scale aggregation.
- Panel-data feasibility: SigMA (Gulhan et al. 2019) is purpose-built for low-mutation-count
  panel/exome data and worth evaluating for MSK-IMPACT-style cohorts.
