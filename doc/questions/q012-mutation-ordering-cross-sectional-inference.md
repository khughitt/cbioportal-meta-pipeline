---
id: "question:q012-mutation-ordering-cross-sectional-inference"
type: "question"
title: "Can mutation ordering (A→B) be robustly inferred from cross-sectional cBioPortal data?"
status: "active"
ontology_terms: []
datasets:
  - "cBioPortal per-study MAFs"
  - "AACR GENIE panel mutation data"
  - "Sanchez-Vega 2018 10-pathway annotations"
  - "PCAWG Gerstung 2020 pan-cancer chronology (external benchmark)"
source_refs: []
related:
  - "discussion:2026-04-24-mutation-ordering-and-path-dependency"
  - "topic:co-occurrence-and-mutual-exclusivity"
  - "search:2026-04-13-cooccurrence-mutual-exclusivity-methods"
  - "task:t078"
  - "task:t081"
  - "task:t087"
  - "task:t111"
created: "2026-04-24"
updated: "2026-04-24"
---

# Can mutation ordering (A→B) be robustly inferred from cross-sectional cBioPortal data?

## Summary

Cancer is a multi-decade accumulation process, but cBioPortal / GENIE samples are nearly
all single-biopsy snapshots at diagnosis. We observe *which* mutations a tumor carries,
not the *order* in which they were acquired. The question is whether we can recover
directed A→B ordering signals — asymmetries such as "A-alone tumors are common but
B-alone tumors are rare" — from this snapshot data, in a way that is statistically
robust and biologically interpretable.

Established methods exist for exactly this: **Mutual Hazard Networks** (MHN, Schill 2020),
**Conjunctive Bayesian Networks** (CBN, Beerenwinkel 2007), **CAPRI / TRONCO**
(Caravagna 2016), **REVOLVER** (Caravagna 2018). PCAWG (Gerstung 2020, *Nature* 578:122)
reports a pan-cancer chronology that can serve as a benchmark for recovered orderings.

## Why It Matters

- Answers a biological question — is there an evolutionary bias toward acquiring
  DNA-repair / checkpoint mutations before growth / immune-evasion mutations, as
  predicted by the mutator-phenotype hypothesis (Loeb 1974, Loeb 2001)?
- Complements `t078` (co-occurrence / mutual exclusivity): co-occurrence gives
  symmetric association; ordering gives direction. The same cohort, callability mask,
  and null model support both.
- Tests whether the project's data + corrections (CH, normal-tissue contamination,
  hypermutator / signature stratification, panel heterogeneity) are sufficient to
  support a higher-moment statistic than simple frequencies.

## Current Evidence

**Supporting inferability:**
- MHN (Schill 2020) has been validated on TCGA pan-cancer with recovered edges
  matching known progression models in CRC (APC → KRAS → TP53), breast (TP53 → PIK3CA),
  and glioma (IDH1 → TP53 → ATRX).
- PCAWG chronology (Gerstung 2020) reconstructs ordering using within-tumor
  VAF/CCF information; a subset of studies in cBioPortal carry VAF, opening a
  second route to the same signal.
- Pathway-level aggregation (Sanchez-Vega 2018 10-pathway framework, already in
  pipeline) increases statistical power per edge.

**Evidence against naive inferability / confounding:**
- Cross-sectional frequency inequalities are consistent with both true temporal
  order AND pure fitness asymmetry — CBN-family methods resolve this only under
  strong assumptions (no reversal, constant hazards).
- Clonal hematopoiesis contamination artificially inflates VAF of DNMT3A / TP53 /
  TET2 / ASXL1 / PPM1D / CHEK2 / PRPF8 in non-matched-normal studies, making them
  look "earliest" by clonality (`topic:clonal-hematopoiesis-contamination`, `t087`).
- Normal-tissue contamination (`q001`, `q002`, `q005`) inflates specific gene
  calls in esophageal, breast, and skin-near-hotspot studies.
- Panel heterogeneity: a gene absent from a panel is not wild-type. Must condition
  on per-sample callability.
- Cancer-type pooling creates Simpson's-paradox artifacts; ordering must be
  per-histology.
- Signature-coupled TMB: MMR-d / POLE tumors acquire mutations faster regardless
  of causal order. `t081` hypermutator annotation and `t111` signature exposures
  are required stratifiers.
- TP53 is often *late* in solid tumors (PCAWG Gerstung 2020 places it among the
  late pan-cancer events), contradicting a naive "all repair genes first" reading
  of the mutator hypothesis. The right framing distinguishes intrinsic mutators
  (MMR, POLE, POLD1) from checkpoint / expansion-permissive genes (TP53, RB1).

## Thoughts

The most plausible path forward is:

1. Keep this tied to `t078` (co-occurrence / mutual exclusivity). Reuse the same
   sample-specific-background-rate null model (DISCOVER-style Poisson binomial) and
   the same per-sample callability mask. Add MHN on top as the "directed companion."
2. Audit VAF availability across studies before committing; if >50% of studies
   retain VAF, add a second, independent clonality-based ordering estimator and
   use agreement between the two as robustness evidence.
3. Report at **pathway level** first (Sanchez-Vega 10 groups), with gene-level as a
   drill-down. Expect MMR / POLE / POLD1 to precede most things; expect TP53 to
   follow lineage-specifying drivers.
4. Calibrate against PCAWG (Gerstung 2020) chronology per histology before claiming
   any novel ordering result.

Hard gate: if VAF is not retained in most studies AND MHN-style inference on our
specific panel + cohort composition fails a simulation calibration test (recover
known edges from synthetic tumors drawn from a known MHN), the project should not
pursue this.

## Connections to Project

- **Related hypotheses:** none yet; this could motivate one if calibration passes.
- **Required data or analyses:**
  - VAF availability audit across studies (new task).
  - Pipeline change: retain `t_alt_count` / `t_ref_count` / `tumor_f` in variant
    feathers (contingent on audit result).
  - Literature search: MHN / CBN / CAPRI / REVOLVER / PCAWG chronology methods
    and benchmarks (new task).
  - Per-histology MHN fit as a follow-on to `t078`.
  - Stratification by `t081` hypermutator class and `t111` signature exposures.
- **Priority level:** P2 — not ahead of `t078`, but logical direct successor.

## Related

- Topic notes: `topic:co-occurrence-and-mutual-exclusivity` (to be written as part of
  `t078`)
- Article notes: to come from the planned literature search
- Methods / Datasets: MHN (Schill 2020), CBN (Beerenwinkel 2007), CAPRI (Caravagna 2016),
  REVOLVER (Caravagna 2018), PCAWG chronology (Gerstung 2020)
