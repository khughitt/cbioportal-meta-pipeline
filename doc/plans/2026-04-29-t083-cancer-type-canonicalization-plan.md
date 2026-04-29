# t083 Cancer-Type Label Canonicalization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Normalize cancer-type and related clinical sample labels at ingestion, with optional
config-driven alias maps and no external OncoTree dependency.

**Architecture:** Add a pure helper module for label normalization, alias-map validation, stats,
and logging. Keep `convert_to_feather.py` as the Snakemake integration layer: read clinical
sample metadata, rename columns, call the helper, then continue existing age/MSI/panel handling.

**Tech Stack:** Python 3.13, pandas, pytest, pyright, ruff, Snakemake script integration.

---

## File Structure

- Create `code/scripts/cancer_type_normalization.py`
  - Owns scalar label normalization, alias-map validation, DataFrame normalization, categorical
    rebuilding, per-column stats, and logging.
- Create `code/scripts/tests/test_cancer_type_normalization.py`
  - Unit tests for the pure helper module.
- Modify `code/scripts/convert_to_feather.py`
  - Imports the helper and calls it immediately after clinical sample column rename.
- Modify `tasks/active.md`
  - Only via `uv run --frozen science-tool tasks done t083 --note "Implemented ingest-time cancer label canonicalization with categorical-safe normalization, config-driven aliases, logging, and tests."` during closeout.

## Task 1: Pure Normalization Tests

**Files:**
- Create: `code/scripts/tests/test_cancer_type_normalization.py`
- Create: `code/scripts/cancer_type_normalization.py`

- [ ] **Step 1: Write failing scalar normalization tests**

Add this initial test file:

```python
"""Tests for t083 cancer-type label normalization."""

import pandas as pd
import pytest

from cancer_type_normalization import normalize_code_label, normalize_human_label


def test_human_label_strips_collapses_and_preserves_case() -> None:
    assert normalize_human_label("  Breast   Cancer  ") == "Breast Cancer"
    assert normalize_human_label("breast cancer") == "breast cancer"


def test_code_label_strips_collapses_and_uppercases() -> None:
    assert normalize_code_label("  luad  ") == "LUAD"
    assert normalize_code_label(" nsclc  nos ") == "NSCLC NOS"


@pytest.mark.parametrize("value", ["", "   ", None, pd.NA, float("nan")])
def test_blank_and_missing_labels_return_none(value: object) -> None:
    assert normalize_human_label(value) is None
    assert normalize_code_label(value) is None
```

- [ ] **Step 2: Run scalar tests and verify they fail**

Run:

```bash
uv run --frozen pytest code/scripts/tests/test_cancer_type_normalization.py -q
```

Expected: FAIL during import with `ModuleNotFoundError: No module named 'cancer_type_normalization'`.

- [ ] **Step 3: Add minimal helper module for scalar functions**

Create `code/scripts/cancer_type_normalization.py`:

```python
"""Cancer-type label normalization for convert_to_feather.py.

Implements t083: deterministic whitespace/case cleanup plus optional config-driven
alias maps for cancer labels.
"""

from __future__ import annotations

import re

import pandas as pd

_WHITESPACE_RE = re.compile(r"\s+")


def normalize_human_label(value: object) -> str | None:
    """Normalize a display label while preserving case."""
    if pd.isna(value):
        return None
    normalized = _WHITESPACE_RE.sub(" ", str(value).strip())
    return normalized or None


def normalize_code_label(value: object) -> str | None:
    """Normalize a code-like label using uppercase canonical form."""
    normalized = normalize_human_label(value)
    if normalized is None:
        return None
    return normalized.upper()
```

- [ ] **Step 4: Run scalar tests and verify they pass**

Run:

```bash
uv run --frozen pytest code/scripts/tests/test_cancer_type_normalization.py -q
```

Expected: PASS with `3 passed`.

- [ ] **Step 5: Commit scalar helpers**

Run:

```bash
git add code/scripts/cancer_type_normalization.py code/scripts/tests/test_cancer_type_normalization.py
git commit -m "test: cover cancer label scalar normalization"
```

## Task 2: Alias Map Validation

**Files:**
- Modify: `code/scripts/cancer_type_normalization.py`
- Modify: `code/scripts/tests/test_cancer_type_normalization.py`

- [ ] **Step 1: Add failing alias-map tests**

First replace the existing helper import at the top of
`code/scripts/tests/test_cancer_type_normalization.py` with:

```python
from cancer_type_normalization import (
    canonicalize_alias_map,
    extract_label_alias_maps,
    normalize_code_label,
    normalize_human_label,
)
```

Then append these tests:

```python

def test_alias_map_keys_and_values_are_normalized() -> None:
    aliases = canonicalize_alias_map(
        {"  Breast   Cancer ": "Breast carcinoma"},
        normalizer=normalize_human_label,
    )
    assert aliases == {"Breast Cancer": "Breast carcinoma"}


def test_code_alias_map_uses_code_normalization() -> None:
    aliases = canonicalize_alias_map({" luad ": " lung adeno "}, normalizer=normalize_code_label)
    assert aliases == {"LUAD": "LUNG ADENO"}


def test_alias_map_is_single_pass_and_self_loops_are_allowed() -> None:
    aliases = canonicalize_alias_map(
        {"A": "B", "B": "C", "C": "C"},
        normalizer=normalize_human_label,
    )
    assert aliases == {"A": "B", "B": "C", "C": "C"}


def test_duplicate_normalized_alias_keys_fail() -> None:
    with pytest.raises(ValueError, match="Duplicate alias key"):
        canonicalize_alias_map(
            {"Breast Cancer": "A", "  Breast   Cancer ": "B"},
            normalizer=normalize_human_label,
        )


@pytest.mark.parametrize("bad_key", ["", "   ", None, pd.NA])
def test_empty_alias_keys_fail(bad_key: object) -> None:
    with pytest.raises(ValueError, match="empty alias key"):
        canonicalize_alias_map({bad_key: "Breast Cancer"}, normalizer=normalize_human_label)  # type: ignore[dict-item]


@pytest.mark.parametrize("bad_value", ["", "   "])
def test_empty_alias_values_fail(bad_value: object) -> None:
    with pytest.raises(ValueError, match="empty alias value"):
        canonicalize_alias_map({"Breast Cancer": bad_value}, normalizer=normalize_human_label)  # type: ignore[dict-item]


@pytest.mark.parametrize("bad_value", [None, pd.NA, 123])
def test_non_string_alias_values_raise_typeerror(bad_value: object) -> None:
    with pytest.raises(TypeError, match="must be a string"):
        canonicalize_alias_map({"Breast Cancer": bad_value}, normalizer=normalize_human_label)  # type: ignore[dict-item]


def test_non_mapping_alias_config_fails() -> None:
    with pytest.raises(TypeError, match="cancer_type_alias_map"):
        extract_label_alias_maps({"cancer_type_alias_map": ["not", "a", "mapping"]})


def test_none_alias_config_is_treated_as_empty() -> None:
    assert extract_label_alias_maps({"cancer_type_alias_map": None}) == {}


def test_extract_label_alias_maps_ignores_unrelated_config() -> None:
    maps = extract_label_alias_maps(
        {
            "cancer_type_alias_map": {" breast  cancer ": "Breast carcinoma"},
            "oncotree_code_alias_map": {" luad ": "LUAD"},
            "unrelated": {"A": "B"},
        }
    )
    assert maps == {
        "cancer_type": {"breast cancer": "Breast carcinoma"},
        "oncotree_code": {"LUAD": "LUAD"},
    }
```

- [ ] **Step 2: Run alias-map tests and verify they fail**

Run:

```bash
uv run --frozen pytest code/scripts/tests/test_cancer_type_normalization.py -q
```

Expected: FAIL with import errors for `canonicalize_alias_map` and `extract_label_alias_maps`.

- [ ] **Step 3: Implement alias-map validation**

Update `code/scripts/cancer_type_normalization.py` to include:

```python
from collections.abc import Callable, Mapping

type LabelNormalizer = Callable[[object], str | None]

_ALIAS_CONFIG_TO_COLUMN: Mapping[str, tuple[str, LabelNormalizer]] = {
    "cancer_type_alias_map": ("cancer_type", normalize_human_label),
    "cancer_type_detailed_alias_map": ("cancer_type_detailed", normalize_human_label),
    "primary_site_alias_map": ("primary_site", normalize_human_label),
    "oncotree_code_alias_map": ("oncotree_code", normalize_code_label),
}


def canonicalize_alias_map(
    alias_map: Mapping[object, object], *, normalizer: LabelNormalizer
) -> dict[str, str]:
    """Return alias map normalized for single-pass lookup."""
    out: dict[str, str] = {}
    for raw_key, raw_value in alias_map.items():
        key = normalizer(raw_key)
        if key is None:
            raise ValueError("Label normalization alias map contains an empty alias key.")
        if not isinstance(raw_value, str):
            raise TypeError(
                f"Label normalization alias value for {key!r} must be a string, "
                f"got {type(raw_value).__name__}."
            )
        value = normalizer(raw_value)
        if value is None:
            raise ValueError(f"Label normalization alias map contains an empty alias value for {key!r}.")
        if key in out:
            raise ValueError(f"Duplicate alias key after normalization: {key!r}.")
        out[key] = value
    return out


def extract_label_alias_maps(config: Mapping[str, object]) -> dict[str, dict[str, str]]:
    """Extract and validate t083 alias maps from Snakemake config."""
    out: dict[str, dict[str, str]] = {}
    for config_key, (column, normalizer) in _ALIAS_CONFIG_TO_COLUMN.items():
        raw_aliases = config.get(config_key, {})
        if raw_aliases is None:
            raw_aliases = {}
        if not isinstance(raw_aliases, Mapping):
            raise TypeError(f"{config_key} must be a mapping of raw label to canonical label.")
        aliases = canonicalize_alias_map(raw_aliases, normalizer=normalizer)
        if aliases:
            out[column] = aliases
    return out
```

- [ ] **Step 4: Run alias-map tests and verify they pass**

Run:

```bash
uv run --frozen pytest code/scripts/tests/test_cancer_type_normalization.py -q
```

Expected: PASS.

- [ ] **Step 5: Commit alias-map validation**

Run:

```bash
git add code/scripts/cancer_type_normalization.py code/scripts/tests/test_cancer_type_normalization.py
git commit -m "feat: validate cancer label alias maps"
```

## Task 3: DataFrame Normalization And Stats

**Files:**
- Modify: `code/scripts/cancer_type_normalization.py`
- Modify: `code/scripts/tests/test_cancer_type_normalization.py`

- [ ] **Step 1: Add failing DataFrame normalization tests**

First replace the helper import at the top of
`code/scripts/tests/test_cancer_type_normalization.py` with:

```python
from cancer_type_normalization import (
    LabelNormalizationStats,
    canonicalize_alias_map,
    extract_label_alias_maps,
    normalize_code_label,
    normalize_human_label,
    normalize_sample_labels,
)
```

Then append these tests:

```python

def _sample_labels() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "sample_id": ["S1", "S2", "S3", "S4"],
            "cancer_type": pd.Series(
                ["  Breast   Cancer ", "Lung Cancer", "   ", "breast cancer"],
                dtype="category",
            ),
            "cancer_type_detailed": pd.Series(
                ["  Invasive   Breast Carcinoma ", "LUAD", None, "LUAD"],
                dtype="category",
            ),
            "primary_site": pd.Series([" Breast ", " Lung ", " ", "Breast"], dtype="category"),
            "sample_class": pd.Series([" Tumor ", "Tumor", " ", None], dtype="category"),
            "sample_type": pd.Series([" Primary  Tumor ", "Metastasis", "", None], dtype="category"),
            "sample_type_detailed": pd.Series([" Primary ", " Distant   Metastasis ", "", None], dtype="category"),
            "oncotree_code": pd.Series([" brca ", " luad ", " ", None], dtype="category"),
        }
    )


def test_normalize_sample_labels_cleans_aliases_and_rebuilds_categories() -> None:
    out, stats = normalize_sample_labels(
        _sample_labels(),
        {
            "cancer_type": {"breast cancer": "Breast Carcinoma"},
            "cancer_type_detailed": {"LUAD": "Lung Adenocarcinoma"},
            "oncotree_code": {"BRCA": "BRCA"},
        },
    )

    assert out["cancer_type"].tolist()[:2] == ["Breast Cancer", "Lung Cancer"]
    assert out.loc[3, "cancer_type"] == "Breast Carcinoma"
    assert pd.isna(out.loc[2, "cancer_type"])
    assert out["cancer_type_detailed"].tolist()[:2] == [
        "Invasive Breast Carcinoma",
        "Lung Adenocarcinoma",
    ]
    assert out["primary_site"].tolist()[:2] == ["Breast", "Lung"]
    assert out["sample_class"].tolist()[:2] == ["Tumor", "Tumor"]
    assert out["sample_type"].tolist()[:2] == ["Primary Tumor", "Metastasis"]
    assert out["sample_type_detailed"].tolist()[:2] == ["Primary", "Distant Metastasis"]
    assert out["oncotree_code"].tolist()[:2] == ["BRCA", "LUAD"]

    for column in [
        "cancer_type",
        "cancer_type_detailed",
        "primary_site",
        "sample_class",
        "sample_type",
        "sample_type_detailed",
        "oncotree_code",
    ]:
        assert str(out[column].dtype) == "category"

    by_column = {item.column: item for item in stats}
    assert by_column["cancer_type"].alias_rewritten == 1
    assert by_column["cancer_type"].blanked_to_na == 1
    assert by_column["oncotree_code"].changed == 3


def test_normalize_sample_labels_is_idempotent() -> None:
    first, _ = normalize_sample_labels(_sample_labels(), {"cancer_type": {"breast cancer": "Breast Carcinoma"}})
    second, stats = normalize_sample_labels(first, {"cancer_type": {"breast cancer": "Breast Carcinoma"}})
    pd.testing.assert_frame_equal(first, second)
    assert all(item.changed == 0 and item.alias_rewritten == 0 and item.blanked_to_na == 0 for item in stats)


def test_normalize_sample_labels_alias_resolution_is_single_pass() -> None:
    frame = pd.DataFrame({"sample_id": ["S1"], "cancer_type": ["A"]})
    out, _ = normalize_sample_labels(frame, {"cancer_type": {"A": "B", "B": "C"}})
    assert out.loc[0, "cancer_type"] == "B"


def test_normalize_sample_labels_ignores_missing_optional_columns() -> None:
    frame = pd.DataFrame({"sample_id": ["S1"], "cancer_type": ["  A  "]})
    out, stats = normalize_sample_labels(frame, {"primary_site": {"X": "Y"}})
    assert out["cancer_type"].tolist() == ["A"]
    assert "primary_site" not in out.columns
    assert [item.column for item in stats] == ["cancer_type"]


def test_normalize_sample_labels_returns_copy() -> None:
    frame = pd.DataFrame({"sample_id": ["S1"], "cancer_type": ["  A  "]})
    out, _ = normalize_sample_labels(frame, {})
    assert out is not frame
    assert frame.loc[0, "cancer_type"] == "  A  "
```

- [ ] **Step 2: Run DataFrame tests and verify they fail**

Run:

```bash
uv run --frozen pytest code/scripts/tests/test_cancer_type_normalization.py -q
```

Expected: FAIL with import errors for `LabelNormalizationStats` and `normalize_sample_labels`.

- [ ] **Step 3: Implement DataFrame normalization and stats**

Extend `code/scripts/cancer_type_normalization.py` with:

```python
from collections.abc import Sequence
from dataclasses import dataclass

_HUMAN_LABEL_COLUMNS = (
    "cancer_type",
    "cancer_type_detailed",
    "primary_site",
    "sample_class",
    "sample_type",
    "sample_type_detailed",
)
_CODE_LABEL_COLUMNS = ("oncotree_code",)


@dataclass(frozen=True)
class LabelNormalizationStats:
    """Per-column stats; changed is the total transformed count.

    blanked_to_na and alias_rewritten are non-disjoint subsets of changed.
    """

    column: str
    changed: int
    blanked_to_na: int
    alias_rewritten: int


def normalize_sample_labels(
    sample_mdat: pd.DataFrame, alias_maps: Mapping[str, Mapping[str, str]]
) -> tuple[pd.DataFrame, list[LabelNormalizationStats]]:
    """Normalize clinical sample label columns and rebuild target columns as categoricals."""
    out = sample_mdat.copy()
    stats: list[LabelNormalizationStats] = []
    for column in (*_HUMAN_LABEL_COLUMNS, *_CODE_LABEL_COLUMNS):
        if column not in out.columns:
            continue
        normalizer = normalize_code_label if column in _CODE_LABEL_COLUMNS else normalize_human_label
        aliases = alias_maps.get(column, {})
        normalized_values: list[str | None] = []
        changed = 0
        blanked_to_na = 0
        alias_rewritten = 0
        for value in out[column].astype(object).tolist():
            base = normalizer(value)
            mapped = base
            if base is None:
                if not pd.isna(value):
                    blanked_to_na += 1
            elif base in aliases:
                mapped = aliases[base]
                if mapped != base:
                    alias_rewritten += 1
            if _values_differ(value, mapped):
                changed += 1
            normalized_values.append(mapped)
        series = pd.Series(
            [pd.NA if value is None else value for value in normalized_values],
            index=out.index,
            dtype="object",
        )
        out[column] = series.astype("category")
        stats.append(
            LabelNormalizationStats(
                column=column,
                changed=changed,
                blanked_to_na=blanked_to_na,
                alias_rewritten=alias_rewritten,
            )
        )
    return out, stats


def _values_differ(original: object, normalized: str | None) -> bool:
    if pd.isna(original):
        return normalized is not None
    original_text = str(original)
    if normalized is None:
        return True
    return original_text != normalized
```

- [ ] **Step 4: Run tests and verify they pass**

Run:

```bash
uv run --frozen pytest code/scripts/tests/test_cancer_type_normalization.py -q
```

Expected: PASS.

- [ ] **Step 5: Commit DataFrame normalization**

Run:

```bash
git add code/scripts/cancer_type_normalization.py code/scripts/tests/test_cancer_type_normalization.py
git commit -m "feat: normalize clinical sample cancer labels"
```

## Task 4: Logging And Snakemake Integration

**Files:**
- Modify: `code/scripts/cancer_type_normalization.py`
- Modify: `code/scripts/convert_to_feather.py:7-14`
- Modify: `code/scripts/convert_to_feather.py:230-246`
- Modify: `code/scripts/tests/test_cancer_type_normalization.py`

- [ ] **Step 1: Add failing logging test**

First add `import logging` with the other imports at the top of
`code/scripts/tests/test_cancer_type_normalization.py`.

Then replace the helper import at the top with:

```python
from cancer_type_normalization import (
    LabelNormalizationStats,
    canonicalize_alias_map,
    extract_label_alias_maps,
    log_label_normalization_stats,
    normalize_code_label,
    normalize_human_label,
    normalize_sample_labels,
)
```

Then append this test:

```python

def test_log_label_normalization_stats_emits_per_study_counts(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO, logger="cancer_type_normalization")
    stats = [
        LabelNormalizationStats(column="cancer_type", changed=2, blanked_to_na=1, alias_rewritten=1),
        LabelNormalizationStats(column="oncotree_code", changed=1, blanked_to_na=0, alias_rewritten=0),
    ]

    log_label_normalization_stats(stats, study_id="study_a")

    assert "study study_a" in caplog.text
    assert "cancer_type" in caplog.text
    assert "alias_rewritten=1" in caplog.text
    assert "oncotree_code" in caplog.text
```

- [ ] **Step 2: Run logging test and verify it fails**

Run:

```bash
uv run --frozen pytest code/scripts/tests/test_cancer_type_normalization.py::test_log_label_normalization_stats_emits_per_study_counts -q
```

Expected: FAIL with import error for `log_label_normalization_stats`.

- [ ] **Step 3: Implement logging**

Add to `code/scripts/cancer_type_normalization.py`:

```python
import logging

logger = logging.getLogger("cancer_type_normalization")


def log_label_normalization_stats(
    stats: Sequence[LabelNormalizationStats], *, study_id: str
) -> None:
    """Emit per-study diagnostics for non-zero t083 label normalization events."""
    for item in stats:
        if item.changed == 0 and item.blanked_to_na == 0 and item.alias_rewritten == 0:
            continue
        logger.info(
            "cancer_type_normalization: study %s column %s changed=%d blanked_to_na=%d alias_rewritten=%d",
            study_id,
            item.column,
            item.changed,
            item.blanked_to_na,
            item.alias_rewritten,
        )
```

- [ ] **Step 4: Run logging test and verify it passes**

Run:

```bash
uv run --frozen pytest code/scripts/tests/test_cancer_type_normalization.py::test_log_label_normalization_stats_emits_per_study_counts -q
```

Expected: PASS.

- [ ] **Step 5: Wire helper into `convert_to_feather.py`**

Add this import near the existing helper imports:

```python
from cancer_type_normalization import (
    extract_label_alias_maps,
    log_label_normalization_stats,
    normalize_sample_labels,
)
```

After the sample metadata rename block, before age conversion, insert:

```python
label_alias_maps = extract_label_alias_maps(snek.config)
sample_mdat, label_stats = normalize_sample_labels(sample_mdat, label_alias_maps)
log_label_normalization_stats(label_stats, study_id=snek.wildcards["id"])
```

- [ ] **Step 6: Run helper and existing convert tests**

Run:

```bash
uv run --frozen pytest code/scripts/tests/test_cancer_type_normalization.py code/scripts/tests/test_convert_to_feather.py -q
```

Expected: PASS.

- [ ] **Step 7: Commit integration**

Run:

```bash
git add code/scripts/cancer_type_normalization.py code/scripts/convert_to_feather.py code/scripts/tests/test_cancer_type_normalization.py
git commit -m "feat: apply cancer label normalization on ingest"
```

## Task 5: Static Verification And Task Closeout

**Files:**
- Modify: `AGENTS.md`
- Modify: `tasks/active.md` through `science-tool`
- Modify: `tasks/done/2026-04.md` through `science-tool`

- [ ] **Step 1: Document optional config keys**

Add this paragraph after the hypermutator annotation bullet list in `AGENTS.md`:

```markdown
### Optional ingest-time label canonicalization

`convert_to_feather.py` applies deterministic t083 cleanup to clinical sample labels:
whitespace is stripped/collapsed for `cancer_type`, `cancer_type_detailed`, `primary_site`,
`sample_class`, `sample_type`, and `sample_type_detailed`; `oncotree_code` is also uppercased.
Run configs may provide `cancer_type_alias_map`, `cancer_type_detailed_alias_map`,
`primary_site_alias_map`, and `oncotree_code_alias_map` to collapse known study-specific labels
without adding an external OncoTree table.
```

- [ ] **Step 2: Run focused tests**

Run:

```bash
uv run --frozen pytest code/scripts/tests/test_cancer_type_normalization.py code/scripts/tests/test_convert_to_feather.py -q
```

Expected: PASS.

- [ ] **Step 3: Run pyright**

Run:

```bash
uv run --frozen pyright
```

Expected: `0 errors, 0 warnings, 0 informations`.

- [ ] **Step 4: Run Ruff check**

Run:

```bash
uv run --frozen ruff check code/scripts
```

Expected: `All checks passed!`.

- [ ] **Step 5: Run format check**

Run:

```bash
uv run --frozen ruff format --check code/scripts
```

Expected: all `code/scripts` files are already formatted. If unrelated pre-existing formatting
drift appears, do not reformat unrelated files in this task; record the drift in the final notes
and run the focused format command below instead:

```bash
uv run --frozen ruff format --check code/scripts/cancer_type_normalization.py code/scripts/convert_to_feather.py code/scripts/tests/test_cancer_type_normalization.py
```

- [ ] **Step 6: Mark t083 done**

Run:

```bash
uv run --frozen science-tool tasks done t083 --note "Implemented ingest-time cancer label canonicalization with categorical-safe normalization, config-driven aliases, logging, and tests."
```

Expected: task t083 moves out of `tasks/active.md` into the monthly done file.

- [ ] **Step 7: Commit task closeout**

Run:

```bash
git add AGENTS.md tasks/active.md tasks/done/2026-04.md
git commit -m "chore(tasks): close t083"
```

- [ ] **Step 8: Final status check**

Run:

```bash
git status --short
```

Expected: no output.

## Self-Review

- Spec coverage: Tasks 1-4 cover scalar normalization, alias maps, categorical rebuilding,
  `None` / `pd.NA` missing handling, single-pass aliases, `sample_class`, logging, idempotency,
  optional-column handling, and `convert_to_feather.py` integration. Task 5 covers verification
  and science-tool closeout.
- Placeholder scan: no deferred implementation markers are present.
- Type consistency: helper names match the design doc: `LabelNormalizer`,
  `LabelNormalizationStats`, `extract_label_alias_maps`, `canonicalize_alias_map`,
  `normalize_sample_labels`, and `log_label_normalization_stats`.
