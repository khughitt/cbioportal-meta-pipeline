# MSK-IMPACT panel-version drift handling per sample (t070) — design

> **For Claude:** REQUIRED SUB-SKILL: use `superpowers:writing-plans` to translate this design into an executable implementation plan. This document is the spec; the plan is the next artifact.

**Closes:** audit finding F6 (`doc/audits/2026-04-13-create-combined-gene-cancer-freq-table-audit.md`).
**Task:** `t070` (`tasks/active.md`).

## Goal

Treat MSK-IMPACT cohorts as a per-sample mixture of panel versions (IMPACT-341 / 410 / 468 / 505 / IMPACT-HEME-400) rather than a single per-study panel. For genes added in IMPACT-410+ (or IMPACT-468+, IMPACT-505+), restrict the per-(cancer, gene) sample-frequency denominator to samples whose panel actually covers the gene, and key the per-sample TMB denominator on the sample's own panel rather than a study-wide assumption.

## Problem statement (recap)

Empirical audit (2026-04-18) of locally-available MSK studies:

| Study | Samples | Panel-resolved | Distribution |
|---|---|---|---|
| `msk_impact_2017` | 10,945 | 100% | IMPACT-410 (74%), 341 (26%) |
| `msk_chord_2024` | 25,040 | 100% | IMPACT-468 (51%), 505 (29%), 410 (16%), 341 (4%) |
| `msk_met_2021` | 25,775 | 100% | IMPACT-468 (68%), 410 (25%), 341 (7%) |
| `heme_msk_impact_2022` | 2,383 | 99.96% | IMPACT-HEME-400 (1 sample missing) |
| `msk_ch_2023` | n/a | (no matrix file; suffix-inferable) | clonal-hematopoiesis call set; panel encoded in sample-id suffix `-IM3`/`-IM5`/`-IM6`/`-IM7` |

Per-sample panel info lives in cBioPortal's `data_gene_panel_matrix.txt`, which the pipeline does **not** currently ingest. As a result:

- A gene added in IMPACT-468 has its `msk_met_2021` per-cancer rate deflated by ~32% (the IMPACT-341 + 410 fraction sequenced before that gene was on the panel) — silently, because non-mutated panel-uncallable samples currently land in the denominator as if they were observed-and-negative.
- The TMB denominator for MSK samples falls through to `wes_default_callable_mb = 30 Mb` (config-poc.yml comment, 2026-04-17), inflating TMB by ~25–30× and breaking the downstream GMM fit.

cBioPortal's panel-name convention (`IMPACT341`) differs from GENIE's (`MSK-IMPACT341`) and from the canonical form used in `panel_callable_mb_override` config keys (`MSK-IMPACT-341`). Naming normalization is a load-bearing piece of this fix.

## Architecture

```
data_gene_panel_matrix.txt ─┐
data_clinical_sample.txt ───┼──> convert_to_feather.py ──> samples.feather (+ panel_id)
                            │
       (sample-id suffix fallback for studies without matrix file)
                            │
                            ▼
samples.feather ──> create_freq_tables.py            (per-(gene, cancer) denominator panel-aware)
samples.feather ──> compute_per_sample_tmb.py        (per-sample callable_mb keyed on panel_id)
samples.feather ──> create_combined_gene_cancer_freq_table.py
                                                      (callability annotation becomes
                                                       sample-weighted in addition to
                                                       study-binary)
```

One canonical column — `panel_id` on `samples.feather` — drives every consumer. Naming is normalized once, on ingest, to the form used in `panel_callable_mb_override` config keys (e.g., `MSK-IMPACT-341`). All consumers do a single lookup against this column.

## Components

### Component 1 — `code/scripts/resolve_panel_id.py` (new)

Pure resolution module. ~80 lines, no I/O.

```python
PANEL_ALIASES: dict[str, str] = {
    "IMPACT341": "MSK-IMPACT-341",
    "MSK-IMPACT341": "MSK-IMPACT-341",
    "MSK-IMPACT-341": "MSK-IMPACT-341",
    "IMPACT410": "MSK-IMPACT-410",
    # ...341/410/468/505 + MSK-IMPACT-HEME-400 + MSK-IMPACT-HEME-V2 variants
    # Canonical form for all heme variants is MSK-IMPACT-HEME-{version} (matches
    # the MSK-IMPACT-XXX pattern used in panel_callable_mb_override config keys).
}

SAMPLE_ID_SUFFIX_MAP: dict[str, str] = {
    "IM3": "MSK-IMPACT-341",
    "IM5": "MSK-IMPACT-410",
    "IM6": "MSK-IMPACT-468",
    "IM7": "MSK-IMPACT-505",
    "IH3": "MSK-IMPACT-HEME-400",
}

def normalize_panel_id(raw: str) -> str:
    """Canonicalize a raw panel string. Raises ValueError on unknown."""

def infer_panel_from_sample_id(sample_id: str) -> str | None:
    """Parse the trailing `-IM[3567]` / `-IH3` suffix; None if absent."""

def resolve_panel_ids(
    samples: pd.DataFrame,
    matrix: pd.DataFrame | None,
    study_id: str,
    study_panel_map: dict[str, str],
    is_panel_study: bool,
) -> pd.Series:
    """Return panel_id Series indexed like samples. See behavior contract below."""
```

Behavior contract:

- **Panel-study classification is set by the caller** via the workflow's `panel_bearing_studies` config list (see Component 2). The function takes an explicit `is_panel_study: bool` argument; the caller decides. This separates classification (config concern) from resolution (function concern).
- **For panel studies** (`is_panel_study=True`), the per-sample resolution chain is:
  1. `matrix['mutations']` column normalized via `PANEL_ALIASES` (preferred when matrix is non-None)
  2. `SAMPLE_ID_SUFFIX_MAP` applied to `sample_id`
  3. `study_panel_map[study_id]` (single panel applied to all samples)

  Every sample must resolve via 1, 2, or 3 — anything unresolved raises `ValueError` carrying `(study_id, sample_id, raw_value)`.
- **For non-panel studies** (`is_panel_study=False`), the function returns `None` for every sample. The resulting `panel_id` column on `samples.feather` is `None`, signaling to downstream consumers that the panel-aware path is bypassed (current scalar-per-cancer denominator behavior preserved).

Reference data citations: Cheng 2015 (PMID 25801821) for IMPACT-341/410, Zehir 2017 (PMID 28481359) for IMPACT-410/468 transition, Bandlamudi 2026 (PMID 41895280) for IMPACT-505. Cited inline in module docstring.

### Component 2 — `code/scripts/convert_to_feather.py` (extension) + Snakemake DAG wiring

A new config key `panel_bearing_studies: list[str]` enumerates studies that ship a `data_gene_panel_matrix.txt` (or are otherwise expected to resolve panels per-sample). This is a **static classification**, not runtime detection — it makes the DAG deterministic and matches the existing `matched_normal_studies` / `study_panel_map` config-driven pattern.

Snakemake DAG wiring:

- `download_study` rule: when `wildcards.id in panel_bearing_studies`, also fetch `data_gene_panel_matrix.txt` and declare it as a fourth output. (cBioPortal study tarballs include this file when present, so this is a download-list change, not a separate fetch.)
- `convert_to_feather` rule: input list becomes 3 fixed + 1 conditional via an input function `_convert_inputs(wildcards)` that appends the matrix path iff the study is panel-bearing. The script reads `snakemake.input.panel_matrix` (a named input) when present, passes `None` otherwise.

Bootstrap: empirically every MSK study with a per-sample matrix file (audit table in Problem Statement) goes into `panel_bearing_studies`. Any study whose ingestion later reveals a panel matrix that wasn't declared raises a config error during `convert_to_feather`.

After reading inputs, call `resolve_panel_ids` and attach the resulting `panel_id` column to `samples.feather`. ~25 lines added across script + Snakefile.

The existing `seq_assay_id` column (GENIE-only) is preserved and remains GENIE-specific. `panel_id` is the canonical column for all downstream consumers; `seq_assay_id` becomes a raw-source column kept for traceability only.

### Component 3 — `code/scripts/create_freq_tables.py` (modified)

Per-study aggregation gains panel-awareness for the gene-bearing tables.

- **`gene.feather`** (gene-keyed): denominator becomes per-gene = count of samples where the sample's panel covers the gene.
- **`gene_cancer.feather`** (`(cancer_type, symbol)`-keyed): denominator becomes per-(cancer, gene) = count of samples in that cancer-type where the sample's panel covers the gene.
- **`cancer_type.feather` / `cancer_type_detailed.feather`**: unchanged — no gene dimension, panel doesn't apply.

Implementation: small `(panel_id, gene) → bool` callability table derived from `genie_panel_coverage.feather`. Per-study, restrict to `(panel_id, gene)` pairs where the panel is one of those used in the study's samples. Left-join against the study's sample table to enumerate `(sample_id, cancer_type, panel_id, gene)` rows where the gene is callable; group to get the panel-aware denominator.

For studies where every sample's `panel_id` is `None` (WES studies), the panel-aware path is bypassed and current scalar-per-cancer denominators are preserved.

**Prerequisite check (fail-loud):** for any non-null `panel_id` value appearing in the study, the `(panel_id, gene)` callability table derived from `genie_panel_coverage.feather` must contain entries for that panel. A panel that resolves but has no coverage rows raises:

```
ValueError(f"Panel {panel_id!r} used in study {study_id} but has no coverage entries in
genie_panel_coverage.feather. Either supply BED-derived coverage (preferred), or remove the
panel from PANEL_ALIASES, or remove the study from panel_bearing_studies.")
```

This catches the case where a panel can be resolved (alias known) and TMB-denominated (Mb override known) but cannot be used for gene-aware aggregation. TMB-only panels are valid; they just must not be used in panel-aware aggregation paths.

Memory note: 25k samples × ≤505 genes per panel ≈ 12M rows max — fine for in-memory pandas.

No `panel_aware` flag column is emitted; the count columns themselves convey panel-restriction (when `n_samples_inclusive` for a (cancer, gene) row is less than the cohort size for that cancer, restriction was applied).

### Component 4 — `code/scripts/compute_per_sample_tmb.py` (modified)

Replace the current `panel_id = study_panel_map.get(study_id)` (line 162) with a per-sample lookup against `samples["panel_id"]`. Each sample's TMB denominator becomes `panel_callable_mb[sample.panel_id]`. ~10 lines changed; no new files.

For samples where `panel_id` is `None` (WES studies), behavior is identical to today (falls through to `wes_default_callable_mb`).

### Component 5 — `code/scripts/create_combined_gene_cancer_freq_table.py` (modified, `_annotate_callability`)

**Data-flow precondition (resolves cross-study underspecification):** to compute sample-weighted callability, the combined step needs per-(study, cancer, gene) sample counts that are **already panel-restricted at the per-study layer** (Component 3 produces them). These are NOT in the current `gene_cancer_study.feather` output. Two columns must be propagated upstream:

- Per-study `gene_cancer.feather` already carries `n_samples_inclusive` and `n_samples_exclusive` keyed on (cancer_type, symbol). After Component 3 lands, these values are panel-restricted.
- The combined script's `combine_paired_pivot` is extended to also pivot these two columns into wide per-study matrices `n_inclusive_df` and `n_exclusive_df` (parallel to `num_df` and `ratio_df`), keyed on (cancer_type, symbol) with one column per study.
- `_annotate_callability` takes these two new matrices as additional arguments.

Three changes to the annotation itself:

- **Redefine `n_panel_covered_studies` for panel-mixed studies**: a study contributes to a gene's count if ≥1 of that study's per-sample panels covers the gene (binary per study). Preserves the column's interpretive meaning ("this study could in principle have observed this gene") without conflating sample mixture into the study-level count.
- **Add paired sample-weighted columns:**
  - `n_panel_covered_samples_inclusive : int` — for each (cancer, gene) row, sum over studies of the per-(study, cancer, gene) panel-restricted inclusive denominator (= `n_inclusive_df.sum(axis=1, skipna=True)`).
  - `n_panel_covered_samples_exclusive : int` — same, but using the exclusive (hypermutator-removed) per-study denominator.
  - These differ by the count of panel-callable hypermutator samples for that gene/cancer. Both are needed because the existing inclusive/exclusive ratio columns each demand their own denominator.
- **Define `n_total_samples_in_cancer` precisely**: for a `(cancer_type, symbol)` row, total samples in that cancer-type across all studies (sum of cohort sizes for that cancer in each study, regardless of panel coverage). This is the cancer-specific denominator that makes `callable_sample_fraction` meaningful as "fraction of cancer-X samples sequenced on a panel that covers this gene". It does **not** condition on panel coverage; that is the ratio's job.
- **Add paired callable_sample_fraction columns:**
  - `callable_sample_fraction_inclusive = n_panel_covered_samples_inclusive / n_total_samples_in_cancer`
  - `callable_sample_fraction_exclusive = n_panel_covered_samples_exclusive / n_total_samples_in_cancer_exclusive` (where the denominator likewise excludes hypermutators).

Existing `callable_fraction = n_panel_covered_studies / n_total_studies` semantics preserved.

## Data flow & schema changes

### `samples.feather` (per-study, in `out_dir/studies/{id}/metadata/`)

| Column | Type | Source | Notes |
|---|---|---|---|
| `panel_id` | `str \| None` | new — `resolve_panel_id` | canonical (`MSK-IMPACT-341`, …); `None` for WES |

`seq_assay_id` is kept as-is for GENIE traceability.

### Per-study freq table outputs

- `gene.feather` and `gene_cancer.feather`:
  - `n_samples_inclusive` / `n_samples_exclusive` semantics change for panel-restricted studies — now per-(cancer, gene) rather than per-cancer (or per-gene, for `gene.feather`).
  - No new columns. The shift from per-cancer to per-(cancer, gene) is implicit in the value (when `n_samples_inclusive < cohort_size_for_cancer`, restriction was applied).
- `cancer_type.feather` / `cancer_type_detailed.feather`: unchanged.

### Cross-study annotated outputs

`gene_cancer_study_annotated.feather`, `gene_cancer_study_ratio_annotated.feather`:

- **New columns** (paired inclusive/exclusive):
  - `n_panel_covered_samples_inclusive : int`
  - `n_panel_covered_samples_exclusive : int`
  - `callable_sample_fraction_inclusive : float`
  - `callable_sample_fraction_exclusive : float`
- Existing `n_panel_covered_studies` and `callable_fraction` semantics preserved.

### `samples_tmb.feather`

No schema change. Values change for MSK samples (denominator now panel-correct).

### Snakemake DAG

No new rules; four edges added:

- `download_study`: when `wildcards.id in panel_bearing_studies`, declares `data_gene_panel_matrix.txt` as a fourth output and fetches it.
- `convert_to_feather`: input list becomes 3 fixed + 1 conditional matrix path via input function `_convert_inputs(wildcards)`. Conditioning is on `panel_bearing_studies` config classification, not file existence at runtime.
- `create_freq_tables`: reads `genie_panel_coverage.feather` (declared as new explicit input).
- `create_combined_gene_cancer_freq_table`: gains two new pivoted matrices in `combine_paired_pivot` (per-study `n_inclusive`, `n_exclusive`); inputs unchanged but per-study output reading expands.
- `compute_per_sample_tmb` inputs unchanged.

A new config key `panel_bearing_studies: list[str]` controls the conditional ingest. Fail-loud if a study not listed here later turns out to have a panel matrix file (caught at `convert_to_feather` time via an existence check on the un-declared sibling file).

## Error handling

All failure modes fail-loud (matches CLAUDE.md "fail early / no silent fallback"). No silent drop, no thresholded tolerance:

1. **Unknown panel name during normalization** → `ValueError(f"Unrecognized panel_id {raw!r} (study={study_id}, sample={sample_id}); add to PANEL_ALIASES if real, or fix upstream data")`.
2. **Sample in a panel-bearing study with no resolvable panel** (matrix-missing, suffix-unrecognized, no study fallback) → `ValueError` carrying the offending sample_id and study. Investigate the upstream data; do not drop, do not tolerate. The lone heme sample in the audit will resolve via suffix fallback (`-IH3` → `MSK-IMPACT-HEME-400`); if any future sample fails, that is a data-quality bug worth surfacing.
3. **`panel_id` resolved but missing from `panel_callable_mb` registry** in `compute_per_sample_tmb.py` → raise. Forces config to declare a Mb override or BED entry for any panel that resolves.
4. **`panel_id` resolved but missing from `genie_panel_coverage.feather`** (Component 3 prerequisite check) → raise with explicit instruction to supply BED-derived coverage.
5. **Study with a `data_gene_panel_matrix.txt` file present but not listed in `panel_bearing_studies`** → raise during `convert_to_feather`. Forces explicit config classification (no implicit "is the file there?" branch).

For panel-aware aggregation, when a gene appears in a study's mutation table but on **zero** of the study's per-sample panels (mutation called outside panel intervals — should be rare): drop the (cancer, gene) row from that study, log at WARNING with the count. Numerator-without-denominator is the only ill-defined case; logging makes it visible. If the dropped-row count exceeds 1% of the study's mutated (cancer, gene) pairs, raise — that magnitude indicates a systematic ingestion problem, not isolated off-target calls.

## Testing

### Unit tests (new)

`code/scripts/tests/test_resolve_panel_id.py`:

- All three resolution paths: matrix file, sample-id suffix, study-level fallback.
- Naming normalization across `IMPACT341` / `MSK-IMPACT341` / `MSK-IMPACT-341`.
- Failure modes (unknown panel raises with helpful message).

### Integration tests (extended)

- `test_convert_to_feather.py`: extend fixture to include a small `data_gene_panel_matrix.txt`; assert `panel_id` column present and correctly normalized.
- `test_create_freq_tables.py` (new file if absent): synthetic 6-sample / 2-panel / 3-gene / 2-cancer fixture; assert per-(cancer, gene) denominator equals cohort-size for a gene on all panels and equals the per-panel-restricted count for a gene on only one panel.
- `test_compute_per_sample_tmb.py`: extend fixture so different samples in one study have different `panel_id` values; assert TMB denominators differ accordingly.
- `test_create_combined_gene_cancer_freq_table.py`: assert paired `n_panel_covered_samples_inclusive` and `n_panel_covered_samples_exclusive` columns differ by exactly the count of panel-callable hypermutators for a (cancer, gene) row in a mixed-panel study fixture.

### Empirical regression (validation deliverable)

After implementation, rerun PoC config (`config-poc.yml`) against `msk_impact_2017` (post-`panel_bearing_studies` + `study_panel_map` population) and emit a comparison report to `doc/interpretations/<implementation-date>-t070-poc-comparison.md` covering both motivating axes:

1. **Frequency rates (aggregation):** top-20 gene rates pre-vs-post-t070 for `msk_impact_2017`, broken out by (cancer-type, gene). Expected: ~26% denominator deflation for IMPACT-410+ genes in this study, larger for genes on IMPACT-468/505 only.
2. **TMB distributions (per-sample):** pre/post histograms of per-sample TMB for `msk_impact_2017` samples, stratified by `panel_id`. Expected: ~25–30× downward shift for MSK samples (per the config-poc.yml header note from 2026-04-17).
3. **Hypermutator GMM assignments:** count of `is_hypermutator` flips and `hypermutator_reason` category transitions between pre and post runs. Expected: many of the false-positive hypermutator calls in `msk_impact_2017` (driven by inflated TMB) should resolve.

This is the scientific deliverable that justifies the work — quantifies the bias on both axes the design is meant to fix.

## Out of scope (follow-on tasks)

- **Rename `study_panel_map` → `study_panel_default_map`.** After t070, the config's primary panel source-of-truth is the per-sample matrix; `study_panel_map` becomes a fallback for non-matrix studies. The rename is reasonable polish but touches 4 shipped configs plus user configs — defer to a separate cleanup task. For now: add a comment in the config docstring noting the demoted role.
- Generalization to non-MSK multi-panel cohorts (DFCI ONCOPANEL versions, Tempus xT releases, etc.). Mechanism generalizes trivially — add to `PANEL_ALIASES` and `SAMPLE_ID_SUFFIX_MAP` — but no current config consumes such studies. Defer until needed.
- Per-(cancer, gene) sample weighting in cross-study aggregation beyond `n_panel_covered_samples_*`. The downstream GLMM (t077) will consume these counts directly; a sample-weighted mean ratio is its concern, not this task's.
- Cross-validation against AACR GENIE per-sample panel assignments for samples appearing in both. Worth doing as a one-shot QA pass, but not blocking — covered by the audit's third follow-up.

## References

- Cheng DT et al. 2015. *J Mol Diagn* 17(3):251-264. PMID 25801821. (IMPACT-341/410)
- Zehir A et al. 2017. *Nat Med* 23(6):703-713. PMID 28481359. (IMPACT-410/468)
- Bandlamudi C et al. 2026. "Cancer type-specific variation in patterns of driver alterations across 50,000 tumors." *Cancer Cell*. PMID 41895280. (IMPACT-505 50k follow-up)
- F6 (panel-version drift), `doc/audits/2026-04-13-create-combined-gene-cancer-freq-table-audit.md`.
- Empirical audit logged in this conversation 2026-04-18; rerun via `uv run python -c "..."` against `/data/raw/cbioportal/msk_*` if reproduction needed.
