---
type: topic
title: DNA damage/repair mechanisms underlying mutational signatures
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: topic:dna-damage-repair-signature-mechanisms
ontology_terms:
- mutational signatures
- DNA damage
- DNA repair
- translesion synthesis
- mismatch repair
- nucleotide excision repair
- base excision repair
- COSMIC signatures
- SBS5
- SBS8
- SBS11
- SBS18
- SBS36
- MMR deficiency
- MUTYH
- chromatin context
related:
- paper:Boysen2025
- paper:Crisafulli2022
- paper:GonzalezPerez2019
- paper:Hwang2025
- paper:Koh2024
- paper:MasPonte2022
- paper:Owusu2025
- paper:Robinson2022
- paper:Seplyarskiy2021
- paper:Singh2020
- paper:Spisak2025
- paper:Volkova2020
- paper:Wojtowicz2026
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
- method:h08-agnostic-association-model
- topic:apobec-mutagenesis
- topic:signature-decomposition-unmatched-normal
- question:0018-can-mutational-signature-decomposition-be-added-downstream-of-the-cross
- question:0019-does-de-novo-extraction-on-the-aggregated-cohort-surface-factors-not-in
---

# DNA damage/repair mechanisms underlying mutational signatures

## Summary

Mutational signatures are not the direct fingerprints of DNA-damaging agents; they are the
emergent products of damage chemistry *filtered through* one or more DNA repair pathways and
then stamped by the error profiles of translesion synthesis (TLS) polymerases or repair-gap-
filling enzymes during replication. The core framework (paper:Volkova2020; paper:Seplyarskiy2021;
paper:GonzalezPerez2019) is: exposure → DNA adduct → (failed or partial) repair → lesion
reaches replication → TLS bypass → signature-specific substitution. This document synthesises
the mechanistic ground truth behind signatures that are positive-control targets for
`hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and`,
surfaces active disputes and gaps in the field, and draws concrete implications for the
cross-study signature-aetiology aggregation.

---

## Established Consensus

### The joint damage–repair framework

The most important lesson from systematic experimental work (paper:Volkova2020) is that 41% of
genotoxin × repair-background combinations alter mutation rates or spectra in a measurable way.
No signature arises purely from damage: the same mutagen produces different signatures depending
on which repair pathway is intact. NER prevents up to 99% of bulky-adduct mutations
(paper:Volkova2020), making it the dominant mutational suppressor; when NER is lost, mutation
rates rise uniformly rather than the spectrum shifting, so NER deficiency inflates TMB without
producing a distinctive trinucleotide fingerprint. TLS polymerases are responsible for the
majority (60–80%) of genotoxin-induced base substitutions while simultaneously suppressing large
deletions — so the same cell that avoids chromosomal instability pays the cost of point-mutation
mutagenesis (paper:Volkova2020; paper:Hwang2025).

Chromatin context mediates local mutation rate heterogeneity through two routes:
(1) differential access of repair machinery (NER reduced at nucleosome dyads; TC-NER producing
strand asymmetry in UV- and tobacco-exposed tumors) and (2) differential damage generation
(BPDE adducts enriched at linker regions; UV-CPDs at nucleosome cores). paper:GonzalezPerez2019
provides the detailed mechanistic account of how nucleosome positioning, TFBS occupancy, and
transcriptional activity jointly shape per-trinucleotide mutation rates for UV (SBS7), tobacco
(SBS4), oxidative damage (SBS17), and APOBEC (SBS2/13).

### Mechanistically validated positive-control signature–aetiology links

The signatures below have the strongest experimental evidence chains and serve as primary
positive-control targets for the agnostic covariate-association hypothesis:

| Signature | Exposure | Mechanistic link | Key evidence |
|---|---|---|---|
| SBS4 | Tobacco/PAH | BPDE-dG adducts at linkers; G>T via TLS; TC-NER asymmetry | paper:Volkova2020; paper:GonzalezPerez2019 |
| SBS7a/b | UV radiation | CPD-induced C>T at TpC; NER impaired at nucleosome cores | paper:GonzalezPerez2019; paper:Seplyarskiy2021 |
| SBS11 | Temozolomide + MGMT silencing | O6-meG/T mispairs; futile MMR cycle → lethality if MMR intact; C>T if MMRd | paper:Hwang2025; paper:Crisafulli2022; paper:Volkova2020 |
| SBS18/SBS36 | Oxidative damage / MUTYH BER deficiency | 8-oxoG; C>A transversions; tissue-specific ROS exposure | paper:Robinson2022; paper:Volkova2020 |
| SBS6/15/20/21/26/44 | MMR deficiency | Replication-error accumulation (MSH2/MLH1/MSH6 loss) | paper:Owusu2025; paper:Hwang2025; paper:MasPonte2022 |
| SBS2/SBS13 | APOBEC3A/3B | C>U deamination of ssDNA during transcription/replication | paper:GonzalezPerez2019; paper:MasPonte2022 |
| SBS22/SBS24 | Aristolochic acid / aflatoxin | Covalent DNA adducts; clear chemical exposure links | paper:Boysen2025 |

### SBS5 and SBS40: the collateral-mutagenesis clock

SBS5 and SBS40 are the most ubiquitous and debated clock-like signatures. Two convergent
experimental results now provide strong mechanistic anchors:

- paper:Hwang2025 (TK6 isogenic cell lines): REV7 knockout (TLS polymerase zeta regulatory
  subunit) reduces spontaneous SNV rate ~2.3-fold and largely eliminates SBS40, establishing TLS
  polymerase zeta as a dominant contributor to the aging-like background.
- paper:Spisak2025 (mathematical model + PCAWG empirical analysis): SBS5 is the footprint of
  "collateral mutagenesis" — errors made by error-prone polymerases at sites *neighbouring* a
  lesion during TLS bypass or NER gap-filling. Multiple damage types (SBS4/smoking, SBS7/UV,
  SBS18/oxidative) funnel into SBS5 because they all recruit the same polymerase (likely
  polymerase zeta), explaining why SBS5 co-varies with damage-specific signatures across tissues
  and why it accumulates in post-mitotic neurons that have no replication and minimal exogenous
  exposure. The relative contribution of TLS-mode vs repair-error-mode is cell-type-dependent:
  rapidly-dividing cells use TLS more; post-mitotic cells accumulate SBS5 primarily via repair
  errors.

These two findings are consistent: both implicate polymerase zeta as the main SBS5/SBS40
generator, differing only in whether TLS (Hwang) or repair gap-filling (Spisak) is the
predominant mode in a given cellular context.

### MMR deficiency: multiple signatures, continuous phenotype

MMR failure is not a single signature but an ensemble of ≥7 COSMIC SBS signatures (SBS6, 14,
15, 20, 21, 26, 44), plus indel signatures ID1, ID2, ID7
(paper:MasPonte2022; paper:Owusu2025). Their relative weights are *not* portable across
biological contexts:
- SBS6 is damage-time-dependent: nearly absent in short in vitro assays but prominent in tumours
  that have accumulated months to years of MMRd (paper:Owusu2025).
- SBS44 is replication-rate-dependent: highest in fast-dividing in vitro knockouts
  (paper:Owusu2025).
- Double knockouts (MSH2 + ATAD5; MSH2 + FANCD2) produce distinct sub-signatures (SBS26/44
  shifts), implying that co-occurring repair defects modulate MMRd spectra (paper:Hwang2025).

MSI is better modelled as a continuous phenotype than a binary MSI-H/MSS classification; the
standard Bethesda 5-locus panel undercounts MMRd prevalence in ovarian, cervical, and
adrenocortical cancers (paper:MasPonte2022). SBS33 and SBS12 have now been linked to MMR
deficiency via guilt-by-association (paper:Wojtowicz2026) and via PMS2-knockout signatures
(paper:MasPonte2022), extending the MMRd signature family beyond the canonical 7.

### SBS8: late-replication replication errors, not environmental exposure

SBS8 is enriched in late-replicating heterochromatin, accumulates with pathological stage, and
is nearly absent from normal tissue — all inconsistent with an exogenous exposure origin
(paper:Singh2020). ATR/CHEK1/CHEK2 checkpoint expression covaries with SBS8 in late-replicating
regions, and the RePrint repair-pathway framework independently clusters SBS8 with NER-processed
PAH signatures (paper:Wojtowicz2026), suggesting NER impairment at heterochromatin is the
mechanistic link. SBS8 and SBS40 share late-replication preference; they may represent
overlapping processes.

### Chromatin architecture as a first-order mediator

Across signatures, local chromatin features — nucleosome occupancy, TFBS density, replication
timing, transcriptional activity, and lamina association — modulate mutation rates independently
of exposure dose. paper:GonzalezPerez2019 documents the 10-bp rotational periodicity within
nucleosomes, strand asymmetries from TC-NER, and TFBS mutation-rate elevation despite open
chromatin. paper:Singh2020 extends this to a composite HMM epigenomic model (MRE states) that
integrates all three axes. paper:Seplyarskiy2021 frames germline mutagenesis within the same
framework, establishing that the replication-timing dependence of SBS1/SBS5 and the R-asymmetry
of SBS4/SBS7 are germline-observable.

### The exposome–adductome gap

paper:Boysen2025 identifies a fundamental three-tier gap: exposures are known
epidemiologically; mutational signatures are catalogued genomically; but the intervening DNA
adductome (50,000–100,000 modifications per cell from endogenous sources alone) is almost
entirely unmeasured in tumour tissue. Of ~200 COSMIC signatures, 64 have unknown aetiologies as
of late 2024. Even signatures with proposed causes often lack mechanistic validation: SBS2/13
(APOBEC) and the MMRd set are well-validated functionally, but molecular mechanism details
(which APOBEC3 family member; which MMR gene is rate-limiting in a given tissue) remain
contested. The proposed integration of DNA adductomics, nanopore long-read sequencing, and AI-
based base-calling could, in principle, close this gap for a subset of signatures, but it
remains aspirational at tumour-tissue scale.

---

## Contested Territory and Active Debates

### How many signatures does MMR deficiency actually produce?

The canonical 7-signature MMRd set (SBS6/14/15/20/21/26/44) is well established in vitro and
in tumour data (paper:Owusu2025; paper:Hwang2025). However:
- paper:Wojtowicz2026 adds SBS12 and SBS33 to the MMRd group via guilt-by-association.
- paper:MasPonte2022 links SBS12 to PMS2 single knockout, which produces a spectrum distinct
  from MLH1/MSH2/MSH6.
- SBS14 and SBS20 co-occur with POLE/POLD1 mutations (paper:MasPonte2022), implying mixed
  POLE-exonuclease + MMRd aetiology rather than pure MMRd.
These overlaps mean that treating any single SBS as a clean MMRd positive control is an
oversimplification; recovery should target the ensemble.

### SBS5 vs SBS40: one process or two?

paper:Spisak2025 argues SBS5 behaves as a single collateral-mutagenesis process; paper:Hwang2025
shows REV7 loss preferentially eliminates SBS40 more than SBS5. paper:Singh2020 treats both as
late-replication-enriched unknowns. The practical question — whether SBS5 and SBS40 should be
tested separately or jointly in association analyses — remains unresolved. Attribution in low-
mutation-count samples (e.g., panel-sequencing) is especially noisy for these flat signatures.

### Is SBS8 a product of NER impairment or checkpoint deficiency?

paper:Singh2020 implicates ATR/CHEK1/CHEK2 checkpoint defects as primary drivers. paper:Wojtowicz2026
clusters SBS8 with NER-processed PAH signatures. These are not mutually exclusive (checkpoint
deficiency could allow late-replication errors to accumulate in low-NER heterochromatin), but
the quantitative contributions are unknown.

### SBS57: biological or artifact?

paper:Owusu2025 demonstrates that SBS57 in MMRd cell lines is a pure alignment artifact driven
by SNP + indel co-occurrence near thymine repeat boundaries; strict filtering eliminates it
entirely. However, SBS57 in non-MMRd tumour contexts (POLE-deficient, SBS17, SBS12 clusters)
survives strict filtering, implying a distinct biological mechanism in those settings —
currently unexplained.

### Chemotherapy-induced signatures and their identity with COSMIC catalogue

SBS11 is now experimentally confirmed (paper:Hwang2025; paper:Crisafulli2022). The CX-5461
drug generates a triad (SBS-CX-5461, DBS-CX-5461, InD-CX-5461) not in the current COSMIC
catalogue — the most mutagenic compound tested in human cells by mutation burden, exceeding
benzo(a)pyrene (paper:Koh2024). Whether the restricted COSMIC assignment used in this pipeline
will fail to capture such drug-induced signatures in clinical trial samples is an open
operational concern.

---

## What Is Settled vs Unsettled

**Settled:**
- TLS is the dominant generator of base substitutions from both exogenous damage and
  endogenous replication errors; NER is the dominant suppressor.
- UV (SBS7), tobacco/PAH (SBS4), aristolochic acid (SBS22), aflatoxin (SBS24), and MUTYH
  deficiency (SBS36) have experimentally validated, full mechanistic chains.
- MMR deficiency (SBS6/15/26/44 + indel signatures ID1/ID2) is mechanistically confirmed at
  single-gene-knockout resolution for MLH1, MSH2, MSH6 (paper:Owusu2025; paper:Hwang2025).
- SBS11 is the product of TMZ + MGMT silencing, modulated by MMR status.
- SBS5/SBS40 are dominated by polymerase-zeta TLS activity, not exogenous exposures.
- Local chromatin and replication timing are first-order modulators of mutation rate independent
  of exposure.

**Unsettled:**
- Causal chain for SBS8 (NER vs checkpoint vs replication error mode).
- Relative contributions of SBS5 vs SBS40 in low-mutation-count contexts.
- Whether the 64 signatures of unknown aetiology include cryptic subtypes of known processes
  or represent genuinely novel chemistries.
- Biological basis of SBS57 in non-MMRd tumours.
- The TLS polymerase identity responsible for SBS5 (polymerase zeta is the leading candidate
  but not proven; paper:Hwang2025; paper:Spisak2025).
- Whether the APOBEC–MMR coupling (EXO1-generated ssDNA → APOBEC substrate; paper:MasPonte2022)
  means APOBEC3 expression and MMR status are co-regulators of SBS2/13, complicating their
  use as independent covariates in the agnostic association scan.

---

## Methodological Tensions

**Cell-line models vs tumour biology.** TK6 (paper:Hwang2025), HAP1 (paper:Owusu2025), and
RPE1 (paper:Koh2024) isogenic knockout systems provide clean mechanistic dissection but differ
from solid tumours in chromatin state, stromal context, diploidization, and epigenetic history.
SBS6 in particular is nearly absent from short-term in vitro assays but common in tumours,
highlighting that some signatures require extended time-based accumulation not achievable in
cell-line experiments.

**C. elegans vs human conservation.** paper:Volkova2020's 54-genotype × 12-genotoxin screen is
the most systematic damage × repair interaction dataset available, but C. elegans lacks key
immune/microenvironment interactions and some human-specific repair pathways. Human translation
is moderate at the qualitative level; quantitative effects differ.

**Restricted COSMIC assignment vs de novo extraction.** If novel drug-induced signatures
(paper:Koh2024) or biological subtypes (SBS57 in non-MMRd contexts; paper:Owusu2025) are not
in the COSMIC catalogue, restricted assignment will silently misattribute them to the nearest
existing signature. This is a concrete operational risk for studies enrolling clinical trial
patients.

**Panel vs WGS for SBS8 and SBS5.** Both signatures are enriched in heterochromatin and late-
replicating regions (paper:Singh2020), which are largely absent from coding-region panels. Panel-
based decomposition will systematically underestimate SBS8 and introduce noise into SBS5
estimates. The cross-study meta-analysis is predominantly panel and exome data.

**RePrint transformation as a clustering tool.** paper:Wojtowicz2026's RePrint framework
outperforms raw cosine similarity for grouping signatures by repair pathway, providing 5/6
validated predictions. However, it operates at the population-level signature (not per-sample)
and cannot be applied directly to sample-level covariate association without an additional
aggregation step.

---

## Implications for the Cross-Study Signature-Aetiology Aggregation

### Positive-control design

The strongest positive controls for the agnostic covariate-association hypothesis, ranked by
mechanistic confidence and aetiology clarity, are:

1. **UV (SBS7) — melanoma/skin**: Full exposure→adduct→NER-bypass→C>T chain validated;
   tissue-restricted; covariate is cumulative UV exposure (or skin-cancer subtype).
2. **Tobacco/PAH (SBS4) — lung/liver**: NER+TLS chain validated; tissue-restricted; covariate
   is smoking status or pack-years from clinical metadata.
3. **MUTYH germline deficiency (SBS18/SBS36) — colorectal**: Cell-level causal chain in normal
   tissue established at single-crypt resolution (paper:Robinson2022); covariate is germline
   MUTYH status (not currently in cBioPortal clinical schema for most studies).
4. **TMZ treatment / MGMT silencing (SBS11) — GBM**: Confirmed by two complementary
   approaches (paper:Hwang2025; paper:Crisafulli2022); covariate is TMZ treatment history
   (available in TCGA clinical tables); recovery in GBM within-tissue strata is a
   near-certain positive control.
5. **MMR deficiency (SBS6/15/26/44 + ID1/ID2) — CRC/endometrial**: Mechanistically confirmed
   at single-gene level (paper:Owusu2025; paper:Hwang2025); covariate is MSI status (available
   in most CRC cBioPortal studies, but binary classification is coarser than continuous
   MSISensor scores; paper:MasPonte2022). Recovery must target the signature ensemble, not any
   single SBS.
6. **APOBEC (SBS2/SBS13)**: See `topic:apobec-mutagenesis` for detailed synthesis; APOBEC3A/B
   expression as covariate is partially confounded by MMR state (paper:MasPonte2022).

### SBS5/SBS40: expected true-negative for environmental exposure covariates

The collateral-mutagenesis model (paper:Spisak2025) and TLS-polymerase-zeta evidence
(paper:Hwang2025) together explain why SBS5 will not cleanly associate with any single
exogenous exposure covariate: it accumulates from multiple damage funnels plus repair errors
regardless of division status. Any agnostic scan returning no strong clinical exposure hit for
SBS5 is a *true negative* (correct model behavior), not a method failure. SBS5 will, however,
co-vary with damage-specific signatures (SBS4 in lung, SBS7 in skin), which should be
interpretable as collateral effects rather than evidence of a distinct SBS5 exposure.
[SPECULATION: If POLZ expression is available from RNA-seq, it may weakly associate with SBS5
across cancer types; this is a testable discovery-arm candidate.]

### SBS8: a discovery target with mechanistic prior

SBS8 is not a positive control (its aetiology is contested), but the mechanistic prior from
paper:Singh2020 and paper:Wojtowicz2026 is strong enough to generate specific discovery-arm
predictions:
(a) ATR/CHEK1/CHEK2 expression modules should associate with SBS8 in late-replicating tumour
contexts; (b) pathological stage should positively associate with SBS8 burden; (c) SBS40 should
show the same associations. These are directly testable using TCGA MC3 data with RNA-seq and
stage annotations.

### Chromatin-context covariates are mechanistic mediators, not nuisance variables

Local replication timing, nucleosome occupancy, and transcriptional activity are not
independent of signature exposures — they are mechanistic mediators of repair efficiency
(paper:GonzalezPerez2019; paper:Singh2020). In the within-tissue association model, including
replication-timing-proxied covariates (e.g., CHEK1 expression, proliferation signatures) as
nuisance variables risks partial mediation adjustment that attenuates genuine causal signals.
They should be modelled explicitly rather than blindly conditioned out.

### Pipeline-specific operational concerns

- **SBS57 artifact risk.** cBioPortal studies using single callers without RepeatMasker
  filters or ±6 bp deletion exclusion may carry SBS57-type artifacts (paper:Owusu2025).
  Matched-normal studies (the `matched_normal_studies` config key) are less susceptible.
  The aggregated mutation table should be checked for SBS57 prevalence before signature-association
  analysis.

- **Treatment-induced confounders.** SBS11 (TMZ; GBM studies), SBS-CX-5461 (clinical trial
  samples; paper:Koh2024), and acquired MMRd post-TMZ treatment (paper:Crisafulli2022) can
  inflate mutation burden and create spurious driver-gene signals (e.g., the MSH6 p.T1219I
  hotspot appearing in cross-study aggregation at elevated frequency in mCRC studies). The
  hypermutator annotation pipeline (tasks t081/t092–t099) does not currently include a
  `treatment_alkylating` category; this is a gap.

- **MMRd signature ensemble required.** The positive-control MMR arm should target the
  ensemble of SBS6/14/15/20/21/26/44, not rely on any single signature, because relative weights
  shift with replication kinetics and biological context (paper:Owusu2025). Continuous MSI scores
  are preferable to binary MSI-H labels as the covariate (paper:MasPonte2022).

- **Panel-data limitations for SBS8.** Since SBS8 is enriched in heterochromatin and depleted
  in exons (paper:Singh2020), panel-based decompositions will systematically underestimate SBS8.
  Restricted SigProfiler assignment from panel data is unlikely to recover SBS8 with adequate
  signal-to-noise for association tests outside of WGS-based inputs (tcga_mc3).

- **Reprint pre-stratification opportunity.** The RePrintPy tool (paper:Wojtowicz2026) could
  reduce the effective number of independent signature outcomes by grouping by repair mechanism
  before running covariate associations. This would also improve the biological
  interpretability of association hits and sharpen multiple-testing correction. Running
  RePrintPy on the cross-study signature extraction output is a low-effort pre-analysis step.

- **Etiology confidence tier for unknown signatures.** The 64 COSMIC signatures of unknown
  aetiology (paper:Boysen2025) should be treated as low-priority discovery targets and flagged as
  uninterpretable if they emerge as association hits — unless a RePrint cluster neighbour
  (paper:Wojtowicz2026) or a mechanistic prior provides interpretive context.

## Key Concepts

The key concepts are defined in the existing prose above and in the linked project entities; this section is present to keep the topic aligned with the current Science topic template.

## Current State of Knowledge

The current project-facing state of knowledge is summarized in the existing prose above. No additional confidence upgrade is made by this structural section.

## Relevance to This Project

This topic is relevant through the linked questions, hypotheses, datasets, and source references in the frontmatter and in the note above.

## Key References

Key references are listed in `source_refs` and cited in the note above.
