# t083 Cancer-Type Label Canonicalization Design

Date: 2026-04-29
Task: t083
Status: design review addressed; awaiting final written-spec review

## Goal

Normalize cancer-type and related clinical sample labels once, at ingestion, so downstream
aggregation sees deterministic labels across studies. This addresses low-level label drift
such as leading/trailing whitespace, inconsistent spacing, and mixed casing in code-like
fields without introducing a full external OncoTree dependency.

## Scope

Implement a config-driven normalization layer in `code/scripts/convert_to_feather.py` after
clinical sample columns are renamed and before MSI/panel annotations are attached.

Normalize these human-readable fields when present:

- `cancer_type`
- `cancer_type_detailed`
- `primary_site`
- `sample_class`
- `sample_type`
- `sample_type_detailed`

Normalize this code-like field when present:

- `oncotree_code`

Add optional config alias maps:

- `cancer_type_alias_map`
- `cancer_type_detailed_alias_map`
- `primary_site_alias_map`
- `oncotree_code_alias_map`

`sample_class`, `sample_type`, and `sample_type_detailed` get deterministic whitespace cleanup
only. They do not need alias maps for t083 because the task is about cancer labels, and
changing sample-class / sample-type vocabularies would be a separate semantic cleanup.

## Behavior

Shared rules:

- Strip leading/trailing whitespace.
- Collapse repeated internal whitespace to one space.
- Treat blank strings as missing; output columns encode them as `pd.NA`.
- Apply the corresponding alias map after basic normalization.
- Normalize mapped values again.

Human-readable labels preserve display case. Code-like labels are uppercased after whitespace
normalization.

Normalization is single-pass with respect to aliases. If the alias map contains `{"A": "B",
"B": "C"}`, an input value of `A` resolves to `B`, not `C`. Self-loops such as `{"A": "A"}`
are tolerated because they are harmless and can be useful while auditing config files.

Alias map keys are normalized with the same function as incoming data before matching. This
makes config maps robust to accidental extra whitespace. Alias map values are normalized with
the target field's normalization function.

## Dtypes And Missing Values

`convert_to_feather.py` currently reads these fields as pandas categoricals. The normalization
helper must not assign new values directly into existing categorical arrays because aliases may
create values not present in the original category set.

The implementation will:

1. Read each target column as an object/string-like series for transformation.
2. Use `None` as the scalar helper's "missing" return value for simple config validation.
3. Convert missing normalized values to `pd.NA` in output columns.
4. Rebuild the output column as `category`, with categories inferred from normalized non-missing
   values, for every target column present in `sample_mdat`.

This preserves the existing categorical output contract while avoiding pandas category-assignment
failures.

## Error Handling

Fail early for invalid configuration:

- Duplicate alias keys after normalization.
- Alias keys that normalize to missing values.
- Alias values that normalize to missing values.
- Alias map values that are not string-like.

Do not infer OncoTree codes from cancer labels. If `oncotree_code` is missing or blank, it
stays missing unless explicitly provided in the source or mapped by `oncotree_code_alias_map`.

Config validation happens when `convert_to_feather.py` invokes the helper for each study. A bad
alias map may therefore fail in multiple study rules in a parallel Snakemake run. The helper will
also expose a separate validation/extraction callable so a future preflight rule can validate the
same config once without touching study files.

## Interfaces

Create a small pure helper module, `code/scripts/cancer_type_normalization.py`, so tests can
import normalization behavior without executing the Snakemake script body in
`convert_to_feather.py`.

Expected helper surface:

- `normalize_human_label(value: object) -> str | None`
- `normalize_code_label(value: object) -> str | None`
- `type LabelNormalizer = Callable[[object], str | None]`
- `@dataclass(frozen=True) class LabelNormalizationStats`
- `extract_label_alias_maps(config: Mapping[str, object]) -> dict[str, dict[str, str]]`
- `canonicalize_alias_map(alias_map: Mapping[str, str], *, normalizer: LabelNormalizer) -> dict[str, str]`
- `normalize_sample_labels(sample_mdat: pd.DataFrame, alias_maps: Mapping[str, Mapping[str, str]]) -> tuple[pd.DataFrame, list[LabelNormalizationStats]]`
- `log_label_normalization_stats(stats: Sequence[LabelNormalizationStats], *, study_id: str) -> None`

`extract_label_alias_maps` is the config boundary. It accepts the whole config mapping, pulls out
only the four t083 alias-map keys, validates them, and returns alias maps keyed by normalized
sample column name (`cancer_type`, `cancer_type_detailed`, `primary_site`, `oncotree_code`).

`normalize_sample_labels` returns a copy and only touches columns that exist. The stats object
reports, per column, counts for changed values, blank-to-missing conversions, and alias rewrites.

## Integration

In `convert_to_feather.py`, call:

```python
label_alias_maps = extract_label_alias_maps(snek.config)
sample_mdat, label_stats = normalize_sample_labels(sample_mdat, label_alias_maps)
log_label_normalization_stats(label_stats, study_id=snek.wildcards["id"])
```

after the sample clinical metadata rename block and before age conversion, MSI ingestion, and
panel-id resolution. This ensures all later consumers see normalized labels.

No Snakefile input changes are needed for t083. No data reference table is added.

## Testing

Add focused unit tests for:

- Whitespace cleanup and blank-to-missing behavior for human-readable labels.
- `oncotree_code` uppercasing.
- Alias-map application after source normalization.
- Alias-map target normalization.
- Single-pass alias semantics.
- Duplicate normalized alias keys fail early.
- Empty alias keys and empty alias values fail early.
- Idempotency: normalizing an already-normalized frame leaves labels unchanged.
- Missing optional columns are ignored.
- Output target columns are categorical with rebuilt categories.

Add these tests in `code/scripts/tests/test_cancer_type_normalization.py`. Keep the existing
`code/scripts/tests/test_convert_to_feather.py` panel-id tests as the integration smoke coverage
for the script-adjacent ingest path.

## Out Of Scope

- Downloading or vendoring an OncoTree reference table.
- Inferring cancer type from `oncotree_code`, or vice versa.
- Rewriting downstream historical output files.
- Changing gene-symbol normalization; that belongs to t082.
- Changing patient/sample composite IDs; that belongs to t084.

Running t083 on existing studies may change per-study `cancer_types` counts in
`study.feather`, because that count is computed from the normalized `sample_mdat.cancer_type`.
That cardinality change is expected when previously distinct whitespace/case variants collapse.

## Verification

Before completion, run:

```bash
uv run --frozen pytest code/scripts/tests/test_cancer_type_normalization.py
uv run --frozen pytest code/scripts/tests/test_convert_to_feather.py
uv run --frozen pyright
uv run --frozen ruff check code/scripts
```
