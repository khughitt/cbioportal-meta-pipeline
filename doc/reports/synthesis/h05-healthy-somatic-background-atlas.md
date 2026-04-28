---
id: "synthesis:h05-healthy-somatic-background-atlas"
type: "synthesis"
report_kind: "hypothesis-synthesis"
hypothesis: "hypothesis:h05-healthy-somatic-background-atlas"
generated_at: "2026-04-28T03:09:06Z"
source_commit: "c1c6b1f29eef8326e3efde948df540ecc23c95ed"
provenance_coverage: "thin"
---

## State

hypothesis:h05-healthy-somatic-background-atlas is in `phase: candidate` with `status: proposed`. No empirical tests have been run inside this project; all supporting evidence is external-literature-grounded.

The hypothesis carries three core propositions. P1 — cross-tissue healthy somatic-mutation rates span more than two orders of magnitude and scale with tissue stem-cell turnover — is inferred from published single-tissue normal sequencing studies (Martincorena 2018, Lee-Six 2018, Li 2021 referenced in the hypothesis spec). P2 — driver-mutation-positive clonal expansions in apparently-healthy individuals at age 70+ exceed the per-tissue cancer-discovery rate for at least three tissues — is suggestive from the esophageal and colon normal-tissue literature cited in the spec, but has not been formally tested by this project. P3 — the project-actionable claim — holds that substituting a meta-analyzed cross-tissue normal null for the current within-pipeline null will produce calibrated, tissue-specific shifts in apparent driver frequency in unmatched-normal cBioPortal studies; this remains untested.

The primary gating risk is data harmonization: available normal-tissue WGS cohorts differ in sequencing depth, caller, age range, and dissection protocol. Task task:t150 (feasibility audit, proposed) is the formal gate — its output will determine whether promotion to `phase: active` is warranted. question:q007-cross-tissue-somatic-mutation-rate-variation-as-null-model is the most directly adjacent resolved question; the Li 2021 body-map is the closest existing cross-tissue reference identified by this project.

## Arc

Arc reconstruction is limited because no interpretations directly cite hypothesis:h05-healthy-somatic-background-atlas, and both tasks (task:t150 and task:t151) are in `status: proposed` with no commits yet recorded.

hypothesis:h05-healthy-somatic-background-atlas was formalized on 2026-04-27 as a generalization of hypothesis:h01-non-tumor-signal-contamination. Where h01 targets within-sample contamination correction, h05 frames "background" as positive cross-population knowledge: a cross-tissue atlas of healthy somatic-mutation rates that can replace the project's current within-pipeline null. This framing was motivated by the body of single-tissue normal sequencing literature already cataloged under question:q007-cross-tissue-somatic-mutation-rate-variation-as-null-model, particularly the Li 2021 body-map across nine tissues.

Two tasks were filed concurrently with hypothesis creation. task:t150 (P2, proposed) is the gating step: enumerate available normal-tissue WGS cohorts, assess coverage across cBioPortal cancer types, and decide between a uniform-subset and a random-effects meta-analytic regime. task:t151 (P3, proposed) is the scoped pilot that follows: apply an age-stratified esophageal or colon normal background as an alternative null in the h01 contamination test and report whether it outperforms the current null. Neither task has been executed; the hypothesis is entirely pre-empirical at this writing.

The current epistemic position is: literature-grounded plausibility, one adjacent infrastructure build (t111 spectra extraction pipeline, grounded in Li 2021 and resolving question:q007-cross-tissue-somatic-mutation-rate-variation-as-null-model partially), and no project-internal hypothesis test yet conducted.

## Research Fronts

**Open tasks.**

- task:t150 (P2, proposed): normal-tissue WGS cohort feasibility audit. This is the formal promotion gate for hypothesis:h05-healthy-somatic-background-atlas. Deliverable: a cohort table with promotion recommendation.
- task:t151 (P3, proposed, blocked on task:t150): scoped meta-analysis pilot on one tractable tissue (esophagus or colon). Deliverable: one tissue-specific interpretation with effect size and scale-up recommendation.

**Live questions.**

- question:q007-cross-tissue-somatic-mutation-rate-variation-as-null-model is partially addressed at the infrastructure level (Li 2021 spectra extraction delivered, per-tissue burden table exists) but the correction has not been applied to cBioPortal outputs. The question of whether the empirical Li 2021 normal null discriminates from a simpler dN/dS-based null (Martincorena 2017) is unresolved and noted as a pre-registration requirement before the correction is rolled out.

**Key uncertainties.** Cohort heterogeneity is the dominant methodological barrier: depth, caller, age range, and dissection protocol vary across all published single-tissue studies. Several cBioPortal-relevant cancer-type contexts (kidney, thyroid, pancreas) have thin or absent normal-mutation reference data, which limits how broadly P1's >2-OoM claim can be tested. P2's "clone prevalence exceeds cancer rate" comparison is also sensitive to normalization: biopsy-level clonal coverage and population-level cancer incidence require explicit modeling to compare on a common axis.

**Knowledge gaps.** No `topic_gaps` data was provided in the bundle for this hypothesis.
