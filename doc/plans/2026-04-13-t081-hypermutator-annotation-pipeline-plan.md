---
id: "plan:2026-04-13-t081-hypermutator-annotation-pipeline-plan"
type: "plan"
title: "Hypermutator / TMB annotation pipeline plan"
status: "active"
created: "2026-04-13"
updated: "2026-04-13"
---

# Hypermutator / TMB annotation pipeline plan (t081)

> **For Claude:** REQUIRED SUB-SKILL: use `superpowers:executing-plans` to implement this plan task-by-task. Do **not** start Task 1 before `t079` (pre-register pooling method) has resolved whether this annotation affects pre-registered decisions.

**Goal:** Add data-driven, multi-source, continuous hypermutation annotation to every sample in every study, exposing both continuous diagnostic columns and a derived boolean flag. Provide a config-controlled hypermutator-exclusion hook for cross-study aggregation, preserving auditability of included-vs-excluded comparisons.

**Architecture** (paths are the ACTUAL Snakefile `out_dir/` layout, verified against `code/workflows/Snakefile`):

```
data_clinical_sample.txt  ─┐
  (per study, raw)          │
                            ├─> convert_to_feather.py ──> out_dir/studies/{id}/metadata/samples.feather
data_mutations.txt ─────────┘                              (adds msi_type, msi_score cols;
  (per study, raw)                                          ADDS study_id col — F3 fix)
                                                                   │
                                                                   ▼
out_dir/metadata/genie_panel_coverage.feather ─┐   ┌──> out_dir/studies/{id}/metadata/samples_tmb.feather
                                               │   │  (per-sample: mutation_count, tmb, tmb_log10,
  study_panel_map (config) ────────────────────┼─> │   pole_hotspot_detected, pold1_hotspot_detected,
                                               │   │   msi_type, study_id, sample_id)
  published panel sizes (config) ──────────────┘   │
                   │                               │
                   ▼                               │
  out_dir/metadata/panel_callable_mb.tsv           │
  (generated artifact, NOT version-controlled)     │
                                                   ▼
                                    out_dir/metadata/samples_tmb_combined.feather
                                    (concat across studies; study_id-prefixed keys)
                                                   │
                                                   ▼
                                    out_dir/metadata/per_cancer_gmm_fits.feather
                                    out_dir/metadata/samples_annotated.feather
                                    (+ tmb_zscore_within_cancer, is_hypermutator_gmm,
                                       hypermutation_score, is_hypermutator,
                                       hypermutator_reason)
                                                   │
                                                   ▼
                          (per-study create_freq_tables.py consumes samples_annotated
                           to emit BOTH inclusive + exclusive per-study num/ratio cols
                           — F1 fix: filter lives at per-study layer)
                                                   │
                                                   ▼
                          out_dir/studies/{id}/mut/table/{entity}_study{,_ratio}.feather
                          with _inclusive / _exclusive column pairs
                                                   │
                                                   ▼
                          out_dir/summary/mut/table/{entity}_study{,_ratio}.feather
                          (combined script concatenates both columns — no ratio
                           recomputation needed)
```

**Note on dataflow correction (F1):** the pipeline's ratio computation happens **per-study** in
`create_freq_tables.py:36–46`, where `groupby('cancer_type').sample_id.nunique() / num_samples` has
access to sample-level `sample_id`. The combined script (`create_combined_gene_cancer_freq_table.py`)
pivots already-computed per-study ratios into a wide table and takes their mean — it has no sample-
level data and cannot recompute exclusive ratios. So the hypermutator-exclusion filter MUST live in
`create_freq_tables.py` (or a new per-study rule that runs before it), not in the combined scripts.

**New dependencies:**
- **Runtime** (added to `[project.dependencies]` in `pyproject.toml`): `diptest>=0.9` (Hartigan's dip test of unimodality — small, C-backed, one function; used by Task 5).
- **Dev** (added to `[project.optional-dependencies].dev` or equivalent in `pyproject.toml`): `pytest>=8.0` (new — project doesn't currently declare a test framework).

`sklearn.mixture.GaussianMixture` is already present via scikit-learn. No other new libraries.

**Task IDs in the backlog:** this plan implements **t081 (P1)**. It creates the machinery that **t077 (GLMM-logit pooling, P1)** will later consume as a sample-level covariate OR as an inclusion gate. It intersects with **t083 (cancer-type canonicalization, P2)** — the per-cancer-type GMM fit quality depends on clean labels; do t083 first if scheduling allows, otherwise document the dependency.

---

## Assumptions & limitations (read before implementing)

These are cited in the audit `doc/meta/bias-audit-cross-study-aggregation-pipeline.md` and in the topic note `doc/background/topics/tumor-mutational-burden.md`. Any of them being wrong changes the design.

1. **cBioPortal MAFs are complete within their called set** — all somatic mutations called by the study's pipeline are present. We do *not* model upstream caller differences (MuTect2 vs Strelka vs Varscan etc.). Impact: a study that uses a stricter caller will appear lower-TMB than one with a permissive caller, even for the same sample. Partly mitigated by per-cancer-type z-score (within-cancer-type comparisons are cancer-dominant, not caller-dominant) but **flagged as residual bias**.
2. **Panel callable-Mb is approximated as "sum of exonic bases in the panel BED"** — we do *not* use per-sample coverage metrics (most studies don't publish them). This means a sample with 20% of panel regions below coverage threshold still has its TMB computed against the nominal panel size. Bias direction: TMB of low-coverage samples is *underestimated*.
3. **Variant-class filter for the TMB numerator** — we count only protein-altering variants (`Missense_Mutation`, `Nonsense_Mutation`, `Frame_Shift_Del/Ins`, `In_Frame_Del/Ins`, `Splice_Site`, `Translation_Start_Site`, `Nonstop_Mutation`). We exclude `Silent`, `Intron`, `3'UTR`, `5'UTR`, `RNA`, `IGR`. This matches Chalmers 2017 F1CDx / FMI TMB convention. A pan-cancer "nonsynonymous" mutational burden is the comparable unit across WES and panel.
4. **POLE / POLD1 hotspot list is literature-curated, not exhaustive** — we use the canonical 8-site POLE list (P286R, V411L, S297F, S459F, A456P, L424V, M295V, F367L) and 6-site POLD1 list (P327L, R689W, S478N, L474P, D316H, D316N) from Campbell 2017, Rayner 2016, Ma 2018. Rare hotspots are missed. Low-impact error — covered in bulk by the tmb_zscore signal.
5. **MSI status availability is study-dependent** — only a subset of cBioPortal studies publish `MSI_TYPE` / `MSI_STATUS` / `MSI_SCORE`. Where present, calling methods vary (MSIsensor, MANTIS, PCR-based pentaplex, immunohistochemistry of MMR proteins). We treat MSI-H as a strong signal but do not assume MSS means not-hypermutated; MSS samples can still be ultra-hypermutated via POLE.
6. **GMM bimodality assumption** — per-cancer-type log10(TMB) is approximately bimodal when hypermutators exist (Campbell 2017 demonstrated for CRC, UCEC, SKCM). For cancers with no hypermutators (most sarcomas, many pediatric tumors) the GMM will either fit a single-component solution or produce spurious bimodality. We guard against both with a Hartigan's dip test + minimum-sample-size threshold.
7. **Raw mutation count conflates drivers and passengers** — hypermutators have more of both. When we later use `is_hypermutator` to exclude samples from per-gene aggregation, we are *under-counting* driver events in MSI-CRC, POLE-UCEC, UV-SKCM cancers. That is the whole point (those drivers are swamped by passengers otherwise), but the exclusion has interpretive cost: pooled driver rates for those cancers should be understood as "among non-hypermutators of this cancer type". Document in every output.

---

## Things to control for (downstream interpretation)

These belong in the output docstring of every consumer of `is_hypermutator`, and in the pre-registration (t079). Listed here so the plan reviewer doesn't have to reconstruct them.

- **Exclusion-rate sanity check per cancer type** — publish per-cancer-type exclusion rates alongside any hypermutator-excluded output. Target ranges from Zehir 2017 / Chalmers 2017: MSK-IMPACT 10k overall ≈ 3–5%, UCEC ≈ 20–25%, CRC ≈ 10–15%, SKCM ≈ 5–10%, pediatric tumors ≈ 0%.
- **Per-study panel-composition bias** — WES studies will have more variance in raw counts than panel studies for the same underlying TMB, because panels sample only ~1–2 Mb. Use `tmb` (normalized), never raw `mutation_count`, for cross-study comparisons.
- **Bimodality fit diagnostics** — for each per-cancer-type GMM, export `bic_1_component`, `bic_2_component`, `hartigans_dip_pvalue`, `n_samples`, `fit_quality`. Consumers can gate on `fit_quality` before trusting `is_hypermutator_gmm`.
- **Sample-level vs patient-level filtering semantics** — `is_hypermutator` is sample-level. If a patient has a hypermutator sample and a non-hypermutator sample, the patient still contributes to non-hypermutator aggregates via the non-hypermutator sample. Document.
- **The flag is not stable under cohort changes** — `is_hypermutator_gmm` depends on the per-cancer-type distribution which depends on study composition. Re-running with different studies can flip borderline samples. Pin the study list for any published analysis.
- **Interaction with CH annotation** — CH-priority-gene mutations in tumor-only panel studies may drive up `mutation_count` without representing true tumor-intrinsic hypermutation. For CH-priority genes in non-matched-normal studies, consider computing TMB both with and without CH-priority-gene mutations, so hypermutator flagging isn't CH-contaminated.

---

## QA / validation criteria (applied to every task below)

Three levels of validation, applied throughout:

**Unit level (per-task, deterministic):**
- Synthetic data with known TMB / hotspot presence → expected columns / flags.
- Edge cases: sample with 0 mutations, sample with 10,000 mutations, sample with POLE hotspot but low TMB, sample with high TMB but no POLE/MSI signal.

**Integration level (real data, known ground truth):**

Integration tests require at least one study with a documented hypermutator rate in the active
config. The current `config-10k-genes.yml` contains **no TCGA cohorts** (only 7 pan-cancer /
metastatic / pediatric studies), so straight TCGA-per-cancer-type validation is unrunnable as
originally specified. **Resolution (review finding #2):** use `tcga_mc3` as the single TCGA
surrogate (already documented in `AGENTS.md` "Alternate data sources" — it bundles 32 TCGA
cancer types, 9,104 samples, in one pseudo-study). Add `tcga_mc3` to the studies list for
validation runs only; it does NOT need to be in the main analysis config.

- **`tcga_mc3` with `cancer_type == "UCEC"` subset:** ~25% hypermutator expected (Cancer Genome
  Atlas 2013 TCGA-UCEC analysis; POLE-ultramutated subset ~7%).
- **`tcga_mc3` with `cancer_type == "COAD"` or `"READ"`:** MSI-H rate ~15%; hypermutator rate
  matches (Kandoth 2013, Ellrott 2018).
- **`tcga_mc3` with `cancer_type == "SKCM"`:** UV-hypermutator tail ~5% (Hayward 2017).
- **`msk_impact_2017`** (if added to the validation config): overall hypermutator rate ~3–5%
  (Zehir 2017); CRC-hypermutator ~10–15%.
- **Acceptance:** flagged rate within ±20% relative of the literature rate per cancer type with
  ≥ 50 samples.

**If `tcga_mc3` is not in the active study list:** integration tests are skipped with a clear
warning log; unit tests must still pass. Validation runs require explicitly appending
`tcga_mc3` to the config. This is documented in the Task 5 / 7 validation sections and in the
implementer's README.

**Cross-source agreement (sanity):**
- All samples with POLE hotspot should have `tmb_zscore_within_cancer > 1.5` (POLE causes ultra-hypermutation). Flag any violations as QA failures.
- All samples with `MSI_TYPE == "MSI-H"` should have `tmb_zscore_within_cancer > 0.5` in CRC / UCEC / STAD. Flag violations.
- Ultra-hypermutators (POLE) should have higher TMB than hypermutators (MSI) within the same cancer type when both are present.

**Diagnostic outputs:**
- Per-cancer-type TMB distribution plots with GMM fit overlay (seaborn/altair).
- Flagged-vs-unflagged TMB scatter colored by POLE/MSI status.
- Cross-study TMB boxplots per cancer type to visualize panel-composition bias.

---

## Changes to existing code (from current working pipeline)

| File | Change | Task |
|---|---|---|
| `code/scripts/convert_to_feather.py` | (a) Ingest `MSI_TYPE` / `MSI_STATUS` / `MSI_SCORE` from `data_clinical_sample.txt` when present; write `msi_type` (normalized categorical) + `msi_score` (float) into `samples.feather`. Zero-impact when columns absent. (b) **Add `study_id` column** to `samples.feather` (currently absent — F3 fix). | Tasks 2, 4 |
| `code/scripts/convert_to_feather.py` | Retain `variant_class` and `hgvsp_short` (already done — verified at `convert_to_feather.py:95,104`). No change. | — |
| `code/config/config-10k-genes.yml` | Add top-level `hypermutator:` block with `gmm_min_samples: 100`, `gmm_min_delta_bic: 10`, `gmm_min_dip_pvalue: 0.1`, `zscore_fallback_threshold: 1.5`, `score_threshold: 0.5`, `exclude_from_aggregation: false` (default False — flips to True only if t079 pre-registration decides so). Also `wes_default_callable_mb: 30`. **GMM random seed reuses the existing top-level `random_seed` config key** (already used by `cluster_genes.py` / `cluster_cancer_types.py`); no new seed key needed. | Task 1 |
| `code/config/config-10k-genes.yml` | Add `panel_callable_mb_override:` map for published panel sizes (MSK-IMPACT-341: 1.014 Mb, IMPACT-410: 1.162 Mb, IMPACT-468: 1.446 Mb — Cheng 2015, Zehir 2017, Bandlamudi 2026). | Task 1 |
| `code/workflows/Snakefile` | New rules: `build_panel_callable_sizes`, `compute_per_sample_tmb`, `detect_polymerase_hotspots`, `combine_samples_tmb`, `fit_per_cancer_tmb_gmm`, `annotate_hypermutators`. See Snakemake-specific appendix for exact targets. | Tasks 1–6 |
| `code/scripts/create_freq_tables.py` | **Major change (F1 fix):** accept optional `samples_annotated.feather` input; when present, emit per-entity tables with paired `num_inclusive` / `num_exclusive` / `ratio_inclusive` / `ratio_exclusive` / `n_samples_inclusive` / `n_samples_exclusive` columns. `num` / `ratio` aliases to the inclusive pair are safe here (consumers — `create_combined_freq_tables.py:19`, `create_combined_gene_cancer_freq_table.py:78`, `create_combined_gene_cancer_mutation_matrices.py:22` — all pivot per-study `ratio` values, so aliasing is transparent). | Task 7 |
| `code/scripts/create_combined_sample_table.py` | Add `study_id`, `is_hypermutator`, `hypermutation_score`, `hypermutator_reason`, `tmb`, `tmb_log10`, `tmb_zscore_within_cancer`, `pole_hotspot_detected`, `pold1_hotspot_detected`, `msi_type` columns to combined output. **Canonical join key becomes (`study_id`, `sample_id`)** — documented in the file docstring. | Task 7 |
| `code/scripts/create_combined_gene_cancer_freq_table.py` | Carry the new `num_inclusive` / `num_exclusive` / `ratio_inclusive` / `ratio_exclusive` per-study columns through the pivot; compute `mean_inclusive` / `mean_exclusive`. **Drop the single `mean` column — do NOT alias.** Downstream Rmd consumer (see below) gets updated to select explicitly. Rationale: `summary.Rmd:175` actively displays `mean` in the final report; aliasing to either inclusive or exclusive creates silent semantic drift at the t079 default-flip (review finding #3). Internal sort uses `mean_inclusive` as the stable default. **No per-sample logic in this file** (it has no access to sample IDs). | Task 7 |
| `code/scripts/create_combined_freq_tables.py` | Same change — write `mean_inclusive` / `mean_exclusive`; drop the unqualified `mean`. Sort internally by `mean_inclusive`. Update `mean_adj` computation to use `mean_inclusive` as the numerator (document this choice; consider whether a `mean_adj_exclusive` variant is also needed — add only if the downstream consumer asks). | Task 7 |
| `code/scripts/create_combined_gene_cancer_mutation_matrices.py` | Exclusion list at lines 11 and 20 (currently `['cancer_type', 'symbol', 'mean', 'mean_adj']`) updates to `['cancer_type', 'symbol', 'mean_inclusive', 'mean_exclusive', 'mean_adj_inclusive']` (plus `_exclusive` if added). Functionality unchanged — this consumer only skips these columns when aggregating per-study values. | Task 7 |
| `code/scripts/annotate_ch.py` | Exclusion list at line 58 updates analogously: `"mean"` → `"mean_inclusive", "mean_exclusive"`. | Task 7 |
| `code/scripts/summary.Rmd` | **Consumer update (review finding #3 fix):** the report's gene-ratio table (line 175) currently selects `mean, mean_adj, ratio_nonna, num_nonna, protein_length`. Replace with explicit handling: if `mean_exclusive` is present, display BOTH `mean_inclusive` and `mean_exclusive` side-by-side with a column labelled "hypermutator-excluded"; otherwise fall back to `mean_inclusive`-only. Sorting (line 184) switches from `mean_adj` to `mean_adj_inclusive`. Document in the Rmd header that downstream rankings use inclusive-default until t079 flips the policy. | Task 7 |
| `AGENTS.md` | Add "Hypermutator / TMB annotation" subsection to "Annotations applied in the pipeline". | Task 8 |
| `doc/guides/modalities/cross-study-aggregation.md` | Add new audit checklist item **agg.15** tying `is_hypermutator`-aware ratio pairs to t081. | Task 8 |

---

## Task breakdown

### Task 1: Panel callable-Mb registry (`build_panel_callable_sizes`)

**Inquiry-node equivalent:** input-side normalization. Computes the denominator for TMB.

**Implements:** Assumption 2 (panel-callable-Mb approximation). Produces
`out_dir/metadata/panel_callable_mb.tsv` — a **generated build artifact**, NOT version-controlled
(Open-question-2 resolution). The version-controlled inputs are the config-defined overrides
and the GENIE coverage feather (itself a build product of `process_genie_panel_coverage`).

**TDD steps:**

1. Write `code/scripts/tests/test_build_panel_callable_sizes.py` asserting:
   - Given a GENIE panel BED with 3 exonic records (each 1000 bp), output is 0.003 Mb.
   - Given MSK-IMPACT-468 in the `panel_callable_mb_override` config map, output is 1.446 Mb
     regardless of BED; `source == "config_override"`.
   - Unknown panel ID → `wes_default_callable_mb` from config (30 Mb); `source == "wes_default"`.
   - BED-derived size for MSK-IMPACT-468 should be within ±5% of 1.446 Mb, else warning logged
     and override is used.
2. Write `code/scripts/build_panel_callable_sizes.py`:
   - Input: `out_dir/metadata/genie_panel_coverage.feather` (from existing
     `process_genie_panel_coverage` rule — verify path at `Snakefile:157`), config
     `panel_callable_mb_override` map, config `wes_default_callable_mb`.
   - Sum `end - start` per panel across `Feature_Type == "exon"` records, convert to Mb.
   - Apply override map where present.
   - Emit `out_dir/metadata/panel_callable_mb.tsv` with columns `[panel_id, callable_mb, source]`
     where `source ∈ {"bed_sum", "config_override", "wes_default"}`.
3. Add Snakemake rule `build_panel_callable_sizes` consuming the GENIE coverage feather +
   config, producing `out_dir/metadata/panel_callable_mb.tsv`. **Caching semantics (review
   finding #6):** declare `localrules: build_panel_callable_sizes` in the Snakefile so the
   rule runs locally (not scheduled on a cluster) and its output persists via Snakemake's
   normal file-timestamp / DAG-invalidation logic. That means the tsv is regenerated whenever
   the GENIE coverage feather or the config-derived override map changes — which is exactly the
   desired behavior. No `temp()` wrapping — the file is part of the audit trail.

**Validation criteria:**
- Unit tests pass (see "Test layout" section below for `pytest` invocation).
- MSK-IMPACT panels: bed-derived size within 5% of published.
- Manual inspection: rule output covers every `panel_id` referenced in `study_panel_map`.

**Reusable:** `reusable: true`. The panel-callable registry has value beyond this task — reused by
t070 (panel-version drift), t076 (NaN-vs-0 panel-aware), and eventually t077 (GLMM-logit) as a
study-level covariate. Flag in the rule's output docstring.

---

### Task 2: Per-sample TMB calculation + `study_id` propagation (`compute_per_sample_tmb`)

**Implements:** core continuous-TMB signal (Assumption 3, protein-altering numerator) AND the
F3 fix for `study_id` as a first-class column on every sample-level artifact.

**TDD steps:**

1. Write `code/scripts/tests/test_compute_per_sample_tmb.py` asserting:
   - 100 synthetic samples, each with N mutations in `variant_class` ∈ protein-altering set →
     `mutation_count == N`.
   - Silent / intron / 3'UTR / 5'UTR / RNA / IGR mutations are excluded from the count.
   - `tmb = mutation_count / panel_callable_mb` (exact arithmetic).
   - `tmb_log10 = log10(tmb + 1)` (log-transform for zero-safety).
   - A sample in a study with unknown panel → uses WES default (30 Mb); `tmb_source == "wes_default"`.
   - Output carries `study_id` column (from the `{id}` wildcard) — test asserts every row has it.
2. Write `code/scripts/compute_per_sample_tmb.py`:
   - Input: `out_dir/studies/{id}/mut/mut_filtered.feather` (existing output of `filter_genes`
     rule), `out_dir/studies/{id}/metadata/samples.feather`, `out_dir/metadata/panel_callable_mb.tsv`,
     config `study_panel_map`, wildcard `{id}` for the study.
   - Filter mutations to protein-altering `variant_class` values (constant list in script; see
     Assumption 3).
   - Group by `sample_id_tumor`, count rows → `mutation_count`. Preserve zero-mutation samples via
     a left join back to `samples.feather`.
   - Look up panel via `study_panel_map[id]` → callable Mb from panel table → compute `tmb`,
     `tmb_log10`, `tmb_source`.
   - Write `study_id = {id}` column to every row (F3 fix).
   - Emit **new file** `out_dir/studies/{id}/metadata/samples_tmb.feather` — does NOT overwrite
     `samples.feather` (preserves existing downstream consumers until they opt in to the new
     schema).
3. Snakemake rule `compute_per_sample_tmb` wildcarded on `{id}`; output at
   `out_dir/studies/{id}/metadata/samples_tmb.feather`.

**Validation criteria:**
- Unit tests pass.
- Integration: on `msk_impact_2017`, median `tmb` across the cohort should be ~3–6 mut/Mb
  (Chalmers 2017, Zehir 2017); zero samples with `mutation_count == 0` (MSK-IMPACT requires ≥1
  call to be in the cohort). Assert.
- Spot-check: sample with >5000 mutations in a panel study → log warning (likely CH-contaminated
  tumor-only or corrupted count; not a test failure, but surface for investigation).
- Every row of the output has a non-null `study_id`.

---

### Task 3: POLE / POLD1 hotspot detector (`detect_polymerase_hotspots`)

**Implements:** Assumption 4; independent biological signal for ultra-hypermutation.

**TDD steps:**

1. Write `test_detect_polymerase_hotspots.py` asserting:
   - Sample with `hgvsp_short == "p.P286R"` in POLE gene → `pole_hotspot_detected = True`.
   - Sample with `hgvsp_short == "p.P286L"` (different AA) → `pole_hotspot_detected = False`.
   - Sample with POLE hotspot on a different transcript/protein → False (case-sensitive AA-change match against canonical list).
   - Sample with any mutation in POLE but not a hotspot → False.
2. Constants (in `code/scripts/detect_polymerase_hotspots.py`):
   ```python
   POLE_HOTSPOTS = frozenset(["P286R", "V411L", "S297F", "S459F", "A456P",
                              "L424V", "M295V", "F367L"])
   POLD1_HOTSPOTS = frozenset(["P327L", "R689W", "S478N", "L474P",
                               "D316H", "D316N"])
   ```
   Citations in docstring: Campbell 2017, Rayner 2016, Ma 2018.
3. Script:
   - Input: `mut.feather` (per study).
   - Strip `p.` prefix from `hgvsp_short`; match against hotspot sets gated on `symbol in {"POLE", "POLD1"}`.
   - Group by `sample_id_tumor`: `pole_hotspot_detected = any(...)`, `pold1_hotspot_detected = any(...)`.
   - Output: `sample_polymerase_hotspots.feather` (per study) with `[sample_id_tumor, pole_hotspot_detected, pold1_hotspot_detected]`.
4. Snakemake rule `detect_polymerase_hotspots` per study.

**Validation criteria:**
- Unit tests pass.
- Integration: TCGA-UCEC samples with POLE hotspot should be ~7% of the cohort (Cancer Genome Atlas 2013). Log and assert ≥ 4% and ≤ 12%.
- Sanity: every POLE-hotspot-positive sample should have `tmb_log10 > population_median_tmb_log10 + 1` (ultra-hypermutation). Log violators.

---

### Task 4: MSI status ingestion (`convert_to_feather.py` extension)

**Implements:** Assumption 5; third biological signal when available.

**TDD steps:**

1. Extend `test_convert_to_feather.py`:
   - Given `data_clinical_sample.txt` with `MSI_TYPE` column, `msi_type` appears in `samples.feather` with same values (normalized to `{MSI-H, MSI-L, MSS, Indeterminate, NaN}`).
   - Given a file without MSI columns, `msi_type` column exists but all `NaN`.
   - Alternative column names `MSI_STATUS`, `MSI_SENSOR`, `MSI_SCORE` are also parsed; `MSI_SCORE` (numeric) is kept separately as `msi_score`.
   - Normalization: `"Instable"`, `"MSI"`, `"High"` → `"MSI-H"`; `"Stable"`, `"Microsatellite stable"` → `"MSS"`. Document the mapping table.
2. Modify `code/scripts/convert_to_feather.py`:
   - Attempt to read MSI columns from `data_clinical_sample.txt`; fall back to NaN where absent.
   - Apply normalization map (explicit dict, exported for testability).
3. Sanity at run time: log counts of each `msi_type` value per study; log a warning if all samples are `MSS` in a cancer type where MSI is expected (CRC, UCEC, STAD).

**Validation criteria:**
- Unit tests pass.
- Integration: any study in the current run that has `MSI_TYPE` in its clinical file → non-null proportion > 50% expected; log if below.
- MSK-IMPACT studies should have `msi_sensor_score` or equivalent; note study-by-study availability in an audit-trail output.

---

### Task 5: Per-cancer-type TMB GMM fit (`fit_per_cancer_tmb_gmm`)

**Implements:** data-driven threshold; Assumption 6.

**TDD steps:**

1. Write `test_fit_per_cancer_tmb_gmm.py`:
   - Synthetic: 200 samples from Normal(log10(3), 0.3) + 50 samples from Normal(log10(100), 0.3) → GMM should identify 2 components; upper-component samples should all have `is_hypermutator_gmm = True`.
   - Synthetic: 500 samples from a single Normal → 2-component GMM fit should have high BIC vs 1-component; `fit_quality = "single_mode"` and fall-back to z-score threshold (no hypermutators flagged).
   - Cohort with N < config threshold (e.g., < 100) → `fit_quality = "insufficient_data"`; fallback to `10 × median` rule.
   - Hartigan's dip test p > 0.1 → `fit_quality = "not_bimodal"`; fallback.
2. Write `code/scripts/fit_per_cancer_tmb_gmm.py`:
   - Input: cross-study samples table (output of `combine_samples_tmb`).
   - **Pin `random_state = snek.config["random_seed"]` (reuses existing project-wide seed).** Every call to
     `sklearn.mixture.GaussianMixture(n_components=N, random_state=...)` must pass this seed.
     Rationale in file docstring: "Reproducibility covenant — flags flip on borderline samples if
     seed drifts; see review doc/plans/2026-04-13-t081-hypermutator-annotation-plan-review.md
     finding #1."
   - Per `cancer_type` group, fit `sklearn.mixture.GaussianMixture(n_components=1)` and `n_components=2`
     with the pinned seed.
   - Compute Hartigan's dip test via `diptest.diptest(tmb_log10)` (new dependency, declared above).
   - Compare BIC(1) vs BIC(2); select 2-component when ΔBIC > 10 AND dip p-value < 0.1 AND
     `n_samples >= gmm_min_samples`.
   - Classify samples: upper component → `is_hypermutator_gmm = True`; else False.
   - Compute `tmb_zscore_within_cancer = (tmb_log10 - group_mean) / group_std` regardless of
     fit quality — this is the fallback signal for row 6/7.
   - Output: `per_cancer_gmm_fits.feather` (per-cancer diagnostics) + `samples_gmm_flagged.feather`
     (sample-level flags with `gmm_posterior_upper` column for continuous score in Task 6).
3. Snakemake rule: consumes all per-study `samples_tmb.feather` + the per-cancer-type canonicalization (t083 when ready, raw labels otherwise).

**Validation criteria:**
- Unit tests pass.
- Integration: TCGA-UCEC exclusion rate ≈ 20–25%, TCGA-COAD ≈ 10–15%, TCGA-SKCM ≈ 5–10%. Assert within ±20% relative.
- Diagnostic plots: GMM overlay on `tmb_log10` histograms per cancer type, saved to `results/diagnostics/tmb_gmm_<cancer_type>.png`.
- Publish `per_cancer_gmm_fits.feather` with columns `[cancer_type, n_samples, bic_1, bic_2, delta_bic, dip_pvalue, fit_quality, upper_component_mean, lower_component_mean]`. Easy for the reviewer to spot-check.

---

### Task 6: Composite hypermutation score + final flag (`annotate_hypermutators`)

**Implements:** the multi-source combination. Emits both a continuous score, a boolean flag, and an
audit trail (`hypermutator_reason`).

**Decision table — the ONE canonical policy (F4 fix):**

The composite score and final flag follow this exhaustive decision table applied per sample.
Evaluated top-to-bottom; first matching row wins; `hypermutator_reason` records which row fired.

| Priority | Condition | `hypermutation_score` | `is_hypermutator` | `hypermutator_reason` |
|---|---|---|---|---|
| 1 | `pole_hotspot_detected == True` | 1.0 | True | `"pole_hotspot"` |
| 2 | `pold1_hotspot_detected == True` | 1.0 | True | `"pold1_hotspot"` |
| 3 | `msi_type == "MSI-H"` | 1.0 | True | `"msi_h"` |
| 4 | GMM fit is **bimodal** for this cancer type AND GMM posterior in upper component > 0.5 | `gmm_posterior_upper` (continuous 0–1) | True | `"gmm_upper_mode"` |
| 5 | GMM fit is **bimodal**, upper posterior ≤ 0.5 | `gmm_posterior_upper` | False | `"gmm_lower_mode"` |
| 6 | GMM fit **unavailable** (single-mode, dip test p ≥ 0.1, or insufficient N) AND `tmb_zscore_within_cancer ≥ 1.5` | `min(1.0, (tmb_zscore - 1.5) / 1.5 + 0.5)` | True | `"zscore_fallback_high"` |
| 7 | GMM fit unavailable AND `tmb_zscore_within_cancer < 1.5` | `max(0.0, tmb_zscore / 3.0)` | False | `"zscore_fallback_low"` |
| 8 | `tmb` is NaN (panel unknown, all-WES-default with no mutations, etc.) | NaN | False | `"tmb_unavailable"` |

Rows 1–3 are **deterministic**: any strong biological signal forces `is_hypermutator = True`
regardless of TMB. This fixes the F4 inconsistency — validation expectations in Task 5/6 are updated
accordingly (100%, not ≥95%, for POLE/POLD1/MSI-H concordance).

**Rationale for row ordering:**
- POLE/POLD1 hotspots force True because these are **diagnostic categories** (clinical pathology
  uses "POLE-hypermutated" as an endometrial-cancer molecular subtype).
- MSI-H is the same (clinical diagnosis, not correlate).
- GMM comes next because it's data-driven and self-calibrating.
- z-score fallback only activates when GMM fails.
- NaN-TMB row is last and is NOT flagged — conservative default for unknown inputs.

**Score threshold note:** `config.hypermutator.score_threshold = 0.5` still exists but in this
policy it only affects rows 4/5 (GMM posterior threshold). Rows 1/2/3 ignore it. Document this
in the config docstring.

**TDD steps:**

1. Write `test_annotate_hypermutators.py` parametrized by the 8 decision-table rows + edge cases:
   - Row 1: POLE hotspot + low TMB → `is_hypermutator == True`, `score == 1.0`, reason `"pole_hotspot"`.
   - Row 2: POLD1 hotspot + no other signal → True, reason `"pold1_hotspot"`.
   - Row 3: MSI-H, normal TMB → True, reason `"msi_h"`.
   - Row 3 edge case: MSI-L → does NOT fire row 3; falls through to rows 4–7.
   - Row 4: bimodal GMM, sample in upper mode with posterior 0.8 → True, score 0.8, reason `"gmm_upper_mode"`.
   - Row 5: bimodal GMM, sample in lower mode with posterior 0.3 → False, score 0.3, reason `"gmm_lower_mode"`.
   - Row 6: GMM unavailable, tmb_zscore = 2.5 → True, reason `"zscore_fallback_high"`.
   - Row 7: GMM unavailable, tmb_zscore = 0.5 → False, reason `"zscore_fallback_low"`.
   - Row 8: tmb is NaN → False, reason `"tmb_unavailable"`.
   - **Edge cases (review finding #4):**
     - **Row 1 priority over NaN-TMB:** POLE hotspot AND tmb is NaN → `is_hypermutator == True`,
       reason `"pole_hotspot"`. Strong signals override missing TMB.
     - **Priority ordering — POLE hotspot AND GMM-lower-mode:** POLE wins (deterministic signal
       overrides GMM posterior).
     - **MSI-H AND tmb_zscore = -1 (low TMB):** row 3 wins; deterministic flag.
     - **Row 8 no-signal:** `pole = pold1 = False`, `msi_type != "MSI-H"`, `tmb is NaN` →
       `is_hypermutator == False`, reason `"tmb_unavailable"`.
2. Write `code/scripts/annotate_hypermutators.py`:
   - Input: `out_dir/metadata/samples_tmb_combined.feather` (contains all per-sample signals after
     Task 3's hotspot detection merge) + `out_dir/metadata/per_cancer_gmm_fits.feather` (Task 5
     output) + `out_dir/metadata/samples_gmm_flagged.feather` (Task 5 output).
   - Apply decision table in priority order via a function `classify_sample(row, gmm_fit) ->
     (score, flag, reason)`.
   - Output: `out_dir/metadata/samples_annotated.feather` with columns `[study_id, sample_id,
     cancer_type, tmb, tmb_log10, tmb_zscore_within_cancer, pole_hotspot_detected,
     pold1_hotspot_detected, msi_type, gmm_posterior_upper, gmm_fit_quality,
     hypermutation_score, is_hypermutator, hypermutator_reason]`.
3. Snakemake rule `annotate_hypermutators` consuming Task 5's outputs.

**Validation criteria:**
- Unit tests cover every row of the decision table (not just the common cases).
- Integration: final `is_hypermutator` rate by cancer type matches Task 5 acceptance ranges.
- Cross-source agreement (now strict, since policy is deterministic): **100%** of
  `pole_hotspot_detected == True` → `is_hypermutator == True`; **100%** of
  `pold1_hotspot_detected == True` → `is_hypermutator == True`; **100%** of `msi_type == "MSI-H"`
  → `is_hypermutator == True`. Any violation is a test failure, not a soft warning.
- `hypermutator_reason` distribution across a realistic study set should be dominated by
  `"gmm_upper_mode"` / `"gmm_lower_mode"` (primary signal), with `"pole_hotspot"`, `"pold1_hotspot"`,
  and `"msi_h"` being minority firings. If rows 6/7 (zscore_fallback) dominate, GMM fits are
  failing broadly — investigate.

---

### Task 7: Per-study inclusive/exclusive ratios + combined passthrough (`create_freq_tables.py` + `create_combined_*`)

**Implements (F1 fix):** the hypermutator-exclusion filter lives at the **per-study** layer where
sample IDs are still available (`create_freq_tables.py:36-46` — `groupby('cancer_type').sample_id
.nunique()`). The combined scripts only pivot already-computed per-study values and cannot
recompute exclusive ratios. This task splits into two parts:

**Task 7a — per-study ratio computation (`create_freq_tables.py`):**

1. Write `test_create_freq_tables.py`:
   - Input: toy per-study `mut.feather` + `samples.feather` + `samples_annotated.feather` (subset of
     samples flagged `is_hypermutator=True`).
   - With no `samples_annotated.feather` input (backward-compat): output matches current
     single-column `num` / `ratio` schema exactly. This is a hard regression check.
   - With `samples_annotated.feather` provided: output gains `num_inclusive` / `num_exclusive` /
     `ratio_inclusive` / `ratio_exclusive` / `n_samples_inclusive` / `n_samples_exclusive` columns.
     `num` / `ratio` remain as aliases for the inclusive pair.
   - Numeric correctness: for a gene present in 10 samples (3 hypermutator, 7 not) within a
     100-sample cohort (20 hypermutators, 80 not): `ratio_inclusive = 10/100 = 0.10`;
     `ratio_exclusive = 7/80 = 0.0875`.
2. Modify `code/scripts/create_freq_tables.py`:
   - Accept optional second input `samples_annotated.feather` path; if provided, left-join its
     `(study_id, sample_id, is_hypermutator)` columns onto the mutation table.
   - Compute each existing `groupby().sample_id.nunique()` ratio twice: once with the full sample
     set (inclusive), once with `is_hypermutator == False` (exclusive). Preserve backward-compat
     `num` / `ratio` aliases.
   - Emit `n_samples_inclusive` / `n_samples_exclusive` per cancer-type as explicit denominators so
     the combined script can compute weighted averages later if desired.
3. Update `code/workflows/Snakefile` `create_freq_tables` rule (review finding #5):
   - **Option chosen: always require `samples_annotated.feather` as an input.** Simpler than
     conditional optional-input plumbing; forces the hypermutator rules into the DAG, which is
     what we want once t081 lands. No legacy-run escape hatch — if you run the Snakefile after
     t081 lands, you must run through the new rules. This is acceptable because the pipeline
     is not yet published and there are no external reruns to support.
   - The rule gains a named input `samples_annotated = out_dir.joinpath("metadata/samples_annotated.feather")`.
   - The script reads it unconditionally. If the column `is_hypermutator` isn't present (e.g.,
     because all samples had `row = 8` reasons), emit a warning; all samples become "not
     hypermutators" → `ratio_inclusive == ratio_exclusive` automatically. No special-case code.

**Task 7b — combined-script passthrough (`create_combined_gene_cancer_freq_table.py`):**

1. Extend `test_create_combined_gene_cancer_freq_table.py` (if one exists; otherwise create):
   - Input: multiple per-study tables each with paired columns (`ratio_inclusive`, `ratio_exclusive`).
   - Output: the wide per-study columns now pivot in pairs (study_A_ratio_inclusive,
     study_A_ratio_exclusive, study_B_...) and two pooled-mean columns (`mean_inclusive`,
     `mean_exclusive`) are emitted.
   - Regression check: when all per-study inputs have `ratio_inclusive == ratio_exclusive`
     (no hypermutators), `mean_inclusive == mean_exclusive` bitwise.
2. Modify `code/scripts/create_combined_gene_cancer_freq_table.py`:
   - Treat paired columns as a single pivot operation that produces two wide matrices.
   - Compute `mean_inclusive` / `mean_exclusive` via existing `mean(axis=1, skipna=True)`.
   - **Drop the single `mean` column** (review finding #3) — consumers explicitly select
     `mean_inclusive` or `mean_exclusive`. Internal sort uses `mean_inclusive` for ranking
     stability.
3. Similarly extend `create_combined_gene_cancer_mutation_matrices.py` — the count matrix gets
   inclusive + exclusive variants.

**Config default — Open-question-1 resolution:**
`hypermutator.exclude_from_aggregation: false` is the default **shipped in t081**. This means
downstream published outputs and the summary.Rmd report surface `mean_inclusive` as the primary
displayed column until t079 (pre-registration) explicitly decides otherwise. Both inclusive and
exclusive columns are **always emitted** regardless of this flag. **Per review finding #3, there
is no `mean` alias** — consumers explicitly select `mean_inclusive` or `mean_exclusive`. The flip
at t079 time becomes a Rmd / consumer-side change ("switch the primary displayed column") rather
than a silent schema-aliasing change.

**Validation criteria:**
- Unit tests pass, including the strict regression check when no hypermutators are present
  (bitwise equality of `mean_inclusive` with the legacy `mean`).
- Integration: for TCGA-UCEC, POLE-driver genes should show noticeably *lower* `mean_exclusive`
  than `mean_inclusive` (hypermutator-inflated rates collapse once excluded).
- Diagnostic report at `doc/reports/hypermutator-impact-<date>.md` showing top 20 gene × cancer
  cells with the largest `|mean_inclusive - mean_exclusive|` gap. This report feeds t079's
  pre-registration decision.

---

### Task 8: Documentation + AGENTS.md updates

**Implements:** future-collaborator onboarding + audit-trail hygiene.

**TDD steps:** (no tests — doc change)

1. Add to `AGENTS.md` "Annotations applied in the pipeline" section:
   - New subsection: "Hypermutator / TMB annotation".
   - Explain continuous columns, boolean flag, composite score, data sources, threshold policy, audit trail.
2. Add section to `doc/guides/modalities/cross-study-aggregation.md` linking `is_hypermutator` to audit-checklist item **(new) agg.15**: "Hypermutator-exclusion applied to cross-study pooled ratios" (paralleling agg.07 for CH).
3. Update `doc/background/topics/tumor-mutational-burden.md` "Relevance to this project" section to point to `samples_annotated.feather` schema.
4. Close t081 with a note pointing to this plan + the implementing commits.

---

## Snakemake-specific appendix

Verified against `code/workflows/Snakefile` — uses `out_dir` (not `data_dir`) for produced
artifacts; `{id}` wildcard from the `studies` list in config. `data_dir` is only used for raw
inputs.

```python
rule build_panel_callable_sizes:
    input:
        genie_coverage = out_dir.joinpath("metadata/genie_panel_coverage.feather"),
    output:
        out_dir.joinpath("metadata/panel_callable_mb.tsv")
    script: "../scripts/build_panel_callable_sizes.py"

rule compute_per_sample_tmb:
    input:
        mut         = out_dir.joinpath("studies/{id}/mut/mut_filtered.feather"),
        samples     = out_dir.joinpath("studies/{id}/metadata/samples.feather"),
        panel_sizes = out_dir.joinpath("metadata/panel_callable_mb.tsv"),
    output:
        out_dir.joinpath("studies/{id}/metadata/samples_tmb.feather")
    script: "../scripts/compute_per_sample_tmb.py"

rule detect_polymerase_hotspots:
    input:
        mut = out_dir.joinpath("studies/{id}/mut/mut_filtered.feather"),
    output:
        out_dir.joinpath("studies/{id}/metadata/sample_polymerase_hotspots.feather")
    script: "../scripts/detect_polymerase_hotspots.py"

rule combine_samples_tmb:
    input:
        samples_tmb   = expand(out_dir.joinpath("studies/{id}/metadata/samples_tmb.feather"), id=ids),
        pole_hotspots = expand(out_dir.joinpath("studies/{id}/metadata/sample_polymerase_hotspots.feather"), id=ids),
    output:
        out_dir.joinpath("metadata/samples_tmb_combined.feather")
    script: "../scripts/combine_samples_tmb.py"

rule fit_per_cancer_tmb_gmm:
    input:
        samples_tmb_combined = out_dir.joinpath("metadata/samples_tmb_combined.feather"),
    output:
        per_cancer_fits      = out_dir.joinpath("metadata/per_cancer_gmm_fits.feather"),
        samples_flagged      = out_dir.joinpath("metadata/samples_gmm_flagged.feather"),
    script: "../scripts/fit_per_cancer_tmb_gmm.py"

rule annotate_hypermutators:
    input:
        samples_tmb_combined = out_dir.joinpath("metadata/samples_tmb_combined.feather"),
        per_cancer_fits      = out_dir.joinpath("metadata/per_cancer_gmm_fits.feather"),
        samples_flagged      = out_dir.joinpath("metadata/samples_gmm_flagged.feather"),
    output:
        out_dir.joinpath("metadata/samples_annotated.feather")
    script: "../scripts/annotate_hypermutators.py"
```

The existing `create_freq_tables` rule (see `Snakefile` current block producing per-entity study
tables) gains `samples_annotated.feather` as a new optional input and emits the new paired-column
schema. The existing `create_combined_gene_cancer_freq_table` rule needs no structural change
beyond carrying the new columns through its pivot.

## Test layout + verification commands

The repo does not currently carry a `pyproject.toml`-declared tests tree (confirmed by grepping
`pyproject.toml` — no `[tool.pytest.ini_options]` or `tool.hatch.envs.test` sections). For this
task, establish a convention:

- New tests live at `code/scripts/tests/test_<module>.py`, importable as plain modules (no
  package `__init__.py` needed — `pytest` auto-discovers via `rootdir` inference).
- Add `pytest>=8.0` to `[project.optional-dependencies].dev` in `pyproject.toml` (new dep;
  complements the already-listed `diptest`).
- Verification commands to append to this task's docstring:
  ```bash
  uv run --frozen pytest code/scripts/tests/ -v
  uv run --frozen ruff check code/scripts/
  uv run --frozen pyright code/scripts/  # if configured; optional
  uv run snakemake --lint -s code/workflows/Snakefile --configfile code/config/config-10k-genes.yml
  ```
- Integration tests that require real study inputs (MSK-IMPACT, TCGA-UCEC) go in
  `code/scripts/tests/integration/` with a `pytest.mark.slow` marker and a pytest option
  `--run-slow` (configured in `conftest.py`) to opt in. Skipped by default in local / CI loops.

Test-infrastructure setup itself is a one-time subtask of Task 8 (documentation): land the
`pyproject.toml` dev-deps update + an empty `code/scripts/tests/conftest.py` as part of the
same commit that adds the first unit test.

---

## Decision criteria (go / no-go / pivot)

This is an exploratory task in the sense that the GMM approach might not produce usable bimodality for all cancer types. Go / no-go checkpoints:

1. **After Task 2** (continuous TMB): if median TMB per cancer type disagrees with published values by >2× across multiple cancers, there's a panel-size or variant-class-filter bug. **Stop and debug before proceeding.**
2. **After Task 5** (GMM fit): if GMM `fit_quality = "single_mode"` or `"not_bimodal"` for CRC, UCEC, and SKCM (the three cancers with established bimodal distributions), the approach is broken. **Stop; fall back to pure z-score threshold + POLE/MSI boolean signals (skip Task 5 outputs).**
3. **After Task 7** (integration): if `mean_inclusive` and `mean_exclusive` differ by < 5% for every top-20 driver gene in every cancer type, the hypermutator exclusion is not producing meaningful signal. **Publish the inclusive ratios only; mark this task as "no material impact" in the done note.** This is a legitimate outcome, not a failure.

---

## After the plan

1. **Run `/science:review-pipeline 2026-04-13-t081-hypermutator-annotation`** before starting implementation — surfaces reviewer-visible gaps in this document.
2. **Pre-registration (t079):** add a statement that pooled ratios in published outputs default to `mean_exclusive`; the inclusive ratio is diagnostic-only. Do this in t079's pre-registration draft.
3. **Surface tasks to the backlog:** Tasks 1–8 above should each be trackable tasks under t081. Offer to create sub-tasks via `science-tool tasks add` with `--related=task:t081`.
4. **Cooling-off (process-bias mitigation):** implementation should begin after ≥24 hours and ideally after a separate reviewer — even just a `superpowers:requesting-code-review` pass on *this plan* — has sanity-checked the GMM + composite score design.
