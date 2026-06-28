---
type: paper
title: Germline predisposition to pediatric Ewing sarcoma is characterized by inherited
  pathogenic variants in DNA damage repair genes
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: paper:Gillani2022
ontology_terms:
- germline predisposition
- Ewing sarcoma
- DNA damage repair
- Fanconi anemia
- pediatric cancer
- case-control study
datasets: []
source_refs:
- cite:Gillani2022
related: []
---

# Germline predisposition to pediatric Ewing sarcoma is characterized by inherited pathogenic variants in DNA damage repair genes

- **Authors:** Riaz Gillani, Sabrina Y. Camp, Seunghun Han, Jill K. Jones, Hoyin Chu, Schuyler O'Brien, Erin L. Young, Lucy Hayes, Gareth Mitchell, Trent Fowler, Alexander Gusev, Junne Kamihara, Katherine A. Janeway, Joshua D. Schiffman, Brian D. Crompton, Saud H. AlDubayan, Eliezer M. Van Allen
- **Year:** 2022
- **Journal:** The American Journal of Human Genetics, vol. 109, pp. 1026–1037
- **DOI/URL:** https://doi.org/10.1016/j.ajhg.2022.04.007
- **BibTeX key:** Gillani2022
- **Source:** PDF

## Key Contribution

This study identifies a distinct germline predisposition pattern in Ewing sarcoma driven by inherited pathogenic variants in DNA damage repair (DDR) genes, particularly heterozygous loss-of-function variants in *FANCC* (a Fanconi anemia gene), validated across two independent cohorts. Unlike osteosarcoma and rhabdomyosarcoma — where *TP53* is the dominant germline predisposition gene — Ewing sarcoma shows no enrichment for pathogenic germline *TP53* variants and instead harbors a broader DDR gene signal spanning *FANCC*, *FANCA*, *CHEK2*, and *ERCC2*. Trio-based parent-proband sequencing demonstrates that these DDR variants are predominantly inherited autosomally rather than arising de novo, framing them as moderate-penetrance risk factors rather than sole drivers.

## Methods

**Design:** Three-stage study — (1) European-ancestry pan-sarcoma case-control discovery (141 established cancer predisposition genes), (2) independent European-ancestry Ewing sarcoma validation with ancestry-matched controls, and (3) parent-proband trio inheritance analysis [@Gillani2022].

**Discovery cohort:** 1,147 individuals with pediatric sarcoma (226 Ewing, 438 osteosarcoma, 180 rhabdomyosarcoma, 303 other) from four data sources aggregated via St. Jude Cloud.
Case-control analysis restricted to 879 European-ancestry cases vs. 10,548 matched cancer-free controls (from Autism Sequencing Consortium, Framingham Heart Study, Multi-Ethnic Study of Atherosclerosis, Lung Cohort, and NHLBI GO-ESP) [@Gillani2022].

**Validation cohort:** 433 additional Ewing sarcoma individuals (Gabriella Miller Kids First program / Project GENESIS); 356 European-ancestry cases vs. 10,680 matched controls.
Trio subset: 301 Ewing sarcoma probands with WGS from both parents (602 parents) [@Gillani2022].

**Sequencing:** Combination of WGS and WES; WGS converted to WES equivalents by restriction to coding target intervals. Mean target coverage 53.9x (discovery) and 27.3x (validation).

**Variant calling:** DeepVariant (v0.8.0) for germline variant calling; pathogenicity classified per ACMG guidelines using ClinVar + VEP consequence annotations. Only putative loss-of-function (frameshift, splice site, stop-gain) and pathogenic/likely pathogenic missense variants retained.

**Gene sets:** 141 established cancer predisposition genes (primary screen); 43 genes with established DDR roles (OMIM + Reactome) for targeted validation analysis [@Gillani2022].

**Population stratification:** PCA with 1000 Genomes super-population reference; random forest ancestry classifier; matching on first 10 principal components [@Gillani2022].

**Statistics:** Two-sided Fisher's exact test; exact2x2 package for OR and 95% CI; Benjamini-Hochberg FDR.
FDR < 0.05 threshold for discovery; single-hypothesis p < 0.05 for pre-specified validation tests [@Gillani2022].

## Key Findings

**Sarcoma subtype-specific enrichment patterns:**
- Across the pan-sarcoma cohort, nominal enrichment (p < 0.05) observed for *TP53*, *DICER1*, *FANCC*, and *PTPN11*; only *TP53* reached FDR < 0.05.
- **Osteosarcoma:** enrichment in *TP53*, *RB1*, *RECQL*, *MUTYH*, *RECQL4* (only *TP53* FDR-significant).
- **Rhabdomyosarcoma:** enrichment in *TP53*, *DICER1*, *BRCA2*, *SDHD*.
- **Ewing sarcoma (discovery):** No pathogenic germline *TP53* variants; sole gene with enrichment signal was *FANCC* (3/195 individuals, 1.5%; OR 12.6, 95% CI 3.0–43.2, p = 0.003, FDR = 0.40).

**FANCC validation:**
- In the independent Ewing sarcoma validation cohort (356 EUR cases): *FANCC* again enriched — 3/356 individuals (0.8%), OR 7.0, 95% CI 1.7–23.6, p = 0.014 (single-hypothesis test).
- Pooled across discovery + validation (6/551): OR 9.0, 95% CI 3.7–22.0, p < 0.0001.
- Sensitivity analysis varying assumed population frequency (0.10%–0.18%) confirmed robustness of enrichment signal (Figure 3B).

**Broader DDR gene signal in Ewing sarcoma (validation cohort, 43 DDR genes):**
- *CHEK2*: 7 individuals, OR 3.6, 95% CI 1.6–7.9, p = 0.005.
- *FANCA*: 4 individuals, OR 3.3, 95% CI 1.1–9.1, p = 0.042.
- *ERCC4* and *NBN*: marginal signals (OR ~4, p ~0.09).
- Five DDR genes (*FANCC*, *FANCA*, *CHEK2*, *ERCC4*, *NBN*) collectively contributed pathogenic variants in 18/356 Ewing sarcoma cases (5.1%) vs. 137/10,680 controls (1.3%).

**TP53 distinction:** Rate of pathogenic germline *TP53* variants in Ewing sarcoma (0%) was significantly lower than in all sarcomas combined (1.6%, p = 0.006) and osteosarcoma in particular (2.7%, p = 0.0005), consistent with the clinical observation that Ewing sarcoma is not seen frequently in Li-Fraumeni families [@Gillani2022].

**Inheritance analysis (trio cohort, n = 301) [@Gillani2022]:**
- 32/301 probands (10.6%) harbored pathogenic germline DDR variants.
- 32/32 (100%) of probands with pathogenic DDR variants had the identical variant identified in a carrier parent — confirming autosomal inheritance, not de novo origin.
- Only 19/269 probands without a DDR variant had at least one parent with a germline DDR variant (7.1%), consistent with population carrier frequency.
- No recurrent de novo pathogenic variants in other coding genes were found that would implicate a second-hit complementation model.

**Mechanism implication:** *FANCC* knockout is known to contribute to rearrangement signatures consistent with homologous recombination deficiency (HRD), providing a mechanistic link between germline DDR deficiency and the translocation-driven oncogenesis characteristic of Ewing sarcoma (EWSR1-ETS fusions).

## Relevance

**Connection to hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and (agnostic covariate-signature association):** This paper is relevant indirectly but importantly as biological context for the H_normgerm sub-topic group. The core hypothesis:0007 asks whether agnostic association of per-sample signature exposures against covariates (including germline-derived features) can recover known aetiologies and surface novel ones.

Gillani et al. provide several pieces of context:

1. **DDR germline variants as upstream determinants of somatic mutational processes.** The paper mechanistically links heterozygous *FANCC* loss-of-function to HRD-associated rearrangement signatures in Ewing sarcoma. This is a germline-to-somatic-signature causal chain of the type hypothesis:0007 aims to detect from the covariate-association direction. If cBioPortal Ewing sarcoma studies include germline carrier status (or proxies such as high HRD exposure scores or SBS3 enrichment), a hypothesis:0007 scan might recover this association directionally.

2. **Distinct sarcoma subtype signature of absence (no TP53).** The observation that Ewing sarcoma uniquely lacks germline *TP53* enrichment is itself a signature feature. In cBioPortal cross-study analyses, TP53 somatic mutation rates are markedly lower in Ewing sarcoma relative to osteosarcoma. This is a known positive-control data point for the "structured enrichment across cancer types" framing of the meta-analysis.

3. **Low-prevalence moderate-penetrance variants and statistical power.** The per-variant frequencies (0.8%–1.5% in cases) illustrate the power challenge when seeking germline-correlated somatic signature enrichment in small per-study cBioPortal cohorts. Aggregation across studies (as in the cross-study pipeline) is the appropriate strategy, but even aggregated Ewing sarcoma cohorts in cBioPortal are likely underpowered to detect these individual DDR gene signals without pre-stratification.

4. **FANCC / Fanconi pathway → HRD-like somatic signatures.** COSMIC SBS3 and the HRD signature landscape are known downstream consequences of Fanconi pathway deficiency. The hypothesis:0007 agnostic scan, if run on Ewing sarcoma data with HRD-related signatures (SBS3, ID6, CN signatures), might recover Fanconi pathway germline burden as an upstream covariate — a testable positive-control extension beyond the current H08a arms (UV, smoking, APOBEC3).

5. **Relevance to cross-study aggregation framework.** The distinct subtype-specific enrichment pattern (Ewing vs. osteosarcoma vs. rhabdomyosarcoma) mirrors the rationale for the cross-study pipeline's cancer-type stratification. Studies that collapse histologic subtypes would obscure the Ewing-specific DDR signal exactly as the underpowered pan-ancestry analysis in this paper did.

**Direct relevance to hypothesis:0007:** Peripheral (this paper is germline epidemiology, not signature decomposition). Indirect relevance is meaningful: it establishes the germline→DDR-pathway→HRD-signature causal axis as a documented phenomenon in Ewing sarcoma, which hypothesis:0007's agnostic scan could in principle recover from the somatic side if SBS3/HRD signatures are included.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Heterozygous pathogenic germline DDR variants | Germline predisposition covariate (H_normgerm sub-topic) | Potential upstream covariate for hypothesis:0007 agnostic scan |
| FANCC/Fanconi pathway → HRD-like rearrangements | SBS3 / HRD signature exposure | Germline-to-somatic causal chain detectable via signature assignment |
| European-ancestry case-control enrichment analysis | Cross-study ancestry-stratified aggregation | Same population-stratification concern motivates the pipeline's per-study approach |
| Pediatric sarcoma subtype stratification | Cancer-type stratification in gene x cancer matrix | Collapsing histologic subtypes masks DDR signal; same logic applies cross-study |
| 141-gene cancer predisposition panel | — | Not directly mapped; pipeline focuses on somatic not germline |
| Autosomal inheritance (not de novo) | — | Implies persistent carrier burden across affected families; not modelled in current pipeline |

## Limitations

- **European-ancestry bias:** Primary enrichment analysis restricted to European-ancestry individuals due to power constraints; pan-ancestry analysis was underpowered and limited by population frequency mismatches for rare variants.
- **Moderate effect sizes, low absolute frequencies:** FANCC enrichment involves 3–6 individuals across two cohorts; confidence intervals are wide (OR CIs spanning ~4-fold). Clinical actionability requires replication in larger, more diverse cohorts.
- **FDR not achieved in discovery for FANCC:** The discovery cohort FANCC signal had FDR = 0.40 (only nominally significant at p = 0.003); validation was essential and pre-specified, not post-hoc, but the multi-gene DDR analysis in the validation cohort carries its own multiple-testing burden.
- **No somatic data linked:** The study does not demonstrate that germline DDR carriers have elevated HRD/SBS3 somatic signatures in their tumors — the mechanistic link to rearrangement signatures is inferred from prior in vitro *FANCC* knockout work, not directly shown in this cohort.
- **Coding variants only:** WGS-to-WES conversion restricts the analysis to coding regions; non-coding regulatory variants in DDR genes are not captured.
- **No de novo complementation modelled:** Recurrent de novo variants impacting other genes were not found (only *TTN*, not biologically plausible), leaving the unexplained germline risk in the ~89% of cases without identified DDR variants uncharacterized.
- **CHEK2 and FANCA signals marginal:** The broader DDR gene enrichment (CHEK2, FANCA) is nominally significant but the pan-ancestry analysis was underpowered to confirm these signals; replication in independent ancestrally diverse cohorts is needed.

## Model / Tool Availability

No model or computational tool released. Sequencing data deposited in dbGaP (phs000804, phs000699, phs001228) and St. Jude Cloud (Pediatric Cancer Genome Project, St. Jude Lifetime, Genomes for Kids, Childhood Cancer Survivor Study). Code for deep-learning variant calling used DeepVariant v0.8.0 (publicly available).

## Follow-up

- **Somatic HRD signatures in FANCC carriers:** A follow-up study linking germline *FANCC* carrier status to tumor-level SBS3, ID6, or CN-HRD signatures in Ewing sarcoma would validate the germline→somatic chain and provide a direct hypothesis:0007-relevant positive control.
- **Larger, diverse cohorts:** Pan-ancestry replication with sufficient power (particularly African and admixed American populations) is needed to determine whether DDR enrichment generalizes beyond European ancestry.
- **CHEK2 in Ewing sarcoma:** *CHEK2* p.Ile200Thr (low-penetrance founder variant) was excluded and analyzed separately; its role in Ewing sarcoma susceptibility merits targeted analysis with sufficient power.
- **Structural variant germline burden:** As germline structural variant discovery improves, Fanconi pathway deletions and other non-coding DDR alterations may further increase the explained germline fraction.
- **Cascade genetic testing guidelines:** The autosomal inheritance finding (100% of DDR-variant probands inherited from a parent) directly motivates family-based cascade testing for Ewing sarcoma kindreds — a clinical translation question not addressed by the current study design.
