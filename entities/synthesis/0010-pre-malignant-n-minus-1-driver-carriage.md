---
type: synthesis
title: 'Synthesis: h06-pre-malignant-n-minus-1-driver-carriage'
status: active
created: '2026-06-02'
updated: '2026-06-02'
report_kind: hypothesis-synthesis
id: synthesis:0010-pre-malignant-n-minus-1-driver-carriage
hypothesis: hypothesis:0006-pre-malignant-n-minus-1-driver-carriage
generated_at: 2026-06-02 09:52:22+00:00
source_commit: 037f0ab2d3c84ecc56bebd843e361c1a9dfbfa66
provenance_coverage: thin
---

## State

`hypothesis:0006-pre-malignant-n-minus-1-driver-carriage` is in `phase: candidate`. No
analysis has been run and no interpretations exist; the current epistemic position rests
entirely on the hypothesis specification and its supporting literature framing.

The organizing conjecture is that cBioPortal pre-malignant cohorts — Barrett's esophagus,
MGUS/SMM, MDS, IPMN, ASAP/HGPIN, colorectal adenomas, and cervical CIN — already carry
most canonical invasive-cancer drivers of the same lineage. Three falsifiable propositions
structure the claim: P1 (≥80% top-25 driver overlap between pre-malignant and invasive
cohorts of the same lineage), P2 (residual "late-stage" set ≤5 genes per cancer type,
enriched for checkpoint and chromatin genes such as TP53, RB1, CDKN2A, and ARID1A), and P3
(shared-driver frequency within a 2× band between stages, indicating clonal establishment
rather than sub-clonal leakage).

Supporting literature cited in the hypothesis spec — `paper:Martincorena2018` (normal tissue
harbors driver-positive clones at high prevalence) and `paper:LeeSix2018` (colon-crypt
phylogenies show gradual, cumulative driver acquisition) — provides a prior consistent with
P1, but neither source was analyzed against cBioPortal data. No pre-malignant cohort audit
has yet been performed (`t156` is open, not started). The primary epistemic blocker is that
pre-malignant coverage in cBioPortal is not systematically catalogued; the hypothesis cannot
be tested until `t156` resolves which cancer types have sufficient pre-malignant samples.
The inverse question `question:0012-mutation-ordering-cross-sectional-inference` flags a
complementary limitation: if pre-malignant coverage proves insufficient, ordering biology
would need to be inferred from cross-sectional invasive data instead, carrying its own
methodological constraints.

## Arc

Arc reconstruction is limited because no interpretations are linked to this hypothesis; `t156`
and `t157` are both open and unstarted with no execution history to narrate.

`hypothesis:0006-pre-malignant-n-minus-1-driver-carriage` was formalized on 2026-04-27/28
as a complement to the sibling hypothesis `hypothesis:0004-mhn-pathway-ordering`, which
shares `question:0012-mutation-ordering-cross-sectional-inference` as a non-primary link.
The framing distinguishes h06 from h04 on operational grounds: where h04 requires
cross-sectional probabilistic inference, h06 uses directly observed pre-malignant versus
invasive sequencing data — a cleaner empirical test where paired cohorts exist. This
distinction motivated the creation of two gating tasks. `t156` (cBioPortal pre-malignant
cohort audit) was registered as the blocking prerequisite, with its acceptance criterion
being an audit document enumerating study pairs, sub-stage labels, sample sizes, assay
regimes, and matched-normal status. `t157` (first paired driver-overlap analysis) was
registered as the first substantive analysis, contingent on `t156`, with Barrett's
esophagus → EAC and MDS → AML identified as the most tractable candidate pairs.

The broader mutation-ordering scaffolding — `t132` (literature review of ordering methods),
`t135` (MHN fit per histology), and `t152` (MHN simulation calibration) — was filed
concurrently as part of the h04/h06 ordering work cluster. These tasks provide a fallback
inference path if h06's direct-observation route is blocked by insufficient pre-malignant
sample coverage. Neither gating task has started; the hypothesis sits at the boundary
between ideation and operationalization.

## Research Fronts

**Open tasks:**

- `t156` (P2, proposed) — cBioPortal pre-malignant cohort audit. Gating task for h06.
  Enumerates studies with pre-malignant samples, records sub-stage labels, sample sizes,
  assay regime, matched-normal status, and modality availability. Acceptance criterion is
  a promotion recommendation for h06.
- `t157` (P3, proposed, blocked on `t156`) — First paired driver-overlap analysis on the
  most tractable cancer type (likely Barrett's → EAC or MDS → AML). Computes
  mutation-observable top-25 driver overlap, identifies late-stage residual, and tests
  checkpoint/chromatin enrichment. Restricted to SNV/indels unless CNA modalities are
  explicitly added.
- `t132` (P2, proposed) — Literature search on mutation-ordering methods. Relevant as
  fallback if h06's direct paired-cohort route is blocked by insufficient pre-malignant
  coverage, directing work toward cross-sectional inference under
  `question:0012-mutation-ordering-cross-sectional-inference`.
- `t135` (P3, proposed) — MHN fit per histology; provides inferred-ordering results for
  cross-comparison once h06 direct-observation results exist.
- `t152` (P2, proposed) — MHN simulation calibration; assesses viability of population-
  level ordering inference where pre-malignant cohorts are absent.
- `t167` (P3, blocked) — PCAWG/ICGC-25K WGS cohort acquisition; would provide an
  independent chronology benchmark (Gerstung 2020) for validating any h06 late-stage
  driver claims.

**Key uncertainties:** Pre-malignant cBioPortal coverage is patchy and uncharacterized —
if `t156` finds fewer than three cancer types with n ≥ 30 pre-malignant samples, P1 is
likely untestable within the current pipeline scope. Assay-regime mismatch (panel vs WES)
between pre-malignant and invasive cohorts must be controlled; the pipeline lacks
callability-matching logic for paired-cohort comparisons. The pipeline is somatic-SNV/indel-
only, making CNA-driven events (IgH rearrangements in plasma-cell disorders; chromosomal
instability in Barrett's) invisible and potentially causing systematic underestimation of
pre-malignant driver burden. Sub-stage heterogeneity (Barrett's with vs without dysplasia;
MGUS vs SMM; low-risk vs high-risk MDS) may collapse signal if cohorts are not
sub-stratified.

**Knowledge gaps:** No `topic_gaps` were present in the bundle.
