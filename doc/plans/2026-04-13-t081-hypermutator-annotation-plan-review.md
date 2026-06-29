# Pipeline Plan Review: t081 Hypermutator Annotation

- **Plan:** doc/plans/2026-04-13-t081-hypermutator-annotation-pipeline-plan.md
- **Date:** 2026-04-13
- **Reviewer:** independent agent (science:review-pipeline)
- **Overall:** WARN
- **Implementation-ready?** yes-with-caveats

## Summary

The plan is broadly sound in architecture and addresses the core audit findings (TMB/hypermutator confounding). However, three significant issues remain: (1) the GMM implementation lacks a specified `random_state` parameter, creating non-reproducibility risk; (2) the plan claims `mean` can transparently alias `mean_inclusive`, but doesn't acknowledge that downstream consumers of the old single-column `mean` will silently receive inclusive ratios when they may have expected something else; (3) the integration test targets (TCGA-UCEC ~25%, TCGA-COAD ~15%, TCGA-SKCM ~5%) cannot be validated against the current study list, which contains no TCGA cohorts. The plan shows strong process awareness (cooling-off language, decision checkpoints) but needs these three gaps closed before implementation.

## Rubric Results

| Dim | Score | Finding |
|---|---|---|
| **1 — Evidence coverage** | PASS | POLE/POLD1 hotspot lists, TCGA-UCEC rate (25%), panel sizes cited; all reasonable |
| **2 — Assumption audit** | PASS | 7 assumptions are explicit and justified; residual caller bias flagged as acceptable |
| **3 — Data availability** | WARN | TCGA cohorts in integration tests are not in `config-10k-genes.yml`; no baseline for validation |
| **4 — Identifiability** | PASS | DAG is complete; all outputs traced back to inputs |
| **5 — Reproducibility** | FAIL | GaussianMixture lacks `random_state` parameter; bimodal fit will vary between runs |
| **6 — Validation criteria** | WARN | Integration tests reference missing datasets; decision-table row 8 edge case underspecified |
| **7 — Scope check** | PASS | POLE/POLD1/MSI in scope (somatic mutations + clinical); no creep detected |
| **8 — Integration boundaries** | WARN | `mean` aliasing backwards-compat claim underspecified; `create_freq_tables.py` lacks optional-input structure |
| **9 — Manifest completeness** | N/A | No `datapackage.json` used in repo; dimension not applicable |

## Detailed Findings

### HIGH

#### 1. **Missing `random_state` in GaussianMixture will break reproducibility**
- **Issue:** Task 5 specifies `sklearn.mixture.GaussianMixture(n_components=2)` but does NOT set `random_state`. The resulting GMM fit will differ between runs, causing `is_hypermutator_gmm` flags to flip non-deterministically on borderline samples. This violates the **reproducibility requirement for scientific pipelines**.
- **Concrete fix:** Explicitly set `random_state=42` (or document choice) in Task 5 script. Cite in the pipeline docstring that the seed is pinned for reproducibility, not tuning.
- **File refs:** Plan line 291–293; no script yet (to be written in Task 5).
- **Severity:** HIGH — affects every downstream use of `is_hypermutator`.

#### 2. **Integration test targets (TCGA-UCEC, TCGA-COAD, TCGA-SKCM) are not in the config study list**
- **Issue:** Plan lines 102–105 specify validation against "TCGA-UCEC (~25% hypermutator expected)", "TCGA-COAD/READ (~15% hypermutator)", and "TCGA-SKCM (~5%)". However, `code/config/config-10k-genes.yml:56–64` lists only 7 studies: `metastatic_solid_tumors_mich_2017, mixed_allen_2018, mixed_pipseq_2017, pancan_pcawg_2020, pediatric_dkfz_2017, pog570_bcgsc_2020, pptc_2019`. **None of these are TCGA cohorts.** The plan cannot be validated against the stated ground-truth acceptance criteria.
- **Concrete fix:** Either (a) explicitly add TCGA-UCEC, TCGA-COAD, TCGA-SKCM to the config before running Task 5 integration tests, OR (b) revise the acceptance criteria to match studies actually in the config. If (a), document that the config will be pinned for validation. If (b), re-run the acceptance-rate estimates on whichever cohorts are actually present.
- **File refs:** Plan lines 102–105 vs config-10k-genes.yml:56–64.
- **Severity:** HIGH — validation tests will not run; cannot confirm the approach works.

#### 3. **`mean` aliasing for backward-compat contradicts downstream-consumer realities**
- **Issue:** Plan line 426 claims "`mean` remains as an alias for `mean_inclusive`", and Task 7 intends this to be transparent to legacy code. However, this is not truly transparent — consumers that expect `mean` to be inclusive (numerator = samples with mutation, denominator = all samples) will get exactly that, but consumers that expected some kind of cancer-type-stratified mean, or a different denominator, will silently receive the wrong value. The plan doesn't audit whether any downstream consumers actually expect `mean` to mean something else. **Silent semantic drift is a bug vector.**
- **Concrete fix:** Before implementation, grep for all uses of the `mean` column downstream: `annotate.py`, clustering scripts, Rmd reports, publication-path Jupyter notebooks. For each, verify that `mean_inclusive` semantics are actually correct. If any consumer expects a different semantics, choose a different aliasing strategy (e.g., drop the alias and require explicit column selection).
- **File refs:** Plan lines 426; config lines not audited. Consumer audit needs to include `code/scripts/{annotate.py, cluster_*.py}` and any `.Rmd` or notebooks in `results/`.
- **Severity:** HIGH — risk of silently breaking downstream analysis.

### MEDIUM

#### 4. **Decision-table row 8 (TMB unavailable) needs explicit edge-case handling in tests**
- **Issue:** Plan lines 326–327 specify that when `tmb is NaN`, the sample is flagged `is_hypermutator = False` with reason `"tmb_unavailable"`. But the decision-table test (Task 6, line 347+) doesn't show a row 8 test case. More importantly, the interaction with rows 1–3 is underspecified: if a sample has `pole_hotspot_detected = True` but `tmb_log10 = NaN` (panel unknown), what happens? The decision table says "row 1 fires first," but row 1 doesn't check TMB. So a POLE-hotspot sample with unknown panel would still be flagged True. That's correct, but the tests need to explicitly validate this edge case to prevent future regressions.
- **Concrete fix:** Add a test row: "POLE hotspot + tmb NaN → is_hypermutator == True, reason = 'pole_hotspot'" (i.e., confirm that strong signals override missing TMB). Also add "no signals + tmb NaN → is_hypermutator == False, reason = 'tmb_unavailable'".
- **File refs:** Plan Task 6, test section line 346+.
- **Severity:** MEDIUM — correct logic, but insufficient test coverage invites future breaks.

#### 5. **`create_freq_tables.py` modification requires optional-input plumbing in Snakemake rule**
- **Issue:** Plan Task 7a (line 404–407) says the script should "accept optional second input `samples_annotated.feather` path". However, the Snakemake rule signature was not shown in the plan; the current rule (Snakefile) has fixed input positions. The plan doesn't specify whether this is a Snakemake `input.samples_annotated` named input or how the rule handles the case where `samples_annotated.feather` doesn't exist yet (e.g., on a legacy run without the hypermutator tasks). Ambiguity here can lead to rule failure on partial DAGs.
- **Concrete fix:** Specify in Task 7a that the Snakemake rule gains a second optional input: `samples_annotated = expand(out_dir.joinpath("metadata/samples_annotated.feather"), allow_missing=True)` or similar, and the script checks `if snek.input[1] is not None` before attempting to join. Alternatively, document that the rule always requires the new input and t081 must be fully in the DAG.
- **File refs:** Plan Task 7a line 411; current Snakefile rule at `code/workflows/Snakefile` (verified, no optional inputs shown).
- **Severity:** MEDIUM — will cause cryptic rule failures if not handled.

#### 6. **Panel-callable-Mb registry is a generated artifact, not version-controlled — caching strategy unclear**
- **Issue:** Plan line 145–146 correctly states that `panel_callable_mb.tsv` is a **generated build artifact, NOT version-controlled**. However, the plan doesn't specify: (a) if this is regenerated on every pipeline run, or (b) if it's cached and only regenerated when config/GENIE input changes. If (a), the Snakemake rule should have no `persist` flag. If (b), the caching strategy needs to be explicit in the rule (e.g., `localrules: build_panel_callable_sizes`). The choice affects reproducibility and runtime.
- **Concrete fix:** Specify in Task 1 whether `panel_callable_mb.tsv` is ephemeral-per-run or persistent across runs with the same config. If persistent, declare `localrules: build_panel_callable_sizes` in the rule to avoid cluttering temp files.
- **File refs:** Plan Task 1, line 145–146.
- **Severity:** MEDIUM — affects DAG correctness and runtime, but not data integrity.

### LOW / Nitpicks

#### 7. **Diptest dependency declaration inconsistent**
- **Issue:** Plan line 59 mentions `diptest>=0.9` as a new dependency, but the plan also says (line 534) to add `pytest>=8.0` to `pyproject.toml` dev-deps. However, reading the current `pyproject.toml` (line 1–23), I see `diptest` is NOT listed anywhere; it should also be in `[project.dependencies]` if it's a runtime dependency. The plan should clarify: is `diptest` a runtime or dev dependency?
- **Concrete fix:** Add `diptest>=0.9` to `[project.dependencies]` in `pyproject.toml` (not dev — it's needed at runtime for Task 5). Update Task 8 to include this.
- **File refs:** Plan line 59, 534; `pyproject.toml` line 7–14.
- **Severity:** LOW — easy fix, but omission would cause import errors at runtime.

#### 8. **Hartigans dip test p-value threshold logic could be over-sensitive**
- **Issue:** Plan line 288 specifies "dip test p > 0.1 → fit_quality = 'not_bimodal'". A p-value threshold of 0.1 is liberal (typically 0.05 is convention). For small cancer-type cohorts (N < 100), the dip test has low power; a false negative (p > 0.1 when bimodality exists) is likely. The plan acknowledges this (line 287 fallback) but doesn't quantify the error rate or recommend a sensitivity analysis.
- **Concrete fix:** Document in Task 5 that the p-value threshold is a tuning parameter; recommend a sensitivity analysis (re-run at p=0.05 and p=0.15) and report how many cancer types change fit_quality under the alternatives.
- **File refs:** Plan Task 5, line 288.
- **Severity:** LOW — acceptable as stated, but additional validation recommended.

#### 9. **Cooling-off period is specified but not enforced**
- **Issue:** Plan line 3 and line 568 explicitly request a ≥24-hour cooling-off before implementation and ideally a separate reviewer pass. However, there is no mechanism to enforce this — the next section doesn't mention who enforces it or what prevents immediate implementation. In the context of the bias audit flagging "process bias" (single-analyst iteration, 23 tasks in one day), the cooling-off is hygiene but lacks teeth.
- **Concrete fix:** No code change needed, but recommend: (a) formally add a "blocked-by-cooling-off" task to the backlog, marked for auto-completion ≥24 hours from plan creation (could be a scheduled reminder), and (b) add the requirement to AGENTS.md that t081 implementation cannot begin until this checklist item is closed.
- **File refs:** Plan line 3, 568.
- **Severity:** LOW — process issue, not technical.

## Strengths

1. **Explicit assumption itemization:** All 7 assumptions are listed, justified, and impact-rated. Residual biases (caller divergence, panel coverage dropouts) are acknowledged and not hand-waved.
2. **Decision-table formalism:** The composite scoring policy (rows 1–8) is unambiguous and testable; priority ordering is clear and defended. This closes audit finding F4 (inconsistent policy).
3. **Per-cancer-type validation targets:** The plan names specific cohorts and acceptance ranges, making the validation criteria falsifiable (even though the cohorts aren't in the config yet).
4. **Process awareness:** The plan explicitly requests a cooling-off period, separation from synthesis, and review — evidence of thinking about meta-process.
5. **Scope discipline:** Correctly punts signature decomposition and CNA; stays on somatic mutations + clinical.
6. **Backwards-compat attention:** The plan documents the intent to retain `num` / `ratio` aliases and preserve existing outputs, which is considerate.

## Recommendations (prioritized)

1. **BEFORE Task 1:** Pin the `random_state=42` for GaussianMixture in Task 5 placeholder; document this choice in the task header. Add a "Reproducibility covenant" statement to the pipeline docstring.
2. **BEFORE Task 1:** Either add TCGA-UCEC, TCGA-COAD, TCGA-SKCM to the config, or revise the integration test acceptance criteria to match the studies that are actually in scope. Choose one path and document in Task 5.
3. **BEFORE Task 7a:** Audit all downstream consumers of the `mean` column in `{annotate.py, cluster_*.py, summary_*.Rmd}` and confirm that `mean_inclusive` semantics are correct. If any mismatch found, choose a different backward-compat strategy (e.g., no alias; explicit selection).
4. **Task 6 test design:** Add explicit edge-case rows to the decision-table parametrized test: row 1 with NaN TMB, row 8 validation, and priority override verification.
5. **Task 7a Snakemake rule design:** Specify the rule input signature for the optional `samples_annotated` input and how the script handles its absence (pre-existing legacy runs).

## Open questions for the author

1. **Integration test cohorts:** The plan references TCGA-UCEC, TCGA-COAD, TCGA-SKCM as ground truth, but these aren't in the current config. Are you planning to ingest these for validation, or should the acceptance targets be re-estimated from the cohorts that are in scope?
2. **Mean-column aliasing:** Have you audited the downstream consumers of the `mean` column (especially `annotate.py`, clustering, and any Rmd reports) to confirm that transparent aliasing to `mean_inclusive` is semantically correct for all of them?
3. **Random seed:** Why `random_state=42`? Is this a deliberate choice, or should it be a config parameter so analyses can be re-run with different seeds to assess stability?

## Commit Record

This review does not commit changes; it is a standalone assessment document. Implementation should proceed only after addressing the three HIGH findings and confirming the `task:t081` decision criteria (lines 555–559) are achievable with the studies in scope.
