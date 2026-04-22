---
type: "curation-sweep"
generated_at: "2026-04-22T18:54:12-04:00"
source_commit: "47d5528f6b66daa78afab492361b2af45f41b2a3"
scope: "all"
since: null
mode: "propose"
applied_changes: 0
pending_decisions: 4
---

# Curation Sweep — 2026-04-22

## Executive Summary

- The main curation issue is no longer backlog drift alone; it is metadata drift around newly landed April 22 work, especially `q009`, `t077`, and dataset/provenance docs.
- `science-tool dag audit` is clean. The highest-signal curation findings are semantic linking gaps and profile/tooling mismatches, not DAG freshness failures.
- Two unresolved refs from `science-tool health` are high-confidence metadata problems, both caused by canonical docs lacking machine-resolvable IDs:
  - `doc:2026-04-22-t077-glmm-logit-plan`
  - `doc:replication-timing-constitutive-regions`
- `question:q009-sbs1-lrr-bias-as-normal-contamination-flag` is now semantically behind the codebase: it still frames `t121` as the current entry point and does not incorporate the negative `t123` screening result or the new `t124` decision point.
- The project relies on several document kinds that the current profile/tooling does not register cleanly (`meta`, `pre-registration`, `synthesis`, `guide`, `modality-guide`). This now produces persistent health noise and weakens curation signal quality.
- `doc/interpretations/2026-04-18-t070-poc-comparison.md` remains a conspicuous metadata outlier: no frontmatter, no machine ID, no `related`, and no `source_refs`, despite being an important validation artifact.
- `doc/interpretations/2026-04-17-poc-run.md` is better linked than the `t070` note, but still lacks `source_refs` even though it makes several evidence-bearing claims that now anchor downstream task decisions.
- No source artifacts were edited in this sweep. All findings below are recorded as proposals or safe-obvious candidates pending approval.

## Corpus Inventory

Deterministic inventory from `uv run science-tool curate inventory --project-root . --format json`:

- datasets: 2
- interpretations: 6
- knowledge sources: 3
- papers: 10
- plans: 9
- questions: 10
- specs: 1
- tasks: 124
- topics: 1

Notable coverage gaps surfaced by inventory/health:

- missing `related`:
  - `doc/interpretations/2026-04-18-t070-poc-comparison.md`
  - `doc/papers/Poon2021.md`
- missing `source_refs`:
  - `doc/interpretations/2026-04-17-poc-run.md`
  - `doc/interpretations/2026-04-18-t070-poc-comparison.md`
- unresolved refs:
  - `doc:2026-04-22-t077-glmm-logit-plan` from `t115`–`t120`
  - `doc:replication-timing-constitutive-regions` from `t121`
- profile/tooling mismatch:
  - `science-tool health` skips `guide`, `modality-guide`, `meta`, `pre-registration`, and `synthesis` docs as unknown entity kinds
- additional structural noise:
  - many tasks still use legacy `type: dev|research` values, which `science-tool health` reports under `legacy_task_type`

## Forgotten Insights

### 1. `t070` validation note is still under-linked relative to its importance

- Source artifact: `doc/interpretations/2026-04-18-t070-poc-comparison.md`
- Why it matters now:
  - It validates the load-bearing denominator correction that made the later hypermutator and pooled-analysis work trustworthy.
  - It is a key bridge between `t070`, `t100`, `t105`, and the downstream `t076`/`t077` chain.
- Current issue:
  - The file has no frontmatter, no machine ID, and no `related`/`source_refs`, so inventory correctly flags it as a metadata outlier.

### 2. `Poon2021` has substantive framework relevance but no outbound `related`

- Source artifact: `doc/papers/Poon2021.md`
- Why it matters now:
  - It sharpens the argument that the current CH flag is a lower bound and remains relevant to `q006` and the blood/selection branch.
- Current issue:
  - `related: []` despite explicit conceptual links in the prose to `q006`, CH contamination, and dNdScv/selection interpretation.

## Missed Connections

### High-confidence, small, local candidates

1. Add a canonical frontmatter ID to `doc/plans/2026-04-22-t077-glmm-logit-plan.md`.
   - Source artifacts: `tasks/done/2026-04.md#t115`–`#t120`
   - Target artifact: `doc/plans/2026-04-22-t077-glmm-logit-plan.md`
   - Evidence: health unresolved ref `doc:2026-04-22-t077-glmm-logit-plan` appears 6 times from `t115`–`t120`.
   - Proposed action: add frontmatter with a resolvable `id`, likely `plan:2026-04-22-t077-glmm-logit-plan`, then update task refs to that canonical entity name.
   - Confidence: high
   - Applied: no

2. Add a canonical frontmatter ID to `doc/datasets/replication-timing-constitutive-regions.md`.
   - Source artifact: `tasks/done/2026-04.md#t121`
   - Target artifact: `doc/datasets/replication-timing-constitutive-regions.md`
   - Evidence: health unresolved ref `doc:replication-timing-constitutive-regions`.
   - Proposed action: add dataset frontmatter with a resolvable `id`, then convert the `t121` reference to that canonical dataset ID.
   - Confidence: high
   - Applied: no

3. Link `question:q009-sbs1-lrr-bias-as-normal-contamination-flag` to the new negative-result chain.
   - Source artifacts:
     - `doc/questions/q009-sbs1-lrr-bias-as-normal-contamination-flag.md`
     - `doc/interpretations/2026-04-22-t122-rt-brca-pilot.md`
     - `doc/interpretations/2026-04-22-t123-rt-brca-sbs1-proxy-pilot.md`
     - `tasks/active.md#t124`
   - Proposed action:
     - add `t122`, `t123`, and `t124` as explicit links in the q009 doc
     - update “Current implementation entry point” language so it reflects the actual current state, not the earlier `t121` entry point
   - Confidence: high
   - Applied: no

4. Add outbound `related` to `doc/papers/Poon2021.md`.
   - Suggested links:
     - `question:q006-ch-priority-gene-completeness`
     - `topic:clonal-hematopoiesis-contamination`
     - possibly `paper:Martincorena2018` and/or `paper:LeeSix2018`
   - Confidence: high
   - Applied: no

### Medium-confidence semantic candidates

5. Add `source_refs` to `doc/interpretations/2026-04-17-poc-run.md`.
   - Evidence:
     - the interpretation makes evidence-bearing claims about Campbell thresholds, TCGA UCEC validation, and MSK TMB denominator failure
   - Proposed action:
     - add explicit paper/task refs only after a short pass confirms the smallest sufficient set
   - Confidence: medium
   - Applied: no

6. Normalize `doc/interpretations/2026-04-18-t070-poc-comparison.md` into the same frontmatter/linking shape as the other interpretation docs.
   - Proposed action:
     - add interpretation frontmatter, `id`, `related`, and `source_refs`
   - Confidence: medium
   - Applied: no

## Drift

### 1. `q009` narrative drift after `t122` and `t123`

- Source artifacts:
  - `doc/questions/q009-sbs1-lrr-bias-as-normal-contamination-flag.md`
  - `doc/interpretations/2026-04-22-t122-rt-brca-pilot.md`
  - `doc/interpretations/2026-04-22-t123-rt-brca-sbs1-proxy-pilot.md`
  - `tasks/active.md#t124`
- Drift:
  - q009 still says the “current implementation entry point” is `task:t121`.
  - It records the negative `t110` result, but not the newer `t122` mixed result, the negative `t123` screening result, or the explicit `t124` fork decision.
- Impact:
  - A reader entering through q009 will overestimate how early this branch still is and miss the newly established negative constraint: the simple panel/WES CpG proxy is too sparse.

### 2. Tool/profile drift is obscuring real health signals

- Evidence:
  - `science-tool health` skips multiple project-native kinds as unknown:
    - `meta`
    - `pre-registration`
    - `synthesis`
    - `guide`
    - `modality-guide`
- Impact:
  - repeated warning noise makes it harder to spot genuine unresolved refs and metadata regressions
  - curation quality is now bounded by profile registration, not just by corpus quality

### 3. Legacy task typing remains an unresolved migration tail

- Evidence:
  - `science-tool health` still reports many `legacy_task_type` entries in both `tasks/active.md` and `tasks/done/2026-04.md`
- Impact:
  - health output is noisier than necessary
  - future sweeps will keep re-surfacing a structural issue that is not about research meaning

## Duplication and Fragmentation

- No major topic duplication was found in this sweep.
- The more relevant fragmentation is provenance fragmentation:
  - key state transitions are spread across `doc/meta/next-steps-2026-04-22.md`, task notes, and interpretations
  - some of those artifacts are not machine-discoverable because their kinds or IDs are not registered cleanly
- The `q009` branch is the clearest example:
  - the true current state is distributed across `t121`, `t122`, `t123`, `t124`, the dataset doc, and two interpretations
  - the question file has not yet been brought back into alignment

## Actioned Fixes

None in this sweep.

Reason:

- the user did not request `--apply-obvious`
- the high-confidence fixes are small and local, but still change source metadata
- they are therefore recorded here as ready-to-apply candidates rather than edited directly

## Pending Decisions

1. Apply the two obvious canonical-ID fixes now?
   - `doc/plans/2026-04-22-t077-glmm-logit-plan.md`
   - `doc/datasets/replication-timing-constitutive-regions.md`

2. Normalize `q009` immediately, or wait until `t124` decides whether the panel/WES proxy route is retired?
   - My view: update now. The question doc is already behind known evidence.

3. Should the project register or local-override the currently skipped entity kinds?
   - `meta`, `pre-registration`, `synthesis`, `guide`, `modality-guide`
   - This is not just cosmetic anymore; it affects health/curation signal quality.

4. Is the legacy task-type migration worth a dedicated cleanup task, or should it be folded into a larger science-tool migration sweep?
   - Current health output suggests the tail is large enough that ad hoc cleanup will stay noisy.

## Suggested Follow-Ups

- Short curation apply pass:
  - add frontmatter IDs to the `t077` plan doc and the replication-timing dataset doc
  - fix the corresponding task refs
- Short semantic update pass:
  - refresh `doc/questions/q009-sbs1-lrr-bias-as-normal-contamination-flag.md` with `t122`, `t123`, and `t124`
- Tooling cleanup:
  - decide whether to add project-local support for the skipped document kinds or explicitly map them to registered kinds
- Optional metadata cleanup:
  - add frontmatter/linking to `doc/interpretations/2026-04-18-t070-poc-comparison.md`
  - add `related` to `doc/papers/Poon2021.md`

## Self-Reflection

What made this sweep harder than it should have been:

1. `science-tool health` mixes high-value findings with expected profile noise.
   - Friction:
     - the unresolved refs were useful, but they were surrounded by repeated “unknown entity kind” warnings for document classes the project already uses intentionally.
   - Smallest improvement:
     - let projects register local entity-kind aliases in `science.yaml` or `.ai/` so health can treat those docs as first-class rather than always skipped.

2. Inventory can detect missing links, but not whether a question doc is semantically behind its downstream task/interpretation chain.
   - Friction:
     - `q009` drift was obvious to a human after reading `t122`/`t123`, but the deterministic scan could only hint at it indirectly.
   - Smallest improvement:
     - add an inventory heuristic for “question updated before newer related interpretations/tasks” so likely narrative drift surfaces earlier.

3. Missing canonical IDs on otherwise important docs create avoidable curation noise.
   - Friction:
     - the unresolved refs here were not conceptually hard; they were just consequences of plan/dataset docs without machine-resolvable IDs.
   - Smallest improvement:
     - a lightweight lint or template rule for `doc/plans/` and `doc/datasets/` requiring frontmatter IDs when the doc is intended to be referenced from tasks.

4. The skill asks to load `research-methodology` and `scientific-writing`, but those skill files were not present in the expected Science tree.
   - Friction:
     - the sweep could proceed, but the failure mode is silent unless the operator notices it.
   - Smallest improvement:
     - either ship those skills at stable paths or update the command preamble so missing helper skills are reported explicitly as optional rather than assumed present.

## Update — 2026-04-22 19:00 EDT

Applied the three high-confidence fixes from the original sweep:

- added canonical frontmatter IDs to:
  - `doc/plans/2026-04-22-t077-glmm-logit-plan.md`
  - `doc/datasets/replication-timing-constitutive-regions.md`
- updated task references to use canonical entities:
  - `plan:2026-04-22-t077-glmm-logit-plan`
  - `dataset:replication-timing-constitutive-regions`
- refreshed `question:q009-sbs1-lrr-bias-as-normal-contamination-flag` so it now reflects:
  - the mixed `t122` all-mutation RT result
  - the negative `t123` SBS1-proxy result
  - the new `t124` fork decision

Immediate outcome to verify:

- the 7 unresolved-reference failures from `science-tool graph audit` should now be gone
- the remaining health noise should mostly collapse to the broader document-kind/profile mismatch (`meta`, `pre-registration`, `synthesis`, `guide`, `modality-guide`, `curation-sweep`) rather than project-local broken links

## Update — 2026-04-22 19:15 EDT

Applied the next repo-contained cleanup after the link fixes:

- removed redundant legacy task `type:` fields from `tasks/active.md` and `tasks/done/2026-04.md`
  - verified beforehand that every affected task already carried `aspects:`, so this was a pure metadata cleanup rather than a semantic rewrite
- added follow-up task `t125` to track the remaining shared-profile/entity-kind problem that cannot be solved from this repo alone

Verification outcome:

- `uv run science-tool health --project-root . --format json` now reports:
  - `unresolved_refs: []`
  - `legacy_task_type: []`
- the only remaining health/graph noise is the unsupported document-kind set:
  - `meta`
  - `pre-registration`
  - `synthesis`
  - `guide`
  - `modality-guide`
  - `curation-sweep`

## Update — 2026-04-22 19:36 EDT

Applied the last two repo-local metadata fixes from this sweep:

- normalized `doc/interpretations/2026-04-18-t070-poc-comparison.md` into the standard interpretation frontmatter shape with a canonical ID, `mode`, `source_refs`, `related`, and `prior_interpretations`
- added outbound `related` links on `doc/papers/Poon2021.md` to the already-linked CH topic/question/paper cluster:
  - `topic:clonal-hematopoiesis-contamination`
  - `question:q006-ch-priority-gene-completeness`
  - `paper:LeeSix2018`
  - `paper:Martincorena2018`

Expected verification after this pass:

- `uv run science-tool graph audit --project-root . --format json` remains clean on unresolved refs
- `uv run science-tool health --project-root . --format json` continues to report only the shared-profile kind skips
- `git diff --check` remains clean

## Update — 2026-04-22 19:44 EDT

Applied one more consistency cleanup after a quick interpretation-schema scan:

- normalized `doc/interpretations/2026-04-17-poc-run.md` to match the newer interpretation contract by adding:
  - `mode: dev`
  - `source_refs`
  - `input`
  - `workflow_run`
  - `prior_interpretations`
- expanded its `related` links to include the immediate downstream fixes it actually surfaced (`task:t070`, `task:t105`)

This appears to close the last obvious repo-local interpretation-metadata mismatch from the 2026-04-22 curation sweep.
