---
type: paper
title: Mutational signature analyses in multi-child families reveal sources of age-related
  increases in human germline mutations
status: active
created: '2026-05-31'
updated: '2026-06-28'
id: paper:Shojaeisaadi2024
ontology_terms:
- mutational signatures
- germline de novo mutations
- paternal age effect
- DNA mismatch repair
- SigProfiler
- whole-genome sequencing
- Mexican-American cohort
datasets: []
source_refs:
- cite:Shojaeisaadi2024
related:
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
- paper:Seplyarskiy2021
---

# Mutational signature analyses in multi-child families reveal sources of age-related increases in human germline mutations

- **Authors:** Habiballah Shojaeisaadi, Andrew Schoenrock, Matthew J. Meier, Andrew Williams, Jill M. Norris, Nicholette D. Palmer, Carole L. Yauk, Francesco Marchetti
- **Year:** 2024
- **Journal:** Communications Biology (7:1451)
- **DOI/URL:** https://doi.org/10.1038/s42003-024-07140-2
- **BibTeX key:** Shojaeisaadi2024
- **Source:** PDF

## Key Contribution

This germline-mutational-signature family study note links paper:Seplyarskiy2021.

This study characterises 2,479 validated germline de novo SNVs (DNMs) in 13 multi-child Mexican-American families using whole-genome sequencing, and applies three distinct mutational signature databases (COSMIC, human germline, CRISPR-Cas9 DNA-repair KO) to decompose the de novo SNV spectrum. The authors demonstrate a strong overall paternal age effect (PAE; ~1.29 additional DNMs per year of paternal age) with extensive inter-family variability in the slope, identify that C>T transitions at CpG sites increase specifically with older paternal age, and propose a model in which inaccurate DNA mismatch repair (MMR) — particularly inefficiency in the initiation and excision steps (EXO1, PMS1, PMS2) — is a major mechanistic contributor to the accumulation of germline DNMs with advancing paternal age.

## Methods

**Cohort:** The IRASFS (Insulin Resistance Atherosclerosis Family Study) Mexican-American population-based cohort. Thirteen multi-child families (2–6 children per family) were selected; 26 parents and 48 offspring were sequenced. Mean paternal age at birth: 27.5 ± 6.4 years (range: 16.4–41.2 years). WGS at ~30x median depth (Illumina HiSeq X Ten; 150 bp paired-end; GRCh38 alignment via BWA-MEM v0.7.17; GATK v4.0.11.0 best-practices pipeline).

**Variant calling:** Two complementary tools — DeNovoGear (identified 123–387 candidates per child) and GATK (24–111 per child); >90% of GATK calls were confirmed by DeNovoGear. A merged set of 11,590 candidate SNVs was generated after quality filtering (read depth ≥12, GQ ≥20, AAF <10% in parents, forward+reverse read support). Targeted resequencing (SureSelect custom baits, Illumina HiSeq 4000, ~300x) of 6,118 candidates validated 2,479 SNVs.

**Parent-of-origin phasing:** Unfazed (read-based phasing) complemented by WhatsHap; all phased SNVs visually validated in IGV.

**Signature analysis:** SigProfilerMatrixGenerator v1.1 (hg38) + SigProfilerExtractor (v1.0.18) for de novo extraction; SigProfilerExtractor for decomposition and fitting against:
1. COSMIC SBS v3.3.1 (79 SBS signatures from PCAWG WGS);
2. Human germline SBS dataset — 14 components from Seplyarskiy et al. 2021 (TOPMed cohort);
3. Nine SBS signatures from CRISPR-Cas9 KO of DNA repair genes in human iPSCs (Zou et al. 2021).

Cosine similarity used to evaluate goodness-of-fit for reconstructed signatures.

**Statistical analyses:** Poisson regression (Lme4 v1.1-35.1) for PAE slope and confidence intervals; R v4.0.2.

## Key Findings

**DNM rate and PAE:**
- Average germline DNM rate: 1.03 × 10⁻⁸ (95% CI: 0.96–1.1 × 10⁻⁸) per base pair per generation; consistent with prior trio-based studies.
- Overall PAE slope: 1.29 additional SNVs per year of paternal age (95% CI: 0.83–1.74; p < 0.0001).
- Extensive inter-family variability: per-family slopes ranged from −1.88 (Family 09; youngest father, possibly stochastic) to +6.52 (Family 05) additional SNVs per year.

**Parent-of-origin:**
- 78.6% (95% CI: 71.7–85.6%) of phased autosomal SNVs were of paternal origin; 5.4:1 paternal:maternal ratio.
- Paternally-phased SNVs increased significantly with paternal age (R²adj = 0.14; p = 5.4 × 10⁻⁸); maternally-phased SNVs showed no significant correlation with paternal age (R²adj = −0.21; p = 0.63).

**Mutation spectrum:**
- C>T transitions are the most common DNM type overall; at CpG sites specifically (CCG, GCG, TCG motifs), C>T transitions increase with paternal age.
- ACG trinucleotide context had the highest absolute mutation counts.
- C>A and T>A transversions were least common.

**COSMIC decomposition:**
- The extracted de novo SNV signature was best reconstructed by SBS5 (~85%) + SBS1 (~15%) (cosine similarity = 0.989).
- SBS1 (spontaneous 5mC deamination, clock-like) + SBS5 (unknown etiology, replication-independent, clock-like) are the two COSMIC signatures required.
- The GEL expanded COSMIC repertoire (2022) did not change this finding (~73% SBS5, ~27% SBS1; cosine similarity = 0.972).

**Human germline decomposition:**
- Best fit achieved with germline components 1, 3, and 10 in decreasing proportions (~45%, ~18%, ~37%); cosine similarity = 0.954.
- Component 1 (~45%): asymmetric resolution of bulky DNA damage (replication-independent, strand-dependent, NER-associated).
- Component 10 (~37%): C>T transitions at NpCpG sites — 5mC deamination or erroneous replication over 5mC.
- Component 3 (~18%): replication error footprint (C>T at non-CpG sites).

**DNA repair KO decomposition:**
- Best fit by KO of three MMR genes: ΔEXO1 (~41%), ΔPMS1 (~35%), ΔPMS2 (~24%); cosine similarity = 0.915.
- ΔEXO1: relatively high T>C transitions at ATA and TTA motifs (HR and MMR roles).
- ΔPMS1: predominantly C>T transitions at NpCpG and ACA motifs.
- ΔPMS2: C>T transitions at ATA, ATG, CTG trinucleotides.
- These three genes implicate MMR initiation (PMS1/PMS2 as components of MutLα) and lesion excision (EXO1) as critical steps.

**Proposed mechanistic model (Fig. 7):**
- DNA damage (5mC deamination, mismatches, replication errors, bulky adducts/unknown) accumulates in germline.
- MMR efficiency declines with paternal age — especially at initiation and excision steps.
- NER efficiency also implicated (via component 1) but not directly testable (NER gene KO causes lethality in hiPSCs).
- Model proposes that declining MMR — not simply increased replication errors from more cell divisions — drives age-related DNM accumulation.

**Signature age-stratification:**
- Attempt to extract separate signatures from youngest (<24 years) vs oldest (>33.1 years) paternal-age quartiles produced reconstructed signatures with lower cosine similarities (insufficient mutations per stratum), preventing robust differential conclusions.

## Relevance

This paper is relevant to hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and (agnostic covariate↔signature-exposure association) in the following ways:

1. **Germline signature aetiologies as a reference frame for non-cancer contexts.** The paper applies the human germline signature compendium [@Seplyarskiy2021] (14 components) to de novo SNVs, demonstrating that germline and somatic mutation signatures have overlapping but distinct aetiological mappings. The germline compendium is an alternative reference frame to COSMIC for projects involving normal/germline-adjacent mutation accumulation — relevant background when building the hypothesis:0007 positive-control panel.

2. **SBS1 and SBS5 as clock-like signatures.** The finding that COSMIC decomposition requires only SBS1 (5mC deamination, age-correlated) and SBS5 (unknown/replication-independent, age-correlated) to explain germline de novo SNVs reinforces the identification of SBS1 and SBS5 as clock-like processes operating in normal cells. For hypothesis:0007, this means that age — not just cancer-specific exposures — is a primary covariate driving SBS1/SBS5 exposures across cBioPortal studies; these signatures should be modelled with age as covariate rather than as discovery targets in H08b.

3. **MMR deficiency as a signature aetiology.** The decomposition against DNA-repair KO signatures identifies EXO1, PMS1, and PMS2 as critical MMR components. In the somatic cancer setting, MMR deficiency (MSI-H) is a well-established positive-control aetiology for the hypothesis:0007 recovery arm (SBS6/15/26/44). This paper provides mechanistic grounding for why MMR deficiency produces specific spectral patterns — informing the interpretation of MMR-associated signatures in the cancer meta-analysis.

4. **Inter-family variability as a warning for within-study heterogeneity.** The extensive inter-family variability in the PAE slope (ranging from negative to +6.52 per year) illustrates that family/study structure must be accounted for even when studying a single biological process. By analogy, inter-study heterogeneity in cBioPortal is expected to be at least as large — supporting the pipeline's use of per-study stratification and matched-normal flags.

5. **Mexican-American cohort — population diversity.** The finding that PAE and its inter-family variability are independent of ethnicity (consistent with results from Amish, Middle Eastern, and CEPH/Utah cohorts) supports the use of multi-ethnic cBioPortal studies without requiring ethnicity stratification for the clock-like signatures (SBS1/SBS5).

6. **Scope boundary (germline vs somatic).** This paper's scope is strictly germline DNMs, not somatic mutations. Its direct application to the cBioPortal cross-study meta-analysis is therefore limited — cBioPortal studies sequence tumours, not germline. The relevance is primarily as mechanistic background for why certain signatures (SBS1, SBS5, germline components 1/3/10) are clock-like and age-dependent, which informs covariate selection in the hypothesis:0007 association model.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| SBS1 + SBS5 (germline DNMs) | Clock-like positive-control signatures; age nuisance covariate | Must include age in hypothesis:0007 covariate model to avoid confounding |
| ΔEXO1 / ΔPMS1 / ΔPMS2 repair KO signatures | MMR-deficiency aetiologies (SBS6/15/26/44 in COSMIC) | Germline and somatic MMR signatures share spectral features |
| Human germline components 1, 3, 10 | Non-COSMIC germline reference — alternative signature frame | Not used in current pipeline; informative for future normal-tissue analyses |
| Paternal age effect slope variability | Study-level heterogeneity in mutation rate | Supports per-study stratification in cBioPortal meta-analysis |
| Multi-child family design | N/A (cBioPortal is per-tumour, not pedigree-based) | Design is specific to germline context |

## Limitations

- The 13-family cohort is small (N = 48 offspring); inter-family variability estimates are imprecise, and age-quartile signature extraction was underpowered.
- The paternal age range within each family is limited (~10 years difference between oldest and youngest sibling's paternal age), constraining the ability to detect age-dependent signature shifts within families.
- All three signature databases used contain proposed aetiologies that are not fully experimentally validated; cosine similarity-based decomposition identifies associations, not causes.
- The DNA repair KO signatures are from hiPSCs — only genes viable in that model system were tested, excluding NER genes (which cause lethality when knocked out in hiPSCs). The role of NER cannot be directly quantified.
- Scope is restricted to germline SNVs; indels were not analysed for signatures. No somatic tumour data.
- The IRASFS cohort is predominantly female (64.6%) with near-normal lipid levels — a healthy, metabolically selected population; results may not generalise to all human populations even within Mexican-American ancestry.
- Maternal age was not available for this cohort, so maternal DNM accumulation rate could not be directly modelled against maternal age.

## Model / Tool Availability

- **SigProfiler suite:** used for all signature extraction, decomposition, and fitting.
  - SigProfilerExtractor: https://github.com/AlexandrovLab/SigProfilerExtractor
  - SigProfilerMatrixGenerator: https://github.com/AlexandrovLab/SigProfilerMatrixGenerator
- **Analysis workflow (SNVs_DNMs_IRASFS):**
  - GitHub: https://github.com/hashoja/SNVs_DNMs_IRASFS
  - Zenodo: https://doi.org/10.5281/zenodo.13864620
- **WGS data:** Sequence Read Archive, accession PRJNA1166126.
- **2,479 validated SNVs:** listed in Supplementary Data.
- **CRISPR-Cas9 DNA repair KO signatures:** Zou et al. 2021 (Nat. Cancer 2:643–657); https://doi.org/10.17632/ymn3ykkmyx

## Follow-up

- Seplyarskiy et al. 2021 (Science 373:1030–1035) — the human germline compendium of 14 components used in this study; read for context on germline-specific mutational processes.
- Zou et al. 2021 (Nat. Cancer 2:643–657) — the CRISPR-Cas9 DNA repair KO signature dataset; relevant for understanding MMR-associated spectral patterns in the somatic context.
- For hypothesis:0007: confirm that age is included as a nuisance covariate when testing SBS1/SBS5 associations (already flagged in Alexandrov2020 relevance notes).
- For future normal-tissue analyses (hypothesis:0005): this paper's germline framework (14-component human germline signatures) may be more appropriate than COSMIC for characterising normal-tissue somatic mosaicism or clonal haematopoiesis.
