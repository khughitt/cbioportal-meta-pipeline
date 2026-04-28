# t127 — q008 quantitative pass: unmatched-normal SBS1/SBS5 contamination magnitude — Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development. Steps use `- [ ]` checkbox syntax.

**Goal:** Produce the first numeric estimate of the SBS1/SBS5 contamination magnitude attributable to unmatched-normal sequencing in cBioPortal-style cohorts, using SigProfilerAssignment over a matched-vs-unmatched study pair and the Li2021 reference spectra landed by t111. Closes the "built-but-unexploited" gap from `meta:next-steps-2026-04-24` and gives `question:q008` a quantitative anchor.

**Hypothesis under test (q008 quantitative):** In matched-cancer-type cohorts, unmatched-normal samples carry a higher fraction of SBS1+SBS5 mutations than matched-normal samples, and the excess is attenuated when the per-tissue Li2021 normal-tissue spectrum is subtracted as a fixed offset prior to decomposition.

**Pre-registered thresholds (declared before running decomposition):**

- **Effect threshold:** ≥ 5 percentage-point excess in mean SBS1+SBS5 exposure fraction in unmatched vs matched cohort, at the cancer-type level — substantive (consistent with the 8% CH-style false-positive rate). Below 2 pp — null.
- **Subtraction threshold:** the per-tissue background-subtraction step (Strategy 2 in `topic:signature-decomposition-unmatched-normal`) "works" if it reduces the unmatched-vs-matched SBS1+SBS5 gap by ≥ 50% without inflating cancer-type-specific signature exposures (SBS2/SBS13/SBS3/SBS10 etc.) by more than 10%.
- **Test:** two-sided Mann–Whitney on per-sample SBS1+SBS5 fraction, FDR-corrected across cancer types; supplemented with bootstrap CIs on the cohort-mean gap.

**Scope:** SBS only. Single matched-vs-unmatched study pair. Two-stage analysis (raw decomposition; with background subtraction). No de-novo NMF; no purity covariate (filed as follow-up).

**Tech stack:** Python 3.13+, SigProfilerAssignment, SigProfilerMatrixGenerator, pandas, pyarrow, polars, click, pytest. Output as feather + a marimo summary notebook.

**Related:** `task:t127`, `task:t111`, `question:q008-signature-decomposition-tissue-background-subtraction`, `question:q009-sbs1-lrr-bias-as-normal-contamination-flag`, `topic:signature-decomposition-unmatched-normal`, `paper:Li2021`, `paper:DiazGay2023`.

---

## Cohort selection

| Role | Study | Sequencing | Normal | Rationale |
|---|---|---|---|---|
| Matched-normal anchor | `tcga_mc3` (already configured per AGENTS.md) | WES, MC3 7-caller consensus | matched (by design) | 9,104 samples × 32 cancer types; cleanest possible matched-normal baseline |
| Unmatched-normal probe | `msk_impact_2017` | MSK-IMPACT panel (~410-468 genes depending on version) | unmatched / PoN | Largest unmatched-normal panel cohort already in the pipeline; stage-aligned to TCGA cancer types |

**Cancer-type intersection.** Restrict the analysis to cancer types with ≥ 50 samples in BOTH cohorts. Likely candidates from prior pipeline runs: Breast, Colorectal, Lung Adenocarcinoma, Lung Squamous, Endometrial, Bladder, Pancreatic, Glioma, Melanoma, Ovarian. Final list determined in Task 1.

**Caveat (pre-registered):** `msk_impact_2017` is panel-sequenced (~1.2 Mb callable) while `tcga_mc3` is WES (~30 Mb). Per-sample mutation counts will be ~25× lower in the panel arm. SigProfilerSingleSample (per Jin2024 benchmarking) outperforms MuSiCal at panel mutation counts; we use SigProfilerAssignment which has SingleSample mode. The signal we test (SBS1+SBS5 *fraction*, not absolute count) is robust to total-count differences but loses statistical power below ~20 SBS calls per sample. Samples with < 20 callable SBS calls are dropped at Task 2 and the dropped fraction is reported.

---

## Task 0 — Pre-flight gate

Before any code is written.

- [ ] **Step 1: SigProfilerAssignment dependency resolution.** Confirm `SigProfilerAssignment` and `SigProfilerMatrixGenerator` are addable via `uv add`. Verify GRCh37 and GRCh38 reference installation hooks (the matrix generator downloads ~3 GB of trinucleotide context tables on first run; we cache to `data/sigprofiler-cache/`, gitignored).
- [ ] **Step 2: Cohort feasibility check.** Read `studies/tcga_mc3/mut/table/gene_cancer_study.feather` and `studies/msk_impact_2017/mut/table/gene_cancer_study.feather` (or upstream per-sample MAFs); confirm per-sample SBS-call counts and the cancer-type intersection ≥ 5 cancer types meeting the n=50/n=50 floor. If not, halt and re-scope.
- [ ] **Step 3: Genome-build alignment.** MC3 is GRCh37; MSK-IMPACT public is GRCh38. Decide: either (a) lift one to a single build before context counting or (b) run two SigProfiler matrix-generation jobs and join in signature space (signature definitions are build-agnostic). Default: (b) — cheaper and less error-prone. Document choice in the design doc.
- [ ] **Step 4: Document the threshold pre-registration in this plan file** (already declared above) and commit the plan before any data is touched. Reproducibility covenant.

---

## Task 1 — Per-sample SBS96 matrix construction

**Files:**
- New: `code/scripts/build_sample_sbs96_matrix.py`
- New: `code/scripts/tests/test_build_sample_sbs96_matrix.py`

- [ ] **Step 1: Per-study MAF → SigProfilerMatrixGenerator input.** From the per-study MAF (or per-study `gene_cancer_study.feather` upstream, whichever carries chrom/pos/ref/alt + sample_id), emit a `simple_format.txt` per cancer-type cohort in each study, suitable as SPMG input. Drop indels (we are SBS-only); drop variants with N alleles.
- [ ] **Step 2: Matrix generation.** Run SigProfilerMatrixGenerator with `exome=True` for both studies (panel coverage approximated as exome for the trinucleotide normalization step is acceptable per Diaz-Gay2023 supplementary — confirmed before run; if not, use `exome=False` with raw counts and document).
- [ ] **Step 3: Output.** Write `/data/packages/cbioportal/q008-validation/sbs96/{study}/{cancer_type}.SBS96.tsv` plus a manifest at `/data/packages/cbioportal/q008-validation/sbs96/manifest.feather` listing (study, cancer_type, sample_id, callable_mb, n_sbs_called).
- [ ] **Step 4: Tests.** Pure-function tests on the MAF→simple_format conversion; one slow-marked end-to-end test on a 5-sample fixture.

---

## Task 2 — Per-sample SigProfilerAssignment with cancer-type-restricted catalogue

**Files:**
- New: `code/scripts/decompose_sbs96.py`
- New: `code/scripts/tests/test_decompose_sbs96.py`

- [ ] **Step 1: Cancer-type → allowed SBS list.** Build `data/cosmic_v3p3_per_cancer_signature_exclusions.tsv` from COSMIC Extended Data Figure 5 / Alexandrov2020 supplement (Intervention 1 in the topic note). One row per cancer-type, columns `cancer_type, allowed_sbs (semicolon-list)`. Manual / one-time extraction.
- [ ] **Step 2: Per-sample assignment.** Run `Analyzer.decompose_fit` with `signature_database='COSMIC_v3.3_SBS_GRCh37'` (or build-matched), `exclude_signature_subgroups` populated from the cancer-type list, `nnls_add_penalty=0.05` (default), `cosmic_version=3.3`, `make_plots=False`, `seed=0`. Output is per-sample SBS96 → COSMIC exposures.
- [ ] **Step 3: Quality gate.** Drop samples with < 20 SBS calls; record drop count per (study, cancer_type) in a side feather. Exposures are normalized to fractions per sample (sum to 1).
- [ ] **Step 4: Output.** `/data/packages/cbioportal/q008-validation/exposures/{study}_{cancer_type}_raw.feather` with columns `sample_id, study, cancer_type, n_sbs, sbs01, sbs02, …, sbs95, sbs1_5_fraction`.
- [ ] **Step 5: Tests.** Pure-function test on the cancer-type→allowed-list lookup; integration test on a deterministic fixture cohort with known signature ground truth.

---

## Task 3 — Background-subtraction variant (Strategy 2)

**Files:**
- New: `code/scripts/subtract_normal_background.py`
- New: `code/scripts/tests/test_subtract_normal_background.py`

- [ ] **Step 1: Cancer-type → tissue UBERON mapping.** Build `data/cancer_type_to_normal_tissue.tsv` mapping each cancer type to its closest Li2021 tissue UBERON (e.g., LUAD → UBERON:0002185 bronchia; COAD → UBERON:0001155 colon; ESCA → UBERON:0001043 esophagus). Manual / curated. Document non-matches (e.g., breast, glioma have no Li2021 reference; those cancer types are dropped from the subtraction arm).
- [ ] **Step 2: Reference spectrum extraction.** From `data/normal_tissue_spectra.tsv` (t111 output), extract the `donor_averaged_fraction` row for each mapped tissue. Renormalize to a probability vector over 96 trinucleotide contexts.
- [ ] **Step 3: Per-sample subtraction.** For sample with mutation count vector `m_i` (length 96, sum = `n_i`) and tissue reference fraction vector `r_t`:
  - Choose contamination fraction `c` (hyperparameter). Default 0.10. Sensitivity panel at c ∈ {0.0, 0.05, 0.10, 0.20, 0.30}.
  - Subtract: `m_i' = max(0, m_i − c · n_i · r_t)` element-wise.
  - Discard samples where post-subtraction `sum(m_i') < 10` (insufficient residual signal).
- [ ] **Step 4: Re-decomposition.** Re-run Task 2 Step 2 on the subtracted matrices; output `_subtracted_c{cc}.feather` per c value.
- [ ] **Step 5: Tests.** Conservation test: decomposing a pure-tissue spectrum should yield (after subtraction at c=1.0) a near-zero residual that does not assign meaningful exposure to any cancer-type signature. Round-trip test: subtraction at c=0 must equal raw decomposition exactly.

---

## Task 4 — Statistical comparison

**Files:**
- New: `code/scripts/compare_matched_vs_unmatched_sbs.py`
- New: `code/scripts/tests/test_compare_matched_vs_unmatched_sbs.py`

- [ ] **Step 1: Effect-size estimation.** For each cancer type with ≥ 50 samples in both arms, compute `Δ = mean(SBS1+SBS5 fraction | unmatched) − mean(SBS1+SBS5 fraction | matched)`. Bootstrap 1000 iterations for 95 % CI on Δ. Same for individual SBS1, SBS5, and SBS18 fractions.
- [ ] **Step 2: Hypothesis test.** Two-sided Mann–Whitney U on per-sample SBS1+SBS5 fraction, BH-FDR across cancer types. Pre-registered α = 0.05.
- [ ] **Step 3: Subtraction-effect estimation.** For each cancer type and each `c ∈ {0, 0.05, 0.10, 0.20, 0.30}`, recompute Δ. Report Δ(c) curve; cite the c* value at which Δ first crosses below 50 % of Δ(0).
- [ ] **Step 4: Cancer-signature collateral check.** For SBS2, SBS13 (APOBEC), SBS3 (HRD), SBS10a/b (POLE) — confirm post-subtraction exposures change by ≤ 10 % vs raw. If they don't, the subtraction is over-correcting and the c* gate above is unsafe.
- [ ] **Step 5: Output.** `/data/packages/cbioportal/q008-validation/comparison/q008_quantitative_pass.feather` with columns `cancer_type, n_matched, n_unmatched, delta_sbs1_5, delta_ci_low, delta_ci_high, mannwhitney_p, fdr_q, c_star, delta_post_subtraction, collateral_max_pct_change`.
- [ ] **Step 6: Tests.** Synthetic cohort test: inject known SBS1 excess into unmatched arm, verify recovery within bootstrap CI.

---

## Task 5 — Interpretation + verdict

**Files:**
- New: `doc/interpretations/2026-MM-DD-t127-q008-quantitative-pass.md`
- New: `code/notebooks/2026-MM-DD-q008-quantitative-pass.py` (marimo)

- [ ] **Step 1: Marimo summary notebook.** Altair plots: (a) per-cancer-type Δ with CI bars; (b) Δ(c) curves; (c) per-cancer-type SBS1+SBS5 fraction histograms (matched vs unmatched, raw vs subtracted); (d) collateral signature panel.
- [ ] **Step 2: Interpretation doc.** Use the project's interpretation frontmatter convention. Verdict against the pre-registered thresholds. Verdict categories: **substantive contamination** (Δ ≥ 5 pp in ≥ half of cancer types), **mild** (2–5 pp), **null** (< 2 pp). Subtraction verdict: **rescues** (Δ(c\*) reduction ≥ 50 % with collateral ≤ 10 %), **partial**, **fails / over-corrects**. Cite the topic note plus q008 / q009 questions.
- [ ] **Step 3: Update topic + question state.** If verdict is substantive: file follow-up tasks for (a) scaling Strategy 2 to all cBioPortal unmatched studies, (b) tumor-purity covariate integration (Strategy 4), (c) per-study annotation flag analogous to `ch_priority_gene`. If verdict is null: update q008 with the negative result; deprioritize Strategies 2–5 in the topic note.

---

## Compute budget

- Task 1 SPMG run: ~30–60 min on the MC3 + MSK-IMPACT pair.
- Task 2 SigProfilerAssignment over ~10 cancer-type cohorts × 2 studies: ~2–4 hours per cancer type at ~1k samples; ~20–40 hours total. Embarrassingly parallel; use `parallel::mclapply`-equivalent (`joblib.Parallel`) or per-cancer-type Snakemake rules. Realistic wall clock: 4–8 hours with parallelism.
- Task 3 subtraction + re-decomposition × 5 c-values: another 4–8 hours. Mitigation: run only c ∈ {0.0, 0.10, 0.20} initially, fill in the curve only if the headline signal warrants it.
- Tasks 4–5: < 1 hour.

Total: one dedicated session, ideally on the workstation with the SigProfiler cache pre-warmed.

---

## Out-of-scope (deferred)

- Tumor-purity covariate (Strategy 4) — needs ABSOLUTE/PureCN per-sample purity ingestion (separate task).
- WGS-based LRR/ERR topographic test for q009 — not applicable to MC3 / MSK-IMPACT (both are exome/panel).
- MuSiCal / SigFormer cross-tool comparison.
- Extending to all cBioPortal unmatched studies — gated on the pilot result here.
- CUPLR-style classifier (q010) — separate plan.

---

## Reproducibility covenant

- `random_seed = 0` for SigProfilerAssignment and the bootstrap.
- All thresholds declared in this file before any decomposition is run; commit this plan before Task 0 Step 2.
- All intermediate outputs written under `/data/packages/cbioportal/q008-validation/` with per-step manifests.
- The SigProfiler reference cache (`data/sigprofiler-cache/`) is gitignored but its version is pinned in `pyproject.toml` via the `SigProfilerAssignment` entry.
