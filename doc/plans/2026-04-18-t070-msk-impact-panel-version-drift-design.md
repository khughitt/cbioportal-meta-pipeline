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
    # ...341/410/468/505 + IMPACT-HEME-400 + IMPACT-HEME-V2 variants
}

SAMPLE_ID_SUFFIX_MAP: dict[str, str] = {
    "IM3": "MSK-IMPACT-341",
    "IM5": "MSK-IMPACT-410",
    "IM6": "MSK-IMPACT-468",
    "IM7": "MSK-IMPACT-505",
    "IH3": "IMPACT-HEME-400",
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
) -> pd.Series:
    """Return panel_id Series indexed like samples. See behavior contract below."""
```

Behavior contract:

- **Panel-study detection** (any one of these makes a study a "panel study"): a `data_gene_panel_matrix.txt` file is present; OR the study appears in `study_panel_map`; OR ≥1 sample has a recognized MSK sample-id suffix.
- **For panel studies**, the per-sample resolution chain is:
  1. `matrix['mutations']` column normalized via `PANEL_ALIASES` (preferred)
  2. `SAMPLE_ID_SUFFIX_MAP` applied to `sample_id`
  3. `study_panel_map[study_id]` (single panel applied to all samples)

  Every sample must resolve via 1, 2, or 3 — anything unresolved raises `ValueError` carrying `(study_id, sample_id, raw_value)`.
- **For non-panel studies** (no matrix file, no recognized suffix, not in `study_panel_map`), the function returns `None` for every sample. The resulting `panel_id` column on `samples.feather` is `None`, signaling to downstream consumers that the panel-aware path is bypassed (current scalar-per-cancer denominator behavior preserved).

Reference data citations: Cheng 2015 (PMID 25801821) for IMPACT-341/410, Zehir 2017 (PMID 28481359) for IMPACT-410/468 transition, Bandlamudi 2024 for IMPACT-505. Cited inline in module docstring.

### Component 2 — `code/scripts/convert_to_feather.py` (extension)

After reading `data_clinical_sample.txt`, attempt to read sibling `data_gene_panel_matrix.txt`. Pass both into `resolve_panel_ids`, attach the resulting `panel_id` column to `samples.feather`. ~15 lines added.

The existing `seq_assay_id` column (GENIE-only) is preserved and remains GENIE-specific. `panel_id` is the canonical column for all downstream consumers; `seq_assay_id` becomes a raw-source column kept for traceability only.

### Component 3 — `code/scripts/create_freq_tables.py` (modified)

Per-study aggregation gains panel-awareness for the gene-bearing tables.

- **`gene.feather`** (gene-keyed): denominator becomes per-gene = count of samples where the sample's panel covers the gene.
- **`gene_cancer.feather`** (`(cancer_type, symbol)`-keyed): denominator becomes per-(cancer, gene) = count of samples in that cancer-type where the sample's panel covers the gene.
- **`cancer_type.feather` / `cancer_type_detailed.feather`**: unchanged — no gene dimension, panel doesn't apply.

Implementation: small `(panel_id, gene) → bool` callability table derived from `genie_panel_coverage.feather`. Per-study, restrict to `(panel_id, gene)` pairs where the panel is one of those used in the study's samples. Left-join against the study's sample table to enumerate `(sample_id, cancer_type, panel_id, gene)` rows where the gene is callable; group to get the panel-aware denominator.

For studies where every sample's `panel_id` is `None` (WES studies), the panel-aware path is bypassed and current scalar-per-cancer denominators are preserved.

Memory note: 25k samples × ≤505 genes per panel ≈ 12M rows max — fine for in-memory pandas.

A new column `panel_aware : bool` on each gene-bearing output table records whether the row's denominator was panel-restricted.

### Component 4 — `code/scripts/compute_per_sample_tmb.py` (modified)

Replace the current `panel_id = study_panel_map.get(study_id)` (line 162) with a per-sample lookup against `samples["panel_id"]`. Each sample's TMB denominator becomes `panel_callable_mb[sample.panel_id]`. ~10 lines changed; no new files.

For samples where `panel_id` is `None` (WES studies), behavior is identical to today (falls through to `wes_default_callable_mb`).

### Component 5 — `code/scripts/create_combined_gene_cancer_freq_table.py` (modified, `_annotate_callability`)

Two changes to the cross-study annotation:

- **Redefine `n_panel_covered_studies` for panel-mixed studies**: a study contributes to a gene's count if ≥1 of that study's per-sample panels covers the gene (binary per study). Preserves the column's interpretive meaning ("this study could in principle have observed this gene") without conflating sample mixture into the study-level count.
- **Add `n_panel_covered_samples`**: total samples across all studies where the sample's panel covers the gene. This is the column downstream meta-analysis (t077 GLMM-logit) actually needs.

Existing `callable_fraction = n_panel_covered_studies / n_total_studies` semantics preserved. A paired `callable_sample_fraction = n_panel_covered_samples / n_total_samples` is added.

## Data flow & schema changes

### `samples.feather` (per-study, in `out_dir/studies/{id}/metadata/`)

| Column | Type | Source | Notes |
|---|---|---|---|
| `panel_id` | `str \| None` | new — `resolve_panel_id` | canonical (`MSK-IMPACT-341`, …); `None` for WES |

`seq_assay_id` is kept as-is for GENIE traceability.

### Per-study freq table outputs

- `gene.feather` and `gene_cancer.feather`:
  - `n_samples_inclusive` / `n_samples_exclusive` semantics change for panel-restricted studies — now per-(cancer, gene) rather than per-cancer (or per-gene, for `gene.feather`).
  - **New column** `panel_aware : bool` — true if denominator was panel-restricted, false if cohort-wide (WES study).
- `cancer_type.feather` / `cancer_type_detailed.feather`: unchanged.

### Cross-study annotated outputs

`gene_cancer_study_annotated.feather`, `gene_cancer_study_ratio_annotated.feather`:

- **New columns:**
  - `n_panel_covered_samples : int`
  - `callable_sample_fraction : float`
- Existing `n_panel_covered_studies` and `callable_fraction` semantics preserved.

### `samples_tmb.feather`

No schema change. Values change for MSK samples (denominator now panel-correct).

### Snakemake DAG

No new rules; three edges added:

- `convert_to_feather` reads `data_gene_panel_matrix.txt` when present.
- `create_freq_tables` reads `genie_panel_coverage.feather` (already a workflow input on other rules; needs to be added as an explicit input here).
- `compute_per_sample_tmb` inputs unchanged (already reads `samples.feather` + `panel_callable_mb.tsv`).

## Error handling

Three explicit failure modes, all fail-loud (matches CLAUDE.md "fail early / no silent fallback"):

1. **Unknown panel name during normalization** → `ValueError(f"Unrecognized panel_id {raw!r} (study={study_id}, sample={sample_id}); add to PANEL_ALIASES if real, or fix upstream data")`.
2. **Sample present in `data_clinical_sample.txt` but absent from `data_gene_panel_matrix.txt` when matrix exists** → log warning + drop sample with explicit count. If dropped fraction exceeds 0.1%, raise. (The 1 missing sample in `heme_msk_impact_2022` logs; the threshold catches future regressions.)
3. **`panel_id` resolved but missing from `panel_callable_mb` registry** in `compute_per_sample_tmb.py` → raise. Forces config to declare a Mb override or BED entry for any panel that resolves.

For panel-aware aggregation, when a gene appears in a study's mutation table but on **zero** of the study's per-sample panels (mutation called outside panel intervals — should be rare): drop the (cancer, gene) row from that study, log at INFO. Numerator-without-denominator is the only ill-defined case and logging makes it visible.

## Testing

### Unit tests (new)

`code/scripts/tests/test_resolve_panel_id.py`:

- All three resolution paths: matrix file, sample-id suffix, study-level fallback.
- Naming normalization across `IMPACT341` / `MSK-IMPACT341` / `MSK-IMPACT-341`.
- Failure modes (unknown panel raises with helpful message).

### Integration tests (extended)

- `test_convert_to_feather.py`: extend fixture to include a small `data_gene_panel_matrix.txt`; assert `panel_id` column present and correctly normalized.
- `test_create_freq_tables.py` (new file if absent): synthetic 6-sample / 2-panel / 3-gene / 2-cancer fixture; assert per-(cancer, gene) denominator differs from per-cancer denominator for genes off the smaller panel; assert `panel_aware` flag.
- `test_compute_per_sample_tmb.py`: extend fixture so different samples in one study have different `panel_id` values; assert TMB denominators differ accordingly.
- `test_create_combined_gene_cancer_freq_table.py`: assert `n_panel_covered_samples` differs from `n_panel_covered_studies × avg_study_size` for a mixed-panel study.

### Empirical regression (validation deliverable)

After implementation, rerun PoC config (`config-poc.yml`) against `msk_impact_2017` (post-`study_panel_map` population) and emit a small comparison table — top-20 gene rates pre-vs-post-t070 — to `doc/interpretations/<implementation-date>-t070-poc-comparison.md`. Quantifies the bias the audit predicted (~26% denominator deflation for IMPACT-410+ genes in this study). This is the scientific deliverable that justifies the work.

## Out of scope (follow-on tasks)

- Generalization to non-MSK multi-panel cohorts (DFCI ONCOPANEL versions, Tempus xT releases, etc.). Mechanism generalizes trivially — add to `PANEL_ALIASES` and `SAMPLE_ID_SUFFIX_MAP` — but no current config consumes such studies. Defer until needed.
- Per-(cancer, gene) sample weighting in cross-study aggregation beyond `n_panel_covered_samples`. The downstream GLMM (t077) will consume `n_panel_covered_samples` directly; a sample-weighted mean ratio is its concern, not this task's.
- Cross-validation against AACR GENIE per-sample panel assignments for samples appearing in both. Worth doing as a one-shot QA pass, but not blocking — covered by audit's Q3 follow-up.

## References

- Cheng DT et al. 2015. *J Mol Diagn* 17(3):251-264. PMID 25801821. (IMPACT-341/410)
- Zehir A et al. 2017. *Nat Med* 23(6):703-713. PMID 28481359. (IMPACT-410/468)
- Bandlamudi C et al. 2024. (IMPACT-505 release notes)
- F6 (panel-version drift), `doc/audits/2026-04-13-create-combined-gene-cancer-freq-table-audit.md`.
- Empirical audit logged in this conversation 2026-04-18; rerun via `uv run python -c "..."` against `/data/raw/cbioportal/msk_*` if reproduction needed.
