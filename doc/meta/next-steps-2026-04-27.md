---
id: "meta:next-steps-2026-04-27"
type: "meta"
title: "Next Steps — 2026-04-27"
created: "2026-04-27"
updated: "2026-04-27"
prior: "meta:next-steps-2026-04-24"
related: []
---

# Next Steps — 2026-04-27

## Recent Progress

- **q009 fork closed.** `t124` decided 2026-04-24; `t126` (SBS1 LRR-bias per-study test) ran and closed. The panel/WES proxy branch is retired with an explicit decision record rather than left open.
- **Main P1 cleared.** `t052` (per-study cohort-stage descriptor) shipped 2026-04-25 with two run artifacts (`t052-stage-stratified-2026-04-25/`, `t052-validation-2026-04-25/`) and an interpretation document (`2026-04-25-t052-stage-stratified-ar-esr1.md`). The aggregation spine no longer carries an open documented bias lever.
- **Co-occurrence / mutual-exclusivity landed.** `t078` (DISCOVER/WeSME + Stouffer) closed 2026-04-25 with unit tests + DAG dry-run validation; production wiring deferred to `t137` (gaps surfaced when attempting end-to-end run).
- **Full pan-cancer dNdScv run completed and interpreted.** `t131` ran end-to-end (12+ hr meta-analysis) and produced `2026-04-26-t131-full-pan-cancer-dndscv-run.md`. The interpretation surfaced **two new P1 bugs** (`t144` tiebreaker, `t145` mean_inclusive inflation) and **three perf bottlenecks** (`t141` R mclapply, `t142` corr-matrix O(n²), `t143` dndscv install race).
- **Canalization synthesis branch.** Eight new paper summaries (Harlapur2026, Nagpal2022, Jung2025, Bavisetty2025, Rashid2025, plus three more) plus a cross-paper synthesis (`synthesis-2026-04-25-canalization-gene-regulatory-networks.md`). Surfaced `t138` interpretive cross-link to t081 hypermutator topic.
- **Three new questions.** `q011` (gene length × literature attention) and `q012` (mutation ordering from cross-sectional data) added; q009 still listed as active in the index but operationally retired.
- **Conventions / framework hygiene.** `t140` filed (project already converges on Science 2026-04-25 P1 conventions, no migration work needed). Validate.sh updated to v2026.04.26.3 — but health check now reports it stale at v2026.04.26.5 (1 version behind).

## Current State

**Overall:** ~32 active tasks (was 27 on 2026-04-24): **2 P1, ~13 P2, ~17 P3**. All `proposed` except `t055` (`deferred`). One blocked task (`t134` on the VAF audit `t133`; `t135` blocked on `t078` which is now done).

### P1 tasks

| Task | Title | Status | Notes |
|---|---|---|---|
| t144 | Fix dNdScv per-gene aggregation tiebreaker | proposed | Surgical fix; validated outcome (62/100 Bailey recovery, TP53/KRAS/PIK3CA at ranks 1–9). No re-compute needed — re-run only `aggregate_dndscv_per_gene` + `join_dndscv_into_annotated` + `compare_three_way_rankings`. |
| t145 | Diagnose pooled-meta-analysis `mean_inclusive` inflation | proposed | snoU13/Y_RNA/CFS-genes (LSAMP, MACROD2, FHIT, …) at 65–84% per their best cancer; Bailey top-100 recovery = 0. Root-cause split: t139 callability-nesting bypass vs upstream `build_pooled_gene_cancer_input`. Diagnostic re-run on 3–5 cancers. |

### P2 queue shape

- **t131 follow-ups (new since last analysis):** `t141` (R mclapply), `t146` (external validation IntOGen/Martincorena), `t147` (hypermutator-stratified dNdScv), `t139` (promote t077 to canonical aggregation), `t136` (GRCh38 liftover at ingestion).
- **t078 production wiring:** `t137` (samples_annotated, gene_sample_long, schema mismatches, smoke run).
- **q011 length×attention branch:** `t129` (regression pipeline step), `t130` (Stoeger 2018 paper summary).
- **q012 ordering branch:** `t132` (methods literature search), `t133` (VAF availability audit — gates `t134`).
- **Carried over from 2026-04-24:** `t082`, `t083`, `t087`, `t090`, `t103`, `t104`, `t106`, `t107`, `t108`, `t114`, `t127` (q008 first quantitative pass), `t128` (retroactive `datapackage.json`).

### Blocked Tasks

| Task | Blocked by | Notes |
|---|---|---|
| t134 | t133 (VAF availability audit) | Decision rule is in t133: gate retention on ≥50% sample VAF coverage. |
| t137 (effectively) | t081 producing `samples_annotated.feather` for the 10k dataset | t081 hypermutator pipeline needs to run on 10k config. |

### Hypothesis / question status

12 active questions (q001–q012); `q009` operationally retired via `t124` but still listed `active` in the index — minor curation lag. q011, q012 are new and have task seeding (`t129`/`t130`/`t132`/`t133`/`t134`/`t135`). q007/q008/q010 still no first quantitative result against `t111` reference spectra (`t127` filed but unstarted). `specs/hypotheses/` remains empty.

### Workflow Runs

`results/` directory — no `datapackage.json` manifests anywhere. Inferring from directory conventions:

| Bundle | Mtime | Interpretation | Note |
|---|---|---|---|
| `results/poc-2026-04-17/` | 2026-04-17 | `2026-04-17-poc-run.md` | t100 PoC; no manifest (recurring gap, see `t128`) |
| `results/signature-brca-2026-04-22/` | 2026-04-22 | `2026-04-22-t110-sbs1-sbs5-brca-comparison.md` | no manifest |
| `results/t126-sbs1-lrr-bias-2026-04-24/` | 2026-04-24 | `2026-04-24-t126-sbs1-lrr-bias-per-study.md` | no manifest |
| `results/t052-validation-2026-04-25/` | 2026-04-25 | `2026-04-25-t052-stage-stratified-ar-esr1.md` | no manifest |
| `results/t052-stage-stratified-2026-04-25/` | 2026-04-25 | same as above | no manifest |

A **t131 full pan-cancer-dndscv** run is referenced in `2026-04-26-t131-full-pan-cancer-dndscv-run.md` but has no clearly-named directory under `results/` — its outputs are inferred to live in the canonical pipeline `out_dir`, not a date-stamped run bundle. Manifests gap is now 5 bundles deep.

## Coverage Gaps

### Coverage Map

| Area | Coverage | Direction | Key Gap |
|---|---|---|---|
| Cross-study aggregation implementation | Strong | **stable** | Spine landed; t139 promotion to canonical is now the structural improvement to make. |
| dNdScv-based driver detection | Partial | **new** | First full pan-cancer run produced ranking + interpretation but two ranking-quality bugs (t144, t145) block headline use. |
| Workflow provenance / retained run artifacts | Missing | **regressing** | 5 run bundles, 0 manifests. Was 2 → 3 → 5 across the last three sessions. t128 still open. |
| Question formalization / hypothesis spine | Partial | **stable** | 12 q*; `specs/hypotheses/` still empty. q009 retirement is in a task close note, not in q009.md. |
| Task-state fidelity | Strong | **stable** | No drift detected (see Status Drift). |
| Normal-tissue / signature-analysis branch | Partial | **stable** | `t111` infrastructure still unexploited; `t127` filed 2026-04-24 has not moved. |
| Length × attention / mutation-ordering | Partial | **new** | Two new questions (q011, q012) seeded with tasks; nothing executed yet. |
| Pipeline performance / scalability | Missing | **new** | t141/t142/t143 surfaced as concrete bottlenecks during the t131 full run; meta-analysis at 12+ hr blocks iteration. |
| External validation of pipeline outputs | Missing | **new** | t131 interpretation flagged Bailey-driver-recovery circularity; `t146` filed but unstarted. |

### High-Impact Gaps

**Gap 1 — Two ranking-quality bugs make the t131 headline run unfit to ship.**
`t144` (alphabetical tiebreaker on q=0 ties) and `t145` (pooled-meta `mean_inclusive` dominated by snoU13/Y_RNA/fragile-site genes at 65–84%) together drop Bailey driver recovery to 0/100 in the raw and length-adjusted columns and to 29/100 in the dNdScv column. This is the highest-leverage open work: cheap fixes against a finished run.

**Gap 2 — Pipeline iteration is bounded by a 12+ hour serial step.**
`t141` (R `lapply` → `mclapply`) is the highest-leverage perf change on the board. Until it lands, every t141/t145/t147 diagnostic re-run takes 12+ hours of single-core CPU. Compounds with `t142` (correlation matrix) and `t143` (dndscv install race) but is the dominant term.

**Gap 3 — Workflow-provenance gap is now five bundles deep.**
Five run directories, zero manifests. The recurring finding has been flagged in three consecutive next-steps. `t128` is the dedicated remediation task.

**Gap 4 — `t111` normal-tissue infrastructure remains unexploited.**
9 days since `t111` landed (2026-04-18). `t127` (first q008 quantitative pass) was filed 2026-04-24 and has not moved. q007/q008/q010 are still infrastructure-only. This is the same "built-but-unexploited" gap flagged on 2026-04-24 — direction has not improved.

**Gap 5 — External validation of dNdScv ranking is still open.**
`t146` (validate against IntOGen / Martincorena / CGC tier 1, none of which use dNdScv as input) is required before the t131 ranking can be used as a project headline output without circularity caveats.

### Status Transitions

**Newly unblocked since 2026-04-24:**
- `t135` (MHN fit per histology) — blocking dependency `t078` is now done. Task body still lists `blocked-by: [t078]` and should be cleaned up.

**Newly blocked since 2026-04-24:**
- None new at the structural level. `t134` (retain VAF) gates on `t133` (VAF audit) — both filed in this window.

**Newly irrelevant / pruning opportunities:**
- 2026-04-24 recommendation *"Resolve `t124` (q009 fork)"* is resolved (`t124` closed 2026-04-24).
- 2026-04-24 recommendation *"Execute `t052`"* is resolved (closed 2026-04-25).
- 2026-04-24 recommendation *"Refresh cross-project sync"* is resolved (sync is now 0 days stale, ran today 05:30 UTC).
- The "`t128` retroactive datapackage.json" recommendation persists — and the gap has grown from 2 → 5 bundles. Re-recommend.

### Status Drift

Mandatory audit performed. Scanned `tasks/active.md` against `results/`, `doc/interpretations/`, recent git log (since 2026-04-24).

**No drift detected.** `t135`'s body lists `blocked-by: [t078]` after `t078` closed — cosmetic, but worth fixing on next pass. No `proposed`/`blocked`/`in_progress` task in `active.md` has matching evidence of completion.

### Managed artifact updates

`science-tool health` reports `validate.sh` 1 version behind:

> Update `validate.sh` from `2026.04.26.3` → `2026.04.26.5`. Run:
>
> ```bash
> science-tool project artifacts update validate.sh
> ```
>
> If a migration step ships with the bump, the CLI will surface it interactively.

## Strategic Decision Point

**Decision:** what to do with the t131 full pan-cancer-dndscv run.

The run is the single largest pipeline event since the aggregation spine landed. The interpretation surfaced two cleanly-bounded bugs (`t144`, `t145`), two perf concerns (`t141`, `t142`), one external-validation gap (`t146`), and one design follow-up (`t139` — promote t077 meta-analysis to canonical so dNdScv joins onto a well-founded aggregation). The decision is whether to:

**Option A — Patch-and-ship the existing run.** Land `t144` (fully validated fix, no re-compute) + `t145` diagnostic on a small subset; if `t145`'s root cause is t139's callability bypass, fold it into `t139` and ship a t139'd re-run. End state: a credible pan-cancer ranking with an external-validation footnote (`t146`) attached.

**Option B — Optimize first, then re-run.** Execute `t141` (R parallelization), `t142` (correlation matrices), then re-run end-to-end. Any number of follow-up bug fixes after that come at 1–2 hour rather than 12+ hour iteration cost. Higher up-front cost but unlocks `t147` (hypermutator-stratified) and any future re-runs.

**Option C — External validation first.** Run `t146` against the *current* (buggy) ranking to characterize where the bugs hurt vs where they don't, then fix t144/t145.

**Recommendation: Option A first, then Option B.** `t144` is a one-commit fix with validated outcome. `t145` diagnostic is bounded (3–5 cancer types). Both should land before any infrastructure investment so the next full re-run is run on a known-good codebase. Option B is the right second move: the 12+ hour ceiling will compound once `t146`/`t147` enter the queue. Option C is implicitly subsumed — `t146` becomes obviously valuable after t144/t145 are closed.

## Recommended Next Actions

| Priority | Action | Rationale | Command |
|---|---|---|---|
| P1 | Fix `t144` dNdScv tiebreaker (lexicographic sort `(min_qglobal ASC, n_cancers_significant_q05 DESC)`) and re-run only `aggregate_dndscv_per_gene` + downstream rules | Validated outcome (TP53/KRAS/PIK3CA at ranks 1–9, 62/100 Bailey recovery). Cheapest credible improvement to the headline pan-cancer ranking. | implementation session for `t144` |
| P1 | Execute `t145` diagnostic — re-run meta-analysis on 3–5 cancers with `enforce_callability_nesting_check=true` and compare top-15 raw `mean_inclusive` ranking | Determines whether the inflation is a `t139`-induced regression (escalate `t139` to P1) or upstream of `build_pooled_gene_cancer_input` | `/science:plan-analysis t145` then implementation session |
| P2 | Land `t141` R `mclapply` swap before any further full re-run | Single change unlocks the 12+ hr → ~2 hr meta-analysis cycle. Compounds with all other follow-ups. | implementation session for `t141` |
| P2 | First q008 quantitative pass (`t127`) using `t111` reference spectra against `tcga_mc3` vs `msk_impact_2017` | `t111` infrastructure has been unexploited for 9 days; one targeted run gets q007/q008/q010 out of infrastructure-only status | `/science:plan-analysis t127` then implementation |
| P2 | Emit retroactive `datapackage.json` (`t128`) for all 5 result bundles | Recurring gap flagged 3 sessions running; bundle count grew 2 → 3 → 5. ~30 min remediation. | implementation session for `t128` |
| P3 | Update managed artifact `validate.sh` to `2026.04.26.5` | Health check shows 1 version stale | `science-tool project artifacts update validate.sh` |
| P3 | Curation: clean stale `blocked-by: [t078]` line in `t135`; mark `q009` status `retired` to match the `t124` close decision | Index-level fidelity drift only; cheap hygiene | task edit + question edit |

## Session Summary

The 2026-04-24 → 2026-04-27 window was an execution-heavy block: the q009 fork closed (`t124`), the only open P1 (`t052`) shipped, `t078` landed unit-tested, and the first full pan-cancer dNdScv run completed end-to-end. That run is now the new strategic centerpiece — and it surfaced two ranking-quality bugs (`t144`, `t145`) plus three perf bottlenecks (`t141`, `t142`, `t143`) that together define the next session's work. The recommended sequence is patch-and-ship the existing run via `t144` and the `t145` diagnostic, then invest in `t141` parallelization before any further full re-run. The `t111` "built-but-unexploited" risk and the `t128` provenance-manifest gap have both worsened by one tick and need to enter rotation.
