---
id: "discussion:2026-06-07-tissue-cell-type-specificity-of-cancer-drivers"
type: "discussion"
title: "Are cancer-type-specific drivers genes with tissue/cell-type-restricted normal expression — more than chance?"
status: "active"
focus_type: "approach"
mode: "standard"
source_refs:
  - "paper:Garraway2006"
  - "paper:Shaffer2008"
  - "paper:Haigis2019"
  - "paper:Hoadley2018"
  - "paper:Sack2018"
  - "paper:MartinezJimenez2020"
  - "paper:KryuchkovaMostacci2017"
related:
  - "topic:lineage-addiction-and-cell-of-origin-driver-specificity"
  - "question:q042-driver-normal-expression-tissue-cell-type-specificity"
  - "topic:cancer-driver-genes"
  - "topic:oncofetal-developmental-reprogramming"
  - "hypothesis:h12-neural-gene-enrichment-length-histology-artifact"
  - "hypothesis:h03-gene-length-confounds-literature-attention"
  - "question:q035-label-free-neural-gene-definition"
created: "2026-06-07"
updated: "2026-06-07"
---

# Are cancer-type-specific drivers genes with tissue/cell-type-restricted normal expression?

## Focus

To what extent are the **drivers of a given cancer type** genes that are **normally expressed only
(or preferentially) in that tissue / cell type** in healthy individuals? Some drivers are
pan-cancer (TP53, KRAS, PIK3CA); others are cancer-type-restricted — and the question is whether
the restricted ones are **lineage genes of the cancer's cell-of-origin** (e.g. multiple myeloma's
plasma-cell differentiation program), and whether oncogenes/tumor suppressors are tissue-biased
**more than chance**.

## Two terminology distinctions (pinned down first, per the user's note)

- **"Driver" vs "oncogene + tumor suppressor."** *Driver* = selection-defined and
  **cancer-type-relative** (recurrence / dN-dS / clustering; `paper:MartinezJimenez2020` IntOGen);
  a gene can drive in one tissue and be neutral in another. *Oncogene / tumor suppressor* = **mode
  of action** (gain-of-function activator vs loss-of-function brake; COSMIC CGC `Role in Cancer`).
  Crossed axes, not synonyms — and they have **opposite expression-breadth priors** (below).
- **"Tissue" vs "cell type."** *Tissue* = bulk organ grain (GTEx). *Cell type* = the
  **cell-of-origin** lineage/state (single-cell; HPA / Tabula Sapiens). The relevant specificity is
  cell-of-origin: MM's drivers (IRF4, PRDM1, XBP1) are **plasma-cell**-specific, which bulk "bone
  marrow" would dilute. Bulk tissue is the approximation; cell type is the target
  (`paper:Hoadley2018`).

## Current Position

**Yes — this is a real, named phenomenon (lineage addiction), but it is class-dependent, and the
honest aggregate answer is probably "no."** Two distinct mechanisms both produce "tissue-specific
drivers," and only one is the user's hypothesis:

1. **Lineage-factor drivers — the driver *is* a cell-type-restricted normal gene.**
   `paper:Garraway2006`: MITF/melanoma, AR/prostate, NKX2-1/lung, ESR1/breast. `paper:Shaffer2008`:
   **IRF4 addiction** in MM — a lethal dependency on the plasma-cell master TF, *even without IRF4
   mutation*. These genuinely have high normal-expression specificity (and lineage addiction is
   often an **expression dependency, not a recurrent mutation** — the `h12` caveat again).
2. **Context-dependent ubiquitous drivers — broadly expressed, specific only in *effect*.**
   `paper:Haigis2019` ("the rule, not the exception"), `paper:Sack2018` (experimental): APC, KRAS,
   TP53 drive in a tissue-restricted way without being tissue-restricted in expression.

The **oncogene/TSG axis predicts the split**: lineage-survival drivers are overwhelmingly
**oncogenes**; the broad genome-guardian **tumor suppressors** (TP53, RB1, PTEN, MMR) are
housekeeping-like, possibly *less* specific than random. So a blanket "cancer genes are more
tissue-specific than chance" likely **washes out**; the defensible claim is narrower:
**cancer-type-restricted drivers — concentrated in the oncogene subset — are enriched for
cell-type-restricted normal expression, while pan-cancer drivers are broad.**

## Critical Analysis

- **The test must separate the two mechanisms.** Route-2 drivers (APC/KRAS) are **expected low-Tau
  "false negatives"** for an expression-restriction test; counting them as refutation would be a
  mistake. `q042` measures route-1 enrichment, with route-2 modeled, not ignored.
- **Confounds are the project's usual set.** Gene length (`h03` — length-match the background *and*
  note COSMIC's literature-attention bias); expression level (Tau is mechanically high for
  lowly/narrowly expressed genes — `paper:KryuchkovaMostacci2017` — so match on expression too);
  essentiality (housekeeping breadth drives the TSG end — signal for the OG/TSG contrast, confound
  for an undifferentiated test); ascertainment ("restricted" depends on which cohorts exist);
  bulk-tissue under-resolution (the MM/plasma-cell dilution).
- **Expression ≠ mutation (the `h12` parallel).** IRF4 is the cleanest warning: a gene can be the
  defining lineage dependency of a cancer and contribute *nothing* to a mutation-frequency table.
  A mutation-only pipeline sees the route-1 drivers that *are* recurrently mutated/amplified, and
  misses pure expression dependencies — state that boundary.
- **We can do the driver side now; the specificity side needs ingest.** COSMIC CGC role+tissue
  labels and Bailey rosters are on disk; a normal-expression reference (GTEx / HPA / Tabula
  Sapiens) + a Tau computation is a new prerequisite (no expression modality exists yet).

## Relationship to existing entities

- **`hypothesis:h12` is a special case** — "are neural genes top-mutated because they are
  tissue-restricted developmental genes?" `q035`/`q036` already build the
  specificity-of-a-gene-set + fetal-vs-adult machinery `q042` needs.
- **`topic:oncofetal-developmental-reprogramming`** — lineage/developmental genes overlap the
  oncofetal axis; restricted-oncogene lineage factors are often developmental TFs.
- **`hypothesis:h03`** — the length null and annotation-attention bias apply directly.
- **`topic:cancer-driver-genes` / `paper:MartinezJimenez2020`** — the driver-definition backbone.

## Prioritized Follow-Ups

| Priority | Item | Where |
|---|---|---|
| **P3** | `question:q042` — restricted-vs-pan-cancer driver Tau, OG vs TSG, length+expression-matched background, bulk + cell-type grains. Substrate (roster + role labels) on disk; gated on vendoring a normal-expression reference + Tau. | `question:q042`, `data/cosmic_cgc.tsv` + new expression ingest |
| **P3** | Promote a **hypothesis** ("restricted oncogenes > TSGs > matched background in cell-type Tau; pan-cancer drivers broad") once the specificity reference exists and a pilot shows the effect direction. | from `q042` |
| **P4** | Decide the expression reference + grain: GTEx (tissue) vs HPA / Tabula Sapiens (cell type). Cell-type grain is the rigorous version (MM/plasma-cell), bulk the cheap approximation. | ingest task |
| **note** | 3 of 7 source papers are **paywalled / abstract-based** (`paper:Garraway2006`, `paper:Haigis2019`, `paper:MartinezJimenez2020`) — summaries carry `[UNVERIFIED]`; deepen if PDFs are obtained. | `doc/papers/` |

## Synthesis

The user's intuition is right and has a name — **lineage addiction** (`paper:Garraway2006`;
IRF4/MM `paper:Shaffer2008`) — but the rigorous claim is **narrower** than "cancer drivers are
tissue-specific." Two mechanisms produce tissue-specific drivers, and only **lineage-factor
drivers** (mostly **oncogenes**) are genes with restricted *normal expression*; **context-dependent
drivers** (`paper:Haigis2019`/`paper:Sack2018`) and **broad tumor suppressors** are not. So the
defensible, testable statement is: *cancer-type-restricted drivers — concentrated in the oncogene
subset — are enriched for cell-type-of-origin-restricted normal expression beyond length/
expression-matched chance, measured at single-cell grain* (`question:q042`). Our pipeline can build
the driver side today; the specificity side needs a normal-expression reference, and the IRF4 case
reminds us a mutation-only readout will miss the pure-expression dependencies entirely.
