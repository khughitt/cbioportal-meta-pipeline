---
type: interpretation
title: First end-to-end PoC run of the annotated pipeline
status: active
created: '2026-04-17'
updated: '2026-06-28'
id: interpretation:0001-poc-run
mode: dev
source_refs:
- task:t100
- task:t081
related:
- task:t100
- task:t081
- task:t070
- task:t105
- plan:0001-t081-hypermutator-annotation-pipeline-plan
input: "task:t100 \u2014 config-poc.yml end-to-end annotated pipeline run"
workflow_run: t100-2026-04-17-poc
prior_interpretations: []
---

# Interpretation — 2026-04-17 PoC run (t100)

Project links: this PoC interpretation is anchored to `task:t100`, `task:t081`, `task:t070`, and
`task:t105`, with the hypermutator implementation context in
`plan:0001-t081-hypermutator-annotation-pipeline-plan`.

## Verdict

**Verdict:** [~] Pipeline runs end-to-end; POLE detector validates at canonical UCEC frequency, but composite hypermutator flag miscalibrated for BRCA/SKCM and MSK TMB deflated 30×.

<!-- Backfilled 2026-04-19 per discussion:2026-04-19-verdict-polarity-display -->

## What ran

**Studies (4 / `config-poc.yml`):**

| Study | N samples | Platform | Matched-normal |
|---|---:|---|---|
| `ucec_tcga_pan_can_atlas_2018` | 529 | TCGA WES | yes |
| `skcm_tcga_pan_can_atlas_2018` | 448 | TCGA WES | yes |
| `brca_tcga_pan_can_atlas_2018` | 1,084 | TCGA WES | yes |
| `msk_impact_2017` | 10,945 | Panel (IMPACT-341/410/468) | no |
| **Total** | **13,006** | | |

Pipeline: full `rule all` minus the commented-out R summary.Rmd target. 54 jobs. Wallclock ~1h 45m.
Outputs under `results/poc-2026-04-17/` (4.8 GB, gitignored).

## Headline findings

### Finding 1 — the first `results/` artifact from the annotated pipeline exists.

All canonical annotated outputs landed:

- `summary/mut/table/gene_cancer_study.feather` (68,287 rows)
- `summary/mut/table/gene_cancer_study_annotated.feather` — Bailey / CGC / Sanchez-Vega overlays applied
- `summary/mut/table/gene_cancer_study_ratio_annotated.feather` — overlays + CH annotation + per-study paired inclusive/exclusive ratio columns (t098 paired schema working end-to-end)
- `metadata/samples_annotated.feather` (13,006 × 48) — per-sample hypermutator annotation with `is_hypermutator` + 3 dual flags (absolute / ultra / relative) + `hypermutator_reason` audit trail
- `metadata/panel_callable_mb.tsv`, `per_cancer_gmm_fits.feather`, `samples_gmm_flagged.feather` — all hypermutator pipeline diagnostic outputs

### Finding 2 — the POLE detector empirically validates at canonical frequency.

| Study | POLE hotspot rate | Expected (literature) |
|---|---:|---|
| UCEC TCGA | 41 / 529 = **7.8%** | TCGA 2013 UCEC canonical ~7% ✓ |
| SKCM TCGA | 0.0% | expected ~0% ✓ |
| BRCA TCGA | 0.2% | expected ~0% ✓ |

This is the first empirical validation of t094 (POLE/POLD1 detector). It matches published canonical frequencies tightly.

### Finding 3 — Campbell-absolute flag (`is_hypermutator_absolute`, ≥10 mut/Mb) is the most reliable of the four hypermutator columns.

| Study | Absolute (≥10) | Ultra (≥100) | Relative (Samstein top-20%) | Composite `is_hypermutator` |
|---|---:|---:|---:|---:|
| UCEC TCGA | 34.6% | **9.3%** | 28.2% | 42.0% |
| SKCM TCGA | **62.7%** | 2.7% | 36.4% | 96.4% |
| BRCA TCGA | 2.6% | 0.4% | 45.5% | 92.2% |
| msk_impact_2017 | 0.1% | 0.0% | 20.7% | 12.1% |

UCEC ultra (9.3%) is very close to canonical POLE-UCEC prevalence (~7%). SKCM absolute (63%) matches the expectation that most cutaneous melanomas exceed 10 mut/Mb [@Alexandrov2013Nature].

### Finding 4 — the **composite GMM-derived `is_hypermutator` flag is biased high for cohorts with uniformly-high TMB or no real bimodality.**

BRCA 92% "hypermutator" and SKCM 96% "hypermutator" are not biologically plausible. Looking at `fit_quality`: BRCA and SKCM were both fit as `bimodal` (100% of samples), and 997/1084 BRCA samples were assigned to `gmm_upper_mode`. The t097 decision table places `gmm_upper_mode → is_hypermutator=True` as rule 4, but that rule assumes the "upper mode" is genuinely the hypermutated tail. When the GMM overfits noise into two components over a unimodal distribution (BRCA) or when the whole distribution is above the canonical threshold (SKCM), the rule breaks.

Similarly, `is_hypermutator_relative` (Samstein top-20%) shows 45% for BRCA and 36% for SKCM. The implementation likely promotes tied samples above the 80th-percentile cut-line; needs inspection.

**Recommendation for t077 (GLMM-logit pooling) and any downstream analysis**: use `is_hypermutator_absolute` as the primary exclusion flag in the inclusive/exclusive pivot pair until the composite is recalibrated.

### Finding 5 — MSK-IMPACT TMB is deflated ~30× because `study_panel_map` is empty.

msk_impact_2017 median TMB = 0.13 mut/Mb (reported in the output) vs expected ~4 mut/Mb for MSK-IMPACT [@Zehir2017]. Ratio ≈ 30×, which equals `wes_default_callable_mb (30) / IMPACT-410 (1.01)`. With `study_panel_map` left empty for this PoC, every MSK sample fell back to the 30-Mb WES default in the denominator, deflating every per-sample TMB.

This is exactly what t070 exists to solve (per-sample panel-version assignment from the per-sample panel column MSK studies carry). **t070 is now confirmed load-bearing for any analysis that mixes panel + WES studies.** Single-study panel or single-study WES analyses are unaffected.

### Finding 6 — cross-study ratio numbers for genes common to MSK-IMPACT look sane.

TP53 ratios in cancer types covered by MSK-IMPACT:

| Cancer type | TP53 ratio (msk_impact_2017) | Canonical |
|---|---:|---|
| Small Cell Lung Cancer | 87% | 85-90% ✓ |
| Esophagogastric Cancer | 70% | 70-85% ✓ |
| Non-Small Cell Lung Cancer | 55% | 45-55% ✓ |
| Colorectal Cancer | 72% | 45-55% (slightly high — possible MSI-H/POLE upward pull) |
| Pancreatic Cancer | 57% | 60-75% ✓ |

Results are in the right ballpark. No gross misencoding of the count table.

## Bugs surfaced by the PoC

All of the following were latent in the Snakefile / scripts — the previous complete run was before the t081 arc, so these had never been exercised:

| # | Severity | Bug | Fix |
|---|---|---|---|
| 1 | **High** | All 11 t081-era scripts had `from __future__ import annotations` after other statements → `SyntaxError` under Snakemake's preamble injection. These scripts had **never** executed under Snakemake; only unit-tested via pytest imports. | Removed `from __future__` (unnecessary on Python 3.13). |
| 2 | **High** | `cluster_genes.py` / `cluster_cancer_types.py` require a `clustering.{gene,cancer}.*` config sub-tree that appears in **no** shipped config file. These rules had also never successfully run. | Added defaults to `config-poc.yml`. Existing configs (`config-10k-genes.yml`, `config-full.yml`, `config-pan-cancer.yml`) still lack them → follow-up task. |
| 3 | Medium | `rule create_gene_cancer_mutation_count_matrix` declared `mut/mut_filtered.feather` as input while `filter_genes` produces `mut/table/mut_filtered.feather` (inconsistent with sister rule `create_gene_patient_mutation_count_matrix`). | Fixed in-place in Snakefile. |
| 4 | Medium | `summary/summary.html` was still listed in `rule all` despite the producing R-Rmd rule being commented out pending Python port. | Removed from `rule all`. |
| 5 | Medium | `convert_to_feather.py` for `skcm_tcga_pan_can_atlas_2018` failed with `TypeError: dtype of categories must be the same` — pandas C parser's chunked read produces categoricals whose dtypes differ across chunks. | Added `low_memory=False` to force single-pass read. |
| 6 | Medium | `create_correlation_matrices.py`'s `gene.T.corr()` is O(n_genes²); brca_tcga ~20k genes took **55 min**. Will be worse for any pan-cancer run. | Recorded as **t104**. |
| 7 | Low | `bailey2018_source` / `cgc_source` / `sanchez_vega_source` columns in the annotated tables contain **output file paths** (e.g. `results/poc-2026-04-17/metadata/bailey2018_drivers.feather`) rather than version strings. Provenance is supposed to be a version stamp. | Follow-up task. |
| 8 | Low | `tee` in the shell command line masked snakemake's real exit code; needed `echo "SNAKEMAKE_EXIT=$?"` inside a subshell to get the actual status. Affects anyone running the pipeline with `| tee`. | Use `set -o pipefail` or `PIPESTATUS[0]` consistently in docs. |

## Revised P1 priorities for the pipeline

Pre-PoC P1 list: t052, t070, t076, t077. Post-PoC, ordered by what the run empirically surfaced as load-bearing:

| Rank | Task | Why | Evidence |
|---|---|---|---|
| 1 | **t070** (MSK-IMPACT panel-version drift) | Without it, every MSK TMB is deflated ~30×, which cascades into GMM fit, z-score fallback, and composite flag calibration. | Finding 5: MSK median TMB 0.13 mut/Mb vs expected ~4. |
| 2 | **NEW t105 (proposed): recalibrate composite `is_hypermutator` flag.** Options: (a) require `fit_quality == "bimodal"` **AND** the upper-mode mean > some absolute floor; (b) replace GMM rule with absolute + Samstein as the two primary flags and demote the composite to a derived column; (c) inspect the Samstein-relative implementation for tied-sample promotion bug. | Finding 4: composite flag is wrong for BRCA and SKCM. | Recommend Option (a) + Option (c) fix. |
| 3 | **NEW t106 (proposed): use version stamps, not output-file paths, for annotation-source provenance.** | Finding 7: sources contain results-relative paths that change every run. | Read a VERSION constant at the top of each annotate_* script. |
| 4 | t076 (F2 full close: NaN-vs-0 handling) | Still load-bearing for cross-study pooling. | Not surfaced as wrong by this PoC (single-study-per-cancer-type bulk), but will bite when we pool across panels. |
| 5 | t077 (GLMM-logit pooled gene×cancer) | Should run against a **fixed t070 + recalibrated hypermutator-exclusion** pooled table, not this PoC's raw output. | Pre-registration is in hand (t079); decomposition task is t101. |
| 6 | t052 (cohort-stage descriptor) | Not surfaced as urgent by this PoC (MSK-IMPACT 2017 is a single-stage cohort; TCGA cohorts are primary). Re-evaluate once a metastatic panel cohort (e.g. msk_met_2021) is added. | Lower priority than above. |

## Recommended follow-up tasks to create

- **t105**: Recalibrate composite `is_hypermutator` — Finding 4. Either require bimodal + absolute floor, or demote composite to derived. **P1**.
- **t106**: Replace output-path provenance with version stamps across annotate_* scripts. **P2**.
- **t107**: Backport `clustering.*` defaults to `config-10k-genes.yml`, `config-full.yml`, `config-pan-cancer.yml` or make the rule opt-out when missing. **P2**.
- **t108**: Investigate `is_hypermutator_relative` 45% BRCA rate — likely tied-sample promotion at the 80th-percentile cut. **P2**.

## What the PoC did NOT test

- MC3 pseudo-study (`tcga_mc3`): not in this run; t102 / t108-style bugs in MC3 ingestion will surface only when added.
- AACR GENIE: not in this run (would multiply wallclock).
- The co-occurrence / mutual-exclusivity track (t078): never connected to the pipeline — still proposed.
- R-dependent `dndscv` rule: not in `rule all`; no run.
- Age-adjusted TMB (t088): optional; not implemented.
- Graded CH probability (t087): not implemented; this PoC carries the uniform boolean CH flag.

## Update — post-t105 (composite hypermutator floor)

Re-ran the `annotate_hypermutators` rule and downstream ratio tables on the
existing PoC outputs after landing t105 (composite-floor gate on row 4 of
the decision table; default 10 mut/Mb applied to BOTH the cancer type's
GMM upper-component mean AND the sample's own TMB).

| Study | composite (pre-t105) | composite (post-t105) | absolute (≥10) | gmm_upper_mode_below_floor (new reason) |
|---|---:|---:|---:|---:|
| BRCA | 92.2% | **0.2%** | 2.6% | 997 (entire upper mode demoted: BRCA upper_mean=2.4 mut/Mb fails per-mode gate) |
| SKCM | 96.4% | **62.7%** | 62.7% | 151 (per-sample gate filtered samples with TMB <10 from the high-TMB melanoma upper mode) |
| UCEC | 42.0% | **34.8%** | 34.6% | 38 (small drop; POLE/POLD1/MSI rows take precedence anyway) |
| MSK-IMPACT 2017 | 12.1% | **0.7%** | 0.1% | 1245 (MSK per-cancer upper modes mostly fall below the 10 mut/Mb floor due to t070-related TMB deflation; will recover once t070 lands) |

The composite flag now agrees closely with `is_hypermutator_absolute` for
SKCM and UCEC, and is appropriately near-zero for BRCA — fixing Finding 4.
MSK's apparent drop is a downstream consequence of the t070 panel-denominator
issue (see Finding 5); reassessing MSK composite numbers after t070 lands is
expected.

The new audit-trail reason `gmm_upper_mode_below_floor` records the
demotions explicitly so a researcher can always reconstruct why a sample
that "looked like" an upper-mode hypermutator was not flagged.

## Bottom line

The annotated pipeline now runs end-to-end on real data, and the hypermutator annotation arc (t092–t099) works for its two primary signals: **POLE detector validates at canonical 7.8% UCEC frequency**, and the **Campbell-absolute flag (≥10 mut/Mb)** gives biologically-plausible hypermutator rates across the 4 PoC cohorts. The composite GMM-driven flag is miscalibrated for homogeneous-high-TMB cohorts (BRCA / SKCM) and needs recalibration before pooled analyses (t077) consume it. Eight latent Snakefile / script bugs were flushed out, confirming that the "the plan claims it works, the tests pass, therefore it works" assumption about t092–t099 was partly wrong — unit tests passed but the pipeline never actually ran.

The pivot recommendation (t070 first → t105 recalibrate → t076 → t077 decomposition → t077 execution) is now grounded in run output rather than speculation.
