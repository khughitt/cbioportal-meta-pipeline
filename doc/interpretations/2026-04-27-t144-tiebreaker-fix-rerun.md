---
id: "interpretation:2026-04-27-t144-tiebreaker-fix-rerun"
type: "interpretation"
title: "t144 tiebreaker fix — Bailey driver recovery hits spec exactly; canonical drivers lift to top of rank_dndscv"
status: "active"
source_refs:
  - "interpretation:2026-04-26-t131-full-pan-cancer-dndscv-run"
related:
  - "task:t144"
  - "task:t131"
  - "task:t145"
  - "task:t147"
  - "task:t148"
created: "2026-04-27"
updated: "2026-04-27"
input: "/data/packages/cbioportal/pan-cancer/summary/mut/table/three_way_ranking_comparison.feather"
workflow_run: "config-pan-cancer-dndscv 2026-04-27T07:55 (cheap rules only — aggregate_dndscv_per_gene + join_dndscv_into_annotated + compare_three_way_rankings)"
---

# Interpretation: t144 tiebreaker fix re-run

## Verdict

**[+] Confirmed.** The lexicographic-sort fix lands the exact Bailey driver recovery numbers stated in the t144 spec, and lifts canonical drivers (TP53/KRAS/NRAS/PIK3CA/RB1/PTEN/FBXW7) from their previous alphabetically-arbitrary positions to ranks 1–7 of `rank_dndscv`. No dNdScv re-compute was required — only the three downstream summary rules ran (~25 s wall time).

## Findings

### F1 — Bailey driver recovery matches spec exactly

| K | OLD | NEW | Spec |
|---|---:|---:|---:|
| 10 | 2 | **8** | 8 |
| 25 | 5 | **22** | 22 |
| 50 | 17 | **37** | 37 |
| 100 | 29 | **62** | 62 |
| 500 | 104 | **145** | 145 |

(`bailey_driver` is the `bailey2018_driver` overlay rolled up to per-gene by `_per_gene_rollup` in `compare_three_way_rankings.py`.)

### F2 — Canonical drivers occupy ranks 1–7

`rank_dndscv` top-15 (NEW): TP53(1), KRAS(2), NRAS(3), PIK3CA(4), TTN(4), FBXW7(5), KMT2D(5), PTEN(5), RB1(5), TET2(5), ARID1A(6), ARID2(6), DNMT3A(6), BRAF(7), SETD2(8). Old top-15 was the alphabetical-A bucket (AATK / ABCA13 / ABCA2 / ABCA7 / ABCB11 / ABL1 / ACACB / ACTG1 / ACVR1 / ACVR1B / AGO2 / AGRN / AHNAK / AHNAK2 / AKAP13).

The acceptance criterion — `rank_dndscv == 1` held by the gene with the highest `n_cancers_significant_q05` among the q=0 set — is met: TP53 holds rank 1 with `n_cancers_significant_q05 = 64`.

### F3 — Residual issues (out of scope for t144)

Three concerns visible in the new artifact remain governed by other tasks:

- **`best_cancer_type` still alphabetical.** Top entries report Ampullary / Anal / Appendiceal / Bladder for TP53/KRAS/NRAS/etc. The single-cancer field is information-lossy when many cancers tie at q=0 — replacement with a multi-cancer set field is `t148`.
- **TTN at rank 4** despite dNdScv's trinucleotide-context correction. Leading hypothesis: hypermutated cohorts (POLE/POLD1/MSI-H) inflate per-gene counts at the longest genes — `t147` will re-run with `is_hypermutator == False` filter.
- **Raw `mean_inclusive` ranking unchanged** (snoU13/Y_RNA/CFS-genes still dominate). The t144 fix only touched the dNdScv rank; the pooled-meta inflation is `t145`.

## Recommended Next Actions

| Priority | Action | Rationale |
|---|---|---|
| P1 | Execute `t145` diagnostic — re-run meta-analysis on 3-5 cancers with `enforce_callability_nesting_check=true` | dNdScv side now sound; raw-frequency side is the remaining headline-blocking issue |
| P2 | Land `t141` (R `mclapply`) before any `t147` re-run | The `t147` hypermutator-stratified dNdScv re-run depends on per-cancer dNdScv re-computation, not the cheap summary rules — and meta-analysis at 12+ hr serial is the binding constraint |
| P2 | `t148` `best_cancer_type` → multi-cancer field | Surfaces straight from this run (Ampullary/Anal/Appendiceal artifacts visible in the top-15) |

## Provenance

- **Code**: commit `8d4776c` `fix(t144): break q=0 ties in dNdScv per-gene rollup by n_cancers_significant_q05`.
- **Backup**: `dndscv_pooled.pre-t144.feather`, `gene_cancer_study_ratio_annotated_dndscv.pre-t144.feather`, `three_way_ranking_comparison.pre-t144.feather` retained alongside the new outputs for future bisection.
- **Re-run command**:
  ```bash
  uv run snakemake -s code/workflows/Snakefile \
    --configfile code/config/config-pan-cancer-dndscv.yml \
    --config out_dir=/data/packages/cbioportal/pan-cancer \
    --rerun-triggers mtime -j1 \
    --forcerun aggregate_dndscv_per_gene join_dndscv_into_annotated compare_three_way_rankings \
    -- /data/packages/cbioportal/pan-cancer/summary/mut/table/{dndscv_pooled,gene_cancer_study_ratio_annotated_dndscv,three_way_ranking_comparison}.feather
  ```
