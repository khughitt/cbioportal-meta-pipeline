---
type: topic
title: Co-occurrence and mutual exclusivity of cancer alterations
status: active
created: '2026-04-13'
updated: '2026-04-13'
id: topic:co-occurrence-and-mutual-exclusivity
ontology_terms: []
source_refs: []
related:
- paper:Cerami2012
- paper:Gao2013
- paper:SanchezVega2018
- paper:Bailey2018
- paper:Ciriello2013
- topic:cancer-driver-genes
---

# Co-occurrence and mutual exclusivity of cancer alterations

## Summary

Pairs of genes whose alterations occur together (co-occurrence) or alternative-of-one-another
(mutual exclusivity) across tumors are informative beyond per-gene rates: co-occurrence suggests
synergistic functional roles; mutual exclusivity suggests redundant pathway activation
(alterations in different genes that both achieve the same downstream effect, so one suffices).
This topic is the methodological frame for the correlation-matrix outputs already in our
pipeline (`scripts/create_correlation_matrices.py` produces `studies/{id}/mut/matrix/gene_cor.feather`).

## Key Concepts

- **Pairwise tests.** The simplest approach: for each gene pair (A, B), build a 2x2 contingency
  table of (A altered y/n) × (B altered y/n) across samples, test with Fisher's exact / chi-squared.
  Cerami 2012 / Gao 2013 implemented this in cBioPortal's "Mutual Exclusivity" tab.
- **Burden-corrected tests.** Naive pairwise tests are confounded by per-tumor mutation burden
  (high-TMB tumors trivially co-mutate everything). DISCOVER (Canisius et al. 2016 Genome Biol),
  WeSME, and SELECT (Mina et al. 2017/2020 Cancer Cell) are designed to control for this.
- **Pathway-level co-occurrence / exclusivity.** Sanchez-Vega 2018 reports **152 mutually
  exclusive + 116 co-occurring pathway pairs** (across 10 canonical pathways) — a much cleaner
  signal than gene-level pairs, as it aggregates rare events.
- **Specific examples to validate against.**
  - Co-occurring: TP53 + cell-cycle (broad); PI3K + Nrf2 (lung / esophageal / H&N squamous);
    KRAS + LKB1/STK11 (lung adenocarcinoma).
  - Mutually exclusive: within RTK-RAS (EGFR vs KRAS vs ERBB2 in lung); BRAF V600 vs KRAS in
    melanoma / colorectal; APC vs CTNNB1 in colorectal; CDH1 vs CTNNB1 in stomach.

## Current State of Knowledge

The field has moved beyond naive pairwise Fisher tests to burden-corrected methods:

- **DISCOVER** (Canisius 2016) — explicit per-tumor mutation rate covariate.
- **SELECT** (Mina 2020) — multi-cohort, identifies evolutionarily-stable patterns.
- **WeSME** — weighted sampling for null distribution.
- **Sanchez-Vega 2018** — pathway-level extension; aggregates rare per-gene signals.

Cancer Hotspots / OncoKB further encode hotspot-vs-domain-loss exclusivity at the variant level
(e.g., BRAF V600 hotspot vs BRAF kinase-domain truncation are functionally different events
within the same gene).

## Controversies & Open Questions

- **What's the appropriate denominator for cross-study mutual-exclusivity testing?** Per-study
  pooled-with-meta-analysis vs combined cross-study pool. Per-study + meta-analysis is more
  defensible but harder. See `topic:cross-study-meta-analysis-cancer-genomics`.
- **Power for rare gene pairs.** Most gene pairs are too rare for statistically significant
  per-cohort co-occurrence / exclusivity. Pathway-level aggregation (Sanchez-Vega) helps; cross-
  cohort meta-analysis helps; some pairs simply require very large cohorts.
- **Tissue-conditional interactions.** A gene pair may co-occur in one cancer and be exclusive
  in another. Pan-cancer aggregation hides this; cancer-stratified analysis surfaces it but
  loses power.

## Relevance to This Project

Our pipeline produces per-study `gene_cor.feather` correlation matrices but **does not currently
test for statistical significance, control for mutation burden, or aggregate across studies**.
Concrete additions:

1. **Burden-corrected pairwise tests** (DISCOVER-style) per study, output as per-study
   `(gene_a, gene_b, p, q, direction)` tables.
2. **Cross-study meta-analysis** of per-study effect sizes, with random-effects pooling.
3. **Pathway-level co-occurrence / exclusivity** using Sanchez-Vega 2018 pathway memberships
   (overlay already planned, task t049). Aggregates rare-gene signal into pathway-pair tests.

Task t042 (focused discovery search) is queued to pull the methods literature systematically.

## Key References

Cerami2012 / Gao2013 (original cBioPortal pairwise mutual-exclusivity testing); SanchezVega2018
(pathway-level co-occurrence / exclusivity tabulation); Bailey2018 / Ciriello2013 (gene-level
patterns at scale). Method-paper seeds — DISCOVER (Canisius 2016), SELECT (Mina 2020), WeSME —
documented but not yet read; see task t042.
