# Audit: code/scripts/create_combined_gene_cancer_freq_table.py

*As-of: 2026-04-13*

- **Auditor:** Claude session (parent task t067)
- **Task ref:** t067
- **File manifest:**
  - `code/scripts/create_combined_gene_cancer_freq_table.py` (target)
  - `code/scripts/create_freq_tables.py` (immediate upstream — produces the per-study
    `gene_cancer_study.feather` inputs)
  - `code/scripts/filter_genes.py` (further upstream — gene-presence-across-studies filter)
  - Snakefile rule `create_combined_gene_cancer_freq_table` (orchestration)
- **Modalities applied:** `panel-mutation-data.md`, `cross-study-aggregation.md`
- **Prior audit:** none — first audit of this scope

## Summary

**11 findings: 4 Critical, 6 Significant, 1 Minor.** Closure status: **open** — Critical fixes
must be merged or accepted as mitigation before any cross-study `gene_cancer_study.feather`
output is treated as a quantitative claim. The audit unblocks pipeline-addition tasks t048
(MC3 ingestion), t050 (CH-aware filter), t049 (Sanchez-Vega pathway overlay), and adds a new
P0 task for the unweighted-mean aggregation bug.

The script does what it advertises (concatenate per-study `(cancer_type, symbol, num, ratio)`
tables into a wide cross-study matrix, compute means, normalize by protein length, and write
feather output) — but **the means it produces are statistically incoherent** and **the
aggregation does not address any of the four bias axes named in
`topic:cross-study-harmonization`** (panel content, matched-normal, cohort selection,
annotation drift). Outputs should not be cited as cross-study mutation-frequency claims in
their current form.

## Findings

### F1: Unweighted `mean(axis=1)` of raw counts is statistically incoherent  [Critical]

- **Checklist item:** `cross-study-aggregation.md` `agg.09`
- **Status:** fail
- **Location:** `code/scripts/create_combined_gene_cancer_freq_table.py:30` (`num_df.loc[:, 'mean'] = num_df.mean(axis=1)`)
- **Evidence:** Code-path inspection. `num_df` columns are raw per-study mutation counts. A gene
  with 100 mutations in a 10,000-sample study and 100 mutations in a 200-sample study contributes
  the same `100` to the mean, despite per-sample rates of 1% and 50% respectively. The downstream
  `mean_adj = mean / protein_length` (line 47) inherits the same incoherence.
- **Why this matters:** Any consumer interpreting `mean` or `mean_adj` as a "cross-study average
  mutation rate / count for this gene in this cancer" gets a number that is not in any meaningful
  sense an average. This invalidates any per-gene ranking derived from `num_df.mean` or
  `num_df.mean_adj`, including downstream consumers of `gene_cancer.feather`.
- **Recommended action:** (a) For ratios: continue to use unweighted mean only if studies are
  treated as exchangeable observations of the per-cancer rate; document this choice. (b) For
  raw counts: drop the `num.mean` column entirely, or replace with **sample-size-weighted mean
  rate** (sum of per-study counts / sum of per-study sample-sizes for studies with the gene
  callable). (c) Long-term: per `cross-study-meta-analysis-cancer-genomics`, replace with
  per-study effect sizes combined via random-effects meta-analysis.
- **Blocker status:** blocks t067 closure; blocks any downstream interpretation of the `num`
  columns.
- **Resolution status:** open
- **Re-audit check:** `mean` for raw counts is replaced with a sample-size-weighted aggregate
  OR removed; `mean_adj` recomputed against the corrected aggregate.
- **Linked task:** new task to be registered (Critical fix).

### F2: No per-(study, gene) callability adjustment  [Critical]

- **Checklist item:** `panel-mutation-data.md` `panel.03`; `cross-study-aggregation.md` `agg.02`
- **Status:** fail
- **Location:** `code/scripts/create_combined_gene_cancer_freq_table.py:12-28` (the per-study
  concat loop) — no callability column is read or applied.
- **Evidence:** Code-path inspection. The script reads `(cancer_type, symbol, num, ratio)` from
  each per-study feather and concatenates. `pandas.DataFrame.mean(axis=1, skipna=True)`
  implicitly treats "gene absent from a study's panel" the same as "gene present but
  un-mutated." There is no per-(study, gene) callable-region mask; per
  `topic:targeted-panel-sequencing-bias`, this is the dominant source of bias for cross-panel
  mutation-frequency outputs (APC ~10× region-length difference between small and large GENIE
  panels per AACR GENIE 2017).
- **Why this matters:** A gene only present on the large hybrid-capture panels (DFCI, MSK,
  Vanderbilt of the GENIE launch panels) will look under-mutated in the pooled mean across
  cohorts dominated by small-amplicon-panel studies. A gene on every panel still has different
  per-gene region length across panels — naive pooled means inflate the contribution of large-
  region panels.
- **Recommended action:** Implement task t016 (GENIE per-assay BED ingestion;
  `process_genie_panel_coverage.py` is wired but the input directory must be populated from
  Synapse syn24179663). Then add a join in this script: per (study, symbol), compute callable-
  region length and either restrict aggregation to studies where the gene is callable, or
  weight contributions by callable fraction.
- **Blocker status:** blocks t067 closure; gating for the entire `cross-study-aggregation.md`
  modality.
- **Resolution status:** open
- **Re-audit check:** output table carries a `n_callable_studies` column and per-(study, gene)
  rates are restricted to studies where the gene is callable.
- **Linked task:** depends on t016; new fix-task to be registered.

### F3: No CH-priority gene flag or matched-vs-unmatched stratification  [Critical]

- **Checklist item:** `panel-mutation-data.md` `panel.05`; `cross-study-aggregation.md` `agg.07`
- **Status:** fail
- **Location:** `code/scripts/create_combined_gene_cancer_freq_table.py` whole-file — no CH or
  matched-normal logic anywhere.
- **Evidence:** Per `topic:clonal-hematopoiesis-contamination` (synthesizing Bolton et al. [@Bolton2020] over
  24,146 MSK-IMPACT patients): the 7-gene CH-priority list (DNMT3A, PPM1D, TET2, TP53, ASXL1,
  CHEK2, PRPF8) is systematically inflated in tumor-only-called cohorts. Cheng et al. [@Cheng2015] quantify
  the matched-normal advantage at ~9 extra spurious germline calls per unmatched-normal sample
  that population-AF filters cannot remove. Pugh et al. [@Pugh2022]: 52% of GENIE v9.1 is tumor-only. Pooling
  matched + unmatched cohorts in `mean(ratio)` for these 7 genes will overstate per-cancer rates.
- **Why this matters:** CH-driver genes are among the highest-frequency hits in clinical-
  sequencing cohorts. Their pooled cross-study rates in our outputs are biased upward by an
  amount that varies with the matched-normal fraction of contributing studies. TP53 in
  particular dominates pan-cancer aggregations and is a CH driver under therapy-selection
  (Bolton et al. [@Bolton2020]).
- **Recommended action:** Implement task t050 (CH-aware filter) — add `ch_priority_gene` boolean
  column to outputs, ingest per-study `matched_normal` flag from cBioPortal study definitions,
  and report matched-normal vs tumor-only stratified ratios for the 7 priority genes.
- **Blocker status:** blocks t067 closure for any output where CH-priority genes appear.
- **Resolution status:** open
- **Re-audit check:** output table carries `ch_priority_gene` boolean + per-(gene, cancer)
  matched-normal-stratified ratio columns; documented in script header.
- **Linked task:** t050 (already queued as P1).

### F4: No external driver-catalog overlay  [Critical]

- **Checklist item:** `panel-mutation-data.md` `panel.10`; `cross-study-aggregation.md` `agg.05`,
  `agg.06`
- **Status:** fail
- **Location:** `code/scripts/create_combined_gene_cancer_freq_table.py` whole-file — output
  feathers carry only `(cancer_type, symbol, per-study counts, per-study ratios, mean, mean_adj)`.
- **Evidence:** Code-path inspection + `topic:cancer-driver-genes` synthesis: high-frequency
  rankings without external-catalog overlay cannot distinguish "known driver", "long-tail
  candidate", "tissue-borrowed driver", or "artifact." Bailey et al. [@Bailey2018] publish the 299-gene
  PanCanAtlas consensus + per-cancer rosters (Table S1, downloadable). The Bailey overlay is
  *already wired* via `code/scripts/annotate_drivers.py` and Snakemake rule
  `annotate_drivers_in_gene_cancer_table` (output:
  `summary/mut/table/gene_cancer_study_annotated.feather`) — the annotated table exists but
  `gene_cancer_study.feather` itself remains unannotated.
- **Why this matters:** Consumers reading the un-annotated `gene_cancer_study.feather` cannot
  contextualize their long-tail rankings against the field's reference driver list. Per Bailey
  et al. [@Bailey2018], 19% of driver mutations are tissue-borrowed (driver in a different cancer than the
  patient's primary). Per Bandlamudi et al. [@Bandlamudi2026], ~1/3 of detected drivers are in non-canonical tissue
  contexts and behave differently. Both insights are invisible without overlay.
- **Recommended action:** Promote consumption of the *annotated* feather
  (`gene_cancer_study_annotated.feather`) as the canonical downstream input. Either retire or
  prominently flag the un-annotated `gene_cancer_study.feather` as "raw, no driver overlay
  applied." Stamp the Bailey et al. [@Bailey2018] catalog version in the output.
- **Blocker status:** blocks t067 closure for downstream consumers expecting interpretable
  driver context.
- **Resolution status:** open
- **Re-audit check:** annotated feather is the documented downstream input; un-annotated table
  has a flag warning consumers; catalog version stamped.
- **Linked task:** t053 (catalog version stamping, P2) + new disposition task on the
  un-annotated table.

### F5: No cohort-stage stratification for resistance-associated alterations  [Significant]

- **Checklist item:** `panel-mutation-data.md` `panel.06`; `cross-study-aggregation.md` `agg.04`
- **Status:** fail
- **Location:** whole-file — no `cohort_stage` ingestion.
- **Evidence:** Per `topic:cohort-selection-bias-representativeness`: AR mutations 18% in MSK
  metastatic prostate vs 1% in TCGA primary; ESR1 11% vs 4%; EGFR T790M 11.3% vs 2.2%
  (Zehir et al. [@Zehir2017], AACR GENIE 2017). The script pools studies regardless of primary / metastatic /
  pre-treated stage; resistance-associated alterations will be elevated in cohorts dominated
  by clinical-sequencing studies relative to TCGA-derived studies, but the output presents this
  as a single cross-study rate.
- **Why this matters:** For ~10–20 well-known resistance markers (AR, ESR1, EGFR T790M, MET,
  ESR1 Y537S, ABL1 T315I, etc.), the pooled cross-study rate is meaningfully different from any
  underlying biological per-cancer rate. Consumers cannot distinguish "this gene is mutated 18%
  of the time in this cancer biologically" from "this gene appears mutated 18% of the time
  because the contributing cohorts are mostly post-treatment metastatic biopsies."
- **Recommended action:** Implement task t052 (per-study cohort-stage descriptor). Output
  stratified ratios for cancer types with substantial primary vs metastatic vs pre-treated
  cohort contributions. Flag known resistance markers in particular.
- **Blocker status:** requires disposition.
- **Resolution status:** open
- **Re-audit check:** output table carries per-study `cohort_stage`; sensitive resistance
  markers reported stratified for cancers with mixed-stage cohorts.
- **Linked task:** t052 (already queued as P2).

### F6: No panel-version drift handling within MSK-IMPACT  [Significant]

- **Checklist item:** `panel-mutation-data.md` `panel.04`
- **Status:** fail
- **Location:** whole-file.
- **Evidence:** Code-path inspection + Cheng et al. [@Cheng2015] / Zehir et al. [@Zehir2017] / Bandlamudi et al. [@Bandlamudi2026]: MSK-IMPACT
  spans IMPACT-341 (2014) → 410 → 468 → 505. Genes added in later versions are uncallable in
  earlier-cohort samples but are silently treated as "not mutated" by naive aggregation.
- **Why this matters:** For genes added in IMPACT-468 or IMPACT-505 (e.g., a number of
  immune-related genes added in 2017+), the per-cancer rate computed across all MSK-IMPACT
  vintages is biased downward in proportion to the early-cohort fraction.
- **Recommended action:** Per-sample `panel_version` flag ingested from cBioPortal study
  definitions. For aggregation, restrict to samples where the gene is on the relevant panel
  version (or weight by per-version callability).
- **Blocker status:** requires disposition.
- **Resolution status:** open
- **Re-audit check:** per-sample `panel_version` carried; later-added MSK-IMPACT genes excluded
  from earlier-cohort denominators.
- **Linked task:** new disposition task to be registered (P2).

### F7: No matched-normal flag per study  [Significant]

- **Checklist item:** `panel-mutation-data.md` `panel.02`
- **Status:** fail
- **Location:** whole-file — no `matched_normal` column.
- **Evidence:** Per `topic:clonal-hematopoiesis-contamination` and Pugh et al. [@Pugh2022] (52% of GENIE v9.1
  is tumor-only). Required prerequisite for the F3 stratification.
- **Why this matters:** Without per-study matched-normal annotation, F3's CH-stratification
  cannot be implemented, and the matched-vs-unmatched pooling concern affects every gene
  weakly (not just CH-priority genes — see the "~9 extra spurious germline calls per
  unmatched sample" finding from Cheng et al. [@Cheng2015]).
- **Recommended action:** Ingest per-study `matched_normal` flag from cBioPortal study
  definitions / GENIE per-assay metadata. Add as a column on `gene_cancer_study.feather`.
- **Blocker status:** requires disposition; prerequisite for F3 fix.
- **Resolution status:** open
- **Re-audit check:** per-study `matched_normal` boolean is a column in the per-study
  feather + the cross-study output.
- **Linked task:** part of t050 (CH-aware filter).

### F8: Catalog version not stamped on outputs  [Significant]

- **Checklist item:** `cross-study-aggregation.md` `agg.06`
- **Status:** fail
- **Location:** `code/scripts/create_combined_gene_cancer_freq_table.py:66-67` — outputs written
  with no metadata about input data versions, pipeline version, or catalog versions used in any
  upstream filtering.
- **Evidence:** Per Suehnholz et al. [@Suehnholz2024]: OncoKB Level 1/2 actionability rose 8.9% → 31.6% in 5 years
  on the same MSK-IMPACT cohort. Without version stamping, any longitudinal claim derived from
  our outputs cannot be reproduced or compared across re-runs.
- **Why this matters:** Reproducibility. Two runs of this script against differently-versioned
  inputs (different cBioPortal data releases, different OncoKB snapshots upstream) can produce
  meaningfully different outputs that look identical to consumers.
- **Recommended action:** Add a sidecar JSON or feather metadata block: input data hashes,
  pipeline version (git SHA), upstream catalog versions (OncoKB snapshot, Bailey release date,
  CGC release).
- **Blocker status:** requires disposition.
- **Resolution status:** open
- **Re-audit check:** sidecar metadata exists alongside each output feather; documented in
  script header.
- **Linked task:** t053 (catalog version stamping, P2).

### F9: Unweighted mean of ratios is unjustified  [Significant]

- **Checklist item:** `cross-study-aggregation.md` `agg.09`
- **Status:** needs-judgment
- **Location:** `code/scripts/create_combined_gene_cancer_freq_table.py:31`
  (`ratio_df.loc[:, 'mean'] = ratio_df.mean(axis=1)`)
- **Evidence:** Code-path inspection + `topic:cross-study-meta-analysis-cancer-genomics`. The
  script takes a simple unweighted mean of per-study ratios. Defensible as "treat each study as
  an exchangeable observation of the per-cancer rate," but undefended in the script. A
  sample-size-weighted mean (weight by per-study cancer-specific N) gives a different (and for
  most use cases more defensible) answer; a random-effects pooled estimate gives a third.
- **Why this matters:** Different aggregation choices give materially different per-gene rate
  estimates; the choice should be explicit, not incidental to the implementation.
- **Recommended action:** Document the aggregation choice in the script header. Consider adding
  a sample-size-weighted variant alongside the unweighted variant. Long-term: per-study effect
  sizes + random-effects pooling per `topic:cross-study-meta-analysis-cancer-genomics`.
- **Blocker status:** requires disposition.
- **Resolution status:** open
- **Re-audit check:** aggregation choice documented; if simple mean retained, justification is
  in the script header citing this audit.
- **Linked task:** new disposition task; long-term covered by `cross-study-aggregation.md`
  task t062.

### F10: No saturation-aware interpretation context  [Significant]

- **Checklist item:** `cross-study-aggregation.md` `agg.10`
- **Status:** fail
- **Location:** whole-file — outputs have no per-cancer expected-driver-count context.
- **Evidence:** Per Lawrence et al. [@Lawrence2014] saturation analysis: only 4 of 21 cancer types were close to
  driver-discovery saturation in 2014, with per-type required-N estimates ranging from ~650
  (neuroblastoma) to ~5,300 (melanoma). Long-tail rankings for cancer types below saturation
  contain a non-trivial false-positive rate. Our outputs present long-tail rankings without
  this context.
- **Why this matters:** A gene appearing at the long tail of per-cancer rankings for a low-
  mutation-burden, under-sampled cancer is much more likely to be a false positive than the
  same gene at the long tail of well-saturated melanoma. Consumers cannot make this distinction
  without per-cancer saturation context.
- **Recommended action:** Add a `cancer_saturation_status` column derived from per-cancer cohort
  size + the per-cancer required-N estimates from Lawrence et al. [@Lawrence2014]. Flag long-tail rankings for under-sampled
  cancers.
- **Blocker status:** requires disposition.
- **Resolution status:** open
- **Re-audit check:** output table carries per-cancer saturation status / contributing-N
  context.
- **Linked task:** new low-priority task.

### F11: Per-study contributing count not explicit in output  [Minor]

- **Checklist item:** `cross-study-aggregation.md` `agg.03`
- **Status:** needs-judgment
- **Location:** `code/scripts/create_combined_gene_cancer_freq_table.py:27-28`,`53-54`
- **Evidence:** The output preserves per-study columns (one per study), so "how many studies
  contributed" is recoverable by counting non-null columns. But there's no explicit
  `n_studies_contributing` column, and any downstream consumer using only the `mean` /
  `mean_adj` columns loses this context.
- **Why this matters:** Minor — recoverable from the wide format. But explicit is better than
  implicit.
- **Recommended action:** Add `n_studies_contributing` column derived from non-null per-study
  values per row.
- **Blocker status:** defer OK.
- **Resolution status:** open
- **Re-audit check:** column present.
- **Linked task:** none — listed in audit only.

## Non-findings

| File | Checklist ID | Status | Note |
|---|---|---|---|
| create_combined_gene_cancer_freq_table.py | panel.01 | pass | Per-study identity preserved as column name extracted from path (line 16); carried through concat and into output via wide-format columns. |
| create_combined_gene_cancer_freq_table.py | panel.07 | not-applicable | Synonymous-mutation handling done upstream (`convert_to_feather.py` / `filter_genes.py`); not in scope for this aggregation script. |
| create_combined_gene_cancer_freq_table.py | panel.08 | needs-judgment | `study_id` is preserved (good), but no per-call source / cBioPortal data version / Oncotator-canonical-isoform restriction is annotated. Demoted from finding because this is an upstream concern; revisit when auditing `convert_to_feather.py`. |
| create_combined_gene_cancer_freq_table.py | panel.09 | not-applicable | This script does not compute TMB. |
| create_combined_gene_cancer_freq_table.py | agg.01 | pass | Per-study identity preserved before pooling; raw long-format implicit in the per-study columns. |
| create_combined_gene_cancer_freq_table.py | agg.08 | not-applicable | This script aggregates per-study summaries; hypermutator handling is in `filter_genes.py` upstream and per-study `convert_to_feather.py`. |
| create_combined_gene_cancer_freq_table.py | agg.11 | not-applicable | Clustering outputs are produced by `cluster_genes.py` / `cluster_cancer_types.py`, not this script. |
| create_combined_gene_cancer_freq_table.py | mutation-rate-normalization (informal) | pass-with-caveat | Protein-length normalization (`mean_adj = mean / length`, lines 47, 51) is applied. Per `topic:mutation-rate-normalization` this is the simplest first-order correction; insufficient for driver discovery but adequate for long-tail-vs-real ranking adjustment. Not promoted to finding because the script does *something*, even if minimal. |

## Open questions

- **What is the intended downstream consumer of `gene_cancer_study.feather`?** If it's the
  Snakemake `annotate_drivers_in_gene_cancer_table` rule (which produces
  `gene_cancer_study_annotated.feather`), most of F4's concerns are addressed. If consumers are
  reading the un-annotated version directly (e.g., in the `summary.html` report),
  F4 needs a hard fix.
- **Is the unweighted-mean choice (F9) intentional design or implementation default?** Affects
  whether F9 is a disposition (justify and keep) or a fix (replace with weighted variant).

## Recommended fix sequence

Critical first (block any cross-study quantitative claim):

1. **F1 fix**: drop or replace `num.mean` and `num.mean_adj` with sample-size-weighted aggregate.
   Independent of F2. Quick (lines 30, 47).
2. **F3 fix**: implement t050 (CH-aware filter). Depends on F7 (matched-normal flag ingestion).
3. **F2 fix**: implement t016 + add per-(study, gene) callability join. Larger effort —
   gated on the manual GENIE Synapse download.
4. **F4 fix**: redirect downstream consumers to the annotated feather; flag the un-annotated
   table.

Significant + Minor in parallel as bandwidth allows:

5. F5 (cohort-stage stratification) → t052
6. F6 (panel-version drift) → new task
7. F7 (matched-normal flag) → part of t050
8. F8 (catalog version stamping) → t053
9. F9 (weighted-mean disposition) → new task
10. F10 (saturation context) → new low-priority task
11. F11 (contributing-count column) → trivial drive-by fix

The audit task t067 may close once: F1 has a registered fix task (or merged fix); F2/F3/F4
have explicit dispositions (fix task IDs or accepted mitigation plans). F1 is the only Critical
finding that does not have an existing pipeline-addition task to attach to and therefore
requires a new task.
