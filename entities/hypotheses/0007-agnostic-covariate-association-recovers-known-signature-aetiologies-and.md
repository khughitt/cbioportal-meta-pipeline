---
type: hypothesis
title: Agnostic covariate association recovers known signature aetiologies and surfaces
  novel upstream causes
status: proposed
created: '2026-05-30'
updated: '2026-05-30'
id: hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
phase: active
ontology_terms:
- mutational signatures
- somatic mutation
- gene expression
- tumor mutational burden
datasets:
- cBioPortal (~300 studies)
- TCGA MC3 (tcga_mc3)
- AACR GENIE
source_refs:
- paper:Alexandrov2020
- paper:Degasperi2022
related:
- topic:signature-decomposition-unmatched-normal
- question:0018-can-mutational-signature-decomposition-be-added-downstream-of-the-cross
- question:0019-does-de-novo-extraction-on-the-aggregated-cohort-surface-factors-not-in
- discussion:0004-common-mutational-signatures-known-vs-learned-immune-causes-and
---
# Hypothesis: Agnostic covariate association recovers known signature aetiologies and surfaces novel upstream causes

## Summary

Mutational-signature aetiologies are conventionally assigned by hand: an analyst correlates a
de-novo factor's spectrum against COSMIC, attaches a label (UV, smoking, APOBEC…), and post-hoc
links it to one suspected exposure. This privileges processes we already believe are causative
(see `discussion:0004-common-mutational-signatures-known-vs-learned-immune-causes-and`).

This hypothesis proposes an **agnostic** alternative: treat per-sample signature exposures
(`H`, the columns of the NMF factorization `M ≈ W·H`) as outcomes, and run a phenome-wide,
multiplicity-corrected, **within-tissue** association of every exposure against every
co-measured covariate the pipeline already holds — structured clinical fields
(age, sex, race, stage, MSI, primary_site, oncotree_code), derived molecular features (TMB,
hypermutator class), and — most informatively — **co-measured mRNA expression**
(`export_study_expression.py`) reduced to unsupervised modules. Let effect sizes rank the
associations rather than a curator.

The hypothesis is **two-pronged and explicitly falsifiable on the positive-control prong**:

- **H08a (recovery / positive control):** an agnostic association recovers the textbook
  exposure→signature links *without being told them* — UV↔SBS7 in skin, smoking↔SBS4 in lung,
  APOBEC3 expression↔SBS2/13, MMR-loss/MSI↔SBS6/15/26, POLE↔SBS10. If it cannot reproduce the
  known map, its novel hits are not trustworthy.
- **H08b (discovery):** beyond the known map, the same scan surfaces covariates — especially
  expression modules (immune/inflammation, a candidate blind spot per the discussion's Q2) —
  associated with signatures whose aetiology is unknown or only labelled clock-like (SBS5,
  SBS40), generating ranked candidate upstream causes.

## Rationale

- **The substrate already exists.** `convert_to_feather.py` ingests the clinical covariates;
  `export_study_expression.py` surfaces co-measured mRNA + a merged clinical table for the
  *same* samples; `run_restricted_sigprofiler_assignment.py` already does restricted
  assignment. The missing piece is the association layer, not the data.
- **Expression is a second, independent "unbiased" decomposition of the same patients.**
  Concordance between a latent mutation factor and a latent expression module is stronger
  evidence of a shared upstream driver than either modality alone (cross-decomposition
  concordance).
- **The known map is a built-in positive control.** Unusually for a discovery method, we can
  validate it before trusting it: aetiologies with strong literature support must re-emerge
  unprompted.

## Predictions

1. Within-tissue, FDR-controlled association recovers ≥ the canonical exposure→signature links
   at effect sizes clearly above the null (H08a).
2. APOBEC signatures (SBS2/13) associate with *APOBEC3A/B expression* more strongly than with
   any single clinical label — demonstrating expression resolves a mediator the clinical
   covariates cannot.
3. At least one clock-like / unexplained signature (SBS5 or SBS40) shows a reproducible
   association with an expression module not currently in its COSMIC aetiology — a ranked novel
   candidate (H08b).
4. Associations attenuate or reverse sign when tissue is *not* conditioned on — quantifying how
   much of the naive "exposure→signature" story is tissue collinearity.

## Falsifiability

- **Falsifies H08a (and undermines the whole approach):** the scan fails to recover the
  well-supported exposure→signature links within tissue at any reasonable FDR — i.e. the method
  is underpowered or confounded beyond rescue on cBioPortal/MC3-scale data.
- **Falsifies H08b:** after positive-control recovery succeeds, no novel covariate↔signature
  association survives FDR + reverse-causation screening + a held-out-cohort replication — i.e.
  the agnostic scan adds nothing beyond the known map.
- **Design guards (pre-registration material for `science:pre-register`):**
  - within-tissue strata only; report the unconditioned version solely to quantify confounding.
  - per-sample de-novo signatures only on WES/WGS substrates (tcga_mc3); panels enter as
    cohort-pooled / refit, never per-sample (the binding mutation-count constraint, q018).
  - **reverse-causation guard:** an expression↔signature association is a hypothesis, not a
    cause — expression can be *downstream* of a driver mutation. Flag, do not assert causality;
    require mediation logic before any upstream claim.
  - multiplicity: FDR across the full covariate×factor grid, reported with the grid size.

## Alternative Explanations

These are **co-equal rivals**, to be adjudicated by the data — none privileged, including this
hypothesis's own framing:

- **R1 — Tissue collinearity, not exposure.** Any covariate↔signature link may be a restatement
  of tissue-of-origin (each exposure is tissue-enriched). Adjudicated by the within- vs
  unconditioned-tissue contrast (Prediction 4).
- **R2 — Reverse causation / consequence.** Expression module tracks the signature because the
  signature's driver mutation *changed* expression (e.g. a driver remodels its own pathway),
  not because expression is upstream. Adjudicated by mediation + temporality where available.
- **R3 — Selection / immunoediting on burden.** Association reflects which clones *survived*
  (acting on `H`), not which process *generated* the mutations (`W`) — the discussion's Q2
  point. Adjudicated by testing spectrum-attribution vs burden-attribution separately.
- **R4 — Batch / study / assay artifact.** The "agnostic" covariate is actually a study or
  panel-coverage proxy. Adjudicated by including study/assay as nuisance covariates and by the
  artifact-signature flag (SBS27/43/45–60).
- **R5 — The hand-labelled map is already optimal.** The agnostic scan recovers exactly the
  known map and nothing reproducible beyond it (= H08b falsified). A legitimate, data-decided
  outcome, not a failure of execution.

## Status & Next Steps

- **status: proposed.** The first H08a positive-control read has now run and remains
  inconclusive rather than promoted.
- **Positive control (H08a) is now pre-registered:**
  `pre-registration:0003-h08-positive-control-agnostic-association-must-recover-known-signature` (committed 2026-05-30). It locks the recovery design —
  three confirmatory arms (UV→SBS7 / smoking→SBS4 / APOBEC3-expr→SBS2/13), a **2-of-3** pass gate,
  a **top-3 rank + FDR q<0.05** per-arm criterion, anatomic-site UV proxy, and the rule that a
  `[-]` (0/3) verdict voids the H08b discovery prong. H08b (discovery) remains **unregistered** and
  is gated behind a passing H08a verdict — author its own pre-reg once H08a passes and t177 fixes
  the novelty bar.
- **2026-06-01 update:** `task:t199` ran the registered H08a scan and produced a `[?]` verdict
  (1/3 arms passed). `task:t200` diagnosed the failed arms, and `task:t204` ran a repaired
  smoking-arm read; the repair was positive and significant but still failed the top-3 rank gate.
  Per `discussion:0005-h08b-gate-handling`, H08b is not opened as confirmatory work.
  A narrow SBS40/SBS5 expression-module prototype may proceed only as exploratory analysis.
- Next: if continuing H08, either run a clearly labeled exploratory `task:t182` prototype or design
  a new repaired positive-control gate that addresses both the UV proxy and lung burden-dominance
  issues before any H08b promotion decision.

## Proposition DAG

The causal model (`models/h08-agnostic-signature-association.dot`) is materialized as a proposition DAG
with support/dispute evidence at `doc/figures/dags/h08-agnostic-covariate-association.edges.yaml`
(+ `.dot`, auto-rendered PNG), built by `t214`. Twelve edges carry the arm-level H08a verdicts and the
R1–R5 rivals with task IDs and concrete numbers: APOBEC3-expr→SBS2/13 (Arm C, **supported**: rank 1/10,
β = +0.458, q ≈ 4.4e-12, permutation- and leakage-guarded), smoking→SBS4 (Arm B, **tentative**: repaired
β = +0.267, q = 5.1e-4, but rank 5/8), UV→SBS7 (Arm A, **eliminated** as a proxy: rank 10/14, negative),
the gated H08b expr-module→H edge (**unknown**, carrying the R2 reverse-causation non-identification), and
the R1/R3/R4 confounders (tissue / selection-on-H / study-assay) as structural adjustment-set edges.

## Related

- Topic notes: `topic:signature-decomposition-unmatched-normal`
- Method/model: `method:h08-agnostic-association-model`, `models/h08-agnostic-signature-association.dot`
- Proposition DAG: `doc/figures/dags/h08-agnostic-covariate-association.edges.yaml`
- Discussion: `discussion:0004-common-mutational-signatures-known-vs-learned-immune-causes-and`
- Questions: `question:q018-...`, `question:q019-...`
- Code substrate: `code/scripts/export_study_expression.py`, `code/scripts/convert_to_feather.py`,
  `code/scripts/run_restricted_sigprofiler_assignment.py`

## Literature-informed design refinements (2026-05-31 paper batch)

A ~80-paper mutational-signature literature batch (summaries in `doc/papers/`, syntheses in the
`topic:*` notes linked above) sharpened the h08 design. Key consequences:

- **Positive-control set extended.** Beyond UV/SBS7, smoking/SBS4, APOBEC/SBS2-13, MMR/SBS6-15-26,
  POLE/SBS10: add **SBS9** (germinal-centre/AID) as a *tissue-restricted* positive control in
  lymphoid strata (`paper:Machado2022`), and evaluate **SBS54** as an MSI discriminator
  (`paper:Ji2023`) pending a germline-artefact check. See `question:0021`.
- **APOBEC Arm C respecified** to a joint A3A+A3B expression score, with MMR expression as a
  positive co-predictor of SBS2/13 in MSS strata (MMR-omikli coupling; `paper:Carpenter2023`,
  `paper:MasPonte2020`). See `question:0022`.
- **Clock-like confounders.** SBS1/SBS5 are clock-like by construction (age must be a pre-specified
  nuisance covariate); **SBS5 is an expected true-negative** for single exogenous covariates
  (`paper:Spisak2025`). The flagship h08b discovery test is **SBS40-vs-SBS5 separation via
  age-conditioned expression modules** (`question:0023`).
- **Reliability gates.** De novo extraction needs consensus-called studies and adequate per-sample
  counts (`paper:Jiang2025a`, `paper:Islam2022`, `paper:Medo2024`); single-caller studies are flagged.
  See `question:0020`, `task:t178`, `task:t179`.
- **Treatment confound.** Iatrogenic signatures (SBS11/SBS31/SBS35/SBS87) must be flagged as a
  confound stratum before the scan (`paper:Diamond2023`, `paper:Crisafulli2022`). See `question:0024`,
  `task:t181`.
- **Causal-direction guard.** The expression→`H` edge remains unidentified by adjustment; h08b hits
  require a pre-specified guard (mediation / clonal timing / cross-study replication) before any
  upstream claim. See `question:0025`.

These refinements are tracked as `task:t178`–`task:t183`; they do not change the committed H08a
positive-control gate in `pre-registration:0003-h08-positive-control-agnostic-association-must-recover-known-signature` (they extend and operationalise it).
