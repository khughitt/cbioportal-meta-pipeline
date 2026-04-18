# t111 — Extract per-tissue normal-tissue spectra — design

- **Task:** t111 (Extract per-tissue 96-trinucleotide reference spectra from Li2021 + Xu2025 supplementals)
- **Priority:** P1 (gates q007, q008, q010)
- **Related topic:** `topic:signature-decomposition-unmatched-normal`
- **Related questions:** q007, q008, q010
- **Status:** design approved 2026-04-18

## Goal

Produce `data/normal_tissue_spectra.tsv` — one long-format table holding 96-trinucleotide SBS spectra per normal tissue, computed from the raw per-variant supplementary data released by Li et al. 2021 (*Nature*) and Xu et al. 2025 (bioRxiv). The table is the common input to three downstream workstreams: q007 (per-tissue null model), q008 (background-spectrum subtraction during signature decomposition), and q010 (cosine-similarity tissue-of-origin classifier).

The table is observational and faithful: what the papers actually measured, not a signature-model reconstruction.

## Scope

**In scope**
- Ingesting Li2021 and Xu2025 per-variant mutation tables.
- Computing 96-context SBS counts via `SigProfilerMatrixGenerator`.
- Emitting three aggregations per tissue: pooled counts, donor-averaged fractions, per-donor rows.
- Keying output rows on UBERON ontology IDs; hand-curating the source-label → UBERON mapping for ~50 unique tissues.
- A provenance doc at `doc/datasets/normal-tissue-spectra.md` capturing per-tissue donor counts, source table/figure pointers, notable environmental exposures, and UBERON mapping rationale for non-obvious calls.

**Out of scope (deferred)**
- cBioPortal primary-site → UBERON mapping. Will be built in the first downstream task (q007 / q008 / q010) that actually consumes the join.
- Additional normal-tissue sources (Lee-Six2018, Martincorena2018, Moore2020, Yoshida2025). Adapter-style refactor deferred until the third source needs to be added.
- Trinucleotide-opportunity correction for exome vs panel vs WGS sequencing targets. Extraction is faithful to observed counts; opportunity correction is a consumer concern.
- Indel / DBS / CN spectra. SBS96 only.

## Architecture

Single Snakemake rule invoking a single Python script:

- **Rule:** `extract_normal_tissue_spectra` (added to `code/workflows/Snakefile`)
- **Script:** `code/scripts/extract_normal_tissue_spectra.py`
- **Pattern:** matches the existing `process_bailey2018_drivers` rule — manual-prereq files in `data/`, one `process_*.py`-style script in `code/scripts/`, output consumed directly by downstream rules as a reference table.

```
for source in [li2021, xu2025]:
    df = read_source_tsv(source)                       # per-variant rows
    df = filter_snvs(df)                               # drop indels, keep SBS only
    df = attach_uberon(df, mapping_tsv)                # join on (source, tissue_label)
    contexts = SigProfilerMatrixGenerator.matrix(df)   # per-variant → 96-context counts

    for tissue in df.tissue_uberon.unique():
        rows.append(pooled_counts(tissue, contexts))
        rows.append(donor_averaged_fraction(tissue, contexts))
        rows.extend(per_donor_rows(tissue, contexts))

write_tsv(rows, "data/normal_tissue_spectra.tsv")
```

## Inputs

Three hand-staged files in `data/` (all manual prereqs, all gitignored per existing policy *except* the UBERON mapping which is version-controlled).

| Path | Source | Format | Expected rows | Committed to git |
|---|---|---|---|---|
| `data/li2021_somatic_mutations.tsv` | Li 2021 Supplementary Table (paper Data Availability — preprint cites GSA PRJCA003552 → Nature EGA EGAD00001007859). If per-variant calls are not in a downloadable Supplementary Table, fall back to EGA access and document the reproducibility caveat in the provenance doc. | Per-variant, hg19: `donor_id, tissue_label, chrom, pos, ref, alt` | ~15k–30k | No |
| `data/xu2025_somatic_mutations.tsv` | Xu 2025 bioRxiv Supplementary Table | Per-variant, GRCh38: `donor_id, tissue_label, chrom, pos, ref, alt` | ~8,470 (matches paper) | No |
| `data/tissue_uberon_mapping.tsv` | Hand-curated during implementation via EBI OLS lookup | `source, tissue_label, tissue_uberon, uberon_label, notes` | ~50 | Yes |

Non-data prerequisites:
- `SigProfilerMatrixGenerator` added via `uv add sigprofilermatrixgenerator`.
- Reference bundles (`GRCh37`, `GRCh38`) auto-downloaded on first run to SigProfiler's user cache; extraction script calls `SigProfilerMatrixGenerator.install.install(assembly, bash=True)` idempotently before matrix generation.

## Output schema

`data/normal_tissue_spectra.tsv` (long format, TSV matching existing `data/` convention):

| Column | Type | Notes |
|---|---|---|
| `source_id` | str | `li2021` or `xu2025` |
| `tissue_uberon` | str | e.g. `UBERON:0007650` |
| `tissue_label` | str | Source-native label, preserved for audit |
| `aggregation` | str | `pooled_counts` \| `donor_averaged_fraction` \| `per_donor` |
| `donor_id` | str | Filled only for `aggregation=per_donor`; empty otherwise |
| `assembly` | str | `GRCh37` or `GRCh38` — assembly used for context lookup |
| `n_donors` | int | Donors contributing to this row |
| `n_samples` | int | Mini-bulk biopsies / exome samples contributing |
| `total_snvs` | int | Sum of SNVs across the 96 contexts in this row |
| `A[C>A]A` … `T[T>G]T` | float or int | 96 columns, one per SigProfiler-standard trinucleotide context |

Row counts per tissue ≈ `1 (pooled) + 1 (averaged) + n_donors`. With ~50 unique tissues at median 3–4 donors each, expect ~250 rows total.

Context-column values:
- integer counts when `aggregation ∈ {pooled_counts, per_donor}`
- fractions summing to exactly 1 when `aggregation=donor_averaged_fraction` (donor-level fractions averaged across donors, then re-normalized to guard against rounding drift)

Companion file `doc/datasets/normal-tissue-spectra.md` (target ≤100 lines) — per-tissue provenance: n_donors, donor IDs, source figure/table reference, notable exposures (e.g. Li2021 PN2 liver = aristolochic acid, PN9 liver = tobacco), and UBERON mapping rationale for non-obvious choices.

## Extraction subtleties

- **SBS-only filtering.** SigProfilerMatrixGenerator emits SBS96 / DBS / ID matrices separately; the script keeps only SBS96. Documented in the provenance doc.
- **Donor-averaged normalisation.** Each donor's 96-vector is divided by its per-donor sum *before* averaging. Donors with fewer than 50 SNVs contributing to a given tissue are excluded from that tissue's `donor_averaged_fraction` row (they still appear in `pooled_counts` and get their own `per_donor` row). The threshold (50) is configurable via script argument, defaults to 50.
- **Cross-assembly handling.** The `assembly` column is per-row. No liftover. Consumers doing cross-source comparison must decide whether hg19-computed and GRCh38-computed fractions are comparable for their purpose. The ~0.3% of coding positions affected by liftover is negligible for 96-context fractions, but making the consumer acknowledge the caveat is preferable to silent conflation.

## Failure handling

Follows CLAUDE.md "fail early / explicit > defensive":

| Failure | Handling |
|---|---|
| Supplementary TSV missing from `data/` | Script exits with message listing expected paths and paper Sup-Table URLs. Matches `process_bailey2018_drivers.py` convention. |
| Unmapped `(source, tissue_label)` | Script exits with list of unmapped pairs and pointer to append to `data/tissue_uberon_mapping.tsv`. No silent drops. |
| SigProfilerMatrixGenerator reference bundle absent | First call wrapped in `try/except FileNotFoundError`; on miss the script runs `install(assembly)` and retries once. |
| Donor has <50 SNVs in a tissue | Excluded from that tissue's `donor_averaged_fraction` with a `stderr` warning (tissue + donor). Still contributes to `pooled_counts` and gets a `per_donor` row. Counted in provenance doc. |

No catch-all exception handlers. Indel / DBS variants are filtered via SigProfiler output-selection (SBS96), not input-side — malformed ref/alt columns surface as SigProfiler errors rather than silent skips.

## Testing

Unit + integration tests under `tests/test_extract_normal_tissue_spectra.py`:

| Test | What it checks |
|---|---|
| `test_pooled_counts_sum_matches_input` | Fixture of 10 hand-crafted variants → pooled row `total_snvs=10`, 96 context columns sum to 10. |
| `test_donor_averaged_fraction_sums_to_one` | Donor-averaged row sums to 1.0 ± 1e-9; low-variant donor exclusion threshold (default 50) behaves as documented. |
| `test_per_donor_row_count_matches_input` | 3-donor tissue → exactly 3 `per_donor` rows with correct `donor_id` values. |
| `test_uberon_mapping_required` | Unmapped `(source, tissue_label)` raises explicitly — no silent drop. |
| `test_end_to_end_golden` | Integration: 50-variant fixture (3 tissues × 2 donors) through full script, diffed against checked-in `tests/fixtures/expected_normal_tissue_spectra.tsv`. |

SigProfilerMatrixGenerator is **not** mocked — the integration test calls it for real against GRCh37 (auto-installed by the test harness on first run). Keeps the trinucleotide-lookup path honest.

No regression tests over the real Li2021 / Xu2025 datasets (supplementary tables will drift). Instead, the extraction script writes a `stderr` summary (tissues found, donors per tissue, total SNVs) and the run output is captured in the provenance doc on each re-extraction.

## Deliverables

1. `code/scripts/extract_normal_tissue_spectra.py` — the extraction script
2. New rule in `code/workflows/Snakefile` — `extract_normal_tissue_spectra`
3. `data/tissue_uberon_mapping.tsv` — hand-curated UBERON mapping (committed)
4. `data/normal_tissue_spectra.tsv` — extracted reference table (gitignored, regenerable)
5. `doc/datasets/normal-tissue-spectra.md` — provenance
6. `tests/test_extract_normal_tissue_spectra.py` + `tests/fixtures/` — tests
7. `pyproject.toml` update — `sigprofilermatrixgenerator` dependency
8. Task status updates: t111 → in_progress, later → completed

## Open questions (tracked, not blocking)

- Do Li2021 and Xu2025 publish per-variant Supplementary Tables directly, or only summary exposure tables? If the former, extraction proceeds directly. If only EGA/GSA raw data is available, the task still proceeds but with a longer data-acquisition step documented in the provenance doc. **Resolved during implementation, not during design.**
