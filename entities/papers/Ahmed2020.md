---
type: paper
title: Gastrointestinal neuroendocrine tumors in 2020
status: active
created: '2026-06-06'
updated: '2026-06-06'
id: paper:Ahmed2020
ontology_terms:
- neuroendocrine tumor
- gastrointestinal cancer
- chromogranin A
- synaptophysin
- Ki-67 grading
- carcinoid syndrome
- somatostatin receptor
- neuroendocrine lineage
datasets: []
source_refs:
- cite:Ahmed2020
related:
- paper:Kulke2012
- paper:Tan2024
---

<!-- Author: Monjur Ahmed | 2020 | World J Gastrointest Oncol 12(8):791-807 -->
<!-- DOI recorded in BibTeX entry -->
<!-- BibTeX: Ahmed2020 -->
<!-- Source: PDF -->

# Gastrointestinal neuroendocrine tumors in 2020

- **Authors:** Monjur Ahmed
- **Year:** 2020
- **Journal:** World Journal of Gastrointestinal Oncology, Vol. 12, No. 8, pp. 791-807
- **DOI/URL:** recorded in BibTeX entry
- **BibTeX key:** Ahmed2020
- **Source:** PDF

## Key Contribution

This invited clinical review synthesizes the epidemiology, WHO 2017 classification, biology, site-specific clinical features, and management of gastrointestinal neuroendocrine tumors (GI-NETs) as of 2020. It provides a single-author, accessible reference for the full spectrum of GI-NET entities — gastric, small intestinal (duodenal, jejuno-ileal), appendiceal, colonic, and rectal — and their distinguishing biological characteristics. A key conceptual point is that NETs arise from neuroendocrine cells (cells with both neural and endocrine properties), constitutively express a stereotyped set of lineage markers (CgA, SYP, NSE/ENO2), and are classified as a distinct histological entity separate from adenocarcinomas and from tumors in which neural pathways regulate epithelial growth.

## Methods

Single-author narrative clinical review; no original cohort data, genomic analysis, or statistical methods. Evidence synthesized from published literature, SEER epidemiology data, WHO classification, and clinical society guidelines (ENETS, NANETS, NCCN). 123 references cited.

## Key Findings

1. **Classification and grading.** The 2017 WHO classification stratifies well-differentiated NETs into G1 (Ki-67 < 3%, mitotic index < 2/10 HPF), G2 (Ki-67 3-20%, mitotic index 2-20/10 HPF), and G3 (Ki-67 > 20%, mitotic index > 20/10 HPF). Poorly differentiated tumors are NEC grade 3 (small cell or large cell type, Ki-67 > 20%). Mixed tumors containing both a neuroendocrine and a non-neuroendocrine component (each ≥ 30%) are classified as MiNEN (mixed neuroendocrine neoplasm), replacing the older "mixed adenoneuroendocrine carcinoma" label.

2. **Lineage markers.** Neuroendocrine cells contain cytoplasmic dense core granules storing chromogranin A (CgA/CHGA), synaptophysin (SYP), and neuron-specific enolase (NSE/ENO2). CgA and SYP are required for diagnostic confirmation; Ki-67 and mitotic index provide prognostic grading. Serum CgA is the primary circulating biomarker used for disease monitoring.

3. **Epidemiology.** NETs are rare (0.5% of all malignancies, ~2% of GI tumors) but have increased 6.4-fold in age-adjusted incidence from 1973 to 2012 (1.09 to 6.98/100,000 persons). The SEER-18 highest GI-NET incidence is 3.56/100,000. GI-NETs account for 55% of all NETs; bronchopulmonary NETs account for 25%. Small intestinal NETs are most common (45% of GI-NETs), followed by rectum (20%), appendix (16%), colon (11%), and stomach (7%).

4. **Site-specific biology.** Gastric NETs arise mainly from enterochromaffin-like (ECL) cells and are classified into 4 types (I: ECL/hypergastrinemia/autoimmune CAG — most common 70-80%; II: ECL/hypergastrinemia/MEN1-ZES; III: sporadic/normogastrinemia; IV: non-ECL/rare/aggressive). SI-NETs arise from enterochromaffin cells in the intestinal crypts submucosa; > 2/3 occur in the terminal ileum. Appendiceal NETs are EC-cell serotonin-producing. Colonic NETs arise from Kulchitsky cells or enterochromaffin cells in the crypts of Lieberkühn.

5. **Functional syndromes.** Carcinoid syndrome (flushing in 94%, diarrhea in 80%, wheezing in 10-20%, carcinoid heart disease in 40-50%) occurs in 20-30% of jejuno-ileal NETs upon hepatic metastasis, driven by serotonin and tachykinins (substance P, neurokinin A) entering systemic circulation. Diagnosed by elevated 24-hour urinary 5-HIAA (sensitivity/specificity > 90%) and serum CgA.

6. **Genetic associations.** About 20% of NETs are associated with hereditary syndromes: multiple endocrine neoplasia type 1 (MEN1, chromosome 11q13 mutation in the menin suppressor gene) and neurofibromatosis type 1 (NF-1). Type II gastric NETs are specifically linked to MEN1-ZES; somatostatinomas are associated with MEN1 or NF-1 (up to 10% of NF-1 patients). No systematic somatic driver gene catalog is provided; the review does not cover genomic mutation frequencies.

7. **Treatment.** Somatostatin analogs (octreotide LAR, lanreotide) are first-line for carcinoid syndrome and antiproliferative control. Peptide receptor radionuclide therapy (PRRT; 177-Lutetium DOTA-lanreotide/octreotate), targeted agents (everolimus, sunitinib, bevacizumab, sorafenib), chemotherapy (streptozocin, 5-FU, capecitabine/temozolomide), hepatic embolization/TACE, and radiofrequency ablation are used for metastatic disease. Immunotherapy is noted as a future modality.

## Relevance

**This paper is relevant primarily as a boundary-setting reference for the cbioportal project's neuroendocrine-lineage artifact concern.**

NETs are tumors OF neuroendocrine cells — cells that are developmentally programmed to constitutively express a stereotyped neural/endocrine gene signature (CgA/CHGA, SYP, NSE/ENO2, somatostatin receptors, NCAM1/CD56, vesicular monoamine transporters). This is not neural regulation of epithelial cancer; it is a distinct histological lineage whose baseline transcriptional and proteomic identity is neuroendocrine.

**Neuroendocrine-lineage confound — NET studies in the cBioPortal cohort.** If any cBioPortal studies in the pipeline's `studies` list include NET histologies (e.g., pancreatic NETs, GI-NETs labeled under broad cancer-type codes), those samples will carry constitutive high expression of neuroendocrine genes. In the cross-study somatic mutation frequency tables this matters less directly (somatic mutations, not expression), but it matters for two specific artifact pathways:

- If the pipeline's hypothesis:0007 covariate-association scan uses expression covariates, NET samples will produce spurious strong associations between neuroendocrine lineage genes and "neural gene" mutation patterns.
- More directly relevant: if OncoTree codes for NET histologies are not correctly mapped and end up binned under a broad GI or "other" cancer type bucket, their constitutive expression and possibly elevated mutation rates in neuroendocrine-lineage genes (e.g., MEN1, DAXX, ATRX in pancreatic NETs [UNVERIFIED for GI-NETs]) could inflate apparent neural-gene signal in that cancer type stratum, mimicking a neural-gene lineage artifact.

**Recommendation.** NET histologies should be identified via OncoTree codes (e.g., GINET, PNET, CANED, NET\_STOMACH, NET\_SI, NET\_R, SCLC-adjacent NEC codes) and treated as a sensitivity stratum in any analysis where neural/neuroendocrine-lineage gene frequency is the outcome. Excluding or separately analyzing NET-labeled studies is a prerequisite before attributing elevated neuroendocrine gene mutation frequency to a "neural regulation" mechanism in non-NET cancers.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| CgA (CHGA), SYP, NSE/ENO2, NCAM1/CD56 | Neuroendocrine lineage marker genes | These genes appearing in top-mutated lists is a NET-contamination signal, not a neural-regulation signal |
| Ki-67 grading (G1/G2/G3) | Hypermutator/TMB stratification | High-grade NECs (G3) have higher proliferative index; TMB may differ from low-grade NETs |
| MEN1 (chromosome 11q13 menin) | Driver gene overlay (`annotate_drivers.py`) | MEN1 germline/somatic loss is a NET-specific driver; its presence in top-mutated genes may flag NET studies |
| OncoTree codes (GINET, PNET, etc.) | `oncotree_code` column in `convert_to_feather.py` | Use for NET histology flagging in sensitivity analysis |
| WHO 2017 NET vs NEC vs MiNEN | Cancer-type classification in cBioPortal studies | Mixed entities may be mislabeled or inconsistently coded across studies |
| Carcinoid syndrome / serotonin secretion | Not currently modeled | Functional NETs secrete bioactive amines; not relevant to somatic mutation frequency tables |
| 20% hereditary NET (MEN1, NF1) | CH-aware annotation / germline confound | Germline MEN1/NF1 in NET studies adds non-somatic signal |

## Limitations

- This is a clinical narrative review with no original genomic data; it does not report somatic mutation frequencies, driver gene catalogs, or TMB for GI-NETs. Molecular/genomic characterization of GI-NETs requires separate literature (e.g., TCGA pancreatic NET papers [UNVERIFIED for GI-NET somatic landscape]).
- The review does not distinguish between somatic drivers in NETs vs NEC vs MiNEN at the molecular level; the genomic heterogeneity across these subtypes is mentioned only in passing.
- Coverage of driver genes is limited to hereditary syndrome genes (MEN1, NF1); the somatic landscape (e.g., DAXX/ATRX alterations common in pancreatic NETs [UNVERIFIED for GI-NETs], CDK4/6, PTEN, TSC1/TSC2) is not discussed.
- Being a 2020 review, it predates more recent pan-NET genomic studies and updated ENETS/ESMO guidelines.

## Model / Tool Availability

No software or computational tools. Clinical review only. No datasets generated.

## Follow-up

- Identify which cBioPortal studies in the pipeline's `studies` config include NET histologies. Check `oncotree_code` values: GINET, PNET, NET\_STOMACH, NET\_SI, NET\_R, CANED, PANET, and NEC variants. Flag these studies in a `net_histology` sensitivity stratum.
- Before attributing elevated CHGA, SYP, ENO2, NCAM1, or MEN1 mutation/expression signal to a "neural regulation of cancer" mechanism, verify that the relevant cBioPortal studies are not predominantly or partially composed of NET samples.
- The MEN1 gene specifically is both a NET driver (germline/somatic loss in GI-NETs) and a CH-relevant gene. If MEN1 appears in top-mutated gene lists across GI cancer studies, investigate whether NET-labeled studies dominate that signal.
- Consider adding an `is_net_histology` boolean annotation flag to the per-sample metadata feather, populated from OncoTree code matching, to enable clean sensitivity analyses toggling NET samples in/out.
