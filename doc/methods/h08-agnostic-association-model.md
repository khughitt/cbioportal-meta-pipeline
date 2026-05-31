---
id: "method:h08-agnostic-association-model"
type: "method"
title: "Agnostic covariate–signature-exposure association model (h08)"
status: "active"
created: "2026-05-30"
updated: "2026-05-31"
related:
  - "hypothesis:h08-agnostic-covariate-association-recovers-known-signature-aetiologies-and"
  - "topic:signature-decomposition-unmatched-normal"
  - "discussion:2026-05-30-common-mutational-signatures-known-vs-learned-immune-causes-and-confounding"
  - "search:2026-05-30-ehr-rich-substrates-for-agnostic-signature-association"
  - "search:2026-05-31-prior-agnostic-signature-aetiology-association"
  - "topic:aetiology-covariate-association"
  - "topic:signature-extraction-fitting-methods"
  - "topic:dna-damage-repair-signature-mechanisms"
  - "topic:apobec-mutagenesis"
  - "topic:signatures-expression-microenvironment"
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

**Set extensions (2026-05-31 batch; see `hypothesis:h08` design-refinements section):** add
**SBS9** (germinal-centre/AID) as a *tissue-restricted* positive control in lymphoid strata
(`paper:Machado2022`); evaluate **SBS54** as an MSI discriminator (`paper:Ji2023`) pending a
germline-artefact check (`question:q021`). **SBS5/SBS1 are clock-like by construction** — pre-classify
as nuisance, not discovery targets; **SBS5 is an expected true-negative** for any single exogenous
covariate (`paper:Spisak2025`). Treatment-induced signatures (SBS11/SBS31/SBS35/SBS87) must be
flagged as a confound stratum, not read as covariate hits (`question:q024`).

## Prior art (t177 literature scan, 2026-05-31)

The agnostic covariate↔signature-activity association is **not novel** — see
`search:2026-05-31-prior-agnostic-signature-aetiology-association`. The direct method predecessor is
**TCSM** (`paper:Robinson2019`), which already models tumor covariates of signature exposure to infer
etiology and validates by recovering UV/smoking/APOBEC/MMR. Related tools: signeR 2.0
(`paper:Drummond2023`), Diffsig (`paper:Park2023`), PPF (`paper:Zito2025`); the supervised inverse is
SuperSigs (`paper:Afsari2021`). The closest large systematic scans are `paper:Sorensen2023`
(DNA-repair-gene deficiencies, the best design template for our scan shape) and `paper:ValiPour2022`
(germline variants); `paper:Luo2023` covers the immune/TME axis but with deconvolution features, not
de-novo expression modules.

**Consequence for the design:** H08a (positive control) is a *pre-registered re-validation* of the
TCSM logic on MC3 — reproducible and feasible (multiple papers recover the textbook map unprompted),
but it should be stated as confirmatory-of-method, not as novelty. H08b's defensible delta is
narrowed to **unsupervised co-expression *modules* as the agnostic covariate set + cross-decomposition
concordance (latent `H` ↔ latent expression module) + pre-registered positive-control gating** — none
of which is the stated primary design of the prior work. A generic "associate signatures with
covariates" discovery claim would be scooped.

## Next steps

- Literature gate: `task:t177` — **DONE** (see prior-art section above); H08b scope narrowed accordingly.
- `science:pre-register` the positive-control + discovery design once `q018` confirms downstream
  signature feasibility + panel adequacy.
- Two-track substrate plan per `search:2026-05-30-ehr-rich-substrates-for-agnostic-signature-association`:
  MC3 (signature-grade + expression) and GENIE BPC / MSK-CHORD (EHR-covariate, pooled signatures).
