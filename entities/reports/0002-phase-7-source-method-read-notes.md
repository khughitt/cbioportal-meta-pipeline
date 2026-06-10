---
type: report
title: Phase 7 source-method read notes for trajectory inference
status: active
created: '2026-05-02'
updated: '2026-05-02'
id: report:0002-phase-7-source-method-read-notes
ontology_terms:
- cBioPortal
- cross-sectional inference
- mutation ordering
source_refs:
- hypothesis:0004-mhn-pathway-ordering
- question:0012-mutation-ordering-cross-sectional-inference
related:
- hypothesis:0004-mhn-pathway-ordering
- question:0012-mutation-ordering-cross-sectional-inference
---

# Phase 7 source-method read notes for trajectory inference

## Summary

This report records the cBioPortal-owned Phase 7 read notes for source-method limits
on trajectory inference from cross-sectional mutation data. It supports meta Q2 by
separating biological trajectory claims from what cBioPortal-style data can defend.

The two candidate anchors converge on the same method boundary: cBioPortal and GENIE
diagnostic cohorts may support recurrent, benchmarked, per-histology ordering signals,
especially at the pathway level, but they do not directly observe temporal acquisition.
Any export to meta should therefore be framed as method-qualified trajectory evidence,
not as a standalone biological chronology.

## Candidate Notes

### `phase6:c018` - H04 MHN pathway-ordering hypothesis

#### Source

`hypothesis:0004-mhn-pathway-ordering` proposes that Mutual Hazard Networks (MHN),
especially the Schill 2024 observation-event extension and the Vocht 2026 Python
implementation, can recover interpretable pathway-level ordering from cross-sectional
cBioPortal / GENIE mutation states.

#### Target Questions

- Can Sanchez-Vega pathway-level MHN fits recover an intrinsic-mutator to
  lineage-driver to checkpoint-loss pattern within individual histologies?
- Can gene-level drill-downs recover benchmark orderings such as APC to KRAS to TP53
  in colorectal cancer, STK11 to KEAP1 in LUAD, BRAF to TERT in thyroid cancer, and
  TP53 / PIK3CA relationships in breast cancer?
- Does the observation-event MHN formulation improve agreement with PCAWG chronology
  relative to the older cMHN model?

#### Evidence Levels

- Proposed biological-method hypothesis, not yet promoted to active.
- Current evidence is mostly method plausibility and external benchmark alignment:
  MHN has prior TCGA validation, PCAWG provides independent chronology, Sanchez-Vega
  pathway aggregation is already available, and Vocht 2026 demonstrates tractability
  on 3,662 GENIE LUAD samples.
- The hypothesis requires local validation before export as recurrent trajectory
  evidence: VAF audit, primary-method check, and synthetic calibration are explicit
  promotion gates.

#### Phase 7 Status

Keep as a source-method candidate for Phase 7. It is useful for defining what
cBioPortal can test, but the anchor should not be used as completed evidence that the
intrinsic-mutator to lineage-driver to checkpoint-loss trajectory has been recovered
in this federation.

#### Key Evidence

- H04 defines the primary endpoint as inferred edge direction or path position, not
  marginal mutation frequency, because rare early events can have low prevalence.
- The proposed strongest signal is pathway-level, per-histology ordering; gene-level
  ordering is a secondary drill-down expected to be less stable because of power and
  panel coverage.
- Promotion requires an audit of VAF availability, confirmation that Schill 2024's
  observation-event correction is usable for diagnostic cBioPortal cohorts with
  panel-specific missingness, and simulation calibration recovering at least 70% of
  injected pathway-level edges.
- Falsification criteria are operational: unstable bootstrap or leave-one-study-out
  edge sets, failed synthetic recovery, or poor agreement with PCAWG-overlapping
  cancer-type chronologies would block biological interpretation.

#### Supports

- Supports using cBioPortal-style mutation data as a source of method-qualified,
  recurrent trajectory comparisons when analyses are per-histology, callability-aware,
  and benchmarked against independent chronology.
- Supports treating pathway aggregation as the preferred Phase 7 comparison level,
  because it is expected to absorb some panel heterogeneity and improve power.
- Supports distinguishing intrinsic mutators such as MMR, POLE, and POLD1 from
  checkpoint or expansion-permissive genes such as TP53 and RB1.

#### Limits

- H04 is still proposed and explicitly gated; it does not yet provide validated
  cBioPortal-derived ordering results.
- Cross-sectional ordering remains under-identified without model assumptions such as
  no reversal and approximately stable hazards.
- Diagnostic ascertainment is a collider unless explicitly modeled; cMHN-only edges
  are not sufficient as biological chronology evidence.
- Panel heterogeneity means absence from a panel is not wild type, so per-sample
  callability conditioning is required.

#### Exportable Comparison Points

- Meta may compare whether cBioPortal-derived analyses, once calibrated, repeatedly
  place intrinsic-mutator pathway events upstream of checkpoint-loss pathway events
  within specific histologies.
- Meta may use H04 to justify a pathway-first comparison axis for trajectory evidence,
  with gene-level examples treated as drill-downs rather than primary cross-project
  claims.
- Meta may cite H04's promotion criteria as the required evidentiary threshold for
  moving from plausible ordering inference to trajectory support.

#### Follow-Up Reads

- Schill 2024 primary method details for the observation-event extension and its
  treatment of genotype-dependent ascertainment.
- Vocht 2026 package and GENIE LUAD demonstration, especially reproducibility of the
  top trajectories under this project's data processing.
- PCAWG Gerstung 2020 chronology tables for benchmark orderings in overlapping
  histologies.
- Sanchez-Vega 2018 pathway annotation details for the 10-pathway aggregation layer.

### `phase6:c019` - Q012 cross-sectional mutation-ordering inference

#### Source

`question:0012-mutation-ordering-cross-sectional-inference` asks whether directed
A-to-B mutation ordering can be robustly inferred from cBioPortal and GENIE
single-biopsy diagnostic snapshots.

#### Target Questions

- What can cBioPortal-style cross-sectional mutation data support about event order,
  given that the observed data are mutation states rather than acquisition times?
- Which method requirements must be met before a directional edge is interpreted as
  trajectory evidence?
- Which confounders make naive frequency or co-occurrence asymmetries unsafe?

#### Evidence Levels

- Active method question defining constraints for downstream trajectory claims.
- Strong support for method availability: MHN, CBN, CAPRI / TRONCO, REVOLVER, and
  PCAWG benchmarks provide candidate frameworks and external validation targets.
- Strong caution against naive inference: cross-sectional inequalities can reflect
  true order, fitness asymmetry, ascertainment, contamination, panel missingness, or
  cancer-type mixture.

#### Phase 7 Status

Use as the primary cBioPortal guardrail for Phase 7 exports. Q012 permits
method-qualified discussion of ordering signals only after observation-event modeling,
per-histology analysis, callability correction, contamination control, and benchmark
calibration.

#### Key Evidence

- cBioPortal / GENIE samples are mostly single-biopsy snapshots at diagnosis; they
  observe mutation presence, not acquisition order.
- Schill 2024's observation-event formulation is identified as the minimum viable MHN
  approach for diagnostic cohorts because observation at diagnosis is genotype
  dependent.
- The anchor lists major confounders: collider bias, clonal hematopoiesis
  contamination, normal-tissue contamination, panel heterogeneity, cancer-type pooling,
  signature-coupled TMB, and hypermutator status.
- Q012 recommends reporting pathway-level results first, retaining gene-level results
  as drill-down, and calibrating against PCAWG plus the Vocht 2026 GENIE LUAD demo.

#### Supports

- Supports cBioPortal as a source for recurrent directional association hypotheses
  when the analysis is explicit about the model and the benchmark.
- Supports pairing ordering analyses with co-occurrence infrastructure from `t078`,
  especially per-sample callability masks and sample-specific background-rate nulls.
- Supports VAF-aware work as a second route where available, but does not make VAF
  availability a prerequisite for all population-level binary-state analyses.

#### Limits

- Q012 does not allow cross-sectional frequency asymmetry to be treated as direct
  temporal evidence.
- It rejects cancer-type pooled ordering claims because Simpson's-paradox artifacts
  can create misleading directions.
- It requires stratification or correction for hypermutator status, mutational
  signatures, clonal hematopoiesis, normal-tissue contamination, and panel coverage
  before interpreting edges.
- If VAF is sparse and MHN calibration fails under the project's panel and cohort
  composition, the project should not pursue the ordering claim from this source.

#### Exportable Comparison Points

- Meta may state that cBioPortal-style data can contribute directional trajectory
  evidence only as model-inferred ordering from cross-sectional snapshots.
- Meta may use Q012 to separate symmetric co-occurrence evidence from directed
  ordering evidence.
- Meta may compare cBioPortal-derived ordering signals against PCAWG-style chronology
  rather than presenting them as independently observed timelines.

#### Follow-Up Reads

- Schill 2020 and Schill 2024 for MHN assumptions, observation-event correction, and
  collider-bias treatment.
- Vocht 2026 for practical implementation and the GENIE LUAD demonstration.
- Beerenwinkel 2007, Caravagna 2016, and Caravagna 2018 for alternative CBN, CAPRI /
  TRONCO, and REVOLVER ordering approaches.
- Project notes on `t078`, `t081`, `t087`, and `t111` for callability, hypermutator,
  contamination, and signature requirements.

## cBioPortal Export To Meta

- Meta may use cBioPortal-style sources as method-qualified evidence for recurrent
  trajectory patterns when ordering is inferred per histology and benchmarked against
  independent chronology.
- Meta may safely distinguish pathway-level trajectory comparisons from gene-level
  drill-downs, with pathway-level results treated as the more stable export layer.
- Meta may describe observation-event MHN as the preferred cBioPortal ordering frame
  for diagnostic cohorts because it addresses genotype-dependent observation.
- Meta may use cBioPortal guardrails to flag whether a trajectory claim is supported
  by callability-aware, contamination-aware, and hypermutator-aware analysis.
- Meta may compare candidate ordering signals to PCAWG and Vocht GENIE LUAD benchmarks
  as validation targets rather than as completed local results.

## Source-Method Guardrails

- Do not infer acquisition time directly from mutation prevalence, co-occurrence, or
  A-alone / B-alone asymmetry in cross-sectional data.
- Do not export cMHN-only or uncorrected directional edges as biological chronology
  evidence for diagnostic cohorts.
- Do not pool histologies for ordering claims without a specific analysis showing that
  mixture artifacts are controlled.
- Do not treat uncalled genes as wild type; panel-specific callability must be part of
  any ordering analysis.
- Do not interpret TP53 or other checkpoint events as generic early repair events
  without separating intrinsic-mutator biology from checkpoint-loss biology.
- Do not claim Phase 7 biological trajectory evidence from cBioPortal until the relevant
  VAF audit, observation-event method check, and calibration requirements have been
  resolved for the analysis being cited.
