---
type: question
title: Does chronic adrenergic / glucocorticoid (stress-HPA) signaling leave a detectable
  mutational-signature or TMB footprint, via DNA-repair suppression?
status: active
created: '2026-06-07'
updated: '2026-06-07'
id: question:0039-stress-hpa-adrenergic-mutational-footprint
ontology_terms:
- stress signaling
- HPA axis
- adrenergic signaling
- DNA repair
- mutational signatures
- tumor mutational burden
datasets: []
source_refs:
- paper:Magnon2023
- paper:Mravec2008
- paper:Pu2025
related:
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
- topic:aetiology-covariate-association
- topic:neuro-immune-crosstalk-cancer
- theme:0002-cancer-neuroscience-in-a-mutation-only-pipeline-expression-not-mutation
---

# Does chronic adrenergic / glucocorticoid (stress-HPA) signaling leave a detectable mutational-signature or TMB footprint?

## Summary

`paper:Magnon2023` states that β-adrenergic signaling can **inhibit DNA repair**, and the
nervous–endocrine–immune triad (`paper:Mravec2008`) and neuro-immune reviews (`paper:Pu2025`)
implicate chronic stress (catecholamines, glucocorticoids) in tumor biology. If true, this is
the one place where neuro-biology could plausibly touch the **mutational** layer the project
actually measures: via a repair-deficiency-flavored signature or elevated TMB. This asks whether
any such footprint is detectable in the project's signature/TMB outputs.

## Why It Matters

- Unlike the candidate-gene question (likely artifact), this is a mechanism by which neural/
  endocrine signaling could leave a *real mutational* mark — testable with existing infrastructure.
- Connects cancer-neuroscience to the project core (signatures, TMB,
  `hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and` agnostic association).
- Risk if unanswered: missing a genuine neuro→genome link while (rightly) dismissing the spurious one.

## Current Evidence

- `paper:Magnon2023`: β-adrenergic signaling suppresses DNA repair; HPA glucocorticoids modulate
  immune surveillance and angiogenesis.
- No direct mutational-signature evidence in the batch; this is a hypothesis-generating lead.
- Confounders are severe: stress is correlated with smoking, age, treatment, deprivation.

## Thoughts

- Best current interpretation: speculative; if any footprint exists it is weak and heavily
  confounded — a covariate-association question, not a driver question.
- Major uncertainty: no direct stress covariate in cBioPortal; would need a proxy (e.g.
  beta-blocker exposure as inverse proxy — see `question:0040`) or an external EHR-rich substrate.

## Connections to Project

- Related hypotheses: `hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and` (agnostic covariate–signature association is the natural test bed)
- Required data or analyses: treat adrenergic/glucocorticoid exposure proxies as covariates in
  the agnostic covariate-signature scan against SBS/ID exposures and TMB; check repair-associated signatures specifically;
  require an EHR-rich substrate (MSK-CHORD / GENIE-BPC) for any real test.
- Priority level: P3 (lead; substrate-gated)

## Related

- Topic notes: topic:aetiology-covariate-association, topic:neuro-immune-crosstalk-cancer
- Article notes: paper:Magnon2023, paper:Mravec2008, paper:Pu2025
- Methods/Datasets: agnostic covariate-signature association model; MSK-CHORD / GENIE-BPC
