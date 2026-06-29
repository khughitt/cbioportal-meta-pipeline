---
type: synthesis
title: 'Synthesis: h09-cross-study-signature-exposure-reproducibility'
status: active
created: '2026-06-02'
updated: '2026-06-02'
id: synthesis:0012-cross-study-signature-exposure-reproducibility
report_kind: hypothesis-synthesis
hypothesis: hypothesis:0008-cross-study-signature-exposure-reproducibility
generated_at: '2026-06-02T09:52:22Z'
source_commit: 037f0ab2d3c84ecc56bebd843e361c1a9dfbfa66
provenance_coverage: thin
---

## State

`hypothesis:0008-cross-study-signature-exposure-reproducibility` is **proposed** and untested. No cross-study comparison of per-cancer-type signature-exposure profiles has been performed; there are no interpretation documents and no graph claims to draw on. The claim — that per-cancer-type SBS exposures reproduce across independent cBioPortal/MC3 studies and that divergences track technical batch rather than biology — remains a pre-registered conjecture grounded only in external literature and project design.

The infrastructure prerequisite is partially complete. `t178` pinned the COSMIC SBS reference to v3.4, instituted a per-study caller-consensus flag, and produced a signature-audit sidecar confirming zero positive-control signatures absorbed during `h08` decomposition. `t179` added a per-sample mutation-count floor (383 SBS for WES; 100 for matched-normal), producing `passes_count_floor` columns and a `*.denovo_decision.feather` sidecar. Together these hardened the per-sample exposure layer that `h09` will consume. However, this infrastructure was built for `hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and`; no `h09`-specific analysis has run on it yet.

Key open questions: `question:0026-cancer-types-with-multiple-independent-cbioportal` (which cancer types have adequate multi-study depth for a replication test) and `question:0020-minimum-sample-size-and-caller-provenance-for` (what caller-provenance and sample-size thresholds are defensible). `question:0021-positive-control-signature-set-expansion-sbs9` bears on reference harmonisation before any cross-study comparison can be trusted.

## Arc

Arc reconstruction is limited because no interpretations with `prior_interpretations` chains exist for this hypothesis. The following account is reconstructed solely from task creation dates and task-level notes.

`h09` was registered as a hypothesis at roughly the same time the `h08` signature-decomposition layer was being designed — it is the reproducibility sibling of `hypothesis:0002-cross-study-ranking-divergence-is-structured` (mutation-frequency ranking divergence), asking whether signatures, like gene-frequency ranks, carry a stable cross-study signal. The hypothesis entered `active` phase but immediately sat behind the `h08` engineering work: until per-sample SBS exposures existed for more than one study, no reproducibility comparison was possible.

`task:t178` and `task:t179` (both closed 2026-05-31) hardened the exposure layer for `h08` purposes; the caller-consensus flag and count-floor infrastructure produced by those tasks are exactly the batch covariates `h09`'s predictions invoke. `task:t195` (closed 2026-06-01) ran the first `h08` positive-control scan on MC3, demonstrating that the exposure pipeline delivers coherent signal (SKCM SBS7a+b ~0.83, lung SBS4 0.28–0.36 per `task:t197` completion note) — an indirect existence proof that per-study exposures are meaningful. `task:t212` (proposed 2026-06-01) is the first task scoped explicitly to `h09`: a cross-study exposure reproducibility pass using the on-disk per-sample SBS assignments. As of this synthesis, `task:t212` has not been executed.

The current epistemic position is: infrastructure ready, analysis not yet run, hypothesis untested.

## Research Fronts

**Open tasks:**

- `t212` (proposed, P2) — first concrete `h09` analysis: compare per-cancer-type SBS exposure profiles across independent cBioPortal studies, quantify divergence, and attribute to technical vs biological covariates using the t178/t179 provenance flags.
- `t183` (proposed, P3) — adds ERCC2 somatic-mutation status as a bladder/urothelial positive-control covariate for SBS5; while scoped under `h08`, any confirmed SBS5 batch signal there would directly bear on `h09` prediction 4 (artefact-prone flat signatures account for disproportionate cross-study disagreement).

**Live questions:**

- `question:0026-cancer-types-with-multiple-independent-cbioportal` — census of which cancer types have >=2 independent studies at adequate caller/assay depth; this directly gates which types are admissible into the `h09` replication analysis.
- `question:0020-minimum-sample-size-and-caller-provenance-for` — the defensible per-cancer-type sample-size floor and caller-consensus threshold that must be satisfied before a cross-study comparison is meaningful.
- `question:0021-positive-control-signature-set-expansion-sbs9` — COSMIC-version harmonisation and SBS9/SBS54 adjudication are prerequisites for cross-study comparison, because mismatched reference versions are one of `h09`'s named alternative explanations for apparent divergence.

No knowledge gaps (topic_gaps) were provided in the bundle for this hypothesis.
