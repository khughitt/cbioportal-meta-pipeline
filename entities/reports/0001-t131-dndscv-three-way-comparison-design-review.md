---
type: report
title: "Pipeline review \u2014 t131 dNdScv three-way ranking comparison (design v3)"
status: active
created: '2026-04-25'
updated: '2026-06-28'
id: report:0001-t131-dndscv-three-way-comparison-design-review
plan: doc/plans/2026-04-24-t131-dndscv-three-way-comparison-design.md
related:
- task:t131
- question:0011-gene-length-as-literature-attention-confounder
- discussion:0001-gene-length-bias-in-mutation-rankings-and-literature
- task:t136
overall: WARN
---

# Pipeline Review — t131 dNdScv three-way ranking comparison

- **Plan:** `doc/plans/2026-04-24-t131-dndscv-three-way-comparison-design.md` (design v3)
- **Implementation status:** shipped to `main` in commits `673b1a3` (impl) + `021bc5b` (PoC bug fixes); end-to-end PoC run executed against 4 studies / 57 cancer types; full pan-cancer-dndscv run not yet started.
- **Date:** 2026-04-25
- **Overall:** **WARN — proceed with caveats**

## Summary

The t131 plan is methodologically sound, has empirical validation from the PoC run (74/199 Bailey drivers @ top-100; clean `question:0011-gene-length-as-literature-attention-confounder` falsifier readout), and the implementation matches the design with the schema contract, status enum, and split-build flag all correctly wired. The main weaknesses are operational rather than methodological: (a) the conda env path has not been validated end-to-end (PoC used system R, violating `feedback:r-reproducibility`); (b) reproducibility seeding is incomplete — `random_seed` is declared in config but is not threaded through to `set.seed()` in `run_dndscv.R`; (c) the t131 schema landed on a *new* file `_dndscv.feather` rather than mutating the canonical `gene_cancer_study_ratio_annotated.feather`, which is a safer choice than the plan called for but means downstream consumers must opt in explicitly. Two methodological items deserve a second look before publishing: dNdScv's built-in `max_coding_muts_per_sample=3000` filter is *independent* of the project's existing `annotate_hypermutators` step and may produce a different sample-exclusion set than the user expects (POLE/UCEC/SKCM cohorts in particular); and the PubTator `entrez→symbol` join via `data/grch37.tsv` is likely incomplete, which will bias the `question:0011-gene-length-as-literature-attention-confounder` falsifier toward older/established gene symbols.
This report reviews `task:t131`, is grounded in
`discussion:0001-gene-length-bias-in-mutation-rankings-and-literature`, and leaves the
GRCh38 canonicalization follow-up to `task:t136`.

## Rubric Results

| Dimension | Score | Issues |
|---|---|---|
| 1. Evidence coverage | WARN | Threshold parameters (`dndscv_min_samples=50`, `dndscv_min_variants=500`, `max_coding_muts_per_sample=3000`) heuristic and uncited. |
| 2. Assumption audit | WARN | Min-q vs Stouffer choice well-justified. PubTator-as-literature-attention proxy not interrogated. Hypermutator-handling assumption uncoordinated with `annotate_hypermutators`. |
| 3. Data availability | PASS-with-caveat | All required paths verified on disk (incl. PubTator + grch37.tsv); GENIE in `studies` requires synapse sync; no formal `dataset:<slug>` entity tracking (project-wide gap). |
| 4. Identifiability | PASS | Snakemake DAG fully connected; PubTator conditional input is null-safe. |
| 5. Reproducibility | WARN | Conda env + dndscv git SHA pinned; `random_seed` config knob exists but is *not* threaded into `run_dndscv.R` (`set.seed` never called). Conda path itself never run end-to-end. |
| 6. Validation criteria | WARN | Smoke tests enumerated in plan; no automated test fixtures shipped; PubTator-correlation panel has no falsification criterion beyond "either result is informative." |
| 7. Scope check | PASS | Within `specs/research-question.md`. Literature-attention sub-axis is methodological cross-check, justified via `question:0011-gene-length-as-literature-attention-confounder`. |
| 8. Integration boundaries | PASS-with-caveat | Schema-contract types pinned; new file `gene_cancer_study_ratio_annotated_dndscv.feather` is *additive*. Downstream consumers reading the un-suffixed file see no new columns and do not break — but also gain no signal unless updated. Plan said "join into the canonical feather"; implementation chose the safer additive-file route. Update `doc/guides/canonical-outputs.md` to reflect this. |
| 9. Manifest completeness | N/A | Project does not generate `datapackage.json` for any pipeline output; not specific to t131. |

## Detailed Findings

### F1 — Reproducibility seed is declared but never used (Dim 5)

`code/config/config-pan-cancer-dndscv.yml:53` carries `random_seed: 0`, mirroring the t081 hypermutator-annotation reproducibility covenant. But `code/scripts/run_dndscv.R` never calls `set.seed()` and never reads `snakemake@config[["random_seed"]]`. dNdScv's `dndscv()` invokes maximum-likelihood fits (`poilog`-based negative-binomial overdispersion estimation, indel rate fits) that can vary run-to-run on borderline cohorts. For headline numbers like the PoC's "74/199 Bailey drivers @ top-100" to be exactly reproducible, the seed needs to flow through.

**Recommendation:** Add `set.seed(snakemake@config[["random_seed"]])` near the top of `run_dndscv.R`, immediately after the bootstrap+library block. Pass `random_seed` into the rule's `params` for visibility. Cost: 2 lines.

### F2 — Hypermutator handling is uncoordinated with `annotate_hypermutators` (Dim 2)

The pipeline already has a formal hypermutator-annotation step (`annotate_hypermutators`, plan `doc/plans/2026-04-13-t081-hypermutator-annotation-pipeline-plan.md`) that produces `metadata/samples_annotated.feather` with an 8-category audit-trail `hypermutator_reason`. dNdScv's built-in `max_coding_muts_per_sample = 3000` filter (set in `run_dndscv.R:201`) is *independent* of that — it operates on the per-cancer-type combined cohort and silently excludes any sample with > 3000 coding mutations.

For UCEC (POLE), SKCM (UV), and MSI-H cohorts this matters in two ways:
1. The dndscv-internal filter at 3000 disagrees with the project's documented absolute hypermutator threshold of 10 mut/Mb (≈ 300 muts in 30 Mb) and ultra threshold of 100 mut/Mb (≈ 3000 muts) — so the dndscv filter is *roughly* the ultra-hypermutator cut, not the standard hypermutator cut. The PoC's UCEC dndscv-significance row reflects POLE-driven cohorts unevenly: some POLE samples are dropped by the 3000 cap, others retained.
2. There is no audit trail. `prepare_dndscv_input.py` does not log which samples dndscv will end up dropping; the user only sees the final retention rate from `run_dndscv.R`.

**Recommendation:** Add explicit upstream filtering using the existing `annotate_hypermutators` output (`is_hypermutator_ultra`) in `prepare_dndscv_input.py`, document the choice in the side-config header, and either (a) drop the dndscv internal cap to a higher value, or (b) emit a per-cohort log line counting the samples dropped by each filter. Phase-2 follow-up; not blocking the full run.

### F3 — PubTator `entrez→symbol` join via `data/grch37.tsv` is incomplete (Dim 2)

`compare_three_way_rankings.py:112-128` joins PubTator concept_ids to symbols via `data/grch37.tsv` (Ensembl GRCh37 entrez↔symbol map). The plan flags this as a known limitation that HGNC alias normalization (`task:t082`) would fix. Two specific risks for the `question:0011-gene-length-as-literature-attention-confounder` falsifier:

1. **Symbol drift** — Common-word symbols (CAT, SET, ACE, PAX) and symbols renamed since GRCh37 (KMT2A↔MLL, etc.) will be either lost or mis-merged. The mis-merge case actively biases the literature-attention slope.
2. **Multi-entrez genes** — A symbol with multiple entrez IDs (recurrent for genes with paralogs / readthrough transcripts) gets PubTator counts summed across all entrez. The script does this via `groupby(symbol)["n"].sum()`. That is the right convention but inflates the count for a small number of genes (e.g., gene families with many pseudogene paralogs).

**Recommendation:** Before publishing the `question:0011-gene-length-as-literature-attention-confounder` falsifier readout from the full run, either (a) check the join-rate against PubTator's own gene-info dump and report it in the notebook, or (b) gate the `question:0011-gene-length-as-literature-attention-confounder` panel on `task:t082` landing first. Cheap remediation: in the notebook, add a "PubTator join coverage" cell reporting `n_pub / n_with_dndscv_signal` to make the gap visible.

### F4 — Out_dir choice has order-of-magnitude cost implications (operational)

`config-pan-cancer-dndscv.yml:28` writes to `/data/packages/cbioportal/pan-cancer-dndscv/`, which does not currently exist on disk. Full run cost depends on whether the user wants a clean rebuild or wants to share upstream outputs with `/data/packages/cbioportal/pan-cancer/` (which does exist).

- **Clean rebuild path:** ~hours of upstream pipeline (download + convert_to_feather + filter + annotate chain + meta-analysis) before any dndscv work runs. The handoff doc's "147 jobs / 30-90 min" estimate appears to assume the *existing* pan-cancer/ outputs are reused, not a clean rebuild.
- **Shared-upstream path:** symlink `pan-cancer-dndscv/studies/` and `pan-cancer-dndscv/summary/` to `pan-cancer/`'s versions, OR change `out_dir` to `pan-cancer/`. The latter mutates the canonical pan-cancer out_dir with the new `_dndscv` outputs, which is fine since they're additive.

**Recommendation:** Confirm with the user which mode they want before kicking off the full run. If clean rebuild, expect hours of work and budget accordingly. If shared upstream, change the out_dir or pre-stage symlinks.

### F5 — Per-cancer-type build-split: min-q rollup may inflate small-cohort q (Dim 2 / 6)

`reconcile_dndscv_per_cancer.py:128-146` takes min(qglobal_cv) across builds for any cancer type that spans both hg19 and hg38 sub-cohorts, and sets `dndscv_split_build = True`. This is the documented choice — a single warning flag for consumers to filter on. But a small hg38 sub-cohort that achieves q=1e-6 for a gene will outrank a large hg19 sub-cohort that achieves q=1e-5, even though the latter has more evidence.

The plan acknowledges this as a known approximation and the long-term fix is t136 (canonicalize to GRCh38). For the `question:0011-gene-length-as-literature-attention-confounder` falsifier readout this is unlikely to matter (top-100 driver recovery is dominated by mono-build cancer types). For per-cancer claims about specific tissues it could matter.

**Recommendation:** Document explicitly in the notebook's split-build cell: "for cancer types with `dndscv_split_build = True`, the q-value reported is min across sub-cohorts, not a unified-cohort q. Treat per-cancer significance for these as a lower-bound on the unified q." No code change required.

### F6 — Threshold parameters lack citation (Dim 1)

`dndscv_min_samples = 50` and `dndscv_min_variants = 500` (config defaults) are heuristic. Martincorena et al. [@Martincorena2017] and the dndscv tutorial recommend "at least a few hundred samples" for reliable signal but do not give a hard threshold. The 3000-coding-muts hypermutator cap is the dndscv default.

**Recommendation:** Add a brief comment in the config header explaining the 50/500 choice ("conservative — below ~50 samples the trinucleotide background is unreliable per dndscv tutorial; 500 variants is roughly 10/sample × 50 samples"). Add citation for Martincorena et al. [@Martincorena2017] inline. Cost: a few lines of documentation; no code change.

### F7 — `panel_bearing_studies` config is not consulted by `prepare_dndscv_input.py` (Dim 8)

`prepare_dndscv_input.py:97-106` infers per-sample modality from the presence of `panel_id` in the sample row. But `config-pan-cancer-dndscv.yml:44-45` declares `panel_bearing_studies: [msk_met_2021]`, which is the canonical project list. If a panel-bearing study has any samples without populated `panel_id` (e.g., samples that were sequenced on a now-retired panel that wasn't re-mapped), those samples will be classified as `modality = "wes"` and will land in the WES sub-cohort.

The downstream impact is that `dndscv_input_modality = "mixed"` will be triggered for cancer types that should have been classified as `panel`, and `dndscv_wes_only=true` will not actually exclude all panel data when set.

**Recommendation:** Cross-check that for the studies in the run config, every sample with `panel_id IS NULL` is genuinely WES. Quick smoke check: `pd.read_feather("studies/msk_met_2021/metadata/samples.feather")[["sample_id","panel_id"]].isnull().sum()`. If counts are >0, change `prepare_dndscv_input.py` to also consult `panel_bearing_studies` from config: any study in that list → all its samples are `modality = "panel"`.

### F8 — File deviation from plan: `_dndscv.feather` instead of mutating the canonical (Dim 8)

The plan §"Schema contract on canonical feather" says: "`gene_cancer_study_ratio_annotated.feather` gains the following columns." The implementation writes a *new* file `gene_cancer_study_ratio_annotated_dndscv.feather` and leaves the un-suffixed canonical untouched. This is the **safer** choice (existing consumers continue to work without re-validation) but it means:

- Consumers must opt in by reading the new path.
- `doc/guides/canonical-outputs.md` needs updating to document the new file (currently not done — verify before merge).
- The "canonical" status is now ambiguous: is the canonical `_annotated.feather` (no dndscv) or `_annotated_dndscv.feather` (with dndscv)?

**Recommendation:** (a) Update `doc/guides/canonical-outputs.md` to add `_annotated_dndscv.feather` as a separate canonical output, document its provenance and which downstream consumers should prefer it. (b) Optionally: have `rule join_dndscv_into_annotated` also overwrite the un-suffixed file when run, matching the original plan. The PoC results are unaffected either way.

### F9 — No automated test fixtures shipped (Dim 6)

The plan §"Validation steps" enumerates several smoke tests (prepare_dndscv_input on existing PoC mut.feather, combine_mut_per_cancer with empty inputs, etc.) but no test file under `tests/` was committed. This means each smoke test depends on the user remembering to run it manually after refactors.

**Recommendation:** Defer to follow-up — a `tests/test_dndscv_chain.py` with the synthetic-fixture cases from the plan §"Validation steps" item 4. Phase-2 work; not blocking the full run.

### F10 — Conda env path validated only by env build, not by Snakemake `--use-conda` invocation (Dim 5 / operational)

Per handoff: PoC ran against system R; conda env was successfully built once via `micromamba env create`, but Snakemake `--use-conda --conda-frontend mamba` was never exercised end-to-end. Two failure modes that won't surface until the full run:
1. `bioconductor-rsamtools` build failure on certain conda channel combinations (occurs on Linux x86_64 occasionally).
2. The dndscv self-bootstrap inside the conda env may fail silently if `r-remotes` cannot reach GitHub from the rule's spawned shell environment.

**Recommendation:** Before kicking off the full run, do a single-cancer-type smoke run with `--use-conda` to validate. The plan §"Validation steps" item 5 anticipated this with a `config-dndscv-smoke.yml`; that smoke config does not currently exist. Add one (1 small WES study + 1 cancer type, ~10 min including env build) before the full pan-cancer run. **This is the single most important pre-run check.**

## Recommendations (in priority order)

1. **F10** — Run the conda env path on a single (study, cancer_type) before the full pan-cancer-dndscv run. Add `code/config/config-dndscv-smoke.yml` if not present.
2. **F4** — Decide `out_dir` strategy (clean rebuild vs shared upstream from `pan-cancer/`); confirm with user before kickoff.
3. **F1** — Add `set.seed(snakemake@config[["random_seed"]])` in `run_dndscv.R` (2 lines).
4. **F8** — Update `doc/guides/canonical-outputs.md` to document the new `_annotated_dndscv.feather`.
5. **F3** — Add a PubTator join-coverage cell to the notebook before relying on the `question:0011-gene-length-as-literature-attention-confounder` falsifier readout for any external claim.
6. **F2** — Phase-2 follow-up task: coordinate `prepare_dndscv_input.py` filtering with `annotate_hypermutators` output.
7. **F7** — Spot-check `panel_id` populated-ness in `msk_met_2021/metadata/samples.feather`; if mixed-null, fix the modality inference.
8. **F5, F6, F9** — Documentation / test-fixture work; not blocking.

## Strengths

- The plan **identifies and closes two latent bugs** in the original `run_dndscv.R` (column-name mismatch + `mut_filtered.feather` input source). That is the kind of finding a review pass is supposed to surface, and it was caught at planning time rather than at run time.
- **The schema contract is comprehensive and the status enum is well-designed.** The `not_run / below_threshold / failed_qc / tested_not_significant / tested_significant` taxonomy avoids the common pitfall of conflating "absent" with "tested-and-null."
- **Min-q rollup choice is correctly justified** with a tissue-specific-driver argument (BRAF/melanoma, KRAS/pancreatic) — this is exactly the kind of decision-with-rationale a future reviewer should not have to relitigate.
- **PoC empirical results validate the design**: dNdScv recovers 74/199 Bailey drivers @ top-100 vs. raw=5 / length-adj=6, and the `question:0011-gene-length-as-literature-attention-confounder` falsifier panel shows the predicted gradient (raw ρ=+0.127 → length_adj ρ=−0.009 → dNdScv ρ=+0.055). The plan's headline claim survived first contact with data.
- **Fail-loud build-metadata behavior** correctly implements `AGENTS.md`'s "explicit > defensive, fail early" rule. The `study_reference_build_override` map is the right escape hatch.
- **Side-config + side-target** keeps the default `rule all` R-free for users without conda. Good operational hygiene.
- **Latent-bug fix attribution** in the eventual commit message — good provenance discipline.

## Process Notes

- This project does not have a `doc/inquiries/` directory; the review is filed alongside the plan in `doc/plans/`. Adjusted Step 3 of the workflow accordingly.
- `science-tool inquiry validate` returned "no inquiries found" — the t131 plan is a task plan, not a formal inquiry. Applied the rubric to the plan's internal consistency rather than to a parent inquiry, per the workflow's sub-plan handling guidance.
- No `specs/scope-boundaries.md` in this project; cross-referenced against `specs/research-question.md` instead.
