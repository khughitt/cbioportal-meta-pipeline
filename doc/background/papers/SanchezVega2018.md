---
id: "paper:SanchezVega2018"
type: "paper"
title: "Oncogenic Signaling Pathways in The Cancer Genome Atlas"
status: "read"
ontology_terms: []
datasets: ["tcga-pancanatlas"]
source_refs: ["cite:SanchezVega2018"]
related: ["paper:Bailey2018", "paper:Ciriello2013", "paper:Hoadley2018", "topic:pan-cancer-mutation-landscape"]
created: "2026-04-13"
updated: "2026-04-13"
---

# Oncogenic Signaling Pathways in The Cancer Genome Atlas

- **Authors:** Sanchez-Vega F, et al.
- **Year:** 2018
- **Journal:** Cell
- **PMID:** 29625050
- **DOI:** 10.1016/j.cell.2018.03.035
- **BibTeX key:** SanchezVega2018

## Key Contribution

A pan-cancer, pathway-centric reanalysis of the PanCanAtlas freeze (~9,125 samples, 33 cancer
types). Rather than ranking individual driver genes, the authors curate ten canonical oncogenic
signaling pathways and project each sample's mutations, copy-number alterations, fusions, and
(where relevant) epigenetic events onto pathway membership. The resulting per-(sample, pathway)
binary altered/not-altered matrix becomes the unit of downstream analysis, supporting cross-cancer
comparison, co-occurrence/mutual-exclusivity testing, and a pan-cancer view of therapeutic
actionability.

## Methods

### The ten curated pathways

Cell cycle, Hippo, Myc, Notch, Nrf2 (NFE2L2/KEAP1), PI3K/Akt, RTK-RAS, TGFβ, TP53, and
Wnt/β-catenin. Pathway templates were assembled by reviewing previous TCGA marker papers
(2008–2017) and the broader literature, then refined by pathway-specific working groups.

### Gene membership and "altered" gene definition

For each pathway, candidate member genes were retained only if there was evidence for recurrent
or known oncogenic alteration. Per-gene alteration calls combined:

- Statistical recurrence: MutSigCV for mutations, GISTIC 2.0 for copy-number.
- Functional impact: linear and 3D mutational hotspots.
- Curated knowledge: OncoKB annotations, expert review.
- Alteration types considered: somatic mutation, copy-number gain/loss, gene fusion, and DNA
  methylation where relevant. Each event is classified as activating or inactivating depending on
  the role of the gene (oncogene vs. tumor suppressor).

Genes lacking evidence for recurrent or previously known oncogenic alterations were dropped from
the templates.

### "Altered pathway" call per sample

A sample is called altered for a given pathway if **at least one** member gene carries a
recurrent or known driver alteration. This produces a sample x pathway binary matrix used for all
downstream summarization.

### Supplementary data of interest

- **Table S2 / S3:** Pathway templates and the per-gene list of alterations counted as
  oncogenic — i.e., the pathway membership table is published and downloadable, suitable for
  overlaying on external gene x cancer matrices.
- **Table S4:** Per-sample x per-gene binary "genomic alteration matrices" for all 9,125 samples.
- **Figure 3:** Per-(cancer type, pathway) alteration-rate heatmap, with the underlying matrix
  available in the supplement.

## Key Findings

### Pan-cancer pathway alteration frequencies

- **89%** of tumors carry a driver alteration in at least one of the ten pathways; the remaining
  ~11% have no detected alteration in this curated set.
- **RTK-RAS** is the most frequently altered pathway pan-cancer (median ~46% of samples; up to
  ~95% in melanoma).
- **PI3K** is the next most pervasive, reaching very high frequencies in selected subtypes
  (up to ~95% in some uterine/endometrial contexts).
- **TP53 and cell cycle** are broadly altered across carcinomas, often together.
- **Nrf2** is the least altered pan-cancer (~4%) but strongly enriched in squamous lineages.

### Per-cancer variability

Pathway frequencies vary dramatically by tissue: melanoma is RTK-RAS-dominated; serous ovarian and
basal breast are TP53/cell-cycle-dominated; endometrial and several others are PI3K-dominated;
squamous tumors are enriched for Nrf2 + PI3K. The published Figure 3 / supplementary matrix gives
the full per-(cancer, pathway) rate table.

### "Every cancer has a few altered pathways"

Cumulatively, almost every tumor type has multiple recurrently altered pathways, and most
individual tumors carry alterations in more than one of the ten pathways — supporting a
"few-pathways-per-tumor" model rather than single-pathway dominance. The 89% with ≥1 altered
pathway is the headline statistic; per-tumor multi-pathway burden varies by lineage.

### Co-occurrence and mutual exclusivity

A pathway-aware analysis identified **152 mutually exclusive** and **116 co-occurring** alteration
pairs. Notable examples:

- **Co-occurring:** TP53 mutation + Rb/cell-cycle alterations; PI3K + Nrf2 (lung, esophageal,
  head & neck).
- **Mutually exclusive:** within RTK-RAS (e.g., EGFR amplification vs. ERBB2 activation); within
  PI3K, cell-cycle, and TP53 modules.

### Actionability

- **57%** of tumors carry at least one alteration potentially targetable by an available drug.
- **30%** carry multiple targetable alterations, motivating combination strategies.
- Actionability is highly tissue-specific (e.g., uveal melanoma ~2.5% vs. melanoma very high).

## Relevance

Pathway-level pan-cancer view across TCGA — frames driver alterations in terms of 10 canonical
oncogenic signaling pathways (RTK-RAS, PI3K, Notch, etc.) rather than gene-by-gene. Natural
interpretation layer above our gene x cancer matrices: collapsing genes into pathway memberships
can reveal cross-cancer convergence that single-gene aggregation misses.

The published Table S2/S3 (pathway membership) and Table S4 (per-sample alteration matrix) are
directly reusable as an annotation overlay for our gene x cancer outputs and as a benchmark for
any pathway-collapsing summarization we implement.

## Limitations

- **Power for rare events:** the analysis is underpowered for tumor-type-specific alterations
  occurring at very low frequencies.
- **Tumor scope:** most hematologic malignancies are excluded (TCGA scope).
- **Sample state:** restricted to primary, untreated tumors; metastatic and post-treatment
  samples are not represented, limiting inferences about resistance and progression.
- **Curated templates:** the ten pathways are intentionally canonical and conservative; non-
  canonical drivers, epigenetic regulators, and immune/microenvironment signaling are
  underrepresented.
- **Binary "altered" abstraction:** loses dose, allele, and context information; co-occurrence
  statistics are sensitive to the curation choices upstream.

## Follow-up

- Overlay Table S2/S3 pathway memberships onto our per-gene x cancer matrices and recompute
  per-(cancer, pathway) frequencies; compare against the paper's Figure 3 matrix as a sanity
  check.
- Test whether pathway-collapsing changes our cancer-cancer similarity / clustering structure
  versus gene-level aggregation — does it surface cross-lineage convergence (e.g., squamous
  Nrf2+PI3K) that gene-level views miss?
- Re-examine co-occurrence / mutual-exclusivity at the pathway level on contemporary cohorts
  (e.g., GENIE, MSK-IMPACT) where metastatic and treated samples are represented.
- Extend the template set with non-canonical pathways (epigenetic regulators, immune signaling,
  metabolism) and compare coverage of "unexplained" 11% of tumors.
