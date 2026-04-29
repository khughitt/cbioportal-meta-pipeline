# t083 Cancer-Type Label Canonicalization Design

Date: 2026-04-29
Task: t083
Status: design approved in chat; awaiting written-spec review

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
- `sample_type`
- `sample_type_detailed`

Normalize this code-like field when present:

- `oncotree_code`

Add optional config alias maps:

- `cancer_type_alias_map`
- `cancer_type_detailed_alias_map`
- `primary_site_alias_map`
- `oncotree_code_alias_map`

`sample_type` and `sample_type_detailed` get deterministic whitespace cleanup only. They do
not need alias maps for t083 because the task is about cancer labels, and changing sample-type
vocabularies would be a separate semantic cleanup.

## Behavior

Human-readable labels:

- Strip leading/trailing whitespace.
- Collapse repeated internal whitespace to one space.
- Preserve display case.
- Convert blank strings to missing values.
- Apply the corresponding alias map after basic normalization.
- Normalize mapped values again.

Code-like labels:

- Strip leading/trailing whitespace.
- Collapse repeated internal whitespace to one space.
- Uppercase values.
- Convert blank strings to missing values.
- Apply the corresponding alias map after basic normalization.
- Normalize mapped values again.

Alias map keys are normalized with the same function as incoming data before matching. This
makes config maps robust to accidental extra whitespace. Alias map values are normalized with
the target field's normalization function.

## Error Handling

Fail early for invalid configuration:

- Duplicate alias keys after normalization.
- Alias keys that normalize to missing values.
- Alias values that normalize to missing values.
- Alias map values that are not string-like.

Do not infer OncoTree codes from cancer labels. If `oncotree_code` is missing or blank, it
stays missing unless explicitly provided in the source or mapped by `oncotree_code_alias_map`.

## Interfaces

Create a small pure helper module, `code/scripts/cancer_type_normalization.py`, so tests can
import normalization behavior without executing the Snakemake script body in
`convert_to_feather.py`.

Expected helper surface:

- `normalize_human_label(value: object) -> str | None`
- `normalize_code_label(value: object) -> str | None`
- `canonicalize_alias_map(alias_map: Mapping[str, object], *, normalizer: LabelNormalizer) -> dict[str, str]`
- `normalize_sample_labels(sample_mdat: pd.DataFrame, config: Mapping[str, object]) -> pd.DataFrame`

`normalize_sample_labels` returns a copy and only touches columns that exist.

## Integration

In `convert_to_feather.py`, call:

```python
sample_mdat = normalize_sample_labels(sample_mdat, snek.config)
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
- Duplicate normalized alias keys fail early.
- Empty alias keys and empty alias values fail early.
- Missing optional columns are ignored.

Use the existing `code/scripts/tests/test_convert_to_feather.py` file if import boundaries stay
clear; otherwise add `test_cancer_type_normalization.py`.

## Out Of Scope

- Downloading or vendoring an OncoTree reference table.
- Inferring cancer type from `oncotree_code`, or vice versa.
- Rewriting downstream historical output files.
- Changing gene-symbol normalization; that belongs to t082.
- Changing patient/sample composite IDs; that belongs to t084.

## Verification

Before completion, run:

```bash
uv run --frozen pytest code/scripts/tests/test_cancer_type_normalization.py
uv run --frozen pytest code/scripts/tests/test_convert_to_feather.py
uv run --frozen pyright
uv run --frozen ruff check code/scripts
```

If tests remain in `test_convert_to_feather.py`, the first pytest command should be replaced
with the concrete test file that exists after implementation.
