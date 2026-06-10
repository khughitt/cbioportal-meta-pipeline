---
type: hypothesis
title: Treated/relapsed cohorts inflate apparent gene-by-cancer mutation frequencies
  via iatrogenic mutational signatures
status: proposed
created: '2026-05-31'
updated: '2026-05-31'
id: hypothesis:0009-treatment-induced-signature-frequency-contamination
phase: active
ontology_terms:
- mutational signatures
- somatic mutation
- tumor mutational burden
- chemotherapy
datasets:
- dataset:cbioportal
- dataset:tcga-mc3
- dataset:aacr-genie
source_refs:
- paper:Diamond2023
- paper:Crisafulli2022
- paper:Pleasance2020
- paper:Maura2023
related:
- hypothesis:0001-non-tumor-signal-contamination
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
- topic:clinical-translational-signatures
- topic:signatures-hematologic-malignancies
- question:0024-treatment-exposed-cohort-chemotherapy-signature
---

# Hypothesis: Treated/relapsed cohorts inflate apparent gene-by-cancer mutation frequencies via iatrogenic mutational signatures

## Summary

The project's primary deliverable is cross-study **gene × cancer mutation-frequency** tables. This
hypothesis proposes a specific, signature-detectable contamination of that deliverable: cohorts
enriched for **treated / relapsed / metastatic** patients carry therapy-induced mutational
signatures (temozolomide/SBS11, platinum/SBS31+SBS35, thiopurine/SBS87, melphalan/SBS-MM1) that
**raise total mutation burden and therefore the apparent per-gene mutation frequency** relative to
treatment-naive cohorts of the same cancer type — a batch effect that masquerades as biology in the
aggregated frequency tables. This is the signature-era refinement of `hypothesis:0001`
(non-tumor/contamination signal) applied to the project's core output.

## Rationale

- Therapy signatures are strong, specific, and well-characterised (`paper:Diamond2023`,
  `paper:Crisafulli2022`); `paper:Pleasance2020` and `paper:Maura2023` show they dominate
  advanced/treated cohorts.
- cBioPortal mixes treatment-naive primary cohorts with metastatic/relapsed cohorts (e.g. MSK-MET,
  Hartwig-style studies) for the same cancer types — exactly the contrast that would let an
  iatrogenic burden inflation leak into a pooled frequency table.
- The pipeline already has a hypermutator/TMB annotation layer; adding a treatment-exposed stratum
  (`question:0024`, `task:t181`) makes this directly testable against the existing frequency outputs.

## Predictions

1. Within a cancer type, treatment-exposed cohorts show elevated median TMB and a detectable
   therapy-signature exposure (SBS11/31/35/87) absent (or much lower) in treatment-naive cohorts.
2. Per-gene mutation frequencies in treated cohorts are systematically inflated for genes whose
   trinucleotide context matches the active therapy signature, beyond a uniform burden shift.
3. Excluding (or down-weighting) treatment-signature-high samples measurably changes the pooled
   gene × cancer frequency table and at least one cross-study driver ranking.
4. The inflation co-localises with the hypermutator annotation but is **not** fully captured by it
   (therapy signatures occur below hypermutator thresholds too).

## Falsifiability

- **Refuted** if treatment-exposed cohorts carry no detectable therapy-signature exposure above
  treatment-naive baselines at cBioPortal/panel scale (i.e. the contamination is undetectable in
  practice).
- **Refuted (impact claim)** if down-weighting therapy-signature-high samples leaves the pooled
  frequency tables and driver rankings unchanged within noise — i.e. the effect exists but is
  negligible for the deliverable.

## Alternative Explanations

- **Genuine biology of advanced disease** — treated/metastatic tumors really do carry more drivers;
  the burden difference is real signal, not artefact (adjudicate by context-specificity:
  Prediction 2 separates a signature-shaped inflation from a uniform driver increase).
- **Hypermutator confound** — the effect is just MSI/POLE hypermutators, already handled by the
  existing annotation (adjudicate by Prediction 4).
- **Panel ascertainment** — treated cohorts are panel-sequenced on different gene sets (adjudicate
  with the assay/panel nuisance covariate).

## Status & Next Steps

- **status: proposed.** The H08 MC3 substrate now has explicit treatment-exposure covariates
  (`question:0024`, `task:t181`), but the broader H10 impact test still needs a non-TCGA
  cBioPortal cohort audit. The impact test reuses the existing `create_freq_tables.py` outputs
  (inclusive/exclusive columns already keyed on hypermutator status — a treatment-exposed parallel
  is the natural extension).
- Next: audit treatment-exposed non-TCGA cohorts (`task:t206`), then re-run the frequency tables
  with/without treatment-exposed or therapy-signature-high samples and diff the driver rankings.

## Related

- Hypotheses: `hypothesis:0001-non-tumor-signal-contamination` (contamination lineage),
  `hypothesis:h08-...` (treatment is a named confounder there)
- Topics: `topic:clinical-translational-signatures`, `topic:signatures-hematologic-malignancies`
- Questions: `question:q024-...`
- Tasks: `task:t181`
- Code substrate: `code/scripts/create_freq_tables.py`, the hypermutator/TMB annotation layer
