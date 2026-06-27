# t111 — Extract per-tissue normal-tissue spectra — design

- **Task:** t111 (Extract per-tissue 96-trinucleotide reference spectra from Li2021 + Xu2025 supplementals)
- **Priority:** P1 (gates `q007`, `q008`, `q010`)
- **Related topic:** `topic:signature-decomposition-unmatched-normal`
- **Related questions:** `q007`, `q008`, `q010`
- **Status:** design approved 2026-04-18, **pending data-access gate** (see §Data-access gate)

## Goal

Produce two companion reference tables:

- `data/normal_tissue_spectra.tsv` — 96-trinucleotide SBS spectra per normal tissue (shape of mutagenesis)
- `data/normal_tissue_burden.tsv` — per-tissue and per-donor mutation burden (rate of mutagenesis, including callable-space denominator and sequencing-modality metadata)

Both are computed from the raw per-variant supplementary data released by Li et al. 2021 (*Nature*) and Xu et al. 2025 (bioRxiv). The two-table split exists because spectrum (shape) and burden (rate) serve different downstream consumers:

- `q007` (per-tissue null model for mutation *rate*) consumes `normal_tissue_burden.tsv`
- `q008` (background-spectrum subtraction during signature decomposition) consumes `normal_tissue_spectra.tsv`
- `q010` (cosine-similarity tissue-of-origin classifier) consumes `normal_tissue_spectra.tsv` plus comparability columns

Both tables are observational and faithful: what the papers actually measured, not a signature-model reconstruction.

## Data-access gate

This gate runs **before** any implementation work. The design assumes per-variant Supplementary Tables are publicly accessible; if they are not, scope and deliverables change.

1. Verify Li 2021 per-variant calls (or equivalent) are retrievable from a public Supplementary Table or preprint repository — e.g., Nature Supplementary Data, bioRxiv supplement, or Zenodo mirror.
2. Verify Xu 2025 per-variant calls are retrievable from the bioRxiv supplement.
3. Record the exact source (URL, filename, retrieval date, file hash) in `doc/datasets/normal-tissue-spectra.md` before running the extraction.

**Branch A — both sources publicly accessible (assumed).** Proceed with this design as-written.

**Branch B — one or both sources require EGA/GSA controlled access.** Stop. The task becomes materially different (DUA, EGA/GSA download infrastructure, BAM→VCF reprocessing for raw-read-level access, per-source callable-space computation from BED files) and scope may need to be reduced to a single accessible source for this task, with the other deferred to a follow-up task. Raise back to the user before continuing.

The data-access gate is the single biggest risk in this task; it is listed first so it does not get lost in the detail.

## Scope

**In scope**
- Ingesting Li2021 and Xu2025 per-variant mutation tables.
- Computing 96-context SBS counts via `SigProfilerMatrixGenerator`.
- Emitting three aggregations per tissue in `normal_tissue_spectra.tsv`: pooled counts, donor-averaged fractions, per-donor rows.
- Emitting per-donor and per-tissue burden rows in `normal_tissue_burden.tsv`, including callable-Mb denominators sourced from the capture-kit documentation.
- Keying output rows on UBERON ontology IDs; hand-curating the source-label → UBERON mapping for ~50 unique tissues.
- A provenance doc at `doc/datasets/normal-tissue-spectra.md` capturing per-tissue donor counts, source table/figure pointers, notable environmental exposures, and UBERON mapping rationale for non-obvious calls.

**Out of scope (deferred)**
- cBioPortal primary-site → UBERON mapping. Will be built in the first downstream task (`q007` / `q008` / `q010`) that actually consumes the join.
- Additional normal-tissue sources (Lee-Six2018, Martincorena2018, Moore2020, Yoshida2025). Adapter-style refactor deferred until the third source needs to be added.
- Trinucleotide-opportunity correction for exome vs panel vs WGS sequencing targets. Extraction is faithful to observed counts; opportunity correction is a consumer concern (the burden table's `sequencing_modality` and `callable_mb` columns provide the inputs a consumer needs to make the correction).
- Indel / DBS / CN spectra. SBS96 only.

## Architecture

Single Snakemake rule invoking a single Python script:

- **Rule:** `extract_normal_tissue_spectra` (added to `code/workflows/Snakefile`)
- **Script:** `code/scripts/extract_normal_tissue_spectra.py`
- **Pattern:** matches the existing `process_bailey2018_drivers` rule — manual-prereq files in `data/`, one `process_*.py`-style script in `code/scripts/`, output consumed directly by downstream rules as a reference table.
- **Two outputs from one pass:** the script walks the per-variant rows once, emits both the spectra TSV and the burden TSV.

```
for source in [li2021, xu2025]:
    df = read_source_tsv(source)                       # per-variant rows
    df = validate_input_contract(df)                   # coord system, alleles, dedup (see §Input contract)
    df = filter_snvs(df)                               # drop indels, keep SBS only
    df = attach_uberon(df, mapping_tsv)                # join on (source, tissue_label)
    df = attach_assay_metadata(df, source)             # sequencing_modality, capture_kit, callable_mb

    contexts = SigProfilerMatrixGenerator.matrix(df)   # per-variant → 96-context counts

    for tissue in df.tissue_uberon.unique():
        spectra_rows.append(pooled_counts(tissue, contexts))
        spectra_rows.append(donor_averaged_fraction(tissue, contexts))
        spectra_rows.extend(per_donor_rows(tissue, contexts))

        burden_rows.append(pooled_burden(tissue, df))
        burden_rows.extend(per_donor_burden(tissue, df))

write_tsv(spectra_rows, "data/normal_tissue_spectra.tsv")
write_tsv(burden_rows, "data/normal_tissue_burden.tsv")
```

## Input contract

Each source's per-variant TSV is validated against a contract before any processing. Failures halt extraction with a clear error.

| Field | Required form |
|---|---|
| Coordinate system | 1-based, closed (matches VCF/MAF convention). Converted to the SigProfiler-expected form in a single documented step. |
| Chromosome naming | `chr1` … `chr22`, `chrX`, `chrY`, `chrM`. Script strips or adds the `chr` prefix as needed to match the SigProfiler reference bundle for the source's assembly. Mitochondrial variants are dropped (SBS96 is nuclear). |
| `ref` / `alt` | Single DNA bases from `{A,C,G,T}` for the SBS96 path. Indels (`alt` length ≠ 1 or `ref` length ≠ 1) routed to a drop counter reported in the provenance doc, not propagated. |
| Multi-allelic | Splits must already be applied upstream (one row per alt allele). Rows with comma-separated `alt` halt extraction. |
| Duplicates | Exact duplicates (same donor_id, chrom, pos, ref, alt, tissue_label) collapsed once with a `stderr` count. Duplicates across donors or tissues are kept (they are biologically distinct). |
| Assembly | Per-source constant, not per-row: Li2021=GRCh37, Xu2025=GRCh38. Script asserts the asserted assembly matches the chrom/pos ranges (sanity check against reference chromosome lengths). |

## Inputs

Three hand-staged files in `data/` (raw variant TSVs gitignored per existing policy; UBERON mapping version-controlled).

| Path | Source | Format | Expected rows | Committed to git |
|---|---|---|---|---|
| `data/li2021_somatic_mutations.tsv` | Li 2021 Supplementary Table (paper Data Availability — preprint cites GSA PRJCA003552 → Nature EGA EGAD00001007859). Gated on §Data-access gate. | Per-variant, hg19: `donor_id, tissue_label, chrom, pos, ref, alt` | ~15k–30k | No |
| `data/xu2025_somatic_mutations.tsv` | Xu 2025 bioRxiv Supplementary Table. Gated on §Data-access gate. | Per-variant, GRCh38: `donor_id, tissue_label, chrom, pos, ref, alt` | ~8,470 (matches paper) | No |
| `data/tissue_uberon_mapping.tsv` | Hand-curated during implementation via EBI OLS lookup | `source, tissue_label, tissue_uberon, uberon_label, notes` | ~50 | Yes |

Non-data prerequisites:
- `SigProfilerMatrixGenerator` added via `uv add sigprofilermatrixgenerator`.
- Reference bundles (`GRCh37`, `GRCh38`) auto-downloaded on first run to SigProfiler's user cache.
- Per-source assay metadata (sequencing_modality, capture_kit, callable_mb) encoded as a small constants dict in the script, sourced from each paper's Methods. Li2021: WES, SureSelectXT V6 (esophagus) or V7 (other tissues), callable ~60 Mb. Xu2025: to be confirmed from the paper Methods during implementation. If a source mixes modalities across tissues, the metadata is keyed at (source, tissue_label) rather than (source,).

## Output schemas

### `data/normal_tissue_spectra.tsv`

Long format, TSV, one row per `(source_id, tissue_uberon, aggregation, donor_id)` combination.

| Column | Type | Notes |
|---|---|---|
| `source_id` | str | `li2021` or `xu2025` |
| `tissue_uberon` | str | e.g. `UBERON:0007650` |
| `tissue_label` | str | Source-native label, preserved for audit |
| `aggregation` | str | `pooled_counts` \| `donor_averaged_fraction` \| `per_donor` |
| `value_type` | str | `counts` (for `pooled_counts` and `per_donor`) or `fractions` (for `donor_averaged_fraction`). Redundant with `aggregation` but explicit — prevents a careless consumer from comparing counts to fractions. |
| `donor_id` | str | Filled only for `aggregation=per_donor`; empty otherwise |
| `assembly` | str | `GRCh37` or `GRCh38` — assembly used for context lookup |
| `sequencing_modality` | str | `WES` \| `WGS` \| `panel` |
| `capture_kit_or_panel` | str | e.g. `SureSelectXT V6` — empty for WGS |
| `callable_mb` | float | Callable target size in megabases; used as denominator when consumers convert counts to rates |
| `n_donors_total` | int | Donors available for this tissue in the source |
| `n_donors_included` | int | Donors contributing to this row (= n_donors_total − n_donors_excluded_low_snvs for `donor_averaged_fraction`; = n_donors_total otherwise) |
| `n_donors_excluded_low_snvs` | int | Donors excluded for having <threshold SNVs in this tissue |
| `low_snv_threshold` | int | The threshold used (default 50) — recorded on every row so the audit trail survives even if the script default changes |
| `n_samples` | int | Mini-bulk biopsies / exome samples contributing |
| `total_snvs` | int | Sum of SNVs across the 96 contexts in this row |
| `A[C>A]A` … `T[T>G]T` | float or int | 96 columns, one per SigProfiler-standard trinucleotide context |

Row counts per tissue ≈ `1 (pooled) + 1 (averaged) + n_donors`. With ~50 unique tissues at median 3–4 donors each, expect ~250 rows total.

Context-column values:
- integer counts when `value_type=counts` (aggregation ∈ {pooled_counts, per_donor})
- fractions summing to exactly 1 when `value_type=fractions` (aggregation=donor_averaged_fraction); donor-level fractions averaged across donors, then re-normalized to guard against rounding drift

### `data/normal_tissue_burden.tsv`

Long format, TSV, one row per `(source_id, tissue_uberon, aggregation, donor_id)`.

| Column | Type | Notes |
|---|---|---|
| `source_id` | str | `li2021` or `xu2025` |
| `tissue_uberon` | str | |
| `tissue_label` | str | |
| `aggregation` | str | `pooled` \| `per_donor` (no donor-averaged here — burden is rate, averaging a rate across donors of different sample counts is not a primitive worth caching) |
| `donor_id` | str | Filled only for `aggregation=per_donor` |
| `assembly` | str | |
| `sequencing_modality` | str | |
| `capture_kit_or_panel` | str | |
| `callable_mb` | float | |
| `n_donors` | int | |
| `n_samples` | int | |
| `snvs` | int | Total SBS96 SNVs (post-indel-filter, post-dedup) |
| `snvs_per_mb` | float | `snvs / callable_mb / n_samples` — per-sample rate, directly comparable to TMB in cancer cohorts |

This is the `q007` null-model input.

### `doc/datasets/normal-tissue-spectra.md`

Companion provenance file (target ≤100 lines): per-tissue n_donors, donor IDs, source figure/table reference, notable exposures (e.g. Li2021 PN2 liver = aristolochic acid, PN9 liver = tobacco), UBERON mapping rationale for non-obvious choices, input-file retrieval URLs + hashes, extraction-run stderr summary.

## Extraction subtleties

- **SBS-only filtering.** SigProfilerMatrixGenerator emits SBS96 / DBS / ID matrices separately; the script keeps only SBS96. Indel and DBS counts are still reported per source in the provenance doc so the drop is auditable.
- **Donor-averaged normalisation.** Each donor's 96-vector is divided by its per-donor sum *before* averaging. Donors with fewer than `low_snv_threshold` (default 50) SNVs in a given tissue are excluded from that tissue's `donor_averaged_fraction` row (they still contribute to `pooled_counts` and get their own `per_donor` row). The exclusion is recorded on the output row via `n_donors_excluded_low_snvs` and `low_snv_threshold`, not just in stderr — a consumer can see at a glance whether a low-burden tissue's average is actually averaging over the intended donor set.
- **Cross-assembly handling.** The `assembly` column is per-row. No liftover. Consumers doing cross-source comparison must decide whether hg19-computed and GRCh38-computed fractions are comparable for their purpose.

## Failure handling

Follows CLAUDE.md "fail early / explicit > defensive":

| Failure | Handling |
|---|---|
| Supplementary TSV missing from `data/` | Script exits with message listing expected paths and paper Sup-Table URLs. Matches `process_bailey2018_drivers.py` convention. |
| Input-contract violation (see §Input contract) | Script exits with the specific violation and offending row count. No silent coercion. |
| Unmapped `(source, tissue_label)` | Script exits with list of unmapped pairs and pointer to append to `data/tissue_uberon_mapping.tsv`. No silent drops. |
| SigProfilerMatrixGenerator reference bundle absent | First call wrapped in `try/except FileNotFoundError`; on miss the script runs `install(assembly)` and retries once. |
| Donor has fewer than `low_snv_threshold` SNVs in a tissue | Excluded from that tissue's `donor_averaged_fraction`; recorded on the row via `n_donors_excluded_low_snvs`. Still contributes to `pooled_counts` and gets a `per_donor` row. |
| Assay-metadata dict missing an expected `(source, tissue_label)` | Script exits with the specific missing key. No defaulting. |

No catch-all exception handlers. Indel / DBS variants are filtered via SigProfiler output-selection (SBS96), not input-side — malformed ref/alt columns surface as SigProfiler errors or contract-validation errors, not silent skips.

## Testing

Two-tier test suite under `tests/test_extract_normal_tissue_spectra.py`: pure/deterministic tests run on every CI invocation; the slow integration test that hits SigProfiler is gated behind a `pytest` marker.

**Pure tests (deterministic, no external deps, always run):**

| Test | What it checks |
|---|---|
| `test_pooled_counts_aggregation` | Given synthetic 96-context count vectors for 3 donors, pooled row = element-wise sum; `total_snvs` = row sum. |
| `test_donor_averaged_fraction_math` | Donor-fraction-averaging math: normalize per donor, average across donors, renormalize. Sums to 1.0 ± 1e-9. |
| `test_low_snv_threshold_exclusion` | Donor with 49 SNVs excluded at default threshold; `n_donors_excluded_low_snvs` and `low_snv_threshold` reflected on the output row. |
| `test_per_donor_row_count_matches_input` | 3-donor tissue → exactly 3 `per_donor` rows with correct `donor_id` values. |
| `test_input_contract_violations` | Each of: indel row, multi-allelic row, unknown chromosome, wrong assembly range, duplicate row → expected behaviour (error, drop-with-counter, dedup). |
| `test_uberon_mapping_required` | Unmapped `(source, tissue_label)` raises explicitly — no silent drop. |
| `test_burden_snvs_per_mb_math` | `snvs_per_mb = snvs / callable_mb / n_samples` round-trip on fixture values. |
| `test_value_type_matches_aggregation` | `value_type=counts` iff `aggregation ∈ {pooled_counts, per_donor}`; `value_type=fractions` iff `aggregation=donor_averaged_fraction`. |

**Integration test (marked `slow`, not in default CI run):**

| Test | What it checks |
|---|---|
| `test_end_to_end_golden` | Full script on 50-variant fixture (3 tissues × 2 donors) including the real SigProfilerMatrixGenerator trinucleotide lookup; diffed against `tests/fixtures/expected_normal_tissue_spectra.tsv` and `tests/fixtures/expected_normal_tissue_burden.tsv`. |

The aggregation code path is tested entirely in the pure tier by injecting pre-computed 96-context count vectors — the real trinucleotide-lookup step is only exercised in the integration test, which is skipped unless `pytest -m slow` or a dedicated CI job asks for it.

No regression tests over the real Li2021 / Xu2025 datasets (supplementary tables will drift). Instead, the extraction script writes a `stderr` summary (tissues found, donors per tissue, total SNVs, indel/DBS drops, duplicate drops) and the run output is captured in the provenance doc on each re-extraction.

## Deliverables

1. `code/scripts/extract_normal_tissue_spectra.py` — the extraction script
2. New rule in `code/workflows/Snakefile` — `extract_normal_tissue_spectra`
3. `data/tissue_uberon_mapping.tsv` — hand-curated UBERON mapping (committed)
4. `data/normal_tissue_spectra.tsv` — extracted SBS96 reference table (gitignored, regenerable)
5. `data/normal_tissue_burden.tsv` — extracted burden reference table (gitignored, regenerable)
6. `doc/datasets/normal-tissue-spectra.md` — provenance
7. `tests/test_extract_normal_tissue_spectra.py` + `tests/fixtures/` — tests (pure + slow integration)
8. `pyproject.toml` update — `sigprofilermatrixgenerator` dependency
9. Task status updates: t111 → in_progress, later → completed
