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
- `bash validate.sh --verbose`: passed with one existing `[UNVERIFIED]` warning in `doc/papers/Schill2024.md`

## Move Notes

This run log is still at `/home/keith/d/r/cbioportal/doc/plans/2026-04-30-phase-2-run-log.md`. During the cbioportal
move it should travel with the repository to
`/mnt/ssd/Dropbox/cancer/data-sources/cbioportal/doc/plans/2026-04-30-phase-2-run-log.md`.
