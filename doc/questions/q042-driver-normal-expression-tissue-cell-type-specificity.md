---
id: "question:q042-driver-normal-expression-tissue-cell-type-specificity"
type: "question"
title: "Are cancer-type-restricted drivers enriched for cell-type-restricted normal expression — more than length/expression-matched chance — and do oncogenes differ from tumor suppressors?"
status: "active"
ontology_terms:
  - lineage addiction
  - cell of origin
  - tissue specificity
  - driver gene
  - oncogene
  - tumor suppressor
datasets:
  - "data/cosmic_cgc.tsv (COSMIC Cancer Gene Census v100 — Role in Cancer, Tissue Type, Tumour Types(Somatic))"
  - "data/bailey2018_table_s1.tsv (PanCanAtlas 299-driver consensus + per-cancer rosters)"
  - "gene_cancer_study_annotated.feather (per-cancer driver overlay)"
  - "IntOGen / Martinez-Jimenez 2020 per-cancer-type driver compendium (external)"
  - "GTEx tissue expression (external — bulk-tissue Tau)"
  - "Human Protein Atlas / Tabula Sapiens single-cell (external — cell-type Tau)"
  - "data/uniprotkb_hsapiens_protein_lengths.tsv.gz (length control)"
  - "data/gene_replication_timing.feather (mutation-rate confound control)"
source_refs:
  - "paper:KryuchkovaMostacci2017"
  - "paper:Garraway2006"
  - "paper:Shaffer2008"
  - "paper:Haigis2019"
  - "paper:Sack2018"
  - "paper:MartinezJimenez2020"
  - "paper:Hoadley2018"
  - "paper:Pavinato2025"
  - "paper:dosSantos2023"
related:
  - "topic:lineage-addiction-and-cell-of-origin-driver-specificity"
  - "topic:cancer-driver-genes"
  - "topic:oncofetal-developmental-reprogramming"
  - "hypothesis:h12-neural-gene-enrichment-length-histology-artifact"
  - "hypothesis:h03-gene-length-confounds-literature-attention"
  - "question:q035-label-free-neural-gene-definition"
  - "question:q036-oncofetal-fetal-vs-adult-neural-expression"
  - "discussion:2026-06-07-tissue-cell-type-specificity-of-cancer-drivers"
created: "2026-06-07"
updated: "2026-06-07"
---

# Are cancer-type-restricted drivers enriched for cell-type-restricted normal expression, beyond chance — and do oncogenes differ from tumor suppressors?

## Summary

Some drivers are **pan-cancer** (TP53, PIK3CA, KRAS); others are **restricted** to one cancer
type or a few. The hypothesis: **cancer-type-restricted drivers are enriched for genes whose
*normal* expression is confined to that cancer's cell-of-origin** — i.e. lineage genes
(`paper:Garraway2006`'s lineage-survival oncogenes: MITF/melanoma, AR/prostate, NKX2-1/lung; and,
as the project's exemplar, IRF4 in multiple myeloma — a plasma-cell master TF, `paper:Shaffer2008`)
— whereas pan-cancer drivers are broadly expressed. The sharp, testable version separates two
sub-questions:

1. Do **restricted** drivers have higher normal-expression **tissue/cell-type specificity** (Tau,
   `paper:KryuchkovaMostacci2017`) than **pan-cancer** drivers, and than a **length- and
   expression-matched random background**?
2. Does each restricted driver's **peak-expression cell type/tissue match the cancer type it
   drives** (lineage concordance)?
3. Do **oncogenes** carry more tissue-bias than **tumor suppressors**? (Prediction: yes —
   lineage-survival drivers are overwhelmingly oncogenes; broad genome-guardian TSGs — TP53, RB1,
   PTEN, MMR — are housekeeping-like and may be *less* specific than random.)

## Terminology this question depends on (kept distinct)

- **Driver** = under positive selection in a cancer type (recurrence / dN-dS / clustering;
  `paper:MartinezJimenez2020` IntOGen). Cancer-type-relative; "restricted vs pan-cancer" is the
  key variable here. **Oncogene / tumor suppressor** = mode of action (GoF activator vs LoF brake;
  COSMIC CGC `Role in Cancer`). The two axes are crossed, not synonymous.
- **Tissue** = bulk organ grain (GTEx). **Cell type** = cell-of-origin lineage/state (single-cell;
  HPA / Tabula Sapiens). The rigorous test uses **cell-type** grain — multiple myeloma's drivers
  are *plasma-cell*-specific, which bulk "bone marrow" would dilute; bulk tissue is the
  approximation, cell-of-origin the target (`paper:Hoadley2018`).

## Why It Matters

- Turns the user's question into a falsifiable enrichment test rather than a vague "more than
  chance," and forces the OG-vs-TSG split that makes a *blanket* "cancer genes are tissue-specific"
  claim probably **false in aggregate** but **true for restricted oncogenes**.
- It is the **same machinery** as the project's label-free neural-gene work (`q035` definition,
  `q036` fetal-vs-adult expression): specificity-of-a-gene-set, length-controlled. `h12` is a
  special case ("are neural genes top-mutated because they are tissue-restricted developmental
  genes?"). A clean method here generalizes to that.

## What we can compute (substrate already on disk)

- **Driver axis (substrate on disk, but needs an explicit roster-counting step — not the
  annotated feathers).** Mode-of-action labels come from `data/cosmic_cgc.tsv` (`Role in Cancer`
  oncogene/TSG/fusion, `Tissue Type`). **The "restricted vs pan-cancer" count must NOT be read off
  the annotated gene×cancer feathers:** `annotate_lib.py` ORs Bailey **PANCAN** drivers into the
  `bailey2018_driver` flag for *every* cancer-type row (documented in
  `doc/guides/canonical-outputs.md`), so a gene's apparent per-cancer breadth there is
  contaminated by pan-cancer broadcast. The restriction variable requires a dedicated counting
  step over **raw per-cancer rosters** — `data/bailey2018_table_s1.tsv` with the `PANCAN` rows
  **excluded or separately encoded**, and/or the IntOGen per-tumor-type compendium
  (`paper:MartinezJimenez2020`: 360/568 driver genes (63%) restricted to 1–2 tumor types; only 12
  cancer-wide drivers — TP53, KRAS, PIK3CA, PTEN, KMT2D, KMT2C, LRP1B, ARID1A, RB1, FAT4, NF1,
  CDKN2A). Cross-check the two roster sources; do not let PANCAN-broadcast semantics define
  "pan-cancer."
- **Specificity axis (external prerequisite — not yet vendored):** a normal-expression reference
  + a Tau computation. **Tissue grain:** GTEx. **Cell-type grain:** HPA / Tabula Sapiens. This is
  a new ingest task (no expression modality exists in the pipeline today).
- **Test:** Tau(restricted drivers) vs Tau(pan-cancer drivers) vs Tau(matched background);
  lineage-concordance rate; OG vs TSG Tau contrast.

## Confounds that decide interpretability

- **Gene length (`h03`)** — long genes are over-called as drivers *and* skew the candidate set;
  background **must be length-matched**, and the annotation set (COSMIC) carries the same
  literature-attention bias h03 describes.
- **Expression level / breadth** — Tau is mechanically inflated for **lowly/narrowly expressed**
  genes (`paper:KryuchkovaMostacci2017`); match background on mean expression, not just length.
- **Essentiality** — broadly-essential guardians (TSGs) are housekeeping-like; this is *signal*
  for the OG/TSG contrast but a *confound* for an undifferentiated "all drivers" test.
- **Ascertainment** — "cancer-type-restricted" partly reflects *which cohorts exist*; restriction
  measured on our cBioPortal/GENIE composition differs from IntOGen's. Cross-check driver rosters.
- **Bulk under-resolution** — bulk-tissue Tau will miss cell-type-restricted drivers in
  heterogeneous tissues (the MM/plasma-cell case); report bulk and single-cell grains separately.
- **Context-dependent ≠ expression-restricted** — `paper:Haigis2019` / `paper:Sack2018`: many
  drivers are tissue-*specific in effect* while broadly *expressed* (APC, KRAS). These are
  **expected low-Tau "false negatives"** for an expression-restriction test and must not be read
  as refuting lineage addiction — they are a *different* route to tissue-specific driving.
  `paper:Pavinato2025` (oncogenic competence) is the mechanism: the same mutation transforms only
  in a permissive cell *state* (e.g. PIK3CA-H1047R growth-promoting in esophagus, growth-suppressive
  in skin) — so route-2 specificity lives in the cell state, not the driver gene's expression.
- **Use NORMAL expression, never tumor expression (design-critical).** `paper:dosSantos2023` shows
  tumors **lose 20.5–51.3% of their tissue-of-origin-specific genes** and gain ectopic other-tissue
  expression ("loss of identity"). Computing a driver's specificity from tumor RNA would therefore
  measure the disease, not the cell-of-origin baseline. Tau must be computed on a **normal**
  reference (GTEx / HPA / Tabula Sapiens). (THCA and PRAD are noted exceptions to the loss-of-
  identity pattern — watch them if they surface as outliers.)

## Predictions

- Restricted drivers > pan-cancer drivers in cell-type Tau, surviving length+expression matching —
  but the effect concentrated in the **oncogene** subset; **TSGs near or below background**.
- High lineage-concordance for the restricted-oncogene subset (MITF↔melanocyte, AR↔prostate
  luminal, IRF4/PRDM1↔plasma cell, NKX2-1↔lung epithelium).
- Cell-type grain (single-cell) shows the effect more strongly than bulk-tissue grain.

## Stop / null conditions

- The null must be evaluated **stratified by mode of action (OG/TSG) and route**, not on the
  pooled set. An *unstratified* restricted-vs-pan-cancer Tau difference vanishing after
  length+expression matching does **not** by itself imply a detection/annotation artifact — it is
  equally consistent with the restricted-driver set being **dominated by route-2 context-dependent
  drivers** (broadly expressed, low-Tau by design; `paper:Haigis2019`/`paper:Sack2018`). The
  artifact reading is warranted only if the effect also vanishes **within the restricted-oncogene
  subset** (where lineage-factor route-1 drivers concentrate). So: null = "no Tau enrichment in the
  restricted *oncogene* subset vs matched background," not "no difference in the pooled set."
- No expression reference can be vendored at acceptable cost → question blocked at the ingest
  prerequisite (document, do not fake with GO labels).

## Connections to Project

- **Topic / discussion:** `topic:lineage-addiction-and-cell-of-origin-driver-specificity`,
  `discussion:2026-06-07-tissue-cell-type-specificity-of-cancer-drivers`.
- **Sibling questions:** `q035`/`q036` (same specificity machinery on the neural-gene set); `h12`
  as the special case; `h03` as the length null.
- **Priority:** P3 — substrate (driver roster + role labels) is on disk; gated on vendoring a
  normal-expression reference and a Tau computation. A hypothesis (formal "OG > TSG > background"
  enrichment claim) can be promoted from this question once the specificity reference exists.
