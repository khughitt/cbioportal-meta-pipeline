---
type: paper
title: A Compendium of Mutational Signatures of Environmental Agents
status: active
created: '2026-05-31'
updated: '2026-06-28'
id: paper:Kucab2019
ontology_terms:
- mutational signatures
- environmental mutagens
- somatic mutation
- DNA repair
- iPSC
- whole-genome sequencing
datasets: []
source_refs:
- cite:Kucab2019
related: []
---

# A Compendium of Mutational Signatures of Environmental Agents

- **Authors:** Jill E. Kucab, Xueqing Zou, Sandro Morganella, Madeleine Joel, A. Scott Nanda, Eszter Nagy, Celine Gomez, Andrea Degasperi, Rebecca Harris, Stephen P. Jackson, Volker M. Arlt, David H. Phillips, Serena Nik-Zainal
- **Year:** 2019
- **Journal:** Cell (Vol. 177, pp. 821–836)
- **DOI/URL:** https://doi.org/10.1016/j.cell.2019.03.001
- **BibTeX key:** Kucab2019
- **Source:** PDF

## Key Contribution

This paper establishes a first comprehensive experimental reference compendium of mutational signatures induced by 79 known or suspected environmental carcinogens, assayed by whole-genome sequencing (WGS) of 324 human induced pluripotent stem cell (iPSC) subclones. Forty-one agents produced characteristic single-base substitution (SBS) signatures, 6 produced double-substitution (DBS) signatures, and 8 produced indel signatures. Several experimentally derived signatures closely matched signatures previously extracted from human tumors, providing direct causal evidence linking specific environmental exposures to cancer-associated mutation patterns. The study also revealed mechanistic insights through strand-asymmetry analyses, demonstrating that transcription-coupled nucleotide excision repair (TC-NER) and mismatch repair (MMR) are fully functional in iPSCs [@Kucab2019].

## Methods

**Experimental design:**
- 77 chemical carcinogens, therapeutic agents, or DNA damage response (DDR) inhibitors, plus 2 radiation sources and a range of controls, were tested across 113 treatment conditions.
- A human iPSC line (a single, stable, diploid, undifferentiated cell line) was treated at concentrations causing 40–60% cytotoxicity (IC40–60). Some compounds were also tested with S9 rodent liver-derived metabolic enzyme mixture to capture metabolic activation.
- After treatment, cells recovered for 7 days and were expanded into single-cell-derived subclones (2–4 subclones per treatment arm, 324 total).
- Each subclone underwent 30x WGS aligned to GRCh37/hg19. All somatic mutation classes (substitutions, double-substitutions, indels, rearrangements, copy-number changes) were called relative to the parental iPSC clone.

**Signature extraction:**
- Background signature identified from 128 control subclones (ubiquitous in all iPSCs, attributed to ROS-related damage; resembles COSMIC SBS18).
- A permutation test (q < 0.01) determined whether each treatment arm's mutation load significantly exceeded controls (mutagenicity index = (N_treatment − N_control) / N_control).
- Signatures were extracted only from treatments where the signal-to-noise ratio (SNR) ≥ 2.
- Background signature subtracted to yield putative treatment-associated signatures.
- Stability assessed across subclones; hierarchical clustering of all 53 signatures by their 96-channel profiles.
- Double-substitution (DBS) profiles used 78-type classification; indel signatures used a 29-channel classification incorporating motif size, CG/TA content, and repeat-flanking context.
- Strand asymmetry: assessed replication-timing domain (RTD) distribution and transcriptional strand bias (Pearson chi-square with multiple-test correction).

**Comparison to tumor signatures:**
- De-novo extraction from 2,577 whole cancer genomes (unpublished at paper time) across 21 tissue types generated 196 independent signatures; experimental signatures compared against these by cosine similarity.

## Key Findings

**Substitution signatures (SBS):**
- 41 of 79 agents produced significant SBS signatures (53 putative signatures total, some agents at multiple concentrations).
- Several recapitulate well-known tumor signatures:
  - Simulated solar radiation (SSR) → UV-like signature (cossim 0.91 to UV-associated cancers; C>T/G>A transitions at dipyrimidines, CC>TT doublets).
  - Aristolochic acid I (AAI) → signature matching urothelial and liver cancers associated with AAI exposure (cossim 0.99 to Signature 22; A>T/T>A transversions dominant).
  - Aflatoxin B1 (AFB1) + S9 → G>T transversions, consistent with AFB1-liver cancer association.
  - Benzo[a]pyrene (BaP) and diol-epoxide (BPDE) → G>T/C>A signatures resembling lung cancer (tobacco smoking, COSMIC SBS4; cossim 0.84–0.95 to smoking-lung signatures).
  - Cisplatin/carboplatin → G>A/C>T dominant, similar to signature extracted from myeloid tumors in platinum-treated patients.
- Alkylating agents (ENU, MNU, temozolomide): T>C/A>G and C>T/G>A transitions; ENU/MNU signatures highly similar to temozolomide (cossim ~0.98). O6-alkylguanine explains C>T/G>A; O4-alkylthymine explains T>C/A>G.
- 1,2-DMH: unique C>T/G>A peaks at NpCpC and NpCpT, resembling COSMIC Signature 11 component.
- PAHs (DBA, DBADE, DBP, BPDE, 5-methylchrysene): G>T/C>A transversions; signatures closest to their diol-epoxide metabolites rather than to each other, confirming diol-epoxide as the primary mutagenic pathway.
- Nitro-PAHs (1,6-DNP, 1,8-DNP, 3-NBA): very similar indel signatures (C deletions at long repeat tracts).
- Several compounds did not produce detectable signatures (38 of 79 agents), including MMS, MNNG, nickel chloride, DBC — confirming mutagenicity ≠ detectability.

**Double-substitution (DBS) signatures:**
- 6 agents produced DBS signatures (8 treatments): SSR (CC>TT dominant), PAHs (BaP, BPDE, DBA, DBADE → CC>AA/GG>TT and CA>AT/TG), platinum compounds (AG>TT, GA>TT), and cisplatin/carboplatin.
- Observed DBS frequency exceeded chance across all subclones including controls, suggesting a universal cellular stressor elevating DBS likelihood in iPSCs.

**Indel signatures:**
- 8 agents (10 treatments) produced indel signatures: 1,2-DMH (C deletions flanked by T at poly-T tracts), nitro-PAHs (1,8-DNP, 3-NBA: C deletions at long repeat tracts), BaP/BPDE (C deletions at short repetitive sequences, cossim 0.95 to smokers' lung indel signature), cisplatin (T insertions at single T in GpG context), DBADE (T and C insertions), 6-nitrochrysene (mixed phenotype).

**Strand asymmetries and DNA repair:**
- No replicative strand asymmetry detected in any signature, consistent with DDR being fully functional.
- Transcriptional strand asymmetry (TC-NER footprint) detected for tobacco-related compounds (BaP, BPDE: G>A/C>T class), ENU, 6-nitrochrysene, and AAI — particularly strong in early replication timing domains (early RTD), indicating TC-NER is more active in early RTD in iPSCs.
- The ubiquitous background signature (control subclones) resembles COSMIC SBS18 and shows no transcriptional strand bias; attributed to ROS during cell culture, consistent with BER + MMR activity.
- RTD analysis: background signature enriched in late RTD (typical of ROS); DBADE signature enriched in early RTD on non-transcribed strand (TC-NER removing guanine adducts from transcribed strand preferentially).

**Comparison to cancer-derived signatures:**
- Strongest matches: AAI ↔ liver/kidney cancers (cossim 0.99/0.94); SSR ↔ UV-associated skin cancers; DBP/DBPDE ↔ DBPDE-associated signatures (cossim 0.86–0.96); tobacco PAHs ↔ smoking lung (cossim 0.84–0.95).
- Cisplatin and carboplatin signatures concordant with a signature extracted from myeloid tumors in chemotherapy patients.
- Weaker correspondences for nitro-PAHs, heterocyclic amines, alkylating agents, and some drug therapies; these require caution in epidemiological interpretation.

## Relevance

**Direct relevance to hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and (agnostic covariate↔signature-exposure association; positive-control recovery):**

This paper is the canonical experimental reference catalog linking specific environmental agents to their mutational signature "fingerprints." It is directly relevant to:

- **Hypothesis:0007 positive-control design.** The paper provides ground-truth cosine similarities between experimentally generated signatures and the COSMIC catalog (SBS4 ↔ tobacco/BaP/BPDE; SBS7 ↔ UV/SSR; SBS22 ↔ AAI; SBS11/SBS-PT ↔ platinum). Any pipeline that claims to recover known etiology associations should reproduce these correspondences; the Kucab signatures serve as an independent validation layer.
- **Known vs. ambiguous signals.** The paper explicitly notes that 38/79 agents did not generate detectable signatures despite cytotoxicity, reinforcing the point (relevant to hypothesis:0007) that absence of a signature is not absence of exposure — the pipeline's agnostic scan must tolerate this asymmetry.
- **Mechanistic interpretation of strand asymmetries.** The TC-NER footprint on BaP/BPDE signatures (C>A strand asymmetry, early RTD enrichment) provides a mechanistic positive control: any agnostic scan recovering the BaP↔lung signature link should ideally also recover the TC-NER mechanistic signature as a co-feature.
- **APOBEC, MMR, and endogenous processes are notably absent from environmental exposures tested here.** The compendium covers exogenous agents; APOBEC (SBS2/13) and MMR-loss (SBS6/15/26) signatures arise from endogenous processes, not from any of the 79 agents. This cleanly separates the exogenous-agent catalog from the endogenous-process catalog relevant to the hypothesis:0007 APOBEC-expression and MMR/MSI arms.
- **Cross-study aggregation context.** In the cbioportal pipeline, the annotated ratio table carries COSMIC-matched signature exposures downstream. Knowing which COSMIC signatures have strong experimental causal anchors (from this compendium) vs. only epidemiological associations helps prioritize which hypothesis:0007 recovery arms are genuinely "positive controls" vs. weaker tests.

**Broader relevance:**
- Provides a resource for "reverse aetiology" queries: given a mutation profile, which environmental agents are consistent? This is the inverse problem to the h08b discovery prong.
- The iPSC system's intact DDR and stable karyotype provide a cleaner substrate than tumor cell lines, making the catalog more applicable to early carcinogenic events rather than evolved tumor biology.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Putative treatment-associated SBS signature | COSMIC SBS reference signature | Paper signatures compared to project's restricted SigProfiler assignment targets |
| Cosine similarity to cancer-derived signatures | hypothesis:0007 positive-control recovery criterion (top-3 rank + FDR q<0.05) | Kucab cossim values set empirical expectation for what "recovery" looks like |
| Background signature (control iPSCs, SBS18-like) | Endogenous / artifact signatures flagged in the pipeline | Relevant to audit F1 / SBS27/43/45-60 artifact flags |
| Mutagenicity index (N_treat − N_ctrl)/N_ctrl | TMB / hypermutator annotation | Conceptually parallel; both normalize mutation load to a baseline |
| Metabolic activation (S9 mix) | Not modeled in current pipeline | cBioPortal studies capture end-state tumor mutations; metabolic state unknown |
| TC-NER transcriptional strand asymmetry | Not yet in pipeline | Potential downstream annotation for strand-aware signature analysis |

## Limitations

- **Single cell type.** All experiments used one human iPSC line. Tissue-specific DNA repair differences (e.g., TC-NER activity, MGMT expression, chromatin accessibility) could alter signatures in differentiated tissues — the authors explicitly acknowledge this.
- **Controlled concentrations ≠ chronic low-dose in vivo.** Treatment was acute (2–24 h at IC40–60), not the chronic low-dose exposures typical of environmental carcinogenesis. This may explain some signatures being undetectable or weaker than tumor-derived counterparts.
- **38/79 agents produced no detectable signature.** Including known carcinogens. This may reflect genuine low mutational efficiency, requirement for tissue-specific metabolism, or insufficient statistical power at the subclone numbers used.
- **S9 metabolic activation not standardized across agents.** Only 28/77 chemical agents were tested +S9; activation status is compound-specific and the human metabolic competence of iPSCs is unverified. Extrapolation of +S9 results to human in vivo exposure requires caution.
- **Double-substitution and indel analyses limited by small counts.** Many DBS and indel signature calls are based on low absolute counts, resulting in "unstable" signatures (marked in blue in the paper) that may not replicate at different concentrations or in independent experiments.
- **Cancer-comparison signatures unpublished at time of paper.** The 196 tissue-specific signatures extracted from 2,577 whole cancer genomes were described as "unpublished data" — comparison cosine similarities may not be fully reproducible from public resources at the time of publication.
- **No modeling of combined or sequential exposures.** Real human cancers arise from multiple overlapping exposures; this compendium characterizes single-agent effects only.

## Model / Tool Availability

- All 53 mutational signatures, double-substitution signatures, and indel signatures from this study are publicly available as a resource (see paper's Data and Software Availability section; downloadable from the paper's supplemental tables).
- Signatures were subsequently incorporated into the COSMIC mutational signatures catalog (v3+) and SigProfiler reference sets.
- The iPSC experimental system and protocols are described in STAR Methods; no software tool per se is released, but the analytical framework (background subtraction, SNR filtering, stability assessment) is documented and reproducible.

## Follow-up

- **Alexandrov et al. 2020 (Nature)** — the COSMIC v3 SBS catalog that incorporates and expands on these experimentally validated signatures; already in `doc/papers/` as Alexandrov2020 (referenced in hypothesis:0007).
- **Degasperi et al. 2022** — extends the framework to a larger cancer cohort and refines tissue-specific signatures; already in `doc/papers/`.
- Questions this raises for the project:
  - The Kucab compendium covers exogenous agents but not APOBEC or MMR endogenous processes. Does the hypothesis:0007 positive-control arm for APOBEC (SBS2/13) have a comparable "ground-truth" experimental reference from a different source?
  - For the cross-study aggregation pipeline, can the Kucab agent-to-signature mapping table be used as a lookup to flag studies enriched in particular exposures (e.g., high-platinum chemotherapy studies) that might inflate certain signatures?
  - The paper notes that 38/79 agents produced no detectable signature at IC40–60. At lower (chronic) doses used in real human populations, are some of these agents implicated in tumor signatures through accumulation rather than acute damage? This is relevant to hypothesis:0007 discovery of novel exposures.
