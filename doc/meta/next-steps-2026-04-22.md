---
id: "meta:next-steps-2026-04-22"
type: "meta"
title: "Next Steps and Gap Analysis (2026-04-22)"
status: "active"
created: "2026-04-22"
updated: "2026-04-22"
---

# Next Steps — 2026-04-22

## Recent Progress

- **Cross-study aggregation execution moved from design to validated implementation**: the `t070` MSK-IMPACT per-sample panel-version fix landed as a full implementation branch and its PoC comparison verified the predicted ~30x TMB correction and 401 MSK false-to-true hypermutator flips.
- **The first end-to-end pipeline artifact was produced and interpreted**: `t100` completed on 2026-04-17, yielding the first annotated PoC run plus the integration interpretation at `doc/interpretations/2026-04-17-poc-run.md`.
- **Hypermutator calibration was tightened immediately after the PoC**: `t105` closed the composite-flag overcalling issue surfaced by `t100`, bringing BRCA and SKCM rates back into biologically plausible ranges.
- **A new normal-tissue / signature-analysis branch was built out**: `t111` landed the Li2021 normal-tissue spectra extraction pipeline, wrote its interpretation, and directly enabled q007/q008/q010-style downstream analyses.
- **Project metadata and knowledge assets were migrated over the last 14 hours**: tasks migrated (`4328958`), paper metadata migrated (`8fdb53a`, `2c65fed`), and the knowledge graph plus local mappings were refreshed.
- **Question formalization is materially stronger than in the 2026-04-17 snapshot**: `science-tool project index --format json` now returns 10 active questions under `doc/questions/`, closing the earlier “index is empty” problem.

## Current State

**Overall:** 35 active tasks: 5 P1, 18 P2, 12 P3. By type: 24 dev, 11 research. By status: 31 proposed, 2 blocked, 1 active, 1 deferred. No P0 tasks.

### P1 tasks

| Task | Title | Status | Notes |
|---|---|---|---|
| t052 | Per-study cohort-stage descriptor | proposed | Still open; not exercised by the 4-study PoC. |
| t070 | MSK-IMPACT panel-version drift handling per sample | **proposed (stale)** | Implementation branch and positive validation doc exist; this status no longer matches the codebase. |
| t076 | NaN-vs-0 handling for panel-aware aggregation | proposed | Still the main denominator-hygiene fix before pooled cross-study modeling. |
| t077 | Random-effects pooled gene x cancer (GLMM-logit) | **blocked (stale)** | `blocked-by: [t081, t079]`, but both tasks are already closed. |
| t101 | Decompose t077 into a plan + tracked subtasks | proposed | Still the cleanest next step once `t077` is unblocked in task state. |

### P2/P3 queue shape

- **Active now:** `t109` (per-study cancer-type signature restriction for SigProfilerAssignment).
- **Blocked now:** `t110` is still genuinely blocked by `t109`.
- **Open follow-up cluster from the PoC / null-model work:** `t102`, `t103`, `t104`, `t106`, `t107`, `t108`, `t112`, `t113`, `t114`.
- **Deferred:** `t055` remains correctly deferred because CNA ingestion is still out of scope.

### Blocked Tasks

| Task | Current status | Blocking condition | Assessment |
|---|---|---|---|
| t077 | blocked | `t081`, `t079` | **Stale blocker.** Both are closed in `tasks/done/2026-04.md`; this should be unblocked. |
| t110 | blocked | `t109` | Real blocker. Signature-restriction rule needs to land first. |

### Hypothesis / question status

- `specs/research-question.md` still carries one project-level hypothesis in prose, but there are **no formal files under `specs/hypotheses/`**.
- `science-tool project index --format json` now returns **10 active questions** (`q001`–`q010`), mostly concentrated in the normal-tissue contamination / null-model branch.
- This is a real change from the 2026-04-17 analysis, which reported an empty project index.

### Workflow Runs

- **No `results/**/datapackage.json` manifests are present on disk today.**
- That means there are **no current runs to classify** as recent / superseded / draft from `results/` alone.
- However, three interpretation documents demonstrate recent executed work:
  - `doc/interpretations/2026-04-17-poc-run.md` (`t100`, first annotated PoC run)
  - `doc/interpretations/2026-04-18-t070-poc-comparison.md` (pre/post `t070` validation)
  - `doc/interpretations/2026-04-19-t111-normal-tissue-spectra-pipeline.md` (`workflow_run: t111-2026-04-19`)
- **Gap:** run interpretations exist, but the corresponding manifests are not currently auditable in the workspace. Provenance is therefore split between docs and a now-empty `results/` tree.

## Coverage Gaps

### Coverage Map

| Area | Coverage | Direction | Key Gap |
|---|---|---|---|
| Cross-study aggregation implementation | Partial | improving | `t070`, `t100`, and `t105` landed, but `t076` and the `t101` → `t077` path are still unfinished. |
| Workflow provenance / retained run artifacts | Missing | regressing | Interpretations exist, but no `datapackage.json` manifests are on disk for auditing run state or supersession. |
| Question formalization / project indexability | Stronger | improving | `doc/questions/` now has 10 active questions, but the core research question is still not decomposed into formal hypotheses. |
| Task-state fidelity | Weak | regressing | Several active tasks no longer match reality (`t026`, `t043`, `t060`, `t070`, `t077`). |
| Normal-tissue / signature-analysis branch | Partial | improving | `t111` built the infrastructure and `t109` is active, but no first downstream q007/q008 result has been produced yet. |
| Cross-project sync | Partial | improving | Sync is 3 days stale rather than 6, but still worth refreshing before another design-heavy session. |

### High-Impact Gaps

**Gap 1 — Task-state drift is now blocking prioritization.**  
The backlog no longer cleanly tells you what the frontier is. `t070` is effectively done but still marked `proposed`; `t077` is still marked `blocked` even though its blockers are closed; `t026`, `t043`, and `t060` all have matching deliverable commits yet remain active. Until this is reconciled, every task review overstates the amount of unfinished work and hides the real next dependency chain.

**Gap 2 — The main research-question spine is still one task away from being truly “execution ready.”**  
The project’s stated research question is about cross-study mutation structure and recurrent gene-cancer associations. Relative to that objective, the highest-value remaining chain is now `t076` (denominator hygiene) followed by `t101`/`t077` (planned GLMM pooling). That path is clearer than it was on 2026-04-17, but it still has not been taken.

**Gap 3 — Run provenance is documented narratively, not operationally.**  
The workspace currently has interpretation documents for `t100`, `t070`, and `t111`, but no retained manifests under `results/`. That prevents a proper run inventory and makes supersession/status checks impossible from the filesystem alone. In a pipeline-heavy project, that is a real operational blind spot.

**Gap 4 — The normal-tissue branch has infrastructure but not yet a decisive first analytic payoff.**  
`t111` materially improved feasibility for q007/q008/q010, and `t109` is active. But until either q007 correction effects or q008 contamination magnitude is quantified, the branch remains “promising infrastructure” rather than evidence-bearing analysis.

### Status Transitions

**Newly unblocked since 2026-04-17:**

- **t077** is functionally unblocked because `t079` and `t081` are closed, even though the task file still says `blocked`.
- **q007 / q008 / q010 downstream work** is meaningfully unblocked by `t111` and its interpretation; the necessary normal-tissue spectra table now exists.

**Newly blocked since 2026-04-17:**

- No newly blocked top-priority task emerged. `t110` is blocked, but that blocker (`t109`) is explicit and expected.

**Newly irrelevant / pruning opportunities:**

- The old “project index is empty / `doc/questions/` is empty” recommendation from the 2026-04-17 analysis is no longer current. That generic gap has been closed by migration and question creation work.
- `t026`, `t043`, and `t060` look more like stale-status cleanup candidates than live execution work.

### Task Tracking Gaps

No major new plan-to-task gap was found in `doc/plans/`.

- The earlier `t081` subtask gap remains resolved.
- The `t070` and `t111` plan documents map to substantial landed commit series rather than to missing untracked implementation work.
- The current coordination failure is **status drift**, not “buried plan work with no task.”

### Status Drift

| Task | Current status | Evidence | Suggested update |
|---|---|---|---|
| t026 | proposed | Commit `76f82fd` landed `doc/background/topics/cross-panel-normalization-methods.md`; prior next-steps docs already called it “done in substance” | close or rescope to residual implementation work only |
| t043 | proposed | Commit `43b44ce` landed the pathway-level pan-cancer methods search; downstream benchmark work was split out into `t090` | close search task |
| t060 | proposed | Commit `c1096bd` landed the panel-mutation-data guide expansion | close task |
| t070 | proposed | Full implementation branch merged (`cae4243`) and `doc/interpretations/2026-04-18-t070-poc-comparison.md` verifies the fix | mark done |
| t077 | blocked | `tasks/done/2026-04.md` shows `t079` and `t081` complete; `doc/meta/next-steps-2026-04-17.md` already called `t077` unblocked | update to proposed/unblocked; keep `t101` as the immediate next action |

## Strategic Decision Point

**Decision:** return to the main cross-study aggregation spine now, or continue deepening the newer normal-tissue/signature branch first.

**What bears on the decision:**

- The project’s formal research question is still centered on **cross-study gene-cancer structure**, not on signature contamination per se.
- That main path is now closer to execution than before: `t070` and `t105` are done in practice, leaving `t076` and `t101`/`t077` as the main remaining sequence.
- The normal-tissue branch is now credible and useful, but still lacks a first high-impact downstream result. `t109` is active; `t110` is blocked by it.
- Backlog drift currently obscures both paths; without a cleanup pass, either choice will be harder to reason about.

**Options:**

1. **Aggregation-first:** reconcile task statuses, then do `t076` followed by `t101` and `t077`.
2. **Signature-first:** keep pushing `t109`, then `t110`, and try to answer q008/q009 before returning to pooled frequency modeling.
3. **Hygiene-first reset, then choose:** spend one short session reconciling statuses and blockers, then pivot immediately to option 1 unless new evidence says otherwise.

**Recommendation:** **Option 3, then Option 1.**  
The backlog is currently misleading enough that a quick task-hygiene pass has unusually high leverage. After that, the default next path should be `t076` → `t101` → `t077`, because that sequence most directly serves the project’s primary research question and uses the execution momentum already built by `t070`, `t100`, and `t105`. Keep `t109` as the active secondary branch, not the main line.

## Recommended Next Actions

| Priority | Action | Rationale | Command |
|---|---|---|---|
| P1 | Reconcile stale task state (`t026`, `t043`, `t060`, `t070`, `t077`) | The backlog is currently overstating open work and hiding the real frontier; this is the shortest path to a trustworthy queue | `/science:review-tasks` |
| P1 | Execute `t076` (NaN-vs-0 panel-aware aggregation close) | This is now the main remaining denominator-hygiene fix before cross-study pooled modeling | new implementation session for `t076` |
| P1 | Write the `t077` execution plan and break it into tracked subtasks (`t101`) | `t077` is functionally unblocked; a t081-style decomposition is the cleanest way to restart that branch | `/science:plan-pipeline` |
| P2 | Continue `t109` only after the aggregation spine is back in motion | The normal-tissue branch now has good infrastructure, but it is still secondary to the main research question | new implementation session for `t109` |
| P2 | Refresh cross-project sync | Sync is 3 days stale; adjacent projects may have methods or conventions relevant to the next planning step | `/science:sync` |

## Session Summary

Relative to the 2026-04-17 snapshot, the project is in a better state than the raw task file suggests. The biggest improvements are real execution work (`t070`, `t100`, `t105`, `t111`) and stronger formal question tracking (`q001`–`q010`). The biggest regression is operational, not scientific: task-state drift now obscures the actual frontier.

The practical consequence is straightforward: treat today as a queue-reconciliation checkpoint, not as a “what should we invent next?” session. Clean the board, then continue the main cross-study aggregation path.
