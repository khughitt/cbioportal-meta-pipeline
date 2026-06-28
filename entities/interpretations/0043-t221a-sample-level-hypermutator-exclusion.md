---
type: interpretation
title: "t221(a): the full-WES neural-gene residual is NOT a hypermutator artifact\
  \ \u2014 a sample-level exclusion across all 91 WES studies (326 hypermutator samples,\
  \ 1.15M variant rows dropped) leaves the genomic-span residual exactly where it\
  \ was (span-matched p 0.002 -> 0.002)"
status: active
created: '2026-06-08'
updated: '2026-06-08'
id: interpretation:0043-t221a-sample-level-hypermutator-exclusion
related:
- hypothesis:0012-neural-gene-enrichment-length-histology-artifact
- question:0032-neural-gene-length-null
- interpretation:0041-t217-genomic-span-cfs-null
- interpretation:0042-t218-cns-exclusion-wes-panel
- task:t221
---

# Interpretation: t221(a) — full-config sample-level hypermutator exclusion

> **Verdict: the significant full-WES candidate residual is NOT a hypermutator / TMB sample-composition
> artifact.** Re-aggregating candidate variant counts across all 91 WES/WGS-class `full` studies straight
> from the per-study `mut_filtered.feather`, then dropping every variant row contributed by an
> `is_hypermutator` sample (326 hypermutator samples in 23/91 studies; 1,150,599 rows removed), leaves the
> t217 genomic-span-matched residual **exactly** where it was: candidate median percentile 0.250 → 0.236,
> span-matched p **0.002 → 0.002**, span + late-replication-class p **0.0004 → 0.0004**. Only **0.4–1.9 %**
> of each candidate's rows are dropped. This closes the one hypermutator control t218 explicitly deferred —
> at the sample level across the whole WES cohort, not just the driver cohort.

- **Task:** `t221`, arm (a) (QA / sanity battery for the neural-gene program — the sample-level
  hypermutator control).
- **Script:** `code/notebooks/t221a_sample_level_hypermutator_exclusion.py`
- **Artifacts:** `results/neural-gene-hypermutator-2026-06-08/` — `enrichment_inclusive_vs_exclusive.tsv`,
  `candidate_rows_inclusive_vs_exclusive.tsv`, `per_study_hypermutator_burden.tsv`, datapackage.json.
- **Substrate:** `full` config. Wide `gene_cancer_study.feather` (variant-row counts) for the WES study
  set and the validation target; per-study `mut_filtered.feather` for the re-aggregation;
  `metadata/samples_annotated.feather` for `is_hypermutator`; genomic span from
  `data/gene_replication_timing.feather`. `random_seed = 0`, 5,000 null draws.

## Why this run was needed

t218 found the t217 genomic-span residual lives in the WES/WGS-class studies (`full` span-matched
p ≈ 0.0022) and is driven by one cohort (`pog570_bcgsc_2020`). Its hypermutator evidence, however, was
**driver-cohort-specific** — pog570 carries 0/570 hypermutators — and its only *aggregate* hypermutator
arm tested an already-non-significant pan-cancer arm. So the question *"does the **significant** full-WES
residual survive removing hypermutator samples?"* was never answered at the sample level across all 91 WES
studies. t221(a) answers it directly.

## Implementation note (the load-bearing part)

The wide `gene_cancer_study.feather` count that t217/t218 operate on is a **variant-row count** per
(cancer_type, symbol, study) — verified empirically (pog570 NKAIN2 = 4806 wide-table count = 4806 variant
rows, not the 482 distinct mutated samples) — and there are **no `_exclusive` twins for `full`**. So the
exclusion cannot read a column; it re-reads each WES study's per-variant table and drops the rows from
`is_hypermutator` samples. Two correctness guards make the exclusive arm trustworthy:

1. **Exact self-check.** Because the wide per-study column *is* the per-study variant-row count, the
   re-aggregated **inclusive** total must reproduce `gene_totals(wide, wes_cols)` gene-for-gene. It does:
   21,167 / 21,169 genes exact; the only residue is **IQCA1 / IQCD off by 2 rows each** (4 rows in one
   study, `prad_tcga_pan_can_atlas_2018`) from a symbol-aliasing edge between the wide-table build and the
   raw tables — **all 9 candidates reproduce exactly**, and the inclusive arm reproduces t218 `wes_only`
   (p = 0.0022) exactly. The self-check tolerates only a few non-candidate genes off by ≤ a few rows and
   **hard-fails** on any candidate mismatch or material discrepancy.
2. **Join-coverage guard.** `sample_id_tumor` is int64 in some studies (e.g. pog570) and str in others,
   while `samples_annotated` keys on str; both sides are cast to str so the hypermutator join cannot
   silently no-op, and any study with < 95 % of mut samples matched to the flag table is surfaced loudly.
   All 91 WES studies joined at 100 %.

## Findings

**F1 — Sample-level hypermutator exclusion does not move the residual.** Across the 91 WES studies:

| arm | candidate median pct | n in top-100 | span-matched p | span + late-CL-class p |
|---|---|---|---|---|
| inclusive (all samples) | 0.250 | 6 | **0.002** | 0.0004 |
| exclusive (hypermutators dropped) | 0.236 | 6 | **0.002** | 0.0004 |

The residual is unchanged. Removing hypermutators is inert for these genes.

**F2 — Hypermutators contribute mass genome-wide, but not preferentially to the candidates.** 326
hypermutator samples in 23/91 WES studies account for **1,150,599** dropped variant rows
(candidate-universe), heavily concentrated in MSI/POLE-rich cohorts — `ucec_tcga_pan_can_atlas_2018` alone
sheds 518,203 rows (56 % of its rows), `coadread_dfci_2016` 175,809. Yet each **candidate** loses only
**0.4–1.9 %** of its rows (RIT2 1.9 %, LSAMP 0.4 %). Hypermutators dump enormous coding/genome-wide mass
that is *not* aimed at these large late-replicating loci, so excluding them barely touches the candidate
percentile. The candidates' rows come from the all-region `pog570` cohort (0 hypermutators, t218) and
diffusely from non-hypermutator samples elsewhere — passenger accumulation scaling with genomic span, not
TMB sample composition.

## Bearing on `hypothesis:0012`

This removes the last alternative the candidate-set mutational-count thread had left open. The full-WES
residual identified by t218 is **not** explained by hypermutator/TMB sample composition — at the sample
level, across the entire 91-study WES cohort, not merely the driver cohort. Combined with t217
(genomic-span null dissolves it; coding-length null fails; dndscv 0/9), t216 (a neural score cannot beat a
size-matched CFS control), and t218 (not CNS, not panel ascertainment; one all-region cohort tiling the
loci), every non-span explanation for the candidate enrichment has now been tested and rejected. As with
t218, this is recorded as strong supporting evidence for the **candidate-set mutational-count thread** of
`hypothesis:0012`; the project entities `hypothesis:0012` (proposed) and `question:0032` (active) are left in their
prior states — one thread does not by itself flip the hypothesis.

## Decision & redirect

1. **t221 arm (a) is complete and negative** — hypermutators ruled out at the sample level. The remaining
   t221 work is **arm (b)**, the standing-controls panel: per-study call-set region scope
   (intronic-fraction) as a first-class covariate, a CFS positive-control gene panel the candidates should
   track, matched- vs unmatched-normal stratification (germline-leak), and data-driven-set
   (`gene_neural_enrichment`) vs hand-labelled-set sensitivity.
2. **Promote `is_hypermutator` exclusion from "open control" to "tested and inert"** for this gene class in
   any downstream neural-gene QA — it need not be re-run per analysis.
3. **Keep the per-study hypermutator-burden map** (`per_study_hypermutator_burden.tsv`) as a reusable QA
   reference: it is a clean census of where hypermutator mass sits across the WES cohort.

## Caveats

- **Variant-row substrate.** The metric is variant rows (the t217/t218 substrate), the quantity in which
  the genomic-span confound lives; the sample-level *ratio* tables (num/n_samples) are a separate view and
  are not what this residual is about.
- **Unknown hypermutator status treated as non-hypermutator.** Mirrors `create_freq_tables` (left-merge +
  fill False); all 91 WES studies matched at 100 % join coverage, so this affects no rows here.
- **Two-gene self-check residue.** IQCA1 / IQCD differ by 4 rows total in one study from symbol aliasing in
  the canonical wide-table build (pre-dates t221); immaterial and on non-candidate genes.
- **`full` only.** Arm (a) targets the powered residual; the pan-cancer WES arm is underpowered (t218,
  n = 7) and not re-run here.
