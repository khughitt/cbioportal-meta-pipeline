---
id: "paper:Everall2026"
type: "paper"
title: "Comprehensive repertoire of the chromosomal alteration and mutational signatures across 16 cancer types"
status: "active"
ontology_terms:
  - mutational signatures
  - structural variation
  - copy number aberration
  - COSMIC
  - whole-genome sequencing
  - pan-cancer
datasets: []
source_refs:
  - "cite:Everall2026"
related:
  - "paper:Alexandrov2020"
  - "paper:Degasperi2022"
  - "paper:Islam2022"
  - "paper:Steele2022"
created: "2026-05-31"
updated: "2026-05-31"
---

# Comprehensive repertoire of the chromosomal alteration and mutational signatures across 16 cancer types

- **Authors:** Andrew Everall, Avraam Tapinos, Aliah Hawari, Alex J. Cornish, Amit Sud, Daniel Chubb, Ben Kinnersley, Anna Frangou, Miguel Barquin, Josephine Jung, David N. Church, Ludmil B. Alexandrov, Richard S. Houlston, Andreas J. Gruber, David C. Wedge (equal contributors: Everall, Tapinos, Hawari, Cornish; joint senior: Houlston, Gruber, Wedge)
- **Year:** 2026
- **Journal:** Nature Genetics, Volume 58, pp. 570–581 (March 2026)
- **DOI/URL:** https://doi.org/10.1038/s41588-025-02474-x
- **BibTeX key:** Everall2026
- **Source:** PDF

## Key Contribution

Using WGS from 10,983 patients across 16 tumor types in the 100,000 Genomes Project (100KGP), this study performs the most comprehensive joint extraction of all five somatic mutation classes — SBS, DBS, ID, CN, and SV — generating 134 signatures, of which 26 are new to COSMIC. Crucially, it introduces a COSMIC reference set for structural variation (SV) signatures, derived de novo for the first time at this scale. By systematically associating these signatures with clinical phenotypes, histological subtypes, DNA repair gene inactivation, therapy exposure, clonality timing, and patient survival, the paper moves the COSMIC catalog from a static spectral reference toward a functionally annotated resource that directly supports precision oncology.

## Methods

- **Cohort:** 10,983 tumors across 16 cancer types (bladder, breast, CNS, colorectal, haematological, head and neck, hepatopancreatic, kidney, lung, ovary, prostate, sarcoma, skin, testis, upper gastrointestinal, uterus) from the 100KGP WGS program. 371,254,410 mutations analyzed.
- **Signature extraction:** SigProfilerExtractor (SPE) applied per tissue type. SBS signatures expanded to 288 classes (transcriptional strand context). DBS, ID, and CN signatures classified by type, size, and clustering per COSMIC conventions. SV signatures — new to COSMIC — characterized into 10 components (clustered/nonclustered deletions, inversions, translocations) across 20 classes.
- **Signature catalog update logic:** New signatures added sequentially (smallest maximum cosine similarity to any existing reference < 0.8, or not decomposable from the reference list). Two COSMIC reference signatures (SBS24/29) showed no activity in any sample.
- **Association framework:** (a) Spearman correlations across all 134 signatures (inter-signature relationships); (b) logistic and negative-binomial regression of signature activity against tumor histology subtype and grade (Fig. 4, 6); (c) logistic/NB regression against DNA repair gene inactivation (Fig. 5a); (d) regression against therapy exposure (Fig. 5b); (e) ranked comparison of subclonal fraction per signature (Mann-Whitney, Fig. 7); (f) Cox proportional hazard (CPH) models for overall survival adjusting for age, sex, grade, and PCs (Fig. 8). FDR control via Benjamini-Hochberg.
- **Clonality assessment:** Subclonal vs clonal fractions of mutations per signature type tested using Wilcoxon rank-sum across tumor groups.

## Key Findings

### New signatures
- **134 signatures total** (67 SBS, 19 DBS, 18 ID, 20 CN, 10 SV); 26 are new to COSMIC, including SBS96–98, DBS12–19, ID19–22, CN25, and 10 SV signatures (SV1–SV10).
- **SV signatures:** SV1–SV6 match previously reported breast cancer signatures; SV7–SV10 are new. SV1/SV3 feature nonclustered tandem duplications (>100 kb and <100 kb). SV2/SV4 are translocations. SV5/SV7 are small deletions. SV8 is small inversions. SV9/SV10 are complex multi-type rearrangements.
- **CN25** is characterized by <1-Mb LOH deletions linked to chromothripsis, distinctive in that it reflects diploid/single-copy LOH states (unlike other CN chromothripsis signatures CN4–CN8).
- **SBS98** (NCG context, similar to SBS87) is linked to thiopurine treatment in acute lymphoblastic leukemia. **SBS96** has a broad mutation profile in a minority of kidney cancers. **SBS97** (C>T dominated, similar to SBS7b) is a skin cancer / sarcoma feature.
- **DBS13** (TC-dinucleotide mutations, HRD-linked) was found in breast, ovarian, and uterine cancers, associated with HRD signatures SBS3, ID6, and CN17.

### Signature co-clustering and relationships
- Hierarchical clustering (Ward/Euclidean on log-activity) reveals distinct clusters: UV (SBS7), smoking (SBS4, SBS92), HRD (SBS3, ID6, CN17), POLE, MMR/dMMR, and APOBEC (SBS2, SBS13) — Fig. 3.
- SV4, SV6, SV9, CN6, CN7 associated with chromothripsis across multiple tumor groups (e.g. SV4 with breast ductal carcinoma and colorectal adenocarcinoma, P = 3.5×10⁻⁶³).
- CN6 and CN7 enriched in WGD tumors (e.g. Breast-DuctalCA, P = 2.6×10⁻²²). CN9 was a non-WGD specific feature.
- APOBEC (SBS2, SBS13) active in 88% bladder, 89% head and neck, 69% breast, 37% lung tumors, and 38% sarcomas out of 10,983 total.

### Aetiology associations
- **dMMR:** SBS15/26/44 (and SBS93, DBS4, ID14) linked to MSH6 inactivation in CRC; SBS26/SBS44 linked to MLHI inactivation and 5-FU treatment; CN25 associated with somatic MSH6.
- **HRD:** SBS3, ID6, CN17 associated with grade in breast cancer and with BRCA2 germline mutation; 381 (17%) breast, 134 (30%) ovarian, 41 (4%) lung, 33 (5%) uterus, 28 (5%) sarcoma samples show evidence of HRD (nonzero activity in at least two of SBS3, ID6, CN17).
- **POLE:** SBS10a/10b linked to POLE inactivation in uterine adenocarcinoma and CRC; POLE-mutated tumors have better clinical outcomes.
- **Therapy:** DBS5 (oxaliplatin) in CRC; ID8 associated with radiotherapy in CNS-GBM-IDHwt, head and neck, and primary CNS (ID8 also linked to NHEJ inactivation); DBS5 and DBS2 (radiotherapy) identified.
- **MUTYH:** SBS18 linked to germline MUTYH across CRC, prostate, and ovarian adenocarcinoma; SBS18 mutations are relatively clonal, consistent with pre-tumorigenic accumulation.
- **E. coli / SBS88:** Rectal cancers (vs colon) enriched for SBS88 (pks+ E. coli colibactin exposure), active early in life; concordant with rising early-onset CRC incidence.
- **Aristolochic acid:** SBS22 in kidney PRCC and clear cell RCC; SBS22 inversely associated with SBS88 in CRC.

### Timing (clonality)
- Exogenous process signatures (UV — SBS7a/7b, tobacco — SBS4) are more clonal than endogenous (dMMR — SBS26/44), consistent with early mutagenic exposure. APOBEC (SBS2/13) occurs later (predominantly subclonal in breast, colorectal, and lung, particularly in clonal sweeps — Fig. 7).
- SBS1 (CpG deamination) was more likely subclonal than UV mutations in melanoma, or aristolochic acid mutations in kidney cancers.

### Clinical relevance / survival
- HRD (SBS3) and APOBEC (SBS2/13) are associated with poorer OS in Breast-DuctalCA after adjusting for grade (OS Cox P = 2.2×10⁻², 3.5×10⁻²); these associations do not survive ER-status adjustment.
- SBS17b associated with reduced OS in ColoRect-AdenoCA (P = 1.9×10⁻³).
- CN17 active in 88/296 Bladder-TCC significantly reduces OS (P = 5.9×10⁻³).
- ID8 burden associated with reduced OS in CNS-GBM-IDHwt, likely confounded by recurrent vs primary tumor type.

## Relevance

This paper is directly relevant to **hypothesis h08** (agnostic covariate–signature-exposure association) at multiple levels:

**H08a — positive-control recovery:** Everall et al. provide the ground-truth association map against which the h08 agnostic scan must be validated. Their large-scale systematic regression of signature exposures against histology, DNA repair gene status, therapy, and clinical features is exactly the canonical "known map" that H08a must recover unprompted:
- UV ↔ SBS7a/7b (skin melanoma; strong and clonal)
- Smoking ↔ SBS4/SBS92 (Lung-AdenoCA; SBS92 distinct from SBS4, see Fig. 3)
- APOBEC ↔ SBS2/13 (bladder, head and neck, breast; predominantly subclonal — a timing clue)
- MMR loss ↔ SBS15/26/44/SBS93/ID14 (CRC; MSH6, MLH1 inactivation)
- POLE ↔ SBS10a/10b (uterine, CRC)

**H08b — discovery candidate:** CN25 / MSH6 somatic, SBS17a/b / POLG inactivation, and the APOBEC–immunotherapy link are examples of associations whose mechanistic basis is not fully understood, suitable targets for an agnostic discovery scan. The expression module angle (APOBEC3A/B co-expression↔SBS2/13) identified in h08 is supported by Everall et al. observing that APOBEC is the single most prevalent exogenous signature class across the cohort (88% bladder, 69% breast) — strong signal in any co-expression module association.

**Cross-study meta-analysis context:** The 100KGP cohort (10,983 WGS) is larger and uses matched normals — it is the kind of high-quality WGS reference that validates cBioPortal-based panel-sequencing signature inferences. The CH-contamination problem (h01) is addressed here by the 100KGP matched-normal design; the subclonal fraction analysis (Fig. 7) is a resource for understanding which signatures in cBioPortal studies are most likely CH-confounded (CH signatures like DNMT3A are predominantly clonal; dMMR signatures are subclonal).

**SV signatures:** The new SV reference (SV1–SV10) is out of scope for the current cBioPortal pipeline (which aggregates point mutations / small indels from MAF files), but is relevant background for understanding chromothripsis (CN4–CN8, CN25) and HRD (SV3/SV5) in future modality expansions.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| 134 extracted signatures (SBS/DBS/ID/CN/SV) | Reference signature catalog for restricted assignment | Input to `run_restricted_sigprofiler_assignment.py` |
| 26 new COSMIC signatures | Potential update to reference SBS catalog used in h08 | Check whether these appear in COSMIC v3.4 used by the pipeline |
| Signature-histology regression (logistic/NB) | h08 agnostic association model output | Everall uses per-tissue logistic regression — same design as h08 |
| Subclonal fraction per signature (Fig. 7) | CH-contamination annotation (h01, t081) | Clonal CH-like vs subclonal dMMR signals — relevant to matched-normal flag |
| Matched-normal 100KGP design | `matched_normal_studies` config parameter | Validates that CH signatures SBS5/SBS40 are depleted in matched-normal studies |
| APOBEC subclonal timing | h08 positive control (APOBEC↔SBS2/13 arm) | Subclonality pattern predicts co-expression association will be late-developmental |

## Limitations

- The 100KGP cohort is UK-based and has limited ethnic diversity; the authors note this limits germline variant associations (no significant germline-ancestry effects found, possibly underpowered).
- The SV signature framework covers only 10 components; all are de novo and require further functional validation.
- CN25 etiology (MSH6-associated LOH) is new and has no prior COSMIC entry — mechanistic validation is pending.
- COSMIC's iterative addition of signatures creates linear dependence: 66/42 of current COSMIC SBS signatures can be produced by linear combinations of others (cos(sim) > 0.8). The paper proposes but does not implement a solution to this redundancy problem.
- The SBS96–98 new signatures have only partial mechanistic validation; SBS97 etiology remains uncertain.
- Survival associations are generally not study-wide significant after multiple testing correction; flagged as hypothesis-generating rather than definitive.
- Causal direction is not established for most signature–clinical associations (acknowledged by the authors).

## Model / Tool Availability

- SigProfilerExtractor (SPE) used for de novo extraction — publicly available (PyPI).
- Signature profiles and activity matrices to be deposited per the 100KGP data access policy (data access through Genomics England Research Environment).
- Extended Data, Supplementary Tables (12 tables), and Supplementary Notes available at the DOI.
- New signature profiles available at https://doi.org/10.1038/s41588-025-02474-x (Online content).

## Follow-up

- Compare the 26 new COSMIC signatures against the version of the COSMIC reference currently used in the pipeline's restricted-assignment step; determine whether SBS96–98 / DBS12–19 / ID19–22 require a catalog update.
- Examine Supplementary Table 3 (etiologies for all 134 signatures) as an input to the h08 positive-control design — specifically which signatures have *confirmed* vs *unknown* aetiology and can serve as positive vs negative controls.
- The SBS17a/b–POLG association (colorectal, Fig. 4/5) is a novel candidate for the h08 discovery prong; also the CN25–MSH6 link.
- The paper's clonality data (Fig. 7) provide empirical prior probabilities that APOBEC mutations are subclonal — useful for weighting in any cross-study signature-exposure model.
- Consider citing as supporting evidence in the h08 pre-registration (H08a arms 1–3 have explicit empirical grounding in Everall et al.'s Figs. 3–5).
