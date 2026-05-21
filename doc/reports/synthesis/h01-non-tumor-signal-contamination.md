---
id: "synthesis:h01-non-tumor-signal-contamination"
type: "synthesis"
title: "Non-tumor signal contaminates cBioPortal mutation-frequency estimates"
report_kind: "hypothesis-synthesis"
hypothesis: "hypothesis:h01-non-tumor-signal-contamination"
generated_at: "2026-04-28T03:09:06Z"
source_commit: "c1c6b1f29eef8326e3efde948df540ecc23c95ed"
provenance_coverage: partial
---

# Synthesis: Non-tumor signal contaminates cBioPortal mutation-frequency estimates in identifiable, partially correctable ways

## State

The hypothesis asserts that a measurable fraction of high-frequency genes in cBioPortal and AACR GENIE cross-study tables reflects mutational processes operating in non-tumor cell populations — clonal hematopoiesis (CH), normal-tissue clonal expansions, and common-fragile-site instability — and that these contributions are tissue-, gene-, and study-design-specific, hence partially correctable.

The claim rests on three partitioned propositions. **P1 (presence):** elevated per-gene mutation rates in unmatched-normal studies should concentrate on CH gene sets (Bolton 2020 7-gene panel) and tissue-specific normal-clone loci (NOTCH1 in esophagus, per question:q001-normal-epithelial-clone-contamination-in-esophageal-studies). No internal project analysis has yet tested P1 numerically; the matched-vs-unmatched BRCA pilot from interpretation:2026-04-22-t110-sbs1-sbs5-brca-comparison explicitly returned a negative result on the SBS1/SBS5 ratio, meaning SBS1 excess in the unmatched cohort is not supported on that pair. **P2 (mechanism partition):** three contamination channels (CH leakage, normal-tissue clonal contamination, CFS loci) are asserted distinguishable. This partition is structurally motivated but empirically untested within the project. **P3 (correctability):** per-tissue background subtraction using reference spectra built by task:t111 and CH-priority annotations from task:t087 is proposed as the correction route, but no subtraction pass has been run yet (question:q008-signature-decomposition-tissue-background-subtraction; task:t127 is the planned first quantitative pass). The SBS1 late-replication-region bias route (question:q007-cross-tissue-somatic-mutation-rate-variation-as-null-model) was deferred due to structural panel-coverage limitations documented in interpretation:2026-04-24-t126-sbs1-lrr-bias-per-study.

Current epistemic status: **proposed / under-tested**. Infrastructure is in place; decisive evidence has not been produced.

## Arc

The investigation opened with literature-grounded framing. Question:q001-normal-epithelial-clone-contamination-in-esophageal-studies assembled the Martincorena 2018 evidence that NOTCH1-mutant clones colonize 30–80% of normal esophageal epithelium in middle-aged donors, exceeding ESCC NOTCH1 tumor rates — a direct contamination risk for unmatched esophageal studies. Question:q007-cross-tissue-somatic-mutation-rate-variation-as-null-model and question:q008-signature-decomposition-tissue-background-subtraction established the mechanistic framing around SBS1/SBS5 as the dominant normal-tissue signal and per-tissue background subtraction as the proposed intervention.

The first major investigative move was infrastructure: interpretation:2026-04-19-t111-normal-tissue-spectra-pipeline delivered a validated pipeline extracting 56 per-tissue reference spectra from Li 2021, reproducing the expected tissue-burden ordering (liver highest, pancreas lowest, 6x range). This unblocked q007, q008, and question:q010-cuplr-style-tof-classifier-for-suspect-normal-samples without itself testing any proposition. Scope was reduced to Li 2021 only after a data-access gate revealed Xu 2025 per-variant calls are dbGaP-controlled; task:t112 was filed to add blood-tissue coverage (Lee-Six 2018) as the next source.

The second move was empirical hypothesis testing on the BRCA matched-vs-unmatched pair. Interpretation:2026-04-22-t110-sbs1-sbs5-brca-comparison returned a negative verdict: TCGA MC3 (matched, WES) showed materially higher SBS1 than MSK-IMPACT-2017 (unmatched, panel), the opposite of the contamination-proxy hypothesis, with the comparison confounded by assay regime (WES vs panel). The gene-level replication-timing pilot (interpretation:2026-04-22-t122-rt-brca-pilot) produced a suggestive but coverage-confounded relative late-replication enrichment in the unmatched cohort. The SBS1-proxy CpG-subset version (interpretation:2026-04-22-t123-rt-brca-sbs1-proxy-pilot) collapsed under panel sparsity — 96% of MSK-IMPACT constitutive-bin coverage lies in early-replicating territory, making the SBS1 LRR-bias signal structurally unmeasurable on this cohort.

Interpretation:2026-04-24-t126-sbs1-lrr-bias-per-study formalized this structural barrier with a pre-registered power analysis, triggering a `defer` verdict: both panel safety gates (n_sbs1_pooled = 176 vs floor 500; CI half-width = 0.194 vs ceiling 0.10) fired. Question:q009 was moved to deferred pending WGS input. The project is now positioned at the boundary between infrastructure readiness and the first genuine contamination-magnitude estimate, with task:t127 (q008 quantitative pass) and task:t151 (esophagus/colon normal background pilot, linked to h01 via hypothesis:h01-non-tumor-signal-contamination) as the next decisive moves.

## Research fronts

**Live questions under h01:**

- question:q001-normal-epithelial-clone-contamination-in-esophageal-studies — no internal NOTCH1 rate comparison across esophageal studies has been run; blocked on tumor-purity metadata and matched-vs-unmatched study stratification.
- question:q007-cross-tissue-somatic-mutation-rate-variation-as-null-model — null-model table exists (task:t111 output); pre-registration of the correction impact is required before rolling it into the frequency pipeline (task:t114).
- question:q008-signature-decomposition-tissue-background-subtraction — first quantitative pass planned in task:t127 using t111 reference spectra against tcga_mc3 vs msk_impact_2017; no result yet.
- question:q010-cuplr-style-tof-classifier-for-suspect-normal-samples — reference spectra available; cosine-similarity classifier analysis not run.

**Open tasks with direct h01 bearing:**

- task:t087 — graded ch_contamination_prob column to replace uniform boolean; required for CH-channel correction.
- task:t112 — add Lee-Six 2018 blood spectra as second normal-tissue source; required for CH-locus background subtraction.
- task:t114 — pre-register q007 null-model correction impact.
- task:t127 — first q008 quantitative contamination-magnitude estimate.
- task:t151 — normal-tissue background meta-analysis pilot on esophagus or colon, directly testing q001 NOTCH1 prediction.
- task:t153 — CFS overlap annotation and RT-vs-CFS residual regression; tests whether CFS loci form a distinct third correction channel as claimed in P2.

**Structural obstacle carried forward:** Panel sequencing cohorts (MSK-IMPACT and equivalents) are structurally underpowered for the SBS1 LRR-bias route because driver-gene panels concentrate coverage in early-replicating territory. Any WGS-based cohort addition (Hartwig HMF, PCAWG follow-ons) would immediately enable the deferred q009 test with no code changes (interpretation:2026-04-24-t126-sbs1-lrr-bias-per-study).

**Knowledge gaps:** No claim-level graph evidence exists yet for this hypothesis; topic_gaps are empty pending first materialization of the proposition graph.
