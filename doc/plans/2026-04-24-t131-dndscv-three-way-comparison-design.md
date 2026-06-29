# t131 — dNdScv selection-based driver detection + three-way ranking comparison — design

- **Task:** t131 (Opt dNdScv into rule all via config-pan-cancer-dndscv.yml + three-way ranking comparison)
- **Priority:** P2
- **Related discussion:** `discussion:0001-gene-length-bias-in-mutation-rankings-and-literature`
- **Related question:** `question:0011-gene-length-as-literature-attention-confounder`
- **Related topic:** `topic:mutation-rate-normalization`
- **Related paper:** `paper:Martincorena2017`
- **Companion follow-up task:** `task:t136` (canonicalize-to-GRCh38 at ingestion — long-term build strategy)
- **Status:** design v3 proposed 2026-04-24, awaiting approval

## Goal

Produce a per-(gene, cancer_type) dNdScv selection signal that is (a) ingested
into the canonical pipeline output `gene_cancer_study_ratio_annotated.feather`
as new columns and (b) consumed by a per-gene three-way ranking comparison
notebook + feather artifact, with literature-attention (PubTator) correlation
panels that close the loop with `question:0011-gene-length-as-literature-attention-confounder`.

| Ranking | Source | What it measures |
|---|---|---|
| Raw mutation frequency | `gene_cancer_study_ratio_annotated.feather`, `mean_inclusive` (pan-cancer mean across cancer types) | Recurrence — biased toward long genes |
| Length-adjusted | `mean_adj` = `mean_inclusive / protein_length` | First-order length correction — biased toward tiny proteins (`question:0011-gene-length-as-literature-attention-confounder` notebook empirical result) |
| Selection-based | dNdScv per-cancer-type `qglobal_cv`, rolled up per gene by min-q across cancer types | Excess of non-synonymous over synonymous mutations relative to trinucleotide-aware background — length-aware by construction |

The empirical `task:t131` input result from `code/notebooks/q011_length_adjustment_topn_comparison.py`
(Spearman ρ = 0.372, Jaccard@100 = 0.015 between raw and length-adjusted)
established that neither raw counts nor length-only adjustment produces a
defensible head-of-distribution. The deliverable answers two coupled questions:

1. Does dNdScv produce a ranking that overlaps better with one of the two
   simpler scores than they do with each other, and which canonical drivers
   (Bailey 299, CGC tier 1) recover under each scoring scheme?
2. How does each ranking correlate with PubTator gene-mention counts? If
   length-aware (dNdScv) ranking shows substantially weaker mention-count
   correlation than raw-count ranking, that is direct evidence that gene
   length confounds the literature-attention axis through the mutation-count
   mediator (the central conjecture of `q011`).

## Latent bug found during planning

Per code review of plan v2, two latent bugs were discovered in
`code/scripts/run_dndscv.R`:

1. **Wrong input source.** v2 fed dNdScv from `mut_filtered.feather`, which
   `code/scripts/filter_genes.py:23` already filters by cross-study gene
   coverage (gates by `min_studies_ratio`). dNdScv consuming a coverage-
   censored input would estimate trinucleotide-context background rates
   from a subset of the coding genome, producing miscalibrated p/q values.
2. **Column-name mismatch.** `run_dndscv.R:39-40` checks for MAF-style
   capitalized columns (`Tumor_Sample_Barcode`, `Chromosome`, `Start_Position`,
   `Reference_Allele`, `Tumor_Seq_Allele2`) but `convert_to_feather.py:126-148`
   has long since renamed these to lowercase project conventions
   (`sample_id_tumor`, `chromosome`, `start`, `reference_allele`,
   `tumor_seq_allele2`). The R script's required-column check would
   immediately `stop()` on real input. The script has never actually run
   end-to-end against pipeline output — it was authored against a raw MAF
   and never re-validated when ingestion conventions changed.

t131 closes both bugs in the course of implementing the architecture
described below. Worth calling out in the eventual commit message — t131 is
also a latent-bug fix.

## Decisions baked in (v3)

These were surfaced and revised during planning. Document them so a future
agent doesn't relitigate.

1. **R via conda YAML, not Docker.** Matches the existing `code/envs/r-meta.yml`
   pattern used by `rule run_gene_cancer_meta_analysis`. Respects
   `feedback:r-reproducibility`. Self-bootstrap dndscv from a pinned GitHub
   SHA at first run since dndscv is not on conda-forge or Bioconductor.
   Trade-off: first-time env build is slow (~5–15 min) and brittle if
   conda channels drift.

2. **Per-cancer-type combined MAF granularity.** New rule
   `combine_mut_per_cancer_type` aggregates per-study inputs into per-cancer-
type combined MAFs. dNdScv is invoked once per cancer type rather than
once per study. Cohorts are now biologically meaningful (matches dNdScv's
intended use per Martincorena et al. [@Martincorena2017]); removes the awkward Stouffer-of-q-
   values step from v1. The existing per-study `rule run_dndscv` is replaced
   (not preserved as a fallback in v3 — the v2 idea of keeping both turned
   out unnecessary, and the per-study script is the one with the latent bug;
   simpler to fix in one place).

3. **dNdScv input source: `mut.feather`, not `mut_filtered.feather`.**
   New script `prepare_dndscv_input.py` between `mut.feather` and the
   per-cancer combine step:
   - validates required lowercase columns exist,
   - joins `samples.feather` to attach `cancer_type`,
   - restricts to SNV variant types (dNdScv's per-codon background model
     applies to SNVs; indels go into `wind_cv` separately, dndscv handles
     them, but we filter to SNVs for input simplicity in Phase 1),
   - writes a known-schema feather consumed by the combine step.

4. **`run_dndscv.R` rewritten for project-feather column conventions.**
   Replaces the MAF-name `required_cols` check; drops the pre-existing
   column-rename block that was operating on never-present columns. Also
   accepts a `params.refdb` value ("hg19" or "hg38") and emits a per-run
   retention-rate log line (raw input rows vs rows accepted by dNdScv).

5. **dNdScv signal joined into the canonical pipeline output.** New columns
   land on `gene_cancer_study_ratio_annotated.feather` (full schema in
   §"Schema contract on canonical feather" below). Existing columns
   preserved unchanged.

6. **Per-study refdb routing — build metadata is a hard requirement, not a
   silent fallback.** `meta_study.txt` becomes a declared download rule
   output and a `convert_to_feather` declared input. Per-study build is
   parsed from `reference_genome_id` and persisted to
   `studies/{id}/metadata/study_build.txt`. If the field is absent or
   non-standard, the rule fails loudly with a clear error message naming
   the study; an explicit per-study config map
   (`study_reference_build_override`) lets the user supply build for studies
   with broken metadata. **No silent default** — that conflicts with
   AGENTS.md's "Fail early / avoid silent fallbacks" rule and would let
   hg38 cohorts be silently misprocessed against hg19 RefCDS.
   Interim solution; long-term destination is `task:t136` (canonical GRCh38
   throughout the pipeline).

7. **`reconcile_dndscv_per_cancer` is in scope.** v2 listed it both in the
   architecture and in out-of-scope — direct contradiction, resolved here in
   favor of in-scope. The reconcile output explicitly flags split-build
   cancer types via a `dndscv_split_build` boolean rather than presenting
   min-q across builds as a unified-cohort result. For mono-build cancer
   types the reconcile is a pass-through.

8. **Panel/WES handling: explicit per-output flag columns + optional
   WES-only mode.** dNdScv on panel data is exploratory per the script's
   own docstring. For a column landing in the canonical feather, "include
   with warning" is too soft. Per-(gene, cancer_type) modality columns
   (full schema in §"Schema contract" below) let consumers filter cleanly.
   Optional config knob `dndscv_wes_only` (default `false`) excludes panel
   studies from the per-cancer combine when set; a primary release run
   may want this.

9. **PubTator literature-attention deliverable.** Per t131 task description
   ("per-list correlation with PubTator gene-mention counts"), the
   comparison artifact + notebook now include PubTator mention-count joins
   and per-list rank correlation panels. This closes the loop with `q011`'s
   central conjecture and is required for acceptance.

10. **Side-config + side-target, not modifying default rule all.** New
    `rule all_with_dndscv:` in the Snakefile. Default `rule all` stays
    R-free for users without conda.

## Schema contract on canonical feather

`gene_cancer_study_ratio_annotated.feather` gains the following columns,
joined per (symbol, cancer_type). Existing columns are preserved unchanged.

| Column | Type | Semantics |
|---|---|---|
| `dndscv_qglobal_cv` | float64, nullable | dNdScv's per-cancer combined positive-selection q-value. Null when `dndscv_input_status != "tested_*"`. |
| `dndscv_significant_q05` | boolean, nullable | Convenience flag (`qglobal_cv < 0.05`). Null when not tested. |
| `dndscv_input_status` | category | One of: `not_run` (cancer type excluded by config or had zero variants), `below_threshold` (cancer type cohort smaller than `dndscv_min_samples`), `failed_qc` (dndscv stopped or returned no row for this gene), `tested_not_significant` (q ≥ 0.05), `tested_significant` (q < 0.05). |
| `dndscv_input_modality` | category | One of: `wes`, `panel`, `mixed`. Computed per (cancer_type, build) cohort from per-study `assay_type` metadata. |
| `dndscv_panel_only` | boolean | True iff the cohort feeding dndscv was 100% panel studies. Convenience flag derived from `dndscv_input_modality == "panel"`. |
| `dndscv_n_samples` | int64 | Sample count in the cohort dndscv was run on (per cancer_type, post-build-split). |
| `dndscv_n_variants` | int64 | Variant count in the cohort after `prepare_dndscv_input.py` filters. |
| `dndscv_split_build` | boolean | True if reconcile combined hg19 and hg38 sub-cohorts for this cancer type (per Decision #7). |
| `dndscv_refdb` | string | `"hg19"` or `"hg38"`. For split-build cancer types, the build of the lower-q sub-cohort. |
| `dndscv_package_version` | string | dNdScv R package `packageVersion("dndscv")` at run time. |
| `dndscv_git_sha` | string | Pinned dndscv commit SHA from `run_dndscv.R`. |

Naming follows the existing project convention (`bailey2018_driver` /
`bailey2018_source`, `cgc_tier_1` / `cgc_source`, `sanchez_vega_pathway` /
`sanchez_vega_source`): `<source>_<attribute>` for data, `<source>_<provenance>`
for versioning. The status column separates "not run" / "below threshold" /
"failed QC" / "tested not significant" / "tested significant" cleanly —
nullable-only would conflate the first three with the last.

## Scope

**In scope**
- `code/envs/dndscv.yml` — conda env for R + Bioconductor + dndscv runtime deps.
- Self-bootstrap of dndscv from pinned GitHub SHA inside `run_dndscv.R`.
- `code/scripts/prepare_dndscv_input.py` — new schema-validating + cancer-type-
  joining + SNV-restricting input preparation.
- `code/scripts/combine_mut_per_cancer_type.py` — new aggregation script.
- `code/scripts/run_dndscv.R` — rewritten for project-feather column conventions
  + self-bootstrap + `params.refdb` + retention-rate logging.
- `code/scripts/reconcile_dndscv_per_cancer.py` — new (combines per-build
  outputs back per cancer type with `dndscv_split_build` flag).
- `code/scripts/aggregate_dndscv_per_gene.py` — per-gene rollup across cancer
  types (min q + n_cancers_significant counts + best_cancer_type).
- `code/scripts/join_dndscv_into_annotated.py` — join per-(gene, cancer_type)
  dNdScv columns into `gene_cancer_study_ratio_annotated.feather`.
- `code/scripts/compare_three_way_rankings.py` — three-way per-gene ranking
  comparison feather, **with PubTator mention-count join**.
- `code/scripts/convert_to_feather.py` — extended to capture
  `reference_genome_id` from `meta_study.txt`; persist
  `studies/{id}/metadata/study_build.txt`.
- `code/workflows/Snakefile` — new rules + `conda:` directive on the new
  per-cancer dndscv rule + declared-input wiring for `meta_study.txt`.
- `code/config/config-pan-cancer-dndscv.yml` — side config that targets
  `all_with_dndscv` and supports `dndscv_wes_only`,
  `dndscv_min_samples`, `dndscv_min_variants`, and
  `study_reference_build_override`.
- `code/notebooks/t131_three_way_ranking_comparison.py` — marimo notebook,
  including PubTator-correlation panels.

**Out of scope (handled by separate tasks or filed on demand)**
- `task:t136` — canonicalize to GRCh38 at ingestion via liftover. Removes
  per-study refdb routing complexity entirely once shipped.
- Container/Docker recipe instead of conda.
- Sample-count-weighted aggregation across cancer types.
- Per-cancer-type panel-vs-WES exclusion config beyond the binary
  `dndscv_wes_only` switch.
- Vendored dndscv tarball if `install_github` becomes a recurring failure
  point.
- Replacing `bailey2018_driver` boolean column with a `dndscv_driver`
  column on the annotated feather (additive only; consumers opt in).
- Making indel-side dNdScv signal (`wind_cv`) a separate column;
  Phase 1 collapses to `qglobal_cv` only.

## Architecture

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Per-study chain                                                            │
│                                                                             │
│ raw cBioPortal study download                                               │
│       │                                                                      │
│       ▼  rule download_study  (extended: meta_study.txt as declared output) │
│                                                                             │
│ studies/{id}/raw/meta_study.txt                                             │
│       │                                                                      │
│       ▼  rule convert_to_feather  (extended: parse reference_genome_id)     │
│                                                                             │
│ studies/{id}/mut/table/mut.feather              ← UNFILTERED (Decision #3) │
│ studies/{id}/metadata/samples.feather                                       │
│ studies/{id}/metadata/study_build.txt   (NEW — "hg19" or "hg38",           │
│                                          fail-loud if absent per Decision #6) │
└────────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼  rule prepare_dndscv_input
                                                (Python — validate, join cancer_type, SNV-only)
┌────────────────────────────────────────────────────────────────────────────┐
│ studies/{id}/mut/dndscv_input.feather                                       │
│   columns: sample_id, cancer_type, chr, pos, ref, alt, build, modality      │
└────────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼  rule combine_mut_per_cancer_type
                                                (Python; splits by cancer_type × build)
┌────────────────────────────────────────────────────────────────────────────┐
│ summary/mut/dndscv_input/{cancer_type}__{build}/mut_combined.feather       │
│   one feather per (cancer_type, build) tuple. Empty tuples pruned.         │
│   Carries cohort-level metadata: n_samples, n_variants, modality.          │
└────────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼  rule run_dndscv_per_cancer
                                                (R, conda: ../envs/dndscv.yml,
                                                 params.refdb from {build} wildcard)
┌────────────────────────────────────────────────────────────────────────────┐
│ summary/mut/dndscv/per_cancer_per_build/{cancer_type}__{build}/genes.feather│
│   per-gene wmis/wnon/wspl/wind/qglobal_cv + cohort metadata + run provenance│
└────────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼  rule reconcile_dndscv_per_cancer
                                                (Python; combines build splits;
                                                 sets dndscv_split_build flag)
┌────────────────────────────────────────────────────────────────────────────┐
│ summary/mut/dndscv/per_cancer/{cancer_type}/genes.feather                  │
│   one row per gene per cancer type with all schema-contract columns         │
└────────────────────────────────────────────────────────────────────────────┘
                                  │
              ┌───────────────────┴───────────────────┐
              ▼                                       ▼
   rule join_dndscv_into_annotated         rule aggregate_dndscv_per_gene
              │                                       │
              ▼                                       ▼
   gene_cancer_study_ratio_annotated.feather   summary/mut/table/dndscv_pooled.feather
   (canonical output, additive schema           (one row per gene, pan-cancer rollup:
    per §"Schema contract")                      min_qglobal, n_cancers_significant,
                                                 best_cancer_type, n_cancers_tested)
                                                       │
                                                       ▼
                                              rule compare_three_way_rankings
                                                       │
                       (joins: dndscv_pooled, per-gene mean_inclusive/mean_adj,
                        protein_lengths, Bailey/CGC/CH flags,
                        PubTator gene_concept_ids.feather counts)
                                                       │
                                                       ▼
                       summary/mut/table/three_way_ranking_comparison.feather
                       columns: symbol, length, mean_inclusive, mean_adj,
                                pooled_qglobal, n_cancers_significant_q05,
                                pubtator_mention_count, pubtator_log10_mentions,
                                rank_raw, rank_length_adj, rank_dndscv,
                                three pairwise rank-shifts,
                                bailey_driver, cgc_tier_1, ch_priority_gene
                                                       │
                                                       ▼
                                          notebook (marimo) — per architecture
                                          §"Notebook detail" below.
```

### Per-cancer-type combine detail (`combine_mut_per_cancer_type.py`)

For each per-study `dndscv_input.feather`:
- Read with `cancer_type`, `study_id`, `modality` columns already attached
  by `prepare_dndscv_input.py`.
- Group rows by `cancer_type`.
- For each `(cancer_type, build)` group, append rows to the corresponding
  output feather.
- Compute and emit per-cohort metadata: `n_samples`, `n_variants`,
  `modality` (= `wes` if all source studies are wes, `panel` if all are
  panel, else `mixed`).
- If `dndscv_wes_only` config is set, drop panel-source rows before
  grouping.

Snakemake handles wildcard expansion: rule output is
`summary/mut/dndscv_input/{cancer_type}__{build}/mut_combined.feather`
and a Python helper computes the (cancer_type, build) tuples from the
filtered input set so empty combinations don't end up in the DAG.

### dNdScv per-cancer-type detail (rewritten `run_dndscv.R`)

- Self-bootstrap block at top: install pinned dndscv SHA from GitHub if
  not present.
- New required-cols check uses lowercase project-feather names:
  `sample_id`, `chr`, `pos`, `ref`, `alt`, `cancer_type`, `build`.
- Map directly to dndscv's expected schema (sampleID, chr, pos, ref, mut)
  without the v2 column-rename layer that was operating on absent columns.
- Pass `refdb = params.refdb` to the `dndscv()` call.
- Emit per-run log line: input rows, accepted rows, retention rate.
- On `dndscv` failure (e.g., too few synonymous mutations for stable fit),
  catch and emit an empty `genes.feather` with `failed_qc` status flag in
  the cohort metadata; downstream rules treat this as `dndscv_input_status
  = "failed_qc"`.
- Hypermutator filter retained (`max_coding_muts_per_sample = 3000`).

### Reconcile per-cancer detail (`reconcile_dndscv_per_cancer.py`)

For each cancer type:
- If only one build's per-cancer feather exists: pass-through, set
  `dndscv_split_build = false`, set `dndscv_refdb` from the present build.
- If both hg19 and hg38 per-cancer feathers exist: per gene, take min
  `qglobal_cv` across builds; set `dndscv_split_build = true`; set
  `dndscv_refdb` to the build of the lower-q sub-cohort. Emit a warning
  in the run log so the notebook can surface this as a known approximation.
- Carry forward all cohort metadata columns.

### Per-gene rollup detail (`aggregate_dndscv_per_gene.py`)

For each gene present in ≥1 per-cancer dNdScv output:
- `min_qglobal` = min `qglobal_cv` across cancer types.
- `n_cancers_significant_q05` = count of cancer types with q < 0.05.
- `n_cancers_significant_q01` = count of cancer types with q < 0.01.
- `best_cancer_type` = argmin cancer type.
- `n_cancers_tested` = count of cancer types where the gene appeared at all.

Rationale for **min-q rollup** rather than Stouffer: with per-cancer-type
combined MAFs, cohorts are biologically meaningful. A gene that is a strong
driver in even one cancer type should rank high pan-cancer; this is what
min-q captures. Stouffer would dilute strong-but-tissue-specific drivers
(BRAF in melanoma, KRAS in pancreatic) by averaging in non-significant
signal from unrelated cancer types.

### Join into annotated feather (`join_dndscv_into_annotated.py`)

Insert a new rule between `rule join_gene_cancer_meta_in_ratio_table` and
its consumers, reading per-(cancer_type) dndscv outputs + cohort metadata
and writing all columns from §"Schema contract" above. Existing columns
are preserved unchanged.

### Three-way comparison detail (`compare_three_way_rankings.py`)

- Aggregate `gene_cancer_study_ratio_annotated.feather` per gene by averaging
  `mean_inclusive` and `mean_adj` across cancer types (matches
  `question:0011-gene-length-as-literature-attention-confounder`).
- Join `dndscv_pooled.feather` (per-gene rollup) on `symbol` (left join).
- Join `protein_lengths.feather` for length context.
- Join Bailey / CGC / CH flags.
- **Join PubTator gene-mention counts from
  `/data/proj/lit-explore/pubtator/2026-01-16/counts/gene_concept_ids.feather`**
  on `symbol` (after HGNC alias normalization where it improves match rate).
  Compute `pubtator_log10_mentions = log10(pubtator_mention_count + 1)`.
- Compute three rank columns (raw and length-adjusted descending in score,
  dNdScv ascending in `min_qglobal`). Use dense rank.
- Compute three pairwise rank-shift columns (signed Δrank).

If the PubTator feather is unavailable (path resolution fails), emit a
warning, leave PubTator columns null, and proceed — the rest of the
comparison should still produce a valid feather. Notebook handles the
null-PubTator case with a "PubTator data not available" cell rather than
crashing.

### Notebook detail (`t131_three_way_ranking_comparison.py`)

Mirrors `q011_length_adjustment_topn_comparison.py`'s structure with
extensions:

1. Per-gene rollup head.
2. Three top-20 tables (raw / length-adjusted / dNdScv).
3. Spearman correlation **matrix** (3×3): raw, length-adjusted, dNdScv.
4. Jaccard@N table with three pairwise columns
   (raw↔length-adjusted, raw↔dNdScv, length-adjusted↔dNdScv).
5. Three scatter plots: length vs each score, colored by Bailey driver,
   labeled with canonical drivers.
6. **Recovery panel**: of Bailey drivers [@Bailey2018] in cohort, how many land in
   top-N for each scheme? Stratify by protein length quartile.
7. **Failure-mode panel**: top-100 of each scheme that are NOT Bailey
   drivers AND NOT CGC tier 1, by length quartile.
8. **Per-cancer significance heatmap**: `n_cancers_significant_q05`
   distribution; tissue-specific drivers visible as low cancer-counts
   but high biological recognition.
9. **PubTator correlation panel** (per Decision #9, Finding 3 in v2 review):
   - Per-list Spearman ρ vs `pubtator_log10_mentions` for raw,
     length-adjusted, dNdScv.
   - Jaccard@N between each ranking's top-N and PubTator's top-N.
   - Scatter: protein length vs PubTator mentions, colored by score
     bucket (top-100 in each ranking gets a category).
   - **Falsifier readout**: if dNdScv's PubTator-correlation is meaningfully
     lower than raw's, that is direct support for
     `question:0011-gene-length-as-literature-attention-confounder`'s central conjecture
     that gene length confounds the literature-attention axis through
     mutation count. If they're equal, the conjecture survives but
     length is purely a mediator. Either result is informative.
10. Synthesis cell.

## File-by-file delta

| Path | Status | Description |
|---|---|---|
| `code/envs/dndscv.yml` | new | r-base ≥4.3, r-arrow, r-remotes, r-devtools, bioconductor-genomicranges, bioconductor-biostrings, r-survival, r-mass, r-poilog (dndscv runtime deps) |
| `code/scripts/run_dndscv.R` | rewrite | Self-bootstrap pinned dndscv SHA. Accept `params.refdb`. Lowercase column contract. Failure → empty output + status flag. Per-run retention-rate log line. |
| `code/scripts/convert_to_feather.py` | edit | Capture `reference_genome_id` from `meta_study.txt`; write `studies/{id}/metadata/study_build.txt`. Fail loudly when unparseable + no override. |
| `code/scripts/prepare_dndscv_input.py` | new | Validate columns, join cancer_type from samples, restrict to SNVs, attach build + modality, write known-schema feather. |
| `code/scripts/combine_mut_per_cancer_type.py` | new | Aggregate per-study `dndscv_input.feather` into per-(cancer_type, build) MAFs; emit per-cohort metadata; honor `dndscv_wes_only`. |
| `code/scripts/reconcile_dndscv_per_cancer.py` | new | Combine per-build dndscv outputs back per cancer_type; set `dndscv_split_build`. |
| `code/scripts/aggregate_dndscv_per_gene.py` | new | Per-gene min-q rollup across cancer types → `summary/mut/table/dndscv_pooled.feather`. |
| `code/scripts/join_dndscv_into_annotated.py` | new | Join schema-contract columns into `gene_cancer_study_ratio_annotated.feather`. |
| `code/scripts/compare_three_way_rankings.py` | new | Three-way per-gene ranking comparison feather **including PubTator join** + null-safe PubTator handling. |
| `code/workflows/Snakefile` | edit | (a) Add `meta_study.txt` to download rule outputs and to `convert_to_feather` declared inputs. (b) Add `conda: "../envs/dndscv.yml"` to new dndscv rule. (c) New rules: `prepare_dndscv_input`, `combine_mut_per_cancer_type`, `run_dndscv_per_cancer`, `reconcile_dndscv_per_cancer`, `aggregate_dndscv_per_gene`, `join_dndscv_into_annotated`, `compare_three_way_rankings`, `all_with_dndscv`. (d) Insert join_dndscv_into_annotated between `join_gene_cancer_meta_in_ratio_table` and downstream consumers. |
| `code/config/config-pan-cancer-dndscv.yml` | new | Side config. Knobs: `dndscv_wes_only`, `dndscv_min_samples`, `dndscv_min_variants`, `study_reference_build_override`. Header documents the conda-env build cost and the fail-loud build-metadata behavior. |
| `code/notebooks/t131_three_way_ranking_comparison.py` | new | Marimo notebook per architecture sketch with PubTator-correlation panel. |
| `tasks/active.md` | edit | Mark t131 in-progress when implementation starts. |

## Risks

1. **First conda env build is slow and brittle.** R + Bioconductor +
   GitHub-pulled dndscv chain. ~5–15 min on warm cache, longer cold.
   Channel drift can break the build. Mitigation: pin r-base version
   explicitly; pin dndscv SHA; document build time in side-config header.
2. **dndscv `install_github` failure inside conda env.** GitHub rate
   limits or network failures. Mitigation: bootstrap block has a clear
   error message pointing to offline workarounds (manual clone +
   `R CMD INSTALL`). Future: vendored tarball.
3. **Per-study build metadata gaps in older studies.** Some pre-2014
   cBioPortal studies may have no `reference_genome_id` field or have it
   labeled non-standardly (`GRCh37`, `hg19`, `b37`). Mitigation:
   `convert_to_feather.py` normalizes to `"hg19"`/`"hg38"` with a small
   accepted-aliases list; if still unmatched, fail loudly naming the
   study and pointing to `study_reference_build_override` in the config
   (per Decision #6 — no silent default).
4. **Per-cancer-type cohort sizes too small.** Rare cancer types with few
   samples across studies will produce unreliable dNdScv results.
   Mitigation: config knobs `dndscv_min_samples` (default 50) and
   `dndscv_min_variants` (default 500); below thresholds the cohort is
   skipped at the combine step and downstream sees `dndscv_input_status =
   "below_threshold"`.
5. **Joining nullable dNdScv columns into the canonical annotated feather.**
   Downstream consumers may not expect the new nullable columns and could
   break on null-handling. Mitigation: nullable columns + status column
   with a category for every reason for nullness; nullable columns
   documented in `doc/guides/canonical-outputs.md`; the existing
   `mean_inclusive` and `mean_adj` columns are preserved unchanged so
   consumers that don't opt into the new columns are unaffected.
6. **Same-cancer-type-spans-both-builds case.** If a single cancer type
   has samples from both hg19 and hg38 studies, the reconcile step's min-q
   rollup may understate the true per-cancer significance (one build's q
   is based on only a subset of samples). Mitigation: `dndscv_split_build`
   flag; notebook surfaces split-build cancer types as a known
   approximation; long-term fix is t136.
7. **Panel-vs-WES mixing in the same per-cancer cohort.** dNdScv's global
   background degrades on small panels per the script's existing comment.
   Mitigation: `dndscv_input_modality` column so consumers can filter;
   `dndscv_wes_only` config knob for primary release runs.
8. **Empty `(cancer_type, build)` tuples in DAG.** Snakemake may try to
   materialize rules for empty combinations. Mitigation: input-resolution
   helper computes the tuple set from the actual prepared input feathers;
   only those tuples appear in the rule expansion.
9. **PubTator path unavailable.** Notebook needs to degrade gracefully if
   `/data/proj/lit-explore/...` is missing in some user's environment.
   Mitigation: null-safe join in `compare_three_way_rankings.py`; notebook
   "PubTator data not available" cell rather than crash.
10. **dndscv refdb-mismatch silent failure.** dndscv won't crash if input
    coordinates don't match its refdb — it silently drops variants. Without
    instrumentation we wouldn't know. Mitigation: `run_dndscv.R` emits the
    retention rate on every invocation; `reconcile_dndscv_per_cancer.py`
    propagates it; notebook surfaces low-retention cancer types.

## Validation steps

After implementation, before committing:

1. `uv run snakemake --lint -s code/workflows/Snakefile --configfile code/config/config-pan-cancer-dndscv.yml` — must pass.
2. `uv run snakemake -s code/workflows/Snakefile --dry-run --configfile code/config/config-pan-cancer-dndscv.yml all_with_dndscv` — must produce expected DAG without errors. (Does not require conda env to exist.)
3. `uv run --frozen ruff check` on all new Python scripts — must pass.
4. **Smoke tests** (per refinement bullet from review):
   - `prepare_dndscv_input.py` on existing `poc-2026-04-17` mut.feather:
     verify lowercase columns are accepted, samples join is correct, SNV
     filter is applied.
   - `combine_mut_per_cancer_type.py`: feed it a 2-study fixture with one
     cancer type spanning both, verify modality column is `mixed` only when
     it should be.
   - `combine_mut_per_cancer_type.py` with empty inputs: must not crash.
   - `convert_to_feather.py` build-metadata branch: feed it a study with a
     missing `reference_genome_id` and no override → must fail with the
     intended error message.
   - `convert_to_feather.py` build-metadata branch: feed it a study with a
     non-standard alias (`GRCh37`) → must normalize to `"hg19"`.
   - `reconcile_dndscv_per_cancer.py` with both build inputs present:
     verify `dndscv_split_build` is set true and refdb is the lower-q one.
   - `compare_three_way_rankings.py` with PubTator path absent: verify
     null PubTator columns + warning, no crash.
   - `aggregate_dndscv_per_gene.py` on synthetic per-cancer outputs: verify
     `gene_name` → `symbol` column normalization (dndscv outputs
     `gene_name`; project convention is `symbol`).
   - Notebook: `marimo export script code/notebooks/t131_three_way_ranking_comparison.py`
     must succeed.
5. **Optional `--use-conda` smoke test** (per refinement bullet): create a
   minimal `code/config/config-dndscv-smoke.yml` with one small WES study and
   one cancer type. User-runnable with
   `snakemake --use-conda all_with_dndscv --configfile code/config/config-dndscv-smoke.yml`;
   takes ~10 min including conda env build, ~1 min on subsequent runs.
   Documented in the side-config header. Not required for acceptance, but
   the smallest reproducible end-to-end check available.

**Not validated in this implementation pass:** full end-to-end snakemake
run with `--use-conda` on `config-pan-cancer-dndscv.yml`. That requires
real conda env build + per-cancer dNdScv runs across the full cohort
(~30+ minutes); user-driven kickoff.

## Out-of-scope follow-up tasks (filed separately)

- **t136** — Canonicalize to GRCh38 at ingestion via liftover.
- (To file on demand) Sample-count-weighted aggregation across cancer types.
- (To file on demand) Vendored dndscv tarball if `install_github` becomes a
  recurring failure point.
- (To file on demand) Container/Docker recipe replacing conda.
- (To file on demand) Indel-side dNdScv signal (`wind_cv`) as a separate
  column.
- (To file on demand) HGNC alias normalization for the PubTator join (would
  improve match rate) — currently scoped under `task:t082`.

## Acceptance criteria

This task is done when:

1. `code/envs/dndscv.yml` exists and validates as parseable YAML.
2. `code/scripts/run_dndscv.R` self-bootstraps dndscv, accepts
   `params.refdb`, and uses the lowercase project-feather column contract
   (closes the latent bug from §"Latent bug found during planning").
3. `convert_to_feather.py` captures and persists `study_build` per study;
   fails loudly on missing/unparseable build metadata absent an override.
4. All new Python scripts exist, pass ruff, and pass the smoke tests in
   §"Validation steps".
5. New rules are wired into the Snakefile and the dry-run DAG resolves.
6. `gene_cancer_study_ratio_annotated.feather` schema includes the columns
   from §"Schema contract on canonical feather"; existing columns
   unchanged.
7. `code/config/config-pan-cancer-dndscv.yml` exists with all four config
   knobs from the In-scope list; snakemake lint passes against it.
8. `code/notebooks/t131_three_way_ranking_comparison.py` parses
   (`marimo export script` succeeds) and includes the PubTator-correlation
   panel from §"Notebook detail" item 9.
9. A commit ships the lot with a discussion-style commit message linking
   back to `discussion:2026-04-24-gene-length-bias`, `q011`, `t136`, and
   noting the `run_dndscv.R` latent bug fix.

## Reproducibility covenant

- conda env file is checked in.
- dndscv GitHub SHA is pinned in `run_dndscv.R` and recorded in the run log
  for every dndscv invocation; surfaced as `dndscv_git_sha` column on the
  canonical feather.
- Per-study build inference rules are deterministic given the same
  `meta_study.txt` files, with explicit override config for non-standard
  metadata.
- min-q rollup is deterministic given the same per-cancer dNdScv outputs.
- All new pipeline outputs are written under the existing `out_dir` tree;
  no out-of-band side-effects.
