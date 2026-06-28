---
type: synthesis
title: 'Synthesis: joint-indel-sbs-improves-aetiology-discrimination'
status: active
created: '2026-06-02'
updated: '2026-06-02'
id: synthesis:0014-joint-indel-sbs-improves-aetiology-discrimination
report_kind: hypothesis-synthesis
hypothesis: hypothesis:0010-joint-indel-sbs-improves-aetiology-discrimination
generated_at: '2026-06-02T09:52:22Z'
source_commit: 037f0ab2d3c84ecc56bebd843e361c1a9dfbfa66
provenance_coverage: thin
---

## State

`hypothesis:0010-joint-indel-sbs-improves-aetiology-discrimination` is **proposed** with no
experimental results yet. The claim is that jointly decomposing indel (ID) signatures alongside
SBS improves discrimination of ambiguous aetiologies — notably MMR-deficiency versus clock-like
signatures — beyond what SBS alone achieves, but only where indel-call depth is adequate.

The hypothesis identifies three testable predictions: (1) joint SBS+ID assignment on MC3/PCAWG
separates MMRd from clock-like SBS5/SBS40 better than SBS alone; (2) the redefined 89-channel
indel taxonomy improves on COSMIC-83 by reducing unmatched-normal artefacts; (3) the
discrimination gain collapses to near-zero on panel-sequenced studies, quantifying the depth
gate.

The critical prerequisite — which fraction of the cBioPortal/MC3 corpus carries indel calls at
usable depth — is unanswered; `question:0028-indel-call-availability-across-cbioportal-studies`
frames it and is marked active. The associated task `t188` (indel availability census, P3,
proposed) has not yet started. A parallel data-quality question — minimum sample size and
caller provenance for reliable signature decomposition — is partly addressed for SBS by
`question:0020-minimum-sample-size-and-caller-provenance-for`, but whether those thresholds
translate to joint SBS+ID models is not yet established.

## Arc

Arc reconstruction is limited because no interpretations have been filed under this hypothesis
and no `prior_interpretations` chains exist.

The hypothesis was registered on 2026-05-31 (creation dates of `t188` and `t189`) as part of
the `signature-modality-expansion` task group, which arose alongside the hardening of the
`hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and`
SBS decomposition layer. Two foundational tasks for that parent hypothesis — `t178` (COSMIC
reference version-pin and caller-provenance audit, completed 2026-05-31) and `t179`
(per-sample mutation-count floor and de-novo-vs-refit decision rule, completed 2026-05-31) —
established the infrastructure on which any indel extension would depend. The completion of
`t178` and `t179` closed critical data-quality prerequisites for SBS-based decomposition,
creating the preconditions for `hypothesis:0010-joint-indel-sbs-improves-aetiology-discrimination` to become actionable. However, the hypothesis itself remains
entirely in the planning stage: `t188` (indel census) and `t189` (pilot joint SBS+ID on MC3
MMRd vs MSS) are both P3/proposed, and no analysis has been initiated.

## Research Fronts

**Open questions:**

- `question:0028-indel-call-availability-across-cbioportal-studies` — What fraction of
  cBioPortal/MC3 studies carry indel calls at sufficient depth for joint SBS+ID decomposition?
  This is the gating prerequisite for `hypothesis:0010-joint-indel-sbs-improves-aetiology-discrimination` and is currently unresolved.
- `question:0020-minimum-sample-size-and-caller-provenance-for` — Minimum sample-size and
  caller-provenance requirements for signature decomposition; established for SBS but not yet
  extended to joint SBS+ID models.

**Open tasks:**

- `t188` (P3, proposed) — Census indel-call availability across the cBioPortal/MC3 corpus;
  deliverable is a per-study indel-feasibility flag. Directly executes
  `question:0028-indel-call-availability-across-cbioportal-studies`.
- `t189` (P3, proposed) — Pilot joint SBS+ID decomposition on MC3 MMRd vs MSS using the
  redefined indel taxonomy and multimodal catalogue; the cleanest prospective test of
  `hypothesis:0010-joint-indel-sbs-improves-aetiology-discrimination`'s
  primary prediction.

Both tasks are lower priority than ongoing
`hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and` work and are not scheduled until the indel
census (`t188`) first establishes feasibility scope. The main risk is that the joint modality
may be supportable only on MC3 and PCAWG substrates, limiting generalizability to the broader
cBioPortal corpus.
