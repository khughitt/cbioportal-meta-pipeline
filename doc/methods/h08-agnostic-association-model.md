---
id: "method:h08-agnostic-association-model"
type: "method"
title: "Agnostic covariate–signature-exposure association model (h08)"
status: "active"
created: "2026-05-30"
updated: "2026-05-30"
related:
  - "hypothesis:h08-agnostic-covariate-association-recovers-known-signature-aetiologies-and"
  - "topic:signature-decomposition-unmatched-normal"
  - "discussion:2026-05-30-common-mutational-signatures-known-vs-learned-immune-causes-and-confounding"
  - "search:2026-05-30-ehr-rich-substrates-for-agnostic-signature-association"
---

# Agnostic covariate–signature-exposure association model (h08)

A causal-DAG sketch for the agnostic association proposed in `hypothesis:h08`. DAG source:
`models/h08-agnostic-signature-association.dot` (render with
`dot -Tsvg models/h08-agnostic-signature-association.dot`).

## The estimand

For each (signature, covariate) pair, the target is the **within-tissue association between a
covariate and a signature's per-sample exposure `H`** — *not* its spectrum `W`. We model `H`
(burden, "how much") separately from `W` (identity, "which process") because selection /
immunoediting act on `H`, so reading exposure as dose risks reverse causation (see
`discussion:2026-05-30-common-mutational-signatures-known-vs-learned-immune-causes-and-confounding`,
Q2).

## Variables

- **Outcome:** signature exposure `H` (per-sample, per-signature). Derived per-sample only on
  WES/WGS substrates (`tcga_mc3`); cohort-pooled on panels.
- **Candidate causes (the agnostic scan):** exogenous exposure proxies, endogenous enzyme
  activity (APOBEC3/POLE), DNA-repair capacity (MMR/HRD), and **co-measured expression modules**
  (the most informative novel covariate, from `export_study_expression.py`).
- **Confounders (condition on):** tissue of origin (master confounder), ancestry/germline,
  treatment history, study/panel/assay (batch + callable footprint).
- **Selection:** acts on `H` only; modeled as a node that biases burden, not spectrum.

## Identification

- **Adjustment set:** {tissue, treatment, study/assay, ancestry}; run **within tissue strata**,
  reporting the unconditioned version *only* to quantify how much of a naive association is tissue
  collinearity (Prediction 4 of h08).
- **The expression→`H` edge is NOT identified by adjustment alone.** It shares a bidirected edge
  with `H` (reverse causation R2: a driver mutation can remodel its own expression module). An
  expression↔signature hit is a **ranked hypothesis**, requiring mediation logic and, where
  available, temporality before any upstream claim.

## Rival explanations encoded in the DAG

Co-equal, data-adjudicated (1:1 with h08's Alternative Explanations):

| Rival | DAG mechanism | Discriminating test |
|---|---|---|
| R1 tissue collinearity | `Tissue → {covariate, H}` | within- vs unconditioned-tissue contrast |
| R2 reverse causation | `H → ExprModule` (dashed) | mediation / temporality |
| R3 selection on burden | `Selection → H` | spectrum- vs burden-attribution split |
| R4 batch/assay artifact | `StudyAssay → {H, ExprModule}` | nuisance covariate + artifact-signature flag |
| R5 known map is optimal | (no surviving novel edge) | post-positive-control discovery yield |

## Positive control

Before trusting any novel edge, the scan must **recover the textbook edges unprompted**: UV↔SBS7
(skin), smoking↔SBS4 (lung), APOBEC3 expr↔SBS2/13, MMR/MSI↔SBS6/15/26, POLE↔SBS10. Failure here
(H08a falsified) means the method is underpowered or confounded beyond rescue and the discovery
prong is void.

## Next steps

- Literature gate: `task:t177` (what agnostic/PheWAS signature-aetiology work already exists).
- `science:pre-register` the positive-control + discovery design once `q018` confirms downstream
  signature feasibility + panel adequacy.
- Two-track substrate plan per `search:2026-05-30-ehr-rich-substrates-for-agnostic-signature-association`:
  MC3 (signature-grade + expression) and GENIE BPC / MSK-CHORD (EHR-covariate, pooled signatures).
