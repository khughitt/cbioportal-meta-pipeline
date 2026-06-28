---
type: meta
title: "Bias Audit: cross-study aggregation pipeline (preprocessing \u2192 clustering)"
status: proposed
created: '2026-04-13'
updated: '2026-06-28'
id: meta:0001-bias-audit-cross-study-aggregation-pipeline-preprocessing-clustering
source_refs:
- spec:research-question
- topic:cross-study-harmonization
- search:0002-cross-study-meta-analysis-stats
- search:0001-cooccurrence-mutual-exclusivity-methods
related:
- topic:cross-study-harmonization
- topic:cross-study-meta-analysis-cancer-genomics
- topic:clonal-hematopoiesis-contamination
- topic:targeted-panel-sequencing-bias
- topic:cohort-selection-bias-representativeness
- task:t052
- task:t070
- task:t076
- task:t077
- task:t079
---

# Bias Audit: cross-study aggregation pipeline (preprocessing → clustering)

## Scope

Methodological-rigor audit of every transformation the cbioportal pipeline applies to somatic
mutation data *after it enters our hands* — from raw cBioPortal MAFs through per-study
feather tables, per-study ratios, cross-study pooling, annotation overlays, and clustering.
Scope chosen by the user (not by recency heuristics): "have we carefully assessed every
analysis we have done, and ensured that we are properly preprocessing, normalizing, etc.?"
Upstream data provenance (cBioPortal's own curation, variant calling, sequencing) is
out of scope — this audit covers only transformations we control.

Project links: this audit is anchored to `topic:cross-study-harmonization`,
`topic:clonal-hematopoiesis-contamination`, `topic:targeted-panel-sequencing-bias`, and
`topic:cohort-selection-bias-representativeness`.
The immediate mitigation tasks it originally organized were `task:t052`, `task:t070`,
`task:t076`, `task:t077`, and `task:t079`.

Pipeline surfaces audited (in topological order): `convert_to_feather.py` →
`check_gene_coverage.py` → `filter_genes.py` → `create_freq_tables.py` →
`create_gene_{patient,cancer}_mutation_count_matrix.py` → `create_combined_*` family →
`annotate.py` (Bailey/CGC/Sanchez-Vega) → `annotate_ch.py` (CH stratification) →
`cluster_{genes,cancer_types}.py`. Config: `code/config/config-10k-genes.yml` (+ full +
pan-cancer variants).

## Cognitive Biases

### Confirmation Bias

- **Rating:** possible
- **Evidence:**
  - Literature searches this session (t042 co-occurrence, t027 meta-analysis) were explicitly
    scoped as *discovery* (not seed-verification) and turned up methods that would disconfirm
    the current pooling approach (GLMM-logit over naive averaging; DISCOVER/WeSME over
    Pearson correlation). The searches themselves are well-designed against confirmation bias.
  - However, the top-level hypothesis in `specs/research-question.md` is broad enough to be
    nearly unfalsifiable: "Aggregating somatic mutation evidence across heterogeneous
    cBioPortal studies reveals gene-cancer associations that are more robust and more
    generalizable than any single study…". Almost any non-trivial output will "confirm" this.
    Without a pre-registered falsifiable prediction, confirming-by-default is the path of
    least resistance.
  - The `topic:cross-study-meta-analysis-cancer-genomics` note correctly describes the
    project's current pooling as below the modern methodological bar — that's the opposite
    of confirmation bias in the *method* assessment. But the *hypothesis* framing still
    risks it.
- **Mitigation:** Run `/science:pre-register` (t079) to convert the hypothesis into specific
  falsifiable predictions (e.g., "gene X's pooled rate in cancer Y differs from its per-study
  median by ≤ Δ after GLMM-logit pooling" rather than "we will observe recurrent associations").

### Anchoring

- **Rating:** possible
- **Evidence:**
  - Naive sample-weighted mean pooling was the original approach and is still the operative
    default in `create_combined_gene_cancer_freq_table.py:89`. The cross-study meta-analysis
    search (2026-04-13) produced clear evidence that GLMM-logit (Stijnen et al. [@Stijnen2010];
    Lin and Xu [@LinXu2020]) is the modern default, but the pipeline has not yet moved
    (t077 newly filed, P1).
  - Protein-length normalization was chosen early (see `topic:mutation-rate-normalization`);
    it's a single-length-per-gene approximation that ignores transcript isoforms. No
    revisit since. Not wrong, but not revisited against alternatives (nucleotide-context
    model from Lawrence et al. [@Lawrence2014]; dN/dS framing from Martincorena et al.
    [@Martincorena2017]).
  - Cluster k hardcoded in config (k=10 for genes, 10 for cancers in `config-full.yml`) with
    no visible selection rationale in the repo. The earliest config values appear to have
    been inherited into later variants.
- **Mitigation:** t079 (pre-register pooling method) and t077 (implement GLMM-logit) break
  the anchoring on naive averaging. File a small follow-up: revisit k via silhouette /
  gap statistic before treating cluster IDs as interpretable.

### Availability Bias

- **Rating:** possible
- **Evidence:**
  - Heavy use of familiar Python stack (pandas, scikit-learn, pyarrow) for everything
    including statistical pooling. The meta-analysis search recommends `metafor::rma.glmm`
    in R as the tool of record; integrating it will require either an R bridge, `rpy2`, or
    a less-canonical Python equivalent (`statsmodels.BinomialBayesMixedGLM`). The path of
    least resistance ("stay in pandas, do a weighted mean") is tempting and would underdeliver.
  - Clustering uses KMeans + cosine similarity — a familiar default. The literature on
    mutation-pattern clustering suggests alternatives (consensus clustering, spectral on
    Jaccard, NMF) that may be better matched to the binary / sparse nature of the data.
- **Mitigation:** When implementing t077, explicitly compare against a hand-rolled Python
  weighted-mean as a sanity check *and* against `rma.glmm` results; don't shortcut to the
  convenient option. For clustering, file a follow-up to bench KMeans-cosine against at
  least one alternative (consensus clustering or spectral on Jaccard).

### Sunk Cost

- **Rating:** not detected
- **Evidence:** The project has demonstrably pivoted in response to evidence. Recent
  examples: adding the CH-aware annotation after Bolton et al. [@Bolton2020] evidence; adding MC3 ingestion
  after audit F2; filing t077/t078/t079 after this session's literature searches turned up
  a clear methodological upgrade path. The backlog review today closed 6 tasks as done and
  retired 2 as out-of-scope — willingness to kill work that isn't paying off.

### Process Bias

- **Rating:** likely
- **Evidence:**
  - `git log --oneline -20` shows rapid single-analyst iteration (one author on the
    `Keith Hughitt` line for every commit). No external reviewer check-in visible.
  - 23 tasks created in a single day (2026-04-13); most of today's progression has been
    inside a single session with the AI assistant. No cooling-off period between literature
    search, synthesis, guide flesh-out, and task re-prioritization.
  - Momentum bias risk: each step feels like "progress" even when it's unverified synthesis
    (e.g., the GLMM-logit default recommendation came out of a search-agent summary; the
    search artifacts in `doc/searches/` were written by the same automation in the same hour).
- **Mitigation:** Before acting on today's decisions (especially implementing t077), impose
  a deliberate cooling-off: revisit the pooling-method choice after ≥24 hours have passed
  and re-read the primary Stijnen et al. [@Stijnen2010] / Langan et al. [@Langan2018] /
  Lin and Xu [@LinXu2020] papers directly — not
  just the search summary. Consider requesting an outside review of the recommended recipe
  before committing code (could be a `superpowers:requesting-code-review` run on the written
  guide, or a human collaborator if one is available).

## Methodological Biases

### Selection Bias

- **Rating:** likely
- **Evidence:**
  - **Gene filter (`filter_genes.py`):** drops genes appearing in fewer than
    `ceil(0.2 × N_studies)` studies. The threshold is a *total* count, not stratified by
    cancer type. A gene well-covered in panels used for Cancer A but absent from panels
    used for Cancer B will either pass (if A-dominant panels are well-represented among
    the N studies) or silently get dropped — either way the decision is driven by panel
    composition, not biology. This is documented in the `cross-study-aggregation` guide's
    agg.02 but not enforced anywhere in code.
  - **Sample selection (convert_to_feather.py):** cBioPortal `SAMPLE_CLASS` and
    `SAMPLE_TYPE` fields (Primary / Metastasis / Recurrence) are ingested but never used to
    filter or stratify. All samples are treated as exchangeable. This is the headline bias
    worry W2 — confirmed.
  - **Cancer-type label canonicalization:** raw cBioPortal study labels are used as-is; no
    OncoTree mapping. "Breast Cancer" and "Breast Cancer " (trailing space) would be treated
    as distinct categories and fragment cross-study aggregation. No visible guard.
  - **Gene-symbol canonicalization:** raw symbols are used as-is; no HGNC alias mapping.
    MLL2 and KMT2D, LIN-28B and LIN28B, etc. become separate rows.
- **Mitigation:** file two small tasks (below) for gene-symbol alias mapping and
  cancer-type canonicalization. Wire `SAMPLE_CLASS` into per-study processing via t052
  (cohort-stage descriptor — already P1).

### Survivorship Bias

- **Rating:** possible
- **Evidence:**
  - The `data/` directory holds what was kept; failed ingests, studies that couldn't be
    parsed, and dropped mutation types are not logged anywhere. There's no "why was this
    study excluded" audit trail.
  - Literature search runs only log results, not discarded queries / null-result papers.
    (Acceptable for methods searches; would be a problem for a systematic review claim.)
- **Mitigation:** low-priority — add a per-run `excluded_studies.tsv` output that captures
  which studies were dropped at which pipeline stage and why. Not blocking.

### HARKing (Hypothesizing After Results are Known)

- **Rating:** likely (risk-wise)
- **Evidence:**
  - **No pre-registration documents exist** under `doc/meta/pre-registration-*.md`. The
    hypothesis in `specs/research-question.md` is broad ("aggregating… reveals gene-cancer
    associations that are more robust and more generalizable than any single study"). Almost
    any non-empty output confirms it.
  - Downstream outputs (gene and cancer clusterings, gene × cancer heatmaps, top-N gene
    rankings) are not pre-specified: the number of clusters, the genes to highlight, the
    cancer-type groupings — all are determined after seeing the data.
  - Recent pivots (MC3 ingestion, CH-aware annotation, pathway overlay) happened in response
    to audit findings — that's good practice — but the interpretive claims made off the
    resulting outputs have not been locked in advance.
- **Mitigation:** **t079 (pre-register pooling-method choice) — P1 — is the right instrument.**
  Expand its scope slightly to also pre-register (a) the falsifiable form of the main
  hypothesis, (b) the clustering metric and k-selection rule, and (c) the top-N gene
  reporting threshold. Do this BEFORE running t077 on the full dataset.

### Multiple Comparisons / p-hacking Risk

- **Rating:** likely
- **Evidence:**
  - A gene × cancer table with ~10K genes × ~90 cancer types = ~900K cells. Any per-cell
    significance test without correction will produce thousands of false positives.
  - The current pipeline does not run per-cell significance tests (only pooled ratios and
    counts), so this is a latent risk that activates the moment t077 (GLMM-logit with
    per-gene-cancer CIs) or t078 (DISCOVER/WeSME p-values) lands.
  - Clustering with hardcoded k is a silent multiple-comparisons-flavored issue: different
    k values would produce different "findings" about which cancers cluster together; with
    no k-selection procedure we're implicitly picking k by taste.
- **Mitigation:** t077's spec must include a multiple-testing correction plan (BH-FDR or
  Storey's q) applied to the per-gene-cancer pooled CIs / p-values. t078's spec must do
  the same for co-occurrence p-values. Pre-registration (t079) must commit to the correction
  family before running on full data.

### Confounding

- **Rating:** likely

#### Confound Severity Matrix

| Confound | Severity | Fixability | Mitigation (task) |
|---|---|---|---|
| **TMB / hypermutators** pool with non-hypermutators; inflates per-gene rates in MSI-CRC, POLE-endometrial, UV-skin | HIGH | EASY | File new task: hypermutator-exclusion config (exclude samples with total mutations > 10× cohort median, or implement Lawrence et al. [@Lawrence2014] covariate). Current pipeline has **zero** TMB awareness. |
| **Cohort-stage (metastatic vs primary)** pooled without stratification; AR/ESR1/EGFR-T790M rates distorted | HIGH | MEDIUM | **t052** (cohort-stage descriptor, P1) — wire `SAMPLE_CLASS` through pipeline so primary/metastatic/pretreated can be stratified. |
| **Panel content** — gene-not-on-panel and gene-on-panel-unmutated both become 0 in the final wide matrix | HIGH | MEDIUM | **t076** (NaN-vs-0 handling, P1) — preserve panel-callability through the matrix so consumers can distinguish. |
| **Unweighted cross-study pooling** — 20-sample study and 2000-sample study contribute equally to ratio mean | HIGH | MEDIUM | **t077** (GLMM-logit pooling, P1) — binomial model weights per-study contribution by `n`, natively. Interim fix: sample-size-weighted mean with a single-line config flag. |
| **Clonal hematopoiesis leakage** in tumor-only panel studies for DNMT3A/PPM1D/TET2/TP53/ASXL1/CHEK2/PRPF8 | MEDIUM-HIGH | HARD for non-priority genes | `annotate_ch.py` handles 7-gene priority list already. Remaining CH-sensitive genes not flagged. Watch for CH-signal creep in other genes via search t059 (ASXL1/TET2 disambiguation). |
| **Annotation-catalog version drift** (OncoKB Level 1/2 actionability drifted 8.9%→31.6% in 5 years, Suehnholz et al. [@Suehnholz2024]) | MEDIUM | EASY | Already handled — t053 closed; `bailey2018_source` / `cgc_source` / `sanchez_vega_source` columns emitted by annotate.py. |
| **Gene-symbol aliases** (MLL2/KMT2D, LIN-28B/LIN28B) fragment counts across synonymous rows | MEDIUM | EASY | File new task: HGNC alias-mapping pass in `convert_to_feather.py`. |
| **Cancer-type label normalization** — raw study strings with whitespace / case variation fragment aggregation | MEDIUM | EASY | File new task: cancer-type canonicalization (strip + case-normalize; optional OncoTree mapping). |
| **Patient-ID collision** across studies — both studies may use "PATIENT_001" without a study prefix | LOW-MEDIUM | EASY | File new task: prefix patient_id with `study_id` in `create_combined_sample_table.py` and downstream combined matrices. |
| **Protein-length single-isoform approximation** — one mean length per gene, no transcript awareness | MEDIUM | MEDIUM | Acknowledge as limitation in methods write-up; defer fix unless evidence suggests it materially affects rankings. |
| **Cluster k hardcoded** without selection procedure; k=10 may or may not be the right grain | LOW | EASY | File small follow-up: silhouette / gap-statistic / consensus clustering for k selection; report stability alongside cluster IDs. |
| **Protein-length median-fallback invisibility** — genes missing UniProt entries silently use median length; no indicator column | LOW | EASY | Add `length_is_fallback` boolean column in `create_combined_gene_cancer_freq_table.py`. |

### Publication Bias

- **Rating:** not applicable (to the pipeline itself — this is an analysis project, not a
  systematic review). However: the 2026-04-13 literature searches did bias toward
  methods-positive papers (named methods that worked; benchmark papers that concluded). A
  truly null-result search ("methods that failed to detect mutual exclusivity in cancer
  data") was not run. Low priority — flagged for completeness.

## Summary

- **Overall threat level:** **elevated** — not "high" because most of the threats are
  known, partially mitigated, or scheduled in the P1 backlog; not "moderate" because
  multiple HIGH-severity confounds (TMB, cohort-stage, unweighted pooling) are currently
  live in the default outputs.

- **Top 3 threats by severity:**
  1. **Confounding cluster (TMB + cohort-stage + panel + unweighted-pooling)** — four
     HIGH-severity confounders all active simultaneously in the current outputs. Any
     cross-study aggregate ratio today is interpretable only with explicit caveats about
     hypermutator cohorts, clinical-sequencing bias, panel content, and small-study
     weight. Mitigations are tracked (t052, t076, t077, plus one new TMB task below) but
     none has shipped yet.
  2. **HARKing / multiple-comparisons latent risk** — the combination of a broad hypothesis,
     no pre-registration, and the incoming t077/t078 work that will produce thousands of
     per-gene-cancer estimates is a textbook setup for post-hoc significance fishing.
     t079 (pre-register) must land before t077 / t078 run on full data.
  3. **Process bias (rapid single-analyst iteration, no external review, same-session
     synthesis)** — today's velocity is a symptom, not a virtue. The GLMM-logit
     recommendation was synthesized in the same session that surfaced the literature; the
     bias audit is being written in the same session that wrote the guide it audits.
     Impose a cooling-off before acting on t077.

- **Top mitigations (concrete actions):**
  1. File and prioritize a new **P1** task for **hypermutator / TMB-aware denominator**
     (HIGH severity, EASY fix — currently the single biggest gap with no task coverage).
  2. Expand **t079 (pre-register pooling)** scope to cover: (a) a falsifiable form of the
     research-question.md hypothesis, (b) multiple-testing correction family, (c)
     clustering k-selection procedure, (d) top-N reporting thresholds. Land t079 *before*
     t077 / t078.
  3. File small-fix tasks for the easy-win biases: gene-symbol alias mapping, cancer-type
     label canonicalization, patient-ID study-prefixing, `length_is_fallback` indicator
     column. None alone is severe; collectively they tighten the provenance chain.

- **Recommended next actions:**
  - Apply today's task-file additions below.
  - Impose a 24-hour cooling-off on the t077 / t078 implementation — re-read Stijnen et al.
    [@Stijnen2010] and Langan et al. [@Langan2018] *directly* (not the search summaries)
    before writing the GLMM-logit
    code.
  - Before the first run of t077 on the full dataset, write `doc/meta/pre-registration-
    cross-study-pooling.md` (via `/science:pre-register`) with falsifiable predictions,
    multiple-testing correction family, and exclusion rules for TMB / cohort-stage /
    panel content.
  - When t078 lands, explicitly check the outputs against van de Haar 2019's confounder
    checklist before treating any co-occurrence / mutual-exclusivity call as biological.
  - Consider requesting a `superpowers:requesting-code-review` pass on the written
    `cross-study-aggregation.md` guide before letting it drive implementation — mitigates
    the single-session process-bias risk.
