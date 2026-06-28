---
type: topic
title: Lineage addiction, cell-of-origin, and the tissue/cell-type specificity of
  cancer drivers
status: active
created: '2026-06-07'
updated: '2026-06-28'
id: topic:lineage-addiction-and-cell-of-origin-driver-specificity
ontology_terms:
- lineage addiction
- lineage-survival oncogene
- cell of origin
- tissue specificity
- oncogene vs tumor suppressor
- tissue-specificity metric
source_refs:
- paper:Garraway2006
- paper:Shaffer2008
- paper:Haigis2019
- paper:Hoadley2018
- paper:Sack2018
- paper:MartinezJimenez2020
- paper:KryuchkovaMostacci2017
- paper:Pavinato2025
- paper:Kauko2025
- paper:dosSantos2023
related:
- question:0042-driver-normal-expression-tissue-cell-type-specificity
- question:0043-driver-cancer-type-breadth-distribution
- question:0045-pathway-grain-convergence-vs-gene-grain-divergence
- question:0047-hypermutation-confound-on-driver-tissue-specificity
- topic:cancer-driver-genes
- topic:oncofetal-developmental-reprogramming
- hypothesis:0012-neural-gene-enrichment-length-histology-artifact
- hypothesis:0003-gene-length-confounds-literature-attention
- discussion:0008-tissue-cell-type-specificity-of-cancer-drivers
---

# Lineage addiction, cell-of-origin, and the tissue/cell-type specificity of cancer drivers

## Scope

Background for the question: **to what extent are the drivers of a given cancer type genes with
strong tissue/cell-type-restricted *normal* expression, and is that more than chance?**
(`question:0042`). Collects the lineage-addiction literature, the cell-of-origin framework, the
oncogene/tumor-suppressor mode-of-action distinction, and the specificity-metric tooling.

## Two terminology distinctions this topic keeps sharp

- **Driver** (selection-defined, cancer-type-relative; `paper:MartinezJimenez2020` IntOGen) vs
  **oncogene / tumor suppressor** (mode of action — GoF activator vs LoF brake; COSMIC CGC
  `Role in Cancer`). Crossed axes, not synonyms.
- **Tissue** (bulk organ; GTEx) vs **cell type** (cell-of-origin lineage/state; single-cell —
  HPA / Tabula Sapiens). The relevant specificity is **cell-of-origin**, which bulk tissue only
  approximates (multiple myeloma → *plasma cell*, not "bone marrow").

## Two distinct routes to a "tissue-specific driver" (do not conflate)

1. **Lineage-factor drivers — the driver *is* a cell-type-restricted normal gene.**
   `paper:Garraway2006` (lineage dependency / lineage-survival oncogenes): cancers stay dependent
   on the master regulator of their normal lineage — MITF (melanocyte), AR (prostate), NKX2-1
   (lung), ESR1/GATA3 (luminal breast), SOX2 (squamous), PAX8 (Müllerian/thyroid).
   `paper:Shaffer2008` is the project's multiple-myeloma exemplar: **IRF4 addiction** — MM cells
   die without the plasma-cell master TF IRF4 *even though IRF4 is rarely mutated*. Lineage
   addiction is frequently an **expression/network dependency, not a recurrent somatic mutation** —
   the same expression-not-mutation caveat as `hypothesis:0012`.
2. **Context-dependent ubiquitous drivers — broadly expressed, tissue-specific only in *effect*.**
   `paper:Haigis2019` ("tissue-specificity is the rule, not the exception"): the same gene/mutation
   drives in some tissues and not others (APC→colon, KRAS, BRAF). `paper:Sack2018` gives
   experimental backing — proliferation-control responses to driver genes and aneuploidies are
   profoundly tissue-specific across cell contexts. Here the specificity lives in the
   regulatory/selective **context**, not the gene's expression breadth.

**Only route 1 predicts high normal-expression specificity of the driver gene.** Route-2 drivers
are expected low-Tau "false negatives" for an expression-restriction test — a feature to model,
not a refutation.

## The oncogene/TSG split (why a blanket claim is probably false)

- **Oncogenes**, especially lineage-survival ones, skew tissue-restricted (amplified/activated
  lineage programs).
- **Tumor suppressors / genome guardians** (TP53, RB1, PTEN, MMR, checkpoint) are broadly
  expressed, housekeeping-like — if anything *less* specific than a random gene. (Tissue-restricted
  TSGs exist — VHL/kidney, APC/colon, CDH1/lobular-breast+gastric, MEN1 — but are the minority.)
- Net: "cancer genes are more tissue-specific than chance" likely **washes out in aggregate**; the
  defensible claim is narrower — **cancer-type-*restricted* drivers, concentrated in the oncogene
  subset, are enriched for cell-type-restricted normal expression**, while pan-cancer drivers are
  broad.

## Cell-of-origin organizes the pan-cancer landscape

`paper:Hoadley2018` (TCGA PanCanAtlas, 10,000 tumors / 33 types): integrated multi-platform
clustering is dominated by **cell-of-origin**, not anatomical site — tumors regroup by lineage
(e.g. squamous across organs). Empirical backbone for using **cell-type-of-origin**, not bulk
tissue, as the specificity grain in `question:0042`.

## Measuring specificity (tooling)

`paper:KryuchkovaMostacci2017` benchmarks tissue-specificity metrics and recommends **Tau** as the
most robust, while flagging the key confound: **lowly/narrowly expressed genes score as more
specific by construction** — so any driver-specificity test must match background on **expression
level** as well as **gene length** (`hypothesis:0003`). Tau is computed on a chosen normal-expression
reference (bulk GTEx for tissue grain; HPA / Tabula Sapiens single-cell for cell-type grain) —
neither is vendored in the pipeline yet (the `question:0042-driver-normal-expression-tissue-cell-type-specificity`
prerequisite).

## Oncogenic competence, convergence, and loss-of-identity (2025 additions)

- **Oncogenic competence (`paper:Pavinato2025`).** The mechanistic core of route 2: a mutation
  transforms only in a **permissive cell state** set by the transcriptional/epigenetic program plus
  microenvironment (PIK3CA-H1047R is growth-promoting in esophagus, growth-suppressive in skin).
  Specificity can live in the **cell state**, not the driver gene's expression — so a low-Tau driver
  is not evidence against tissue-specific driving.
- **Convergence (`paper:Kauko2025`).** Diverse oncogenes **converge** on a shared growth program
  (MYC → ribosome biogenesis / translation; NOLC1 node). This **tempers** "each tissue has its own
  driver biology": the divergence is largely at the *entry point* (which oncogene the cell-of-origin
  makes accessible), not the downstream program — although **invasion/metastasis** hallmarks do not
  converge.
- **Loss of identity (`paper:dosSantos2023`).** Tumors **downregulate 20–51% of their
  tissue-of-origin-specific genes** and ectopically activate other-tissue genes (survival-associated,
  age-independent). This is the **design constraint** for
  `question:0042-driver-normal-expression-tissue-cell-type-specificity`: a driver's
  normal-expression specificity must be measured on a **normal** reference (GTEx/HPA/Tabula Sapiens),
  because tumor RNA no longer reflects the cell-of-origin baseline. (THCA, PRAD are noted
  exceptions.)

## What this project has vs needs

- **Have:** driver rosters + role/tissue labels — `data/cosmic_cgc.tsv` (CGC v100: Role in Cancer,
  Tissue Type, Tumour Types), `data/bailey2018_table_s1.tsv`, the annotated gene×cancer feathers.
- **Need:** a normal-expression reference (GTEx / HPA / Tabula Sapiens) + a Tau computation — a new
  ingest task; the pipeline has no expression modality today.

## Connections

- **Question:** `question:0042-driver-normal-expression-tissue-cell-type-specificity` (the enrichment
  test).
- **Related project work:** `topic:oncofetal-developmental-reprogramming` (lineage/developmental
  genes overlap the oncofetal axis);
  `hypothesis:0012-neural-gene-enrichment-length-histology-artifact` (neural-gene enrichment as a
  special case); `hypothesis:0003-gene-length-confounds-literature-attention` (length null);
  `question:0043-driver-cancer-type-breadth-distribution`,
  `question:0045-pathway-grain-convergence-vs-gene-grain-divergence`, and
  `question:0047-hypermutation-confound-on-driver-tissue-specificity` (adjacent driver-breadth
  checks); `discussion:0008-tissue-cell-type-specificity-of-cancer-drivers`; and
  `topic:cancer-driver-genes` (driver-definition background).
- **External / not-yet-in-library:** GTEx v8 expression atlas; Human Protein Atlas baseline paper;
  Tabula Sapiens cell-type atlas; MITF, NKX2-1, and SOX2 lineage-oncogene primaries.

## Summary

This topic note is currently a concise project-facing record; the existing sections above carry the substantive synthesis until a fuller rewrite is warranted.

## Key Concepts

The key concepts are defined in the existing prose above and in the linked project entities; this section is present to keep the topic aligned with the current Science topic template.

## Current State of Knowledge

The current project-facing state of knowledge is summarized in the existing prose above. No additional confidence upgrade is made by this structural section.

## Relevance to This Project

This topic is relevant through the linked questions, hypotheses, datasets, and source references in the frontmatter and in the note above.

## Key References

Key references include `paper:Garraway2006`, `paper:Shaffer2008`, `paper:Haigis2019`,
`paper:Hoadley2018`, `paper:Sack2018`, `paper:MartinezJimenez2020`,
`paper:KryuchkovaMostacci2017`, `paper:Pavinato2025`, `paper:Kauko2025`, and
`paper:dosSantos2023`.
