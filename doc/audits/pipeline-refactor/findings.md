# Pipeline audit findings - cbioportal

Audit date: 2026-05-31.
Method: `~/d/science/docs/process/pipeline-audit-and-refactor.md`.
Evidence sources: `code/workflows/Snakefile`, `code/scripts/`, `tasks/active.md`, `doc/guides/canonical-outputs.md`, `doc/datasets/`, and validation commands recorded in `synthesis.md`.

## Chain: cBioPortal study mutation+clinical ingest

- **Axis 1 - Data QA:** FAIL - `convert_to_feather` performs several fail-fast checks, including NCBI build validation, MSI normalization, and panel-id resolution, but no declared QA rule validates the clean per-study feathers as built artifacts.
  - substrates with a wired-in QA step: clean base no; downstream per-study substrates no
  - consumer-contract QA: WARN - downstream consumers assume `sample_id`, cancer labels, panel columns, and build metadata are present.
  - companion DAG-validation (output-ownership): WARN - the shipped dry-run resolves, but there is no guard checking declared-input completeness or registered external inputs.
- **Axis 2 - Consistency/quality:** WARN - study-specific cleanup is explicit, but config and schema contracts are scattered across scripts.
- **Axis 3 - Portability/commons:** FAIL - this is the main reusable base substrate, but there is no per-study datapackage or dataset entity for the generated feather package.

### Findings
| # | Axis | Finding | Severity | Disposition | Task |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | Per-study mutation, sample, patient, study, and build outputs lack a wired structural QA rule that checks required columns, key uniqueness, label null policy, build enum, and panel-id validity. | structural | fix-now | task:t191 |
| 2 | 3 | Generated per-study clean-base feathers are reusable outside this project but lack datapackages and dataset entities. | portability | backlog | task:t193 |
| 3 | 2 | Study-specific ingestion exceptions are embedded in `convert_to_feather.py`; they are explicit and fail-fast, but need a schema audit trail so future exceptions remain visible. | quality | backlog | task:t191 |

## Chain: TCGA MC3 pseudo-study ingest

- **Axis 1 - Data QA:** FAIL - `process_mc3` mirrors the per-study schema, but the schema equivalence is not enforced by a wired QA rule.
  - substrates with a wired-in QA step: clean base no; downstream same as cBioPortal no
  - consumer-contract QA: WARN - ruleorder routes `tcga_mc3` away from `convert_to_feather`, so contract drift can occur unless checked explicitly.
  - companion DAG-validation (output-ownership): WARN
- **Axis 2 - Consistency/quality:** PASS - `process_mc3` is intentionally shaped to match the cBioPortal schema.
- **Axis 3 - Portability/commons:** WARN - `doc/datasets/tcga-mc3.md` exists, but generated runtime datapackage/readiness is not complete.

### Findings
| # | Axis | Finding | Severity | Disposition | Task |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | MC3 output should pass the same per-study clean-base QA contract as ordinary cBioPortal studies. | structural | fix-now | task:t191 |
| 2 | 3 | MC3 pseudo-study needs a generated datapackage that records source MAF, case map, hashes, and matched-normal semantics. | portability | backlog | task:t193 |

## Chain: Driver and pathway overlays

- **Axis 1 - Data QA:** WARN - processors validate basic source schemas and deduplicate keys, but no downstream QA verifies the overlay output keys and version fields before annotation.
  - substrates with a wired-in QA step: clean base no; downstream canonical output no
  - consumer-contract QA: WARN - `join_gene_cancer_meta.py` validates the pooled join, but overlay-specific consumer contracts are mostly in tests/docs.
  - companion DAG-validation (output-ownership): WARN
- **Axis 2 - Consistency/quality:** WARN - unified `annotate.py` is a good consolidation, but version provenance is still tracked as an open task.
- **Axis 3 - Portability/commons:** WARN - overlay feathers are reusable clean-base catalogs but are not packaged as a commons-ready dataset.

### Findings
| # | Axis | Finding | Severity | Disposition | Task |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | Overlay feathers need structural QA for key uniqueness, required columns, allowed tier/pathway values, and source/version columns before annotation. | structural | backlog | task:t191 |
| 2 | 2 | Output-path provenance in overlay annotations is already tracked as a reproducibility issue. | quality | backlog | task:t106 |
| 3 | 3 | Bailey/CGC/Sanchez-Vega processed overlays are reusable base substrates and should get datapackages/entities if reused across projects. | portability | backlog | task:t193 |

## Chain: GENIE panel coverage and callable size registry

- **Axis 1 - Data QA:** WARN - `process_genie_panel_coverage.py` validates source columns and `build_panel_callable_sizes.py` tests callable-size logic, but no wired QA validates the built registry against config.
  - substrates with a wired-in QA step: clean base no; downstream no
  - consumer-contract QA: WARN - downstream TMB and frequency rules assume every required panel has callable Mb and source provenance.
  - companion DAG-validation (output-ownership): WARN
- **Axis 2 - Consistency/quality:** PASS - the chain is config-driven and separates GENIE coverage from callable-size overrides.
- **Axis 3 - Portability/commons:** WARN - the coverage and callable registry are reusable but not packaged/promoted.

### Findings
| # | Axis | Finding | Severity | Disposition | Task |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | Add registry QA checking one row per required panel, positive callable Mb, expected source enum, and override-vs-BED tolerance reporting. | structural | backlog | task:t191 |
| 2 | 3 | Package GENIE coverage, panel BEDs, and callable-size registry with hashes and access notes. | portability | backlog | task:t193 |

## Chain: Hypermutator / TMB sample annotation

- **Axis 1 - Data QA:** FAIL - the chain has many script-level checks and tests, but `metadata/samples_annotated.feather` is load-bearing and has no wired QA target.
  - substrates with a wired-in QA step: clean base no; downstream per-study frequency tables no
  - consumer-contract QA: WARN - `create_freq_tables.py` checks `is_hypermutator`, but does not validate the full annotation contract.
  - companion DAG-validation (output-ownership): WARN
- **Axis 2 - Consistency/quality:** PASS - configuration is explicit for seed, GMM minimum sample size, and panel callable sizes.
- **Axis 3 - Portability/commons:** WARN - sample annotation is project-specific rather than a clean external dataset, but its manifest should travel with canonical outputs.

### Findings
| # | Axis | Finding | Severity | Disposition | Task |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | `samples_annotated.feather` needs wired QA for unique `(study_id, sample_id)`, TMB numeric domains, hypermutator reason enum, boolean dual flags, and GMM status vocabulary. | structural | fix-now | task:t191 |
| 2 | 1 | Relative top-20% hypermutator behavior remains suspect from prior PoC output. | structural | backlog | task:t108 |

## Chain: Per-study mutation-derived tables and matrices

- **Axis 1 - Data QA:** FAIL - per-study count, ratio, matrix, and correlation outputs feed `rule all` but lack per-substrate QA rules.
  - substrates with a wired-in QA step: clean base no; downstream no
  - consumer-contract QA: WARN - some scripts check required columns internally, but final artifacts are not separately validated.
  - companion DAG-validation (output-ownership): WARN
- **Axis 2 - Consistency/quality:** WARN - file naming is consistent, but clustering defaults and correlation scaling are already known risks.
- **Axis 3 - Portability/commons:** WARN - these are mostly project-specific intermediates; portability is lower priority than QA.

### Findings
| # | Axis | Finding | Severity | Disposition | Task |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | Per-study frequency tables need QA for non-negative counts, ratio bounds, denominator columns, cancer/gene key uniqueness, and hypermutator inclusive/exclusive consistency. | structural | fix-now | task:t191 |
| 2 | 1 | Matrices and correlations need shape/key checks and numeric-domain checks before clustering/interpretation. | structural | backlog | task:t191 |
| 3 | 2 | Clustering config defaults are missing from main configs or need an explicit opt-out path. | quality | backlog | task:t107 |
| 4 | 2 | Gene-correlation computation is a known scaling bottleneck for WES studies. | quality | backlog | task:t104 |

## Chain: Cross-study mutation aggregation and meta-analysis

- **Axis 1 - Data QA:** FAIL - this chain is the primary analysis substrate and should have the strongest wired QA; currently checks live in scripts/tests and consumer joins.
  - substrates with a wired-in QA step: clean base no; final analysis substrates no
  - consumer-contract QA: WARN - `join_gene_cancer_meta.py` validates keys and meta-analysis view vocabulary, but there is no full canonical-output QA.
  - companion DAG-validation (output-ownership): WARN
- **Axis 2 - Consistency/quality:** WARN - canonical outputs are documented and the pooled meta-analysis rule declares R sidecars, but `rule all` still includes several raw/intermediate summary tables alongside canonical outputs.
- **Axis 3 - Portability/commons:** WARN - a dataset entity exists for the annotated ratio product, but commons-readiness is blocked by project-wide dataset validation issues.

### Findings
| # | Axis | Finding | Severity | Disposition | Task |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | Canonical count and ratio tables need wired QA for keys, required annotation columns, inclusive/exclusive paired columns, rate bounds, pooled status vocabularies, and no duplicate `(cancer_type, symbol)` rows. | structural | fix-now | task:t191 |
| 2 | 1 | `gene_cancer_pooled_input.feather` and pooled meta-analysis sidecars need structural and result-QA checks for model readiness, convergence statuses, leave-one-out coverage, panel-sensitivity coverage, and placebo seed/status consistency. | structural / result-QA | fix-now | task:t191 |
| 3 | 3 | The canonical annotated ratio product should be made commons-ready after dataset-promotion validation is repaired. | portability | backlog | task:t185; task:t193 |
| 4 | 2 | `rule all` should distinguish consumer-facing canonical outputs from retained raw/intermediate products, either by a QA target or named target groups. | quality | backlog | task:t191 |

## Chain: dNdScv selection scan

- **Axis 1 - Data QA:** WARN - input preparation and R wrapper have schema checks, but result-bundle QA is not wired into the target.
  - substrates with a wired-in QA step: clean base partial; downstream no
  - consumer-contract QA: WARN - `join_dndscv_into_annotated.py` joins an 11-column schema contract, but the full bundle contract is not a rule-level QA output.
  - companion DAG-validation (output-ownership): WARN
- **Axis 2 - Consistency/quality:** WARN - the chain is documented and opt-in, but environment installation remains a known operational issue.
- **Axis 3 - Portability/commons:** WARN - dNdScv results are project-specific analysis outputs, not clean base data.

### Findings
| # | Axis | Finding | Severity | Disposition | Task |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | Add wired QA for dNdScv input, per-cancer run summaries, pooled rollup, and annotated join columns. | structural | backlog | task:t191 |
| 2 | 2 | dNdScv environment bootstrap can race in parallel runs. | quality | backlog | task:t143 |
| 3 | 1 | External validation against non-Bailey driver references is already tracked. | result-QA | backlog | task:t146 |

## Chain: Restricted mutational-signature assignment

- **Axis 1 - Data QA:** WARN - t178/t179 added sidecar audits and count-floor columns, but signature exposure outputs are not yet wired as default QA'd substrates.
  - substrates with a wired-in QA step: clean base partial via sidecars; downstream no
  - consumer-contract QA: WARN - h08 downstream contract is still being specified.
  - companion DAG-validation (output-ownership): WARN
- **Axis 2 - Consistency/quality:** PASS - reference version, caller provenance, and count-floor policy are explicit.
- **Axis 3 - Portability/commons:** WARN - signature outputs are analysis substrates and should be manifest-backed before reuse.

### Findings
| # | Axis | Finding | Severity | Disposition | Task |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | Add wired QA for exposure schema, sample/signature key uniqueness, non-negative exposures, audit sidecar completeness, count-floor missingness, and de-novo/refit decision vocabulary. | structural | backlog | task:t191 |
| 2 | 2 | Treatment-exposure and additional covariate strata remain planned h08 confound controls. | quality | backlog | task:t181; task:t180 |

## Chain: Replication-timing reference and burden comparisons

- **Axis 1 - Data QA:** WARN - `prepare_replication_timing_annotations.py` validates input schemas and coordinate basics, but the clean reference feathers and comparison outputs lack wired QA.
  - substrates with a wired-in QA step: clean base no; downstream no
  - consumer-contract QA: WARN
  - companion DAG-validation (output-ownership): WARN
- **Axis 2 - Consistency/quality:** WARN - current assembly range-check TODO is tracked.
- **Axis 3 - Portability/commons:** WARN - replication-timing reference has a dataset note but not a complete generated package.

### Findings
| # | Axis | Finding | Severity | Disposition | Task |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | Add wired QA for replication-timing bins, per-gene annotation uniqueness, allowed labels, and comparison output domains. | structural | backlog | task:t191 |
| 2 | 2 | Assembly-aware coordinate range checking remains open. | quality | backlog | task:t113 |
| 3 | 3 | Package replication-timing clean-base feathers with dataset entity/datapackage readiness. | portability | backlog | task:t193 |

## Chain: SELECT co-occurrence / mutual-exclusivity

- **Axis 1 - Data QA:** WARN - SELECT has unit and DAG wiring tests, but production chain gaps prevent treating outputs as fully audited.
  - substrates with a wired-in QA step: clean base no; downstream no
  - consumer-contract QA: FAIL - existing task t137 records production wiring mismatches.
  - companion DAG-validation (output-ownership): WARN
- **Axis 2 - Consistency/quality:** WARN - chain is gated and documented, but still has open integration blockers.
- **Axis 3 - Portability/commons:** WARN - outputs are project-specific analysis products; inputs directory is a package-like substrate but lacks manifest/QA.

### Findings
| # | Axis | Finding | Severity | Disposition | Task |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | Add QA for SELECT input directories and aggregate outputs once production blockers are closed. | structural | backlog | task:t137; task:t191 |
| 2 | 1 | Production contract mismatch for `bailey_alteration_class.feather` and other t078 inputs is already tracked. | consumer-contract | backlog | task:t137 |

## Chain: Expression export

- **Axis 1 - Data QA:** PASS - this is the strongest clean-base pattern in the repo: `export_study_expression` emits a QA report and datapackage as declared outputs.
  - substrates with a wired-in QA step: clean base yes for expression export
  - consumer-contract QA: WARN - downstream CYCLOPS-style complete-matrix requirements are recorded in QA, not enforced here by design.
  - companion DAG-validation (output-ownership): WARN
- **Axis 2 - Consistency/quality:** PASS - clean generic export is separated from analysis-specific processing.
- **Axis 3 - Portability/commons:** WARN - package exists, but dataset entity/promotion must be verified per study before commons promotion.

### Findings
| # | Axis | Finding | Severity | Disposition | Task |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | Expression exports are commons-ready in shape but still need dataset entities and dry-run promotion per study. | promote | backlog | task:t193 |
| 2 | 1 | Use expression export as the local pattern for mutation-chain QA reports and datapackages. | structural | backlog | task:t191 |

## Chain: Normal-tissue spectra reference

- **Axis 1 - Data QA:** WARN - the script validates source contract and records dropped-row counters, but outputs are not accompanied by a declared QA artifact.
  - substrates with a wired-in QA step: clean base partial; downstream no
  - consumer-contract QA: WARN
  - companion DAG-validation (output-ownership): WARN
- **Axis 2 - Consistency/quality:** WARN - the current single-source implementation is acceptable, but a second-source adapter refactor is already planned.
- **Axis 3 - Portability/commons:** WARN - this is a reusable reference substrate and should be packaged if reused.

### Findings
| # | Axis | Finding | Severity | Disposition | Task |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | Emit a QA sidecar for normal-tissue spectra/burden outputs covering source-yield, dropped-row counters, 96-context completeness, tissue mapping coverage, and burden numeric domains. | structural | backlog | task:t191 |
| 2 | 2 | Multi-source adapter refactor is already tracked for future normal-tissue sources. | quality | backlog | task:t112 |
| 3 | 3 | Package Li2021-derived spectra and burden tables as a clean reference dataset with access/provenance metadata. | portability | backlog | task:t193 |

## Cross-chain workflow findings

| # | Axis | Finding | Severity | Disposition | Task |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | There is no project-level Snakemake DAG-validation guard for single-writer ownership, declared-input completeness, orphan declared inputs, or dry-run checks across shipped configs. | workflow-DAG | fix-now | task:t192 |
| 2 | 2 | `snakemake --lint` exits nonzero because active rules broadly lack `log:` directives and most Python rules do not declare conda/container execution environments. | quality | backlog | task:t194 |
| 3 | 3 | Project-wide dataset-promotion validation currently has pre-existing failures, blocking reliable commons promotion. | portability | backlog | task:t185 |
