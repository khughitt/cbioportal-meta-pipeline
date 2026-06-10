# t127 — q008 quantitative pilot: unmatched-normal SBS1/SBS5 contamination magnitude — Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development. Steps use `- [ ]` checkbox syntax.

**Goal:** Produce a first numeric **pilot estimate** of how the SBS1+SBS5 exposure-fraction differs between matched-normal and unmatched-normal cohorts of the same cancer type, under the existing t109/t110 SigProfilerAssignment surface, and test whether subtracting the Li2021 normal-tissue spectrum (t111 output) as a residual-matrix transform attenuates the gap. Closes the "built-but-unexploited" gap from `meta:0007-next-steps-and-gap-analysis-2026-04-24` for `question:0008`.

**Framing.** This is a **pilot consistency test**, not a causal attribution. The matched/unmatched contrast confounds normal-status with assay (WES vs panel), variant caller, primary-vs-clinical cohort, and likely age/stage mix. The verdict language reflects this: results read as "consistent / inconsistent with contamination" with named alternative explanations; causal attribution requires a follow-up study with a within-cohort matched-vs-unmatched comparator.

**Pre-registered hypothesis (q008 quantitative).** In matched-cancer-type cohorts that pass all sensitivity gates, unmatched-normal samples carry a higher fraction of SBS1+SBS5 mutations than matched-normal samples; this gap is reduced when the per-tissue Li2021 spectrum is subtracted as a fixed shape offset prior to re-assignment.

**Pre-registered thresholds (committed before any decomposition is run; no post-hoc relaxation).**

- **Effect threshold:** ≥ 5 percentage-point cohort-mean Δ(SBS1+SBS5 fraction) — substantive consistency. < 2 pp — null. 2–5 pp — mild.
- **Subtraction "rescue":** Δ(c\*) ≤ 50 % of Δ(c=0) AND collateral cancer-type signature change (SBS2/SBS3/SBS10/SBS13) ≤ 10 % per signature.
- **Test:** two-sided Mann–Whitney U on per-sample SBS1+SBS5 fraction, BH-FDR across cancer types; bootstrap (1000 resamples, seed 0) for cohort-mean Δ CI.
- **No-go rule:** if fewer than **3** cancer types survive the Task 1 feasibility gate, the run is downgraded to a *descriptive* pilot (per-cancer-type Δ reported, but the "≥ half of cancer types" verbiage and any aggregate verdict are dropped).
- **No-go rule (subtraction arm):** if fewer than **3** cancer types are subtraction-eligible (Li2021 tissue mapping present + survives feasibility gate), the subtraction verdict is descriptive only.

**Scope:** SBS only. Single matched-vs-unmatched study pair. No de-novo NMF, no MuSiCal cross-tool comparison, no purity covariate, no LRR/ERR test (deferred, per t126 / q009).

**Tech stack:** Python 3.13+, the existing `code/scripts/run_restricted_sigprofiler_assignment.py` and Snakefile rules (no parallel decomposition path), plus a new `subtract_normal_background.py` operating on the SBS96 matrix. Statistical comparison + interpretation in a marimo notebook.

**Related:** `task:t127`, `task:t109`, `task:t110`, `task:t111`, `task:t126`, `question:0008`, `question:0009`, `topic:signature-decomposition-unmatched-normal`, `paper:Li2021`, `paper:DiazGay2023`.

---

## Cohort selection (raw-comparison population)

| Role | Study | Sequencing | Normal | Build |
|---|---|---|---|---|
| Matched-normal anchor | `tcga_mc3` | WES (MC3 7-caller consensus) | matched | GRCh37 (verify per Task 0) |
| Unmatched-normal probe | `msk_impact_2017` | MSK-IMPACT panel (~410–468 genes) | unmatched / PoN | per `metadata/study_build.txt`; do not assume |

**Confounders the verdict must explicitly note (named, not dismissed):** WES vs panel callable territory; variant caller / filter pipeline (MC3 7-caller vs MSK clinical); primary-treatment-naïve vs metastatic-clinical cohort balance; tobacco-/UV-exposure mix; age distribution. Sensitivity controls in Task 4.

**Subtraction-eligible population.** Restricted to cancer types whose tissue maps to a Li2021 organ (Bronchia, Cardia, Colon, Duodenum, Esophagus, Liver, Pancreas, Prostate, Small Intestine — exact list emitted in Task 3 from `data/normal_tissue_spectra.tsv`). Cancer types without a Li2021 reference (Breast, Ovarian, Glioma, Endometrial, Bladder, Melanoma, etc.) appear in the raw-comparison arm only.

---

## Task 0 — Pre-flight gate

Before any code is written; before Task 1 runs.

- [ ] **Step 1: SigProfilerAssignment is already a project dep (t109/t110).** Verify by running the existing rule on a small fixture or checking that `studies/<id>/mut/signatures/restricted_assignment_per_sample.feather` exists for at least one current study. No new `uv add`.
- [ ] **Step 2: Confirm the Snakefile per-sample surface (`rule run_restricted_sigprofiler_assignment_per_sample`, `code/workflows/Snakefile:612`) is the input we use.** Output schema documented at `code/scripts/run_restricted_sigprofiler_assignment.py:430` — long-format `(study_id, cancer_type, sample_name, signature, exposure, total_mutations, cosine_similarity, ...)`.
- [ ] **Step 3: Per-study assembly check.** Read `studies/tcga_mc3/metadata/study_build.txt` and `studies/msk_impact_2017/metadata/study_build.txt` (or equivalent — confirm the file name in `convert_to_feather.py`). Record both. Wire each study's build into the Snakemake invocation rather than assuming the single global `signature_assignment_genome_build`. If the field doesn't exist, file a sub-task to add it; do **not** proceed with a hard-coded build.
- [ ] **Step 4: Commit this plan and the threshold pre-registration before any decomposition runs.**

---

## Task 1 — Feasibility table (hard pre-run power gate)

This task replaces the old "≥ 5 cancer types" handwave. We compute the projected retained-sample and retained-SBS counts per cancer type *before* committing to the comparison; the cancer-type list emerges from the table, it is not declared up front.

**Files:**
- New: `code/scripts/build_q008_feasibility_table.py`
- New: `code/scripts/tests/test_build_q008_feasibility_table.py`
- Output: `results/q008-quantitative-pass-2026-04-28/feasibility/feasibility_table.feather`

For each cancer-type label present in **both** `studies/tcga_mc3/metadata/samples.feather` and `studies/msk_impact_2017/metadata/samples.feather`:

- [ ] **Step 1: Per-sample SBS-call counts.** From each study's `mut.feather`, count SBS calls per sample (filter chrom-normal, ref/alt single-nucleotide ACGT — same filter as `prepare_sigprofiler_variants`).
- [ ] **Step 2: Apply sensitivity exclusions before counting** (per review F3): drop hypermutators (use the existing `samples_annotated.feather` `is_hypermutator` flag from the t081 hypermutator pipeline), drop MSI-H, drop POLE/POLD1 hotspot carriers. Record dropped counts.
- [ ] **Step 3: Apply count-floor filter (n_sbs ≥ 20)** and report the dropped fraction.
- [ ] **Step 4: Emit the feasibility table** with columns: `cancer_type, n_matched_pre, n_matched_hypermut_dropped, n_matched_msi_dropped, n_matched_pole_dropped, n_matched_n20_dropped, n_matched_retained, median_sbs_matched, n_unmatched_pre, ..._retained, median_sbs_unmatched, li2021_tissue_uberon (or null), li2021_eligible_bool, raw_eligible_bool`.
- [ ] **Step 5: Eligibility rule.** A cancer type is `raw_eligible` iff `n_matched_retained ≥ 50 AND n_unmatched_retained ≥ 50 AND median_sbs_unmatched ≥ 20`. It is `li2021_eligible` additionally iff `li2021_tissue_uberon is not null`.
- [ ] **Step 6: Decision.** Count `raw_eligible` cancer types. If < 3, halt and re-frame as descriptive pilot per the no-go rule. If ≥ 3, proceed; record the canonical eligible-cancer-type list to the feasibility table.

---

## Task 2 — Run the existing per-sample assignment surface

We do **not** build a new SBS96 / decomposition path. We use what t109/t110 already produce, plus one tweak.

**Files:**
- Touch: `code/scripts/run_restricted_sigprofiler_assignment.py` (small extensions only)
- Touch: `code/workflows/Snakefile` (configuration only; no new rules)

- [ ] **Step 1: Persist the per-cohort SBS96 matrices.** The existing script writes the matrix to `group_dir / "sample_matrix.tsv"` inside `work_dir` and then deletes `work_dir` (`code/scripts/run_restricted_sigprofiler_assignment.py:471` and `:488`). Add a small extension: when a `--keep-matrix-output <path>` parameter (or equivalent Snakemake `params.keep_matrix`) is set, copy each `sample_matrix.tsv` to `<path>/{study_id}__{lookup_key}.SBS96.tsv` before tearing down. This makes the matrices available as the input to Task 3 without re-running matrix generation.
- [ ] **Step 2: Add a parallel input mode `--matrix-input <path>`.** When set, skip `prepare_sigprofiler_variants` + `build_sigprofiler_input_matrix` and feed the matrix directly to `run_sigprofiler_assignment`. This is what the subtraction arm (Task 3) needs.
- [ ] **Step 3: Run per-study, per-sample assignment for the eligible cohort.** Use the existing `rule run_restricted_sigprofiler_assignment_per_sample` for `tcga_mc3` and `msk_impact_2017`, configured with `signature_assignment_lookup_keys` set to the eligible-cancer-type lookup keys from Task 1, and `keep_matrix_output` set to `results/q008-quantitative-pass-2026-04-28/sbs96/`.
- [ ] **Step 4: Outputs.** `studies/{tcga_mc3,msk_impact_2017}/mut/signatures/restricted_assignment_per_sample.feather` and the persisted SBS96 matrices.
- [ ] **Step 5: Tests.** Pure-function regression on the new `--keep-matrix-output` and `--matrix-input` paths. The existing assignment behaviour must remain bit-identical when neither flag is set.

---

## Task 3 — Background-subtraction transform on the SBS96 matrix

**Files:**
- New: `code/scripts/subtract_normal_background.py`
- New: `code/scripts/tests/test_subtract_normal_background.py`
- Output: `results/q008-quantitative-pass-2026-04-28/sbs96-subtracted/{c}/{study}__{cancer_type}.SBS96.tsv` plus a per-(sample, c) subtraction-diagnostics manifest.

Per review F6, the Li2021 reference is a WES-derived shape; subtracting it from MSK-IMPACT panel counts is a **shape-only approximation**. We accept this explicitly and report subtraction diagnostics so the downstream interpretation can flag where the approximation breaks.

- [ ] **Step 1: Cancer-type → tissue UBERON mapping.** Build `data/cancer_type_to_normal_tissue_uberon.tsv`, one row per cancer type, with the closest Li2021 organ or `null`. Manual / curated; cite Li2021 organ list. Cancer types with `null` are skipped in the subtraction arm.
- [ ] **Step 2: Reference shape vector.** From `data/normal_tissue_spectra.tsv`, take rows with `aggregation == 'donor_averaged_fraction'` and `value_type == 'fractions'` for each mapped UBERON. Renormalize to sum-1 across the 96 trinucleotide contexts.
- [ ] **Step 3: Per-sample residual-matrix transform.** For each sample with SBS96 count vector `m_i` (sum `n_i`), tissue reference fraction vector `r_t`, and contamination fraction `c`:
  - `m_i'(k) = max(0, m_i(k) − c · n_i · r_t(k))` per context k.
  - Diagnostics recorded per sample: `removed_mass = c · n_i`, `clipped_mass = sum(c · n_i · r_t − m_i)+ ` (mass that could not be removed because the sample had less than the reference assigned to that context), `residual_mass = sum(m_i')`.
  - Drop sample from subtraction arm if `residual_mass < 10`.
- [ ] **Step 4: Sensitivity sweep.** Compute residual matrices for `c ∈ {0.0, 0.05, 0.10, 0.20, 0.30}`. `c = 0.0` is the round-trip control (must equal the raw matrix exactly).
- [ ] **Step 5: Re-assignment.** Re-run Task 2 Step 3 against each `c > 0` matrix using the new `--matrix-input` mode. Cancer-type signature restriction (the existing lookup) is preserved.
- [ ] **Step 6: Exome-flag sensitivity.** Run the re-assignment with `signature_assignment_exome=True` (the t109 default) and `signature_assignment_exome=False`, on c=0.10 only, to measure how much the exome-context normalization affects the verdict. Record both. (This addresses the "Li2021 WES vs panel territory" caveat in the F6 review point.)
- [ ] **Step 7: Tests.**
  - Round-trip: c=0 residual matrix == raw matrix exactly (per-cell).
  - Mass-conservation diagnostic: `removed_mass + residual_mass + clipped_mass = n_i` (per sample, within float tolerance).
  - Synthetic spike test: a sample synthesized as `m_i = n_i · r_t` with c=1 yields residual_mass = 0.

---

## Task 4 — Statistical comparison with sensitivity controls

**Files:**
- New: `code/scripts/compare_q008_matched_vs_unmatched.py`
- New: `code/scripts/tests/test_compare_q008_matched_vs_unmatched.py`
- Output: `results/q008-quantitative-pass-2026-04-28/comparison/q008_quantitative_pilot.feather` and `..._sensitivity.feather`.

- [ ] **Step 1: Per-sample SBS1+SBS5 fraction.** Compute from the raw and the c-swept assignment outputs. For SBS40 (split a/b/c per `SPLIT_SIGNATURE_ALIASES`), do **not** include in SBS1+SBS5; report SBS40-total separately for context.
- [ ] **Step 2: Primary comparison.** For each `raw_eligible` cancer type, Mann–Whitney U on per-sample SBS1+SBS5 fraction (matched vs unmatched, raw c=0), BH-FDR across cancer types. Bootstrap 1000 (seed 0) for the cohort-mean Δ CI.
- [ ] **Step 3: Subtraction comparison.** For each `li2021_eligible` cancer type and each c, recompute Δ. Report the Δ(c) curve and the `c_star` at which Δ first ≤ 50 % of Δ(0).
- [ ] **Step 4: Collateral signature panel.** For SBS2, SBS13 (APOBEC), SBS3 (HRD), SBS10a, SBS10b (POLE), report mean exposure-fraction change vs raw at c\*. The subtraction "rescue" verdict requires **all** four ≤ 10 %.
- [ ] **Step 5: Sensitivity panels.**
  - **Stage strat** (per review F3): if `samples_annotated.feather` carries a primary/metastatic flag (or stage), recompute Δ within each stratum. If stratification is impossible, report the cohort-stage composition and flag this as an unresolved confounder in the verdict.
  - **Hypermutator-included sensitivity:** recompute Δ with hypermutators retained; large change ⇒ exclusion was load-bearing.
  - **Cohort age sensitivity:** if `samples_annotated.feather` carries patient age, regress per-sample SBS1 fraction on age within each arm and report the residual matched-vs-unmatched gap. SBS1 is clock-like; age-uncorrected Δ is biased.
  - **Negative-control signatures:** SBS9 (lymphoid) and SBS31 (platinum) should show **no** matched-vs-unmatched gap in non-applicable cancer types. If they do, the comparison is picking up assay artifact rather than contamination biology.
- [ ] **Step 6: Output.** Two feathers — primary (Δ + CI + p + q + c\*) and sensitivity (one row per panel). Preserve the eligible-cancer-type list from Task 1.
- [ ] **Step 7: Tests.** Synthetic cohort: inject a known SBS1 excess into the unmatched arm, verify Δ recovery within bootstrap CI; round-trip on a zero-effect synthetic cohort (Δ should be ≈ 0).

---

## Task 5 — Interpretation + verdict

**Files:**
- New: `doc/interpretations/2026-MM-DD-t127-q008-quantitative-pilot.md`
- New: `code/notebooks/2026-MM-DD-q008-quantitative-pilot.py` (marimo)

- [ ] **Step 1: Marimo notebook.** Altair plots: (a) feasibility table; (b) per-cancer-type Δ with CI bars (raw); (c) Δ(c) curves for li2021-eligible types; (d) subtraction diagnostics (removed/clipped/residual mass per cancer type); (e) collateral signature panel; (f) sensitivity panels.
- [ ] **Step 2: Interpretation doc.** Frontmatter follows project convention (`type: interpretation`, related to `task:t127`, `question:0008`, `hypothesis:0001-non-tumor-signal-contamination`). Verdict structure:
  - **Headline verdict:** "pilot evidence consistent / inconsistent with contamination" (not causal). Cite the matched-vs-unmatched Δ and the named confounders that remain unresolved.
  - **Subtraction verdict:** rescues / partial / fails-or-overcorrects, gated on `c_star` AND collateral-signature thresholds. If panel sparsity makes the residual matrix structurally noisy (per t126), report this as the dominant uncertainty.
  - **Confounder ledger:** one paragraph per named confounder (assay, caller, stage, age, exposure mix), what the sensitivity panel showed, what's unresolved.
  - **Population-denominator caveat:** "≥ half of cancer types" framing is used **only if** ≥ 6 raw-eligible cancer types pass; below that, individual cancer-type Δs are reported descriptively without aggregation.
- [ ] **Step 3: Update topic + question state.** If verdict is substantive: file follow-ups for (a) within-cohort matched-vs-unmatched comparator (e.g., stratify a single study with both arms, if any exists), (b) tumor-purity covariate (Strategy 4), (c) per-study `unmatched_normal_risk` annotation analogous to `ch_priority_gene`. If null: update q008 with the negative descriptive result and deprioritize Strategies 2–5 in the topic note.

---

## Compute budget

- Task 1 (feasibility table): minutes.
- Task 2 (re-running existing per-sample rule, two studies, eligible cancer types): the existing rule is per-study + per-cancer-type and embarrassingly parallel. Realistic wall clock 1–3 hours.
- Task 3 (subtraction transform + re-assignment, 5 c values, optional exome-flag sensitivity at c=0.10): the transform itself is fast; re-assignment dominates. ≈ 5 × the Task 2 cost in the worst case, mitigated by running c ∈ {0, 0.10, 0.20} first and infilling only if warranted. Realistic 4–10 hours.
- Tasks 4–5: < 1 hour.

Single dedicated session, with a feasibility-table checkpoint after Task 1 that may halt the run early if the no-go rule fires.

---

## Out-of-scope (deferred)

- Tumor-purity covariate (Strategy 4) — needs ABSOLUTE/PureCN ingestion.
- WGS-based LRR/ERR topographic test for q009 — `defer` per `interpretation:0007-t126-sbs1-lrr-bias-per-study`; gated on a WGS cohort (Hartwig HMF).
- MuSiCal / SigFormer cross-tool comparison.
- Extending to all cBioPortal unmatched studies — gated on this pilot.
- CUPLR-style q010 classifier — separate plan.
- Within-cohort matched-vs-unmatched comparator — strongest causal-attribution design, but no candidate cohort identified yet.

---

## Reproducibility covenant

- `random_seed = 0` for SigProfilerAssignment, the bootstrap, and any sub-sampling.
- All thresholds and no-go rules in this file before any decomposition runs.
- All intermediate outputs under `results/q008-quantitative-pass-2026-04-28/`. Per-step manifest at `results/q008-quantitative-pass-2026-04-28/manifest.feather`.
- The SigProfiler reference cache version is whatever the existing t109/t110 surface uses (`signature_assignment_cosmic_version` config, default `"3.5"` per `code/scripts/run_restricted_sigprofiler_assignment.py:463`). No version downgrade.
- Per-study assembly read from study metadata (Task 0 Step 3). No hard-coded build.
