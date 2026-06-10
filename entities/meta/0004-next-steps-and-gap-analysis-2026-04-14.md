---
type: meta
title: Next Steps and Gap Analysis (2026-04-14)
status: active
created: '2026-04-14'
updated: '2026-04-14'
id: meta:0004-next-steps-and-gap-analysis-2026-04-14
---

# Next Steps — 2026-04-14

## Recent Progress

**Research / documentation (today's session):**

- **t026 cross-panel-normalization-methods topic** — methods-side complement to
  `targeted-panel-sequencing-bias`; FoCR Phase I/II, Buchhalter, Fancello added
  (`76f82fd`).
- **t060 panel-mutation-data modality guide** expanded with 4 new source citations,
  2 new checklist rows (panel.11 NaN-vs-0, panel.12 commercial-BED fallback), 3 new
  pitfalls (`c1096bd`).
- **t043 pathway-level pan-cancer search** — 6 Core-now (Reyna 2020 PCAWG,
  Paczkowska 2020 ActivePathways, Leiserson 2015 HotNet2, Iorio 2018 SLAPenrich,
  Martinez-Jimenez 2020 IntOGen, Horn 2018 NetSig), 7 BibTeX added (`43b44ce`).
- **t059 ASXL1/TET2 CH-leakage search** — Coombs 2018 per-gene stratification
  (8% overall, DNMT3A ~64%, TP53 ~4%), 6 BibTeX added (`f077cab`).
- **t025 rescoped** — TMB follow-up: Campbell 2017 hypermutator cutoffs, Samstein
  2019 per-histology cutpoints, Chalmers 2017 100k-cohort landscape, 6 BibTeX
  added (`26502f2`).

**Task backlog:**

- 5 new follow-up tasks created from session synthesis: **t087** (graded CH prob),
  **t088** (age-adjusted TMB), **t089** (dual hypermutator flags, P1), **t090**
  (pathway benchmark), **t091** (TET2 companion search) (`60717f8`).

## Current State

**Overall**: 26 active tasks — 25 proposed, 1 deferred (t055 blocked on CNA ingestion).
7 P1, 8 P2, 11 P3. By type: 17 dev, 9 research. None in-progress.

### P1 tasks (critical path, 7 items — all proposed, none in-progress)

| Task | Title | Group |
|---|---|---|
| t052 | Per-study cohort-stage descriptor (primary/metastatic/pre-treated) | pipeline |
| t070 | F6 MSK-IMPACT panel-version drift handling per sample | audit-fixes |
| t076 | F2 full close: NaN-vs-0 handling for panel-aware aggregation | pipeline |
| t077 | Random-effects pooled gene×cancer table (GLMM-logit) | meta-analysis |
| t079 | Pre-register GLMM-logit pooling choice before full-dataset run | meta-analysis |
| t081 | Hypermutator / TMB-aware sample exclusion or covariate | pipeline |
| **t089** | **Per-histology relative + absolute dual hypermutator flags (new)** | pipeline |

### P2 tasks (active queue, 8 items — unchanged today)

t026 [done in substance], t043 [done in substance], t060 [done], t078, t082, t083, t087, t090.

### Hypothesis / question status

- `specs/research-question.md` has **1 hypothesis** (pan-cancer cross-study aggregation
  reveals robust gene-cancer associations). No formal hypothesis files under `specs/
  hypotheses/`; no question files under `doc/questions/`.
- `science-tool project index --format json` returns an empty `rows: []` — the
  hypothesis/question index is not populated.
- **Five open methodological questions** surfaced across today's searches are tracked
  in topic "Controversies & Open Questions" sections rather than formal
  `doc/questions/` entries.

### Workflow Runs

- **`results/` is empty.** No `datapackage.json` manifests. Despite heavy
  documentation investment, no pipeline output is published.

## Coverage Gaps

### Coverage Map

| Area | Coverage | Direction | Key Gap |
|---|---|---|---|
| Topics (literature conceptual map) | Strong | new | cross-panel-normalization-methods added today; 15 total |
| Papers (BibTeX + stubs) | Strong | improving | 82 BibTeX, 39 paper stubs; 2026-04-14 searches added 23 refs |
| Pipeline implementation | Partial | stable | t080 committed in-flight scripts; P1 fixes remain proposed |
| Pipeline outputs (results/) | **Missing** | stable | **`results/` is empty — no artifacts published** |
| Pre-registration / falsifiability | Partial | stable | 1 informal hypothesis; t079 pre-registration is P1 but not done |
| Data ingestion (GENIE / MC3) | Partial | stable | Manual Synapse DUA prerequisites; scripts wired, data not in data/ |
| Bias-axis handling in aggregation | Partial | improving | Panel-normalization methods cataloged (t026) — implementation still P1 |
| Hypothesis / question formalization | **Weak** | stable | `doc/questions/` empty; 5+ open questions live only inside topics |
| Cross-project sync | Stale (3 d) | regressing | `seq-feats`, `mm30`, others may have relevant updates |

### High-Impact Gaps

**Gap 1 — Results absence dominates the critique surface.**
The project has invested in ≈5 topics, 4 searches, 82 refs, a full bias audit, and a
t081 implementation plan, but `results/` is empty. Without a single output feather or
interpretation document, every "methodological upgrade" task reads as speculative. One
small-cohort end-to-end run (even on the current imperfect pipeline) would expose
which of the 7 P1 fixes are actually load-bearing vs theoretically nice to have.

**Gap 2 — t081 plan-to-task drift.**
`doc/plans/2026-04-13-t081-hypermutator-annotation-pipeline-plan.md` defines **8
implementation subtasks** (panel callable-Mb registry → TMB calc → POLE/POLD1 detector
→ MSI ingest → GMM fit → composite score → ratios passthrough → docs). None of these
subtasks appear in `tasks/active.md`. They live only in the plan document. When t081
starts executing, the 8 subtasks need to be real tasks so progress is trackable.

**Gap 3 — GLMM-logit pre-registration (t079) blocks t077.**
t077 (random-effects pooled gene×cancer) and t079 (pre-register GLMM-logit choice)
are both P1. Running t077 without t079 risks post-hoc rationalization of pooling
choices on the actual data. t079 is a 1–2 session writing task; should precede t077.

**Gap 4 — `doc/questions/` is empty.**
The five controversies-and-open-questions from today's topics (cross-panel intersection
vs callability; CH filter granularity; per-histology vs universal hypermutator cutoff;
pathway-database choice; MSI-status ingestion) are methodologically load-bearing. Lives
inside topic files means they don't surface in `science-tool project index` and aren't
visible to `science:status` or `science:bias-audit` workflows.

**Gap 5 — No cross-study co-occurrence / ME statistic (t078) despite search done.**
t042 search is done, `topic:co-occurrence-and-mutual-exclusivity` exists, DISCOVER /
SELECT / WeSME are reviewed. But t078 (implementing cross-study co-occurrence with
Stouffer-pooled p-values) is still proposed at P2. The research phase here is
complete; the pipeline phase has not started.

## Task Tracking Gaps

**t081 plan → unbroken-out subtasks (identified Gap 2):**

| Plan subtask | Proposed task ID (not yet created) |
|---|---|
| Task 1 — Panel callable-Mb registry (`build_panel_callable_sizes`) | — |
| Task 2 — Per-sample TMB calculation + `study_id` propagation (`compute_per_sample_tmb`) | — |
| Task 3 — POLE / POLD1 hotspot detector (`detect_polymerase_hotspots`) | — |
| Task 4 — MSI status ingestion (`convert_to_feather.py` extension) | — |
| Task 5 — Per-cancer-type TMB GMM fit (`fit_per_cancer_tmb_gmm`) | — |
| Task 6 — Composite hypermutation score + final flag (`annotate_hypermutators`) | — |
| Task 7 — Per-study inclusive/exclusive ratios + combined passthrough | — |
| Task 8 — Documentation + AGENTS.md updates | — |

Creating these as blocked-by-t081 subtasks would make execution trackable.

## Strategic Decision Point

**Fork**: **Breadth-first research annotation vs depth-first end-to-end execution.**

- **What the decision is**: After today's session the research / documentation surface
  is rich (15 topics, 4 searches, 82 refs). The pipeline implementation surface has 7
  P1 tasks and an empty `results/`. Continuing to add research tasks / searches has
  diminishing returns; continuing to debate methodology in the abstract without
  outputs has even worse returns.

- **Evidence bearing on the decision**:
  - Zero results artifacts in `results/`; zero interpretation documents under
    `doc/interpretations/`.
  - Pipeline was run at least once (t080 "in-flight pipeline work committed" — commit
    `36bfee9`) but outputs are not publishable.
  - 26 active tasks, 0 in-progress, for 4+ days.
  - Five new follow-up research tasks created today (t087–t091) extend the research
    surface but don't move any output closer.

- **Options**:
  1. **Breadth-first research continuation** — work through t025 residual → t078
     implementation → t087 graded CH prob → t091 TET2 companion search. Keeps
     documentation ahead of code; does not produce outputs.
  2. **Depth-first P1 pipeline execution** — (a) t079 pre-registration → (b) t081 +
     its 8 subtasks → (c) t076 F2 close → (d) small-cohort PoC run on 3–5
     MSK-IMPACT + TCGA studies → (e) interpretation document. Produces results;
     exposes real bugs.
  3. **Hybrid** — t079 alone (1 short task, unblocks t077 + t081 design), then step
     into Option 2 Task flow.

- **Recommendation**: **Option 3 (hybrid — t079 first, then pipeline execution).**
  t079 is small and unblocks pre-registration before any GLMM-logit run.
  After t079, prioritize t076 (F2 close; small, unblocks honest denominators),
  then t070 (panel-version drift — a prerequisite for clean t081 TMB), then t081
  (with its 8 subtasks created as real tasks). Defer t077, t078, t087, t090, t091
  until at least one end-to-end run has produced outputs that could be interpreted.

## Recommended Next Actions

| Priority | Action | Rationale | Command |
|---|---|---|---|
| P1 | Execute t079 (pre-register GLMM-logit pooling choice) | Unblocks t077 + t081 design; short writing task; defends against post-hoc rationalization | `/science:pre-register` |
| P1 | Break t081's 8 plan subtasks into tracked tasks with `blocked-by:t079` | Plan → tasks drift is real tracking gap; execution needs per-subtask trackability | `science-tool tasks add` ×8 |
| P1 | Execute t076 (F2 full close — NaN vs 0 handling) | Smallest of the P1 pipeline tasks; fixes statistically-incoherent denominators before any aggregation | new implementation session |
| P2 | Small-cohort PoC run (3–5 MSK-IMPACT + 3 TCGA studies) | Produces the first `results/` artifact; exposes what P1 fixes are load-bearing vs theoretical | `uv run snakemake` on reduced config |
| P2 | Populate `doc/questions/` with 5 open questions from today's topics | Makes methodological controversies first-class in the project index | `/science:add-hypothesis` (question variant) |
| P2 | Cross-project sync (3 days stale) | `seq-feats`, `mm30`, `natural-systems-guide` may have relevant updates | `/science:sync` |
| P3 | Defer t087, t088, t090, t091 until first PoC run exists | Avoids further research depth without outputs | (no command — scheduling only) |

## Session Summary

Arc of today's work: the user wanted to tackle 5 research-topic-style tasks
(t025, t026, t043, t059, t060). They were not uniformly research-topic — t060
was a guide edit, t025/t026/t043/t059 were searches. Dispatching in C-mode
(one at a time with user validation) worked well. Each task closed with
verified PMIDs and a commit. The session produced 23 new BibTeX entries, 1
new topic, 1 guide expansion, 4 new searches, and 5 follow-up tasks.

The unresolved strategic question is the fork framed above: whether to
continue extending research annotation or pivot to executing the 7 P1
pipeline tasks. The evidence points toward pivoting (results/ is empty despite
heavy documentation investment), and this next-steps analysis recommends the
t079 → t076 → t070 → t081-with-8-subtasks sequence as the first concrete
step of that pivot.
