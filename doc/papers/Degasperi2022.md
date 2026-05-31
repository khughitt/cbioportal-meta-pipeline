---
id: "paper:Degasperi2022"
type: "paper"
title: "Substitution mutational signatures in whole-genome-sequenced cancers in the UK population"
status: "active"
ontology_terms:
  - mutational signatures
  - somatic mutation
  - single base substitution
  - double base substitution
  - whole-genome sequencing
  - signature extraction
  - NMF
  - COSMIC
datasets: []
source_refs:
  - "cite:Degasperi2022"
related:
  - "hypothesis:h08-agnostic-covariate-association-recovers-known-signature-aetiologies-and"
created: "2026-05-31"
updated: "2026-05-31"
---

# Substitution mutational signatures in whole-genome-sequenced cancers in the UK population

- **Authors:** Andrea Degasperi, Xueqing Zou, Tauanne Dias Amarante, Andrea Martinez-Martinez, Gene Ching Chiek Koh, João M. L. Dias, Laura Heskin, Lucia Chmelova, Giuseppe Rinaldi, Valerie Ya Wen Wang, Arjun S. Nanda, Aaron Bernstein, Sophie E. Momen, Jamie Young, Daniel Perez-Gil, Yasin Memari, Cherif Badja, Scott Shooter, Jan Czarnecki, Matthew A. Brown, Helen R. Davies, Genomics England Research Consortium, Serena Nik-Zainal (corresponding)
- **Year:** 2022
- **Journal:** Science, 376(6591); doi:10.1126/science.abl9283
- **DOI/URL:** https://doi.org/10.1126/science.abl9283
- **BibTeX key:** Degasperi2022
- **Source:** PDF

## Key Contribution

This paper presents a comprehensive mutational signature analysis of 18,640 WGS cancers drawn
from the UK Genomics England 100,000 Genomes Project (GEL), ICGC, and Hartwig cohorts,
expanding the COSMIC catalog with 40 new high-confidence SBS signatures and 18 new DBS
signatures. It introduces a principled common-vs-rare signature framework — each tumor type
has a small, stable set of "common" signatures and a long tail of rare ones — and proposes a
practical two-step fitting algorithm (FitMS) that exploits this structure to reduce false
positives in per-sample signature assignment.

## Methods

**Cohorts.** Primary analysis: 12,222 tumor-normal matched WGS pairs from the GEL 100,000
Genomes Project (v8 data release), covering 19 tumor types. Validation: 3,001 ICGC primary
and 3,417 Hartwig metastatic WGS cancers (18,640 total across all three cohorts).

**Extraction pipeline.**
1. Per-tumor-type mutational catalogs (96-channel SBS, 78-channel DBS) were constructed.
2. Samples were pre-clustered (hierarchical, 1 − cosine-similarity distance) to isolate
   those with common profiles; rare-profile outliers were removed before the first
   extraction step, which yields a stable set of "common" signatures per organ.
3. NMF with Kullback-Leibler divergence optimization and bootstrapped stability (≥300
   bootstraps) was used for extraction (NNLM R package).
4. Common signatures were fit to all samples; high-residual samples were subjected to a
   second extraction step to recover "rare" signatures.
5. All GEL + ICGC + Hartwig organ-specific signatures were pooled and clustered into
   "reference signatures"; QC (green / amber / red) was assigned based on independent
   reproducibility.
6. 82 SBS and 27 DBS reference signatures passed QC-green. These were matched to COSMIC v3
   (ref 14 = Alexandrov 2020) by cosine similarity.

**DBS curation.** For each DBS signature, the dinucleotides were verified to be in *cis*
(co-occurrence in the same read), an *in silico* analysis tested whether the DBS spectrum
could arise by chance from its correlated SBS, and up to 10 nt of wider mutational context
was examined. Several previously catalogued COSMIC DBS signatures (e.g. DBS3, DBS10, DBS12,
DBS14, DBS29, DBS37) were shown to be mathematical artefacts of adjacent SBS events, not
true dinucleotide processes.

**FitMS (Signature Fit Multi-Step).** A two-step algorithm: Step 1 fits organ-specific common
signatures (constrained non-negative least squares); Step 2 attempts to detect one additional
rare signature per sample via an errorReduction strategy (KLD improvement ≥ 15%) or
constrainedFit (residual cosine ≥ 0.8 to a known rare signature). Simulations (100 genomes,
5 common + 1 rare) demonstrated errorReduction outperformed single-step "fit all" and
constrainedFit strategies.

**Germline-somatic driver association.** For signatures with suspected causal mechanisms (BER,
MMR, POLE/POLD1, DSBR, deamination), germline and somatic mutations in relevant genes were
curated from supplementary tables to link genomic drivers to signature presence.

## Key Findings

**Expanded COSMIC catalog.**
- 82 high-confidence (QC-green) SBS reference signatures identified: 42 match previously
  reported COSMIC SBS signatures; 40 are novel.
- 27 high-confidence DBS reference signatures: 9 match COSMIC DBS; 18 are novel.
- New SBS signatures numbered SBS95 onwards (and selected older numbers); DBS from DBS12
  onwards.

**Common vs. rare signature structure.**
- Each organ has 5–10 common SBS signatures, with the count independent of sample size.
- The number of rare signatures is highly correlated with sample size (the tail lengthens as
  cohort grows), explaining why larger cohorts keep "discovering" signatures.
- Cross-cohort agnostic three-way comparison confirmed organ-specific signatures are
  reproducible regardless of sequencing platform or mutation-calling algorithm (fig. S2).

**Newly described signatures (selected highlights):**
- SBS107: C>A-dominated, kidney/bladder-specific.
- SBS100: APOBEC-like (resembles SBS2 but with taller TCC>TTC peak + context-independent
  C>T).
- SBS110: T>A peak at CTG>CAG, liver/biliary.
- SBS121: C>G at ACT/TCT contexts; colorectal/stomach.
- SBS120 (CNS): T>C at ATN with C>T at GCG peak; present in 75% of CNS tumors.
- SBS122 (sarcoma-enriched): T>C at TTN in 67% of sarcomas.
- SBS96 (MBD4-related): C>T at CpG; 12/18 affected GEL samples carry germline truncating
  MBD4 mutations with LOH.
- SBS108 (OGG1-associated): resembles SBS18, C>A at GCA; carriers of an OGG1 germline
  polymorphism (rs113561019 p.G308E) are enriched among samples.

**Environmental exposures re-confirmed with caveats.**
- UV (SBS7a/7b) confirmed; DBS1 co-occurs as expected.
- Tobacco/smoking: SBS4 + DBS2 in lung (and rare metastases to CNS, breast, colorectal).
- Aristolochic acid: SBS22 in renal cancers from patients with ethnic-minority ancestry (none
  reported direct AAI exposure in GEL); SBS113 may represent alternative PAH exposures.
- Platinum chemotherapy: SBS31/35 confirmed; two additional platinum-associated signatures
  (SBS111/112) found in patients with complex multi-treatment histories.
- APOBEC: SBS2/13 confirmed; DBS11 verified as APOBEC-induced (TpCC context in 10 nt window).

**MMR and polymerase defects.**
- Four MMR-deficiency (MMRd) signatures (SBS6, SBS15, SBS26, SBS44) confirmed, with
  enrichment of inactivating MMR gene mutations.
- SBS10a linked to POLE proofreading mutations (100% of 65 GEL SBS10a samples had POLE
  mutations).
- SBS10d associated with POLD1 exonuclease domain mutations.
- SBS14 (MMRd + POLE) and SBS20 (MMRd + POLD1) confirmed.
- MMRd signatures found at <1% frequency across many non-colorectal/uterine tumor types
  (stomach, prostate, pancreas, ovary, NET, lung, kidney, oropharyngeal, CNS, breast,
  sarcoma, bladder), suggesting undetected MMRd-eligible patients in routine care.

**HR-deficiency (HRD).**
- SBS3 and SBS8 mark BRCA1/BRCA2-null tumors; HRDetect applied across GEL.
- >30% of ovarian, ~11% of breast cancers had high HRDetect scores; caused by germline/somatic
  mutations in BRCA1, BRCA2, PALB2, RAD51C, RAD51D in 47% of cases (40% biallelic confirmed).

**DBS artefact identification.**
- DBS3, DBS10, DBS12, DBS14, DBS29, DBS37 shown to be mathematical consequences of adjacent
  SBS events (hypermutator SBS contexts), not true dinucleotide processes.
- DBS25 resolved as a triple-base substitution (TBS1: TTT>AAA/GAA/CAA/AAA), a novel mutation
  class formally described here.

**FitMS validation.**
- Simulation studies showed FitMS errorReduction strategy outperforms single-step fitting and
  constrainedFit when both common and rare signatures are present.
- Using organ-specific rather than reference (cross-organ-averaged) signatures further improved
  accuracy.

## Relevance

**Direct support for hypothesis h08 (agnostic covariate-signature association).**

This paper provides the most complete current catalog of WGS-derived mutational signatures
and their verified aetiologies, and is directly cited in h08's `source_refs`. Specific
connections:

- **Positive-control ground truth for H08a.** The paper rigorously validates exposure→signature
  links (UV↔SBS7a, smoking↔SBS4 + DBS2, APOBEC↔SBS2/13 + DBS11, MMR-loss↔SBS6/15/26/44,
  POLE↔SBS10a) in a matched-normal WGS cohort. These verified links are precisely the
  recovery targets that H08a must reproduce agnostically. The paper's confirmation that these
  associations are tissue-stratified (smoking in lung, UV in skin, MMRd in colorectal/uterine)
  also pre-validates H08's within-tissue conditioning design.

- **Identification of signatures with unknown aetiology — H08b targets.** Many of the 40 new
  SBS signatures (including clock-like or tissue-specific ones like SBS120, SBS121, SBS122,
  SBS137) have no confirmed etiology. These are candidate targets for H08b's agnostic
  covariate scan using expression modules.

- **Common-vs-rare structure informs the pipeline's signature-fitting strategy.** The paper's
  finding that each organ has a fixed number of common signatures (5–10) and that rare
  signatures grow with sample size is directly relevant to q018 (feasibility of downstream
  signature decomposition across cBioPortal studies, which are far smaller than GEL). Most
  cBioPortal panel studies will only recover common signatures; rare signatures require WGS
  scale (GEL/ICGC/MC3).

- **MMR prevalence data.** The finding that MMRd signatures appear at <1% in many tumor types
  beyond colorectal/uterine is relevant to the pipeline's `matched_normal_studies` config and
  the `annotate_ch.py` CH-aware annotation layer, which uses TP53/DNMT3A/etc. flags that may
  co-occur with MMR signatures in hematological cancers.

- **DBS artefact analysis.** The in-silico demonstration that several DBS signatures are
  mathematical artefacts of hypermutator SBS contexts is methodologically important for any
  signature decomposition step added to the pipeline; it warns against naively including all
  COSMIC DBS signatures in a restricted-fitting reference panel.

- **FitMS algorithm.** The two-step fitting strategy (organ-specific common first, then rare)
  is the practical recommendation for applying signatures to new samples. The `run_restricted_sigprofiler_assignment.py` script in the cbioportal pipeline implements
  restricted assignment; FitMS's errorReduction approach could serve as a downstream
  improvement or benchmark.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Common signatures (5–10 per organ) | Positive-control signature set for H08a | UV, smoking, APOBEC, MMR — directly targeted by H08a arms |
| Rare signatures (long tail, sample-size-dependent) | H08b discovery targets | Most only detectable at WGS scale; panel studies (cBioPortal) will not recover them |
| FitMS (two-step fitting) | `run_restricted_sigprofiler_assignment.py` | FitMS errorReduction is the recommended replacement/complement to single-step restricted fitting |
| Reference signatures (cross-organ average) | COSMIC SBS/DBS v3 reference panel | Paper warns these are mathematical averages; organ-specific signatures preferred for fitting |
| GEL 100,000 Genomes cohort | Not in the cbioportal pipeline (requires Genomics England access) | Serves as external validation ground truth for H08a positive-control expected associations |
| ICGC cohort | Partially overlaps cBioPortal TCGA studies | MC3 pseudo-study in pipeline is the recommended replacement for heterogeneous per-study TCGA MAFs |
| MMRd signatures at <1% across many tumor types | `annotate_ch.py` / clinical covariates | Implies MMR status is a relevant covariate in nearly all tissue strata, not just colorectal/uterine |

## Limitations

- **WGS only.** The GEL and ICGC cohorts are WGS; the paper explicitly notes that WES/panel
  data are 100–4,000× lower in genomic footprint and suffer AT/GC representation biases that
  distort signature extractions. Rare signatures detectable only in large WGS cohorts will be
  inaccessible in cBioPortal panel data (the binding constraint for q018).
- **Primary vs. metastatic mixing.** GEL and ICGC are primary; Hartwig is metastatic. The
  paper validates across cohorts but does not systematically partition primary-vs-metastatic
  effects on signature composition (treatment-induced signatures are more prevalent in the
  metastatic Hartwig cohort).
- **Causal genetic driver identification is incomplete.** For approximately half of MMRd and
  half of HRD cases, no causal germline or somatic driver was identified — methylation data
  were unavailable. This limits the paper's ability to fully close the genotype-to-signature
  loop.
- **Etiology of many new signatures remains unknown.** 40 new SBS signatures are reported;
  most lack any mechanistic explanation. The paper is honest about this but does not offer a
  path to discovery for those signatures.
- **GEL data access is restricted.** Primary data require registration with Genomics England;
  most results are accessible only via the Signal browser or Zenodo aggregate tables.
- **FitMS evaluation used simulated data.** The simulation assumed each sample has exactly five
  common + optionally one rare signature; real cancers have more heterogeneous compositions,
  and FitMS's advantage may be smaller in practice.

## Model / Tool Availability

- **Signal browser:** https://signal.mutationalsignatures.com/explore/study/6 — interactive
  visualization of all signatures, per-tumor-type summaries, and per-sample exposures.
- **Code:** R scripts (Code S1) and updated `signature.tools.lib` R package including FitMS
  (Code S2) deposited on Zenodo (ref 44 and 45 in the paper).
- **Signature tables:** Reference SBS and DBS signatures, QC status, and organ-specific
  exposure matrices available in supplementary tables and via Zenodo download.
- **License:** Not stated explicitly in the manuscript; code is via the `signature.tools.lib`
  package (GPL-3 in the repo [UNVERIFIED]).

## Follow-up

- **Alexandrov2020** (`paper:Alexandrov2020`) — the COSMIC v3 SBS/DBS catalog this paper
  extends; directly cited in the cbioportal pipeline and h08.
- The FitMS `signature.tools.lib` implementation should be evaluated against
  `run_restricted_sigprofiler_assignment.py` for the h08 positive-control refit step.
- For H08b candidate signatures with unknown aetiology (SBS120, SBS121, SBS122, SBS137,
  etc.), the Signal browser provides per-sample exposure tables useful for covariate
  association once matched to clinical data from the pipeline.
- Open question: which of the 40 new signatures are detectable in cBioPortal panel-sequenced
  studies at cohort level (pooled), even if not per-sample? This determines whether H08b can
  be attempted on cBioPortal data or requires MC3/WGS substrates exclusively.
