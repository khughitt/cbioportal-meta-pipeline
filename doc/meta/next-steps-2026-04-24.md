---
id: "meta:next-steps-2026-04-24"
type: "meta"
title: "Next Steps and Gap Analysis (2026-04-24)"
status: "active"
created: "2026-04-24"
updated: "2026-04-24"
---

# Next Steps — 2026-04-24

## Recent Progress

- **The main cross-study aggregation spine closed out.** `t076` (NaN-vs-0 panel-aware denominator hygiene) and the full `t077` chain (`t101`, `t115`–`t120`) all landed on 2026-04-22. The consumer-facing ratio table now carries pooled meta-analysis columns (`pooled_*_{inclusive,exclusive}`, `k_studies_*`, `status_*`) joined from a real `metafor::rma.glmm(PLO)` fit with REML fallback, diagnostics, and leave-one-out sensitivity.
- **Backlog hygiene caught up to reality.** Every stale task flagged in the 2026-04-22 analysis (`t026`, `t043`, `t060`, `t070`, `t077`) is now closed or correctly restated. Active task count dropped from 35 → 27, with only one P1 remaining.
- **Signature-decomposition branch produced first decisive results.** `t109` (cancer-type signature restriction for SigProfilerAssignment) and `t110` (BRCA SBS1/SBS5 matched-vs-unmatched comparison) both closed with a concrete negative finding: SBS1/SBS5 ratio is not operationally useful as a contamination flag on the `tcga_mc3` vs `msk_impact_2017` pair.
- **q009 replication-timing pilot ran to a fork.** `t121` (constitutive RT gene map from Dileep 2015), `t122` (all-mutation CE/CL burden), and `t123` (SBS1-proxy CE/CL burden) landed with three interpretation documents. `t122` was suggestive but coverage-confounded; `t123` collapsed under panel zero-inflation (only 58/1,210 unmatched samples had any proxy mutation at all).
- **Science profile / knowledge layer matured.** `t125` wired repo-local document kinds through `knowledge/sources/local/manifest.yaml`; curation metadata was normalized across `poc-interpretation`, `q009`, and canonical refs.
- **One new live decision point surfaced (`t124`):** whether q009 continues via true SBS1 mutation-context attribution or the panel/WES proxy branch is explicitly retired.

## Current State

**Overall:** 27 active tasks: **1 P1, 14 P2, 12 P3**. All `proposed` except `t055` (`deferred`). No P0 tasks. No `blocked` tasks — the prior blocked set (`t077`, `t110`) all closed.

### P1 tasks

| Task | Title | Status | Notes |
|---|---|---|---|
| t052 | Per-study cohort-stage descriptor | proposed | Only surviving P1. Still unexercised by the PoC; addresses the AR 18% MSK-metastatic vs 1% TCGA-primary class of bias called out in the cohort-selection-bias synthesis. |

### P2 queue shape

- **q009 decision:** `t124` (go/no-go on true SBS1 context vs retire proxy).
- **PoC follow-ups (still open from 2026-04-17):** `t102`, `t103`, `t104`, `t106`, `t107`, `t108`.
- **Meta-analysis / statistics follow-ups:** `t078` (co-occurrence/mutual-exclusivity), `t090` (pathway-layer benchmark), `t114` (pre-register q007 correction impact).
- **Data hygiene:** `t082` (HGNC aliases), `t083` (cancer-type canonicalization), `t087` (graded CH probability).
- **Normal-tissue extension:** `t112` (Lee-Six 2018 blood as second source for `t111`).

### Blocked Tasks

None. For the first time in several analyses, the active queue has no `blocked` rows.

### Hypothesis / question status

- 10 active questions (`q001`–`q010`) under `doc/questions/`, unchanged in count since 2026-04-22.
- `q009` now has the richest empirical trail (three pilots, three interpretations), but has also produced the only "fork" on the board via `t124`.
- `q007`, `q008`, `q010` are still infrastructure-ready but analytically silent — no first-pass quantitative result against the `t111` reference spectra.
- `specs/research-question.md` still carries the project-level hypothesis in prose; no formal files under `specs/hypotheses/`.

### Workflow Runs

- `results/` now holds two named workflow directories:
  - `results/poc-2026-04-17/` (t100 PoC annotated artifact)
  - `results/signature-brca-2026-04-22/` (t109/t110 signature-restriction outputs)
- **No `datapackage.json` manifests present in either.** This is the same operational gap flagged on 2026-04-22 — provenance is still carried narratively in `doc/interpretations/` rather than via run manifests.
- Six interpretation documents cover the distinct runs (`t100`, `t070`, `t111`, `t110`, `t122`, `t123`). No orphan runs without interpretations.

## Coverage Gaps

### Coverage Map

| Area | Coverage | Direction | Key Gap |
|---|---|---|---|
| Cross-study aggregation implementation | Strong | **improving** | Main spine now lands pooled GLMM-logit into the canonical ratio table. Remaining gap is `t052` cohort-stage descriptor, not denominator mechanics. |
| Workflow provenance / retained run artifacts | Missing | **stable (regressing)** | Still no `datapackage.json` manifests even though two runs now sit on disk. Unchanged since 2026-04-22 despite new runs landing. |
| Question formalization / hypothesis spine | Partial | stable | 10 `q*` questions, but `specs/hypotheses/` remains empty; no structured propositions carry the recent negative-result evidence from q009. |
| Task-state fidelity | Strong | **improving** | Every drift candidate from 2026-04-22 is now closed. Queue is trustworthy for the first time in several sessions. |
| Normal-tissue / signature-analysis branch | Partial | **stable** | `t111` infrastructure is still in place and `t109/t110` produced a first answer, but q007/q008/q010 remain without a quantitative first pass. |
| q009 mechanism test | Partial | **new** | Three pilots produced a coherent story: all-mutation RT ratio is coverage-confounded; simple CpG proxy is too sparse on panel cohorts. Decision now framed by `t124`. |
| Cross-project sync | Partial | **regressing** | Now 6 days stale (was 3 days on 2026-04-22). |

### High-Impact Gaps

**Gap 1 — q009 fork is the only live strategic decision and should be resolved before more pilots accrete.**
Three interpretations (`t110`, `t122`, `t123`) converge on the same operational conclusion: panel/WES-only burden summaries are too sparse to carry q009. Continuing to stack similar summaries without deciding the mechanism path is the highest-risk drift currently visible. `t124` is the explicit gate.

**Gap 2 — The `t111` normal-tissue infrastructure has not yet produced a first analytic result.**
The extraction pipeline landed on 2026-04-18 and is gated by three questions (q007, q008, q010). Six days later there is still no quantified first pass (e.g., expected fraction of gene-cancer ranking shifts under the null-model correction, or a single matched-vs-unmatched contamination-magnitude estimate). This branch is starting to accumulate "built but unexploited" risk.

**Gap 3 — Workflow provenance is split between narrative and filesystem, still.**
Two workflow runs on disk, zero `datapackage.json`. That makes run supersession and reproducibility checks impossible from `results/` alone. A small manifest-emission pass would close this.

**Gap 4 — Hypothesis spine does not absorb negative evidence.**
`t110` and `t123` are clean negative results against the original q009 story, but `specs/hypotheses/` is still empty and no structured proposition captures "panel-cohort SBS1 sparsity defeats the Yaacov LRR proxy." Negative results are currently trapped in interpretation docs rather than updating any hypothesis record.

**Gap 5 — The single P1 (`t052`) is now the main remaining known bias lever on the aggregation path.**
With `t076` / `t077` / `t070` all landed, cohort-stage (primary vs metastatic vs pre-treated) is the next documented cross-study confounder with a concrete magnitude estimate (`AR` 18% vs 1%, `ESR1` 11% vs 4%). It has been open since 2026-04-13 without movement.

### Status Transitions

**Newly unblocked since 2026-04-22:**
- None — the main spine already unblocked during the 2026-04-22 close-out session.
- However, `t124` is **newly actionable** as a first-class decision point (it was only hypothetical before the t122/t123 negative reads).

**Newly blocked since 2026-04-22:**
- None. The queue has no blocked tasks at all for the first time in several analyses.

**Newly irrelevant / pruning opportunities:**
- The 2026-04-22 recommendation *"reconcile stale task state (`t026`, `t043`, `t060`, `t070`, `t077`)"* is now fully resolved and should not be re-suggested.
- The 2026-04-22 recommendation *"execute `t076`"* is resolved.
- The 2026-04-22 recommendation *"write the `t077` execution plan (`t101`) and break into subtasks"* is resolved — plan written, `t115`–`t120` all closed, canonical join landed.
- `t055` (M/C-class descriptor) remains correctly deferred pending CNA ingestion; no change.

### Status Drift

Mandatory audit performed. Scanned `tasks/active.md` against `results/`, `doc/interpretations/`, `doc/reports/`, `doc/discussions/`, and recent git commits (since 2026-04-17).

**No drift detected.** Every task with status `proposed`, `blocked`, or `in_progress` in `tasks/active.md` has no matching evidence of completion in the filesystem. The 2026-04-22 reconciliation pass was thorough.

## Strategic Decision Point

**Decision:** where the project spends its next execution block — close the q009 fork, exercise the `t111` infrastructure against q007/q008, or pick up `t052` on the main aggregation spine.

**What bears on the decision:**

- The research question is still about **cross-study gene-cancer structure**. The cross-study aggregation spine is now far closer to "finished" than to "in-progress" — what's left on that path is one documented bias (`t052`) and hygiene (`t082`/`t083`), not new mechanisms.
- q009's three pilots produced a *coherent* negative story. Resolving `t124` doesn't require more data — it requires a decision and a short written record. High leverage per unit time.
- The q007/q008 branch has the reverse shape: infrastructure exists, but actually producing a first quantified answer requires real analytic work. High value but nonzero depth.
- `t052` is the only documented open bias lever on the aggregation path with a named magnitude estimate.

**Options:**

1. **Resolve `t124` first, then exercise `t111` downstream.** Close the q009 fork (one short decision document or a scoped new task), then pick up q008 (unmatched-normal contamination magnitude) using the existing `t111` reference spectra.
2. **Pick up `t052` on the aggregation spine.** Addresses a documented bias directly tied to the main research question; moves the last remaining P1 forward.
3. **Workflow-provenance pass.** Emit `datapackage.json` manifests retroactively for `results/poc-2026-04-17/` and `results/signature-brca-2026-04-22/`, then continue with (1) or (2).

**Recommendation:** **Option 1, then Option 2.** The q009 fork has been open for two days across three interpretations and is the cheapest strategic gate to close. After that, `t052` is the clean next step because it is the *only* open P1 on the main research question and it has a concrete bias magnitude attached. Option 3 is real but smaller; fold it into whichever session runs a new pipeline, rather than treating it as standalone work.

## Recommended Next Actions

| Priority | Action | Rationale | Command |
|---|---|---|---|
| P1 | Resolve `t124` (q009 fork) by choosing: (a) stage true SBS1 context/topography implementation as a new scoped task, or (b) write an explicit retirement/defer decision for the panel/WES proxy branch | `t110`, `t122`, `t123` have converged on a negative operational read; letting this sit without a decision risks further drift and more sparse pilots | `/science:discuss t124` or `/science:tasks done t124 ...` after the decision |
| P1 | Execute `t052` (per-study cohort-stage descriptor) | The only open P1; addresses a documented cross-study bias (`AR` 18% vs 1%, `ESR1` 11% vs 4%) on the main research-question path; the aggregation spine is otherwise clean | new implementation session for `t052` |
| P2 | Exercise `t111` downstream: produce first q008 quantitative estimate (unmatched-normal contamination magnitude against `normal_tissue_spectra.tsv`) | `t111` infrastructure is "built but unexploited" after six days; one targeted run gets q007/q008/q010 out of infrastructure-only status | new analysis session for q008 against `t111` reference |
| P2 | Emit retroactive `datapackage.json` for `results/poc-2026-04-17/` and `results/signature-brca-2026-04-22/` | Two workflow directories with zero manifests is the same operational gap flagged on 2026-04-22; 30-minute fix closes a recurring finding | small Snakemake rule addition or one-shot script |
| P2 | Refresh cross-project sync | Sync is 6 days stale (was 3 on 2026-04-22); adjacent projects may have conventions relevant to the q008 run above | `/science:sync` |

## Session Summary

The 2026-04-22 session was a large close-out — the cross-study aggregation spine landed (denominator hygiene + GLMM-logit pooling + canonical join), and the signature/q009 branch produced three concrete pilots. The queue is trustworthy for the first time in several sessions: no stale status, no blocked tasks, one remaining P1. The strategic picture has simplified to three candidate directions, with the q009 fork (`t124`) being the cheapest to close and the `t052` cohort-stage descriptor being the most direct service to the project's stated research question. The normal-tissue branch is now the "built-but-unexploited" risk to watch.
