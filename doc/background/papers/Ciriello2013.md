---
id: paper:Ciriello2013
type: paper
title: Emerging landscape of oncogenic signatures across human cancers
status: read
ontology_terms: []
source_refs:
- article:Ciriello2013
related:
- paper:SanchezVega2018
- paper:Kandoth2013
- topic:pan-cancer-mutation-landscape
created: '2026-04-13'
updated: '2026-04-13'
---

# Emerging landscape of oncogenic signatures across human cancers

- **Authors:** Ciriello G, Miller ML, Aksoy BA, Senbabaoglu Y, Schultz N, Sander C
- **Year:** 2013
- **Journal:** Nature Genetics
- **PMID:** 24071851
- **PMCID:** PMC4320046
- **DOI:** 10.1038/ng.2762

## Key Contribution

First pan-cancer attempt to classify tumors by *type of oncogenic alteration* rather than
tissue of origin. Distills thousands of genomic features down to ~500 "selected functional
events" (SFEs) and shows that 3,299 TCGA tumors across 12 cancer types fall along an
inverse mutation-vs-aneuploidy axis ("cancer genome hyperbola"), splitting into a
mutation-driven **M class** and a copy-number–driven **C class**, each further resolved into
tissue-spanning oncogenic-signature subclasses.

## Methods

**Sample assembly.** 3,299 tumors from 12 TCGA cancer types: BLCA (97), BRCA (488),
COADREAD (491), GBM (218), HNSC (302), KIRC (420), LAML (184), LUAD (229), LUSC (182),
OV (446), UCEC (242) — plus a stratified subtype layer for BRCA (basal/HER2/luminal),
COADREAD (MSI/non-MSI), and UCEC (endometrioid/serous). A held-out validation cohort
added 907 samples from 6 additional cancer types.

**Selected Functional Events (SFEs).** Final feature set = 479 events:
- **116 amplifications + 151 deletions** — GISTIC peaks on Affymetrix SNP 6.0; overlapping
  peaks merged at >=80% concordance; *only* high-level events scored (GISTIC +2 / -2).
- **199 recurrently mutated genes** — all mutations counted equally except in
  hypermutator samples (MSI, POLE-mutant), where only truncating mutations and hotspot
  missense (>=3 events at the same residue) were retained, to suppress passenger inflation.
- **13 epigenetically silenced genes** — selected from prior silencing literature, requiring
  promoter hypermethylation (beta > 0.1) plus concordant mRNA downregulation.

**Classification.** Recursive network-modularity clustering on the binary
sample-by-SFE matrix yielded an unsupervised hierarchical partition. Robustness was
checked by random subsampling at 5%, 20%, and 50% removal.

**M vs C scoring.** The M/C partition is *emergent* from the modularity decomposition,
not a prior-defined cutoff: clusters dominated by point mutations land in the M branch;
clusters dominated by recurrent SCNAs land in the C branch. TP53 mutation is the notable
exception that tracks with C-class membership (consistent with TP53 loss enabling
chromosomal instability).

## Key Findings

**The cancer-genome hyperbola.** Across the cohort, somatic mutation count and SCNA
burden are anti-correlated: highly altered tumors lie on one of two hyperbolic arms,
either mutation-rich (M) or aneuploid (C), but rarely both. The pattern holds within
individual tumor types and reproduces in the validation cohort.

**M class = mutation-driven (17 subclasses, M1–M17).** Predominantly:
- KIRC (VHL/PBRM1 axis), GBM, LAML (NPM1/FLT3/DNMT3A), most COADREAD, and the
  endometrioid (non-serous) UCEC.
- Subclasses M1–M8 are organized around PI3K–AKT–PTEN signaling alterations.
- Subclasses M9–M14 are organized around APC / TP53 / KRAS combinations
  (colorectal-like).
- Recurrent hotspot mutations in chromatin modifiers (ARID1A, CTCF) prominent in
  hypermutated endometrial tumors.

**C class = copy-number-driven (14 subclasses, C1–C14).** Predominantly:
- Nearly all OV, nearly all BRCA, large fractions of LUSC, HNSC, and serous UCEC.
- C1–C6 lack chr8 gain/loss; differentiated by TP53 + CDKN2A deletion (C3,
  lung/HNSC squamous) vs. CCND1 amplification (C4, alternate cell-cycle bypass).
- C7–C14 carry the heaviest aneuploidy, including 8q24 MYC amplification.
- C13 = BRCA1/BRCA2 inactivation (basal-like breast + ovarian).
- C14 = AURKA amplification.

**Tissue-of-origin recedes at the top of the hierarchy.** The major split is alteration-type,
not tissue. Tissue-specific events (EGFR amp in GBM, NPM1 in LAML, VHL in KIRC) only
appear at lower hierarchy levels. Conversely, lung-squamous and head/neck-squamous tumors
co-cluster in C3/C4 via shared TP53 + 3q26 + CCND1 alterations — an early articulation of
the squamous "pan-tissue" signature later formalized by Hoadley.

**Therapeutic framing.** Subclass-level signatures suggest cross-tissue basket-trial
designs: PI3K + cell-cycle co-inhibition for C3/C4, PARP + Aurora-A inhibition for
C13/C14 BRCA1/2-deficient tumors.

## Relevance

Early pan-cancer oncogenic-event landscape paper from 2013 — establishes the M class
(mutation-driven) vs C class (copy-number-driven) framing that became influential in subsequent
pan-cancer work. Historical context for the pathway-level analyses (Sanchez-Vega 2018) and
methodologically a peer of Kandoth 2013.

## Limitations

- Only 12 tumor types; only one hematologic malignancy (LAML), so heme-specific
  alteration patterns are underrepresented.
- Sample sizes vary 5x across types (97–491), biasing modularity toward larger cohorts.
- SFE selection is conservative: only high-level (GISTIC +/-2) SCNAs and prior-supported
  epigenetic events are scored, so non-focal arm-level aneuploidy and most methylation
  events are absent from the classifier.
- Translocations / structural variants beyond CNV breakpoints are not modeled — limiting
  applicability to fusion-driven cancers.
- The SFE catalog inherits all gene-level driver-calling assumptions (significance from
  GISTIC and MutSig-class methods); novel non-coding or regulatory drivers are missed.
- Authors note results would improve as ICGC data tripled the cohort within ~2 years.

## Follow-up

- **Pathway-level reformulation:** Sanchez-Vega 2018 reframes the same TCGA substrate
  through 10 canonical signaling pathways instead of SFE modules.
- **Cell-of-origin reclassification:** Hoadley 2018 (iCluster across 33 TCGA types) shows
  that when *multi-omics* features (methylation, miRNA, mRNA, protein) are added to DNA,
  ~2/3 of tumors re-cluster by tissue/cell-of-origin rather than by mutation-vs-CNA axis —
  partially walking back the strong "alteration-type beats tissue" claim, while preserving
  the squamous, basal, and pan-GI clusters Ciriello first surfaced.
- **Cross-tumor basket trials:** the C13 BRCA-deficient subclass anticipated PARP-inhibitor
  basket eligibility; C3/C4 squamous subclass motivated PI3K + CDK4/6 combination concepts.
- **Mutation-burden axis:** the hyperbola observation prefigured later work on hypermutator
  phenotypes (MSI, POLE) and immunotherapy response stratification.
