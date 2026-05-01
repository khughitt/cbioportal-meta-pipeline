# Phase 2 Run Log

## Preflight

- science commit: `c29049f`
- cbioportal status before repair: dirty plan docs were committed in `41d32f2`
- mm30 status at cbioportal repair time: clean `main`
- known blocker policy: repair graph/validation blockers before project moves

## cbioportal Preparation

- plan preparation commit: `41d32f2 docs: prepare cancer phase 2 migration plan`
- graph/validation repair commit: `91d63bb fix(graph): restore cbioportal interpretation references`
- repair summary:
  - added canonical interpretation frontmatter to `doc/interpretations/2026-04-27-t145-mean-inclusive-inflation-diagnostic.md`
  - added missing `type`, `status`, and `source_refs` fields to the t146 and t149 interpretation docs
  - added tracked `models/README.md`
  - refreshed `knowledge/graph.trig`
  - updated `uv.lock` to the local `science-tool` 0.2.0 editable version

## cbioportal Verification

- `uv sync`: passed; updated local editable `science-tool` from 0.1.0 to 0.2.0
- `uv run science-tool graph audit --format json > /tmp/cbioportal-graph-audit.json`: passed
- `rg '"status": "fail"' /tmp/cbioportal-graph-audit.json`: no matches
- `SCIENCE_CONFIG_DIR=/tmp/science-phase2-cbioportal uv run science-tool graph build`: passed and materialized `knowledge/graph.trig`
- `SCIENCE_CONFIG_DIR=/tmp/science-phase2-cbioportal-verify uv run --frozen science-tool graph build`: passed and materialized `knowledge/graph.trig`
- `bash validate.sh --verbose`: passed with one existing unverified-source warning in `doc/papers/Schill2024.md`

## mm30 Preparation

- graph/validation repair commit: `cc76a94 fix(graph): restore mm30 validation baseline`
- repair summary:
  - consolidated duplicate BELLINI paper metadata into `doc/background/papers/Kumar2020BELLINI.md`
  - removed duplicate `doc/papers/Kumar2020BELLINI.md`
  - added canonical `code/`, `models/`, and `results/` roots with README markers
  - added falsifiability sections to the active hypothesis specs blocking validation
  - extended the local knowledge profile and mappings for project-local entity kinds and legacy aliases
  - refreshed `knowledge/graph.trig` and graph migration audit artifacts
  - updated `validate.sh` so it resolves the sibling `science/science-tool` checkout from the current layout

## mm30 Verification

- `uv sync`: passed with no dependency changes
- `uv run science-tool graph audit --format json > /tmp/mm30-graph-audit-after3.json`: passed
- `rg '"status": "fail"' /tmp/mm30-graph-audit-after3.json`: no matches
- `SCIENCE_CONFIG_DIR=/tmp/science-phase2-mm30 uv run science-tool graph build`: passed and materialized `knowledge/graph.trig`
- `bash validate.sh --verbose`: passed with existing non-blocking warnings

## mm30 Migration

- pre-move status: clean `main`
- old-path inventory command:
  `rg -n "/mnt/ssd/Dropbox/r/mm30|/home/keith/d/r/mm30|~/d/r/mm30|\\.\\./\\.\\./science/science-tool" .`
- old-path inventory result: 327 matches before the move, mostly historical plans, handoffs, generated evidence fragments,
  and the editable `science-tool` path
- moved from `/mnt/ssd/Dropbox/r/mm30` to `/mnt/ssd/Dropbox/cancer/cancer-types/multiple-myeloma`
- set child identity fields: `id: multiple-myeloma`, `role: cancer-type`, `parent: ~/d/cancer/meta`
- updated editable `science-tool` path to `../../../science/science-tool`
- path rewrite note: actual old mm30 repo-root references were rewritten to the new cancer path. Two historical external
  worktree references, `/mnt/ssd/Dropbox/r/mm30-t277` and `/mnt/ssd/Dropbox/r/mm30-t278`, were not rewritten because
  they do not refer to the moved repository root.
- plan edge-case note: the original post-rewrite `rg` pattern for `../../science/science-tool` also matches inside the
  correct new `../../../science/science-tool` path, so verification used a boundary-aware old-root check plus explicit
  `pyproject.toml`, `uv.lock`, and `validate.sh` path inspection.
- renamed Claude memory directory from `-mnt-ssd-Dropbox-r-mm30` to
  `-mnt-ssd-Dropbox-cancer-cancer-types-multiple-myeloma`
- registered `multiple-myeloma` as the first meta child

## mm30 Moved Verification

- `uv sync`: passed
- `uv sync --reinstall-package science-tool`: regenerated a stale console-script shebang that still pointed at the old
  `.venv` location after the physical move
- `SCIENCE_CONFIG_DIR=/tmp/science-phase2-mm30-moved uv run science-tool graph build`: passed and materialized
  `knowledge/graph.trig`
- `SCIENCE_CONFIG_DIR=/tmp/science-phase2-mm30-moved uv run science-tool sync run`: passed with `Entities: 1316`
- `bash validate.sh --verbose`: passed with existing non-blocking warnings
- `uv run --project /home/keith/d/science/science-tool science-tool federation validate` from meta: passed with
  `ok: federation consistent`

## Deferred mm30 Execution Root Cleanup

Phase 2 created `code/` as the canonical execution root but left legacy `scripts/` in place because progression-script
work was dirty before migration. After that work is committed, plan a follow-up to consolidate executable code under
`code/` and remove the legacy `scripts/` root from validation warnings.

## cbioportal Migration

- pre-move status: clean `main`, ahead of `origin/main`
- old-path inventory command:
  `rg -n "/mnt/ssd/Dropbox/r/cbioportal|/home/keith/d/r/cbioportal|~/d/r/cbioportal|\\.\\./\\.\\./science/science-tool" .`
- old-path inventory result: 58 matches before the move, mostly Phase 2/federation plan documentation plus the editable
  `science-tool` path and a few older plan/data references
- moved from `/mnt/ssd/Dropbox/r/cbioportal` to `/mnt/ssd/Dropbox/cancer/data-sources/cbioportal`
- set child identity fields: `id: cbioportal`, `role: data-source`, `parent: ~/d/cancer/meta`
- updated editable `science-tool` path to `../../../science/science-tool`
- updated `validate.sh` so it resolves `../../../science/science-tool` from the moved layout
- non-Phase-2 old cbioportal root references were rewritten to the new cancer path
- renamed Claude memory directory from `-mnt-ssd-Dropbox-r-cbioportal` to
  `-mnt-ssd-Dropbox-cancer-data-sources-cbioportal`
- registered `cbioportal` as the second meta child

## cbioportal Moved Verification

- `uv sync`: passed
- `uv sync --reinstall-package science-tool`: regenerated a stale console-script shebang that still pointed at the old
  `.venv` location after the physical move
- `SCIENCE_CONFIG_DIR=/tmp/science-phase2-cbioportal-moved uv run science-tool graph build`: passed and materialized
  `knowledge/graph.trig`
- `SCIENCE_CONFIG_DIR=/tmp/science-phase2-cbioportal-moved uv run science-tool sync run`: passed with `Entities: 341`
- `bash validate.sh --verbose`: passed with the existing single unverified-source warning
- `test -f code/workflows/Snakefile` and `test -f code/config/config-10k-genes.yml`: passed
- `uv sync --reinstall-package snakemake`: regenerated a stale Snakemake console-script shebang that still pointed at
  the old `.venv` location after the physical move
- `uv run snakemake -s code/workflows/Snakefile -j1 --configfile code/config/config-10k-genes.yml`: attempted. The
  first run exposed a pre-existing 10k fixture gap: `data/study_panels.tsv` lacked the seven studies in
  `code/config/config-10k-genes.yml`. Added those seven studies as `wes` entries. The resumed run then progressed into
  `create_correlation_matrices`, but that job ran for more than 30 minutes at full CPU, showing that this command is a
  heavy 10k build rather than a short migration smoke. It was intentionally terminated and recorded as a follow-up
  build gate.
- `uv run snakemake -n -s code/workflows/Snakefile -j1 --configfile code/config/config-10k-genes.yml`: passed. The DAG
  resolves under the moved path, with 38 jobs remaining after the interrupted real build.
- `uv run --project /home/keith/d/science/science-tool science-tool federation validate` from meta: passed with
  `ok: federation consistent`

## Move Notes

This run log moved with cbioportal and now lives at
`/mnt/ssd/Dropbox/cancer/data-sources/cbioportal/doc/plans/2026-04-30-phase-2-run-log.md`.
