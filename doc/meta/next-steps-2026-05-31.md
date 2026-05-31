---
id: "meta:next-steps-2026-05-31"
type: "meta"
title: "Next Steps — 2026-05-31"
created: "2026-05-31"
updated: "2026-05-31"
prior: "meta:next-steps-2026-04-27"
related: []
---

# Next Steps — 2026-05-31

> **Window note.** The prior next-steps is dated 2026-04-27 — **34 days stale**. This is a
> full-mode analysis spanning a major pivot: the project's center of gravity moved from
> dNdScv driver-ranking to a **mutational-signature aetiology program** (h08–h11) that the
> 2026-04-27 doc never saw. The "Direction" column is anchored to 2026-04-27 where comparable.

## Recent Progress

**Driver-ranking program closed out (late Apr).** Every 2026-04-27 P1/P2 recommendation
shipped: `t144` (dNdScv tiebreaker), `t145` (mean_inclusive inflation diagnostic), and
`t141` (R `mclapply` parallelization) all landed; `validate.sh` is now `current`
(`2026.05.21.1`). The dNdScv line consolidated with `t146` CGC external validation, `t149`
LOSO replication, and the full `t173` LOSO suite (6 interpretations, 2026-04-29/30),
plus `q003` RT-residual and `q016` panel-ascertainment interpretations.

**Hypothesis spine expanded ~3×.** The project now carries **10 proposed hypotheses**
(h01–h11) and **28 questions** (q001–q028, 27 active + 1 deferred). Five of those
hypotheses (h05, h06, h08, h09, h10, h11) and eleven questions (q018–q028) are new since
2026-04-27, almost all in the signature/normal-tissue/attention space.

**Mutational-signature corpus + topics (late May).** 60+ signature papers batch-summarized
(`doc/papers/` now 102 entries), mutsig topics synthesized, the `h08-agnostic-association-model`
method doc written, and h09/h10/h11 + q026–q028 added (commit `f78108f`).

**h08 signature-decomposition layer hardened (today).** `t178` (COSMIC SBS version pin +
signature-presence audit + caller-consensus flag) and `t179` (per-sample SBS count floor +
de-novo-vs-refit decision sidecar) landed in `run_restricted_sigprofiler_assignment.py`
(commits `02a0b4a`, `6dc4270`).

**Pipeline-refactor audit + QA guards (today).** `t191`/`t192`/`t193`/`t194` shipped:
Snakemake-visible mutation QA reports + `all_qa` target, a DAG-contract validation guard
(`all_workflow_qa`, which caught a missing `cosmic_cgc_path` pin in config-pan-cancer),
log-directive/conda-env normalization, and clean-base datapackage manifests for reusable
substrates (commits `2f01bf1`, `8a63fc7`).

**Literature-loss remediation.** `t184` recovered all 36 signature PDFs lost to the
2026-05-31 fuzzy-dedup bug; `t177` literature scan (gates h08) closed.

## Current State

**Overall:** ~58 active entries in `tasks/active.md`. Almost everything is `proposed`;
notable non-proposed: `t055`, `t127`, `t190` (`deferred`), `t146`, `t187` (`blocked`).
The active queue is now dominated by two clusters: the **h08 signature program**
(t178–t183) and **dataset acquisition** (t166–t172).

### P1 tasks (critical path)

| Task | Title | Status | Notes |
|---|---|---|---|
| t166 | Acquire Hartwig HMF metastatic WGS (~6k tumors) | proposed | DUA 3–6 mo lead time. Unblocks q009 WGS LRR-bias, h02 WES comparator, h05 atlas, RT residual at full scale. |
| t169 | Acquire GTEx v10 + Yizhak2019 / Rockweiler2023 healthy-tissue calls | proposed | Public-tier. The P1 ">2 OoM cross-tissue rate" claim in h05 needs this beyond Li2021-only. |
| t170 | Integrate PubTator + iCite + OpenAlex for h03 attention regression | proposed | Public APIs. Gates `t129`/`q011` partial-slope regression. |
| t171 | External validation: IntOGen 2024 + DepMap | proposed | Public downloads. Unblocks `t146` (currently blocked) — removes Bailey-circularity caveat on the dNdScv headline. |

All four are `proposed` and none has started. **This is the structural bottleneck** (see Strategic Decision Point).

### P2 queue shape (clusters)

- **h08 signature program (input specification):** `t180` (APOBEC A3A+A3B joint + MMR-omikli), `t181` (treatment-exposed study flag), `t182` (SBS40-vs-SBS5 flagship, P3), `t183` (ERCC2 cross-checks, P3). The decomposition *layer* is hardened (t178/t179); these specify the *covariates* the scan will use.
- **dNdScv tail:** `t147` (hypermutator-stratified), `t148` (multi-cancer best-cancer field), `t155`/`q015` aggregator choice, `t159`/`t160`/`t161` spine-hygiene metadata fixes.
- **Normal-tissue / contamination:** `t150`/`t151` (WGS cohort audit + pilot), `t153` (CFS-vs-RT), `t127` (q008 quantitative pass, deferred).
- **commons-hygiene:** `t185` (~57 dataset-promotion validation errors), `t186` (topic datasets-field), `t187` (blocked on upstream `promote` tool bug, fb-2026-05-31-001/002).
- **signature-modality-expansion:** `t188` (indel-call census), `t189` (joint SBS+ID pilot), `t190` (CN/DBS, deferred).

### Blocked tasks

| Task | Blocked by | Notes |
|---|---|---|
| t146 | t171 (IntOGen/DepMap integration) | CGC arm already shipped (`2026-04-28-t146-external-validation-cgc.md`); IntOGen/Martincorena/DepMap arms wait on the dataset. |
| t187 | upstream `science commons promote` tool bug | `TypeError: unhashable type: 'dict'` + topic-abort; filed as feedback, can't proceed locally. |
| t134 | t133 (VAF availability audit) | carried from April. |

### Hypothesis / question status

All 10 hypotheses are `phase: proposed` — **none has been promoted to active/candidate on the
strength of a run**. 27 questions active, 1 deferred (q009). The signature cluster
(h08/h09/h10/h11, q018–q028) is fully specified on paper but has **zero executed results**.
The dNdScv-adjacent hypotheses (h01/h02/h03) have the most evidence (LOSO, CGC, RT, panel
interpretations from late April) yet remain `proposed`.

### Workflow Runs

No `datapackage.json` manifests exist for *run bundles* (the only 2 in the repo are inside
`results/brca-cmag/studies/*/expression/` — clean-base substrate manifests from `t193`, not
run-level provenance). Inferring run bundles from directory conventions (these are **not**
datapackage-grade provenance):

| Bundle | Interpretation | Note |
|---|---|---|
| `results/q008-quantitative-pass-2026-04-28/` | none | t127 deferred (documented in task body); no linking interpretation. |
| `results/brca-cmag/` | **none** | New BRCA expression+signature bundle; no `doc/interpretations/` link. Flag. |
| `results/t052-stage-stratified-2026-04-25/` + `…-validation/` | `2026-04-25-t052-stage-stratified-ar-esr1.md` | linked. |
| `results/t126-sbs1-lrr-bias-2026-04-24/` | `2026-04-24-t126-sbs1-lrr-bias-per-study.md` | linked. |
| `results/signature-brca-2026-04-22/` | `2026-04-22-t110-sbs1-sbs5-brca-comparison.md` | linked. |
| `results/poc-2026-04-17/` | `2026-04-17-poc-run.md` | linked. |

`brca-cmag` is an unlinked run bundle and `q008-quantitative-pass` has no interpretation.

## Coverage Gaps

### Coverage Map

| Area | Coverage | Direction | Key Gap |
|---|---|---|---|
| dNdScv / driver ranking | Strong | improving | t144/t145/t141 shipped; LOSO+CGC done. External validation (t146/t171) still partial. |
| Cross-study aggregation + pipeline QA | Strong | improving | t191–t194 QA guards + DAG-contract validation + clean-base manifests landed today. |
| Signature **decomposition layer** (infra) | Strong | **new** | t178/t179 hardened the exposure step (version pin, count floor, caller flag, refit decision). |
| Signature **h08 scan** (exploitation) | Missing | **new** | The agnostic association scan has **never run** — no h08 interpretation exists. Built-but-unexploited, mirroring the April t111 gap. |
| External / WGS-tier datasets | Missing | **new** | 4 P1 acquisition tasks (t166/t169/t170/t171), all proposed. Spine has outrun data on hand. |
| Hypothesis spine breadth vs depth | Partial | regressing | 10 hypotheses / 28 questions, **0 promoted on evidence**. Breadth grew ~3×; depth (executed verdicts) did not keep pace. |
| Workflow provenance / run manifests | Missing | stable | Run-bundle manifests still absent (t128 open since April); t193 added substrate-level manifests but not run-level. |
| Literature-attention (h03/q011) | Partial | stable | t129 regression blocked on t170 data integration. |
| Normal-tissue atlas (h05) | Partial | stable | Li2021-only; t150/t151/t169 unstarted. |
| Task-state fidelity | Partial | **regressing** | t178/t179 marked done in commit + AGENTS.md but still `proposed` in active.md (see Status Drift). |

### High-Impact Gaps

**Gap 1 — The h08 signature scan is built-but-unrun.** The decomposition layer is now
audited and hardened (t178/t179, the whole point of the late-May work), the method doc
exists, and per-sample exposures are produced. But **no h08 agnostic-association scan has
been executed** — there is no interpretation document reporting positive-control recovery
of any known aetiology (SBS2/13↔APOBEC, SBS4↔smoking, SBS7↔UV, MMR↔MSI). This is the exact
"infrastructure landed, never exploited" pattern flagged for t111 on 2026-04-27, now
recurring one layer up. **It is also the cheapest high-value move on the board**: the data
(MC3 + existing cBioPortal exposures) is already on disk.

**Gap 2 — The hypothesis spine has outrun the data.** 10 hypotheses and 28 questions, with
four P1 dataset acquisitions (Hartwig, GTEx-family, PubTator-family, IntOGen/DepMap) gating
h02/h03/h05/h08. Two of those (Hartwig t166, any controlled-tier) carry **3–6 month DUA
calendar latency**. Adding hypotheses is cheap; promoting them requires data that isn't here
yet. No hypothesis has been promoted past `proposed`.

**Gap 3 — h08 covariate specification is unfinished.** Before the scan can be credible,
`t180` (joint APOBEC + MMR-omikli) and `t181` (treatment-exposed flag — needed so iatrogenic
SBS11/31/35/87 don't contaminate the positive-control arm) should land. These are the
remaining *inputs* to Gap 1's scan.

**Gap 4 — Run-level provenance still missing (carried since April).** t128 has been open
across multiple sessions; `brca-cmag` and `q008-quantitative-pass` are unlinked bundles.
t193 added *substrate* manifests but not *run* manifests.

**Gap 5 — commons-hygiene validation debt.** ~57 `dataset-promotion` validation errors
(t185) plus 35 `[UNVERIFIED]` markers, 3 broken citation refs, 881 bare-author-year prose
lints, and a discussions-section gap in the 2026-05-30 immune-causes discussion. Health
reports 8 issues. None blocking, but accreting.

## Status Transitions

**Recommendations shipped since 2026-04-27 (positive follow-through):**
- `t144` dNdScv tiebreaker ✓ — done (Apr).
- `t145` mean_inclusive inflation diagnostic ✓ — done (Apr).
- `t141` R `mclapply` parallelization ✓ — done (Apr).
- `validate.sh` update ✓ — now `current` at `2026.05.21.1`.

**Newly unblocked:** none structurally — the new P1s (t166/t169/t170/t171) are unblocked but
unstarted; their blocker is calendar/effort, not a dependency.

**Newly blocked:** `t146` is now explicitly `blocked` on `t171` (was `proposed` in April);
the CGC arm shipped, the independent-benchmark arms wait on dataset integration.

**Newly irrelevant / pruning:** the entire 2026-04-27 Strategic Decision Point (what to do
with the t131 dNdScv run) is resolved — patch-and-ship happened, LOSO + CGC validation
followed. That decision is closed.

### Status Drift (mandatory audit)

Audited `proposed`/`blocked`/`in_progress` tasks against commits, `tasks/done/`, results, and
interpretations.

| Task | Current status | Evidence | Suggested update |
|---|---|---|---|
| t178 | proposed | commit `251b7b3` "mark t178/t179 done"; AGENTS.md documents t178 as landed; code in `run_restricted_sigprofiler_assignment.py` | mark `done`, add `completed: 2026-05-31`, archive |
| t179 | proposed | commit `02a0b4a`; task body has "**Done 2026-05-31 (commit 02a0b4a)**"; AGENTS.md documents the count-floor + refit-decision feature | mark `done`, add `completed: 2026-05-31`, archive |

This is genuine drift: a commit *titled* "mark t178/t179 done" landed, but the `status:`
field in `active.md` was never flipped. AGENTS.md already treats both as shipped features.

**Archive lag** (`science health`): `done_in_active = 2` (t177, t184) — and **+2 more once
t178/t179 are corrected** → 4 to archive. Preview with `science tasks archive`, then
`science tasks archive --apply`. `missing_completed = 0`, so routing is clean.

## Task Tracking Gaps

- `doc/plans/` carries large unfiled design docs from the 2026-04-30 federation/cancer-meta
  work (`federation-v1-plan.md` 74 KB, `cancer-phase-2-migration-plan.md` 35 KB,
  `cancer-meta-project-design.md` 25 KB). These appear to belong to a sibling `cancer-meta`
  project (present in the sync registry) rather than cbioportal. Worth confirming they're
  not orphaned implementation work that should be tracked or relocated.
- The h08 program has a method doc and an analysis-relevant cluster (t178–t183) but **no
  `doc/plans/*-analysis-plan.md` and no pre-registration** for the actual association scan.
  Since the next move is running a pre-registered positive-control scan, this is a
  `/science:plan-analysis` + `/science:pre-register` gap (see Recommended Next Actions).

## Strategic Decision Point

**The fork: run depth now on data in hand, or wait on breadth-enabling data acquisition.**

The project has spent a month building signature-program *breadth* — 5 new hypotheses, 11
new questions, 60+ paper summaries, a hardened decomposition layer — without executing a
single signature-program *result*. Simultaneously, four P1 dataset acquisitions sit unstarted,
two with multi-month DUA latency.

**Evidence bearing on it:** the h08 decomposition layer is hardened and the inputs (MC3 +
cBioPortal exposures) are already on disk. A first positive-control scan does **not** require
Hartwig, GTEx, or IntOGen — those expand coverage but aren't prerequisites for testing whether
the scan recovers *known* aetiologies. Conversely, Hartwig (t166) and any controlled tier
carry 3–6 months of calendar latency that only starts when the DUA is filed.

**Options:**
- **A — Depth first.** Pre-register and run a first h08 positive-control scan on MC3 +
  existing exposures now. Promotes h08 from paper to evidence; validates the whole late-May
  investment. Low cost, high information.
- **B — Breadth/data first.** Start the long-lead-time DUAs (t166 Hartwig, t169 GTEx) so the
  3–6 month clock runs in the background. Necessary eventually but produces no near-term result.
- **C — Both, sequenced.** Run A now; in parallel file the t166/t169 DUAs so calendar latency
  burns while the scan runs.

**Recommendation: C.** Run the h08 positive-control scan this session-block (Option A is the
single highest-information, lowest-cost move and de-risks the entire signature pivot), and
*on the same day* file the Hartwig + GTEx data requests so their multi-month latency overlaps
the analysis work rather than following it. Defer t170/t171 integration until after the first
scan tells us which covariates actually matter — don't build all four dataset pipelines before
the first result says which are load-bearing.

## Recommended Next Actions

| Priority | Action | Rationale | Command |
|---|---|---|---|
| P1 | Pre-register + run a first **h08 positive-control scan** on MC3 + existing exposures | The decomposition layer is hardened but never exploited; recovering known aetiologies (APOBEC, smoking, UV, MMR) is the cheapest validation of the whole late-May pivot and needs no new data | `/science:plan-analysis` then `/science:pre-register` (new analysis-plan for h08) |
| P1 | Fix status drift: mark **t178/t179 done** + archive 4 done-in-active tasks | Commit + AGENTS.md treat t178/t179 as shipped; active.md still says `proposed` | `science tasks complete t178 t179` then `science tasks archive --apply` |
| P1 | File **Hartwig (t166)** + **GTEx-family (t169)** data requests now | 3–6 mo DUA latency should run in the background, not block later | start DUA paperwork; mark `t166`/`t169` `in_progress` |
| P2 | Land **t180** (joint APOBEC + MMR-omikli) and **t181** (treatment-exposed flag) before the scan goes beyond positive controls | These are the load-bearing covariate inputs; t181 prevents iatrogenic SBS contaminating the scan | implementation session for `t180`, `t181` |
| P2 | Link or document the **`brca-cmag`** + **`q008-quantitative-pass`** run bundles; close **t128** for run-level manifests | Two unlinked bundles; provenance gap open since April | write interpretation stubs + `datapackage.json` (`science:data`) |
| P3 | Clear **commons-hygiene** debt: t185 (~57 dataset-promotion errors), 3 broken citation refs, discussions-section gap in the 2026-05-30 immune-causes doc | Accreting validation debt; none blocking | implementation session for `t185`; fix the 2 missing discussion sections |
| P2 | Confirm whether the 2026-04-30 federation/cancer-meta plans in `doc/plans/` belong to a sibling project; relocate or track | 134 KB of untracked design docs possibly orphaned in this repo | manual triage; `science:sync` if cross-project |

> **Design/process note to record in memory:** the recurring failure mode this project keeps
> hitting is **infrastructure-landed-but-unexploited** — flagged for t111 on 2026-04-27, now
> recurring for the h08 signature layer. Worth a feedback/memory note that hardening an
> analysis layer should be immediately followed by a first exploiting run before the next
> layer is built.

## Session Summary

The 2026-04-27 → 2026-05-31 window was a **pivot, not an iteration**. The dNdScv driver-ranking
program that dominated April closed out cleanly (every prior recommendation shipped, LOSO + CGC
validation done), and the project's center of gravity moved wholesale to a mutational-signature
aetiology program: five new hypotheses, eleven new questions, a 60+ paper corpus, an h08 method
doc, a hardened-and-audited decomposition layer (t178/t179, today), and a pipeline-refactor QA
pass (t191–t194, today). The defining gap is that all of this is **breadth without a single
executed signature result** — the h08 scan has never run, no hypothesis has been promoted past
`proposed`, and four P1 dataset acquisitions sit unstarted, two with multi-month latency. The
strategic move is to run a first h08 positive-control scan on data already in hand *now* while
filing the long-lead-time DUAs in parallel — converting a month of accumulated infrastructure
into the project's first signature-program verdict. Minor but real: t178/t179 status drift and
a 4-deep archive lag need a hygiene pass.
