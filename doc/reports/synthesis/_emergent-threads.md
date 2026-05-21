---
id: "synthesis:emergent-threads"
type: "synthesis"
title: "Emergent threads - cbioportal"
report_kind: "emergent-threads"
generated_at: "2026-04-28T03:09:06Z"
source_commit: "c1c6b1f29eef8326e3efde948df540ecc23c95ed"
orphan_question_count: 5
orphan_interpretation_count: 8
orphan_ids:
  - "question:q009-sbs1-lrr-bias-as-normal-contamination-flag"
  - "question:q014-cfs-as-distinct-confounder-class"
  - "question:q015-pan-cancer-aggregator-choice"
  - "question:q016-panel-induced-ascertainment"
  - "question:q017-cross-study-saturation-curve"
  - "interpretation:2026-04-17-poc-run"
  - "interpretation:2026-04-18-t070-poc-comparison"
  - "interpretation:2026-04-22-t123-rt-brca-sbs1-proxy-pilot"
  - "interpretation:2026-04-24-t126-sbs1-lrr-bias-per-study"
  - "interpretation:2026-04-25-t052-stage-stratified-ar-esr1"
  - "interpretation:2026-04-26-t131-full-pan-cancer-dndscv-run"
  - "interpretation:2026-04-27-t144-tiebreaker-fix-rerun"
  - "interpretation:2026-04-27-t145-mean-inclusive-inflation-diagnostic"
---

# Emergent Threads — Cross-Hypothesis Bridges and Orphan Inventory

## TL;DR

- Three questions bridge two hypotheses each: `question:q007` (h01 + h05), `question:q011` (h02 + h03), `question:q012` (h04 + h06); these are the load-bearing connective tissue of the current spine.
- Five questions have no primary hypothesis: two involve signature/RT-based contamination diagnostics deferred on data-type grounds (`question:q009`), two involve gene-level confounder taxonomy (`question:q014`) and aggregation methodology (`question:q015`), and one involves ascertainment feedback loops (`question:q016`) and saturation empirics (`question:q017`).
- Eight interpretations are orphaned from the hypothesis spine, falling into three clusters: pipeline-infrastructure runs (PoC and tiebreaker re-runs), SBS1/RT diagnostic branches, and a single cohort-representativeness check.
- Two candidate hypothesis frames emerge from the orphan population: a **quality-control diagnostics** frame absorbing `question:q009` and its associated interpretations, and an **aggregation methodology / pan-cancer rollup** frame absorbing `question:q015` and several pipeline-run interpretations.
- `question:q014` and `question:q016` are strong enough to anchor extensions to existing hypotheses (h02 and h03 respectively) rather than requiring new top-level hypothesis nodes.

---

## 1. Cross-Hypothesis Questions

Three questions in the resolver output match two hypotheses each at `inverse` confidence, forming bridges across the spine.

**`question:q007-cross-tissue-somatic-mutation-rate-variation-as-null-model`** matches `hypothesis:h01-non-tumor-signal-contamination` and `hypothesis:h05-healthy-somatic-background-atlas`. The bridge is mechanistic: tissue-specific normal mutation rates (Li 2021 body-map) serve both as the null model against which non-tumor contamination is gauged (h01) and as the core empirical dataset for the healthy somatic background atlas (h05), making q007 the primary data link between the two hypotheses.

**`question:q011-gene-length-as-literature-attention-confounder`** matches `hypothesis:h02-cross-study-ranking-divergence-is-structured` and `hypothesis:h03-gene-length-confounds-literature-attention`. Gene length is both a confounder of raw mutation-frequency rankings (h02's structured divergence) and an independent predictor of literature attention (h03), so q011 tests whether controlling for length in one domain changes the signal in the other.

**`question:q012-mutation-ordering-cross-sectional-inference`** matches `hypothesis:h04-mhn-pathway-ordering` and `hypothesis:h06-pre-malignant-n-minus-1-driver-carriage`. Cross-sectional co-occurrence data is the shared input for both inferring pathway ordering via MHN (h04) and for detecting pre-malignant driver carriage at the N-1 step (h06); q012 tests whether the inference method is valid in either context.

---

## 2. Orphan Questions

Total: **5** questions with `primary_hypothesis: null`.

**`question:q009-sbs1-lrr-bias-as-normal-contamination-flag`** — asks whether the SBS1 late-replicating-region topographic bias can serve as a contamination quality flag; deferred after the t126 pre-registered decision rule determined the panel coverage of constitutive LRR territory (~20.7 kb on MSK-IMPACT) is insufficient to power the test on current data.

**`question:q014-cfs-as-distinct-confounder-class`** — asks whether common-fragile-site loci (FHIT, WWOX, MACROD2, GRID2, and related) constitute a distinct gene-level confounder class separable from the broader replication-timing covariate already framed in `question:q003`, prompted by the residual CFS-cluster pile-up surfaced in the t131 + t145 diagnostic.

**`question:q015-pan-cancer-aggregator-choice`** — asks which pan-cancer aggregator for multi-cancer dNdScv signals (lexicographic, Stouffer, Fisher, inverse-variance, Bayesian hierarchical) best discriminates among the 829 genes at BH-FDR floor zero and is most stable under leave-one-cancer-out; directly affects what the project reports as its pan-cancer driver list.

**`question:q016-panel-induced-ascertainment`** — asks whether panel-induced ascertainment creates a measurable rich-get-richer loop coupling mutation-frequency rankings and literature-attention measures, with a downstream implication that the partial length-attention slope in h03 requires panel-vs-WES stratification as a required control.

**`question:q017-cross-study-saturation-curve`** — asks at what number of contributing studies the top-N gene-cancer ranking stabilizes per cancer type, with early vs slow vs never-saturating regimes carrying distinct implications for reporting strategy and the cost-benefit of adding new cohorts.

---

## 3. Orphan Interpretations

Total: **8** interpretations whose `related:` field does not intersect any hypothesis directly or via a question with a primary hypothesis.

**`interpretation:2026-04-17-poc-run`** — end-to-end PoC pipeline run confirming the composite hypermutator flag runs but is miscalibrated for BRCA/SKCM and MSK TMB is deflated 30x; relates only to tasks, not to any filed hypothesis.

**`interpretation:2026-04-18-t070-poc-comparison`** — pre/post comparison for the t070 MSK panel-version drift fix, confirming a ~30x TMB correction and correct hypermutator reclassification for 401 samples; relates only to tasks and the PoC interpretation.

**`interpretation:2026-04-22-t123-rt-brca-sbs1-proxy-pilot`** — the simple CpG C>T proxy for SBS1 RT topography on the BRCA panel-vs-WES pair collapsed under panel sparsity (1,157/1,210 panel samples had CE=0), ruling out the coarse proxy route for `question:q009`; relates only to q009 (an orphan question).

**`interpretation:2026-04-24-t126-sbs1-lrr-bias-per-study`** — per-study aggregate SBS1 LRR-bias test reached a pre-registered terminating verdict (both safety gates triggered: n_sbs1_pooled below 500-floor, CI half-width above 0.10 ceiling), deferring `question:q009` until WGS inputs are available; relates only to q009.

**`interpretation:2026-04-25-t052-stage-stratified-ar-esr1`** — stage-stratified AR and ESR1 mutation rates returned partial verdicts (directional signal correct for metastatic > primary; one stratum per comparison within 3 pp tolerance), validating the cohort stage descriptor; relates only to a task and a topic node with no hypothesis connection.

**`interpretation:2026-04-26-t131-full-pan-cancer-dndscv-run`** — full pan-cancer dNdScv chain ran end-to-end (146 cancer types, 474,524 annotated rows) but surfaced a tiebreaker artifact and a mean_inclusive inflation bug distorting the headline three-way comparison; `question:q011` appears in `source_refs` but not in `related:`, leaving this interpretation formally unconnected to any hypothesis.

**`interpretation:2026-04-27-t144-tiebreaker-fix-rerun`** — the lexicographic-sort fix confirmed the Bailey driver recovery spec exactly (14/15 in top-15 at full pan-cancer scale); relates only to tasks.

**`interpretation:2026-04-27-t145-mean-inclusive-inflation-diagnostic`** — root-cause analysis confirming the mean_inclusive inflation in t131 was caused by stale pooled means computed before WES zero-fill, not by the t139 nesting-check bypass; has no frontmatter `related:` field.

---

## 4. Candidate Hypotheses

Two candidate hypothesis frames emerge from recurring orphan topics.

**Candidate A: Quality-control diagnostics via mutational signatures and replication timing.**
Absorbs: `question:q009`, `interpretation:2026-04-22-t123-rt-brca-sbs1-proxy-pilot`, `interpretation:2026-04-24-t126-sbs1-lrr-bias-per-study`. The unifying claim would be: *a well-powered WGS-based topographic or signature-based diagnostic can directly flag studies with excess normal-tissue contamination, independently of tumor-purity proxies*. Currently q009 orbits h01 conceptually but is not claimed by it; a quality-control sub-hypothesis would give these interpretations a formal home and a testable threshold (LRR-bias delta, SBS1 excess fraction).

**Candidate B: Pan-cancer aggregation methodology as a structured methodological choice.**
Absorbs: `question:q015`, `interpretation:2026-04-26-t131-full-pan-cancer-dndscv-run`, `interpretation:2026-04-27-t144-tiebreaker-fix-rerun`, `interpretation:2026-04-27-t145-mean-inclusive-inflation-diagnostic`. The unifying claim would be: *the choice of cross-cancer aggregator (tiebreaker rule, mean computation, weighting scheme) materially changes the pan-cancer driver ranking in the q=0 regime, and a pre-registered aggregator comparison is required before reporting a headline driver list*. This is partly methodological rather than scientific, but the scale of the t131/t144/t145 finding (829 genes at the q=0 floor; tiebreaker changed 12/15 top-gene identities) warrants formal treatment.

**`question:q014`** (CFS as distinct confounder) and **`question:q016`** (panel-induced ascertainment loop) are better absorbed as extensions to existing hypotheses — q014 into h02 (it refines the gene-level confounder taxonomy already claimed there), and q016 into h03 (it identifies panel design as a required covariate in the length-attention regression) — rather than requiring new top-level nodes.

**`question:q017`** (saturation curve) is best folded into h02 once the k-study ablation data is available, as it directly informs the LOO power argument already central to that hypothesis.
