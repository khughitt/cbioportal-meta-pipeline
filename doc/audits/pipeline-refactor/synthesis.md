# Pipeline audit synthesis - cbioportal

Audit date: 2026-05-31.
Method: `~/d/science/docs/process/pipeline-audit-and-refactor.md`.

## Summary

The dominant weakness is not lack of script-level validation.
Many scripts fail early and have focused tests.
The weakness is that QA is not yet a first-class workflow substrate: most clean-base and final analysis outputs are not followed by declared QA rules, and there is no default QA target that validates the artifacts actually produced by Snakemake.

The strongest local pattern is `export_study_expression.py`, which emits a declared `qa_report.md` and `datapackage.json` beside the clean substrate.
The mutation pipeline should reuse that pattern for per-study ingest, `samples_annotated`, pooled meta-analysis inputs/outputs, and the canonical annotated gene-cancer tables.

## Prioritized refactor backlog

| Rank | Axis | Item | Chains affected | Effort | Task |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | Add wired structural QA rules and a root-runnable QA target for per-study clean-base feathers, `samples_annotated`, pooled meta-analysis substrates, and canonical annotated outputs. | cBioPortal ingest, MC3, hypermutator, per-study tables, cross-study aggregation, signatures, dNdScv | L | task:t191 |
| 2 | 1 | Add Snakemake DAG-validation guard for single-writer output ownership, declared-input completeness, orphan inputs, and shipped-config dry-runs. | all workflow chains | M | task:t192 |
| 3 | 3 | Add datapackages and dataset entities for reusable clean-base substrates and the canonical annotated product. | cBioPortal ingest, MC3, overlays, GENIE panel coverage, normal tissue, replication timing, expression | L | task:t193 |
| 4 | 2 | Normalize workflow logs and execution environments so `snakemake --lint` is actionable. | all active Snakemake rules | M | task:t194 |
| 5 | 1 | Promote pooled meta-analysis diagnostics into wired result-QA. | cross-study aggregation | M | task:t191 |
| 6 | 2 | Close already-known production blockers in SELECT and clustering. | SELECT, clustering | M | task:t137; task:t107 |
| 7 | 2 | Close known operational/runtime debt in dNdScv and correlation matrices. | dNdScv, per-study matrices | M | task:t143; task:t104 |
| 8 | 3 | Repair pre-existing dataset-promotion validation failures before attempting commons promotion. | all commons candidates | M | task:t185 |

## Recurring anti-patterns

- Script-level checks without artifact-level QA rules - common across per-study ingest, TMB, per-study tables, cross-study aggregation, dNdScv, signatures, and reference-processing chains.
- Clean-base substrates without datapackages - common across mutation ingest, MC3, overlays, GENIE panel coverage, normal-tissue spectra, and replication-timing annotations.
- Consumer contracts embedded in scripts/tests rather than declared as workflow outputs - visible in `create_freq_tables.py`, `join_gene_cancer_meta.py`, dNdScv joins, and SELECT input generation.
- Workflow execution metadata is under-specified - `snakemake --lint` reports missing `log:` directives broadly and missing per-rule env/container declarations for most Python rules.
- Opt-in analysis branches have good scientific plans but uneven workflow hardening - dNdScv, signatures, replication timing, and SELECT should be promoted through the same QA+manifest pattern before becoming default interpretation substrates.

## Convention nominations (upstream candidates)

| Candidate check | Kind (data-QA / analysis-result-QA / workflow-DAG) | Evidence (chains / bugs caught) | Proposed home |
| --- | --- | --- | --- |
| Snakemake single-writer / declared-input / orphan-input audit for Science projects | workflow-DAG | Needed across this Snakefile; matches the pipeline audit playbook's companion DAG-validation requirement | `~/d/science/docs/conventions/` as a workflow-DAG checkpoint convention |
| Paired inclusive/exclusive mutation-frequency table QA | data-QA | `create_freq_tables.py`, `create_combined_gene_cancer_freq_table.py`, hypermutator-aware denominators | Cross-study aggregation modality guide |
| Pooled meta-analysis result-bundle QA | analysis-result-QA | `gene_cancer_pooled.feather` plus diagnostics, leave-one-out, panel-sensitivity, and placebo sidecars | Computational-analysis conventions or cross-study aggregation modality guide |
| Dataset package pattern using declared `qa_report.md` plus `datapackage.json` | data-QA / portability | `export_study_expression.py` already implements the pattern cleanly | Pipeline QA checkpoint examples |

## Commons promotion candidates

| Dataset | Entity exists? | Promoted? | Blocking prerequisites |
| --- | --- | --- | --- |
| cBioPortal generated per-study mutation+clinical clean feathers | `doc/datasets/cbioportal.md` exists | no | Per-run datapackage, access/license notes, structural QA, dataset entity cleanup |
| TCGA MC3 pseudo-study | `doc/datasets/tcga-mc3.md` exists | no | Generated datapackage with source hashes, schema-equivalence QA |
| Canonical `gene_cancer_study_ratio_annotated.feather` product | `doc/datasets/gene-cancer-study-ratio-annotated-product.md` exists | no | Canonical-output QA, manifest hashes, resolve dataset-promotion validation failures |
| GENIE panel coverage / callable-size registry | GENIE dataset notes exist | no | Separate clean-base datapackage, access restrictions, registry QA |
| Bailey / CGC / Sanchez-Vega processed overlays | partial dataset notes for source families | no | Processed-overlay datapackage and source/version metadata |
| Normal-tissue spectra / burden | `doc/datasets/normal-tissue-spectra.md` exists | no | QA sidecar, datapackage, source-yield accounting |
| Replication-timing annotations | `doc/datasets/replication-timing-constitutive-regions.md` exists | no | Datapackage, coordinate-range QA, source hash |
| Expression export packages | per-study entities exist for some studies | no | Verify per-study dataset entities and dry-run `science commons promote dataset` |

## Validation notes

- `uv run snakemake -s code/workflows/Snakefile --configfile code/config/config-10k-genes.yml -n --quiet` completed successfully.
- `uv run snakemake --lint -s code/workflows/Snakefile --configfile code/config/config-10k-genes.yml` exited nonzero with workflow-quality findings: broad missing `log:` directives and missing conda/container declarations for most Python rules.
- `uv run --frozen science validate --verbose` exited nonzero with pre-existing project validation blockers: duplicate `paper:Degasperi2022` identity across `doc/papers/Degasperi2022.md` and `knowledge/sources/local/entities.yaml`, unresolved dataset-promotion datapackages for `doc/datasets/hartwig-hmf.md` and `doc/datasets/kucab2019-mutagen-compendium.md`, and existing warning classes.
- Existing task `task:t185` records dataset-promotion cleanup work, so this audit did not attempt commons promotion.

## Execution order

Start with `task:t191` on the already-explicit substrates: `samples_annotated`, `gene_cancer_pooled_input`, `gene_cancer_pooled*`, and the two canonical annotated gene-cancer outputs.
Those have clear downstream consumers, rich tests, and small enough schema contracts to make a structural QA pattern concrete.

Next, implement `task:t192` so the workflow itself can guard against output ownership and missing dependency regressions.
Then apply the same QA+datapackage pattern backward to the clean-base ingest substrates and forward to opt-in branches as they become default analysis surfaces.
