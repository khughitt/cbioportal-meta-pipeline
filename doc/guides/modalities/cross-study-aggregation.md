# Cross-study aggregation — best-practices guide

*As-of: 2026-04-13*

This guide codifies the audit checklist for code that **combines mutation data across cBioPortal
studies** to produce per-(gene, cancer) or per-(gene, cancer, study) summary tables. It is the
cross-cutting modality guide that pulls together panel-data, WES-data, and annotation-pipeline
concerns. Most of our `code/scripts/create_combined_*` family of scripts falls under this guide.

The interpretive backbone is `topic:cross-study-harmonization`, which names the four compounding
bias axes: panel content / matched-normal / cohort selection / annotation drift. The statistical
backbone is `topic:cross-study-meta-analysis-cancer-genomics`, which names the effect-size
combination machinery that should replace naive count pooling.

## Sources

**Dataset / cohort (foundational):**

- Pugh TJ, et al. 2022. "AACR Project GENIE: 100,000 Cases and Beyond." *Cancer Discov*
  12:2044–2057. PMID 35819403.
  → quantifies that no portable panel-correction recipe is published; per-assay BEDs are the
  available raw material.
- Bandlamudi C, et al. 2026. "Cancer type-specific variation in patterns of driver alterations
  across 50,000 tumors." *Cancer Cell*. PMID 41895280.
  → "non-canonical context" finding (~1/3 of drivers behave differently in non-canonical
  tissues) — implies tissue-stratified aggregation is the right unit, not pooled.
- Suehnholz SP, et al. 2024. "Quantifying the Expanding Landscape of Clinical Actionability for
  Patients with Cancer." *Cancer Discov*. PMID 37849038.
  → OncoKB version-drift quantification (Level 1/2 actionability 8.9% → 31.6% in 5 years on the
  *same* cohort). Mandates catalog version stamping on annotated outputs.
- Bailey MH, et al. 2018. "Comprehensive Characterization of Cancer Driver Genes and Mutations."
  *Cell* 173. PMID 30096302.
  → 19% of driver mutations are tissue-borrowed — argues for per-cancer-type rosters alongside
  pan-cancer aggregations.
- Martínez-Jiménez F, et al. 2020. "A compendium of mutational cancer driver genes." *Nat Rev
  Cancer* 20:555–572. PMID 32778778.
  → IntOGen consensus voting across ~66 cohorts / ~28,000 samples. The closest cancer-genomics-
  native prior art to what we're building; sits *between* naive pooling and proper
  random-effects meta-analysis (consensus voting, not effect-size combination).

**Meta-analytic statistics (methodology core — added 2026-04-13):**

- DerSimonian R & Laird N. 1986. "Meta-analysis in clinical trials." *Control Clin Trials*
  7:177–188. DOI 10.1016/0197-2456(86)90046-2.
  → seminal random-effects estimator (`method="DL"` in `metafor::rma`). Obligate citation when
  we switch away from naive pooling.
- Viechtbauer W. 2010. "Conducting Meta-Analyses in R with the metafor Package." *J Stat Softw*
  36:1–48. DOI 10.18637/jss.v036.i03.
  → `metafor` manual; defines `rma`, `rma.mh`, `rma.glmm`, `escalc`; covers DL, REML, PM, SJ,
  HE, ML, EB estimators side-by-side. Tool-of-record if we implement meta-analytic pooling in R.
- Langan D, et al. 2018. "A comparison of heterogeneity variance estimators in simulated
  random-effects meta-analyses." *Res Synth Methods*. DOI 10.1002/jrsm.1316.
  → the τ²-estimator shootout. Recommends **REML + HKSJ** as the general default. Answers
  "which random-effects method should we use" with simulation evidence.
- Stijnen T, Hamza TH, Özdemir P. 2010. "Random effects meta-analysis of event outcome in the
  framework of the generalized linear mixed model with applications in sparse data." *Stat Med*
  29:3046–3067. DOI 10.1002/sim.4040.
  → GLMM / beta-binomial for sparse-event meta-analysis. Methodological foundation for pooling
  per-study (mutated, sequenced) counts natively — handles zero-mutation-count genes without
  continuity corrections.
- Lin L & Xu C. 2020. "Arcsine-based transformations for meta-analysis of proportions: Pros,
  cons, and alternatives." *Health Sci Rep* 3:e178. DOI 10.1002/hsr2.178.
  → 2020 critique of Freeman–Tukey arcsine; argues for GLMM logit or Bayesian hierarchical
  alternatives. Current-generation default recommendation for pooling proportions.
- Nyaga VN, Arbyn M, Aerts M. 2014. "Metaprop: a Stata command to perform meta-analysis of
  binomial data." *Arch Public Health* 72:39. DOI 10.1186/2049-3258-72-39.
  → single-proportion meta-analysis recipe (no control arm) — exact structural match to
  per-study mutation-ratio framing. R equivalent: `meta::metaprop`.
- Higgins JPT & Thompson SG. 2002. "Quantifying heterogeneity in a meta-analysis." *Stat Med*
  21:1539–1558. DOI 10.1002/sim.1186.
  → seminal I² paper. Obligate cite for any heterogeneity diagnostic reported alongside pooled
  gene-cancer estimates.
- IntHout J, et al. 2016. "Plea for routinely presenting prediction intervals in meta-analysis."
  *BMJ Open* 6:e010247. DOI 10.1136/bmjopen-2015-010247.
  → prediction intervals (not just pooled CIs) as routine output; practical HKSJ guidance.
- Barendregt JJ, et al. 2013. "Meta-analysis of prevalence." *J Epidemiol Community Health*
  67:974–978. DOI 10.1136/jech-2013-203104.
  → Freeman–Tukey double-arcsine for pooling prevalences. Context read for Lin & Xu 2020's
  critique — know why we should **not** default to arcsine.
- Harrer M, Cuijpers P, Furukawa T, Ebert DD. 2021. *Doing Meta-Analysis with R: A Hands-On
  Guide.* Chapman & Hall/CRC. `dmetar` R package (companion).
  → practitioner handbook; comprehensive coverage of `meta` / `metafor` workflows. Not
  retrieved in the 2026-04-13 search (book, not article); manually noted as an @book entry
  when `dmetar` is added to the pipeline's R dependencies.

**Reviews / synthesis:**

- `topic:cross-study-harmonization` — project-internal master interpretive frame
  (*what biases need correcting*).
- `topic:cross-study-meta-analysis-cancer-genomics` — statistical-methods frame
  (*which machinery does the combining once biases are known*).
- `search:2026-04-13-cross-study-meta-analysis-stats` — 2026-04-13 focused search feeding this
  guide; full rationale for the default recipe below.

## Default statistical recipe

Current state of this project's cross-study outputs (`code/scripts/create_combined_*`): pooled
gene × cancer ratios are produced as **naive sample-weighted sums** across per-study counts.
This is fine as a descriptive denominator but does not respect the per-study data-generating
process, does not expose heterogeneity, and silently collapses zero-count studies into the
pool. Per the 2026-04-13 meta-analysis search, the recommended upgrade is:

1. **Effect-size definition.** For each (gene, cancer, study) triple, define the per-study
   effect as the binomial pair `(k, n)` = (samples mutated in this gene-and-cancer within this
   study, total samples sequenced for this gene-and-cancer within this study). This is the
   single-proportion meta-analysis framing (Nyaga 2014).

2. **Primary pooled estimate.** Fit a **GLMM with logit link** on the per-study `(k, n)`
   counts — a random-intercept binomial model with study as the grouping factor. In R:
   ```r
   metafor::rma.glmm(measure = "PLO", xi = k, ni = n, method = "ML",
                     slab = study_id)
   ```
   Equivalent Bayesian formulation (for uncertainty propagation into downstream clustering):
   ```r
   brms::brm(k | trials(n) ~ 1 + (1 | study_id), family = binomial())
   ```
   This handles zero-count studies natively, respects the binomial DGP, scales to thousands of
   genes, and cleanly extends to study-level covariates (panel class, matched-normal flag,
   cohort stage) as moderators.

3. **Small-K variance adjustment.** When the number of contributing studies `K < 30` for a
   given (gene, cancer) pair, apply the **Hartung–Knapp–Sidik–Jonkman (HKSJ)** adjustment
   (IntHout 2016). Many long-tail cancer types will fall in this regime, so HKSJ is not
   optional.

4. **Heterogeneity diagnostics reported alongside the point estimate:**
   - `I²` (Higgins & Thompson 2002) — fraction of variance attributable to between-study
     heterogeneity.
   - `τ²` (REML or ML, per Langan 2018) — between-study variance on the logit scale.
   - Q statistic + p-value — test of heterogeneity.
   - **95% prediction interval** (IntHout 2016) — the expected range of true per-study rates
     for a new, exchangeable study. For most downstream interpretive claims this matters more
     than the pooled CI.

5. **Explicit alternative disclosure.** Keep the existing **naive sample-weighted ratio** as a
   reported column for transparency and for the common case where `K=1`. Compute a
   **Freeman–Tukey arcsine** pooled estimate (Barendregt 2013) only as a disclosed
   alternative; do **not** use it as the default (Lin & Xu 2020).

6. **Cross-reference to consensus voting.** Where IntOGen (Martínez-Jiménez 2020) reports a
   per-cancer driver call, surface it as an annotation column next to the pooled estimate.
   This lets consumers compare our random-effects pooled evidence against the published
   cancer-genomics consensus.

**Deliverables implied by this recipe** (not yet in the task backlog — see "Recommended
follow-up tasks" below):

- A new `code/scripts/create_pooled_gene_cancer_meta.R` (or `.py` with rpy2 bridge, or a
  pure-Python `statsmodels.BinomialBayesMixedGLM` implementation) that consumes the long-format
  `gene_cancer_study.feather` and produces `gene_cancer_pooled.feather` with columns:
  `gene, cancer, k_pooled, n_pooled, p_hat_naive, p_hat_glmm, ci_lo, ci_hi, pi_lo, pi_hi, i2,
  tau2, q, q_pvalue, k_studies, method`.
- A moderator-enabled variant that adds `panel_class` and `matched_normal` as study-level
  covariates.
- Unit tests on a held-out toy dataset with known ground-truth pooled rates.

## Audit checklist

| ID | Item | Applicability | Settled? | Task | Evidence expected |
|---|---|---|---|---|---|
| agg.01 | Per-study identity preserved through aggregation | any cross-study output | settled | — | `study_id` column carried; raw long-format `gene_cancer_study.feather` produced before any pooling |
| agg.02 | Per-(study, gene) callability adjustment applied to ratios | any cross-study ratio output | contested | — (future: panel-intersect task) | callable-region length used as denominator (ideally from per-assay BED), or explicit panel-intersection restriction with rationale |
| agg.03 | Per-(gene, cancer) ratios reported with per-study contributing-counts | any cross-study ratio output | contested | — | output table shows N studies contributing + per-study counts, not just pooled rate |
| agg.04 | Cohort-stage stratification for sensitive genes | aggregations involving resistance-associated alterations | contested | **t052** | AR / ESR1 / EGFR T790M / similar resistance markers reported stratified by primary / metastatic / pretreated, not pooled |
| agg.05 | Tissue-conditional driver flag distinguishes pan-cancer vs per-cancer drivers | per-(gene, cancer) annotated outputs | contested | **t054** | per-cancer Bailey 2018 roster overlay applied (not just pan-cancer); flag distinguishes tissue-matched driver vs tissue-borrowed |
| agg.06 | OncoKB / CGC / Bailey catalog version stamped on outputs | any annotated output | settled / hardening | **t053** | catalog version (date, release tag, file checksum) recorded per annotation column |
| agg.07 | CH-priority gene matched-vs-unmatched stratification | per-(gene, cancer) outputs for CH-priority genes | settled | — (`annotate_ch.py`) | DNMT3A / PPM1D / TET2 / TP53 / ASXL1 / CHEK2 / PRPF8 reported with separate matched-normal vs tumor-only ratio columns |
| agg.08 | Hypermutator / MSI / POLE handling consistent | per-cancer aggregations | settled | **t081** (implemented via `annotate_hypermutators` / `samples_annotated.feather`; see agg.15) | hypermutator inclusion / exclusion documented via `is_hypermutator` + `hypermutator_reason` audit trail; per-cancer rates emitted in inclusive + exclusive variants |
| agg.09 | Random-effects / heterogeneity-aware pooling implemented | any pooled per-(gene, cancer) rate output | contested | **t077** | per-study `(k,n)` pooled via GLMM-logit (Stijnen 2010; Nyaga 2014); I², τ², Q, 95% prediction interval reported; HKSJ adjustment for K<30 (Langan 2018; IntHout 2016) |
| agg.10 | Saturation-aware long-tail interpretation | per-cancer driver-ranking outputs | contested | — | per-cancer expected SMG count from Lawrence 2014 cited; outputs claiming many more drivers for low-mutation-rate cancers flagged |
| agg.11 | Cross-study clustering reproducibility checked | clustering outputs (`gene.feather`, `cancer.feather`) | settled | **t056** (mutation-only vs Hoadley) | clustering rerun with study held-out; cluster stability reported, OR clustering done per-study + consensus |
| agg.12 | Pan-cancer pathway overlay applied to per-(sample, pathway) aggregations | any per-(cancer, pathway) alteration-rate output | proposed | **t049** | Sanchez-Vega 2018 Tables S2/S3 10-pathway roster applied; per-cancer pathway alteration rate + per-tumor pathway burden reported |
| agg.13 | Mutation × SCNA axis descriptor reported for per-cancer outputs | per-cancer summary outputs | proposed / blocked | **t055** (blocked: no CNA ingestion) | Ciriello 2013 M-class / C-class descriptor; blocked until CNA data flows through the pipeline |
| agg.14 | Cross-study co-occurrence / mutual-exclusivity statistic uses a burden-aware null | any gene-gene interaction output aggregated across studies | proposed | **t078** | DISCOVER Poisson-binomial null (Canisius 2016) OR WeSME weighted-sampling null (Kim 2017); per-study p-values combined via Stouffer or hierarchical model; van de Haar 2019 confounder checklist applied |
| agg.15 | Hypermutator-exclusion applied to cross-study pooled ratios | any per-(gene, cancer) pooled rate output | settled | **t081** / **t098** | `samples_annotated.feather` `is_hypermutator` flag consumed by `create_freq_tables.py`; per-study `gene_cancer_study.feather` carries paired `num_inclusive` / `num_exclusive` / `ratio_inclusive` / `ratio_exclusive` / `n_samples_inclusive` / `n_samples_exclusive` columns; `create_combined_gene_cancer_freq_table.py` pivots per-study columns into `{study}` (legacy inclusive alias) + `{study}_exclusive` pairs and emits pooled `mean_inclusive` + `mean_exclusive` (paralleling agg.07's CH matched/unmatched split; plan finding #4 canonical decision table). POLE/POLD1 hotspots and MSI-H override TMB for is_hypermutator=True regardless of per-cancer GMM posterior |

## Common pitfalls

- **Naive count pooling across heterogeneous panels.** The most pervasive pitfall in cross-
  study cBioPortal aggregation. Per-(study, gene) callable-fraction weighting is the principled
  fix on the input side; **random-effects pooling** (agg.09) is the principled fix on the
  output side. Both matter.
- **Pooling without reporting heterogeneity.** A pooled estimate with I² = 80% and a prediction
  interval that spans an order of magnitude is *not* the same signal as a pooled estimate with
  I² = 5%. Report both the pooled estimate and the heterogeneity diagnostics side-by-side
  (IntHout 2016).
- **Pan-cancer pool of studies dominated by clinical-sequencing cohorts.** AR / ESR1 / EGFR
  T790M will be 5-10× elevated relative to TCGA-derived studies for the same cancer. Stratify
  by cohort-stage (agg.04 / t052).
- **Reporting "% actionable" without OncoKB version.** Suehnholz 2024 shows 3.5× drift in 5
  years on the same cohort. Without a version stamp, longitudinal claims are meaningless
  (agg.06 / t053).
- **Ignoring the "tissue-borrowed driver" phenomenon.** A high-frequency TP53 in a long-tail
  cancer might be the canonical TP53-in-HGSOC driver behavior, or it might be a "non-canonical
  context" with different clonality / late emergence (Bandlamudi 2026 ~1/3 of drivers)
  (agg.05 / t054).
- **Treating cluster outputs as ground truth.** Mutation-only clustering (what our pipeline
  does) is a single axis; multi-omic clusterings (Hoadley 2018) and pathway-level clusterings
  (Sanchez-Vega 2018) give different but complementary structures. See
  `topic:pan-cancer-interpretive-frames`. Concrete audit: agg.11 / t056.
- **Assuming correlation-matrix entries are drop-in co-occurrence / mutual-exclusivity
  results.** `code/scripts/create_correlation_matrices.py` produces per-study Pearson/Jaccard
  matrices; these are *not* burden-aware and will reflect TMB heterogeneity as much as real
  epistasis (van de Haar 2019). Promote correlation-matrix outputs to co-occurrence statistics
  only via agg.14 (DISCOVER / WeSME / SELECT null models).

## Follow-up tasks filed

Implied by the default statistical recipe and the new agg.09 / agg.14 checklist items; added
to `tasks/active.md` on 2026-04-13:

- **t077** — Pipeline addition: random-effects pooled gene × cancer table (GLMM-logit)
  (implements agg.09). Primary references: Stijnen 2010, Nyaga 2014, Langan 2018,
  IntHout 2016.
- **t078** — Pipeline addition: cross-study co-occurrence / mutual-exclusivity statistic
  (DISCOVER / WeSME + Stouffer) (implements agg.14). Primary references: Canisius 2016,
  Kim 2017, Mina 2020, van de Haar 2019.
- **t079** — Pre-register pooling-method choice (GLMM-logit) before running on full dataset.
  Prevents post-hoc method drift once per-gene results start coming in.

**Not yet filed** (lower priority): a benchmark task to contribute to the 2022–2026
ME-method benchmark gap surfaced by `search:2026-04-13-cooccurrence-mutual-exclusivity-methods`
— run DISCOVER vs WeSME vs SELECT on cross-study cBioPortal inputs and report
agreement/disagreement. Cross-study aggregation of ME p-values is itself a published-
literature gap this project could plausibly fill.
