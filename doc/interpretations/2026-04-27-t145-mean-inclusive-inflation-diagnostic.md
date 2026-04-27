# t145 Mean-Inclusive Inflation Diagnostic

Date: 2026-04-27

## Question

Task `t145` asked whether the raw-frequency `mean_inclusive` inflation in the
full pan-cancer t131 comparison was caused by the
`enforce_callability_nesting_check=false` t139 bypass, or by an upstream
aggregation issue.

## Finding

The primary root cause is upstream of the t139 bypass:
`create_combined_gene_cancer_freq_table.py` computed `mean_inclusive`,
`mean_exclusive`, and `mean` before `_fill_missing_unmutated_cells()` zero-filled
WES/unmapped study cells.

For sparse WES studies, a missing `(cancer_type, symbol)` row means
callable-but-unmutated when that cancer exists in the study cohort. The zero-fill
step correctly inserted per-study `0.0` ratios, but the pooled mean columns
remained stale. This let singleton small-study hits dominate the downstream
per-gene rollup used by `compare_three_way_rankings.py`.

Concrete reproduction from `/data/packages/cbioportal/pan-cancer`:

- Current persisted top rows include bladder-cancer genes with
  `mean_inclusive = 1.0`.
- For `Bladder Cancer / HTR2C`, the pooled input has one `1/1` hit in
  `pog570_bcgsc_2020` and four zero rows:
  `genie = 0/6188`, `metastatic_solid_tumors_mich_2017 = 0/16`,
  `mixed_allen_2018 = 0/27`, `pancan_pcawg_2020 = 0/23`.
- The correct per-cancer mean is therefore `0.2`, not `1.0`.

The nesting check does raise on the current pan-cancer inputs when enabled, but
that is not sufficient evidence that t139 caused the raw-ranking inflation. The
guard compares small real study/cancer cohorts against very large cohorts in the
same cancer type, so it flags many legitimate cross-study size differences. The
stale mean bug alone reproduces the exact t131 top-15 failure.

## Effect Of The Fix

After recomputing the mean columns after WES zero-fill, the original reported
top-15 genes drop sharply:

| gene | old mean | fixed mean | old raw rank | fixed raw rank |
|---|---:|---:|---:|---:|
| snoU13 | 0.837193 | 0.258146 | 1 | 10 |
| Y_RNA | 0.816680 | 0.250450 | 2 | 14 |
| LSAMP | 0.733374 | 0.249483 | 3 | 15 |
| MACROD2 | 0.724405 | 0.247350 | 4 | 17 |
| FHIT | 0.650182 | 0.223839 | 15 | 56 |

The recomputed top raw gene is `TP53` (`fixed_mean_inclusive = 0.316983`).
Bailey recovery in the raw top-100 improves from 0 to 1, but common-fragile-site
and long passenger genes remain prominent. That residual signal is no longer the
same 65-84% inflation artifact and should be handled as a separate methodology
question about the raw per-gene rollup.

## Fix Path

Implemented code path:

1. Recompute `mean_inclusive`, `mean_exclusive`, and legacy `mean` after
   `_fill_missing_unmutated_cells()`.
2. Move sort order and `mean_adj` calculation in the Snakemake path until after
   zero-fill, so length-adjusted output is based on the final mean.
3. Add a regression test where one `1/1` WES hit plus one zero-filled WES study
   must yield `mean_inclusive = 0.5`, not `1.0`.

Downstream outputs need regeneration from `create_combined_gene_cancer_freq_table`
forward for the existing pan-cancer feathers to reflect this fix.

## Follow-Up

Do not bump t139 solely from this evidence. The t139 guard still needs a separate
design review because its current cross-study size heuristic can flag legitimate
small WES cohorts. For publication-facing raw rankings, consider replacing the
per-cancer unweighted mean rollup with a pre-registered sample-weighted or
model-based per-gene summary.
