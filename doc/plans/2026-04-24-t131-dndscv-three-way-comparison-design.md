# t131 — dNdScv selection-based driver detection + three-way ranking comparison — design

- **Task:** t131 (Opt dNdScv into rule all via config-pan-cancer-dndscv.yml + three-way ranking comparison)
- **Priority:** P2
- **Related discussion:** `discussion:2026-04-24-gene-length-bias-in-mutation-rankings-and-literature`
- **Related question:** `question:q011-gene-length-as-literature-attention-confounder`
- **Related topic:** `topic:mutation-rate-normalization`
- **Related paper:** `paper:Martincorena2017`
- **Companion follow-up task:** `task:t136` (canonicalize-to-GRCh38 at ingestion — long-term build strategy)
- **Status:** design v2 proposed 2026-04-24, awaiting approval

## Goal

Produce a per-(gene, cancer_type) dNdScv selection signal that is (a) ingested
into the canonical pipeline output `gene_cancer_study_ratio_annotated.feather`
as new columns and (b) consumed by a per-gene three-way ranking comparison
notebook + feather artifact.

| Ranking | Source | What it measures |
|---|---|---|
| Raw mutation frequency | `gene_cancer_study_ratio_annotated.feather`, `mean_inclusive` (pan-cancer mean across cancer types) | Recurrence — biased toward long genes |
| Length-adjusted | `mean_adj` = `mean_inclusive / protein_length` | First-order length correction — biased toward tiny proteins (q011 notebook empirical result) |
| Selection-based | dNdScv per-cancer-type `qglobal_cv`, rolled up per gene by min-q across cancer types | Excess of non-synonymous over synonymous mutations relative to trinucleotide-aware background — length-aware by construction |

The empirical result from `code/notebooks/q011_length_adjustment_topn_comparison.py`
(Spearman ρ = 0.372, Jaccard@100 = 0.015 between raw and length-adjusted)
established that neither raw counts nor length-only adjustment produces a
defensible head-of-distribution. The deliverable answers: does dNdScv produce
a ranking that overlaps better with one of the two simpler scores than they
do with each other, and which canonical drivers (Bailey 299, CGC tier 1)
recover under each scoring scheme?

## Decisions baked in (v2)

These were surfaced and revised during planning. Document them so a future
agent doesn't relitigate.

1. **R via conda YAML, not Docker.** Matches the existing `code/envs/r-meta.yml`
   pattern used by `rule run_gene_cancer_meta_analysis`. Respects the
   `feedback:r-reproducibility` memory. Self-bootstrap dndscv from a pinned
   GitHub SHA at first run since dndscv is not on conda-forge or Bioconductor.
   Trade-off: first-time env build is slow (~5–15 min) and brittle if conda
   channels drift.

2. **Per-cancer-type combined MAF granularity** (revised from v1's per-study).
   New rule `combine_mut_per_cancer_type` aggregates per-study `mut_filtered.feather`
   files into per-cancer-type combined MAFs. dNdScv is invoked once per cancer
   type rather than once per study. Trade-off: per-cancer cohorts are
   biologically the right unit of selection (matches dNdScv's intended use per
   Martincorena 2017); removes the awkward Stouffer-of-q-values step from v1.
   Cost: a new combine rule and a new wildcard dimension. The existing
   per-study `rule run_dndscv` is preserved as a fallback / alternate target
   but is not on the t131 critical path.

3. **dNdScv signal joined into the canonical pipeline output** (revised from
   v1's "comparison-only output"). New columns `dndscv_qglobal` (per
   (gene, cancer_type)) and `dndscv_significant_q05` (boolean) are joined into
   `gene_cancer_study_ratio_annotated.feather` so the new signal ships in the
   canonical artifact every consumer reads. Trade-off: downstream consumers
   may shift their ranking source. Mitigation: the existing `mean_inclusive`
   and `mean_adj` columns are preserved unchanged; consumers opt into the new
   column explicitly. The dNdScv columns are nullable for genes / cancer
   types where dNdScv didn't run or produced no result.

4. **Per-study refdb routing** (revised from v1's "GRCh37-only"). The dNdScv
   rule reads each study's reference genome from cBioPortal `meta_study.txt`
   (`reference_genome_id: hg19` or `hg38`) propagated through to a per-study
   metadata column, and selects the matching dndscv RefCDS (`hg19` or `hg38`).
   Trade-off: the new per-cancer-type combined MAFs may mix studies of
   different builds. **Resolution:** combine rule splits per-cancer-type MAFs
   by build, so each invocation of dNdScv sees one build. Cost: a per-cancer ×
   per-build wildcard expansion. Empty combinations are pruned.
   This is the *interim* answer — the long-term destination is canonical
   GRCh38 throughout the pipeline (`task:t136`).

5. **Side-config + side-target, not modifying default rule all.** New
   `rule all_with_dndscv:` in the Snakefile, invoked via
   `snakemake all_with_dndscv --configfile code/config/config-pan-cancer-dndscv.yml`.
   Default `rule all` stays R-free for users without conda. Trade-off:
   slightly more friction to opt in; cleanly separates the optional
   R-dependent surface.

## Scope

**In scope**
- `code/envs/dndscv.yml` — conda env for R + Bioconductor + dndscv runtime deps.
- Self-bootstrap of dndscv from pinned GitHub SHA inside `run_dndscv.R`.
- `code/scripts/combine_mut_per_cancer_type.py` — new aggregation script.
- `code/scripts/run_dndscv.R` — modified to (a) accept a `params.refdb` value
  ("hg19" or "hg38"), (b) self-bootstrap dndscv, (c) operate on combined
  per-cancer-type MAFs.
- `code/scripts/aggregate_dndscv_per_gene.py` — per-gene rollup across cancer
  types (min q + Bailey-driver-aware metadata).
- `code/scripts/join_dndscv_into_annotated.py` — join per-(gene, cancer_type)
  dndscv qglobal into `gene_cancer_study_ratio_annotated.feather`.
- `code/scripts/compare_three_way_rankings.py` — three-way per-gene ranking
  comparison feather.
- `code/workflows/Snakefile` — new rules + `conda:` directive on existing
  `run_dndscv` (preserved as fallback target).
- `code/config/config-pan-cancer-dndscv.yml` — side config that targets
  `all_with_dndscv` and pins per-study build metadata.
- `code/notebooks/t131_three_way_ranking_comparison.py` — marimo notebook.
- Per-study build inference: extend `convert_to_feather.py` to read
  `reference_genome_id` from `meta_study.txt` and persist into a per-study
  `metadata/study_build.txt` (or as a column in `metadata/studies.feather`).

**Out of scope (handled by separate tasks)**
- Canonicalize-to-GRCh38 at ingestion via liftover (`task:t136`). Removes
  the per-study refdb routing complexity entirely once shipped.
- Container/Docker recipe instead of conda.
- Per-cancer-type **and per-build** dNdScv outputs combined back into single
  per-cancer-type results (only matters when a single cancer type spans both
  builds — currently rare; defer until empirically problematic).
- Sample-count-weighted aggregation across cancer types (defer; min-q is the
  Phase-1 rollup).
- Replacing `bailey2018_driver` boolean column with a `dndscv_driver` column
  on the annotated feather (additive only in Phase 1; consumers opt in).

## Architecture

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Per-study chain (existing — unchanged except for build metadata capture)   │
│                                                                             │
│ raw cBioPortal study download                                               │
│       │                                                                      │
│       ▼  rule convert_to_feather  (extended: capture reference_genome_id)   │
│                                                                             │
│ studies/{id}/mut/table/mut_filtered.feather                                  │
│ studies/{id}/metadata/study_build.txt   (NEW — "hg19" or "hg38")           │
└────────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼  rule combine_mut_per_cancer_type
                                                (Python; splits by cancer_type × build)
┌────────────────────────────────────────────────────────────────────────────┐
│ summary/mut/dndscv_input/{cancer_type}__{build}/mut_combined.feather       │
│   one feather per (cancer_type, build) tuple. Empty tuples pruned.         │
└────────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼  rule run_dndscv_per_cancer
                                                (R, conda: ../envs/dndscv.yml,
                                                 params.refdb from wildcard)
┌────────────────────────────────────────────────────────────────────────────┐
│ summary/mut/dndscv/per_cancer_per_build/{cancer_type}__{build}/genes.feather│
└────────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼  rule reconcile_dndscv_per_cancer
                                                (Python; combines build splits per cancer_type)
┌────────────────────────────────────────────────────────────────────────────┐
│ summary/mut/dndscv/per_cancer/{cancer_type}/genes.feather                  │
│   one row per gene per cancer type with qglobal_cv (min across builds      │
│   when both ran for that cancer type).                                     │
└────────────────────────────────────────────────────────────────────────────┘
                                  │
              ┌───────────────────┴───────────────────┐
              ▼                                       ▼
   rule join_dndscv_into_annotated         rule aggregate_dndscv_per_gene
                                                       │
                                                       ▼
   gene_cancer_study_ratio_annotated.feather   summary/mut/table/dndscv_pooled.feather
   (NEW columns: dndscv_qglobal,                  (one row per gene, pan-cancer rollup:
    dndscv_significant_q05,                        min_qglobal, n_cancers_significant,
    dndscv_n_cancers_significant)                  best_cancer_type)
                                                       │
                                                       ▼
                                              rule compare_three_way_rankings
                                                       │
                                                       ▼
                       summary/mut/table/three_way_ranking_comparison.feather
                       columns: symbol, length, mean_inclusive, mean_adj,
                                pooled_qglobal, rank_raw, rank_length_adj,
                                rank_dndscv, three pairwise rank-shifts,
                                bailey_driver, cgc_tier_1, ch_priority_gene
                                                       │
                                                       ▼
                                          notebook (marimo) — top-N tables,
                                          Spearman 3×3, Jaccard@N, scatter
                                          plots, recovery panel, failure-mode panel.
```

### Per-cancer-type combine detail (`combine_mut_per_cancer_type.py`)

For each per-study `mut_filtered.feather`:
- Read with `cancer_type` and `study_id` columns.
- Look up `study_build` from `studies/{id}/metadata/study_build.txt`.
- Group rows by `cancer_type`.
- For each `(cancer_type, build)` group, append rows to the corresponding
  output feather.

Snakemake handles the wildcard expansion: the rule's `output:` is
`summary/mut/dndscv_input/{cancer_type}__{build}/mut_combined.feather` and
the `input:` is the full set of `mut_filtered.feather` plus build metadata.
A Python helper computes the (cancer_type, build) tuples from the filtered
input set so empty combinations don't end up in the DAG.

### dNdScv per-cancer-type detail (modified `run_dndscv.R`)

- New `params.refdb` value passed in via the wildcard (`{build}` → `"hg19"`
  or `"hg38"`).
- Self-bootstrap block at top: install pinned dndscv SHA from GitHub if not
  already present.
- Pass `refdb = params.refdb` to the `dndscv()` call.
- Emit a per-run log line summarizing variant retention rate (raw input rows
  vs rows accepted by dndscv after coordinate validation) — used by the
  notebook to flag low-quality cancer types.
- Hypermutator filter retained (`max_coding_muts_per_sample = 3000`); the
  pipeline's separate hypermutator annotation is independent and orthogonal.

### Reconcile per-cancer detail (`reconcile_dndscv_per_cancer.py`)

For cancer types where both hg19 and hg38 builds ran (rare in practice;
current cohort is mostly mono-build per cancer type):
- Per gene, take min `qglobal_cv` across builds.
- Sum `n_significant` flags.
- Carry the per-build retention rate forward as metadata.

This step is mostly a no-op for the current cohort but exists to handle the
general case correctly.

### Per-gene rollup detail (`aggregate_dndscv_per_gene.py`)

For each gene present in ≥1 per-cancer dNdScv output:
- `min_qglobal` = min across cancer types.
- `n_cancers_significant_q05` = count of cancer types with q < 0.05.
- `n_cancers_significant_q01` = count of cancer types with q < 0.01.
- `best_cancer_type` = argmin cancer type.
- `n_cancers_tested` = count of cancer types where the gene appeared at all.

Rationale for **min-q rollup** rather than Stouffer: with per-cancer-type
combined MAFs (decision #2), the cohorts are biologically meaningful (one
cancer type's selection regime). A gene that is a strong driver in even
one cancer type should rank high pan-cancer; this is what min-q captures.
Stouffer would dilute strong-but-tissue-specific drivers (BRAF in
melanoma; KRAS in pancreatic) by averaging in non-significant signal from
unrelated cancer types.

### Join into annotated feather (`join_dndscv_into_annotated.py`)

Modify `rule join_gene_cancer_meta_in_ratio_table` (or insert a new rule
between it and downstream consumers) so the final
`gene_cancer_study_ratio_annotated.feather` carries:
- `dndscv_qglobal` (per (gene, cancer_type), nullable)
- `dndscv_significant_q05` (per (gene, cancer_type), nullable)
- `dndscv_pipeline_version` (string, pinned dndscv SHA)

Existing columns are preserved unchanged. Null values mean "dNdScv did not
run or did not return a result for this (gene, cancer_type)" — that's a
distinct signal from "ran but not significant", and consumers should treat
the two cases separately.

### Three-way comparison detail (`compare_three_way_rankings.py`)

- Aggregate `gene_cancer_study_ratio_annotated.feather` per gene by averaging
  `mean_inclusive` and `mean_adj` across cancer types (matches q011 notebook).
- Join `dndscv_pooled.feather` (per-gene rollup) on `symbol` (left join).
- Join `protein_lengths.feather` for length context.
- Join Bailey / CGC / CH flags.
- Compute three rank columns: raw and length-adjusted descending in score,
  dNdScv ascending in `min_qglobal` (lower q = higher significance). Use
  dense rank.
- Compute three pairwise rank-shift columns (signed Δrank).

### Notebook detail (`t131_three_way_ranking_comparison.py`)

Mirrors `q011_length_adjustment_topn_comparison.py`'s structure with
extensions:

1. Per-gene rollup head.
2. Three top-20 tables (raw / length-adjusted / dNdScv).
3. Spearman correlation **matrix** (3×3).
4. Jaccard@N table with three pairwise columns.
5. Three scatter plots: length vs each score, colored by Bailey driver,
   labeled with canonical drivers.
6. **Recovery panel**: of Bailey 2018 drivers in cohort, how many land in
   top-N for each scheme? Stratify by protein length quartile to show
   *which* Bailey drivers each scheme misses.
7. **Failure-mode panel**: top-100 of each scheme that are NOT Bailey drivers
   AND NOT CGC tier 1, by length quartile.
8. **Per-cancer significance heatmap** (new): `n_cancers_significant_q05`
   distribution; tissue-specific drivers should be visible as low cancer
   counts but high biological recognition.
9. Synthesis cell.

## File-by-file delta

| Path | Status | Description |
|---|---|---|
| `code/envs/dndscv.yml` | new | r-base ≥4.3, r-arrow, r-remotes, r-devtools, bioconductor-genomicranges, bioconductor-biostrings, r-survival, r-mass, r-poilog (dndscv runtime deps) |
| `code/scripts/run_dndscv.R` | edit | Self-bootstrap pinned dndscv SHA. Accept `params.refdb`. Emit per-run retention-rate log line. Operate on combined per-cancer-type MAFs. |
| `code/scripts/convert_to_feather.py` | edit | Capture `reference_genome_id` from `meta_study.txt`; write `studies/{id}/metadata/study_build.txt`. |
| `code/scripts/combine_mut_per_cancer_type.py` | new | Aggregate per-study `mut_filtered.feather` into per-(cancer_type, build) MAFs. |
| `code/scripts/reconcile_dndscv_per_cancer.py` | new | Combine per-build dndscv outputs back to one per-cancer-type result (no-op for mono-build cancer types). |
| `code/scripts/aggregate_dndscv_per_gene.py` | new | Per-gene min-q rollup across cancer types → `summary/mut/table/dndscv_pooled.feather`. |
| `code/scripts/join_dndscv_into_annotated.py` | new | Join per-(gene, cancer_type) dNdScv qglobal into `gene_cancer_study_ratio_annotated.feather`. |
| `code/scripts/compare_three_way_rankings.py` | new | Three-way per-gene ranking comparison feather. |
| `code/workflows/Snakefile` | edit | (a) Add `conda: "../envs/dndscv.yml"` to existing per-study `rule run_dndscv`. (b) Add `rule combine_mut_per_cancer_type`. (c) Add `rule run_dndscv_per_cancer` (separate rule from the per-study one — both kept). (d) Add `rule reconcile_dndscv_per_cancer`. (e) Add `rule aggregate_dndscv_per_gene`. (f) Modify or wrap `rule join_gene_cancer_meta_in_ratio_table` to include the dndscv join. (g) Add `rule compare_three_way_rankings`. (h) Add `rule all_with_dndscv`. |
| `code/config/config-pan-cancer-dndscv.yml` | new | Side config mirroring `config-pan-cancer.yml`. Header documents the conda-env build cost and the per-study build inference behavior. |
| `code/notebooks/t131_three_way_ranking_comparison.py` | new | Marimo notebook per architecture sketch. |
| `tasks/active.md` | edit | Mark t131 in-progress when implementation starts. |

## Risks

1. **First conda env build is slow and brittle.** R + Bioconductor + GitHub-pulled
   dndscv chain. ~5–15 min on warm cache, longer cold. Channel drift can break
   the build. Mitigation: pin r-base version explicitly; pin dndscv SHA; document
   build time in side-config header.
2. **dndscv `install_github` failure inside conda env.** GitHub rate limits or
   network failures. Mitigation: bootstrap block has a clear error message
   pointing to offline workarounds (manual clone + `R CMD INSTALL`). Future:
   vendored tarball under `data/dndscv-<sha>.tar.gz`.
3. **Per-study build metadata gaps.** Some older cBioPortal studies may have
   no `reference_genome_id` field, or have it labeled non-standardly
   (`GRCh37`, `hg19`, `b37`). Mitigation: `convert_to_feather.py` normalizes
   to `"hg19"`/`"hg38"` with explicit fallback for missing/unknown values
   (default to `"hg19"` for legacy studies, log a warning, surface the
   per-study build choice in `metadata/studies.feather`).
4. **Per-cancer-type cohort sizes too small.** Rare cancer types with few
   samples across studies will produce unreliable dNdScv results (the script's
   <100-variant warning fires). Mitigation: emit a `min_samples_threshold`
   config knob (default 50 samples or 500 variants); cancer types below the
   threshold are excluded from the dNdScv output but still appear in the
   downstream join (with null dndscv columns).
5. **Joining nullable dNdScv columns into the canonical annotated feather.**
   Downstream consumers may not expect the new nullable columns and could
   break on null-handling. Mitigation: nullable columns documented in
   `doc/guides/canonical-outputs.md`; `pipeline_version` column updated so
   consumers can detect schema change; the existing `mean_inclusive` and
   `mean_adj` columns are preserved unchanged so consumers that don't opt
   into the new columns are unaffected.
6. **Rare same-cancer-type-spans-both-builds case.** If a single cancer type
   has samples from both hg19 and hg38 studies, the reconcile step's min-q
   rollup may understate the true per-cancer significance (one build's q is
   based on only a subset of samples). Mitigation: log when this case
   triggers; flag in the comparison notebook for manual review; long-term
   fix is t136 (canonical GRCh38 ingestion).
7. **MSK-IMPACT-style panel data is genuinely incompatible with dNdScv's
   global background.** Per-cancer combined MAFs that mix WES + panel
   studies will have heterogeneous coverage. Mitigation: include them in
   Phase 1 with a warning in the comparison notebook; add a config-driven
   exclusion list as a follow-up task if results look noisy.
8. **Empty (cancer_type, build) tuples in DAG.** Snakemake may try to
   materialize rules for empty combinations. Mitigation: input-resolution
   helper computes the tuple set from the actual filtered MAFs and only
   those tuples appear in the rule expansion.

## Validation steps

After implementation, before committing:

1. `uv run snakemake --lint -s code/workflows/Snakefile --configfile code/config/config-pan-cancer-dndscv.yml` — must pass.
2. `uv run snakemake -s code/workflows/Snakefile --dry-run --configfile code/config/config-pan-cancer-dndscv.yml all_with_dndscv` — must produce expected DAG without errors. (Does not require conda env to exist.)
3. `uv run --frozen ruff check` on all new scripts — must pass.
4. Smoke-test the Python scripts on the existing `poc-2026-04-17` outputs
   where possible (combine, aggregate, compare). The dNdScv-R step itself
   cannot be smoke-tested without the conda env.
5. `marimo export script code/notebooks/t131_three_way_ranking_comparison.py`
   must succeed (parse-level validation).

**Not validated in this implementation pass:** actual end-to-end snakemake
run with `--use-conda`. That requires building the conda env and running
dNdScv on real cohorts (slow; user-driven kickoff).

## Out-of-scope follow-up tasks (filed separately)

- **t136** — Canonicalize to GRCh38 at ingestion via liftover. Long-term
  destination; removes per-study refdb routing complexity entirely.
- (To file on demand) Sample-count-weighted aggregation across cancer types.
- (To file on demand) Per-cancer-type panel-vs-WES exclusion config.
- (To file on demand) Vendored dndscv tarball if `install_github` becomes a
  recurring failure point.
- (To file on demand) Container/Docker recipe replacing conda.

## Acceptance criteria

This task is done when:

1. `code/envs/dndscv.yml` exists and validates as parseable YAML.
2. `code/scripts/run_dndscv.R` self-bootstraps dndscv if not present and
   accepts `params.refdb`.
3. `convert_to_feather.py` captures and persists `study_build` per study.
4. `combine_mut_per_cancer_type.py`, `reconcile_dndscv_per_cancer.py`,
   `aggregate_dndscv_per_gene.py`, `join_dndscv_into_annotated.py`,
   `compare_three_way_rankings.py` exist, pass ruff, and handle
   empty / partial inputs without crashing.
5. New rules are wired into the Snakefile and the dry-run DAG resolves.
6. `gene_cancer_study_ratio_annotated.feather` schema includes the three
   new dNdScv columns; existing columns are unchanged.
7. `code/config/config-pan-cancer-dndscv.yml` exists; snakemake lint passes
   against it.
8. `code/notebooks/t131_three_way_ranking_comparison.py` parses
   (`marimo export script` succeeds).
9. A commit ships the lot with a discussion-style commit message linking to
   `discussion:2026-04-24-gene-length-bias`, `q011`, `t136`.

## Reproducibility covenant

- conda env file is checked in.
- dndscv GitHub SHA is pinned in `run_dndscv.R` and recorded in the run log
  for every dndscv invocation.
- Per-study build inference rules are deterministic given the same
  `meta_study.txt` files.
- min-q rollup is deterministic given the same per-cancer dNdScv outputs.
- All new pipeline outputs are written under the existing `out_dir` tree;
  no out-of-band side-effects.
