---
id: "synthesis:emergent-threads"
type: "synthesis"
title: "Emergent threads - cbioportal"
report_kind: "emergent-threads"
generated_at: "2026-06-02T09:52:22Z"
source_commit: "037f0ab2d3c84ecc56bebd843e361c1a9dfbfa66"
orphan_question_count: 1
orphan_interpretation_count: 6
orphan_ids:
  - "question:q009-sbs1-lrr-bias-as-normal-contamination-flag"
  - "interpretation:2026-04-17-poc-run"
  - "interpretation:2026-04-18-t070-poc-comparison"
  - "interpretation:2026-04-22-t123-rt-brca-sbs1-proxy-pilot"
  - "interpretation:2026-04-24-t126-sbs1-lrr-bias-per-study"
  - "interpretation:2026-04-25-t052-stage-stratified-ar-esr1"
  - "interpretation:2026-04-27-t144-tiebreaker-fix-rerun"
---

# Emergent Threads — Cross-Hypothesis Bridges and Orphan Inventory

## TL;DR

- Four questions bridge two hypotheses each: `question:q007-cross-tissue-somatic-mutation-rate-variation-as-null-model` (h01 + h05), `question:q014-cfs-as-distinct-confounder-class`
  (h01 + h02), `question:q011-gene-length-as-literature-attention-confounder` (h02 + h03), `question:q012-mutation-ordering-cross-sectional-inference` (h04 + h06); these are the
  load-bearing connective tissue of the current spine.
- The signature-program block (h08, h09, h10, h11) is bound by three cross-hypothesis questions:
  `question:q020-minimum-sample-size-and-caller-provenance-for` (h09 + h08 + h11), `question:q021-positive-control-signature-set-expansion-sbs9` (h09 + h08), and
  `question:q024-treatment-exposed-cohort-chemotherapy-signature` (h10 + h08), all sharing the t178/t179-hardened SBS refit infrastructure.
- One question has no primary hypothesis: `question:q009-sbs1-lrr-bias-as-normal-contamination-flag`, the SBS1 LRR-bias contamination
  flag, deferred until WGS data is available; a candidate hypothesis h07 has been proposed to
  absorb it.
- Six interpretations are orphaned from the hypothesis spine, falling into three clusters:
  pipeline-infrastructure seeding runs (PoC lineage and tiebreaker fix), SBS1/RT diagnostic
  branches (directly testing `question:q009-sbs1-lrr-bias-as-normal-contamination-flag`), and a cohort-representativeness validation.
- One strong candidate hypothesis emerges: **quality-control diagnostics via SBS1 LRR topography**,
  absorbing `question:q009-sbs1-lrr-bias-as-normal-contamination-flag` and its four associated interpretations; the proposed h07 frame is
  explicitly flagged in the task backlog (`task:t164`).

---

## 1. Cross-Hypothesis Questions

Seven questions in the resolver output match two or more hypotheses, forming bridges across the
spine.

**`question:q007-cross-tissue-somatic-mutation-rate-variation-as-null-model`** bridges
`hypothesis:h01-non-tumor-signal-contamination` and `hypothesis:h05-healthy-somatic-background-atlas`.
Tissue-specific normal mutation rates (Li 2021 body-map) serve both as the null model against
which non-tumor contamination is gauged (h01) and as the core empirical dataset for the healthy
somatic background atlas (h05), making q007 the primary data link between those two hypotheses.

**`question:q014-cfs-as-distinct-confounder-class`** bridges
`hypothesis:h01-non-tumor-signal-contamination` and
`hypothesis:h02-cross-study-ranking-divergence-is-structured`. CFS loci (FHIT, WWOX, MACROD2,
GRID2) inflate both raw mutation-frequency rankings and apparent cross-study divergence through a
mechanism (replication stress, not selective pressure) shared with the normal-tissue contamination
signal, making q014 a confounder-taxonomy bridge between the two hypotheses.

**`question:q011-gene-length-as-literature-attention-confounder`** bridges
`hypothesis:h02-cross-study-ranking-divergence-is-structured` and
`hypothesis:h03-gene-length-confounds-literature-attention`. Gene length is both a confounder of
raw mutation-frequency rankings (h02) and an independent predictor of literature attention (h03),
so q011 tests whether length correction in one domain propagates into the other.

**`question:q012-mutation-ordering-cross-sectional-inference`** bridges
`hypothesis:h04-mhn-pathway-ordering` and `hypothesis:h06-pre-malignant-n-minus-1-driver-carriage`.
Cross-sectional co-occurrence data is the shared input for both inferring pathway ordering via MHN
(h04) and detecting pre-malignant driver carriage at the N-1 step (h06); q012 tests whether the
inference method is valid in either context.

**`question:q020-minimum-sample-size-and-caller-provenance-for`** bridges
`hypothesis:h09-cross-study-signature-exposure-reproducibility`,
`hypothesis:h08-agnostic-covariate-association-recovers-known-signature-aetiologies-and`, and
`hypothesis:h11-joint-indel-sbs-improves-aetiology-discrimination`. Per-cancer-type sample-size
floors and caller-provenance requirements are a shared pre-condition for all three hypotheses, as
underpowered or artefact-rich cohorts would contaminate any signature-exposure test.

**`question:q021-positive-control-signature-set-expansion-sbs9`** bridges
`hypothesis:h09-cross-study-signature-exposure-reproducibility` and
`hypothesis:h08-agnostic-covariate-association-recovers-known-signature-aetiologies-and`. Whether
SBS9/SBS54 and the canonical MMR signatures belong in the positive-control panel affects both the
h09 reproducibility benchmark and the h08 positive-control scan.

**`question:q024-treatment-exposed-cohort-chemotherapy-signature`** bridges
`hypothesis:h10-treatment-induced-signature-frequency-contamination` and
`hypothesis:h08-agnostic-covariate-association-recovers-known-signature-aetiologies-and`. Identifying
which studies carry SBS11/SBS31/SBS35/SBS87 is required both to define the h10 treatment-exposure
stratum and to guard the h08 scan from treatment-induced confounds.

---

## 2. Orphan Questions

Total: **1** question with `primary_hypothesis: null`.

**`question:q009-sbs1-lrr-bias-as-normal-contamination-flag`** — asks whether the SBS1
late-replicating-region topographic bias (present in normal tissue, absent in cancer, Yaacov 2023)
can serve as a practical contamination quality flag for cBioPortal studies. Deferred (status:
`deferred`, revisit condition: `WGS inputs ingested`) after the t126 pre-registered decision rule
was triggered: the MSK-IMPACT panel covers only ~20.7 kb of constitutive late-replicating territory
(a 23:1 CE:CL bp ratio), making the test structurally unpowered on current panel data. The t123
SBS1-proxy pilot independently confirmed this via panel sparsity collapse (1,157/1,210 panel BRCA
samples had CE=0). `task:t164` proposes drafting candidate hypothesis h07 to give this question a
formal hypothesis home.

---

## 3. Orphan Interpretations

Total: **6** interpretations whose `related:` field does not intersect any hypothesis directly or
via a question with a primary hypothesis.

**`interpretation:2026-04-17-poc-run`** — first end-to-end PoC pipeline run confirming all
canonical annotated outputs land and the POLE detector validates at canonical UCEC frequency, but
finding the composite hypermutator flag miscalibrated for BRCA/SKCM and MSK TMB deflated 30x by
panel-version drift; connects only to task nodes.

**`interpretation:2026-04-18-t070-poc-comparison`** — pre/post comparison for the t070
MSK-IMPACT panel-version drift fix, confirming the predicted ~30x TMB correction and correct
hypermutator reclassification for 401 samples; its `prior_interpretations` chain leads only to the
PoC run, not to any hypothesis.

**`interpretation:2026-04-22-t123-rt-brca-sbs1-proxy-pilot`** — the simple CpG C>T proxy for
SBS1 replication-timing topography on the BRCA panel-vs-WES pair collapsed under panel sparsity,
ruling out the coarse proxy route for `question:q009-sbs1-lrr-bias-as-normal-contamination-flag`; related only to q009 (an orphan question)
and its predecessor `interpretation:2026-04-22-t122-rt-brca-pilot`.

**`interpretation:2026-04-24-t126-sbs1-lrr-bias-per-study`** — per-study aggregate SBS1 LRR-bias
test reached a pre-registered terminating `defer` verdict (n_sbs1_pooled = 176 < 500-floor; CI
half-width = 0.194 > 0.10 ceiling) and established that the MSK-IMPACT CE:CL bp ratio of 23:1
structurally prevents powering this test on any panel cohort; related only to `question:q009-sbs1-lrr-bias-as-normal-contamination-flag`.

**`interpretation:2026-04-25-t052-stage-stratified-ar-esr1`** — stage-stratified AR and ESR1
mutation rates in MSK-IMPACT vs TCGA returned `partial` verdicts (directional signal correct:
metastatic > primary for both genes; one stratum per comparison within the pre-registered 3 pp
tolerance), validating the cohort stage descriptor; relates only to a task and
`topic:cohort-selection-bias-representativeness`, with no filed hypothesis connection.

**`interpretation:2026-04-27-t144-tiebreaker-fix-rerun`** — lexicographic-sort fix confirmed the
Bailey driver recovery spec exactly (top-15 now TP53/KRAS/NRAS/PIK3CA/FBXW7/PTEN/RB1 at ranks 1–7
vs. a prior alphabetical-A artifact), and surfaced three residual issues (TTN inflation, alphabetical
`best_cancer_type`, raw `mean_inclusive` ranking) tracked under tasks t145–t148; relates only to
tasks.

---

## 4. Candidate Hypotheses

One strong candidate emerges from the orphan population.

**Candidate h07: Quality-control diagnostics via SBS1 LRR topography.** Absorbs
`question:q009-sbs1-lrr-bias-as-normal-contamination-flag`,
`interpretation:2026-04-22-t123-rt-brca-sbs1-proxy-pilot`, and
`interpretation:2026-04-24-t126-sbs1-lrr-bias-per-study`. The unifying testable claim would be:
*a well-powered WGS-based SBS1 topographic diagnostic can directly flag studies with excess
normal-tissue contamination via the LRR-bias delta, independently of tumor-purity proxies.* This
framing is already anticipated in the task backlog — `task:t164` explicitly proposes drafting h07
to absorb q009. The revisit condition (WGS inputs ingested) is concrete and actionable once MC3 or
PCAWG WGS data enters the pipeline. The PoC lineage interpretations
(`interpretation:2026-04-17-poc-run`, `interpretation:2026-04-18-t070-poc-comparison`) and the
stage-descriptor validation (`interpretation:2026-04-25-t052-stage-stratified-ar-esr1`) are
pipeline-infrastructure records rather than hypothesis-bearing science; they are best left as
unaffiliated dev-mode interpretations rather than forcing them into a hypothesis.
