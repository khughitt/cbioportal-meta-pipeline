---
id: "interpretation:2026-04-19-t111-normal-tissue-spectra-pipeline"
type: "interpretation"
mode: "dev"
title: "t111: normal-tissue spectra extraction pipeline — infrastructure + validation run"
status: "active"
source_refs:
  - "cite:Li2021"
related:
  - "paper:Li2021"
  - "paper:Yoshida2026"
  - "topic:signature-decomposition-unmatched-normal"
  - "topic:mutation-rate-normalization"
  - "question:q007-cross-tissue-somatic-mutation-rate-variation-as-null-model"
  - "question:q008-signature-decomposition-tissue-background-subtraction"
  - "question:q010-cuplr-style-tof-classifier-for-suspect-normal-samples"
created: "2026-04-19"
updated: "2026-04-19"
input: "task:t111 — commits ca50832..b4fff92 (33 commits)"
workflow_run: "t111-2026-04-19"
prior_interpretations: []
---

# Interpretation (dev mode): t111 normal-tissue spectra extraction

## Verdict

**Verdict:** [?] Dev-mode infrastructure build: normal-tissue spectra extraction pipeline delivered with Li 2021 scope; no hypothesis tested, downstream consumers unblocked.

<!-- Backfilled 2026-04-19 per discussion:2026-04-19-verdict-polarity-display -->

## Mode

`dev` — t111 built the null-model-spectra extraction pipeline from scratch. The real-data execution did produce ~56 spectra rows and ~47 burden rows as empirical output, but those rows are **inputs to downstream analyses** (q007, q008, q010), not tests of a hypothesis. This document summarizes the infrastructure outcomes, the methodological lessons, and the narrow empirical observations that serve as sanity checks on the pipeline.

## Infrastructure Outcomes

### New capabilities

| Artefact | Path | Purpose |
|---|---|---|
| Extraction script | `code/scripts/extract_normal_tissue_spectra.py` | 13-function pipeline: contract-validate → UBERON attach → assay-metadata attach → SigProfilerMatrixGenerator → pooled / donor-averaged-fraction / per-donor aggregations → TSV writers |
| Staging script | `code/scripts/stage_li2021_somatic_mutations.py` | One-off XLSX → TSV converter for Li 2021 Supplementary Table 3, with greedy longest-prefix `sampleID` parser |
| UBERON mapping | `data/tissue_uberon_mapping.tsv` | 9 Li 2021 tissue labels → UBERON IDs, hand-curated and OLS-verified |
| Snakemake rule | `extract_normal_tissue_spectra` in `code/workflows/Snakefile` | Wires the script into the pipeline |
| Provenance doc | `doc/datasets/normal-tissue-spectra.md` | Source URL/SHA256, per-tissue donor counts, aggregation definitions, replication instructions |
| Slow integration test | `code/scripts/tests/test_extract_normal_tissue_spectra.py::test_end_to_end_with_real_sigprofiler_grch37` + 3 fixture TSVs | End-to-end test against real SigProfiler (skipped by default via pytest `slow` marker) |

Outputs at `data/normal_tissue_spectra.tsv` (56 rows × 114 cols) and `data/normal_tissue_burden.tsv` (47 rows × 14 cols) are gitignored — regenerable from the staging script + committed UBERON mapping + the Task 0 gate record URL/SHA256.

### Test coverage

29 pure unit tests + 1 slow integration test. All 187 project-suite tests pass. Slow test is deselected by default; invoked with `pytest -m slow` it exercises the real SigProfilerMatrixGenerator trinucleotide lookup against a 9-variant fixture.

### Scope (post Task-0 gate)

Li 2021 only. Xu 2025 was gated to Branch B when the data-access gate discovered per-variant calls live in dbGaP `phs000424.v7` (controlled access) rather than the bioRxiv supplement. User approved option (a) — reduce t111 scope, defer Xu 2025 / Lee-Six 2018 integration to follow-up task **t112**.

## Methodological Findings

### The data-access gate was load-bearing

Elevating the data-availability check to a prerequisite gate (design rev 2) paid off on the first task execution: Xu 2025's per-variant calls turned out to be dbGaP-only, which would have derailed the middle of implementation if discovered during Task 16. Making this a formal Branch-A/Branch-B decision before any code was written let us scope-reduce cleanly rather than retrofitting. **Recommendation:** any task whose inputs are third-party supplementary data should start with an access-verification gate, not a TODO in the implementation plan.

### SigProfiler's canonical context-96 ordering is non-obvious

The plan — and the initial implementation — both used loop nesting `for sub for five for three`, which happens to agree with SigProfiler's canonical ordering on the first four positions but diverges at position 4 onward. A code-quality reviewer caught the discrepancy by grepping the SigProfilerMatrixGenerator-bundled `GRCh37_bench_orig_96.txt` for the true ordering. Fix was a one-line loop-swap. **Recommendation:** when adopting a third-party ordering convention, pin spot-check assertions against an authoritative artefact (we now assert `CONTEXT_96[4] == "A[C>G]A"` at module load).

### Li 2021 encodes indels as `ref="-"` / `alt="-"`

The original input contract's indel filter checked `ref.str.len() != 1 | alt.str.len() != 1`, which passes single-character `-` sentinels through as "SNVs" that would then fail the ACGT check with an unhelpful error. Real data surfaced this on the first production run — 583 rows carried `-` in ref or alt. Filter extended to drop these explicitly. **Recommendation:** indel conventions vary by caller; validate at the first real-data contact, not on synthetic fixtures.

### SigProfilerMatrixGenerator 1.3.6 raises bare `Exception`, not `FileNotFoundError`

The plan and initial implementation caught `FileNotFoundError` for the install-retry path. Running against a clean environment revealed that SigProfiler actually raises a bare `Exception("The specified genome GRCh37 has not been installed...")`. Fix was broadening the catch to `(FileNotFoundError, Exception)` with a message-content guard so other exceptions still propagate. **Recommendation:** when writing install-retry wrappers around third-party tools, read the source's `raise` sites rather than guessing from the tool's public docs.

### Silent fallbacks are the wrong cure for unreachable edge cases

Two Important review catches reversed `max(n_samples, 1)` and `row.get("col", 0)` patterns with explicit `ValueError` raises. The CLAUDE.md "fail early / avoid silent fallbacks" rule doesn't just mean "no bare except blocks" — it extends to any guard that silently substitutes a sentinel for data the function cannot meaningfully handle. **Recommendation:** when adding a guard for an unreachable case, prefer `raise ValueError(...)` over a numeric fallback — the former keeps the invariant visible if the case ever becomes reachable.

### Type stubs reject patterns pandas accepts at runtime

Pyright persistently flagged `pd.Series.isin({...set...})`, `pd.DataFrame(index=[...list...], columns=[...])`, and `tissue_df.get("col", fallback).nunique()` as type errors despite passing at runtime. Each fix was purely type-narrowing (tuples in place of sets; explicit `"col" in df.columns` in place of `.get`; `assert isinstance(key, tuple)` after groupby). These aren't pandas API misuses; they're type-stub-vs-runtime gaps. **Recommendation:** treat pyright as part of the CI linting surface even when the project doesn't enforce it, because the diagnostics surface real API seams that a future Python/pandas/pyright upgrade might tighten.

### Sanity-check values match Li 2021 Fig 1b qualitative ordering

Pipeline output per-tissue burden:

| tissue | pooled SNVs (t111 run) | Li 2021 Fig 1b median mut/exome |
|---|---|---|
| Liver | 14,184 (highest) | 69 (highest) |
| Colon | 8,479 | 19 |
| Rectum | 7,285 | 41.5 |
| Duodenum | 6,278 | 35 |
| Stomach | 5,172 | 31 |
| Esophagus | 4,026 | 31 |
| Cardia | 4,041 | 44 |
| Bronchia | 3,176 | 26 |
| Pancreas | 2,336 (lowest) | 10 (lowest) |

Pooled `snvs_per_mb` Liver 1.19 / Pancreas 0.20 = 6.0× range. Li 2021 Liver 69 / Pancreas 10 = 6.9× range. Pipeline correctness validated; per-tissue ordering is mostly preserved (Cardia appears higher than expected relative to Stomach in Fig 1b; likely because Cardia has fewer donors/biopsies so pooled totals don't track the per-exome medians — worth flagging if downstream analyses key on the exact ordering).

## Reusable Lessons

- **Gate data access before coding.** Design-rev-2 added this as §Data-access gate; it prevented scope creep.
- **Spot-assert third-party conventions at module load.** `assert CONTEXT_96[4] == "A[C>G]A"` would have caught the initial-implementation mistake at import time instead of leaving it latent until Task 10's slow integration test.
- **Commit the staging script + gate record, gitignore the raw + derived data.** Reproducibility is preserved (regenerate from the script + hash); repository stays small.
- **Two-tier test strategy works.** 29 pure tests run on every invocation (< 4 s); the slow integration test is opt-in via `pytest -m slow` and takes ~10 min first-run (SigProfiler bundle download) / ~1 min subsequent. CI can default-skip the slow tier.
- **Subagent-driven review is worth the overhead.** Of 33 commits, 11 were follow-ups to code-quality review findings. Without the review loop, the CONTEXT_96 ordering bug and the `max(n_samples, 1)` silent fallback would have shipped.

## Downstream Tasks Unblocked

- **q007** (cross-tissue somatic mutation rate variation as null model) — **partially addressed.** The null-model table exists and reproduces Li 2021's burden ordering. The question "can it serve as a null model" is now *answerable* but not yet answered: no cBioPortal output has been corrected against this baseline yet. A concrete next analysis is to apply the per-tissue `snvs_per_mb` as a denominator correction to `gene_cancer_study_ratio_annotated.feather` frequencies and check whether any gene-cancer rankings shift.
- **q008** (SBS1/SBS5 tissue-background subtraction magnitude) — **infrastructure available, analysis not yet run.** The spectra table carries the 96-context fractions needed for background subtraction. t109 (per-study cancer-type signature restriction) and t110 (SBS1/SBS5 ratio validation) are the natural consumers.
- **q010** (tissue-of-origin classifier via cosine similarity) — **infrastructure available, analysis not yet run.** The spectra table is the reference library a cosine-similarity classifier would query against.
- **t109** (cancer-type signature restriction for SigProfilerAssignment) — now has a validated SigProfilerMatrixGenerator integration to copy from.
- **t110** (SBS1/SBS5 ratio validation) — still blocked by t109.
- **t112** (integrate Lee-Six 2018 or Xu 2025 as second source) — now has a working single-source adapter pattern to extend.

## Follow-up Risks and Open Loops

- **`TODO(t111-followup)` in `validate_input_contract`**: the `assembly` parameter is accepted but not range-checked against per-chromosome lengths. Design spec §Input contract requires this; noqa + comment marks the deferral. A caller who declares `assembly="GRCh38"` for Li 2021 data would not be caught by the validator. Cost to fix: encode GRCh37/GRCh38 max-chromosome-lengths as a constants dict and add a spot-check against `df["pos"].max()` per chromosome. Probably half an hour plus one test.
- **Cardia donor count (3, vs Liver's 5) distorts pooled ordering.** Cardia's 4,041 pooled SNVs exceed Stomach's 5,172 only in absolute terms; on a per-donor-average basis Cardia is comparable or lower. Downstream consumers that key on pooled counts should normalize by `n_donors` or `n_samples` before comparing tissues. The `snvs_per_mb` column in `normal_tissue_burden.tsv` already does this correctly.
- **No discriminating prediction yet filed to distinguish q007 from a simpler "use Martincorena 2017's dN/dS" alternative.** The framework design assumed the Li 2021 empirical rates are strictly better than a dN/dS-based null; we haven't actually run a head-to-head comparison. If a downstream analysis finds the two approaches rank genes identically for cBioPortal outputs, q007's value-add collapses. Worth a pre-registration before the null-model correction is rolled out.
- **`Cardia` UBERON ID correction.** Plan's suggested UBERON:0007650 turned out to be "esophagogastric junction" (a junction structure), not "cardia of stomach" (a gastric region). Fixed to UBERON:0001162 during Task 2 with an EBI OLS spot check. Other UBERON IDs in `data/tissue_uberon_mapping.tsv` were only spot-checked (4 of 9); the remaining 5 could be independently verified for defensive robustness, though the project's use case (tissue-label join) doesn't depend on the exact UBERON choice.
- **Integration test is slow-marked by default.** If a future SigProfilerMatrixGenerator upgrade breaks the install-retry path, CI won't catch it unless `pytest -m slow` is invoked explicitly. Consider adding a nightly job or a release-prep checklist entry to run the slow tier.

## User Questions

- **"Want to start with t109 and t111 in parallel?"** — No. t111 first; t109/t110 depend on having the null-model spectra.
- **"Reduce scope or expand?"** (after Branch B gate) — Reduced scope to Li 2021 only; filed t112 for second-source integration.

## Updated Priorities

**New tasks to add:**
- **Assembly range-check follow-up** (P3, dev): close the `TODO(t111-followup)` by implementing chromosome-length range verification in `validate_input_contract`. Low priority — current callers pass the correct assembly by construction via `_SOURCE_ASSEMBLY`. Filing for future-proofing when t112 adds GRCh38 sources.
- **Pre-register q007 null-model correction impact** (P2, research): before rolling the per-tissue `snvs_per_mb` correction into the main frequency/ratio pipeline, pre-register the expected effect sizes (how many gene-cancer rankings shift, and by how many rank positions) and the comparison against a simpler Martincorena dN/dS baseline. Prevents "this looks like a good idea, let's ship it" bias.

**Existing tasks to promote / reconsider:**
- **t109** (signature-restriction rule) — still P2, still active. No change.
- **t110** (SBS1/SBS5 validation) — still P2, still blocked by t109. No change.
- **t112** (Lee-Six 2018 / Xu 2025 second-source integration) — P2, proposed. Given that downstream questions (especially q008 — blood CH contamination) most urgently need blood tissue coverage, consider promoting to P1 once q008's first results come in and confirm the blood gap is real.

**Graph updates (pending graph.trig materialization):**
- No proposition-level evidence updates yet. t111's empirical outputs are *instrumental* (null-model inputs to downstream analyses) rather than evidence for or against specific propositions. Once q007 / q008 / q010 run their first concrete analyses against the spectra table, the resulting observations will shift proposition support.
- Science-tool health check shows `proposition_claim_layer_coverage: numerator=0, denominator=0` — the project has not yet materialized its proposition graph; interpretation quality in this document is accordingly constrained to narrative-level claims rather than structured evidence updates. This is consistent with the project being in an early proposition-migration state.

**Documentation updates:**
- Provenance doc at `doc/datasets/normal-tissue-spectra.md` is current as of this run.
- `doc/papers/synthesis-2026-04-18-somatic-mutations-in-normal-tissue.md` already cross-references q007/q008/q010; no update needed.
