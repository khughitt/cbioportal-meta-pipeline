---
type: meta
title: Next Steps and Gap Analysis (2026-04-17)
status: active
created: '2026-04-17'
updated: '2026-04-17'
id: meta:0005-next-steps-and-gap-analysis-2026-04-17
---

# Next Steps — 2026-04-17

## Recent Progress

Since the 2026-04-14 analysis, the recommended depth-first pivot executed in
essentially one push and landed most of it:

**Pipeline implementation — t081 hypermutator/TMB pipeline fully landed (8/8 subtasks + parent):**

- t092 panel callable-Mb registry (`a97d429`)
- t093 per-sample TMB computation (`df2bd0a`)
- t094 POLE/POLD1 hotspot detector (`979a61f`)
- t095 MSI status ingestion (`9486ed9`)
- t096 per-cancer TMB GMM fit (`40185e3`)
- t097 composite hypermutation score + flag (`9e24139`)
- t098 per-study inclusive/exclusive ratios + combined passthrough (parts A/B/C
  in `3d063b2`, `3690dc7`, `082bca9`)
- t099 docs / AGENTS.md updates (`b690e7b`)
- t081 parent closed (`213499c`)

**Pre-registration:**

- t079 GLMM-logit pooling pre-registration committed (`52d0086`) — unblocks t077.

**Task tracking gap from 2026-04-14 closed:**

- The 8 plan subtasks were broken out as tracked tasks (`e808455`), then all
  executed — Gap 2 from the prior analysis is fully resolved.

**In-flight / uncommitted-feeling commits:**

- `a2ce3fc` (save) and `c0f48af` (data) — terse messages, worth confirming what
  was staged there.

## Current State

**Overall:** 25 active tasks remain (9 P1 or P2 pipeline, plus P2/P3 research
follow-ups). t081 and all its subtasks are done; t079 is done. t077 is now
unblocked.

### P1 tasks (critical path)

| Task | Title | Status | Notes |
|---|---|---|---|
| t052 | Per-study cohort-stage descriptor (primary/metastatic/pre-treated) | proposed | Pipeline. Addresses cohort-stage bias. |
| t070 | F6 MSK-IMPACT panel-version drift handling per sample | proposed | Pipeline. Prerequisite for clean TMB denominators across MSK cohorts. |
| t076 | F2 full close: NaN-vs-0 handling for panel-aware aggregation | proposed | Pipeline. Dovetails with t098 per-study ratios layer just landed. |
| t077 | Random-effects pooled gene×cancer (GLMM-logit) | **unblocked** (was blocked by t081, t079 — both done) | Meta-analysis. Pre-registration already in hand. |
| t089 | Per-histology relative + absolute dual hypermutator flags | partially absorbed | t097 note says composite flag emits Campbell-absolute + Samstein-relative — verify and close or rescope. |

### P2 tasks (active queue)

t026, t043, t060 (all done in substance per prior analysis); t078, t082, t083,
t087, t090 open. New-since-04-14: none.

### P3 tasks

Unchanged from 04-14.

### Hypothesis / question status

- `science-tool project index --format json` still returns `rows: []`. No
  formal hypothesis/question files under `specs/hypotheses/` or `doc/questions/`.
- The five open methodological questions flagged in the 04-14 analysis remain
  inside topic files, not in the index. **No movement on Gap 4.**

### Workflow Runs

- `results/` is **still empty**. No `datapackage.json`. Despite the hypermutator
  pipeline now being implementable end-to-end, no artifact has been produced.
- `doc/interpretations/` is **still empty**.

## Coverage Gaps

### Coverage Map

| Area | Coverage | Direction | Key Gap |
|---|---|---|---|
| Topics (literature map) | Strong | stable | No new topics since 04-14; 16 topic files. |
| Papers (BibTeX + stubs) | Strong | stable | No new searches since 04-14. |
| Pipeline implementation | Partial → **stronger** | **improving** | Hypermutator / TMB annotation landed; t076, t070, t052 remain P1. |
| Pipeline outputs (`results/`) | **Missing** | **stable (regressing relative)** | Gap 1 from 04-14 unresolved — pipeline capability grew while outputs stayed at zero. |
| Pre-registration / falsifiability | Partial → **stronger** | **improving** | t079 pre-registration committed; t077 ready to run against it. |
| Data ingestion (GENIE / MC3) | Partial | stable | Manual Synapse DUA still the gating step; no ingest artifacts observed. |
| Bias-axis handling in aggregation | Partial → **stronger** | **improving** | Hypermutator pooling bias (F1/F4/F6) now handled; F2 (t076), F6 MSK drift (t070), cohort-stage (t052) remain. |
| Hypothesis / question formalization | Weak | stable | `doc/questions/` still empty; project index still empty. |
| Cross-project sync | Stale (6 d) | **regressing** | Was 3 d stale on 04-14; now 6 d. |

### High-Impact Gaps

**Gap 1 — Results absence now glaring.** The pipeline can, today, produce a
hypermutator-annotated, CH-annotated, driver-annotated, inclusive/exclusive
ratio feather. Nothing in `results/` demonstrates this. Every further
methodological task is speculative until an end-to-end run exists. The 04-14
"small-cohort PoC run" recommendation was not acted on and is now the single
highest-leverage next action. One run on a reduced config (e.g. 3 MSK-IMPACT +
3 TCGA studies) would tell us which of the remaining P1 fixes (t070, t076,
t052) are load-bearing for the first interpretable output vs nice-to-have.

**Gap 2 — t077 is unblocked but has no execution plan.** t081 + t079 were the
two blockers; both are done. t077 as written has no subtask decomposition and
no "first target" (which gene×cancer matrix? what's the MCMC vs PQL tradeoff?
what diagnostics close the run?). Prior art (t081 plan → subtask
decomposition → execution) worked extremely well; t077 needs the same
treatment before it starts.

**Gap 3 — t089 overlap with t097 unresolved.** t097's closeout note says it
already emits `is_hypermutator_absolute` (Campbell cutoff) and
`is_hypermutator_relative` (Samstein per-histology top-20%). t089 was created
on 04-14 as a P1 to do exactly that. Either t089 is already satisfied (and
should close) or its scope is finer than what t097 delivered and needs a
narrow delta description. Either way, t089 should not sit as an untouched P1.

**Gap 4 — `doc/questions/` still empty.** Unchanged from 04-14. The five
open questions (cross-panel intersection vs callability; CH filter
granularity; per-histology vs universal hypermutator cutoff — likely closed
by t097; pathway-database choice; MSI-status ingestion policy — partly closed
by t095) haven't been promoted to first-class question files. Some are now
answered and should be recorded as such.

**Gap 5 — In-flight commits with terse messages (`save`, `data`).** Two of the
last three commits on main are single-word. The repo should probably know what
these contained before the next session builds on top.

## Status Transitions

**Newly unblocked since 2026-04-14:**

- **t077** (GLMM-logit pooled gene×cancer) — was blocked by t081 and t079,
  both now done. The highest-value follow-on from the t081 sprint.

**Newly irrelevant / prunable:**

- **t089** (per-histology dual hypermutator flags) — very likely already
  delivered inside t097's composite-flag output. Verify and close (or rescope
  to any residual).

**Newly closed since 2026-04-14 (from done log):**

- t079, t081, t092, t093, t094, t095, t096, t097, t098, t099 (10 closures in
  one push).

**Newly created since 2026-04-14:**

- None. No new research tasks, no new pipeline tasks, no new searches. This is
  a healthy sign: the session stayed focused on execution.

## Task Tracking Gaps

None detected. The t081 plan subtask gap flagged on 04-14 was fully resolved
(t092–t099 tracked and executed). `doc/plans/` contains only the t081 plan and
its review; both are now reflected in closed tasks.

## Strategic Decision Point

**Fork:** Execute t077 next, or run the PoC first.

- **What the decision is:** Having landed t081 + t079, two paths are open. (A)
  Continue vertical execution into t077 (GLMM-logit pooled gene×cancer),
  producing the first meta-analytic output. (B) Produce a small-cohort
  end-to-end run first, emitting the first `gene_cancer_study_ratio_annotated.
  feather` into `results/`, then decide whether t077 needs t076/t070 first.

- **Evidence bearing on it:**
  - `results/` empty after 4+ days of heavy implementation — this is the
    single largest blocker to honest interpretation of anything.
  - t077's pre-registration (t079) is written, so running it is no longer
    speculative.
  - t077 without t076 (NaN-vs-0 close) will produce coherent-looking numbers
    with a known denominator bias. The bias is **documented** in the
    pre-registration, but still baked in.
  - A PoC run on today's pipeline would reveal whether t076 / t070 are the
    actual blockers to a first result, or whether the present output is
    already publishable-as-preliminary.

- **Options:**
  1. **Run t077 immediately.** Highest research-output velocity; inherits
     known bias from t076-deferred state.
  2. **PoC run first, then t077.** Surfaces which P1 fixes are load-bearing;
     delays first meta-analytic output by one short session.
  3. **t076 first, then PoC, then t077.** Best statistical hygiene; slowest
     to first artifact.

- **Recommendation: Option 2.** One small-cohort run (≈1 session) produces
  the first `results/` artifact and stress-tests t092–t098. If the run
  succeeds cleanly, t077 is the natural next step against that same cohort.
  If the run exposes a denominator or panel-intersection issue, that fix
  (likely t076 or t070) becomes the justified next step. Either way, the
  first action is the same: run the pipeline end-to-end on a reduced config.

## Recommended Next Actions

| Priority | Action | Rationale | Command |
|---|---|---|---|
| **P1** | Small-cohort PoC run (3–5 MSK-IMPACT + 3 TCGA studies) | First `results/` artifact; stress-tests hypermutator pipeline; clarifies which remaining P1 fix is load-bearing | `uv run snakemake -s code/workflows/Snakefile -j1 --configfile code/config/<reduced>.yml` |
| **P1** | Reconcile t089 against t097 delivery; close or rescope | t097 closeout claims both Campbell-absolute and Samstein-relative flags are emitted — t089 should not sit as open P1 if satisfied | `uv run science-tool tasks close t089` (if verified) or edit scope |
| **P1** | Decompose t077 into subtasks before starting (mirror t081 pattern) | t077 is now unblocked; t081 subtask decomposition worked extremely well and should be the template | Write `doc/plans/2026-04-17-t077-glmm-logit-plan.md`, then `science-tool tasks add` per subtask |
| **P2** | Review `a2ce3fc` (save) and `c0f48af` (data) for undocumented changes | Terse messages on main risk losing context; confirm what's there and amend messages or document | `git show a2ce3fc c0f48af` |
| **P2** | Execute t076 (F2 full close: NaN-vs-0) only if PoC run surfaces it | Deferred from 04-14; keep behind PoC run to justify ordering | (post-PoC) |
| **P2** | Cross-project sync (6 d stale, was 3 d on 04-14) | Regressing; `seq-feats`, `mm30`, `natural-systems-guide` possibly relevant | `/science:sync` |
| **P2** | Promote 2–3 closed open-questions from topics to `doc/questions/` (per-histology cutoff; MSI ingestion policy) | Make resolution by t095/t097 discoverable via project index | `/science:add-hypothesis` (question variant) |
| **P3** | Defer t087, t088, t090, t091 until PoC exists | Unchanged from 04-14 — research surface has diminishing returns without outputs | (no command — scheduling only) |

## Session Summary

The 04-14 recommendation was Option 3 (hybrid: t079 first, then depth-first
pipeline execution). That is exactly what ran. Over 3 days, 10 tasks closed,
the hypermutator annotation pipeline landed end-to-end (panel callable-Mb →
per-sample TMB → POLE/POLD1 → MSI → GMM → composite flag → paired
inclusive/exclusive ratios → docs), and t079 pre-registration went in ahead of
t077. This is a clean execution of the prior plan and removes all three
blockers (Gap 2 from 04-14 fully resolved, Gap 3 unblocked, t089 likely
absorbed).

The outstanding blocker from 04-14 — **no artifact in `results/`** — is
unchanged. The single highest-leverage next action is a small-cohort PoC run;
everything else (t077, t076, t070, t052) should branch off what that run
reveals.
