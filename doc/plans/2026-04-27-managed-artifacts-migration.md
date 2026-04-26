# Managed-artifacts migration: cbioportal

**Status:** Draft (ready for execution)
**Target version:** validate.sh @ 2026.04.26.2
**Migration path:** Path 1 (effectively pure-lag — only customization is in `drop` bucket)
**Final placement:** `~/d/r/cbioportal/doc/plans/2026-04-27-managed-artifacts-migration.md`

---

## Current state

- **`validate.sh` SHA-256:** `0a9878c8dd81acc9703dbd58e8ec236254eee8c5c000f341caff26f5a37a3c44`
- **Line count:** 867 lines (32,722 bytes)
- **File last touched:** commit `d6635b0` ("/science:import-project") on 2026-04-12. Imported as part of the project's onboarding to the Science framework.
- **`science-tool project artifacts check` output:** `untracked` — no managed header.

## Drift summary

- **6 lines unique to cbioportal's `validate.sh`.** All are pre-Plan-#7 logic OR a pre-Plan-#7 implementation of something the canonical now does:
  - `.env` sourcing block (cbioportal-added at import time as a workaround). Canonical now does this in Plan #7 Fix 2 with an additional opt-out (`SCIENCE_VALIDATE_SKIP_DOTENV`).
  - Old `ontologies is not None and not isinstance(ontologies, list)` shape check (Plan #7 Fix 3 changed to `curated` shape).
  - Unconditional `Duplicate document roots detected` warn (Plan #7 Fix 5 made it conditional behind a `find -path 'docs/superpowers/*'` probe).
  - Old pre-registration loop spelling.
  - `graph audit produced unparseable output (expected...)` warn (Plan #7 Fix 4 changed to error and dropped the misleading "expected for fresh projects" tail).
- **235 lines unique to canonical.** All Plan #7 fixes, hook dispatch points, section 17 id-prefix, the 4-line managed header.

## Customization analysis

| Diff hunk | Bucket | Action |
|---|---|---|
| `.env` sourcing block | drop | Canonical now does this with opt-out support (Plan #7 Fix 2). Strict superset of cbioportal's version. |
| Old ontology-shape check | drop | Canonical's `curated`-shape check supersedes (Plan #7 Fix 3). |
| Unconditional duplicate-doc-roots warn | drop | Canonical's conditional probe supersedes (Plan #7 Fix 5). |
| Pre-Plan-#7 pre-registration loop | drop | Canonical's logic supersedes. |
| Pre-Plan-#7 graph-audit warn | drop | Canonical now errors (Plan #7 Fix 4). |

**Net: zero customizations to preserve.** cbioportal is functionally pure-lag with one workaround (`.env` block) that the canonical now does properly. Use Path 1.

## In-progress work to keep separate

cbioportal currently has uncommitted modifications to:
- `doc/questions/q011-gene-length-as-literature-attention-confounder.md`
- `tasks/active.md`
- (untracked) `doc/interpretations/2026-04-26-t131-full-pan-cancer-dndscv-run.md`

These are unrelated to this migration and MUST NOT be entangled with the migration commit. Use selective `git add` (only `validate.sh` + the spec doc).

## Migration plan (Path 1)

```bash
cd ~/d/r/cbioportal

# 0. Verify the in-progress work I won't touch.
git status --short
# expected:  M doc/questions/...  M tasks/active.md  ?? doc/interpretations/...

# 1. Verify framework version.
uv run --project ~/d/science/science-tool \
    science-tool project artifacts check validate.sh --project-root . --json
# expected: {"version": "2026.04.26.2", "status": "untracked"}

# 2. Remove the standalone validate.sh.
git rm validate.sh

# 3. Install the canonical.
uv run --project ~/d/science/science-tool \
    science-tool project artifacts install validate.sh --project-root .
# expected output: "validate.sh: install (install_target missing; install canonical)"

# 4. Verify.
uv run --project ~/d/science/science-tool \
    science-tool project artifacts check validate.sh --project-root .
# expected: validate.sh: current

# 5. Smoke-run.
bash validate.sh
echo "exit: $?"
# Expect new findings (canonical does more checks than the pre-Plan-#7 version
# cbioportal was running — particularly section 17 id-prefix and the
# stricter graph-audit error). Capture as follow-up; not part of migration.

# 6. Selective stage (exclude unrelated in-progress work).
git add validate.sh doc/plans/2026-04-27-managed-artifacts-migration.md

git status --short
# expected:
#   M validate.sh
#   A doc/plans/2026-04-27-managed-artifacts-migration.md
# Plus the unrelated in-progress files still as M/?? — that's correct.

# 7. Commit.
git commit -m "chore(framework): migrate validate.sh to managed artifact v2026.04.26.2

Replaces standalone validate.sh body (sha256 0a9878c8...) with the
canonical from the science-tool managed-artifact registry.
Functionally pure-lag: cbioportal's only project-specific addition
was a .env sourcing block, which the canonical now does properly
(Plan #7 Fix 2 — adds opt-out via SCIENCE_VALIDATE_SKIP_DOTENV).

Drops 6 lines of pre-Plan-#7 logic that has since been refactored
upstream:
  - .env sourcing block (Plan #7 Fix 2 supersedes with opt-out)
  - ontology-shape check (Plan #7 Fix 3)
  - duplicate-doc-roots conditional probe (Plan #7 Fix 5)
  - pre-registration loop spelling
  - graph-audit warn -> error (Plan #7 Fix 4)

The canonical surfaces new findings on first post-migration run;
those are real lint debt the old validator did not check. Addressing
them is follow-up work, not part of this migration.

Per docs/migration/managed-artifacts-template.md (Path 1) and
doc/plans/2026-04-27-managed-artifacts-migration.md."
```

## Verification

- [ ] `science-tool project artifacts check validate.sh --project-root .` → `current`
- [ ] `--json` form returns `"version": "2026.04.26.2"`, `"status": "current"`
- [ ] `bash validate.sh` runs to completion (FAILED with N errors / M warnings is acceptable; bash syntax error is a defect)
- [ ] Shim parity: `diff <(bash validate.sh 2>&1 | head -3) <(bash ~/d/science/science-tool/src/science_tool/project_artifacts/data/validate.sh 2>&1 | head -3)` empty
- [ ] `git log -1` shows the migration commit; `git status --short` still shows ONLY the unrelated in-progress files (no leakage)

## Expected new findings (informational)

Once the canonical runs, expect surfaces cbioportal's old `validate.sh` did not check:

- **Section 17 — per-type id-prefix** may flag any task/question/spec files whose IDs don't match the canonical's `PREFIX_RULES` table.
- **graph-audit unparseable** is now an `error` (was `warn`) — if cbioportal's graph audit ever produces unparseable output, this will fail validation. Triage: usually means the project hasn't built its `knowledge/graph.trig` or science-tool path is mis-set.
- **`.env` opt-out** — if anything in cbioportal's tooling depends on `.env` NOT being sourced, set `SCIENCE_VALIDATE_SKIP_DOTENV=1` in the invoking environment.

## Rollback procedure

```bash
cd ~/d/r/cbioportal

# Revert the migration commit (does not touch unrelated in-progress files).
git revert HEAD

# Verify.
uv run --project ~/d/science/science-tool \
    science-tool project artifacts check validate.sh --project-root .
# expected: untracked
sha256sum validate.sh
# expected: 0a9878c8dd81acc9703dbd58e8ec236254eee8c5c000f341caff26f5a37a3c44
```

## Decision log

- **2026-04-27**: drafted from `docs/migration/managed-artifacts-template.md`. cbioportal picked as the second pilot (after mm30) because it's a near-replica of the pure-lag case but exercises the "drop bucket includes a project workaround that's now in canonical" pattern — useful proof point that the migration system handles partial-pre-fix workarounds cleanly.
- mm30 migration (commit `f1615dc`) ran cleanly with no template changes needed; cbioportal expected to follow identical mechanical flow.
