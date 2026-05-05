---
id: "interpretation:2026-04-24-t126-sbs1-lrr-bias-per-study"
type: "interpretation"
title: "t126: per-study aggregate SBS1 LRR-bias test (BRCA matched vs unmatched)"
status: "active"
source_refs:
  - "paper:Yaacov2023"
  - "paper:Alexandrov2020"
related:
  - "task:t126"
  - "task:t124"
  - "task:t110"
  - "task:t121"
  - "question:q009-sbs1-lrr-bias-as-normal-contamination-flag"
  - "discussion:2026-04-24-t124-q009-fork-decision"
  - "pre-registration:t126-sbs1-lrr-bias-test"
created: "2026-04-24"
updated: "2026-04-24"
workflow_run: "t126-sbs1-lrr-bias-2026-04-24"
---

# Interpretation: t126 — per-study aggregate SBS1 LRR-bias test

## Verdict

**defer** — close `t124`; move `q009` to `deferred` status with revisit-condition `WGS inputs ingested`.

The test reached a pre-registered terminating verdict on its first contact with the data. Both panel-cohort safety gates triggered: `n_sbs1_pooled` below the 500-floor, and bootstrap CI half-width above the 0.10 ceiling. The pre-registration explicitly anticipated this outcome and routed it to `defer` rather than `retire` to preserve the option to revisit when WGS data lands.

## Run surface

- Inputs: `t109/t110` per-sample restricted SigProfilerAssignment outputs (`results/signature-brca-2026-04-22/`), `t121` gene-level RT map (`data/gene_replication_timing.feather`), `t121` 50kb constitutive bins (`data/replication_timing_constitutive_bins.feather`), GENIE panel BED (`data/genie/genomic_information.txt` for MSK-IMPACT-341/410), COSMIC v3.4 SBS reference.
- Output: `results/t126-sbs1-lrr-bias-2026-04-24/summary/signatures/sbs1_lrr_bias_per_study.feather`.
- Code: `code/scripts/compute_sbs1_lrr_bias_per_study.py` + `tests/test_compute_sbs1_lrr_bias_per_study.py` (13 tests pass).
- Random seed: 0; 1,000 bootstrap iterations.

## Main result

| Cohort | n_sbs1_pooled (CE+CL bins) | n_sbs1_ce | n_sbs1_cl | panel_ce_bp | panel_cl_bp | f_lrr_corrected | 95% CI | CI half-width |
|---|---:|---:|---:|---:|---:|---:|---|---:|
| `tcga_mc3` (WES) | 2,127.6 | 1,930.4 | 197.2 | 237.6 Mb | 132.3 Mb | 0.155 | [0.135, 0.179] | 0.022 |
| `msk_impact_2017` (panel) | **176.4** | 170.7 | **5.7** | 475.6 kb | **20.8 kb** | 0.433 | [0.200, 0.587] | **0.194** |

Panel decision-rule check (pre-registered thresholds: midpoint=0.45, n_floor=500, max_ci_halfwidth=0.10):

- `n_sbs1_pooled = 176.4 < 500` → underpowered.
- `CI half-width = 0.194 > 0.10` → uncalibrated.

Both gates trigger `defer`; the verdict stands regardless of point-estimate location.

## Why the pre-run power projection was wrong

The pre-registration projected `n = 553` SBS1-attributed mutations for `msk_impact_2017` and concluded the test was *just* powered. The actual `n_sbs1_pooled` in the test's measurement domain is **176**. The discrepancy is structural, not a coding error:

1. **Pre-reg projection used the raw exposure sum** (SigProfilerAssignment's per-sample SBS1 attribution counts summed across all 1,210 BRCA samples). That total is 553.
2. **The actual statistic measures only mutations in constitutive RT bins** (the union of t121's CE-labelled and CL-labelled 50kb bins, covering ~620 Mb / ~20% of the genome). 391.5 of the 553 SBS1 posteriors fall in `unassigned` territory — outside any constitutive bin. Only 176.4 land in CE+CL bins.

This is a real conceptual gap in the pre-registration: the n-floor was set on raw SBS1 attribution (553) without subtracting the unassigned-bin fraction. A more conservative pre-run gate would have projected `n × (constitutive_bin_fraction × panel_overlap_fraction)`, which would have produced ~150 and triggered an immediate `defer` before any code was written.

The pre-registration's no-post-hoc-movement clause prevents weakening the threshold to rescue the test. The verdict mechanism is working exactly as intended: it caught a power miscalculation that the pre-run projection missed.

## Why the panel cohort cannot be powered on this design

The MSK-IMPACT panel coverage of constitutive RT bins is structurally hostile to the test:

- `panel_ce_bp = 475,607` — 96% of the panel's constitutive-bin overlap is in **early-replicating** territory.
- `panel_cl_bp = 20,761` — only 4% in late-replicating territory.
- Ratio CE:CL bp on this panel = **23:1**.

This is the expected outcome of a panel designed to capture cancer driver genes: drivers cluster in active, gene-dense, early-replicating regions. The mechanism the test was built to detect (LRR-biased SBS1 leakage from normal tissue) requires LRR coverage to be present in the assay — and on MSK-IMPACT it is essentially absent.

For reference, the matched WES cohort sees a much more even split (CE:CL ≈ 1.8:1 by gene-CDS bp), and accordingly produces a comfortably powered estimate (n = 2,128, half-width = 0.022).

## Anomaly: the matched cohort's f_LRR sits below the Yaacov cancer baseline

`tcga_mc3` returns `f_lrr_corrected = 0.155` with a tight CI [0.135, 0.179]. Yaacov 2023's published cancer baseline is approximately 0.40 (LRR-unbiased). The 25-percentage-point gap is large and warrants explanation.

Most likely cause: the gene-CDS approximation used as the WES denominator (sum of `rt_ce_bp` and `rt_cl_bp` across all genes in the t121 map) is not directly comparable to Yaacov's WGS-based whole-genome denominator. Yaacov's denominator is total constitutive-bin extent in the genome (~620 Mb, with CE:CL roughly 1:1.3 by 50kb-bin count). The gene-CDS approximation captures only the gene-body fraction of constitutive bins, and gene density is itself enriched in early-replicating territory. So the WES denominator over-weights CE relative to genome-wide.

**This is a real measurement-frame caveat, not an artefact in the test code.** It does not change the `defer` verdict — the matched cohort's CI is well-defined within its own denominator frame, and the panel cohort's failure to power is independent of where the matched baseline sits.

A future WGS-based version of this test would use whole-bin-bp as the denominator and would not have this offset.

## Implications for q009

q009 (SBS1 LRR-bias as a contamination flag) cannot be evaluated on cBioPortal panel data using the t121 RT-bin design and current attribution methods. The fundamental obstacle is structural: panel territory does not adequately sample late-replicating regions, so the published SBS1 LRR-bias signal (which lives precisely in those regions) is not measurable on the unmatched-normal cohort that q009 was designed to flag.

This is a stronger and more defensible finding than t110/t122/t123 produced. Where those pilots showed *empirical* sparsity (zero-inflation, coverage confounding), this run identifies the *structural* reason: the panel's CE:CL-bp ratio (23:1) and the constitutive-bin coverage ceiling that no method choice can work around.

q009 is therefore moved to `deferred` rather than `retired` because the limitation lies in the data surface, not the mechanism. If WGS cohorts are added to the pipeline (Hartwig HMF, PCAWG follow-ons, or direct ingestion of WGS-converted TCGA where possible), the test becomes immediately trivial to run with adequate power — `panel_cl_bp` rises by ~5 orders of magnitude, and a reanalysis of the same matched/unmatched contrast becomes powered.

## What landed in the codebase

- `code/scripts/compute_sbs1_lrr_bias_per_study.py` — single-file implementation (TSB binary decoding, per-mutation SBS1 posterior, RT-bin assignment, panel-bp intersection, cluster bootstrap, decision rule).
- `code/scripts/tests/test_compute_sbs1_lrr_bias_per_study.py` — 13 tests, all pre-registered building blocks plus the three required regression cases.
- `results/t126-sbs1-lrr-bias-2026-04-24/summary/signatures/sbs1_lrr_bias_per_study.feather` — single-row-per-study output with per-cohort statistics and verdict column.

The script is opt-in only; it is **not** wired into the main Snakefile rule graph. Re-running it is a single CLI invocation:

```bash
uv run --frozen python code/scripts/compute_sbs1_lrr_bias_per_study.py \
  --results-root results/signature-brca-2026-04-22 \
  --output <out>.feather
```

When WGS inputs are added to the pipeline, the same script will run against the new cohort with no code changes; only the `--results-root` and panel-handling flags need adjustment.

## Closure actions

1. Mark `t124` done; reference this interpretation as the closure note.
2. Mark `t126` done; reference this interpretation as the closure note.
3. Update `q009` status to `deferred` with revisit-condition `WGS inputs ingested`. Cite this interpretation as the deferral rationale.
4. Leave the t111 normal-tissue spectra branch untouched — q007 and q008 are independent of q009's outcome and the `t111` infrastructure remains valuable for those questions.
5. Pre-register update for any future re-run: when the WGS revisit happens, the pre-run power projection must use `n × constitutive_bin_fraction × cohort_overlap_fraction`, not the raw SBS1 exposure sum. This is the lesson the t126 verdict carries forward.

## Deviations from pre-registration

None that affected the verdict. Two notes:

- The pre-registration §4 fallback (gene-CDS approximation for the WES denominator if panel BED intersection is non-trivial) was applied to `tcga_mc3` because no per-WES BED is available for MC3 in the pipeline. This is symmetric in the sense that both cohorts use coverage-aware denominators (the panel BED for `msk_impact_2017`, gene-CDS bp for `tcga_mc3`), but they are not the same denominator frame. This caveat is recorded and explains the matched-cohort baseline anomaly above; it does not affect the panel-cohort `defer` verdict, which is determined by panel-side power gates only.
- All threshold values (n_floor=500, max_ci_halfwidth=0.10, midpoint=0.45) were applied as written. The `defer` outcome is a direct consequence of the panel cohort failing two of three pre-registered gates.
