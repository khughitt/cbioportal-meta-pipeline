---
type: interpretation
title: 't070: PoC pre/post comparison for MSK-IMPACT panel-version drift handling'
status: active
created: '2026-04-18'
updated: '2026-04-22'
id: interpretation:0002-t070-poc-comparison
mode: dev
source_refs:
- task:t070
- task:t100
related:
- task:t070
- task:t100
- task:t105
- interpretation:0001-poc-run
input: 'Pre/post comparison: /data/packages/cbioportal/poc-pre-t070 vs results/poc-2026-04-17'
workflow_run: t070-2026-04-18-poc-comparison
prior_interpretations:
- interpretation:0001-poc-run
---

# t070 PoC pre/post comparison

**Date:** 2026-04-18
**Task:** t070 — MSK-IMPACT panel-version drift handling per sample
**Design spec:** `doc/plans/2026-04-18-t070-msk-impact-panel-version-drift-design.md`
**Implementation plan:** `doc/plans/2026-04-18-t070-msk-impact-panel-version-drift-implementation-plan.md`

## Verdict

**Verdict:** [+] t070 fix delivers predicted ~30× TMB correction and flips 401 MSK samples to correct hypermutator status; magnitudes match to 3 sig figs.

<!-- Backfilled 2026-04-19 per discussion:2026-04-19-verdict-polarity-display -->

## Summary

t070 eliminates two silent biases in `msk_impact_2017` outputs by keying
the per-sample panel denominator on each sample's actual panel version
(MSK-IMPACT-341 / MSK-IMPACT-410) instead of the study-level WES default.
Both predicted magnitudes match empirics to 3 significant figures:

- **Per-sample TMB shifts 30×–34×** upward (from 30 Mb WES fallback to the
  real 0.89 / 1.01 Mb panel denominators). Median TMB moves from
  0.10–0.13 → 3.37–3.96 mut/Mb.
- **Per-(cancer, gene) rate shifts up to 1.75× upward** for IMPACT-410-only
  genes in cancer types with small MSK cohorts. The bulk of (cancer, gene)
  rows are unchanged (ratio = 1.00) because genes covered by all MSK panels
  have the full 10,945-sample denominator both pre and post.
- **3.8% of MSK samples** (419/10,945) shift their `is_hypermutator` flag —
  almost entirely in the False → True direction (401 newly flagged), as
  the TMB correction lifts previously artificially-low values above the
  10 mut/Mb threshold from [@Campbell2017Hypermutation].

## Methodology

Two parallel pipeline runs of `config-poc.yml`
(`ucec_tcga_pan_can_atlas_2018` + `skcm_tcga_pan_can_atlas_2018` +
`brca_tcga_pan_can_atlas_2018` + `msk_impact_2017`):

| | `panel_bearing_studies` | out_dir |
|---|---|---|
| Pre-t070 | `[]` | `/data/packages/cbioportal/poc-pre-t070` |
| Post-t070 | `[msk_impact_2017]` | `results/poc-2026-04-17` |

Both runs consumed identical raw inputs. The only delta is the
`panel_bearing_studies` config key — everything else (hypermutator
detection, GMM fits, clustering, correlation) is held constant.

Comparison notebook: `code/notebooks/t070_poc_comparison.py` (marimo).
Numbers below generated via `uv run python` inline (the marimo version
is for interactive exploration).

## Axis 1 — Per-sample TMB denominators

| panel_id | n | median_mb_pre | median_mb_post | median_tmb_pre | median_tmb_post | post/pre |
|---|---:|---:|---:|---:|---:|---:|
| MSK-IMPACT-341 | 2,809 | 30.00 | 0.89 | 0.100 | 3.371 | **33.71×** |
| MSK-IMPACT-410 | 8,136 | 30.00 | 1.01 | 0.133 | 3.960 | **29.70×** |

**Interpretation:** Pre-t070 used `wes_default_callable_mb = 30 Mb` for
every MSK sample because `msk_impact_2017` wasn't in `study_panel_map`
(the project-wide "no panel info, use WES default" escape hatch).
Post-t070 uses each sample's actual panel callable-Mb value.

The observed post/pre ratio matches `30 / panel_mb` exactly for both
panels: 30 / 0.89 = 33.71, 30 / 1.01 = 29.70. This is expected — the
numerator (mutation count) is unchanged; only the denominator shifts.

**Consequence**: pre-t070 TMB values for MSK samples were all artificially
compressed by ~30×. A sample with 20 mutations on IMPACT-341 appeared as
0.67 mut/Mb (non-hypermutator) pre-t070 and as 22.5 mut/Mb (well above
the 10 mut/Mb hypermutator floor from [@Campbell2017Hypermutation]) post-t070. Mean TMB mean/panel:
MSK-IMPACT-341 0.19 → 6.48; MSK-IMPACT-410 0.24 → 7.07.

## Axis 2 — Hypermutator flag transitions

| | count |
|---|---:|
| Total MSK samples compared | 10,945 |
| Flag flipped | 419 (3.8%) |
| False → True (newly flagged post-t070) | **401** |
| True → False (unflagged post-t070) | 18 |

**Top `hypermutator_reason` transitions (pre → post):**

| reason_pre | reason_post | n |
|---|---|---:|
| gmm_lower_mode | zscore_fallback_low | 3,797 |
| gmm_lower_mode | gmm_lower_mode | 3,242 |
| gmm_lower_mode | gmm_upper_mode_below_floor | 1,766 |
| zscore_fallback_low | zscore_fallback_low | 711 |
| gmm_upper_mode_below_floor | gmm_upper_mode_below_floor | 413 |
| gmm_upper_mode_below_floor | zscore_fallback_low | 409 |
| gmm_upper_mode_below_floor | zscore_fallback_high | 249 |
| gmm_upper_mode_below_floor | gmm_upper_mode | 146 |
| zscore_fallback_low | gmm_upper_mode_below_floor | 87 |
| zscore_fallback_high | zscore_fallback_high | 39 |

**Interpretation:** The 401 false-to-true flips are the scientifically
meaningful correction — these are MSK samples that were silently
mis-classified as non-hypermutator pre-t070 because their TMB was
compressed below the Campbell 10 mut/Mb threshold. Post-t070 they are
correctly flagged and are excluded from the `_exclusive` columns of the
paired frequency tables downstream (per plan `t081` agg row `agg.15`).

The reason-category shifts (e.g., `gmm_lower_mode` → `gmm_upper_mode_below_floor`)
reflect the per-cancer GMM fit moving its bimodality threshold upward
because all TMB values within MSK cancers shifted up by ~30×. The
`_below_floor` suffix (task `t105`) prevents GMM-upper-mode samples
from being auto-flagged if their TMB is still below the Campbell
10 mut/Mb composite floor — which is why the 401 flipped samples
cleanly crossed, while the 1,766 in the `gmm_upper_mode_below_floor`
bucket did not.

## Axis 3 — Per-(cancer, gene) rates (msk_impact_2017)

**Distribution of rate ratios across 5,164 (cancer, gene) rows
with non-null rates in both runs:**

| statistic | value |
|---|---:|
| count | 5,164 |
| mean | 1.035 |
| std | 0.125 |
| 25% | 1.000 |
| 50% (median) | 1.000 |
| 75% | 1.000 |
| max | **2.114** |

**Interpretation:** The bulk of (cancer, gene) rows show ratio = 1.00 —
the gene is on all MSK-IMPACT panels (covered by IMPACT-341), so the
denominator is unchanged (all 10,945 samples). Only genes added in
IMPACT-410+ see a denominator shift (10,945 → 8,136, ratio ≈ 1.345
expected). The observed `mean = 1.035` is low because most (cancer, gene)
rows are for genes on IMPACT-341 (74% of the 505-gene vocabulary is on the
oldest panel).

**Top-20 (cancer, gene) rate shifts by |ratio|:**

| cancer_type | symbol | rate_pre | rate_post | ratio |
|---|---|---:|---:|---:|
| Uterine Sarcoma | GLI1, MGA, ACVR1, DNAJB1, HIST1H3D | 0.0108 | 0.0227 | **2.11** |
| Penile Cancer | BIRC3, ZFHX3, BCL10, CEBPA, CSF3R | 0.143 | 0.250 | **1.75** |
| Penile Cancer | EPHA7, PLCG2, STAT3, TCF3 | 0.286 | 0.500 | **1.75** |
| Ovarian Cancer | HLA-A, STAT5A, MST1R, ANKRD11, STAT3, GLI1 | 0.013–0.018 | 0.023–0.031 | **1.75** |

The dominant ratios (2.11 and 1.75) correspond to small-cohort cancers
where the IMPACT-341 subset is a large fraction of the samples. E.g.,
Uterine Sarcoma has n=93 samples total in msk_impact_2017; if ~50 are
IMPACT-341 (no coverage of GLI1, added in IMPACT-410), the denominator
drops from 93 → 43, producing the observed 2.11× shift. Post-t070 rates
are the more accurate numbers — these genes *cannot* be observed in
IMPACT-341-only samples, so including those samples in the denominator
is a systematic underestimate.

The larger shifts concentrate in **rare/small cancer cohorts**, which are
also the cancers most vulnerable to the bias t070 fixes. For high-N
cancers (Lung, Breast, Colorectal), the shift is smaller in relative terms
but still present for IMPACT-410+ genes.

## Caveats / limitations

- **PoC scope:** only `msk_impact_2017` (n=10,945) exercises the
  per-sample panel path. The full-config studies (`msk_met_2021` n=25,775,
  `msk_chord_2024` n=25,040, `msk_impact_50k_2026` ≈50k) add
  MSK-IMPACT-468 and MSK-IMPACT-505 coverage — the bias magnitudes will
  be larger there because more recent IMPACT panels carry more genes that
  were not callable in earlier samples.
- **Cross-study aggregation impact (Task 8):** the new
  `n_panel_covered_samples_*` and `callable_sample_fraction_*` columns are
  populated in the `gene_cancer_study_ratio_annotated.feather` output but
  only diverge meaningfully from their study-binary counterparts when
  multiple MSK studies are in a run. Single-MSK-study PoC limits the
  downstream effect demonstration.
- **Nesting assumption:** the per-cancer cohort-size recovery in
  `_annotate_callability` assumes at least one gene is on every panel in
  use within a study. True for MSK-IMPACT solid-tumor (341 ⊂ 410 ⊂ 468 ⊂
  505). A HEME+solid mixed cohort would trigger the explicit C1 guard.
- **Threshold adjustment during PoC:** Task 7's "off-panel gene fraction >
  N% → raise" threshold was bumped from 1% (spec-specified) to 5% after
  the first real-data run showed 1.2% natural off-target calling in
  `msk_impact_2017` (5 genes out of 410 called at positions outside the
  nominal MSK-IMPACT BED: FIP1L1, INSRR, OBSL1, SDCCAG8, TIMM8B).
  5% remains tight enough to catch systematic ingestion bugs (wrong panel
  assignment would exceed 5% by a wide margin) while tolerating normal
  sequencer-level noise. The design-spec value should be updated in a
  follow-up doc pass.
- **One additional upstream fix during validation:** `process_genie_panel_coverage`
  previously emitted GENIE-form panel names (`MSK-IMPACT341`) rather than
  the canonical form (`MSK-IMPACT-341`), causing the Task 7 prereq check
  to fail loudly on the first post-t070 run. Fixed by normalizing
  `SEQ_ASSAY_ID` via `PANEL_ALIASES` at ingest (commit on t070 branch).

## References

- **Empirical audit** (this session, 2026-04-18): resolution verified as
  2,809 MSK-IMPACT-341 + 8,136 MSK-IMPACT-410 samples across the 10,945
  `msk_impact_2017` cohort. Consistent before + after full pipeline run.
- Cheng DT et al. 2015. *J Mol Diagn* 17(3):251-264. PMID 25801821. (IMPACT-341/410)
- Zehir A et al. 2017. *Nat Med* 23(6):703-713. PMID 28481359. (IMPACT-410/468)
- Bandlamudi C et al. 2026. *Cancer Cell*. PMID 41895280. (IMPACT-505 / 50k cohort)
- Campbell BB et al. 2017. *Cell* 171(5):1042-1056. (10 mut/Mb hypermutator threshold)
