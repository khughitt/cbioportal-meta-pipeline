# Hypermutator / TMB annotation pipeline plan (t081)

> **For Claude:** REQUIRED SUB-SKILL: use `superpowers:executing-plans` to implement this plan task-by-task. Do **not** start Task 1 before `t079` (pre-register pooling method) has resolved whether this annotation affects pre-registered decisions.

**Goal:** Add data-driven, multi-source, continuous hypermutation annotation to every sample in every study, exposing both continuous diagnostic columns and a derived boolean flag. Provide a config-controlled hypermutator-exclusion hook for cross-study aggregation, preserving auditability of included-vs-excluded comparisons.

**Architecture:**

```
data_clinical_sample.txt  ─┐
  (per study)               │
                            ├─> convert_to_feather.py  ───> samples.feather (+MSI cols)
data_mutations.txt ─────────┘                                     │
  (per study)                                                     │
                                                                  ▼
genie_panel_coverage.feather ─┐                        ┌──> mutation_counts.feather
                              │                        │  (per-sample totals)
study_panel_map (config) ─────┼─> panel_callable_mb ───┤
                              │    (new rule)          │
published panel sizes ────────┘                        ▼
                                          samples_with_tmb.feather
                                          (tmb, tmb_log10,
                                           pole_hotspot, pold1_hotspot)
                                                       │
              ┌────────────────────────────────────────┤
              │                                        │
              ▼                                        ▼
per-cancer GMM fit                            per-study summaries
  (samples_all_studies.feather)               (rolled up)
              │
              ▼
samples_annotated.feather
  (+ tmb_zscore, is_hypermutator_gmm,
     hypermutation_score, is_hypermutator)
              │
              ▼
(downstream: create_combined_* consume
  is_hypermutator via config flag)
```

**New dependencies:** `diptest>=0.9` (Hartigan's dip test of unimodality — small, C-backed, one function). `sklearn.mixture.GaussianMixture` is already present via scikit-learn. No other new libraries.

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
- Run on a subset of studies with published hypermutator rates and check agreement within tolerance:
  - **TCGA-UCEC (endometrial):** ~25% hypermutator expected (Cancer Genome Atlas 2013); POLE-ultramutated subset ~7%.
  - **TCGA-COAD/READ:** MSI-H rate ~15%; hypermutator rate matches.
  - **TCGA-SKCM:** UV-hypermutator rate ~5% of the upper TMB tail.
  - **msk_impact_2017 (Zehir 2017 10k cohort):** overall hypermutator rate ~3–5%; CRC-hypermutator ~10–15%.
- Acceptance: flagged rate within ±20% relative of the literature rate per cancer type with ≥ 50 samples.

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
| `code/scripts/convert_to_feather.py` | Ingest `MSI_TYPE` / `MSI_STATUS` / `MSI_SCORE` from `data_clinical_sample.txt` when present; add to `samples.feather`. Zero-impact when columns absent. | Task 2 |
| `code/scripts/convert_to_feather.py` | Retain `variant_class` and `hgvsp_short` (already done — verified). No change. | — |
| `code/config/config-10k-genes.yml` | Add `hypermutator` section with `gmm_min_samples`, `zscore_fallback_threshold`, `exclude_from_aggregation` keys. Add WES default callable-Mb (30). | Task 1 |
| `code/config/config-10k-genes.yml` | Add `panel_callable_mb` override map for MSK-IMPACT variants (341, 410, 468 panels have published sizes: 1.014 Mb, 1.162 Mb, 1.446 Mb — Cheng 2015, Zehir 2017). | Task 1 |
| `code/workflows/Snakefile` | New rules: `build_panel_callable_sizes`, `compute_per_sample_tmb`, `detect_polymerase_hotspots`, `fit_per_cancer_tmb_gmm`, `annotate_hypermutators`. Wire between per-study outputs and `create_combined_*`. | Tasks 1–6 |
| `code/scripts/create_combined_sample_table.py` | Add `is_hypermutator`, `hypermutation_score`, `tmb`, `tmb_log10`, `tmb_zscore_within_cancer`, `pole_hotspot_detected`, `pold1_hotspot_detected`, `msi_type` columns to combined output. | Task 7 |
| `code/scripts/create_combined_gene_cancer_freq_table.py` | Add optional hypermutator-exclusion path controlled by `config["hypermutator"]["exclude_from_aggregation"]`. Compute both inclusive and exclusive pooled ratios; mark exclusive as default for consumer-facing outputs. | Task 7 |
| `AGENTS.md` | Add "Hypermutator / TMB annotation" subsection to "Annotations applied in the pipeline". | Task 8 |

---

## Task breakdown

### Task 1: Panel callable-Mb registry (`build_panel_callable_sizes`)

**Inquiry-node equivalent:** input-side normalization. Computes the denominator for TMB.

**Implements:** Assumption 2 (panel-callable-Mb approximation). Produces `data/panel_callable_mb.tsv` (version-controlled).

**TDD steps:**

1. Write a test `test_panel_callable_sizes.py` asserting:
   - Given a GENIE panel BED with 3 records (each 1000 bp exonic), output is 0.003 Mb.
   - Given MSK-IMPACT-468 in the override map, output is 1.446 Mb regardless of BED.
   - Unknown panel ID → config default (30 Mb, WES assumption) with a warning logged.
2. Write `code/scripts/build_panel_callable_sizes.py`:
   - Read `genie_panel_coverage.feather` (from existing `process_genie_panel_coverage`).
   - Sum `end - start` per panel across `Feature_Type == "exon"` records, convert to Mb.
   - Apply override map from config (MSK-IMPACT variants + any other panels with published sizes).
   - Emit `panel_callable_mb.tsv` with columns `[panel_id, callable_mb, source]` where `source ∈ {"bed_sum", "config_override", "wes_default"}`.
3. Add Snakemake rule `build_panel_callable_sizes` consuming the GENIE coverage feather + config, producing `data/panel_callable_mb.tsv`.
4. Sanity check: MSK-IMPACT-468 sum from the BED should be within ±5% of 1.446 Mb. Log the ratio.

**Validation criteria:**
- Unit tests pass.
- MSK-IMPACT panels: bed-derived size within 5% of published. If not, note in `source` column (we'll prefer the config-override in that case).
- Manual inspection: rule output covers every `panel_id` in `study_panel_map` config keys.

**Reusable:** `reusable: true`. A versioned panel-callable registry has value beyond this task — it's reused by t070 (panel-version drift), t076 (NaN-vs-0 panel-aware), and t077 (GLMM-logit) as a study-level covariate. Flag in output.

---

### Task 2: Per-sample TMB calculation (`compute_per_sample_tmb`)

**Implements:** core continuous-TMB signal. Respects Assumption 3 (protein-altering numerator).

**TDD steps:**

1. Write `test_compute_per_sample_tmb.py` asserting:
   - 100 synthetic samples, each with N mutations in `variant_class` ∈ protein-altering set → `mutation_count == N`.
   - Silent / intron mutations are excluded from the count.
   - `tmb = mutation_count / panel_callable_mb` (exact arithmetic).
   - `tmb_log10 = log10(tmb + 1)` (log-transform for zero-safety).
   - A sample in a study with unknown panel → uses WES default (30 Mb) and gets a `tmb_source = "wes_default"` annotation.
2. Write `code/scripts/compute_per_sample_tmb.py`:
   - Input: `mut.feather` (per study), `samples.feather` (per study), `panel_callable_mb.tsv`, `study_panel_map` (from config).
   - Filter `mut.feather` to protein-altering variant classes (constant list in the script, cross-referenced to Assumption 3).
   - Group by `sample_id_tumor`, count rows → `mutation_count`.
   - Join to `samples.feather` (left join on `sample_id_tumor`). Samples with zero mutations get `mutation_count = 0` (preserve row).
   - Look up panel → callable Mb → compute `tmb`, `tmb_log10`.
   - Emit augmented `samples.feather` (overwrites the study's `samples.feather`? OR writes a new `samples_tmb.feather`? → new file for auditability; existing downstream consumers unaffected).
3. Snakemake rule `compute_per_sample_tmb` per study: `samples_tmb.feather` wildcarded on `{id}`.

**Validation criteria:**
- Unit tests pass.
- Integration: on msk_impact_2017, median `tmb` across the cohort should be ~3–6 mut/Mb (Chalmers 2017); zero samples with `mutation_count == 0` (MSK-IMPACT requires ≥1 call to be in the cohort). Log and assert.
- Spot-check: sample with 5000 mutations in a panel study → flag immediately as obvious data issue (likely CH-contaminated tumor-only or corrupted count).

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
   - Input: cross-study samples table (concat of per-study `samples_tmb.feather`).
   - Per `cancer_type` group, fit `sklearn.mixture.GaussianMixture(n_components=2)` to `tmb_log10`.
   - Compute Hartigan's dip test via `diptest.diptest(tmb_log10)` (new dependency, declared above).
   - Compare BIC(1) vs BIC(2); select 2-component when ΔBIC > 10.
   - Classify samples: upper component → `is_hypermutator_gmm = True`; else False.
   - Compute `tmb_zscore_within_cancer = (tmb_log10 - group_mean) / group_std`.
   - Output: `per_cancer_gmm_fits.feather` (per-cancer diagnostics) + `samples_gmm_flagged.feather` (sample-level flags).
3. Snakemake rule: consumes all per-study `samples_tmb.feather` + the per-cancer-type canonicalization (t083 when ready, raw labels otherwise).

**Validation criteria:**
- Unit tests pass.
- Integration: TCGA-UCEC exclusion rate ≈ 20–25%, TCGA-COAD ≈ 10–15%, TCGA-SKCM ≈ 5–10%. Assert within ±20% relative.
- Diagnostic plots: GMM overlay on `tmb_log10` histograms per cancer type, saved to `results/diagnostics/tmb_gmm_<cancer_type>.png`.
- Publish `per_cancer_gmm_fits.feather` with columns `[cancer_type, n_samples, bic_1, bic_2, delta_bic, dip_pvalue, fit_quality, upper_component_mean, lower_component_mean]`. Easy for the reviewer to spot-check.

---

### Task 6: Composite hypermutation score + final flag (`annotate_hypermutators`)

**Implements:** the multi-source combination. Emits both continuous score and boolean.

**TDD steps:**

1. Write `test_annotate_hypermutators.py`:
   - Sample with POLE hotspot + high tmb_zscore + MSI-H → `hypermutation_score` near 1.0; `is_hypermutator = True`.
   - Sample with all three signals absent → score near 0.0; False.
   - Sample with conflicting signals (high tmb_zscore but no MSI/POLE) → score ≈ 0.5; flag based on score threshold.
   - Sample with missing MSI → score computed from TMB+POLE only; scale preserved.
2. Write `code/scripts/annotate_hypermutators.py`:
   - Input: `samples_gmm_flagged.feather` + `samples_tmb.feather` + `sample_polymerase_hotspots.feather` + MSI columns (already in combined samples).
   - Composite score (discussed in design):
     ```
     # Base: GMM-derived membership probability (continuous) if fit_quality=="bimodal"
     # else Tukey-style distance from per-cancer median.
     score_tmb = gmm_upper_component_posterior if bimodal else
                 max(0, min(1, (tmb_zscore - 1.5) / 1.5))

     # Strong boolean boosts
     score_pole = 1.0 if pole_hotspot or pold1_hotspot else 0.0
     score_msi  = 1.0 if msi_type == "MSI-H" else 0.0

     # Combination (weighted max — any strong signal dominates)
     hypermutation_score = max(score_tmb, score_pole, score_msi)

     # Derived boolean (configurable threshold; default 0.5)
     is_hypermutator = hypermutation_score >= config["hypermutator"]["score_threshold"]
     ```
   - Output: `samples_annotated.feather` with full column set.
3. Snakemake rule `annotate_hypermutators` consuming all upstream per-study + GMM outputs.

**Validation criteria:**
- Unit tests pass.
- Integration: final `is_hypermutator` rate by cancer type matches Task 5 acceptance ranges.
- Cross-source agreement: ≥ 95% of `pole_hotspot_detected == True` samples also have `is_hypermutator == True`. Flag any violations. Expect ≥ 80% of `msi_type == "MSI-H"` also flagged (MSI samples have more variance in TMB due to called-indel differences).

---

### Task 7: Cross-study aggregation filter wire-in (`create_combined_*` extensions)

**Implements:** the actual user-facing behavior change. This is where the audit's HIGH-severity confound finally gets mitigated in published outputs.

**TDD steps:**

1. Write `test_create_combined_gene_cancer_freq_table.py` (extend existing):
   - With `config.hypermutator.exclude_from_aggregation = True`: pooled ratio excludes samples where `is_hypermutator == True`.
   - With `False`: pooled ratio matches previous behavior (regression check — must not alter current numbers).
   - Both paths always emit two ratio columns: `mean_inclusive` and `mean_exclusive` (plus per-study counts contributing to each).
2. Modify `code/scripts/create_combined_gene_cancer_freq_table.py`:
   - Load `samples_annotated.feather` as hypermutator lookup.
   - For each per-study ratio calculation, compute the hypermutator-excluded numerator / denominator as a second parallel pathway.
   - Emit both pooled-mean columns + `n_hypermutator_excluded` diagnostic.
3. Similarly extend `create_combined_gene_cancer_mutation_matrices.py` for the wide count matrix.
4. Config default: `exclude_from_aggregation = True` (aligned with audit recommendation) but keep inclusive ratios for audit trail.

**Validation criteria:**
- Unit tests pass, including the regression check on inclusive ratios (must be bitwise-identical to current behavior when recomputed).
- Integration: for TCGA-UCEC, POLE-driver genes (e.g., POLE itself, PTEN, TP53) should show *lower* `mean_exclusive` than `mean_inclusive` because their frequencies are inflated by hypermutators.
- Produce a diagnostic report `doc/reports/hypermutator-impact-<date>.md` showing top 20 gene × cancer cells with the largest |mean_inclusive - mean_exclusive| gap.

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

The project is Snakemake-based (`code/workflows/Snakefile`), so here are the rule sketches for reference. These sit between the existing `convert_to_feather` output (per-study `samples.feather`) and the `create_combined_*` consumers.

```python
rule build_panel_callable_sizes:
    input:
        genie_coverage=f"{data_dir}/genie_panel_coverage.feather",
    output:
        f"{data_dir}/panel_callable_mb.tsv"
    script: "../scripts/build_panel_callable_sizes.py"

rule compute_per_sample_tmb:
    input:
        mut=f"{data_dir}/studies/{{id}}/mut/mut_filtered.feather",
        samples=f"{data_dir}/studies/{{id}}/samples.feather",
        panel_sizes=f"{data_dir}/panel_callable_mb.tsv",
    output:
        f"{data_dir}/studies/{{id}}/samples_tmb.feather"
    script: "../scripts/compute_per_sample_tmb.py"

rule detect_polymerase_hotspots:
    input:
        mut=f"{data_dir}/studies/{{id}}/mut/mut_filtered.feather",
    output:
        f"{data_dir}/studies/{{id}}/sample_polymerase_hotspots.feather"
    script: "../scripts/detect_polymerase_hotspots.py"

rule fit_per_cancer_tmb_gmm:
    input:
        samples_tmb=expand(f"{data_dir}/studies/{{id}}/samples_tmb.feather",
                           id=studies),
    output:
        per_cancer_fits=f"{data_dir}/combined/per_cancer_gmm_fits.feather",
        samples_flagged=f"{data_dir}/combined/samples_gmm_flagged.feather",
    script: "../scripts/fit_per_cancer_tmb_gmm.py"

rule annotate_hypermutators:
    input:
        samples_gmm=f"{data_dir}/combined/samples_gmm_flagged.feather",
        samples_tmb=expand(f"{data_dir}/studies/{{id}}/samples_tmb.feather",
                           id=studies),
        pole_hotspots=expand(f"{data_dir}/studies/{{id}}/sample_polymerase_hotspots.feather",
                             id=studies),
    output:
        f"{data_dir}/combined/samples_annotated.feather"
    script: "../scripts/annotate_hypermutators.py"
```

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
