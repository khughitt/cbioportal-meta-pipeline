---
id: "hypothesis:h04-mhn-pathway-ordering"
type: "hypothesis"
title: "MHN pathway-level ordering recovers intrinsic-mutator → lineage-driver → checkpoint-loss progression"
status: "proposed"
phase: "candidate"
source_refs:
  - "paper:Vocht2026"
  - "paper:Schill2024"
related:
  - "question:q012-mutation-ordering-cross-sectional-inference"
  - "theme:temporal-structure-of-carcinogenesis"
  - "task:t135"
  - "task:t152"
  - "discussion:2026-04-24-mutation-ordering-and-path-dependency"
  - "topic:co-occurrence-and-mutual-exclusivity"
created: "2026-04-27"
updated: "2026-04-28"
---

# Hypothesis: MHN pathway-level ordering recovers intrinsic-mutator → lineage-driver → checkpoint-loss progression

## Organizing Conjecture

Cross-sectional cBioPortal / GENIE data contain enough joint-distribution structure that
**Mutual Hazard Networks** (Schill 2020; observation-event extension Schill 2024; Python
implementation Vocht 2026) can recover a directed progression order at the **Sanchez-Vega
2018 pathway level** which is biologically interpretable and consistent with PCAWG
(Gerstung 2020) chronologies. The recovered order, per histology, follows a pattern: **(i)
intrinsic mutators (MMR, POLE, POLD1) → (ii) lineage-specifying drivers (RTK/RAS, Wnt, NRF2,
PI3K, etc.) → (iii) checkpoint loss / expansion-permitting events (TP53, RB1, cell-cycle)**.
Gene-level ordering, used as a drill-down on top of pathway-level, recovers known
per-histology orderings (APC → KRAS → TP53 in CRC; STK11 → KEAP1 in LUAD; BRAF → TERT in
thyroid; TP53 → PIK3CA in breast).

This is a candidate hypothesis. Promotion to active is gated on (a) VAF availability audit
(`t133`), (b) primary-method verification that Schill 2024's observation-event correction
is usable for cBioPortal-style diagnostic cohorts and panel missingness, and (c) a
simulation-calibration check that recovered edges from synthetic tumors drawn from a known
MHN pass under our panel + cohort-size distribution.

## Proposition Bundle

### Core Propositions

- **P1 (recovery of pathway-level pattern).** Per-histology MHN fits at the Sanchez-Vega
  10-pathway level place intrinsic-mutator events (MMR/POLE/POLD1, where present at
  histology-relevant frequencies) upstream of checkpoint events (TP53/RB1/cell-cycle) more
  often than the converse. The primary ordering endpoint is edge direction / inferred path
  position, not base hazard alone, because rare early events can have low marginal
  frequency.
- **P2 (per-histology gene-level recovery).** Gene-level MHN fits per histology, after
  hypermutator stratification (`t081`) and CH/normal-tissue contamination correction (`h01`),
  recover at least 70% of the per-histology orderings tabulated in PCAWG Gerstung 2020
  Table 1 (CRC: APC → KRAS → TP53; LUAD: STK11 → KEAP1; thyroid: BRAF → TERT; breast:
  TP53 ⇄ PIK3CA → late events).
- **P3 (collider-bias resolution helps).** Schill 2024's observation-event-augmented MHN
  produces edges that are more consistent with PCAWG ground truth than the original
  Schill 2020 model, on the same data — quantified as Spearman ρ between recovered hazard
  ordering and PCAWG chronology rank, comparing the two model variants.

### Supporting Or Auxiliary Propositions

- TP53 places "late relative to lineage drivers" in solid-tumor histologies (consistent with
  PCAWG and the discussion's expectation), confirming that the naive "all repair genes
  first" reading of the mutator-phenotype hypothesis is wrong without distinguishing
  intrinsic mutators from checkpoint genes.
- The pathway-level result is more stable across leave-one-study-out folds than the
  gene-level result — pathway aggregation absorbs panel coverage heterogeneity.

## Current Uncertainty

- **VAF availability is unknown** across cBioPortal studies; `t133` audit gates the
  *clonality-aware* version of this work. The population-level (binary presence/absence)
  version is data-tractable today, but the strongest test combines both routes.
- The collider-bias problem in cross-sectional cancer-progression modeling (a sample is
  observed *because* it became diagnosable; observation rate depends on driver presence)
  was a fundamental concern flagged in `discussion:2026-04-24-mutation-ordering-and-path-
  dependency`. Schill 2024 claims to resolve it via an explicit observation event; this
  is supported by the Vocht 2026 implementation note and the paywalled Schill 2024 summary,
  but the full primary-method details and panel-missingness implications still need to be
  checked before this hypothesis is promoted to active.
- Panel heterogeneity: a gene absent from a panel is not wild-type. Per-sample callability
  conditioning is required for any ordering inference; the same correction applies as for
  `t078` co-occurrence.
- Power at the gene-pair level drops steeply beyond triples for ~10³–10⁴ samples per
  histology. Pathway-level fits should be powered; gene-level may be limited to triples in
  most histologies.

## Predictions

- Per-histology MHN at pathway level: intrinsic-mutator events are uncommon but inferred
  upstream when present; checkpoint events are frequent but tend to sit downstream of
  lineage-specifying drivers after observation-event correction.
- For the LUAD GENIE 3,662-sample dataset (Vocht 2026 demo), our pipeline reproduces
  qualitatively the trajectories shown in their Figure 2 within a documented tolerance
  (recovered top-3 trajectories agree set-wise).
- Adding hypermutator stratification (`t081` `is_hypermutator` filter) sharpens the
  intrinsic-mutator-upstream signal: in the hypermutator-only sub-cohort, MMR/POLE rank
  even more clearly upstream; in the non-hypermutator cohort, intrinsic-mutator events
  drop in inferred hazard, but checkpoint-late persists.
- Schill 2024's observation-event variant produces hazard orderings that correlate more
  strongly with PCAWG chronology than the Schill 2020 variant (ρ improvement ≥ 0.10).

## Falsifiability

- If MHN edges are unstable under leave-one-study-out (or under bootstrap resampling of the
  cohort) — i.e. fold-pair edge-set Jaccard < 0.5 at the pathway level — the inference is
  too noisy to support directional claims; the hypothesis is operationally falsified
  regardless of mean-edge biology.
- If the simulation-calibration check (synthetic tumors from a known MHN, subsampled to our
  panel + cohort-size distribution) fails to recover ≥70% of injected edges, the inference
  pipeline is not powered for this data and the hypothesis is operationally falsified.
- If the inferred order on PCAWG-overlapping cancer types disagrees with PCAWG (recovery of
  ≤30% of Gerstung 2020 Table 1 orderings), the method is not validated and the biology
  claim cannot be defended.

## Promotion criteria

Promote to `phase: active` when **all three** are met:

1. **t133 VAF audit completes** with a binary decision: clonality-aware route is or is not
   available. (Either outcome unblocks promotion — clonality-aware *strengthens* but is not
   required for the population-level version.)
2. **Schill 2024 primary-method check completes** (`paper:Schill2024` plus either primary
   PDF access or a documented package-level pilot) and confirms that the observation-event
   correction is usable for diagnostic cBioPortal cohorts with panel-specific missingness.
3. **Simulation calibration passes** — an MHN fit on synthetic tumors drawn from a known
   MHN, subsampled to our panel + cohort-size distribution per histology, recovers ≥70% of
   injected edges at the pathway level.

## Supporting Evidence

- **Vocht 2026 (paper):** `mhn` Python package; state-space restriction + GPU; >100-event
  ceiling; demonstrated on 3,662 GENIE LUAD samples. Computational tractability for our
  cohort sizes is not in question.
- **Schill 2020 (paper):** original MHN with TCGA pan-cancer validation against known
  per-histology orderings (APC → KRAS → TP53 in CRC; TP53 → PIK3CA in breast; IDH1 → TP53
  → ATRX in glioma).
- **PCAWG Gerstung 2020 Nature 578:122:** independent ground truth for pan-cancer
  chronology, derived from within-tumor VAF/CCF on whole-genome data.
- **Sanchez-Vega 2018 Cell:** project already has the 10-pathway annotation pipeline in
  place (`process_sanchez_vega_pathways.py`); aggregation infrastructure exists.
- **Discussion (2026-04-24):** detailed prior analysis of identifiability, confounders, and
  method-selection rationale.

## Disputing Evidence

- Cross-sectional ordering is fundamentally under-identified — `P(A) > P(B) ∧ P(A,B)` is
  consistent with both "A precedes B in time" *and* "A-only clones are simply fitter than
  B-only clones." MHN/CBN resolve this only under no-reversal and constant-hazard
  assumptions, both arguably violated in cancer.
- TP53 appears late in PCAWG (Gerstung 2020) for many histologies, contradicting the naive
  "all repair genes first" reading of the mutator-phenotype hypothesis. The pathway-level
  framing handles this (TP53 is checkpoint, not intrinsic mutator) but only if the framing
  itself is correct; if hypermutator-driven cohorts are mis-classified, the predicted order
  collapses.
- Diagnostic-cohort selection bias is a known collider; the original Schill 2020 model does
  not account for it. The full hypothesis depends on Schill 2024 actually resolving this.

## Evidence Needed To Shift Belief

- **Decisive supporting test:** Reproduce the Vocht 2026 LUAD demo on `genie` LUAD samples
  in our pipeline; if recovered top-3 trajectories agree with their Figure 2 set-wise, the
  pipeline is validated. Then run on CRC, breast, thyroid, glioma; compare per-histology
  recovered ordering against PCAWG Gerstung 2020 Table 1.
- **Decisive disputing test:** Bootstrap resampling of the cohort gives edge-set Jaccard <
  0.5 at the pathway level; the inference is too unstable to support claims.
- **Identifiability test:** Apply the Schill 2024 observation-event extension and compare
  to the Schill 2020 baseline; if no improvement on PCAWG-overlap, collider bias is either
  not the dominant problem or not being resolved by this method.

## Related Work

- **Questions:** `q012` (this hypothesis is the directed-ordering frame for q012).
- **Discussions:** `discussion:2026-04-24-mutation-ordering-and-path-dependency`.
- **Topics:** `topic:co-occurrence-and-mutual-exclusivity`.
- **Tasks (existing):** `t078` (DISCOVER co-occurrence — provides callability mask + null
  model), `t132` (ordering methods literature search), `t133` (VAF audit), `t135` (MHN fit
  per histology — already filed, blocked on `t078`).
- **Tasks:** `t135` (production MHN fit), `t152` (Vocht LUAD replication + simulation
  calibration).
- **Sibling hypotheses:** `h06` (pre-malignant n-1 driver carriage — observed-ordering
  complement to MHN-inferred ordering).
- **External:** Schill 2020 Bioinformatics; Schill 2024 (collider-bias resolution); Vocht
  2026 Bioinformatics Advances; Gerstung 2020 *Nature* 578:122; Beerenwinkel 2007 (CBN);
  Caravagna 2016 (CAPRI).
