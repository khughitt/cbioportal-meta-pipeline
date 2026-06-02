---
id: "synthesis:h04-mhn-pathway-ordering"
type: "synthesis"
title: "Synthesis: h04-mhn-pathway-ordering"
report_kind: "hypothesis-synthesis"
hypothesis: "hypothesis:h04-mhn-pathway-ordering"
generated_at: "2026-06-02T09:52:22Z"
source_commit: "037f0ab2d3c84ecc56bebd843e361c1a9dfbfa66"
provenance_coverage: "thin"
---

# Synthesis: MHN pathway-level ordering recovers intrinsic-mutator → lineage-driver → checkpoint-loss progression

> **Candidate-phase hypothesis.** This hypothesis has not been promoted to active; it appears in the project rollup under "Candidate frames." Promotion is gated on three explicit criteria described in the Research Fronts section below.

## State

`hypothesis:h04-mhn-pathway-ordering` proposes that cross-sectional cBioPortal and GENIE data contain enough joint-distribution signal for Mutual Hazard Networks (MHN) — specifically the observation-event-corrected formulation from `paper:Schill2024`, implemented by `paper:Vocht2026` — to recover a directed per-histology progression order at the Sanchez-Vega 2018 pathway level. The predicted pattern places intrinsic mutators (MMR/POLE/POLD1) upstream of lineage-specifying drivers (RTK/RAS, Wnt, PI3K, NRF2), which are in turn upstream of checkpoint-permissive events (TP53, RB1, cell cycle). Gene-level MHN fits serve as a drill-down on this pathway scaffold, with benchmarks against per-histology orderings tabulated in PCAWG Gerstung 2020.

The central inferability concern, formalized in `question:q012-mutation-ordering-cross-sectional-inference`, is that cross-sectional frequency asymmetries are consistent with both temporal precedence and pure fitness asymmetry; CBN-family methods resolve this only under constant-hazard and no-reversal assumptions. Diagnostic-cohort selection introduces a collider bias that `paper:Schill2024` claims to resolve via an explicit observation event; whether that correction holds for panel-specific missingness characteristic of cBioPortal studies is unverified (`task:t132`). VAF availability across the studies is audited by `task:t133`; without it, the clonality-aware route remains indeterminate. No `.edges.yaml` edges, bound interpretations, or graph claims exist for this hypothesis; all state characterizations derive from `hypothesis:h04-mhn-pathway-ordering` spec frontmatter and `question:q012-mutation-ordering-cross-sectional-inference`.

## Arc

Arc reconstruction is limited because no interpretations with `prior_interpretations` chains are bound to h04 yet.

The investigation opened with the framing recorded in `discussion:2026-04-24-mutation-ordering-and-path-dependency`, which surveyed the methods landscape (MHN, CBN, CAPRI, REVOLVER) and crystallized two constraints: (i) only population-level progression-order inference (not within-tumor clonality) is data-tractable without VAF retention, and (ii) the mutator-phenotype prediction is partially wrong unless MMR/POLE/POLD1 are separated from TP53, because TP53 is a late expansion-permitting event in most solid-tumor histologies per PCAWG. The discussion recommended MHN-on-top-of-DISCOVER as the natural direction, sharing the callability mask from `task:t078`.

From that foundation, `hypothesis:h04-mhn-pathway-ordering` was drafted to formalize three testable propositions: pathway-level recovery of the intrinsic-mutator → lineage-driver → checkpoint-loss progression (P1), gene-level recovery of ≥70% of PCAWG Gerstung 2020 Table 1 per-histology orderings after hypermutator stratification (P2), and a demonstrable improvement from the Schill 2024 observation-event variant over the Schill 2020 baseline (P3). The hypothesis spec defined the current task staging: `task:t132` → `task:t133` → `task:t152` → `task:t135`. All remain open. PCAWG data access via `task:t167` is listed as blocked, making the external benchmark currently unavailable within the pipeline. No empirical result from this project's data yet bears on any of the three propositions.

## Research Fronts

**Open tasks:**

- `task:t132` — MHN/CBN/CAPRI/REVOLVER literature search; method-selection rationale and assumption table. P2.
- `task:t133` — VAF availability audit across cBioPortal/GENIE studies; binary decision gates the clonality-aware route. P2.
- `task:t152` — Reproduce the Vocht 2026 GENIE LUAD demo and run simulation calibration (recover ≥70% of injected pathway-level edges from synthetic tumors at this project's panel and cohort-size distribution). Direct test of inference power before any biological claim. P2.
- `task:t135` — Production per-histology MHN fits at Sanchez-Vega pathway level; gene-level drill-down stratified by hypermutator class. P3.
- `task:t156` — Pre-malignant cohort audit; provides the observed-ordering complement to MHN-inferred ordering (sibling hypothesis h06), and may surface cohorts that relax the cross-sectional inference constraint. P2.
- `task:t167` — PCAWG/ICGC-25K WGS cohort acquisition (blocked); required as ground-truth comparator for Gerstung 2020 chronology benchmarks. P3.

**Promotion criteria (from hypothesis spec):**

1. `task:t133` VAF audit completes with a binary decision (either outcome unblocks promotion).
2. `paper:Schill2024` primary-method check confirms the observation-event correction is usable for diagnostic cBioPortal cohorts with panel-specific missingness.
3. Simulation calibration passes: ≥70% of injected edges recovered at pathway level (`task:t152`).

**Live question:** `question:q012-mutation-ordering-cross-sectional-inference` (active; no resolved answer yet).

**Topic context:** `topic:co-occurrence-and-mutual-exclusivity` — the directed ordering frame here is the asymmetric companion to the symmetric co-occurrence work in `task:t078`; the callability mask and null model from `task:t078` are required inputs for any MHN fit.
