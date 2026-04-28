---
id: "synthesis:h04-mhn-pathway-ordering"
type: "synthesis"
report_kind: "hypothesis-synthesis"
hypothesis: "hypothesis:h04-mhn-pathway-ordering"
generated_at: "2026-04-28T03:09:06Z"
source_commit: "c1c6b1f29eef8326e3efde948df540ecc23c95ed"
provenance_coverage: "thin"
---

# Synthesis: MHN pathway-level ordering recovers intrinsic-mutator → lineage-driver → checkpoint-loss progression

> **Candidate-phase hypothesis.** This hypothesis has not yet been promoted to active; it appears in the project rollup under "Candidate frames." Promotion is gated on three explicit criteria described in the Research Fronts section below.

## State

`hypothesis:h04-mhn-pathway-ordering` proposes that cross-sectional cBioPortal and GENIE data contain enough joint-distribution signal for Mutual Hazard Networks (MHN) — specifically the observation-event-corrected formulation in `paper:Schill2024`, implemented in `paper:Vocht2026` — to recover a directed per-histology progression order at the Sanchez-Vega 2018 pathway level. The predicted order is: intrinsic mutators (MMR/POLE/POLD1) upstream of lineage-specifying drivers (RTK/RAS, Wnt, PI3K, NRF2), which are in turn upstream of checkpoint-permissive events (TP53, RB1, cell cycle). Gene-level MHN is framed as a drill-down on this pathway scaffold.

The primary open question, `question:q012-mutation-ordering-cross-sectional-inference`, frames the inferability problem precisely: cross-sectional frequency asymmetries are consistent with both temporal order and pure fitness asymmetry; CBN-family methods resolve this only under constant-hazard and no-reversal assumptions. The collider bias introduced by diagnostic-cohort selection is the dominant methodological concern; `paper:Schill2024` claims to resolve it via an explicit observation event, but whether that correction holds for cBioPortal panel-specific missingness and cohort composition has not yet been verified (`task:t132`). VAF availability across studies is unknown (`task:t133`), leaving the clonality-aware route unconfirmed. No `.edges.yaml` edges, graph claims, or bound interpretations exist for this hypothesis yet; all state characterizations derive from the hypothesis frontmatter and `question:q012-mutation-ordering-cross-sectional-inference`.

## Arc

Arc reconstruction is limited because no interpretations with `prior_interpretations` chains are bound to h04 yet.

The investigation opened with `question:q012-mutation-ordering-cross-sectional-inference`, which consolidated the methodological landscape (MHN, CBN, CAPRI, REVOLVER) and identified the PCAWG Gerstung 2020 pan-cancer chronology as the primary external benchmark for recovered orderings. The question document explicitly flagged diagnostic-cohort collider bias as the key identifiability threat, and recorded that `paper:Schill2024` and `paper:Vocht2026` moved the field's minimum viable formulation from the original cMHN to the observation-event extension.

From that foundation, `hypothesis:h04-mhn-pathway-ordering` was drafted to formalize the biological conjecture: the progression pattern intrinsic-mutator → lineage-driver → checkpoint-loss should be recoverable per histology once the observation-event correction, hypermutator stratification (`task:t081`), and CH-contamination correction are applied. The staging logic established by the hypothesis spec itself defined the current task sequence: `task:t132` (methods literature) → `task:t133` (VAF audit) → `task:t134` (VAF retention) → `task:t152` (Vocht 2026 LUAD replication and simulation calibration) → `task:t135` (production per-histology MHN fits). All five tasks remain open. The hypothesis has not yet advanced past the planning phase; no empirical result from this project's data bears on its propositions.

## Research Fronts

**Open tasks (all blocking promotion):**

- `task:t132` — MHN/CBN/CAPRI/REVOLVER literature search; establishes method selection rationale.
- `task:t133` — VAF availability audit across cBioPortal/GENIE studies; binary decision gates the clonality-aware route.
- `task:t134` — Pipeline change to retain VAF columns (`t_alt_count`, `t_ref_count`, `tumor_f`) in per-study variant feathers; contingent on `task:t133`.
- `task:t152` — Reproduce the Vocht 2026 GENIE LUAD demo in this pipeline; run simulation calibration (recover ≥70% of injected edges from synthetic tumors at our panel + cohort-size distribution). This task directly tests whether the inference pipeline is powered for our data before any novel biological claim is made.
- `task:t135` — Production per-histology MHN fits (blocked on `task:t078`, `task:t081`, and `task:t152`).

**Promotion criteria (from hypothesis spec):**

1. `task:t133` VAF audit completes with a binary decision (either outcome unblocks promotion).
2. `paper:Schill2024` primary-method check confirms the observation-event correction is usable for diagnostic cBioPortal cohorts with panel-specific missingness.
3. Simulation calibration passes: ≥70% of injected edges recovered at pathway level.

**Live question:** `question:q012-mutation-ordering-cross-sectional-inference` (active; no resolved answer yet).

**Topic context:** `topic:co-occurrence-and-mutual-exclusivity` — the directed-ordering frame here is the asymmetric companion to the symmetric co-occurrence analysis in `task:t078`; callability mask and null model from `task:t078` are required inputs.

**Knowledge gaps:** No `topic_gaps` data was provided in the bundle for this hypothesis.
