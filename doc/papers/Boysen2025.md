---
id: "paper:Boysen2025"
type: "paper"
title: "Investigating the origins of the mutational signatures in cancer"
status: "active"
ontology_terms: []
datasets: []
source_refs:
  - "cite:Boysen2025"
related: []
created: "2026-05-31"
updated: "2026-05-31"
---

# Investigating the origins of the mutational signatures in cancer

- **Authors:** Gunnar Boysen, Ludmil B. Alexandrov, Raheleh Rahbari, Intawat Nookaew, Dave Ussery, Mu-Rong Chao, Chiung-Wen Hu, Marcus S. Cooke
- **Year:** 2025
- **Journal:** Nucleic Acids Research
- **DOI/URL:** https://doi.org/10.1093/nar/gkae1303
- **BibTeX key:** Boysen2025
- **Source:** PDF

## Key Contribution

This critical review argues that understanding the causal origins of most mutational signatures requires integrating three currently separate evidence streams — the exposome (all exposures over a lifetime), the DNA adductome (all DNA modifications in the genome), and observed mutational signatures — into a single analytical framework. Of the ~200 established COSMIC mutational signatures, 64 have entirely unknown etiologies, and even signatures with proposed causes often lack mechanistic validation. The authors propose that holistic DNA adductomics, combined with long-read nanopore sequencing and advanced AI-based computational analysis, offers a path toward resolving causal relationships between specific DNA lesions and the mutational patterns they produce.

## Methods

This is a critical review / perspective article, not a primary research study. The authors survey:

- The landscape of COSMIC mutational signatures (SBS, DBS, ID, CN, SV, RNA-SBS types; ~200 total signatures as of writing).
- Current mechanistic understanding of how DNA modifications arise from exogenous and endogenous sources (the exposome).
- Existing DNA adductomics approaches: targeted adductomics (focused on known adducts by mass spectrometry), untargeted/global adductomics (high-resolution mass spectrometry, HRMS), and genome-wide mapping methods.
- Technologies for mapping DNA modifications: HRMS, chemical-labeling excision sequencing, nanopore long-read sequencing (Oxford Nanopore Technologies, ONT), and AI/deep-learning base-calling software (DeepMP, NanoCon, DeepMod2, ELIGOS).
- The conceptual pipeline from exposure → DNA adduct formation → translesion synthesis (TLS) bypass → mutation → clonal selection → observed mutational signature.

No new computational or experimental results are presented.

## Key Findings

**Signature etiology landscape.** Of ~200 established COSMIC signatures (99 SBSs, 20 DBSs, 23 IDs, 25 CNs, 10 SVs), 64 have unknown etiologies; COSMIC labels many others only as "possible artifacts." Achieving even a cosine similarity ≥ 0.90 between reconstructed and observed profiles is the community acceptance bar for signature attribution.

**Three-tier mechanistic gap.** The core problem is that (1) exposures are known epidemiologically, (2) mutational signatures are catalogued genomically, but (3) the intervening DNA adduct landscape (the adductome) is almost entirely unmeasured in tumor tissue, preventing causal validation.

**DNA adductome complexity.** A single cell may harbor 50,000–100,000 DNA modifications from endogenous cellular processes alone. Epigenetic marks (5-Me-Cyt, 6-Me-Ade) occur at 1 per ~20 normal nucleotides; endogenous adducts at ~1 per 10³–10⁶ nucleotides; exogenous adducts at ~1 per 10⁸–10¹¹ nucleotides (Figure 4).

**Mutational signatures and their mechanistic links (well-established examples).**
- SBS4: tobacco smoking; C>A mutations from PAH-induced N²-BPDE-dG adducts; dose-response validated across multiple lung-cancer cohorts.
- SBS29: chewing tobacco; also C>A-dominated but with distinct trinucleotide context from SBS4, implying different causal chemistry.
- SBS1: clock-like aging; spontaneous/enzymatic deamination of 5-Me-Cyt → SBS1 (CpG C>T hotspots); additional contribution from Pol ε replication errors at 5mCpG demonstrated by Tomkova et al. (2024).
- SBS2/SBS13: APOBEC cytidine deaminase activity (AID/APOBEC family); exact contributions of APOBEC3A vs. 3B vs. 3C remain debated.
- SBS5/SBS17/SBS40: prevalent in normal and cancer tissue; etiologies still unknown.
- SBS22/SBS24: aristolochic acid and aflatoxin respectively; clear chemical-exposure links confirmed across multiple studies.

**Translesion synthesis (TLS) as the mutation generator.** TLS polymerases bypass blocking DNA adducts with error rates from 0.001 to 100%; the error rate depends on adduct chemistry, flanking sequence context, and which TLS polymerase(s) are recruited. The mutational signature of an adduct is therefore determined by TLS polymerase identity rather than by adduct identity alone — meaning the same adduct can produce different signatures depending on cellular context.

**Adductomics approaches and limitations.**
- Targeted adductomics: measures a pre-selected list of known adducts by LC-MS/MS; misses novel or unexpected modifications.
- Untargeted HRMS-based adductomics: provides qualitative and quantitative landscape of all detectable modifications but gives no genomic location information — cannot assign a specific adduct to a specific trinucleotide context.
- Genome-wide mapping: chemical-labeling + excision-sequencing methods (e.g., using repair enzymes to excise adduct-containing oligos) provide location but are restricted to specific adduct types; antibody-based enrichment has limited specificity.

**Nanopore sequencing as a unifying technology.** ONT long-read native DNA sequencing can simultaneously detect base sequence and DNA modifications without chemical conversion. It has demonstrated proof-of-principle detection of N²-BPDE-dG, 8-oxoG, abasic sites, 5-Me-Cyt, 6-Me-Ade, and other modifications at single-molecule and potentially single-cell resolution. The ELIGOS software (developed partly by Boysen/Nookaew groups) simultaneously detects RNA and DNA modifications from ONT signal data. Key limitation: deep-learning base-callers require large amounts of ground-truth training data, which is scarce for rare adducts; synthetic adducted DNA sequences are needed but challenging to generate at scale.

**Timeline gap.** DNA adductomic data capture acute/chronic exposures; mutational signatures reflect the post-selection clonal landscape. Synchronizing these timescales requires prospective sampling from exposure onset, but is logistically and ethically difficult. Some exposures increase mutation burden but selection pressure, not mutation rate, shapes the visible signature.

**Integration vision.** The authors call for AI-driven integration of three databases: DNA adductome databases (e.g., mzCloud, MassBank), exposome-related databases (ToxCast, HERO), and mutational signature databases (COSMIC), linked through multi-omics platforms and fed by comprehensive adductomics workflows embedded in precision oncology pipelines.

## Relevance

**Directly relevant to h08** (agnostic covariate–signature-exposure association; positive-control recovery of UV/smoking/APOBEC/MMR signatures).

1. **Etiology confidence tiers.** The review provides a useful operational vocabulary for h08: signatures differ enormously in the strength of their causal evidence chain. Positive-control signatures for h08 should be selected from those with the highest confidence tier (experimental reproduction of the full exposure→adduct→mutation chain): SBS4 (smoking), SBS7a/b (UV, CPD-induced C>T at TpC), SBS22 (aristolochic acid), SBS24 (aflatoxin), SBS18 (ROS/8-oxodG-like). APOBEC (SBS2/13) and MMR-deficiency (SBS3/SBS6/SBS26) signatures are well-validated functionally but their molecular details are still contested; treat these as tier-2 positive controls.

2. **Unknown-etiology signatures pose h08 confounding risk.** Of 64 signatures with unknown etiologies, many are relatively common and will appear in our cross-study meta-analysis. Associating clinical covariates (smoking, therapy, tissue-of-origin) with these signatures may produce statistically significant hits that are mechanistically uninterpretable — or that conflate distinct underlying processes. The 64-unknown figure is a useful upper bound on how many signatures in COSMIC could yield uninterpretable associations.

3. **SBS5 / SBS40 ambiguity.** Both are clock-like and pervasive across cancer types; the review explicitly states their etiologies are unknown, even though they increase with age. For the cross-study aggregation pipeline, these signatures will dominate "background" in many cancer types. Any covariate (age, sequencing depth) that correlates with overall mutation burden will spuriously associate with SBS5/SBS40.

4. **Trinucleotide context as a discriminator.** The review illustrates (Figure 2) that SBS4 vs. SBS29 (both C>A-dominated tobacco signatures) are distinguishable by trinucleotide context — emphasizing that aggregate mutation-type counts used in the cross-study pipeline are insufficient to resolve exposures; full 96-channel profiles are needed for h08 signature attribution.

5. **Adductomics–signature integration as a future validation resource.** If the Boysen/Alexandrov/Cooke group succeeds in building the proposed integrated pipeline, the resulting mechanistically validated signature–exposure pairs could provide a gold-standard benchmark for h08's agnostic covariate recovery approach: we could test whether our pipeline recovers the known chemical exposure associations for validated signatures.

6. **Nanopore adductomics for normal-vs-tumor comparison.** The proposed single-cell, native-DNA nanopore sequencing of adducts is relevant if the project expands to include clonal hematopoiesis (CH) or normal tissue contexts, where matched-normal sequencing is available (the pipeline already supports `matched_normal_studies`).

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| COSMIC SBS signature etiology tiers | h08 positive-control signature set | Use etiology confidence to stratify which signatures are reliable positive controls vs. confounders |
| 64 signatures with unknown etiology | Unknown-etiology confounders | Signatures to flag/exclude from interpretable h08 associations |
| Exposome (smoking, UV, chemicals) | Clinical covariates in cross-study meta-analysis | The covariates h08 seeks to recover agnostically |
| DNA adductome | Intermediate layer between exposure and signature | Not currently represented in cbioportal pipeline; would require external data |
| TLS polymerase error rate | Signature generation model | Explains why same exposure can produce different signatures in different cell types |
| Cosine similarity ≥ 0.90 acceptance criterion | Signature fitting quality threshold | Relevant when using SigProfiler or similar tools for per-study signature extraction |

## Limitations

- This is a review/perspective, not a primary data paper; no new signatures are characterized or etiologies established.
- The proposed integrated adductomics pipeline is aspirational — no demonstration that it works at scale in human tumor cohorts.
- The 64 "unknown etiology" count is based on COSMIC as of late 2024; this number changes as COSMIC is updated and some "possible artifacts" are reclassified.
- The review focuses primarily on SBS signatures; CN/SV signature etiology (which may be more relevant to structural rearrangements and copy-number driven cancer types) is discussed only briefly.
- Nanopore detection of rare exogenous DNA adducts in tumor tissue remains a proof-of-principle challenge; the training data bottleneck for deep-learning base-callers is acknowledged but not resolved.
- The timeline gap between exposure-induced adduct formation and selection-shaped mutational signatures is recognized as a fundamental confound but no concrete solution is offered beyond prospective study design.

## Model / Tool Availability

- **ELIGOS** (Epitranscriptional/Epigenomic Landscape Inferring from Glitches of ONT Signals): software for simultaneous RNA and DNA modification detection from ONT data; developed by Jenjareonpun, Nookaew, Boysen, and colleagues. References 116, 132–134 in the paper.
- No new software or datasets are released by this review paper itself.
- External tools referenced: DeepMP (Bonet et al. 2022), NanoCon (Yin et al. 2024), DeepMod2 (Ahsan et al. 2024), COSMIC (https://cancer.sanger.ac.uk/cosmic/signatures).

## Follow-up

- Read Kanaly et al. (2006) for the foundational adductome concept; cited as ref 96 in this paper.
- Read Cooke et al. (2023) *Sci. Total Environ.* 856:159192 (ref 92) for the next-generation adductomics vision paper co-authored by several of the same group.
- Tomkova et al. (2024) *Nat. Genet.* (ref 85): new mechanism for C>T at CpG via Pol ε replication errors — relevant to SBS1 etiology and to the matched-normal study design in the pipeline.
- Consider whether h08 should explicitly stratify by signature etiology confidence tier (using the COSMIC hierarchy of evidence) rather than treating all signatures uniformly.
- The 64 signatures with unknown etiologies: check which of these appear at appreciable frequency in the cbioportal study set — they may need to be treated as nuisance / latent-factor variables in the h08 covariate association model.
