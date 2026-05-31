---
id: "topic:pan-cancer-signature-catalogs"
type: "topic"
title: "Pan-cancer mutational-signature catalogs and reference sets"
status: "active"
ontology_terms:
  - mutational signatures
  - single-base substitution
  - doublet-base substitution
  - insertion-deletion
  - COSMIC
  - NMF
  - pan-cancer
  - DNA damage and repair
  - somatic mutation
  - signature aetiology
datasets: []
source_refs:
  - "cite:Alexandrov2020"
  - "cite:Degasperi2022"
  - "cite:Everall2026"
  - "cite:Koh2025"
  - "cite:Kucab2019"
  - "cite:Otlu2023"
  - "cite:Pleasance2020"
  - "cite:Thatikonda2023"
related:
  - "paper:Alexandrov2020"
  - "paper:Degasperi2022"
  - "paper:Everall2026"
  - "paper:Koh2025"
  - "paper:Kucab2019"
  - "paper:Otlu2023"
  - "paper:Pleasance2020"
  - "paper:Thatikonda2023"
  - "hypothesis:h08-agnostic-covariate-association-recovers-known-signature-aetiologies-and"
  - "method:h08-agnostic-association-model"
created: "2026-05-31"
updated: "2026-05-31"
---

# Pan-cancer mutational-signature catalogs and reference sets

## Summary

Somatic mutations accumulate through recognizable, tissue-varying processes whose composite spectral
fingerprints — mutational signatures — can be decomposed from trinucleotide-context mutation counts
using NMF or related methods. Over the past decade a succession of large WGS cohorts has generated
an expanding COSMIC reference catalog: PCAWG established 49 SBS, 11 DBS, and 17 ID signatures
(paper:Alexandrov2020); GEL-based analysis added 40 SBS and 18 DBS signatures and introduced a
principled common-vs-rare fitting framework (paper:Degasperi2022); a joint five-mutation-class
extraction from 100KGP added structural variant signatures and 26 further entries (paper:Everall2026);
and a redesigned 89-channel InDel taxonomy resolved long-standing ambiguities in MMR vs. polymerase
proofreading signals (paper:Koh2025). Complementary resources fix the experimental ground truth —
an iPSC compendium of 79 carcinogens links specific agents to spectral profiles (paper:Kucab2019),
genome topography maps all COSMIC v3.3 signatures against 516 ENCODE features (paper:Otlu2023),
and clinical cohorts have documented therapy-induced and population-specific signatures in advanced
tumors (paper:Pleasance2020) and pediatric cancers (paper:Thatikonda2023).

## Key Concepts

**Mutational signature:** A characteristic pattern of somatic mutation counts across trinucleotide
(or broader) sequence contexts, interpretable as the fingerprint of a DNA-damaging or repair
process. NMF decomposes a sample-by-mutation-channel matrix M ≈ W × H, where W columns are
signature profiles and H rows are per-sample exposures.

**COSMIC reference catalog:** The versioned, publicly maintained collection of human tumor-derived
signatures; COSMIC v3 (paper:Alexandrov2020) is the current primary reference for restricted
assignment, with v3.3 (paper:Otlu2023) and ongoing additions (paper:Everall2026,
paper:Degasperi2022) extending it.

**Restricted assignment vs. de novo extraction:** Restricted assignment fits known COSMIC profiles
to a new sample set (lower noise, interpretable); de novo extraction allows the data to define new
signatures (higher discovery potential, higher false-positive rate for small cohorts).

**Common vs. rare signature structure:** Each organ has 5–10 stable "common" signatures plus a
sample-size-dependent tail of rare ones (paper:Degasperi2022). Panel-sequenced studies typically
recover only the common layer.

**FitMS (Fit Multi-Step):** A two-step restricted fitting algorithm that first assigns organ-specific
common signatures, then attempts rare-signature detection on high-residual samples
(paper:Degasperi2022). Outperforms single-step fitting in simulation studies.

**Aetiology tiers:** Signatures range from experimentally validated (UV→SBS7, BaP/tobacco→SBS4,
aristolochic acid→SBS22, each with causal iPSC evidence — paper:Kucab2019) through well-supported
epidemiological association (APOBEC3→SBS2/13, MMR-loss→SBS6/15/26/44, POLE→SBS10a/b) to proposed
or unknown (SBS5, SBS8, SBS17a/b, SBS40, and many DBS/ID signatures).

## Current State of Knowledge

### Established consensus signatures and aetiologies

The four "positive-control" signature clusters relevant to hypothesis h08 have multi-study
convergent support:

- **UV / SBS7a-d (+ DBS1, ID13):** Restricted to skin/melanoma; transcriptional strand bias
  indicating NER; clonal timing consistent with early exposure (paper:Alexandrov2020,
  paper:Everall2026). Experimentally confirmed in iPSC simulated-solar-radiation assay with cosine
  similarity 0.91 to tumor-derived profiles (paper:Kucab2019). Topographic enrichment on
  untranscribed strand, highest strand-coordinated mutagenesis of any signature (paper:Otlu2023).

- **Tobacco smoke / SBS4 (+ DBS2, ID3):** Enriched in lung and head-and-neck;
  benzo[a]pyrene-diol-epoxide experimentally generates a profile with cosine similarity 0.84–0.95
  to SBS4 (paper:Kucab2019); TC-NER transcriptional strand asymmetry on transcribed strand
  (paper:Otlu2023); clonal (early) timing (paper:Everall2026); also found at <1% in metastases to
  CNS, breast, colorectal (paper:Degasperi2022).

- **APOBEC3 / SBS2 + SBS13 (+ DBS11, InD9a):** Prevalent across bladder, head-and-neck, breast,
  lung; APOBEC3A and APOBEC3B cytidine deaminase activity well established; mechanistically
  grounded in lagging-strand ssDNA exposure (consistent lagging replication strand bias in all
  cancer types — paper:Otlu2023). Predominantly subclonal in breast, colorectal, lung
  (paper:Everall2026). Tamoxifen treatment in breast cancer elevates SBS2 with concomitant APOBEC3A
  mRNA increase (paper:Pleasance2020). TP53-mutated pediatric tumors show elevated SBS2, consistent
  with p53 suppression of APOBEC3B (paper:Thatikonda2023). A parallel InDel signal (InD9a) via
  UNG abasic-site slippage provides an independent confirmatory channel (paper:Koh2025).

- **MMR-deficiency / MSI / SBS6, 15, 26, 44 (+ multiple DBS/ID):** Four well-validated MMR-loss
  signatures; linked to MSH6, MLH1, MSH2, PMS2 inactivation; also present at <1% across many
  non-colorectal/uterine tumor types (paper:Degasperi2022); POLE mutations drive SBS10a/b
  hypermutation in uterine/CRC; strong depletion of SBS15 at CTCF binding sites (paper:Otlu2023);
  PRRDetect AUROC 1.0 classifies MMRd vs. POLE-dysfunction via a 89-channel InDel taxonomy
  (paper:Koh2025).

### Catalog expansion and fragmentation

The COSMIC catalog has grown from ~30 SBS (v2) to 49 SBS (v3, paper:Alexandrov2020) to >80 SBS
reference signatures after GEL analysis (paper:Degasperi2022), to 67 SBS + 19 DBS + 18 ID + 20 CN
+ 10 SV in the 100KGP joint extraction (paper:Everall2026). This growth reflects both genuine
biological discovery and an artifact of sample-size scaling: rare signatures accumulate in the tail
as cohort size grows, and their count is sample-size-dependent rather than biology-limited
(paper:Degasperi2022). A substantial fraction of the catalog remains mechanistically unexplained —
SBS5, SBS8, SBS12, SBS16, SBS17a/b, SBS39, SBS40, and many DBS/ID signatures — despite systematic
association attempts.

Crucially, paper:Everall2026 demonstrates that 66 of 42 current COSMIC SBS signatures can be
produced as linear combinations of others (cosine similarity >0.8), creating a redundancy problem
that has no accepted solution yet. Paper:Degasperi2022 showed that several previously catalogued DBS
signatures (DBS3, DBS10, DBS12, DBS14, DBS29, DBS37) are mathematical artefacts of adjacent SBS
events in hypermutators, not genuine dinucleotide processes.

### Topographic and mechanistic annotations

Paper:Otlu2023 established that genomic topography is highly informative for signature etiology
assignment: exogenous mutagens show transcriptional strand bias (TC-NER footprint), APOBEC shows
lagging replication strand enrichment, polymerase-proofreading defects show replication strand bias,
and clock-like SBS1 closely mimics a simulated null. SBS17a/b — among the most prevalent signatures
of unknown etiology — show a striking enrichment at CTCF binding sites in all cancer types,
suggesting chromatin organization is mechanistically involved; paper:Otlu2023 also identified that
topographic analysis can split apparently unified signatures (SBS28 → SBS28a/b), revealing hidden
process heterogeneity.

### Population-specific and specialty-population catalogs

Paper:Degasperi2022 identified aristolochic acid signature SBS22 in UK renal cancers from patients
of ethnic-minority ancestry (possibly low-level undisclosed AAI exposure). Paper:Everall2026
identified SBS88 (colibactin from pks+ E. coli) enriched in rectal vs. colon cancers, active early
in life and concordant with rising early-onset CRC. Paper:Thatikonda2023 demonstrated that
pediatric tumors operate with a substantially smaller active signature repertoire (29 SBS vs >40 in
adults), dominated by clock-like processes and with very few MH-associated long deletions; a novel
pediatric-leukemia-restricted InDel signature IDN with clock-like correlates was identified by all
three independent extraction methods. Paper:Pleasance2020 documented therapy-associated signatures
(SBS31/DBS5 with platinum; SBS17b with platinum + DNA-synthesis inhibitor combination; ID8 with
radiation) in advanced post-treatment tumors, with error-prone polymerases POLQ and Polζ mediating
part of the treatment-induced mutagenesis.

## Controversies and Open Questions

### Settled vs. contested aetiologies

Settled (experimental causal evidence): UV→SBS7, tobacco/BaP→SBS4, aristolochic acid→SBS22,
cisplatin/oxaliplatin→SBS31/DBS5 (all from paper:Kucab2019 + clinical confirmation). APOBEC3→SBS2/13
is settled at the association level; mechanistic details (APOBEC3A vs. APOBEC3B dominance,
replication timing, nuclear vs. cytoplasmic activity) remain actively debated. MMR-loss→SBS6/15/26/44
is established; the direction of causation (MMR loss first, or mutational load drives MMR
inactivation) is sometimes contested in individual cases.

Unsettled: SBS5 (clock-like, associated with replication) and SBS40 (broadly flat) both correlate
with age and SV count but have no molecular-mechanistic explanation despite their pan-cancer
ubiquity. SBS8 shows a chromothripsis association (paper:Thatikonda2023) and HRD co-occurrence
but no definitive mechanistic cause. SBS16 shows an alcohol association by epidemiology with
transcriptional strand bias suggesting adduct-based origin, but no experimental confirmation.
SBS17a/b's CTCF-binding-site enrichment is unexplained and constitutes a genuine open question
for the field (paper:Otlu2023).

### Methodological tensions

**NMF rank selection and tool choice.** SigProfilerExtractor and SignatureAnalyzer agree for most
signatures but diverge substantially for flat/featureless signatures (SBS5/40-related space) and
for hypermutated sample decompositions — 13 vs. 25 SBS signatures extracted from hypermutated PCAWG
samples (paper:Alexandrov2020). No consensus exists for choosing extraction rank in small or
panel-sequenced cohorts.

**Restricted assignment vs. de novo extraction.** Restricted fitting to a reference catalog controls
false positives but can miss genuinely novel signatures, particularly in understudied cancer types
or post-treatment cohorts where novel processes are likely (paper:Pleasance2020 novel MSBS1–6;
paper:Thatikonda2023 IDN). De novo extraction from small cohorts produces unstable solutions.

**InDel taxonomy adequacy.** COSMIC-83 InDel channels conflate biologically distinct PRRd subtypes
(MMR-loss vs. POLE dysfunction vs. POLD1 dysfunction), producing cosine similarities >0.89 between
distinct mechanistic signatures (paper:Koh2025). The new 89-channel taxonomy resolves this but has
not yet been incorporated into the COSMIC standard or widely adopted in analysis pipelines. This
means that most published InDel signature analyses, including COSMIC-based studies, may
systematically misassign some MMR- and polymerase-driven signals.

**Catalog redundancy and linear dependence.** More than half of COSMIC SBS signatures can be
produced as linear combinations of other catalog entries (paper:Everall2026). Restricted assignment
using a redundant catalog may produce non-unique solutions, making per-sample signature exposures
poorly identified. No authoritative resolution has been proposed.

**Tissue-specific vs. pan-cancer signatures.** Paper:Degasperi2022 shows that organ-specific
reference signatures outperform cross-organ averages (COSMIC reference) for per-sample fitting;
using COSMIC directly on tissue-specific cohorts inflates fitting residuals and may misattribute
exposures. The cbioportal pipeline's restricted SigProfiler assignment uses the standard COSMIC
reference, which is the main practical tension.

**DBS artefact identification.** Paper:Degasperi2022 demonstrated several COSMIC DBS signatures are
mathematical artefacts, not biological processes. Naive inclusion of the full DBS catalog in
restricted assignment could produce spurious associations with artefactual signatures.

**Therapy contamination vs. intrinsic hypermutation.** Advanced-tumor cohorts (paper:Pleasance2020)
show that long genotoxic therapy elevates TMB ~twofold and induces specific signatures (SBS31/DBS5,
SBS17b), while error-prone polymerases POLQ and Polζ amplify this effect. Hypermutator annotation
pipelines that rely solely on POLE/POLD1 hotspots and MSI will mis-classify therapy-induced
hypermutators as "unknown" rather than treatment-associated — a calibration gap for any pipeline
including the cbioportal TMB/hypermutator annotation.

**Pediatric vs. adult signature space.** Pediatric tumors carry far fewer active processes, a
smaller signature repertoire, and different clock-like proportions (paper:Thatikonda2023). Mixed
pediatric-adult cohorts require age stratification for meaningful signature decomposition; the IDN
leukemia signature has no adult COSMIC equivalent, suggesting either genuine developmental
restriction or a detection gap in adult studies.

## Relevance to This Project

### Implications for h08 and the cross-study signature-aetiology aggregation

**Hypothesis h08** proposes an agnostic within-tissue covariate–signature-exposure association that
must recover known aetiologies (UV/SBS7, smoking/SBS4, APOBEC/SBS2–13, MMR/MSI) as a positive
control tier before any novel discovery claim can be taken seriously. The pan-cancer catalog
literature grounds every aspect of this design.

**The positive-control set for H08a** (recovery arm) is precisely defined by the consensus across
paper:Alexandrov2020, paper:Degasperi2022, paper:Everall2026, and paper:Kucab2019: the four main
exposure–signature links (UV→SBS7, smoking→SBS4, APOBEC3→SBS2/13, MMR-loss→SBS6/15/26/44) have
multi-study, multi-method confirmation including experimental causal evidence (Kucab). The agnostic
scan should recover these associations at FDR q<0.05 within appropriate tissue strata as a
minimum pass criterion. The canonical "known map" is the systematic regression of signatures against
histology, repair gene inactivation, and therapy from paper:Everall2026, which provides ground-truth
expected directionality and effect sizes.

**APOBEC as a specific H08a test case:** The lagging-strand replication enrichment of SBS2/13
(paper:Otlu2023), the tamoxifen→APOBEC3A mRNA elevation (paper:Pleasance2020), and the
TP53→APOBEC3B suppression signal in pediatric tumors (paper:Thatikonda2023) together triangulate
that APOBEC3A/B mRNA expression is a strong within-tissue positive-control covariate. InD9a from
paper:Koh2025 provides an independent InDel-layer confirmatory signal.

**The discovery prong (H08b)** should target the signatures with unknown or only partially
explained aetiologies: SBS5, SBS8, SBS12, SBS16, SBS17a/b, SBS40, the 40 new signatures from
paper:Degasperi2022 (SBS120–SBS137), MSBS1–6 from paper:Pleasance2020, and the 26 new
signatures from paper:Everall2026. The CTCF-site enrichment of SBS17a/b (paper:Otlu2023) and the
chromothripsis-SBS8 association (paper:Thatikonda2023) represent structured prior constraints that
can focus the covariate search.

**Panel-sequencing constraint:** cBioPortal studies are predominantly panel- or exome-sequenced.
Paper:Degasperi2022's finding that panel studies recover only 5–10 common signatures (rare
signatures require WGS scale) directly bounds what h08 can achieve on cBioPortal data. The
positive-control tier (UV/smoking/APOBEC/MMR) corresponds precisely to the common-signature tier
and should be robustly recoverable. H08b discovery of unknown signatures requires either MC3/PCAWG
substrates or a cross-study pooled cohort large enough to accumulate WGS-equivalent mutation counts
per signature. This tension is the subject of question:q018 (feasibility of downstream signature
decomposition) and question:q019 (de novo extraction on the aggregated cohort).

**Age as mandatory nuisance covariate:** SBS1, SBS5, and SBS40 all correlate with age across
multiple cancer types (paper:Alexandrov2020, paper:Thatikonda2023). Any agnostic covariate scan
must residualize or include age to avoid confounding clock-like signature variation with true
exposure signals. This is a binding design constraint for the h08 pre-registration.

**Hypermutator annotation calibration:** The pipeline annotates hypermutators via POLE/POLD1
hotspots, MSI-H status, and GMM-based TMB thresholding. Paper:Pleasance2020 shows that
therapy-induced mutagenesis (SBS31/DBS5, SBS17b, error-prone polymerases) is a distinct cause of
elevated TMB that is not captured by this scheme; paper:Koh2025 shows that PRRDetect outperforms
all current hotspot- and TMB-based classifiers for PRRd detection. These findings suggest the
current `annotate_hypermutators.py` pipeline may systematically misclassify a fraction of treated
samples. Paper:Degasperi2022 warns additionally that several DBS signatures in restricted assignment
panels may be mathematical artefacts — the `run_restricted_sigprofiler_assignment.py` step should
exclude flagged artefactual DBS signatures.

**COSMIC version and catalog update:** The pipeline currently references COSMIC v3 (as defined by
paper:Alexandrov2020). Paper:Everall2026 adds 26 new signatures (SBS96–98, DBS12–19, ID19–22,
CN25, SV1–10) and paper:Degasperi2022 adds 40 SBS and 18 DBS. Depending on the COSMIC version used
by `run_restricted_sigprofiler_assignment.py`, some newly documented signatures (especially
SBS96–98) may be absent from the reference panel, potentially causing their exposures to be
absorbed by nearest-neighbor signatures. This should be checked before finalizing the h08
association results.

**Cross-study confounders specific to the meta-analysis context:**
- Therapy-induced signatures (SBS31/DBS5 platinum, SBS17b combination therapy, ID8 radiation —
  paper:Pleasance2020) inflate signature exposures in treated metastatic cohorts. The
  `matched_normal_studies` config list should ideally be extended to flag not just matched-normal
  design but also treatment-naive status, which is unavailable for most cBioPortal studies.
- The clonality timing evidence from paper:Everall2026 (exogenous signatures more clonal, APOBEC
  subclonal) predicts that APOBEC signals will be more variable across sampling biopsies, inflating
  cross-study variance for that arm.
- Pediatric-specific signals (IDN, paper:Thatikonda2023) and population-specific signals
  (aristolochic acid, colibactin) will appear as cancer-type-specific outliers in the cross-study
  mutation-frequency tables; these are not confounders but features for H08b discovery.

## Key References

- paper:Alexandrov2020 — Primary COSMIC v3 catalog; positive-control signature definitions for h08.
- paper:Degasperi2022 — Expanded catalog + FitMS; common-vs-rare framework; warning about DBS
  artefacts.
- paper:Everall2026 — Joint five-class extraction; SV signatures; systematic association framework
  directly parallel to h08's design.
- paper:Kucab2019 — Experimental causal reference compendium; defines which exposure→signature
  links have direct causal evidence.
- paper:Otlu2023 — Topographic annotations of all COSMIC v3.3 signatures; mechanistic grounding for
  positive-control signature aetiologies and discovery hypotheses for unknown-etiology signatures.
- paper:Koh2025 — 89-channel InDel taxonomy; COSMIC-83 artefact disclosure; PRRDetect calibration
  of hypermutator annotation.
- paper:Pleasance2020 — Therapy-associated signatures in advanced tumors; APOBEC3A expression as
  mediator; confounders for cross-study aggregation.
- paper:Thatikonda2023 — Pediatric signature catalog; clock-like dominance; age-covariate
  confirmation; IDN novel signature.
