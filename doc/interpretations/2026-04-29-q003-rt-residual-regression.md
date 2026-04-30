---
id: "interpretation:2026-04-29-q003-rt-residual-regression"
title: "q003 RT residual regression — late-replication signal does not explain TTN; length adjustment moves TTN but the RT coefficient is null"
date: "2026-04-29"
related:
  - "task:t163"
  - "question:q003-replication-timing-as-gene-level-mutation-rate-confounder"
  - "hypothesis:h02-cross-study-ranking-divergence-is-structured"
  - "task:t131"
  - "task:t147"
  - "task:t153"
  - "interpretation:2026-04-26-t131-full-pan-cancer-dndscv-run"
  - "interpretation:2026-04-28-t146-external-validation-cgc"
prior_interpretations:
  - "2026-04-26-t131-full-pan-cancer-dndscv-run"
  - "2026-04-28-t146-external-validation-cgc"
---

# q003 RT Residual Regression

## Question

Task `t163` asks whether gene-level replication timing explains residual full-scale pan-cancer
dNdScv signal, especially TTN's persistence near the top of the post-t144 dNdScv ranking.

## Method

`code/scripts/analyze_rt_dndscv_residual.py` joins:

- `/data/packages/cbioportal/pan-cancer/summary/mut/table/three_way_ranking_comparison.feather`
- `data/gene_replication_timing.feather`

The primary signal is `dndscv_signal = -log10(max(min_qglobal, 1e-300))`, so q=0 genes are placed
at a finite ceiling of 300. The RT score is `rt_late_score = rt_cl_fraction - rt_ce_fraction`.
The fitted model is:

`dndscv_signal ~ rt_late_score + log10(protein_length)`

Outputs:

- `/data/packages/cbioportal/pan-cancer/summary/rt_residual/rt_dndscv_table.feather`
- `/data/packages/cbioportal/pan-cancer/summary/rt_residual/rt_model_summary.feather`
- `/data/packages/cbioportal/pan-cancer/summary/rt_residual/rt_bootstrap.feather`
- `/data/packages/cbioportal/pan-cancer/summary/rt_residual/ttn_rank_check.feather`

## Findings

### F1 -- The late-RT coefficient is near zero and the bootstrap CI crosses zero

Model summary over 18,591 fitted genes:

| Term | Estimate |
|---|---:|
| `beta_rt_late_score` | 0.111 |
| `beta_log_length` | 46.033 |
| R2 | 0.058 |

Bootstrap for `beta_rt_late_score` with 1,000 resamples:

| Mean | 2.5% | 97.5% |
|---:|---:|---:|
| 0.117 | -1.686 | 1.962 |

This is not evidence that constitutive late replication explains dNdScv residual signal at the
gene level.

### F2 -- Length is the dominant simple covariate

Rank correlations with `dndscv_signal`:

| Feature | Spearman rho |
|---|---:|
| `rt_late_score` | -0.004 |
| `log_length` | 0.564 |
| `n_cancers_significant_q05` | 0.680 |

The strong `log_length` association remains visible even after dNdScv's trinucleotide-context
model. That does not mean dNdScv failed wholesale; it means the pan-cancer q=0 floor and very long
genes still create residual ranking pressure.

### F3 -- TTN is not late-replication annotated in this RT map

TTN has:

| Raw dNdScv rank | RT/length-adjusted rank | RT label | RT late score |
|---:|---:|---|---:|
| 4 | 816 | `unassigned` | 0.0 |

So TTN's drop after RT/length adjustment is not evidence for a late-replication explanation. It is
mainly a length adjustment: TTN has `log10(length) = 4.536`, far above the canonical-driver core.

### F4 -- The RT map is sparse for constitutive late genes

The joined table has:

| RT label | n genes | median dNdScv signal |
|---|---:|---:|
| CE | 5,032 | 0.407 |
| CL | 445 | 0.509 |
| unassigned | 13,521 | 0.403 |

Only 445 genes receive a constitutive late (`CL`) assignment, and most top dNdScv genes are
`unassigned`. This makes the current gene-level RT map a weak instrument for explaining top-rank
driver residuals.

## Verdict

**Negative for q003 as a TTN explanation.** Constitutive late replication does not explain TTN's
top-rank persistence in the current full-scale dNdScv output. TTN is RT-unassigned, the
late-replication coefficient is near zero with a CI crossing zero, and the apparent TTN correction
comes from length rather than RT.

## Recommendation

Do not promote RT as the primary explanation for TTN at this point. The next diagnostic should be
`t147` hypermutator-stratified dNdScv, because hypermutated samples can inflate mutation counts
across the longest genes regardless of RT annotation. `t153` remains useful for separating common
fragile-site biology from generic length effects, but this result does not make RT itself a strong
correction channel.

## Caveats

- The q=0 floor forces many top genes to the same `dndscv_signal = 300`, so effect-size modeling is
  coarse at the top of the ranking.
- `data/gene_replication_timing.feather` uses conservative constitutive CE/CL overlap. Genes
  outside those bins are `unassigned`, not proven RT-neutral.
- The RT/length-adjusted rank is a diagnostic residual ranking, not a proposed production
  replacement for `rank_dndscv`.
