---
type: question
title: "Does the cancer-type specificity of drivers seen at the gene level collapse\
  \ at pathway grain \u2014 i.e. do cancer types converge on shared pathways even\
  \ when they diverge on which gene is hit?"
status: active
created: '2026-06-07'
updated: '2026-06-07'
id: question:0045-pathway-grain-convergence-vs-gene-grain-divergence
ontology_terms:
- convergence
- pathway-level analysis
- mutual exclusivity
- driver gene
- cell of origin
datasets:
- gene_cancer_study.feather (per-gene per-cancer mutation counts, aggregable to pathways)
- gene_cancer_pooled.feather (t077 pooled per-(cancer, gene))
- data/cosmic_cgc.tsv (Role in Cancer for OG/TSG within-pathway redundancy)
- "gene->pathway map (external \u2014 Reactome / KEGG / Sanchez-Vega 10 canonical\
  \ pathways; not yet vendored)"
source_refs:
- paper:Kauko2025
- paper:MartinezJimenez2020
related:
- question:0042-driver-normal-expression-tissue-cell-type-specificity
- question:0043-driver-cancer-type-breadth-distribution
- topic:co-occurrence-and-mutual-exclusivity
- topic:lineage-addiction-and-cell-of-origin-driver-specificity
- theme:0003-temporal-structure-of-carcinogenesis-order-count-and-timing-of-the
- hypothesis:0004-mhn-pathway-ordering
---

# Does the cancer-type specificity of drivers seen at the gene level collapse at pathway grain?

## Summary

`question:0042-driver-normal-expression-tissue-cell-type-specificity` establishes that many drivers are **cancer-type-restricted at the gene level** (lineage
addiction; IntOGen's 63%-restricted tail). `paper:Kauko2025` reports the complementary fact: diverse
oncogenes **converge** downstream on a shared growth program (MYC → ribosome biogenesis / translation;
NOLC1 node). The synthesis question: **does gene-level cancer-type specificity collapse when drivers
are aggregated to pathways?** I.e. melanoma, lung, and colon hit *different* RTK-RAS *genes* (BRAF
vs EGFR/KRAS vs KRAS/APC-context), but all converge on **RTK-RAS / PI3K / cell-cycle** at the
pathway level. The test has two faces:

1. **Convergence.** Is the cancer-type × **pathway** mutation matrix far more shared (lower
   specificity) than the cancer-type × **gene** matrix — and how much of gene-level "restriction" is
   really *interchangeability within a pathway*?
2. **Within-pathway redundancy.** Do drivers in the same pathway show **mutual exclusivity** within
   cancer types (the redundancy signature: you need one hit on the pathway, not two)?

## Why It Matters

- It directly tests the **tension between `question:0042-driver-normal-expression-tissue-cell-type-specificity` (gene-level divergence) and Kauko2025 (downstream
  convergence)**, and tells us at which grain "cancer-type specificity" is actually a real biological
  claim versus an artifact of gene interchangeability.
- It connects to the **temporal theme**: pathway-grain modules are the natural unit for ordering
  (`hypothesis:0004-mhn-pathway-ordering` is already pathway-oriented), and within-pathway mutual exclusivity is the association
  substrate (`topic:co-occurrence-and-mutual-exclusivity`, `task:t078`) that theme consumes.
- Risk if unasked: we over-interpret gene-level driver restriction (`question:0042-driver-normal-expression-tissue-cell-type-specificity`) as tissue-specific *biology*
  when much of it may be *which gene the cell-of-origin makes accessible on a shared pathway* — exactly
  Kauko2025's "divergence at the entry point, convergence downstream."

## Cross-project federation (multiple myeloma — mm30)

This is the **pan-cancer mutation-level echo** of a convergence question the sibling MM project has
been testing at the expression/cell-state level:

- `hypothesis:h4-attractor-convergence` in `~/d/cancer/cancer-types/multiple-myeloma` — MM trajectories
  converging toward a terminal attractor (PR/RRPC). Now `weakened`: convergence is **not** reproducible
  at the within-MM cytogenetic-subtype level, but **is** re-anchored to the **cancer-vs-normal axis**
  (the cross-cluster synthesis `report:2026-05-02-convergence-cross-cluster` in
  `~/d/cancer/mechanisms/evolution`; Gatenby 2025 transcriptomic convergence).
- The lesson MM hands us: **specify the scale before claiming convergence.** `question:0045-pathway-grain-convergence-vs-gene-grain-divergence` tests it at the
  cleanest scale we have — **pathway membership of recurrent somatic drivers** — which is the mutation
  analogue of MM's expression-program convergence, and avoids MM's cross-scale-decoupling trap by
  staying at one scale (gene → pathway) end to end.

## What we can compute (substrate on disk + one small external map)

- **Have:** the cancer-type × gene mutation matrices (`gene_cancer_study.feather`,
  `gene_cancer_pooled.feather`); OG/TSG roles (`data/cosmic_cgc.tsv`); the co-occurrence /
  mutual-exclusivity machinery (`task:t078`).
- **Need (cheap external):** a gene→pathway map — Reactome / KEGG, or the **TCGA pathway analysis**
  10 canonical pathways [@SanchezVega2018] (a small curated table, far cheaper than the expression ingest
  `question:0042-driver-normal-expression-tissue-cell-type-specificity` needs).
- **Test:** aggregate driver hits to pathways per cancer type; compare pathway-grain vs gene-grain
  specificity (e.g. Tau-like spread, or Jaccard sharing across cancer types); within-pathway mutual
  exclusivity per cancer type as the redundancy readout.

## Confounds that decide interpretability

- **Pathway annotation circularity.** Pathway databases are curated partly *from* cancer genetics;
  "convergence on cancer pathways" can be partly definitional. Use a pathway map not built from cancer
  driver lists where possible, and report sensitivity across map choices.
- **Gene length / hypermutation** (`hypothesis:0003-gene-length-confounds-literature-attention`,
  `question:0047-hypermutation-confound-on-driver-tissue-specificity`) inflate within-pathway membership counts; control as
  in `question:0043-driver-cancer-type-breadth-distribution`.
- **Mutual exclusivity ≠ pathway redundancy alone.** Exclusivity also arises from synthetic lethality
  and subtype structure; do not read every exclusive pair as "one pathway hit suffices."
- **Aggregation hides direction.** Pathway grain answers *convergence*, not *order* — keep separate
  from `hypothesis:0004-mhn-pathway-ordering` (the theme's guardrail: association ≠ order ≠ modules).

## Predictions

- The cancer-type × pathway matrix is **substantially more shared** than the gene matrix — gene-level
  restriction partially collapses at pathway grain (Kauko2025 direction).
- **But not fully:** lineage-factor pathways (e.g. melanocyte/MITF, AR signaling) stay restricted,
  matching `question:0042-driver-normal-expression-tissue-cell-type-specificity`'s route-1 oncogene subset — convergence is strongest for the **general growth program**
  (RTK-RAS/PI3K/cell-cycle/MYC), weakest for lineage-identity pathways.
- Within-pathway mutual exclusivity is detectable for canonical redundant pathways (RTK-RAS) within
  high-N cancer types.

## Stop / null conditions

- If pathway-grain sharing is **no greater** than gene-grain after the length/hypermutation controls,
  there is no convergence signal at our resolution → report that driver specificity is genuinely
  gene-level here, and Kauko2025's downstream convergence is not visible in mutation-incidence data
  (it is an expression/functional phenomenon, not a mutation-frequency one) — an informative boundary.
- If results swing entirely with pathway-map choice, report as annotation-dependent, not biological.

## Connections to Project

- **Tension it resolves:** `question:0042-driver-normal-expression-tissue-cell-type-specificity` (gene-level divergence) vs `paper:Kauko2025` (downstream convergence).
- **Shared substrate:** `topic:co-occurrence-and-mutual-exclusivity` / `task:t078`, `hypothesis:0004-mhn-pathway-ordering` (pathway ordering),
  `question:0043-driver-cancer-type-breadth-distribution` (the driver roster), `theme:0003-temporal-structure-of-carcinogenesis-order-count-and-timing-of-the`.
- **Cross-project:** mm30 `hypothesis:h4-attractor-convergence`; evolution-project convergence synthesis.
- **Priority:** **P3** — needs only a small gene→pathway table on top of substrate already on disk;
  cheapest "new biology" question in the batch after `question:0043-driver-cancer-type-breadth-distribution`.
