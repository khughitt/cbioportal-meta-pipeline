---
id: t137
project: ''
title: t078 SELECT pipeline integration wiring (production prerequisites)
type: ''
aspects:
- software-development
priority: P2
status: proposed
blocked_by:
- task:t081
related:
- task:t078
- task:t081
parent: ''
group: pipeline
artifacts: []
findings: []
created: '2026-04-25'
completed: null
---

t078 implementation landed unit-tested + DAG-dry-run-validated, but the
plan referenced upstream artefacts that the existing pipeline does not
currently produce. Discovered when attempting an end-to-end smoke run.
Wiring the gaps closed will let the SELECT rules run on real data:

1. **`gene_sample_long.feather`** — t078 rules read
   `summary/mut/table/gene_sample_long.feather` (per-sample × gene long
   table). No current rule produces it. Needs a new
   `build_gene_sample_long` rule that derives per-(composite_sample_id,
   symbol) rows from the per-study `studies/{id}/mut/table/mut.feather`
   files (concat + project + dedupe).

2. **`samples_annotated.feather`** — t078 expects the
   `metadata/samples_annotated.feather` written by the t081
   hypermutator pipeline. The 10k dataset does not currently have this
   file produced; running the hypermutator pipeline against the 10k
   config would land it. Blocked by t081 readiness for this dataset.

3. **`bailey_alteration_class.feather` schema mismatch** — t078 references
   `metadata/bailey_alteration_class.feather` with cols (symbol,
   alteration_class). The existing `process_bailey2018_drivers` rule
   writes `metadata/bailey2018_drivers.feather` with a different schema.
   Either (i) switch t078 to read the existing feather and adapt its
   loader to the actual schema, or (ii) add a small adapter rule that
   projects the bailey drivers feather to the expected
   (symbol, alteration_class) shape.

4. **`sanchez_vega_pathways.tsv` vs `.feather`** — t078 reads the TSV;
   the existing `process_sanchez_vega_pathways` rule writes a feather.
   Either (i) switch t078 to read the feather, or (ii) add a TSV export
   to the existing rule. Recommend (i) — feather is canonical.

5. **`sample_panel_map.feather`** — producible by the rule t078 added
   (Task 7 of the implementation plan); requires
   `samples_annotated.feather` to exist first (depends on item 2).

After wiring: smoke-run with `n_permut=50` and 1-2 cancer types to
verify production data flows end-to-end, then bump to full
`n_permut=1000` for the headline run.
