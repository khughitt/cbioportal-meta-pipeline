---
type: synthesis
title: 'Synthesis: h01-non-tumor-signal-contamination'
status: active
created: '2026-06-02'
updated: '2026-06-02'
report_kind: hypothesis-synthesis
id: synthesis:0005-non-tumor-signal-contamination
hypothesis: hypothesis:0001-non-tumor-signal-contamination
generated_at: 2026-06-02 09:52:22+00:00
source_commit: 037f0ab2d3c84ecc56bebd843e361c1a9dfbfa66
provenance_coverage: thin
---

# Synthesis: Non-tumor signal contaminates cBioPortal mutation-frequency estimates in identifiable, partially correctable ways

## State

The hypothesis proposes that a measurable, non-random fraction of high-frequency genes in
cBioPortal cross-study mutation tables reflects signal from non-tumor cell populations —
clonal hematopoiesis (CH), normal-tissue clonal expansions, tissue-specific somatic background,
and common-fragile-site (CFS) instability — and that these contributions are partially
correctable via reference spectra and study-level overlays already built in the project.

Status is **proposed but untested at the proposition level**. No graph-level or edges-level
evidence has been materialized; the project has not yet run any end-to-end correction analysis
against the hypothesis's core predictions.

The key outstanding questions span three contamination channels. CH leakage is addressed
operationally by the 7-gene Bolton 2020 priority panel, though
question:0006-ch-priority-gene-completeness asks whether that panel is sufficient to capture
residual leakage. Normal-tissue clonal contamination — covering
question:0001-normal-epithelial-clone-contamination-in-esophageal-studies,
question:0002-normal-breast-cna-background-chr1q-chr16q,
question:0004-mca-burden-in-esophageal-vs-other-study-tissues, and
question:0005-gli1-normal-tissue-hotspot-inflation — remains entirely unaddressed by internal
analysis. The null-model questions (question:0007-cross-tissue-somatic-mutation-rate-variation-as-null-model,
question:0008-signature-decomposition-tissue-background-subtraction,
question:0010-cuplr-style-tof-classifier-for-suspect-normal-samples) have infrastructure
available but no results. Question:q014-cfs-as-distinct-confounder-class asks whether CFS loci
constitute a separable confounder class from replication-timing effects more broadly.

One negative result constrains the SBS1 channel: interpretation:0004-t110-sbs1-sbs5-brca-comparison
found no SBS1 excess in the unmatched MSK BRCA cohort relative to matched-normal TCGA MC3 —
the direction was reversed, with matched-normal carrying materially higher SBS1 — ruling out a
simple SBS1/SBS5 ratio as a thresholdable flag for question:0008-signature-decomposition-tissue-background-subtraction. The comparison was further
confounded by assay regime (WES vs panel).

## Arc

Arc reconstruction is limited because only 2 interpretations are available and neither
carries multi-step prior_interpretations chains linking back to an original framing event.

The investigation opened by building reference infrastructure before testing any proposition.
The first documented move, recorded in interpretation:0003-t111-normal-tissue-spectra-pipeline,
was to construct a normal-tissue reference spectra pipeline from the Li 2021 body-map somatic
mutation dataset, yielding 56 per-tissue spectra rows and 47 burden rows. The pipeline
reproduces Li 2021's qualitative tissue-burden ordering (liver highest at 1.19 SNVs/Mb,
pancreas lowest at 0.20 SNVs/Mb, a 6× range). A data-access gate during execution
discovered that Xu 2025 per-variant calls are dbGaP-controlled, reducing the spectra source to
Li 2021 only and filing downstream tasks for atlas expansion (t150, t151). The t111 outputs
unblock question:0007-cross-tissue-somatic-mutation-rate-variation-as-null-model, question:0008-signature-decomposition-tissue-background-subtraction, and question:0010-cuplr-style-tof-classifier-for-suspect-normal-samples at the infrastructure level but
deliberately deferred all analytic correction work; no cBioPortal output has been corrected
against the baseline.

The second documented move, interpretation:0004-t110-sbs1-sbs5-brca-comparison, tested
the simplest contamination proxy — SBS1 excess in unmatched-normal versus matched-normal BRCA
cohorts. The verdict was negative: the SBS1/SBS5 ratio is not supported as an operational
contamination flag on this pair, and the direction of the SBS1 difference contradicts the
simple proxy hypothesis. The comparison also surfaced a chromosome-name normalization bug in
the signature-prep path that had been producing silently empty outputs, and identified the
assay-regime confound (WES vs panel) as an obstacle requiring deliberate cohort matching.

The current epistemic position: reference infrastructure exists, one proxy approach is ruled
out, and the three-channel partition (CH + normal-clone + CFS) defining proposition P2 remains
entirely untested.

## Research Fronts

**Open tasks with direct bearing on h01:**

- task:t127 (blocked, P3) is the designated first quantitative pass for
  question:0008-signature-decomposition-tissue-background-subtraction — per-gene rate
  comparison before and after spectra subtraction using the t111 reference spectra against
  matched (tcga_mc3) vs unmatched (msk_impact_2017) BRCA cohorts. This is the decisive
  supporting test for proposition P1 and is currently the principal blocker.
- task:t114 (proposed, P2) would pre-register the question:0007-cross-tissue-somatic-mutation-rate-variation-as-null-model
  correction impact before rolling it into the frequency pipeline, preventing post-hoc effect
  size tuning.
- task:t150 and task:t151 (proposed, P2) address the Li-2021-only scope limitation of the
  current spectra atlas: t150 audits WGS cohort feasibility; t151 runs a meta-analysis pilot
  on one tractable tissue.
- task:t153 (proposed, P2) would annotate CFS locus overlap and run RT-vs-CFS residual
  regression to test question:0014-cfs-as-distinct-confounder-class.
- task:t161 (proposed, P2) would absorb orphan questions q014, q016, and q017 into the
  hypothesis spine.
- task:t164 (proposed, P2) would draft candidate hypothesis h07 absorbing the
  signature/topography QC path (question:0010-cuplr-style-tof-classifier-for-suspect-normal-samples).
- Blocked external-data tasks task:t166, task:t167, task:t169, task:t172 gate on Hartwig HMF,
  PCAWG/ICGC-25K, GTEx v10, and MC3 controlled-access acquisition respectively; none are on
  the critical path for the P1 test.

**Structural obstacle carried forward:** Panel-sequencing cohorts (MSK-IMPACT and equivalents)
concentrate coverage in early-replicating territory, making any SBS1 late-replication-region
signal structurally unmeasurable on those cohorts. WGS cohort additions would immediately
enable that deferred channel.
