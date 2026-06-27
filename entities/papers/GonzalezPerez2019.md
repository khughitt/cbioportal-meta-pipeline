---
type: paper
title: Local Determinants of the Mutational Landscape of the Human Genome
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: paper:GonzalezPerez2019
ontology_terms:
- mutational signatures
- somatic mutation
- chromatin structure
- nucleosome
- transcription factor binding
- DNA repair
- mutation rate
- APOBEC
- UV mutagenesis
- mismatch repair
datasets: []
source_refs:
- cite:GonzalezPerez2019
related: []
---

# Local Determinants of the Mutational Landscape of the Human Genome

- **Authors:** Abel Gonzalez-Perez, Radhakrishnan Sabarinathan, Nuria Lopez-Bigas
- **Year:** 2019
- **Journal:** Cell, 177(1): 101–114
- **DOI/URL:** https://doi.org/10.1016/j.cell.2019.02.051
- **BibTeX key:** GonzalezPerez2019
- **Source:** PDF

## Key Contribution

This Leading Edge Review synthesizes how sub-megabase chromatin features — nucleosome occupancy, transcription factor binding sites (TFBS), transcriptional state, and secondary DNA structures — locally modulate somatic mutation rates by differentially influencing both DNA damage generation and the efficiency of DNA repair machineries (NER, BER, MMR). It provides a mechanistic framework for why canonical mutational signatures (UV→SBS7, tobacco→SBS4, APOBEC→SBS2/13, oxidative damage→SBS17, MMR-loss→SBS6/15/26) show characteristic spatial patterns across the nucleosome-linker landscape, and argues that this local variation has implications for driver-gene identification, tumour evolution, and chemotherapy-resistance research.

## Methods

This is a narrative review, not an empirical study. The authors synthesise primary literature spanning:

- Genome-wide nucleosome position maps (MNase-seq, chemical mapping), TFBS ChIP-seq, and DNase I hypersensitivity data.
- Single-nucleotide resolution somatic SNV catalogues from thousands of tumours (primarily TCGA/ICGC cohorts) and large germline variant datasets (1000 Genomes, de novo variant trios).
- Experimental damage maps: whole-genome CPD maps (UV), BPDE-dG adduct maps (tobacco carcinogens), 8-oxo-G maps (reactive oxygen species).
- Mutational signature decompositions from COSMIC (SBS catalogue, Alexandrov et al.).

The key methodological point (Box 2) is that local mutation rate enrichment requires comparison to a *sequence-context-corrected expected rate* based on flanking regions, not raw counts, to avoid confounding by local nucleotide composition.

## Key Findings

### Nucleosome–linker periodicity of mutation rate

- Mutation rates differ between nucleosome cores and inter-nucleosomal linker regions, but the direction depends on the mutational process:
  - **UV (SBS7):** mutation rate is higher *within* nucleosomes because NER efficiency is reduced where DNA is wrapped around histone octamers (less accessible to repair machinery), even though CPD damage itself is generated at roughly equal rates in cores and linkers.
  - **Tobacco/BPDE-dG (SBS4):** mutation rate is higher *at linkers*; BPDE-dGs are generated more in linkers, and NER also repairs them less efficiently in nucleosome-covered regions — the two effects combine to enrich mutations at linkers.
  - **Oxidative damage / ROS (SBS17, esophageal/gastric):** higher mutation rate in nucleosomes, likely because BER acts less efficiently at minor-in (nucleosome-facing) segments.

### 10-bp rotational periodicity within nucleosomes

- Within nucleosome-covered DNA, a 10-bp periodic pattern of mutation rate exists reflecting rotational positioning: whether the DNA minor groove faces the histone core (minor-in) or faces outward (minor-out).
- UV-induced CPDs accumulate more in minor-out segments (exposed, more susceptible to damage generation) while their repair by NER is more efficient in minor-out; the net result is a mutation enrichment at minor-out for UV (SBS7).
- For oxidative damage, BER is less efficient at minor-in segments, producing an opposite pattern for SBS17.
- This fine-scale periodicity has been proposed to be the mechanistic origin of the WW (A/T dinucleotide) periodicity observed in eukaryotic genomes.

### Transcription factor binding sites (TFBS)

- Open chromatin (DHS) regions accessible to NER/BER show *lower* overall somatic mutation rates.
- However, within DHS regions, TF binding footprints show *elevated* mutation rates despite being in open chromatin — because the bound TF itself physically blocks repair machinery access to the DNA it covers.
- In melanomas (UV damage), active TFBS show a striking mutation rate peak; CTCF binding sites similarly show elevated somatic C>T mutations (SBS7) in melanomas.
- TF binding also influences damage generation: different TFs alter DNA conformation, affecting CPD formation probability in a TF-specific and strand-specific manner.
- In colorectal and other non-UV tumours, CTCF sites show elevated T>[GC]A and related substitutions, attributed to reduced repair rather than UV damage.
- Tissue-specific TFs (e.g. estrogen receptor in breast, androgen receptor in prostate) show elevated mutation rates at their cognate sites in the relevant tumour types.

### Transcription-related mutation rate variation in genic regions

- **Transcription-coupled repair (TC-NER):** Preferentially corrects DNA lesions on the template strand, causing asymmetric accumulation of UV and alkylating-agent mutations on the non-template strand. Signatures with transcriptional strand bias include SBS7, SBS4, SBS11.
- **Transcription-coupled damage (TCD):** APOBEC (SBS2/13) and some A>G substitutions in liver cancers (SBS13) also show strand bias traceable to damage asymmetry generated by single-stranded DNA during transcription.
- **Exon-protective MMR:** Exons show *lower* than expected mutation rates (beyond what TC-NER explains) in MMR-proficient tumours; this is driven by recruitment of MMR (via H3K36me3 at exonic nucleosomes) that corrects mismatches in exons more efficiently than introns.
- 3' ends of highly expressed genes are enriched for A>G substitutions from error-prone MMR acting on H3K36me3-rich regions.

### Other secondary structures and local features

- Single-stranded DNA regions (R-loops, G-quadruplexes, hairpins, inverted repeats, Z-DNA zones) cover 0.07–4% of the genome and show elevated somatic mutation rates at these rare loci.
- G-quadruplexes show enriched mutations at single-stranded loop segments.
- DNA curvature also contributes: mutations are depleted in high-curvature regions genome-wide.

### Implications

- Local chromatin context must be accounted for in cancer driver-gene discovery methods; elevated TFBS mutation rates could generate false-positive promoter driver candidates (e.g. TERT promoter hotspots may partly reflect local NER deficiency at the ETS binding motif rather than positive selection alone).
- Differential local repair shapes the background mutation rate used by tools like MutSigCV/dNdScv — failure to correct for it inflates false-positive driver calls.
- Chemotherapy agents that damage DNA (e.g. platinum compounds, alkylating agents) will generate mutations whose distribution is sculpted by the same local chromatin accessibility rules, with implications for understanding treatment-induced secondary malignancies.

## Relevance

This review is directly relevant to **hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and (agnostic covariate↔signature-exposure association; positive-control recovery)**:

1. **Positive-control mechanistic ground truth (H08a):** The paper provides the clearest mechanistic account of *why* the canonical signature↔aetiology links are what they are — UV→SBS7 because NER is inhibited in nucleosomes; tobacco→SBS4 because BPDE-dG adducts accumulate at linkers; APOBEC/AID→SBS2/13 via C>U deamination of single-stranded DNA during transcription; MMR-loss→SBS6/15/26 because exonic MMR is disrupted. Understanding the mechanism behind these links clarifies what features an agnostic covariate association should recover and *why* those are the right targets.

2. **Tissue-level collinearity confound (R1 in hypothesis:0007):** Several signatures reviewed here (e.g. UV in melanoma, tobacco in lung) are confounded with tissue of origin. The review's discussion of TF tissue-specificity underscores that conditioning on tissue/cancer-type is essential before interpreting any exposure↔signature association — directly supporting the hypothesis:0007 design requirement for within-tissue strata.

3. **Expression as a mechanistic mediator:** The review's treatment of TC-NER, TCD, and MMR-via-H3K36me3 establishes that gene *expression level* and *transcriptional activity* are mechanistically upstream of mutation rate for multiple signatures (SBS2/13 via single-stranded DNA during transcription; SBS7 via TC-NER; MMR via H3K36me3). This provides prior justification for the hypothesis:0007 prediction that APOBEC3 expression modules will associate with SBS2/13 independently of clinical covariates.

4. **Non-UV background rate confounds:** The review clarifies that nucleosome occupancy, replication timing, and GC content all shape the background mutation rate against which signature exposures are measured. For cross-study meta-analysis in this project, this reinforces the importance of per-cancer-type normalization and the hypermutator annotation pipeline (t081).

5. **Driver-gene false-positive risk:** The discussion of TFBS hotspots as potential false-positive driver candidates (e.g. TERT, TP53 promoter) is relevant to any driver-enrichment analysis downstream of the mutation-frequency tables.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Mutational signature (SBS) | Signature exposure (COSMIC SBS catalogue) | Project uses SigProfiler restricted assignment against COSMIC v3 |
| Local mutation rate variation | Background mutation rate heterogeneity | Affects normalization in create_freq_tables.py |
| NER deficiency at TFBSs | Potential batch/artifact signal | TFBS-enriched mutations could inflate gene-level ratios for promoter-proximal genes |
| TC-NER strand asymmetry | Transcriptional strand bias (SBS7, SBS4) | Relevant to hypothesis:0007 positive-control arms for UV/tobacco |
| MMR-driven exon protection | Exon vs intron mutation stratification | Not currently implemented in pipeline but noted in hypothesis:0007 rationale |
| 5mCpG deamination clock | Clock-like signatures SBS1/SBS5 | Paper discusses replication-timing dependence of CpG>TpG rates |

## Limitations

- As a review (2019), coverage is limited to studies available at that time; more recent high-resolution damage/repair maps and updated COSMIC v3.3+ signatures are not discussed.
- The review focuses on single-nucleotide substitutions (SNVs); indels and structural variants are largely excluded, even though MMR-deficiency produces characteristic indel signatures (ID1-2).
- The paper does not address tumour-type-specific mutational processes comprehensively — it uses selected cancer types as illustrative examples rather than providing systematic cross-cancer analysis.
- The mechanistic framework is primarily inferred from correlational genomic data and in vitro/yeast experimental systems; causal dissection in human tumour cells remains incomplete.
- The boundary between "local chromatin effect on mutation rate" and "selection on local sequence" is acknowledged but not always cleanly separated (e.g., nucleosome-sequence co-evolution discussion).

## Model / Tool Availability

This is a review article and does not release a new tool or dataset. The review references COSMIC signatures (https://cancer.sanger.ac.uk/cosmic/signatures) and various publicly available genomic datasets (ENCODE, TCGA, 1000 Genomes).

## Follow-up

- **Alexandrov et al.** [@Alexandrov2020] — the comprehensive COSMIC v3 signature compendium; referenced as the primary signature catalogue hypothesis:0007 will use for restricted assignment.
- **Degasperi et al. 2022** (Science) — extends signature extraction to paired tumour/normal and organ-specific contexts; already in project.
- **Frigola et al. 2017** (Nat Genet) — MMR-mediated exon protection cited in this review; relevant to whether exon-level mutation ratios in the pipeline need MMR-correction.
- **Sabarinathan et al. 2016** (Nature) — NER impairment at TF binding sites in melanomas; key primary paper behind one of the TFBS findings summarized here.
- **Pich et al. 2018** (PLoS Genet) — whole-genome nucleosome periodicity of somatic and germline mutations; primary data paper underpinning the 10-bp periodicity finding.
- Questions for project: Does the pipeline's per-gene mutation ratio inadvertently confound promoter-proximal genes (high TFBS density) with genuine driver signal? Would conditioning on replication timing improve the hypothesis:0007 positive-control recovery of signatures correlated with replication (SBS1, SBS5)?
