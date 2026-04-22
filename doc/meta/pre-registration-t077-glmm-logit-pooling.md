---
id: "meta:pre-registration-t077-glmm-logit-pooling"
type: "pre-registration"
title: "Pre-registration: GLMM-logit random-effects pooling for per-(gene, cancer) mutation rates (t077)"
status: "active"
related:
  - "task:t077"
  - "task:t079"
  - "task:bias-audit-cross-study-aggregation-pipeline"
  - "topic:cross-study-meta-analysis-cancer-genomics"
  - "search:2026-04-13-cross-study-meta-analysis-stats"
  - "paper:DerSimonian1986"
  - "paper:Viechtbauer2010"
  - "paper:Langan2018"
  - "paper:Stijnen2010"
  - "paper:LinXu2020"
  - "paper:Nyaga2014"
  - "paper:Higgins2002"
  - "paper:IntHout2016"
created: "2026-04-14"
updated: "2026-04-14"
---

# Pre-registration: GLMM-logit random-effects pooling for per-(gene, cancer) mutation rates

## Hypotheses Under Test

- **H1** (primary, confirmatory — from `specs/research-question.md`):
  *Aggregating somatic mutation evidence across heterogeneous cBioPortal studies reveals
  gene-cancer associations that are more robust and more generalizable than any single
  study, and exposes clusters of cancer types with shared mutational structure.*
- **G1** (methodological gate, confirmatory): GLMM-logit random-intercept meta-analysis
  converges on the majority of (gene, cancer) cells in our cohort, yielding stable
  between-study variance estimates that credibly expose panel- and cohort-effect
  heterogeneity. G1 is a prerequisite gate — if G1 fails, H1's evidence is not
  evaluable and the method has to be revised before re-registering.

## Analysis Under Pre-Registration

### Model

For each (gene g, cancer c) cell, fit a **binomial-logit generalized linear mixed model
with random study intercept** on the per-(study) counts:

```
y_{g,c,s} ~ Binomial(n_{c,s}, p_{g,c,s})
logit(p_{g,c,s}) = β_{g,c} + γ · x_s + u_s
u_s ~ N(0, τ²_{g,c})
```

- `y_{g,c,s}`: number of samples in study s with ≥1 non-synonymous coding mutation in
  gene g within cancer type c.
- `n_{c,s}`: total samples in study s of cancer type c that passed pipeline QC.
- `β_{g,c}`: per-(gene, cancer) fixed effect — the pooled log-odds of mutation.
- `x_s`: per-study covariate vector (see below).
- `u_s`: study random intercept; `τ²` is the between-study variance at this cell.
- `γ`: covariate coefficients (shared across g for computational tractability; revisited
  if G1 fails on convergence).

Implemented via `metafor::rma.glmm(measure="PLO", ...)` in R (see *Environment* below).

### Study-level covariates in the fixed part

| Covariate | Type | Source |
|---|---|---|
| `panel_class` | factor: {large_hybrid_capture, small_amplicon, WES, MC3} | per-study metadata; MC3 is Ellrott 2018 |
| `matched_normal` | bool | per-study metadata; populated by t050 / `annotate_ch.py` |

**Deferred**: `cohort_stage` (primary / metastatic / mixed) depends on task `t052` which
is not done. Running a **sensitivity re-fit** with `cohort_stage` added is pre-registered
as an exploratory analysis once t052 lands. Baseline confirmatory fit runs without it.

### Cell-filtering thresholds (before fitting)

A (gene, cancer) cell enters the pooled fit if **all** of:

1. `n_studies_contributing ≥ 3` (at least three studies report any sample for cancer c
   with gene g callable; see t073).
2. `sum(n_{c,s}) ≥ 200` across contributing studies.
3. `sum(y_{g,c,s}) ≥ 1` (at least one mutation observed somewhere). Cells with zero
   mutations across all contributing studies are kept *only* if all three conditions
   above hold — they then receive a pooled estimate consistent with the zero-event
   likelihood. Cells failing any condition emit `NaN` + a `status` column documenting
   which threshold failed.

**Callable denominator**: when per-(study, gene) callability from t026 / `process_genie_
panel_coverage.py` is available, `n_{c,s}` uses "samples in cancer c of study s for which
gene g is callable". Where callability is unknown, `n_{c,s}` is the full QC-passing
sample count (which biases pooled rates downward for genes with patchy panel coverage —
documented limitation).

### Outputs

For each pooled cell, emit:

- `pooled_logit` (β̂_{g,c}) + back-transformed `pooled_rate`
- `pooled_ci_lo`, `pooled_ci_hi` (95% CI, HKSJ-adjusted when K < 30 per Langan 2018 +
  IntHout 2016)
- `tau2` (between-study variance estimate)
- `i2` (Higgins & Thompson 2002)
- `pi_lo`, `pi_hi` (95% prediction interval per IntHout 2016)
- `k_studies` (contributing studies after filter)
- `n_total` (summed n across contributing studies)
- `y_total` (summed y)
- `converged` (bool)
- `status` (enum: ok / skipped_k / skipped_n / skipped_y / nonconverged)

Written to `gene_cancer_pooled.feather` (joined into `gene_cancer_study_ratio_annotated.
feather` downstream as a consumer-facing annotation).

### Alternatives considered and rejected

| Alternative | Rejected because |
|---|---|
| **DerSimonian-Laird (DL)** on log-OR with a reference rate | Continuity-transforms sparse cells (most gene × cancer × study cells have 0-5 mutations); Langan 2018 shows DL is inferior to REML and to GLMM for small studies / rare events; requires choosing an arbitrary reference rate. |
| **Mantel-Haenszel** | Does not naturally accept per-study covariates (panel_class, matched_normal). Our data are heterogeneous on axes that M-H cannot model. |
| **Fixed-effects (inverse-variance)** | Assumes no between-study heterogeneity. The bias audit (`task:bias-audit-cross-study-aggregation-pipeline`) documents four separate sources of between-study heterogeneity (panel, matched-normal, cohort-stage, annotation drift); fixed-effects pooling would be systematically mis-specified. |
| **Freeman-Tukey double-arcsine** (Barendregt 2013) | Lin & Xu 2020 explicitly deprecates arcsine for proportion meta-analysis in favor of GLMM-logit when cells are sparse; back-transform is non-unique; transform assumptions fail for very rare events. |
| **Bayesian hierarchical model** (brms-style) | Equivalent modeling framework, pragmatically rejected for this round: (a) fit time ~orders of magnitude slower at the ~15k-cell scale; (b) no established metafor-equivalent package; (c) hyperprior choice would require its own pre-registration. Registered as a possible future comparator if GLMM-logit fails G1. |

### Environment (reproducibility)

Per user preference, the GLMM-logit rule runs in an **isolated conda environment** wired
into Snakemake, not the system R:

- Add `code/envs/r-meta.yml` listing: `r-base>=4.3`, `r-metafor`, `r-arrow`,
  `r-optparse`, `r-matrix`, `r-lme4` (dependency of rma.glmm).
- Pin the env hash into `datapackage.json` at run time.
- Invoke snakemake with `--use-conda --conda-frontend mamba` (micromamba works as the
  drop-in frontend; full conda / mambaforge also work).
- Pipeline rule declaration: `conda: "../envs/r-meta.yml"`.

Docker is the acceptable alternative if conda resolution becomes slow on the full
package set; in that case pin a specific image tag and reference via
`container: "docker://rocker/r-ver:4.3.2"` + `--software-deployment-method apptainer`.

The existing `run_dndscv.R` rule is currently not wired into an isolated env — a
**backfill task** to do the same for `run_dndscv.R` should follow this work (tracked
separately; out of scope here).

## Expected Outcomes

**If H1 holds** and the model is correctly specified:

- **Distribution of I²**: right-skewed across cells, with a long tail of high-I²
  (`> 75%`) cells concentrated in gene × cancer combinations where panel content or
  matched-normal status plausibly drives the signal (e.g., CH-priority genes in mixed
  tumor-only/matched cohorts; small-amplicon-only genes across panels). Median I²
  between 25-60% across the core cell set.
- **Per-(gene, cancer) rank stability**: Spearman correlation between pooled rank and
  per-study median rank ≥ 0.70 across the top-quartile-signal cells, with higher
  correlation in low-I² cells.
- **Pooled CIs narrower than any single-study CI** for the cells with high `k_studies`;
  tightening proportional to the square root of `k` in the low-heterogeneity regime.
- **Convergence**: G1 passes if ≥ 90% of filtered cells converge. Between 75-90% triggers
  a convergence-diagnostic review but the confirmatory analysis proceeds on the
  converged subset. Below 75% triggers falling back to REML-logit with HKSJ (Langan 2018
  recommendation) as a pre-registered escape hatch, re-running under the same decision
  criteria.

**Why these expectations**:

- Panel and matched-normal heterogeneity across our ingested cohort (MSK-IMPACT,
  GENIE 91-panel, FoundationOne fragments, TCGA MC3) is documented in
  `topic:targeted-panel-sequencing-bias` and `topic:cross-panel-normalization-methods` —
  high I² in the affected cells is the biologically informed prior.
- GLMM-logit is well-behaved on sparse counts per Stijnen 2010 and Nyaga 2014; we do not
  expect convergence issues in the majority of cells with `y_total ≥ 1`.
- Rank stability (pooled vs per-study) is the concrete H1 test — Samstein 2019 shows
  small panels still give usable gene-level rankings, so pooled rank should track per-
  study rank in low-heterogeneity cells.

## Decision Criteria

### H1 — Primary hypothesis

| Evidence | Threshold | Decision |
|---|---|---|
| **Support H1** | In the top-quartile-signal cells (by pooled rate): ≥ 70% have `i2 < 75%`, AND pooled-vs-per-study rank Spearman ρ ≥ 0.70, AND pooled CIs narrower than the single-study median CI by ≥ 30% on average. | Aggregation *is* gaining us robustness over single-study. Report pooled tables as primary outputs. |
| **Weaken H1** | Top-quartile cells have 40-70% I² > 75%, OR rank ρ falls to 0.40-0.70, OR CI tightening is 10-30%. | Aggregation partially works but heterogeneity or cohort composition dominates in a meaningful minority of cells. Report pooled outputs but flag high-I² cells separately; run per-stratum (panel_class × matched_normal) pooled analyses as confirmatory follow-ups. |
| **Refute H1** | ≥ 70% of top-quartile cells have I² > 75%, AND rank ρ < 0.40, AND pooled CIs not meaningfully narrower than single-study CIs. | Cross-study aggregation does not recover shared biology at our current panel / cohort composition. Document as a null result against H1 and pivot: either restrict to panel-matched sub-cohorts (MSK-IMPACT only, or TCGA MC3 only) or adopt a stratified pooling design (pool within panel_class, report per-stratum). |

### G1 — Methodological convergence gate

| Convergence rate | Decision |
|---|---|
| ≥ 90% of filtered cells converge | Proceed with confirmatory H1 evaluation on all converged cells. |
| 75-90% | Diagnose the non-converged cell subset (typically very-rare-event cells with `y_total < 5`). If non-convergence is concentrated in those, report H1 on the converged set with explicit caveat for rare-event cells. |
| < 75% | Fall back to REML-logit + HKSJ via `metafor::rma(measure="PLO", method="REML")` as a pre-registered escape hatch. Re-evaluate H1 against the same criteria. |

## Null Result Plan

**A null pooled effect at an individual (gene, cancer) cell** is scientifically
meaningful, not a problem: it means the gene is not preferentially mutated in that
cancer type across studies. Distinguish between:

- **True biological null** — low pooled rate with low I² (the gene really isn't mutated
  there; pooled estimate is a precise zero).
- **Heterogeneity-swamped null** — wide pooled CI with high I² (we cannot conclude
  anything because study-level variation overwhelms any biological signal).
- **Callability-masked null** — `k_studies < 3` after callability filter (the gene is
  simply not on enough panels). Emit `status = skipped_k`.

The three cases must be disambiguated in the output schema — `status`, `i2`, and
`k_studies` together are sufficient.

**An aggregate null against H1** (the "refute" row above) would mean panel + cohort
heterogeneity dominates biological signal at our current data scale. Next step in that
case is *not* "give up" but "switch to stratified pooling" — pool within
(`panel_class`, `matched_normal`) strata, accept the resulting smaller per-stratum
sample sizes, and report per-stratum.

## Suspicious/Unexpected Result Plan

**Too-good-to-be-true indicators** for this analysis:

| Indicator | Threshold | Suspected inflator |
|---|---|---|
| **Uniformly low I²** | ≥ 80% of cells have I² < 25% | Implausible given documented panel/cohort heterogeneity. Likely causes: (a) `n_{c,s}` denominator bug (all studies treated as if they have same callable length); (b) covariate mis-specification absorbing real heterogeneity into the fixed effect; (c) pipeline silently filtered down to a panel-homogeneous subset. |
| **Pooled rate >> per-study rates** | Pooled rate > 2× the maximum per-study rate on any cell | Either weighting bug (inverse-variance weights going negative / non-finite) or back-transform error. |
| **Rank ρ implausibly high** | Spearman ρ > 0.95 across all top-quartile cells | Unlikely to hold given true panel heterogeneity. Suggests pipeline is leaking per-study info into the pooled effect (e.g., accidentally weighting a dominant study close to 100%). |
| **Every cell converges** | convergence rate = 100% | Possible in principle, but GLMM-logit on rare-event cells (small `y_total`) typically has some non-convergence. 100% suggests either no rare-event cells are in the filtered set (check `y_total ≥ 1` filter) or silent failure to flag non-convergence. |

**Pre-registered integrity checks before accepting results:**

1. **Hold-out one study** (Jee 2024 small pan-cancer cohort ~500 samples) and re-fit;
   pooled rates should be within CI of the all-studies fit.
2. **Panel-class sensitivity**: drop MC3 (re-fit on panel-only studies) and re-fit; drop
   GENIE tumor-only fraction and re-fit. Pooled direction should be stable on the
   high-signal cells; magnitude may shift.
3. **Random-reshuffling placebo**: shuffle study labels within cell and re-fit; the
   shuffled I² distribution should be close to 0 and pooled CIs approximately equal to
   the pooled CI under naive inverse-variance — confirms the model is doing real work.

## Known Limitations

This analysis cannot:

- **Distinguish "gene is never mutated in cancer c" from "gene is not callable on any
  panel that covers cancer c"** beyond what the callability filter captures. A gene on
  the intersection of zero panels simply fails the `k_studies ≥ 3` filter.
- **Credit or penalize variant-level biology** (e.g., hotspot SNV vs truncating). The
  cell-level count pools across variant types within a gene. A separate t033
  (hotspot-driver) pipeline step would layer on top.
- **Speak to clonality / VAF / sub-clonal structure** — per-sample mutation calls are
  binarized to presence/absence.
- **Correct for clonal hematopoiesis contamination beyond the `ch_priority_gene` flag**
  (uniform boolean). The graded `ch_contamination_prob` from `t087` (surfaced today
  from t059) would be a natural covariate once available.
- **Handle cancer types with K < 3 contributing studies** — rare cancers simply drop
  out. This is a stated limitation, not a bug.
- **Produce causal / mechanistic claims** — the research question is associational.

## Metric Selection Rationale

**Primary metric: pooled log-odds (`β_{g,c}`) with 95% CI and prediction interval.**

Rationale:

- Operates on the natural scale of per-sample mutation probability (0-1); sparse counts
  are handled natively by the binomial likelihood.
- Lin & Xu 2020 explicitly recommends GLMM-logit over arcsine for sparse proportion
  meta-analysis.
- Pooled effect is back-transformable to a pooled rate that downstream consumers can
  read as "fraction of samples with a mutation in this gene × cancer combination."
- `i2`, `tau2`, and the HKSJ-adjusted CI carry the heterogeneity story that pooled
  estimate alone does not.

This is the first meta-analytic metric in the project; not a change from a prior
choice.

## Exploratory vs. Confirmatory

**Confirmatory (pre-registered here):**

1. Pooled GLMM-logit fit on filtered cells with `panel_class` and `matched_normal`
   covariates (H1 test + G1 gate).
2. Convergence diagnostic + REML-logit escape-hatch if G1 fails.
3. I² distribution across cells, top-quartile-signal rank stability, CI tightening —
   all per the decision table above.
4. Three pre-registered integrity checks (hold-out, panel-class sensitivity, random
   reshuffling placebo).

**Exploratory (clearly labeled as such in outputs):**

1. Sensitivity re-fit with `cohort_stage` covariate once `t052` lands.
2. Per-stratum pooled fits (pool within `panel_class × matched_normal`) — as a
   fall-back if H1 is weakened.
3. Sensitivity re-fit with graded `ch_contamination_prob` from t087 once available.
4. Heterogeneity clustering — are the high-I² cells concentrated in particular gene
   families or cancer types? Reported as a figure, not a confirmatory test.
5. Comparison to naive sample-weighted pooled rates (the current pipeline baseline) —
   flagged as "context, not a horse-race."

## Total Comparison Count

Expected cell count based on the full-config run (~2000 gene-level rows in the pipeline
filter × ~35 cBioPortal cancer types): **~70,000 candidate cells**, reduced by filtering
to an expected **~10,000-15,000 pooled cells**.

| Category | Count (est.) | Correction |
|---|---|---|
| Confirmatory cells (H1) | ~10,000-15,000 | **Benjamini-Hochberg FDR at 5%**, stratified by cancer type (35 strata) |
| G1 convergence gate | 1 | no correction (single-threshold decision) |
| Integrity checks | 3 | no correction (diagnostic) |
| Exploratory re-fits | ≤ 5 | no per-exploratory correction; each exploratory table is labeled as such |
| **Total** | **≈ 10,015-15,010** | BH-FDR within cancer type for the confirmatory cells |

FDR is computed within-cancer-type (not pan-cancer-pooled) because the cell count
varies widely by cancer type and pan-cancer FDR would let well-sampled cancers swamp
rare ones. Benjamini-Bogomolov hierarchical FDR is considered and deferred — BH within
stratum is the default and the simpler registration choice.

## Sampling Strategy Rationale

Use **all available studies** matching the `studies:` list in the active config
(`code/config/config-full.yml` for the confirmatory run; `code/config/config-10k-genes.yml`
and `code/config/config-pan-cancer.yml` as sensitivity re-configs). No subsampling.
Rationale: the project's research question is explicitly pan-cancer aggregation;
subsampling would defeat the purpose.

## Cross-Reference to Sibling Tasks

- **t076** (F2 NaN-vs-0 handling): upstream prerequisite. The denominator used here
  depends on correct NaN-vs-0 disambiguation at the per-(study, gene) level. The
  callable-denominator column from t076 is consumed as `n_{c,s}` weighting input.
- **t081** (hypermutator sample exclusion): provides `sample_is_hypermutator` flag used
  as a filter (or covariate) on `n_{c,s}` and `y_{g,c,s}`. Filtering to
  `!is_hypermutator` is the default confirmatory path; a sensitivity fit with
  hypermutators included is registered as exploratory.
- **t052** (cohort-stage descriptor): provides the third covariate, deferred as noted.
- **t087** (graded CH prob): potential future covariate, registered as exploratory.
- **t089** (dual hypermutator flags): refines t081's exclusion list.

## Commit / activation

This pre-registration is considered **active** on commit of this file. Any deviation
from the confirmatory-tagged analyses above when t077 is implemented must be documented
in `doc/meta/pre-registration-t077-glmm-logit-pooling-deviations.md` with a dated
justification, before the pooled results are reported or interpreted.
