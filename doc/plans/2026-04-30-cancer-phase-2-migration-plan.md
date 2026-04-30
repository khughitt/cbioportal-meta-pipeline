# Cancer Phase 2 Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix existing cbioportal/mm30 graph and validation blockers, then migrate cbioportal and mm30 into the cancer federation layout with a minimal meta project and time-boxed compatibility symlinks.

**Architecture:** Phase 2 is repair-first, then move. Each existing project must reach a clean graph/validation baseline before its directory is moved; the meta project is bootstrapped before child moves so `children:` and child `parent:` references can be validated immediately. The move order is mm30 first, cbioportal second, with one atomic commit per migrated project and one meta commit per manifest update.

**Tech Stack:** Git, POSIX shell, `uv`, `science-tool` federation v1.0, existing project `validate.sh`, existing Snakemake workflows where available.

---

## Non-Negotiable Safety Rules

- Do not overwrite uncommitted user work. If `git status --short` shows dirty files outside the current task's ownership, stop and ask the user how to handle them.
- Do not move a project directory unless that project's repair task is committed and its validation gate is documented.
- Do not rely on compatibility symlinks for repo-internal paths. Repo files must use new `~/d/cancer/...` / `/mnt/ssd/Dropbox/cancer/...` paths after migration.
- The compatibility symlinks expire on **2026-06-30**.
- Use `/home/keith/d/science/science-tool` as the upstream `science-tool` source after Phase 1. After moving children under `/mnt/ssd/Dropbox/cancer/...`, editable `pyproject.toml` paths must become `../../../science/science-tool`.

---

## Task 0: Preflight And Dirty-Work Gate

**Files:**
- Read-only: `/home/keith/d/science/`
- Read-only: `/home/keith/d/r/cbioportal/`
- Read-only: `/home/keith/d/r/mm30/`

- [ ] **Step 1: Verify Phase 1 is available on the main science checkout.**

```bash
cd /home/keith/d/science
git status --short --branch
cd science-tool
uv run --frozen science-tool federation --help
uv run --frozen pytest tests/test_federation_integration.py -q
```

Expected:
- `science-tool federation --help` lists `validate` and `status`.
- The integration test passes.

- [ ] **Step 2: Inventory dirty work in the two child projects.**

```bash
cd /home/keith/d/r/cbioportal
git status --short --branch

cd /home/keith/d/r/mm30
git status --short --branch
```

Expected current state before any repair:
- cbioportal has at least `M doc/plans/2026-04-30-federation-v1-plan.md`.
- mm30 may have dirty progression-script changes. These are user work unless the user explicitly assigns them to this phase.

- [ ] **Step 3: Stop if unowned dirty files block safe repair.**

If cbioportal or mm30 is dirty, notify the user with `ohai` and ask whether to:

```text
1. commit/stash the dirty work themselves,
2. let this phase include those files,
3. move the phase work into a fresh worktree once the dirty work is resolved.
```

Do not run `git stash`, `git checkout`, `git reset`, or `rm` on user work without explicit instruction.

- [ ] **Step 4: Record the preflight state in the Phase 2 run log.**

Create `doc/plans/2026-04-30-phase-2-run-log.md` in cbioportal with:

```markdown
# Phase 2 Run Log

## Preflight

- science commit: <output of `git -C /home/keith/d/science rev-parse --short HEAD`>
- cbioportal status: <summary>
- mm30 status: <summary>
- known blocker policy: repair graph/validation blockers before moves
```

Commit the run log before repair work starts so later steps have a durable place to append evidence:

```bash
cd /home/keith/d/r/cbioportal
git add doc/plans/2026-04-30-phase-2-run-log.md
git commit -m "docs: start cancer phase 2 migration run log"
```

The run log lives in cbioportal for this phase. During Task 4, mm30 inventory output is appended while cbioportal is
still at `/home/keith/d/r/cbioportal`; during Task 5, the run log moves with cbioportal to
`/mnt/ssd/Dropbox/cancer/data-sources/cbioportal/doc/plans/2026-04-30-phase-2-run-log.md`.

---

## Task 1: Fix cbioportal Graph And Validation Blockers

**Files:**
- Modify: `/home/keith/d/r/cbioportal/doc/interpretations/2026-04-27-t145-mean-inclusive-inflation-diagnostic.md`
- Modify: `/home/keith/d/r/cbioportal/doc/interpretations/2026-04-28-t146-external-validation-cgc.md`
- Modify: `/home/keith/d/r/cbioportal/doc/interpretations/2026-04-28-t149-loso-replication.md`
- Create: `/home/keith/d/r/cbioportal/models/README.md`
- Verify: `/home/keith/d/r/cbioportal/tasks/active.md`
- Verify: `/home/keith/d/r/cbioportal/tasks/done/2026-04.md`

Current known blockers:
- `science-tool graph build` fails because task references point to interpretation IDs that are not loaded as graph entities.
- `doc/interpretations/2026-04-28-t146-external-validation-cgc.md` and `2026-04-28-t149-loso-replication.md` have `id` but no `type: "interpretation"`.
- `doc/interpretations/2026-04-27-t145-mean-inclusive-inflation-diagnostic.md` has no frontmatter, so `interpretation:2026-04-27-t145-mean-inclusive-inflation-diagnostic` is not a canonical entity.
- `bash validate.sh --verbose` reports missing required directory `models/`.

- [ ] **Step 1: Reproduce the cbioportal graph blocker.**

```bash
cd /home/keith/d/r/cbioportal
uv sync
SCIENCE_CONFIG_DIR=/tmp/science-phase2-cbioportal uv run science-tool graph build
```

Expected failure includes:

```text
Cannot materialize graph with unresolved references:
task:t146 -> interpretation:2026-04-28-t146-external-validation-cgc
task:t160 -> interpretation:2026-04-27-t145-mean-inclusive-inflation-diagnostic
task:t173 -> interpretation:2026-04-28-t149-loso-replication
task:t174 -> interpretation:2026-04-28-t146-external-validation-cgc
```

- [ ] **Step 2: Add canonical interpretation frontmatter to the t145 diagnostic.**

Edit the top of `doc/interpretations/2026-04-27-t145-mean-inclusive-inflation-diagnostic.md` so it begins with:

```markdown
---
id: "interpretation:2026-04-27-t145-mean-inclusive-inflation-diagnostic"
type: "interpretation"
title: "t145 mean-inclusive inflation diagnostic — stale pooled means before WES zero-fill caused raw ranking inflation"
status: "active"
source_refs:
  - "task:t145"
related:
  - "task:t145"
  - "task:t160"
  - "hypothesis:h02-cross-study-ranking-divergence-is-structured"
  - "question:q015-pan-cancer-aggregator-choice"
created: "2026-04-27"
updated: "2026-04-27"
---
```

Keep the existing body after the frontmatter unchanged.

- [ ] **Step 3: Add missing entity fields to t146.**

In `doc/interpretations/2026-04-28-t146-external-validation-cgc.md`, add these fields immediately after `id:`:

```yaml
type: "interpretation"
status: "active"
source_refs:
  - "task:t146"
```

Keep the existing title, date, related list, and body unchanged.

- [ ] **Step 4: Add missing entity fields to t149.**

In `doc/interpretations/2026-04-28-t149-loso-replication.md`, add these fields immediately after `id:`:

```yaml
type: "interpretation"
status: "active"
source_refs:
  - "task:t149"
```

Keep the existing title, date, related list, and body unchanged.

- [ ] **Step 5: Add a real models directory note.**

Create `models/README.md`:

```markdown
# Models

This project currently tracks analysis code, workflow outputs, and graph artifacts, but does not version fitted
statistical model binaries in the repository. Use this directory for durable model specifications or small model
artifacts when a future analysis promotes them to version-controlled project assets.
```

- [ ] **Step 6: Verify the fixed references are loadable.**

```bash
cd /home/keith/d/r/cbioportal
uv run science-tool graph audit --format json > /tmp/cbioportal-graph-audit.json
if rg '"status": "fail"' /tmp/cbioportal-graph-audit.json; then
  exit 1
fi
```

Expected:
- No `status: fail` rows remain. If failures remain, inspect `/tmp/cbioportal-graph-audit.json` and fix them before
  continuing.

- [ ] **Step 7: Re-run cbioportal graph build.**

```bash
cd /home/keith/d/r/cbioportal
SCIENCE_CONFIG_DIR=/tmp/science-phase2-cbioportal uv run science-tool graph build
```

Expected:
- Exit code 0.
- Output includes `Materialized graph at knowledge/graph.trig`.
- No `Materialized federated graph` line, because cbioportal is not yet `role: meta`.

- [ ] **Step 8: Re-run cbioportal validation.**

```bash
cd /home/keith/d/r/cbioportal
bash validate.sh --verbose
```

Expected:
- Exit code 0.
- Warnings may remain for stale graph inputs or unverified markers only if they are non-blocking. Any `ERROR:` output must be fixed before migration.

- [ ] **Step 9: Commit cbioportal repair.**

```bash
cd /home/keith/d/r/cbioportal
git add doc/interpretations/2026-04-27-t145-mean-inclusive-inflation-diagnostic.md \
  doc/interpretations/2026-04-28-t146-external-validation-cgc.md \
  doc/interpretations/2026-04-28-t149-loso-replication.md \
  models/README.md \
  knowledge/graph.trig
git commit -m "fix(graph): restore cbioportal interpretation references"
```

`knowledge/graph.trig` is regenerable, but this project currently commits graph materialization artifacts. Keeping it in
the same repair commit records the exact graph state validated by this task.

---

## Task 2: Fix mm30 Graph And Validation Blockers

**Files:**
- Modify: `/home/keith/d/r/mm30/doc/background/papers/Kumar2020BELLINI.md`
- Delete: `/home/keith/d/r/mm30/doc/papers/Kumar2020BELLINI.md`
- Create or move: `/home/keith/d/r/mm30/code/`
- Create: `/home/keith/d/r/mm30/models/README.md`
- Create: `/home/keith/d/r/mm30/results/README.md`
- Modify: five hypothesis specs listed below

Current known blockers:
- `science-tool graph build` fails because `paper:Kumar2020BELLINI` exists in both `doc/background/papers/` and `doc/papers/`.
- `bash validate.sh --verbose` reports missing `code/`, `models/`, and `results/`.
- Hypotheses `h1`, `h2`, `h3`, `h4`, and `h6` lack `## Falsifiability` sections.
- The mm30 worktree may already contain unrelated dirty progression edits. Do not proceed until user-owned dirty work is resolved or explicitly assigned.

- [ ] **Step 1: Reproduce the mm30 graph blocker.**

```bash
cd /home/keith/d/r/mm30
uv sync
SCIENCE_CONFIG_DIR=/tmp/science-phase2-mm30 uv run science-tool graph build
```

Expected failure includes:

```text
entity 'paper:Kumar2020BELLINI' produced by multiple sources:
  - [markdown] doc/background/papers/Kumar2020BELLINI.md
  - [markdown] doc/papers/Kumar2020BELLINI.md
```

- [ ] **Step 2: Consolidate the duplicate BELLINI paper entity.**

Keep `doc/background/papers/Kumar2020BELLINI.md` as the canonical file because `validate.sh` checks background paper summaries. Merge these unique values from `doc/papers/Kumar2020BELLINI.md` into the canonical file's `related:` list:

```yaml
  - "inquiry:h-treatment-1-venetoclax-bcl2"
  - "inquiry:h-treatment-4-pi-response"
  - "discussion:2026-04-26-treatment-axis-strategy"
  - "interpretation:2026-04-06-gdsc-drug-sensitivity"
```

Do not remove the existing `paper:Kumar2025BELLINI_FinalOS` relation or the `mm30_treatment_axis:` block from the canonical file.

- [ ] **Step 3: Remove the duplicate file.**

```bash
cd /home/keith/d/r/mm30
git rm doc/papers/Kumar2020BELLINI.md
```

- [ ] **Step 4: Create canonical execution/output directories without moving dirty scripts.**

If the user has not assigned the existing dirty `scripts/` work to this task, do not move `scripts/`. Create only the missing canonical roots:

```bash
cd /home/keith/d/r/mm30
mkdir -p code models results
```

Create `code/README.md`:

```markdown
# Code

The legacy execution root is currently `scripts/`. Phase 2 keeps that root in place until the active progression-script
worktree is clean. New or migrated execution code should land under this canonical `code/` root.
```

Create `models/README.md`:

```markdown
# Models

This project currently tracks analysis scripts, workflow outputs, and graph artifacts, but does not version fitted model
binaries in the repository. Use this directory for durable model specifications or small model artifacts when they become
project assets.
```

Create `results/README.md`:

```markdown
# Results

Use this directory for small, version-controlled result summaries. Large generated outputs remain outside the repository
or under the project's configured data package locations.
```

- [ ] **Step 5: Add falsifiability to H1.**

Append this section to `specs/hypotheses/h1-epigenetic-commitment.md`:

```markdown
## Falsifiability

This hypothesis weakens if longitudinal or stage-ordered data show transcriptional activation consistently preceding
chromatin-opening or PHF19/PRC2 changes. It is also weakened if PHF19 loses prognostic signal after appropriate 1q,
plasma-cell maturity, proliferation, and treatment-context adjustment in independent cohorts.

Decisive negative evidence would be a matched multi-omic progression dataset where MGUS/SMM chromatin state remains
stable until after MM-like transcriptional programs appear, or perturbation data showing that PHF19/PRC2 changes are a
downstream passenger of proliferation rather than a ratcheting mechanism.
```

- [ ] **Step 6: Add falsifiability to H2.**

Append this section to `specs/hypotheses/h2-cytogenetic-distinct-entities.md`:

```markdown
## Falsifiability

This hypothesis weakens if cytogenetic strata do not retain distinct expression-survival architecture after controlling
for cohort, treatment line, plasma-cell composition, purity, and batch effects. It also weakens if stratum-specific
rankings replicate poorly across independent cohorts while unstratified rankings replicate better.

Decisive negative evidence would be a well-powered cohort with reliable cytogenetics showing that gain(1q),
hyperdiploidy, and IGH-translocation strata share the same upstream drivers, effect directions, and mediator structure
once measurement artifacts are removed.
```

- [ ] **Step 7: Add falsifiability to H3.**

Append this section to `specs/hypotheses/h3-mutation-reshaping.md`:

```markdown
## Falsifiability

This hypothesis is already weakened by permutation calibration showing that much mutation-stratified ranking divergence
can be reproduced by random equal-size splits. It should be retired if richer mutation tables and interaction models
again show that mutation-context effects are sparse, unstable, or dominated by sample-size artifacts.

It would be revived only if independent cohorts show reproducible mutation-by-expression survival interactions for
specific driver contexts, with effect sizes large enough to change clinical or mechanistic interpretation beyond the
cytogenetic and epigenetic axes.
```

- [ ] **Step 8: Add falsifiability to H4.**

Append this section to `specs/hypotheses/h4-attractor-convergence.md`:

```markdown
## Falsifiability

This hypothesis weakens if longitudinal, single-cell, or perturbation data show no low-dimensional basin structure and
no convergence toward a recurrent late-disease phenotype after accounting for batch, treatment, and cell-state
composition. It also weakens if inferred transition paths are not more stable than simple linear progression scores.

Decisive negative evidence would be a stage-resolved dataset where patient trajectories remain idiosyncratic, reversible,
and unclustered, with no reproducible terminal attractor signature and no measurable barrier-like effect from PHF19/PRC2,
DNA methylation, chromatin opening, or gain(1q).
```

- [ ] **Step 9: Add falsifiability to H6.**

Append this section to `specs/hypotheses/h6-positive-selection-mm-progression.md`:

```markdown
## Falsifiability

This hypothesis weakens if pre-treatment MGUS/SMM/MM sequencing shows neutral-drift models fitting progression as well
as or better than positive-selection models after correcting for purity, copy number, coverage, and cohort ascertainment.
It also weakens if treatment-exposed relapse samples do not show reproducible genotype- or subclone-specific selection
patterns.

Decisive negative evidence would be longitudinal data showing that apparent dN/dS and clonal-shift signals disappear
under well-calibrated null models, and that maintenance therapy changes overall diversity without predictable
subclone-specific enrichment or depletion.
```

- [ ] **Step 10: Re-run mm30 graph build.**

```bash
cd /home/keith/d/r/mm30
SCIENCE_CONFIG_DIR=/tmp/science-phase2-mm30 uv run science-tool graph build
```

Expected:
- Exit code 0.
- Output includes `Materialized graph at knowledge/graph.trig`.
- Unknown-kind warnings may remain only if they are skips, not fatal errors.

- [ ] **Step 11: Re-run mm30 validation.**

```bash
cd /home/keith/d/r/mm30
bash validate.sh --verbose
```

Expected:
- Exit code 0.
- Warnings may remain for legacy `scripts/`, missing optional sections, or unresolved non-blocking references.
- No `ERROR:` lines remain.

- [ ] **Step 12: Commit mm30 repair.**

```bash
cd /home/keith/d/r/mm30
git add doc/background/papers/Kumar2020BELLINI.md \
  code/README.md \
  models/README.md \
  results/README.md \
  specs/hypotheses/h1-epigenetic-commitment.md \
  specs/hypotheses/h2-cytogenetic-distinct-entities.md \
  specs/hypotheses/h3-mutation-reshaping.md \
  specs/hypotheses/h4-attractor-convergence.md \
  specs/hypotheses/h6-positive-selection-mm-progression.md \
  knowledge/graph.trig
git status --short
git commit -m "fix(graph): restore mm30 graph and validation baseline"
```

`git rm doc/papers/Kumar2020BELLINI.md` in Step 3 stages the duplicate deletion; the `git status --short` check confirms
that deletion is present before commit. `knowledge/graph.trig` is regenerable, but this project currently commits graph
materialization artifacts, so it stays with the source repair it verifies.

---

## Task 3: Bootstrap Minimal Cancer Meta Project

**Files:**
- Create directory: `/mnt/ssd/Dropbox/cancer/meta/`
- Create: `/mnt/ssd/Dropbox/cancer/meta/science.yaml`
- Create: `/mnt/ssd/Dropbox/cancer/meta/knowledge/graph.trig`
- Create: `/mnt/ssd/Dropbox/cancer/meta/README.md`

- [ ] **Step 1: Create the umbrella root.**

```bash
mkdir -p /mnt/ssd/Dropbox/cancer/meta/knowledge
cd /mnt/ssd/Dropbox/cancer/meta
git init
```

- [ ] **Step 2: Write minimal meta `science.yaml`.**

```yaml
name: cancer-meta
id: meta
role: meta
created: "2026-04-30"
last_modified: "2026-04-30"
summary: "Umbrella project for cross-cancer data sources, cancer types, mechanisms, and adjacent conditions."
status: active
profile: research
layout_version: 2
tags:
  - cancer
  - federation
  - meta-analysis
research_question: "What shared and distinct mechanisms organize cancer initiation, progression, treatment response, and pre-cancer states across projects?"
knowledge_profiles:
  local: local
children: []
```

- [ ] **Step 3: Write minimal README.**

```markdown
# Cancer Meta

Umbrella Science project for the cancer federation. This project owns cross-project synthesis and federation metadata;
child projects retain ownership of their claims, data, code, and local graphs.
```

- [ ] **Step 4: Initialize an empty graph.**

```bash
cd /mnt/ssd/Dropbox/cancer/meta
uv run --project /home/keith/d/science/science-tool science-tool graph init
```

Expected:
- `knowledge/graph.trig` exists and parses as TriG.

- [ ] **Step 5: Validate empty meta federation.**

```bash
cd /mnt/ssd/Dropbox/cancer/meta
uv run --project /home/keith/d/science/science-tool science-tool federation validate
uv run --project /home/keith/d/science/science-tool science-tool federation status
```

Expected:
- Validate exits 0 with `ok: federation consistent`.
- Status reports `Children: 0`.

- [ ] **Step 6: Commit meta bootstrap.**

```bash
cd /mnt/ssd/Dropbox/cancer/meta
git add README.md science.yaml knowledge/graph.trig
git commit -m "chore: bootstrap cancer meta project"
```

---

## Task 4: Migrate mm30 To `cancer/cancer-types/multiple-myeloma`

**Files:**
- Move repo: `/mnt/ssd/Dropbox/r/mm30` -> `/mnt/ssd/Dropbox/cancer/cancer-types/multiple-myeloma`
- Modify: `science.yaml`
- Modify: `pyproject.toml`
- Modify path references discovered by the inventory command below
- Modify meta: `/mnt/ssd/Dropbox/cancer/meta/science.yaml`
- Rename Claude memory directory if present
- Create symlink: `/mnt/ssd/Dropbox/r/mm30` -> `/mnt/ssd/Dropbox/cancer/cancer-types/multiple-myeloma`

- [ ] **Step 1: Verify mm30 repair baseline is committed and clean.**

```bash
cd /mnt/ssd/Dropbox/r/mm30
git status --short --branch
SCIENCE_CONFIG_DIR=/tmp/science-phase2-mm30 uv run science-tool graph build
bash validate.sh --verbose
```

Expected:
- Git status is clean.
- Graph build and validation exit 0.

- [ ] **Step 2: Inventory old-path references before the move.**

```bash
cd /mnt/ssd/Dropbox/r/mm30
rg -n "/mnt/ssd/Dropbox/r/mm30|/home/keith/d/r/mm30|~/d/r/mm30|\\.\\./\\.\\./science/science-tool" .
```

Save output into the Phase 2 run log. Every repo-internal hit must be updated after the move.

- [ ] **Step 3: Move the repo.**

```bash
mkdir -p /mnt/ssd/Dropbox/cancer/cancer-types
mv /mnt/ssd/Dropbox/r/mm30 /mnt/ssd/Dropbox/cancer/cancer-types/multiple-myeloma
cd /mnt/ssd/Dropbox/cancer/cancer-types/multiple-myeloma
git status --short --branch
```

Expected:
- Git status remains clean immediately after the physical move.

- [ ] **Step 4: Update mm30 `science.yaml`.**

Set these top-level fields near the identity block, adding them if absent or replacing existing values if present. Do
not leave duplicate `id`, `role`, or `parent` keys.

```yaml
id: multiple-myeloma
role: cancer-type
parent: ~/d/cancer/meta
```

Keep existing `name: mm30` unless the user explicitly wants the display name changed in this phase. Stable federation identity comes from `id`.

- [ ] **Step 5: Update mm30 editable science-tool path.**

In `pyproject.toml`, change:

```toml
science-tool = { path = "../../science/science-tool", editable = true }
```

to:

```toml
science-tool = { path = "../../../science/science-tool", editable = true }
```

Then run:

```bash
uv sync
```

- [ ] **Step 6: Update remaining repo-internal path references.**

Run:

```bash
cd /mnt/ssd/Dropbox/cancer/cancer-types/multiple-myeloma
rg -n "/mnt/ssd/Dropbox/r/mm30|/home/keith/d/r/mm30|~/d/r/mm30|\\.\\./\\.\\./science/science-tool" .
```

For each hit in a repo file, update it to the new physical or tilde path:

```text
/mnt/ssd/Dropbox/cancer/cancer-types/multiple-myeloma
/home/keith/d/cancer/cancer-types/multiple-myeloma
~/d/cancer/cancer-types/multiple-myeloma
../../../science/science-tool
```

Re-run the `rg` command. Expected: no repo-internal hits.

- [ ] **Step 7: Rename mm30 Claude memory directory if present.**

```bash
if [ -d /home/keith/.claude/projects/-mnt-ssd-Dropbox-r-mm30 ]; then
  mv /home/keith/.claude/projects/-mnt-ssd-Dropbox-r-mm30 \
    /home/keith/.claude/projects/-mnt-ssd-Dropbox-cancer-cancer-types-multiple-myeloma
fi
```

- [ ] **Step 8: Register mm30 in meta children.**

Edit `/mnt/ssd/Dropbox/cancer/meta/science.yaml` by replacing the initial `children: []` with:

```yaml
children:
  - id: multiple-myeloma
    path: ~/d/cancer/cancer-types/multiple-myeloma
    role: cancer-type
```

- [ ] **Step 9: Validate mm30 child and meta round-trip.**

```bash
cd /mnt/ssd/Dropbox/cancer/cancer-types/multiple-myeloma
SCIENCE_CONFIG_DIR=/tmp/science-phase2-mm30-moved uv run science-tool graph build
SCIENCE_CONFIG_DIR=/tmp/science-phase2-mm30-moved uv run science-tool sync run
bash validate.sh --verbose

cd /mnt/ssd/Dropbox/cancer/meta
uv run --project /home/keith/d/science/science-tool science-tool federation validate
```

Expected:
- Child graph build exits 0 and auto-registers the parent.
- Child validation exits 0.
- Meta federation validate exits 0.

- [ ] **Step 9a: Record the deferred execution-root consolidation.**

Append to the Phase 2 run log:

```markdown
## Deferred mm30 Execution Root Cleanup

Phase 2 created `code/` as the canonical execution root but left legacy `scripts/` in place because progression-script
work was dirty before migration. After that work is committed, plan a follow-up to consolidate executable code under
`code/` and remove the legacy `scripts/` root from validation warnings.
```

- [ ] **Step 10: Create the time-boxed compatibility symlink.**

```bash
ln -s ../cancer/cancer-types/multiple-myeloma /mnt/ssd/Dropbox/r/mm30
test -L /mnt/ssd/Dropbox/r/mm30
readlink /mnt/ssd/Dropbox/r/mm30
```

Expected:
- `readlink` prints `../cancer/cancer-types/multiple-myeloma`.

- [ ] **Step 11: Commit mm30 move and meta manifest update.**

In the moved mm30 repo:

```bash
cd /mnt/ssd/Dropbox/cancer/cancer-types/multiple-myeloma
git add science.yaml pyproject.toml uv.lock
git add -A
git commit -m "chore: migrate mm30 into cancer federation"
```

In meta:

```bash
cd /mnt/ssd/Dropbox/cancer/meta
git add science.yaml knowledge/graph.trig
git commit -m "chore: register multiple myeloma child project"
```

---

## Task 5: Migrate cbioportal To `cancer/data-sources/cbioportal`

**Files:**
- Move repo: `/mnt/ssd/Dropbox/r/cbioportal` -> `/mnt/ssd/Dropbox/cancer/data-sources/cbioportal`
- Modify: `science.yaml`
- Modify: `pyproject.toml`
- Modify path references discovered by inventory
- Modify meta: `/mnt/ssd/Dropbox/cancer/meta/science.yaml`
- Rename Claude memory directory if present
- Create symlink: `/mnt/ssd/Dropbox/r/cbioportal` -> `/mnt/ssd/Dropbox/cancer/data-sources/cbioportal`

- [ ] **Step 1: Verify cbioportal repair baseline is committed and clean.**

```bash
cd /mnt/ssd/Dropbox/r/cbioportal
git status --short --branch
SCIENCE_CONFIG_DIR=/tmp/science-phase2-cbioportal uv run science-tool graph build
bash validate.sh --verbose
```

Expected:
- Git status is clean.
- Graph build and validation exit 0.

- [ ] **Step 2: Inventory old-path references before the move.**

```bash
cd /mnt/ssd/Dropbox/r/cbioportal
rg -n "/mnt/ssd/Dropbox/r/cbioportal|/home/keith/d/r/cbioportal|~/d/r/cbioportal|\\.\\./\\.\\./science/science-tool" .
```

Save output into the Phase 2 run log. Every repo-internal hit must be updated after the move.

- [ ] **Step 3: Move the repo.**

```bash
mkdir -p /mnt/ssd/Dropbox/cancer/data-sources
mv /mnt/ssd/Dropbox/r/cbioportal /mnt/ssd/Dropbox/cancer/data-sources/cbioportal
cd /mnt/ssd/Dropbox/cancer/data-sources/cbioportal
git status --short --branch
```

Expected:
- Git status remains clean immediately after the physical move.

- [ ] **Step 4: Update cbioportal `science.yaml`.**

Set these top-level fields near the identity block, adding them if absent or replacing existing values if present. Do
not leave duplicate `id`, `role`, or `parent` keys.

```yaml
id: cbioportal
role: data-source
parent: ~/d/cancer/meta
```

Keep existing `name: "cbioportal"`.

- [ ] **Step 5: Update cbioportal editable science-tool path.**

In `pyproject.toml`, change:

```toml
science-tool = { path = "../../science/science-tool", editable = true }
```

to:

```toml
science-tool = { path = "../../../science/science-tool", editable = true }
```

Then run:

```bash
uv sync
```

- [ ] **Step 6: Update remaining repo-internal path references.**

Run:

```bash
cd /mnt/ssd/Dropbox/cancer/data-sources/cbioportal
rg -n "/mnt/ssd/Dropbox/r/cbioportal|/home/keith/d/r/cbioportal|~/d/r/cbioportal|\\.\\./\\.\\./science/science-tool" .
```

For each hit in a repo file, update it to the new physical or tilde path:

```text
/mnt/ssd/Dropbox/cancer/data-sources/cbioportal
/home/keith/d/cancer/data-sources/cbioportal
~/d/cancer/data-sources/cbioportal
../../../science/science-tool
```

Re-run the `rg` command. Expected: no repo-internal hits except the Phase 2 plan and run log documenting the old paths.

- [ ] **Step 7: Rename cbioportal Claude memory directory if present.**

```bash
if [ -d /home/keith/.claude/projects/-mnt-ssd-Dropbox-r-cbioportal ]; then
  mv /home/keith/.claude/projects/-mnt-ssd-Dropbox-r-cbioportal \
    /home/keith/.claude/projects/-mnt-ssd-Dropbox-cancer-data-sources-cbioportal
fi
```

- [ ] **Step 8: Register cbioportal in meta children.**

Edit `/mnt/ssd/Dropbox/cancer/meta/science.yaml` by replacing the one-entry `children:` list from Task 4 with this
two-entry list:

```yaml
children:
  - id: multiple-myeloma
    path: ~/d/cancer/cancer-types/multiple-myeloma
    role: cancer-type
  - id: cbioportal
    path: ~/d/cancer/data-sources/cbioportal
    role: data-source
```

- [ ] **Step 9: Validate cbioportal child and meta round-trip.**

```bash
cd /mnt/ssd/Dropbox/cancer/data-sources/cbioportal
SCIENCE_CONFIG_DIR=/tmp/science-phase2-cbioportal-moved uv run science-tool graph build
SCIENCE_CONFIG_DIR=/tmp/science-phase2-cbioportal-moved uv run science-tool sync run
bash validate.sh --verbose
test -f code/workflows/Snakefile
test -f code/config/config-10k-genes.yml
uv run snakemake -s code/workflows/Snakefile -j1 --configfile code/config/config-10k-genes.yml

cd /mnt/ssd/Dropbox/cancer/meta
uv run --project /home/keith/d/science/science-tool science-tool federation validate
```

Expected:
- Child graph build exits 0 and auto-registers the parent.
- Child validation exits 0.
- The 10k-gene Snakemake smoke exits 0.
- Meta federation validate exits 0.

- [ ] **Step 10: Create the time-boxed compatibility symlink.**

```bash
ln -s ../cancer/data-sources/cbioportal /mnt/ssd/Dropbox/r/cbioportal
test -L /mnt/ssd/Dropbox/r/cbioportal
readlink /mnt/ssd/Dropbox/r/cbioportal
```

Expected:
- `readlink` prints `../cancer/data-sources/cbioportal`.

- [ ] **Step 11: Commit cbioportal move and meta manifest update.**

In the moved cbioportal repo:

```bash
cd /mnt/ssd/Dropbox/cancer/data-sources/cbioportal
git add science.yaml pyproject.toml uv.lock
git add -A
git commit -m "chore: migrate cbioportal into cancer federation"
```

In meta:

```bash
cd /mnt/ssd/Dropbox/cancer/meta
git add science.yaml knowledge/graph.trig
git commit -m "chore: register cbioportal child project"
```

---

## Task 6: Post-Migration Federation Smoke

**Files:**
- Read-only: `/mnt/ssd/Dropbox/cancer/meta/`
- Read-only: migrated child repos
- Modify: Phase 2 run log if used

- [ ] **Step 1: Validate the final meta manifest.**

```bash
cd /mnt/ssd/Dropbox/cancer/meta
uv run --project /home/keith/d/science/science-tool science-tool federation validate
```

Expected:
- Exit code 0.
- Output: `ok: federation consistent`.

- [ ] **Step 2: Build child graphs once in their final locations.**

```bash
cd /mnt/ssd/Dropbox/cancer/cancer-types/multiple-myeloma
SCIENCE_CONFIG_DIR=/tmp/science-phase2-final-mm30 uv run science-tool graph build

cd /mnt/ssd/Dropbox/cancer/data-sources/cbioportal
SCIENCE_CONFIG_DIR=/tmp/science-phase2-final-cbioportal uv run science-tool graph build
```

Expected:
- Both exit 0.
- Neither writes outside its own project.

- [ ] **Step 3: Build the meta federated graph.**

```bash
cd /mnt/ssd/Dropbox/cancer/meta
uv run --project /home/keith/d/science/science-tool science-tool graph build
```

Expected:
- Phase 1 wired `science-tool graph build` so `role: meta` runs local materialization and then federation assembly.
- Output includes `Materialized meta local graph` and `Materialized federated graph`. If this is not true, stop and
  inspect `/home/keith/d/science/science-tool/src/science_tool/cli.py::graph_build`; do not treat a local-only meta
  graph as a successful federation build.
- `knowledge/graph.trig` contains named graphs `cancer://multiple-myeloma`, `cancer://cbioportal`, and `cancer://meta`.

- [ ] **Step 4: Verify named graph shape.**

```bash
cd /mnt/ssd/Dropbox/cancer/meta
uv run --project /home/keith/d/science/science-tool python - <<'PY'
from pathlib import Path
from rdflib import Dataset, URIRef

ds = Dataset()
ds.parse(Path("knowledge/graph.trig"), format="trig")
names = {str(g.identifier) for g in ds.graphs() if g.identifier != URIRef("urn:x-rdflib:default")}
required = {"cancer://meta", "cancer://multiple-myeloma", "cancer://cbioportal"}
missing = required - names
if missing:
    raise SystemExit(f"missing graphs: {sorted(missing)}")
print("ok:", ", ".join(sorted(required)))
PY
```

Expected:
- `ok: cancer://cbioportal, cancer://meta, cancer://multiple-myeloma`

- [ ] **Step 5: Run federated status.**

```bash
cd /mnt/ssd/Dropbox/cancer/meta
uv run --project /home/keith/d/science/science-tool science-tool federation status
```

Expected:
- Output includes both child IDs and roles:
  - `multiple-myeloma (cancer-type)`
  - `cbioportal (data-source)`

- [ ] **Step 6: Verify compatibility symlinks.**

```bash
test -L /mnt/ssd/Dropbox/r/mm30
test -L /mnt/ssd/Dropbox/r/cbioportal
test "$(readlink /mnt/ssd/Dropbox/r/mm30)" = "../cancer/cancer-types/multiple-myeloma"
test "$(readlink /mnt/ssd/Dropbox/r/cbioportal)" = "../cancer/data-sources/cbioportal"
```

- [ ] **Step 7: Record completion.**

Append to the Phase 2 run log:

```markdown
## Completion

- mm30 migrated to `/mnt/ssd/Dropbox/cancer/cancer-types/multiple-myeloma`
- cbioportal migrated to `/mnt/ssd/Dropbox/cancer/data-sources/cbioportal`
- compatibility symlinks created under `/mnt/ssd/Dropbox/r/`
- symlink expiry date: 2026-06-30
- final federation validate: passed
- final federated graph build: passed
- final meta graph commit: completed or clean
```

Commit the run log in whichever repo owns it at that point.

- [ ] **Step 8: Commit the final meta federated graph.**

```bash
cd /mnt/ssd/Dropbox/cancer/meta
git add knowledge/graph.trig science.yaml README.md
git commit -m "chore: materialize phase 2 federated graph"
```

Expected:
- Commit succeeds if `knowledge/graph.trig` changed during the final meta build.
- If Git reports nothing to commit, record that in the run log and leave the meta repo clean.

- [ ] **Step 9: Schedule symlink-expiry cleanup.**

Offer the user a follow-up reminder/agent run for **2026-06-15**:

```text
Scan `/mnt/ssd/Dropbox/r/mm30` and `/mnt/ssd/Dropbox/r/cbioportal` compatibility symlink usage, update any remaining
external references, then remove the symlinks on or after 2026-06-30.
```

If a scheduler is available in the environment, create the reminder only after user approval. Otherwise, add a dated task
to the active task list of the meta project.

---

## Rollback Notes

Rollback is only for a failed move before commits are pushed or external users depend on the new paths.

For mm30 before committing the move:

```bash
rm /mnt/ssd/Dropbox/r/mm30
mv /mnt/ssd/Dropbox/cancer/cancer-types/multiple-myeloma /mnt/ssd/Dropbox/r/mm30
```

For cbioportal before committing the move:

```bash
rm /mnt/ssd/Dropbox/r/cbioportal
mv /mnt/ssd/Dropbox/cancer/data-sources/cbioportal /mnt/ssd/Dropbox/r/cbioportal
```

If meta was already updated, remove the corresponding child entry from `/mnt/ssd/Dropbox/cancer/meta/science.yaml` and recommit the corrected manifest.

If a child move commit succeeds but the matching meta manifest commit has not happened yet, do not move the child back
automatically. Either complete the meta registration commit, or create a follow-up meta commit explicitly documenting
that the child is temporarily moved but not yet federated. Run `science-tool federation validate` from meta only after
the manifest reflects the intended state.

---

## Self-Review Notes

- Spec coverage: This plan implements Phase 2 from the cancer meta design: repair blockers, bootstrap minimal meta, migrate mm30 first, migrate cbioportal second, update child `science.yaml`, update meta `children:`, rename Claude memory directories, create time-boxed symlinks, and validate federation.
- Existing blocker coverage: cbioportal unresolved interpretation graph references and missing `models/` are addressed before moving; mm30 duplicate BELLINI paper, missing canonical roots, and missing falsifiability sections are addressed before moving.
- Scope boundary: Phase 3 content scaffolding and first useful federated status synthesis remain outside this plan. Phase 2 only proves the federation and moved paths are structurally sound.
- Dirty work boundary: The plan stops before modifying user-owned dirty files. It does not hide existing dirty work with stash/reset.
