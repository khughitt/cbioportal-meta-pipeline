# cBioPortal Meta-analysis Research Plan

This project asks what structure recurs in somatic mutation data across public cBioPortal
studies and AACR GENIE, with emphasis on gene-cancer associations that persist across
independent cohorts.

## Current Scope

- Aggregate study-level somatic mutation calls into cross-study gene, cancer, and
  gene-cancer frequency tables.
- Annotate pooled mutation rates with panel callability, matched-normal status, CH-priority
  genes, hypermutator state, and driver-gene overlays.
- Compare raw recurrence, length-aware normalization, and selection-aware driver signals.
- Maintain science-facing documentation in `doc/`, task state in `tasks/`, and graph state in
  `knowledge/`.

## Active Planning Surface

Detailed implementation plans live in `doc/plans/`; active and proposed work is tracked in
`tasks/active.md`. Consumer-facing output conventions are summarized in
`doc/guides/canonical-outputs.md`.

## Out of Scope

- Non-mutation modalities are not part of the current pipeline phase.
- AACR GENIE access-controlled inputs are never committed.
- Population-representativeness and outcome/survival modeling are deferred research axes.
