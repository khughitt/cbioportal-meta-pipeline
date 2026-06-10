---
type: paper
title: A compendium of mutational cancer driver genes
status: active
created: '2026-04-21'
updated: '2026-06-07'
id: paper:MartinezJimenez2020
ontology_terms: []
source_refs:
- paper:MartinezJimenez2020
related:
- paper:Bailey2018
- topic:cross-study-meta-analysis-cancer-genomics
- topic:cancer-driver-genes
- topic:lineage-addiction-and-cell-of-origin-driver-specificity
- question:0042-driver-normal-expression-tissue-cell-type-specificity
- discussion:0008-tissue-cell-type-specificity-of-cancer-drivers
---

# A compendium of mutational cancer driver genes

- **Authors:** Martinez-Jimenez F, Muinos F, Sentis I, Deu-Pons J, Reyes-Salazar I,
  Arnedo-Pac C, Mularoni L, Pich O, Bonet J, Kranas H, Gonzalez-Perez A\*, Lopez-Bigas N\*
  (Lopez-Bigas lab, IRB Barcelona)
- **Year:** 2020
- **Journal:** Nature Reviews Cancer 20(10):555-572
- **DOI:** 10.1038/s41568-020-0290-x
- **PMID:** 32778778
- **BibTeX key:** MartinezJimenez2020
- **Source:** PDF (`papers/pdfs/2020_Martinez-Jimenez_A-compendium-of-mutational-cancer-driver-genes.pdf`)

## Key Contribution

Presents the IntOGen pipeline and a systematic snapshot of the compendium of mutational cancer
driver genes, derived from applying seven complementary selection-signal methods to 28,076
tumors across 221 cohorts of 66 cancer types. The pipeline identifies 568 driver genes and
characterizes each gene's mode of action (activating/oncogene vs. loss-of-function/tumor
suppressor) and cancer-type specificity, providing the most comprehensive per-tumor-type driver
roster available from positive-selection evidence alone.

## Methods

### Dataset

- 28,076 tumor samples, 221 cohorts, 66 cancer types.
- Sources: TCGA (10,010 samples / 32 cohorts), ICGC (3,988 / 42), Hartwig Medical Foundation
  (3,742 / 30), PCAWG (2,554 / 31), cBioPortal (3,570 / 34), Pediatric cBioPortal (1,087 / 26),
  St. Jude (622 / 16), TARGET (246 / 2), literature cohorts (2,257 / 8).
- 157 cohorts are primary tumors; 33 are metastatic or relapse (4,340 samples). Pediatric
  malignancies: 2,799 samples in 48 cohorts (25 cancer types).
- Cohort = a set of samples of the same cancer type processed with a uniform sequencing and
  calling pipeline. Each cohort is analyzed independently because re-calling across heterogeneous
  pipelines is not yet feasible at this scale.

### IntOGen pipeline — three stages

**Stage 1 — Pre-processing / QC.** Each cohort is filtered for: duplicate samples from the same
tumor; samples with an abnormal missense-to-synonymous mutation ratio; hypermutator samples.
Mutations overlapping a Panel of Normals (Hartwig) are removed.

**Stage 2 — Seven parallel driver-identification methods.** Each method exploits a different
signal of positive selection:

| Method | Signal exploited |
|---|---|
| dNdScv | Negative-binomial dN/dS with regional (chromatin/expression) covariates |
| OncodriveFML | Functional-impact score bias across observed mutations |
| cBaSE | Bayesian inference of non-synonymous counts given synonymous counts |
| OncodriveCLUSTL | Positional recurrence along the linear DNA/protein sequence |
| HotMAPS (re-implemented with trinucleotide context) | Positional recurrence in 3D protein conformation |
| smRegions | Enrichment of mutations in annotated Pfam functional domains |
| Mutpanning | Non-synonymous recurrence combined with deviation from the neutral trinucleotide mutational context |

**Stage 3 — Weighted-vote combination and post-processing.**

*Combination:* The seven per-cohort p-value lists are combined via a weighted Stouffer's Z-score.
Weights are assigned dynamically per cohort using Schulze's voting method: weights are optimized
so that the enrichment of known Cancer Gene Census (CGC) genes at the top of the consensus
ranking is maximized (CGC-Score objective). Each method's weight is constrained to ≤ 0.30 of the
total credibility simplex, preventing any single method from dominating. Final q-values are
computed via Benjamini-Hochberg FDR correction on combined p-values. Genes are stratified
into Tier 1 (q < 0.05, high-confidence), Tier 2 (CGC genes with CGC-specific q < 0.25 not in
Tier 1), and Tier 3 (remaining ranked candidates meeting rank cutoff).

*Post-processing filters:* Candidate drivers must pass multiple automatic filters before entering the
compendium: (1) non-expressed genes removed using TCGA expression data (genes with ≥ 80%
of samples at log2 RSEM ≤ 0 are excluded for matched tumor types); (2) genes highly tolerant to
SNPs excluded using gnomAD oe scores (oe_mys > 1.5 or oe_lof > 1.5 or oe_syn > 1.5 with
>1 mutation/sample); (3) mutations overlapping Panel of Normals germline variants (>5 germline
hits) are removed; (4) known false-positive gene categories blacklisted (long genes: TTN, OBSCN,
RYR2, etc.; olfactory receptors from HORDE; non-Tier1 CGC genes lacking CancerMine
literature support); (5) non-CGC genes with >3 mutations in a single sample are discarded (local
hypermutation or contamination); (6) genes where >50% of mutations in AID-active lymphoid
cancer types (AML, NHL, CLL, etc.) match COSMIC Signature 9 are excluded.

Benchmark (32 TCGA WES cohorts): the weighted combination achieves higher CGC-Score than
any individual method in 23/32 (71%) cohorts and higher than all other combination strategies
tested in 30/32 (93%) cohorts, while being the least enriched in known non-cancer genes in
14/43 cohorts and never the most enriched.

### Mode-of-action (MoA) classification

MoA is inferred per gene from consequence-type-specific dN/dS ratios estimated by dNdScv
across pan-cancer TCGA cohorts.

- **Act (activating / oncogene):** omega_missense - omega_nonsense > epsilon (epsilon = 0.1)
  — excess of missense over nonsense mutations indicates gain-of-function.
- **LoF (loss-of-function / tumor suppressor):** omega_nonsense - omega_missense > epsilon
  — excess of nonsense (and typically splice-affecting) mutations indicates inactivation.
- **Amb (ambiguous):** |omega_missense - omega_nonsense| < epsilon, or omega_missense < 1.

The quantitative MoA inference is reconciled with prior knowledge from the Cancer Genome
Interpreter (CGI): when inference and prior knowledge agree, the consensus label is used; when
the gene is absent from CGI, the inferred label is used; when they conflict, the CGI prior is used.
The excess rate per consequence type is defined as (omega_c - 1) / omega_c.

**Mutational cluster morphology as a MoA proxy:** Oncogene clusters in the linear sequence are
characteristically narrow and concentrate a high fraction of the gene's mutations (e.g., KRAS
codons 12-13: 5 nt, 85% of mutations in a colorectal cohort of 496; IDH1 codon 132: 100% of
mutations in an AML cohort of 257), reflecting the limited number of gain-of-function positions.
Tumor suppressor clusters are wider and accumulate a smaller fraction of total mutations (e.g.,
TP53: 28 nt, 28% of mutations in pilocytic astrocytoma; SPOP: 44 nt, 83% in prostate
adenocarcinoma).

## Key Findings

### Compendium size and CGC validation

- **568 mutational driver genes** identified across 66 cancer types from 28,076 tumors.
- ~75% of the 568 genes are already annotated in the CGC (v87), validating the pipeline.
- 152 genes in the compendium are **potential new drivers** (not annotated in the CGC at time
  of publication). Five are discussed in detail with independent supporting evidence: RASA1
  (lung/HNSCC, LoF, RAS/MAPK regulator), KDM3B (pilocytic astrocytoma/medulloblastoma),
  FOXA2 (uterine carcinoma), KLF5 (cervical/bladder/lung squamous), BRD7 (melanoma/liver).
- >80% of **driver gene–tumor type associations** in the compendium are not annotated in the
  CGC, revealing that the per-tumor-type breadth of known driver genes is far wider than
  previously documented. Example: KMT2C shows signals in 31 tumor types but is annotated
  in CGC only for medulloblastoma.

### Tissue-specificity of drivers

- **360 out of 568 genes (63%)** act as drivers in only **one or two tumor types** — they are
  cancer-type-restricted.
- **12 genes** are **cancer-wide drivers** acting as drivers in **more than 20 malignancies**:
  TP53, KRAS, PIK3CA, PTEN, KMT2D, KMT2C, LRP1B, ARID1A, RB1, FAT4, NF1, and
  CDKN2A (from Fig. 3d and accompanying barplot). Maximum prevalences for cancer-wide
  drivers range from 0.92 (KRAS) to 0.25 (others).
- **Cancer-specific highly prevalent drivers** are mutated at high frequency in one or very few
  cancer types: GNAQ (50% of uveal melanoma), GNA11 (uveal melanoma), GTF2I (47% of
  thymomas), CCND3 (47% of Burkitt lymphoma), MYC (60% of Burkitt lymphoma), PTCH1
  (skin basal cell carcinoma, max prevalence 0.56).
- The same driver gene can have different tumorigenic mechanisms in different cancer types
  (EGFR: extracellular domain clusters in glioblastoma vs. kinase domain clusters in lung
  adenocarcinoma).

### Recurrently affected protein domains

- The **P53 domain** is significantly enriched for somatic mutations across **42 cancer types**
  (driven entirely by TP53) — more than any other domain.
- The **tyrosine kinase domain** of 13 different genes is enriched across 24 tumor types; BRAF
  has the widest reach (14 tumor types).
- RAS, cadherin, and C2H2 zinc finger domains each show enrichment across 13 cancer types.

### LRP1B note

The compendium flags LRP1B as a recurrent cancer-wide hit but notes that it is a long gene
potentially susceptible to calling artifacts; the paper acknowledges the discussion is unsettled.

## Relevance

This paper provides the precise operational definition of "cancer driver" used by q042 and the
associated discussion on tissue/cell-type specificity of drivers. Key points:

1. **Selection-based, per-tumor-type definition.** A gene is a driver in a given cancer type if its
   somatic mutation pattern deviates from the neutral background — as detected by at least one
   of seven positive-selection signals — in a cohort of that cancer type. This is distinct from the
   oncogene/TSG mode-of-action axis (Act/LoF/Amb), which describes *how* a gene drives cancer
   once identified.

2. **Per-cancer-type rosters vs. pan-cancer broadcast.** The compendium maintains per-tumor-
   type driver lists, not a single pan-cancer flag. This is a cleaner source for q042's "restricted vs.
   shared" substrate than the Bailey2018 annotation in our pipeline feathers, which broadcasts
   pan-cancer CGC membership to all cancer types.

3. **The 360/12 split is the empirical substrate for q042.** 360 genes that drive one or two tumor
   types represent the tissue-restricted substrate; 12 cancer-wide genes are the shared core.
   The question of *why* most drivers are tissue-specific (lineage addiction, cell-of-origin
   expression context, tissue-specific mutational processes) is precisely what q042 asks and what
   the linked discussion (2026-06-07) explores.

4. **Mode-of-action classification.** The Act/LoF/Amb labels — derived from the dN/dS
   missense-vs-nonsense excess with CGI prior reconciliation — are a principled quantitative
   counterpart to the CGC's manually curated oncogene/TSG designations. They are available
   per gene at intogen.org.

5. **cBioPortal as a primary data source.** The compendium itself draws on 3,570 samples from
   34 cBioPortal cohorts (and 1,087 pediatric from Pediatric cBioPortal), directly connecting this
   paper's methods to our pipeline's input data.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Compendium driver gene (per tumor type) | `bailey2018_driver` flag in feathers | Bailey2018 is a different (pan-cancer PANCAN) roster; IntOGen compendium is the cleaner per-type source |
| Act / LoF / Amb mode of action | oncogene / tumor suppressor classification | IntOGen MoA is quantitative (dN/dS-based + CGI prior); CGC is manual curation |
| Cancer-wide driver (>20 types) | Pan-cancer driver | 12 genes: TP53, KRAS, PIK3CA, PTEN, KMT2D, KMT2C, LRP1B, ARID1A, RB1, FAT4, NF1, CDKN2A |
| Cancer-type-restricted driver (1-2 types) | Lineage-specific driver | 360/568 genes (63%) |
| Cohort | Study (per cancer type) | IntOGen requires uniform sequencing/calling within a cohort |
| Hypermutator filtering (pre-processing) | `is_hypermutator` flag in t081/t092-t099 | Both approaches exclude hypermutators before driver calling |
| Signature 9 / AID-driven mutations | Clonal hematopoiesis / mutational signature contamination | IntOGen post-processing removes >50% Sig9 mutations in lymphoid types |

## Limitations

- **Scope:** Point mutations and short indels only. CNV drivers (amplifications, deletions),
  translocations, epigenetic silencing, and non-coding driver elements are explicitly excluded.
- **Cohort-level heterogeneity:** Mutations are not re-called uniformly; technical variability across
  pipelines introduces noise that per-cohort analysis only partially mitigates.
- **Snapshot:** The 568-gene compendium reflects the data available at time of writing (~2020);
  genes mutated at <10% frequency in current cohorts are likely underrepresented.
- **CGC as ground truth:** The paper uses CGC v87 for weight calibration and validation; CGC
  is incomplete and contains some false positives, acknowledged by the authors.
- **LRP1B caution:** Flagged as a potentially spurious cancer-wide hit due to long-gene
  susceptibility to calling artifacts.
- **MoA ambiguity:** Some drivers cannot be cleanly classified Act or LoF (labeled Amb); MoA
  can also differ between tumor types for the same gene.
- **No germline / non-somatic drivers:** Covers somatic point mutations only.

## Model / Tool Availability

- **IntOGen platform:** https://www.intogen.org — web interface for browsing driver gene
  compendium, downloadable data (driver gene lists, mutational features), and the pipeline for
  local installation.
- **Pipeline:** Open-source, hosted at intogen.org; designed to scale to hundreds of thousands
  of samples. Updated snapshots released as new data accumulate.
- **Compendium download:** Driver genes per tumor type, mutational features (linear clusters,
  3D clusters, preferentially mutated domains, excess rates, MoA labels) are all downloadable.

## Follow-up

- Compare the IntOGen per-cancer-type driver rosters directly against our pipeline's
  `bailey2018_driver` overlay to quantify how many genes are Bailey-only (pan-cancer broadcast)
  vs. IntOGen-confirmed per type — addresses q042's tissue-specificity question concretely.
- The 152 potentially new drivers (non-CGC) are a candidate list for hypothesis generation about
  understudied cancer genes; cross-reference with expression data in our feathers.
- For the lineage-specificity discussion: the 360-gene restricted set + the 12 cancer-wide genes
  are the empirical starting point; next step is to ask whether restricted drivers show higher
  tissue-specific expression in matched normal tissue (q042).
- Consider downloading IntOGen compendium and joining to our `gene_cancer_study_ratio_annotated.feather`
  on (gene, cancer_type) to add `intogen_driver` and `intogen_moa` columns alongside
  `bailey2018_driver`.
