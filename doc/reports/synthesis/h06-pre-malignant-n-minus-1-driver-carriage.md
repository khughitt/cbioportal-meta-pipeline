---
id: "synthesis:h06-pre-malignant-n-minus-1-driver-carriage"
type: "synthesis"
report_kind: "hypothesis-synthesis"
hypothesis: "hypothesis:h06-pre-malignant-n-minus-1-driver-carriage"
generated_at: "2026-04-28T03:09:06Z"
source_commit: "c1c6b1f29eef8326e3efde948df540ecc23c95ed"
provenance_coverage: thin
---

# Synthesis: Pre-malignant n-1 driver carriage (h06)

## State

Hypothesis hypothesis:h06-pre-malignant-n-minus-1-driver-carriage is at `phase: candidate` with `status: proposed`. No interpretations are bound and no `.edges.yaml` edges exist; the state below is drawn entirely from hypothesis frontmatter and proposition text.

The organizing conjecture is that cBioPortal pre-malignant cohorts — Barrett's esophagus, MGUS/SMM, MDS, IPMN, ASAP/HGPIN, colorectal adenomas, and cervical CIN — already carry most canonical invasive-cancer drivers of the same lineage (proposition P1: top-25 driver-frequency overlap of ≥20 genes), that the residual "late-stage" set is small (median ≤5 per cancer type) and enriched for checkpoint and chromatin genes such as TP53, RB1, CDKN2A, ARID1A, and KMT2D (P2), and that shared drivers appear at pre-malignant frequencies within a twofold band of invasive-cancer frequencies, indicating clonal establishment rather than sub-clonal leakage (P3).

Supporting literature cited in the hypothesis spec — paper:Martincorena2018 (normal tissue harbors driver-positive clones at high prevalence) and paper:LeeSix2018 (colon-crypt phylogenies show gradual, cumulative driver acquisition) — provides a prior consistent with P1, but neither source was analyzed against cBioPortal data. No cBioPortal study audit has yet been performed (task:t156 is open, not started). The primary epistemic blocker is that pre-malignant coverage in cBioPortal is not systematically catalogued and is likely patchy; the hypothesis cannot be tested until task:t156 resolves which cancer types have sufficient pre-malignant cohorts.

## Arc

Arc reconstruction is limited because no interpretations are linked and task:t156 and task:t157 are both open and unstarted; there is no execution history to narrate.

Hypothesis hypothesis:h06-pre-malignant-n-minus-1-driver-carriage was formalized on 2026-04-27 as a complement to the sibling hypothesis h04 (MHN-inferred ordering on cross-sectional invasive data), which shares question:q012-mutation-ordering-cross-sectional-inference as a non-primary link. The framing distinguishes h06 from h04 on operational grounds: where h04 requires cross-sectional probabilistic inference, h06 uses directly observed pre-malignant versus invasive sequencing data, making it a cleaner empirical test where data exist. This distinction motivated the creation of two gating tasks. task:t156 (cBioPortal pre-malignant cohort audit) was registered as the blocking prerequisite — its acceptance criterion is an audit document enumerating study pairs, sub-stage labels, sample sizes, assay regimes, and matched-normal status. task:t157 (first paired driver-overlap analysis) was registered as the first substantive analysis, contingent on task:t156, with Barrett's esophagus to EAC and MDS to AML identified as the most tractable candidate pairs. Neither task has started. The hypothesis therefore sits at the boundary between ideation and the beginning of operationalization, with promotion to `phase: active` gated on task:t156 completing and at least three paired cohorts passing the n ≥ 30 sample-size threshold.

## Research Fronts

**Open tasks:**

- task:t156 — cBioPortal pre-malignant cohort audit. Gating task. Enumerates study pairs, sub-stages, n_pre_malignant, n_invasive, assay regime, and modality coverage. Not started.
- task:t157 — First paired driver-overlap analysis. Blocked on task:t156. Planned scope: mutation-observable top-25 driver overlap, late-stage residual identification, checkpoint/chromatin enrichment test on the most tractable pair (Barrett's → EAC or MDS → AML).

**Live questions under this hypothesis:**

- question:q012-mutation-ordering-cross-sectional-inference is linked as a non-primary question (primary association is h04). The relevance to h06 is indirect: if pre-malignant cBioPortal cohorts have low or absent VAF data, ordering inferences must fall back to cross-sectional population-level methods that q012 frames.

**Key uncertainties from hypothesis spec:**

- Pre-malignant cBioPortal coverage is patchy and uncharacterized. If task:t156 finds fewer than three cancer types with n ≥ 30 pre-malignant samples, P1 is likely untestable within the current pipeline scope.
- Assay regime mismatch (panel vs WES) between pre-malignant and invasive cohorts within the same lineage must be controlled; the current pipeline does not have callability-matching logic for paired-cohort comparisons.
- Modality restriction: the pipeline is somatic-SNV/indel-only. CNA-driven events (IgH rearrangements in MGUS/MM; chromosomal instability in Barrett's) are invisible, potentially causing systematic underestimation of pre-malignant driver burden for lineages where CNAs are primary.
- Sub-stage heterogeneity (Barrett's with vs without dysplasia; MGUS vs SMM; low-risk vs high-risk MDS) may collapse signal if cohorts are not sub-stratified.

**Knowledge gaps:** No topic_gaps data was included in this bundle.
