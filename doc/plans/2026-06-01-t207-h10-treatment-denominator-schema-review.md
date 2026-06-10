# Pipeline Review: H10 treatment-denominator schema and impact pass

- **Plan:** `doc/plans/2026-06-01-t207-h10-treatment-denominator-schema.md`
- **Related:** `plan:0011-t207-h10-treatment-denominator-schema`, `hypothesis:0009-treatment-induced-signature-frequency-contamination`, `question:0024-treatment-exposed-cohort-chemotherapy-signature`, `question:0027-does-excluding-treatment-signature-high-samples`, `task:t207`
- **Date:** 2026-06-01
- **Overall:** WARN

## Summary

This is a careful, well-instrumented plan. Its central design move — layering broad
treatment-exposure, mutagenic-treatment expectation, PDX sensitivity, positive-naive, and
unknown-metadata as *separate* config fields rather than a flat `treatment_exposed_studies`
list — correctly preserves the specific SBS11/31/35/87 prediction in `hypothesis:0009` and
faithfully implements the t206 manual-review recommendation. Validation criteria and
hard-fail QA are a standout strength. Two issues hold it back from a clean PASS: (1) the
plan operationalizes treatment **exposure labels** (q024), but is filed against q027, whose
impact test is defined on therapy-**signature-high** samples — these are not the same
exclusion set and the relationship must be stated; and (2) the `no_detected_treatment_signal`
cohort view is defined inconsistently between WP3 and WP4. A handful of integration-boundary
details (column-name mapping, raw-clinical sample-ID join, manifest emission) need pinning
before implementation.

## Rubric Results

| Dimension | Score | Issues |
|---|---|---|
| Evidence coverage | PASS | Labels traced to t206 audit; provisional `manual-review-v0` provenance explicit |
| Assumption audit | WARN | Exposure-label exclusion is conflated with the signature-high exclusion that q027 names |
| Data availability | WARN | WP2 depends on raw `data_clinical_sample.txt` columns not present in canonical `samples.feather`; sample-ID join key unspecified |
| Identifiability | WARN | First pass has ~1 study-level primary-mutagenic flag and `sample_level_rules: {}`; most primary contrasts will be `underpowered_non_arbitrating`/`no_contrast` |
| Reproducibility | PASS | Deterministic label assignment; inherits pinned `random_seed`/hypermutator layer; no new stochastic step |
| Validation criteria | PASS | Per-WP DoD + input assertions + inter-stage invariants + sanity checks + failure modes |
| Scope check | PASS | Causal estimation explicitly a non-goal; opt-in target keeps canonical contract untouched |
| Integration boundaries | WARN | WP3 column names diverge from `create_freq_tables.py` (`*_inclusive/_exclusive`); reproduction invariant needs a documented mapping |
| Manifest completeness | WARN | New `summary/mut/table/*` outputs should emit `datapackage.json` (existing convention); WP5 names only a QA report |

## Detailed Findings

### Assumption audit — exposure label vs signature-high exclusion (highest priority)

The plan's `related` block and `q027` both name *"excluding therapy-signature-high samples
(SBS11/31/35/87)"* as the impact test. But every cohort view in this plan excludes samples by
**treatment-exposure label** (study-level or sample-level clinical rule), not by measured
signature exposure. These are different sets:

- A platinum-treated sample with no detectable SBS31/35 would be excluded by this plan but
  retained by the q027 signature-based test.
- A high-SBS11 sample in a study with no treatment-named clinical column would be excluded by
  q027 but retained here.

This is a legitimate and useful arm (it answers the Purpose's *first* question — "does
cohort composition by treatment history change the deliverable?", i.e. q024). The problem is
only that the plan files itself against q027 without saying it is the **complementary
exposure arm**, leaving the eventual impact note at risk of being read as the q027 answer.

**Recommendation:** Add one paragraph (Purpose or a new "Relationship to q027" note) stating
that this pass answers the exposure-label arm; the signature-high arm (h10 Prediction 2/3,
q027) is served by the h08 per-sample signature exposures (`method:h08-agnostic-association-model`,
t178/t179) or is explicitly deferred. The two arms adjudicate each other — say so.

### Internal consistency — `no_detected_treatment_signal` defined two ways

- WP3 cohort-view table: `no_detected_treatment_signal` = *"excludes primary
  mutagenic-treatment labels; comparator is not confirmed naive"*.
- WP4 impact field: `mean_no_detected_treatment_signal` = *"mean ratio after primary
  mutagenic-treatment exclusion"*.

Both descriptions make `no_detected_treatment_signal` indistinguishable from
`mutagenic_treatment_excluded_primary`. The audit's intent (t206 §Interpretation) is that
`no_detected_treatment_signal` is the **retained comparator cohort** — samples negative for
*all* treatment flags — not an exclusion view. As written, two of the five cohort views may
compute the identical denominator.

**Recommendation:** Pick one definition explicitly. Suggested: `no_detected_treatment_signal`
= samples with no positive treatment label of any tier (the comparator/"kept" group);
`mutagenic_treatment_excluded_primary` = `all_samples` minus mutagenic-labeled (the
exclusion/"deliverable-as-corrected" group). They are complements only when broad-but-not-
mutagenic and positive-naive samples are absent, so they must be named distinctly.

### Identifiability / power — the first pass is near-empty for the primary test

At schema introduction the primary mutagenic layer is one study at study level
(`blca_dfarber_mskcc_2014`) with `sample_level_rules: {}`. Consequences:

- `mutagenic_treatment_excluded_primary` excludes exactly one study's samples; for every
  cancer type except bladder the view equals `all_samples` → `no_contrast`.
- Bladder itself has **no clean naive comparator in-config**: `blca_cornell_2016` is a
  fraction-review candidate, not yet a rule. So even bladder is likely
  `underpowered_non_arbitrating`.

The `h10_power_status` field is exactly the right defensive instrument and earns the plan
credit. But the plan should set the expectation that **the first impact note is expected to be
largely `no_contrast`/`underpowered`**, and that the informative pass arrives only after
`blca_cornell_2016` and `difg_glass_2019` sample-level rules land. Otherwise a near-null first
note could be mis-read as "H10 impact is negligible" (the falsification clause in the
hypothesis) when it is really "the test has not yet been powered."

**Recommendation:** State the staged expectation in WP4/WP5, and consider gating the
interpretation note on at least one sample-level rule being populated (blca_cornell_2016 or
difg_glass_2019), or clearly label the first note as a plumbing/no-contrast checkpoint.

### Data availability + integration — raw clinical columns and the sample-ID join

WP2 reads sample-level clinical columns (`TMZ_TREATMENT`, `CONCURRENT_TMZ`,
`SPECIMEN_COLLECTION_PRE_OR_POST_CHEMO`, `TX_CISPLATIN`, `TREATMENT_STATUS`). Verified: these
live only in raw `data_clinical_sample.txt` under `data_dir`
(`audit_treatment_exposed_studies.py:186` reads exactly that file); they are **not** carried
into the canonical `metadata/samples_annotated.feather` that `create_freq_tables.py` consumes.
So WP2 must join two ID spaces: raw cBioPortal `SAMPLE_ID` and the pipeline's normalized
`sample_id` (after `convert_to_feather.py` t083 label cleanup). The plan's DoD says "every
sample appears once" but never specifies this join key or what happens on a raw-vs-canonical
ID mismatch.

**Recommendation:** Add an explicit QA assertion: every sample-level rule row must match a
canonical `sample_id` after normalization; unmatched raw IDs hard-fail (consistent with the
plan's "missing clinical columns hard-fail" stance). Note also that `create_freq_tables.py`
consumes `samples_annotated.feather`, not `samples.feather` (Snakefile:95,115) — WP2/WP3
should name the same input to keep panel_id and hypermutator flags aligned.

### Integration — output column names diverge from the canonical builder

WP3 specifies `num / n_samples / ratio / num_hypermutator_excluded /
n_samples_hypermutator_excluded / ratio_hypermutator_excluded`. The canonical
`create_freq_tables.py` emits `num_inclusive / num_exclusive / n_samples_inclusive /
n_samples_exclusive` (+ `num`/`ratio` as inclusive aliases). The WP3/QA invariant "the
`all_samples` view reproduces `create_freq_tables.py` counts" therefore requires a documented
mapping: `all_samples ↔ *_inclusive`; `*_hypermutator_excluded ↔ *_exclusive`.

**Recommendation:** State the mapping in WP3, and have the reproduction test assert column-by-
column against the renamed canonical columns rather than against ambiguous names. This also
guards the plan's own goal of not reusing `_exclusive` for treatment semantics — the new
`_hypermutator_excluded` suffix is good; just tie it to the canonical `_exclusive` explicitly.

### Manifest completeness

The plan adds `summary/mut/table/gene_cancer_h10_treatment_impact{,_ratio}.feather` and a QA
report, but existing summary outputs ship a `.datapackage.json` (Snakefile:53). WP5 lists a QA
report but no manifest.

**Recommendation:** Emit a `datapackage.json` for the new summary outputs listing resources +
the entity cross-refs (`hypothesis:0009`, `task:t207`) + provenance inputs, matching the
existing convention.

### Minor — asymmetric impact readout

The impact table gives `mean_*` for all five views but `delta_*` / `rank_*` only for
`mutagenic_primary`. The broad-treatment sensitivity view then has a mean but no quantified
shift/rank-shift, which is the actual sensitivity signal. Consider adding `delta_broad` /
`rank_delta_broad` (or state why the broad view is mean-only).

## Recommendations

1. **State the exposure-vs-signature relationship to q027** explicitly (highest priority) —
   one paragraph clarifying this is the exposure-label arm, complementary to the signature
   arm.
2. **Disambiguate `no_detected_treatment_signal`** (comparator group) from
   `mutagenic_treatment_excluded_primary` (exclusion view) in both WP3 and WP4.
3. **Set the staged power expectation** — first note is expected near-`no_contrast`; gate the
   interpretation on ≥1 sample-level rule or label it a plumbing checkpoint.
4. **Pin the raw-clinical → canonical `sample_id` join** with a hard-fail assertion; name
   `samples_annotated.feather` as the canonical input.
5. **Document the column-name mapping** to `create_freq_tables.py` and assert it in the
   reproduction test.
6. **Emit `datapackage.json`** for the new summary outputs.

## Strengths

- Layered labels (broad / mutagenic / PDX-sensitivity / positive-naive / unknown) faithfully
  implement t206 and prevent ICB/endocrine/targeted cohorts from diluting the SBS-specific
  prediction — the single most important design decision, and it is correct.
- `no_detected_treatment_signal` ≠ confirmed-naive is preserved end-to-end (Non-Goals,
  acceptance criteria, DoD), honoring the unmeasured-recall caveat over 109 studies.
- PDX cohorts isolated to a named sensitivity view with a sound mechanistic rationale
  (passaging / mouse-read artifacts independent of patient treatment).
- Sample-level over fractional denominators is well-justified (fractions cannot identify which
  mutated samples to drop, distorting numerator and denominator differently).
- `h10_power_status` is exactly the right defensive instrument for a thin-contrast test.
- Hard-fail config validation (conflicting labels, PDX-in-primary, unknown-never-silent) and
  the full QA ladder (input assertions → inter-stage invariants → sanity checks → failure
  modes) are exemplary.
- Opt-in target leaves the canonical hypermutator inclusive/exclusive contract untouched.

## Note on process

No `science inquiry` status update was made: this is a `type: plan` document, not a
registered inquiry slug, and the parent analysis-plan kind (`analysis-plan`) is not registered
in the active profile (surfaced by `science validate`). Review filed under the repo's existing
`doc/plans/<stem>-review.md` convention.
