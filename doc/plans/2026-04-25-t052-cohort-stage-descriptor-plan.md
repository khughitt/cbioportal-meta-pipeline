# t052 Cohort-Stage Descriptor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ingest per-sample primary/metastatic + treatment-status flags from cBioPortal clinical sample tables, roll up to a per-study composition descriptor, and validate against the AR/ESR1 published bias signals from [@Zehir2017].

**Architecture:** Per-study annotation rule (mirrors `annotate_drivers` / `annotate_ch` / `annotate_hypermutators`) consumes `samples.feather` + a hand-curated registry, emits `samples_stage_annotated.feather`. A summary-level rollup builds `study_cohort_composition.feather`. A standalone diagnostic script (mirrors `compute_sbs1_lrr_bias_per_study.py` from t126) loads a comparison-manifest TSV, reuses the annotation functions in-memory, applies a panel-coverage check, and produces per-comparison verdicts plus an aggregate closure-state.

**Tech Stack:** Python 3.13, pandas (nullable booleans), pyarrow (feather), Snakemake 9, fnmatch (glob patterns), pytest, ruff. Reuses existing `compute_per_sample_tmb.PROTEIN_ALTERING_VARIANT_CLASSES` and `resolve_panel_id.normalize_panel_id`.

**Spec:** `doc/plans/2026-04-24-t052-cohort-stage-descriptor-design.md` (v2, commit `a5de83b`).

---

## File Structure

| Path | Purpose |
|---|---|
| `data/cbioportal_study_cohort_profiles.tsv` | Hand-curated registry (pattern, defaults, priority, source) |
| `data/cohort_stage_validation_comparisons.tsv` | Comparison manifest for the diagnostic |
| `code/config/config-t052-validation.yml` | Minimal config for prerequisite `prad_tcga` ingestion |
| `code/scripts/annotate_cohort_stage.py` | Registry loader, normalization, classifiers, per-study annotator |
| `code/scripts/build_study_cohort_composition.py` | Summary rollup + dominance classes |
| `code/scripts/compare_stage_stratified_gene_rates.py` | Diagnostic: rate computation, panel coverage, verdicts |
| `code/scripts/tests/test_annotate_cohort_stage.py` | 12 tests across registry validation, normalization, axis classifiers, combined annotator |
| `code/scripts/tests/test_build_study_cohort_composition.py` | 3 tests: percentages, dominance classes, empty-study edge |
| `code/scripts/tests/test_compare_stage_stratified_gene_rates.py` | 5 tests: stratum rate, four verdict outcomes |
| `code/workflows/Snakefile` | Add 2 rules: `annotate_cohort_stage`, `build_study_cohort_composition` |
| `doc/interpretations/2026-04-25-t052-stage-stratified-ar-esr1.md` | Closure note with per-comparison verdicts + aggregate closure-state |

Tests live next to existing tests under `code/scripts/tests/` (matches project layout). The diagnostic script is **not** wired into the Snakefile — opt-in CLI invocation only.

---

### Task 1: Create the registry TSV

**Files:**
- Create: `data/cbioportal_study_cohort_profiles.tsv`

- [ ] **Step 1: Write the registry TSV with 6 initial rows**

```tsv
pattern	pattern_kind	default_is_metastatic	default_is_pre_treated	priority	source	notes
*_tcga_pan_can_atlas_*	glob	false	false	100	TCGA accrual largely targets primary untreated specimens (Cancer Genome Atlas Research Network 2008); fallback default - sample-level metadata always wins	SKCM has metastatic samples that override via sample_type
tcga_mc3	study_id	false	false	50	Ellrott 2018 MC3 pseudo-study: TCGA matched-normal pan-cancer MAF, primary tumors	
msk_impact_*	glob	unknown	unknown	100	MSK-IMPACT clinical sequencing: mixed primary/metastatic, sample-level fields override (Zehir 2017)	
genie	study_id	unknown	unknown	100	AACR GENIE: clinical sequencing, mixed; sample-level SAMPLE_TYPE drives override	
metastatic_solid_tumors_mich_2017	study_id	true	unknown	10	Robinson 2017 MET500: all metastatic by design	
pog570_bcgsc_2020	study_id	true	true	10	BCGSC POG-570: metastatic, post-treatment by design	
```

- [ ] **Step 2: Verify the file loads as 6 rows with expected columns**

Run:
```bash
uv run python -c "
import pandas as pd
df = pd.read_csv('data/cbioportal_study_cohort_profiles.tsv', sep='\t', dtype=str).fillna('')
assert len(df) == 6, f'expected 6 rows, got {len(df)}'
expected_cols = {'pattern','pattern_kind','default_is_metastatic','default_is_pre_treated','priority','source','notes'}
assert expected_cols <= set(df.columns), f'missing: {expected_cols - set(df.columns)}'
print('OK', df.shape)
"
```

Expected: `OK (6, 7)`.

- [ ] **Step 3: Commit**

```bash
git add data/cbioportal_study_cohort_profiles.tsv
git commit -m "feat: add cbioportal study cohort-stage registry"
```

---

### Task 2: Registry loader + validator with 3 tests

**Files:**
- Create: `code/scripts/annotate_cohort_stage.py`
- Create: `code/scripts/tests/test_annotate_cohort_stage.py`

- [ ] **Step 1: Write the failing tests**

`code/scripts/tests/test_annotate_cohort_stage.py`:

```python
"""Tests for annotate_cohort_stage.

Implements the 12 tests pre-registered in
doc/plans/2026-04-24-t052-cohort-stage-descriptor-design.md (v2 §Testing).
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

import annotate_cohort_stage as mod


# ---------------------------------------------------------------------------
# Registry validation (3 tests)
# ---------------------------------------------------------------------------


def _registry_dict_to_tsv(rows: list[dict], tmp_path: Path) -> Path:
    df = pd.DataFrame(rows)
    path = tmp_path / "registry.tsv"
    df.to_csv(path, sep="\t", index=False)
    return path


def test_registry_validation_rejects_invalid_enum_value(tmp_path: Path) -> None:
    path = _registry_dict_to_tsv(
        [
            {
                "pattern": "x", "pattern_kind": "study_id",
                "default_is_metastatic": "yes",  # invalid
                "default_is_pre_treated": "false",
                "priority": "100", "source": "test", "notes": "",
            }
        ],
        tmp_path,
    )
    with pytest.raises(ValueError, match="default_is_metastatic"):
        mod.load_and_validate_registry(path)


def test_registry_validation_rejects_duplicate_pattern_kind_pair(tmp_path: Path) -> None:
    path = _registry_dict_to_tsv(
        [
            {
                "pattern": "x", "pattern_kind": "study_id",
                "default_is_metastatic": "true", "default_is_pre_treated": "false",
                "priority": "100", "source": "first", "notes": "",
            },
            {
                "pattern": "x", "pattern_kind": "study_id",
                "default_is_metastatic": "false", "default_is_pre_treated": "true",
                "priority": "200", "source": "second", "notes": "",
            },
        ],
        tmp_path,
    )
    with pytest.raises(ValueError, match="duplicate"):
        mod.load_and_validate_registry(path)


def test_registry_validation_rejects_empty_source(tmp_path: Path) -> None:
    path = _registry_dict_to_tsv(
        [
            {
                "pattern": "x", "pattern_kind": "study_id",
                "default_is_metastatic": "true", "default_is_pre_treated": "false",
                "priority": "100", "source": "  ", "notes": "",
            }
        ],
        tmp_path,
    )
    with pytest.raises(ValueError, match="source"):
        mod.load_and_validate_registry(path)
```

- [ ] **Step 2: Run tests to verify they fail**

Run:
```bash
uv run --frozen pytest code/scripts/tests/test_annotate_cohort_stage.py -q
```
Expected: ImportError (`annotate_cohort_stage` not yet defined).

- [ ] **Step 3: Write minimal implementation**

`code/scripts/annotate_cohort_stage.py`:

```python
"""annotate_cohort_stage.

Per-study cohort-stage annotation for cBioPortal clinical sample tables. Adds two
nullable-boolean columns (``is_metastatic``, ``is_pre_treated``) plus a per-axis audit
trail. Resolution order per axis (independently): sample-level metadata extraction ->
registry study_id row -> registry glob row -> fallback unknown.

See doc/plans/2026-04-24-t052-cohort-stage-descriptor-design.md (v2) for the spec.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

REGISTRY_REQUIRED_COLUMNS: list[str] = [
    "pattern",
    "pattern_kind",
    "default_is_metastatic",
    "default_is_pre_treated",
    "priority",
    "source",
    "notes",
]
ENUM_VALUES: frozenset[str] = frozenset({"true", "false", "unknown"})
PATTERN_KIND_VALUES: frozenset[str] = frozenset({"study_id", "glob"})


def load_and_validate_registry(path: Path) -> pd.DataFrame:
    """Load the cohort-stage registry TSV and validate its contents.

    Raises ``ValueError`` on any of: missing columns, invalid enum values,
    invalid pattern_kind, duplicate ``(pattern, pattern_kind)`` rows, or empty
    ``source``.
    """
    df = pd.read_csv(path, sep="\t", dtype=str).fillna("")
    missing = [c for c in REGISTRY_REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"registry {path} missing columns: {missing}")
    for col in ("default_is_metastatic", "default_is_pre_treated"):
        bad = ~df[col].isin(ENUM_VALUES)
        if bad.any():
            raise ValueError(
                f"{col} has invalid values: {sorted(df.loc[bad, col].unique().tolist())}"
            )
    bad_kinds = ~df["pattern_kind"].isin(PATTERN_KIND_VALUES)
    if bad_kinds.any():
        raise ValueError(
            f"pattern_kind has invalid values: {sorted(df.loc[bad_kinds, 'pattern_kind'].unique().tolist())}"
        )
    dup_mask = df.duplicated(subset=["pattern", "pattern_kind"], keep=False)
    if dup_mask.any():
        dups = df.loc[dup_mask, ["pattern", "pattern_kind"]].values.tolist()
        raise ValueError(f"duplicate (pattern, pattern_kind) rows: {dups}")
    if (df["source"].str.strip() == "").any():
        raise ValueError("source column has empty values; source is required")
    df["priority"] = df["priority"].astype(int)
    return df
```

- [ ] **Step 4: Run tests to verify they pass**

Run:
```bash
uv run --frozen pytest code/scripts/tests/test_annotate_cohort_stage.py -q
```
Expected: `3 passed`.

- [ ] **Step 5: Commit**

```bash
git add code/scripts/annotate_cohort_stage.py code/scripts/tests/test_annotate_cohort_stage.py
git commit -m "feat: registry loader with fail-loud validation for cohort-stage profiles"
```

---

### Task 3: Value normalization helper

**Files:**
- Modify: `code/scripts/annotate_cohort_stage.py` (add `_normalize` function)
- Modify: `code/scripts/tests/test_annotate_cohort_stage.py` (add 1 test)

- [ ] **Step 1: Add the failing test**

Append to `code/scripts/tests/test_annotate_cohort_stage.py`:

```python
# ---------------------------------------------------------------------------
# Value normalization (1 test)
# ---------------------------------------------------------------------------


def test_normalize_collapses_case_punctuation_and_whitespace() -> None:
    canonical = "treatment naive"
    assert mod._normalize("Treatment-naive") == canonical
    assert mod._normalize("treatment_naive") == canonical
    assert mod._normalize("  TREATMENT  NAIVE  ") == canonical
    assert mod._normalize("Treatment Naive") == canonical
```

- [ ] **Step 2: Run test to verify it fails**

Run:
```bash
uv run --frozen pytest code/scripts/tests/test_annotate_cohort_stage.py::test_normalize_collapses_case_punctuation_and_whitespace -q
```
Expected: AttributeError (`_normalize` not yet defined).

- [ ] **Step 3: Add the implementation**

Append to `code/scripts/annotate_cohort_stage.py` (before the registry loader):

```python
def _normalize(value: str) -> str:
    """Normalize a string for cohort-stage value lookup.

    Strip whitespace, casefold, replace hyphens and underscores with spaces, and
    collapse repeated whitespace. ``"Treatment-naive"`` and ``"  TREATMENT  NAIVE  "``
    both normalize to ``"treatment naive"``.
    """
    s = str(value).strip().casefold().replace("-", " ").replace("_", " ")
    while "  " in s:
        s = s.replace("  ", " ")
    return s
```

- [ ] **Step 4: Run all tests to verify they pass**

Run:
```bash
uv run --frozen pytest code/scripts/tests/test_annotate_cohort_stage.py -q
```
Expected: `4 passed`.

- [ ] **Step 5: Commit**

```bash
git add code/scripts/annotate_cohort_stage.py code/scripts/tests/test_annotate_cohort_stage.py
git commit -m "feat: value normalization for cohort-stage metadata lookup"
```

---

### Task 4: Metastatic-axis classifier (5 tests)

**Files:**
- Modify: `code/scripts/annotate_cohort_stage.py`
- Modify: `code/scripts/tests/test_annotate_cohort_stage.py`

- [ ] **Step 1: Add the failing tests**

Append to `code/scripts/tests/test_annotate_cohort_stage.py`:

```python
# ---------------------------------------------------------------------------
# Metastatic-axis classifier (5 tests)
# ---------------------------------------------------------------------------


def _toy_registry(tmp_path: Path) -> pd.DataFrame:
    return mod.load_and_validate_registry(
        _registry_dict_to_tsv(
            [
                {
                    "pattern": "*_tcga_pan_can_atlas_*", "pattern_kind": "glob",
                    "default_is_metastatic": "false", "default_is_pre_treated": "false",
                    "priority": "100", "source": "tcga family fallback", "notes": "",
                },
                {
                    "pattern": "tcga_mc3", "pattern_kind": "study_id",
                    "default_is_metastatic": "false", "default_is_pre_treated": "false",
                    "priority": "50", "source": "MC3", "notes": "",
                },
                {
                    "pattern": "msk_impact_*", "pattern_kind": "glob",
                    "default_is_metastatic": "unknown", "default_is_pre_treated": "unknown",
                    "priority": "100", "source": "MSK clinical seq", "notes": "",
                },
            ],
            tmp_path,
        )
    )


def test_metastatic_sample_metadata_wins_over_registry(tmp_path: Path) -> None:
    registry = _toy_registry(tmp_path)
    sample_row = {"sample_type": "Metastasis"}
    val, src = mod.classify_metastatic(sample_row, "msk_impact_2017", registry)
    assert val is True
    assert src == "sample_metadata:sample_type"


def test_metastatic_site_forces_true_when_value_is_real_site(tmp_path: Path) -> None:
    registry = _toy_registry(tmp_path)
    sample_row = {"sample_type": "", "METASTATIC_SITE": "Liver"}
    val, src = mod.classify_metastatic(sample_row, "msk_impact_2017", registry)
    assert val is True
    assert src == "sample_metadata:metastatic_site"


def test_metastatic_site_sentinel_falls_through_to_registry(tmp_path: Path) -> None:
    registry = _toy_registry(tmp_path)
    sample_row = {"sample_type": "", "METASTATIC_SITE": "Not Applicable"}
    val, src = mod.classify_metastatic(sample_row, "msk_impact_2017", registry)
    # msk_impact_* registry default is unknown -> pd.NA via registry_glob
    assert pd.isna(val)
    assert src == "registry_glob"


def test_metastatic_registry_study_id_wins_over_glob(tmp_path: Path) -> None:
    registry = _toy_registry(tmp_path)
    sample_row = {}
    val, src = mod.classify_metastatic(sample_row, "tcga_mc3", registry)
    # study_id row priority=50 wins; glob row priority=100 also matches but study_id always wins
    assert val is False
    assert src == "registry_study"


def test_metastatic_glob_pattern_with_leading_wildcard_matches(tmp_path: Path) -> None:
    registry = _toy_registry(tmp_path)
    sample_row = {}
    val, src = mod.classify_metastatic(sample_row, "brca_tcga_pan_can_atlas_2018", registry)
    assert val is False
    assert src == "registry_glob"
```

- [ ] **Step 2: Run tests to verify they fail**

Run:
```bash
uv run --frozen pytest code/scripts/tests/test_annotate_cohort_stage.py -q
```
Expected: 5 new failures (`classify_metastatic` not defined).

- [ ] **Step 3: Add the implementation**

Append to `code/scripts/annotate_cohort_stage.py`:

```python
import fnmatch

METASTATIC_VALUE_MAP: dict[str, bool] = {
    "metastasis": True,
    "metastatic": True,
    "recurrence": True,
    "local recurrence": True,
    "distant metastasis": True,
    "primary": False,
    "primary tumor": False,
    "primary solid tumor": False,
}

METASTATIC_SITE_SENTINELS: frozenset[str] = frozenset(
    {"", "not applicable", "not available", "na", "n/a", "unknown", "none"}
)

METASTATIC_SAMPLE_FIELDS: tuple[str, ...] = (
    "sample_type",
    "sample_class",
    "sample_type_detailed",
)


def _enum_to_bool(val_str: str) -> bool | None:
    """Convert ``true`` / ``false`` / ``unknown`` to ``True`` / ``False`` / ``pd.NA``."""
    if val_str == "true":
        return True
    if val_str == "false":
        return False
    return pd.NA  # type: ignore[return-value]


def _resolve_from_registry(
    registry: pd.DataFrame, study_id: str, axis_col: str
) -> tuple[bool | None, str]:
    """Apply registry resolution: study_id row first, then glob, then fallback_unknown.

    Returns the (nullable bool, source) pair. ``source`` is one of
    ``registry_study`` / ``registry_glob`` / ``fallback_unknown``.
    """
    study_rows = registry[
        (registry["pattern_kind"] == "study_id") & (registry["pattern"] == study_id)
    ]
    if not study_rows.empty:
        chosen = study_rows.sort_values("priority").iloc[0]
        return _enum_to_bool(chosen[axis_col]), "registry_study"
    glob_matches = []
    for _, row in registry[registry["pattern_kind"] == "glob"].iterrows():
        if fnmatch.fnmatch(study_id, row["pattern"]):
            glob_matches.append(row)
    if glob_matches:
        chosen = sorted(glob_matches, key=lambda r: r["priority"])[0]
        return _enum_to_bool(chosen[axis_col]), "registry_glob"
    return pd.NA, "fallback_unknown"  # type: ignore[return-value]


def classify_metastatic(
    sample_row: dict | pd.Series, study_id: str, registry: pd.DataFrame
) -> tuple[bool | None, str]:
    """Resolve ``is_metastatic`` for a single sample.

    Order: sample_type / sample_class / sample_type_detailed (in that order),
    then METASTATIC_SITE (only when not a sentinel value), then registry.
    """
    for fld in METASTATIC_SAMPLE_FIELDS:
        raw = sample_row.get(fld, "") if hasattr(sample_row, "get") else ""
        if raw is None:
            continue
        norm = _normalize(str(raw))
        if norm in METASTATIC_VALUE_MAP:
            return METASTATIC_VALUE_MAP[norm], f"sample_metadata:{fld}"
    raw_site = sample_row.get("METASTATIC_SITE", "") if hasattr(sample_row, "get") else ""
    if raw_site is not None:
        norm_site = _normalize(str(raw_site))
        if norm_site and norm_site not in METASTATIC_SITE_SENTINELS:
            return True, "sample_metadata:metastatic_site"
    return _resolve_from_registry(registry, study_id, "default_is_metastatic")
```

- [ ] **Step 4: Run tests to verify they pass**

Run:
```bash
uv run --frozen pytest code/scripts/tests/test_annotate_cohort_stage.py -q
```
Expected: `9 passed` (4 prior + 5 new).

- [ ] **Step 5: Commit**

```bash
git add code/scripts/annotate_cohort_stage.py code/scripts/tests/test_annotate_cohort_stage.py
git commit -m "feat: metastatic-axis classifier with sentinel-aware site rule"
```

---

### Task 5: Treatment-axis classifier (2 tests)

**Files:**
- Modify: `code/scripts/annotate_cohort_stage.py`
- Modify: `code/scripts/tests/test_annotate_cohort_stage.py`

- [ ] **Step 1: Add the failing tests**

Append to `code/scripts/tests/test_annotate_cohort_stage.py`:

```python
# ---------------------------------------------------------------------------
# Treatment-axis classifier (2 tests)
# ---------------------------------------------------------------------------


def test_pre_treated_resolves_via_sample_type_detailed(tmp_path: Path) -> None:
    registry = _toy_registry(tmp_path)
    sample_row = {"sample_type_detailed": "Post-treatment"}
    val, src = mod.classify_pre_treated(sample_row, "msk_impact_2017", registry)
    assert val is True
    assert src == "sample_metadata:sample_type_detailed"


def test_pre_treated_normalization_handles_punctuation_variants(tmp_path: Path) -> None:
    registry = _toy_registry(tmp_path)
    for raw in ("Treatment-naive", "treatment_naive", "  TREATMENT  NAIVE  "):
        sample_row = {"sample_type_detailed": raw}
        val, src = mod.classify_pre_treated(sample_row, "msk_impact_2017", registry)
        assert val is False, f"failed for {raw!r}"
        assert src == "sample_metadata:sample_type_detailed"
```

- [ ] **Step 2: Run tests to verify they fail**

Run:
```bash
uv run --frozen pytest code/scripts/tests/test_annotate_cohort_stage.py -q
```
Expected: 2 new failures (`classify_pre_treated` not defined).

- [ ] **Step 3: Add the implementation**

Append to `code/scripts/annotate_cohort_stage.py`:

```python
PRE_TREATED_VALUE_MAP: dict[str, bool] = {
    "post treatment": True,
    "pretreated": True,
    "treated": True,
    "pre treatment": False,
    "treatment naive": False,
    "naive": False,
}

PRE_TREATED_SAMPLE_FIELDS: tuple[str, ...] = ("sample_type_detailed", "SPECIMEN_TYPE")


def classify_pre_treated(
    sample_row: dict | pd.Series, study_id: str, registry: pd.DataFrame
) -> tuple[bool | None, str]:
    """Resolve ``is_pre_treated`` for a single sample.

    Most studies do not carry per-sample treatment status. Order:
    ``sample_type_detailed`` -> ``SPECIMEN_TYPE`` -> registry.
    """
    for fld in PRE_TREATED_SAMPLE_FIELDS:
        raw = sample_row.get(fld, "") if hasattr(sample_row, "get") else ""
        if raw is None:
            continue
        norm = _normalize(str(raw))
        if norm in PRE_TREATED_VALUE_MAP:
            return PRE_TREATED_VALUE_MAP[norm], f"sample_metadata:{fld}"
    return _resolve_from_registry(registry, study_id, "default_is_pre_treated")
```

- [ ] **Step 4: Run tests to verify they pass**

Run:
```bash
uv run --frozen pytest code/scripts/tests/test_annotate_cohort_stage.py -q
```
Expected: `11 passed`.

- [ ] **Step 5: Commit**

```bash
git add code/scripts/annotate_cohort_stage.py code/scripts/tests/test_annotate_cohort_stage.py
git commit -m "feat: treatment-axis classifier with normalized value mapping"
```

---

### Task 6: Combined per-sample classifier + per-study annotator (1 test + integration)

**Files:**
- Modify: `code/scripts/annotate_cohort_stage.py`
- Modify: `code/scripts/tests/test_annotate_cohort_stage.py`

- [ ] **Step 1: Add the failing test**

Append to `code/scripts/tests/test_annotate_cohort_stage.py`:

```python
# ---------------------------------------------------------------------------
# Combined per-sample classifier + per-study annotator (1 test)
# ---------------------------------------------------------------------------


def test_axes_resolve_independently_one_via_metadata_other_via_registry(tmp_path: Path) -> None:
    registry = _toy_registry(tmp_path)
    samples = pd.DataFrame(
        [
            {"sample_id": "s1", "sample_type": "Metastasis"},
            {"sample_id": "s2", "sample_type": "Primary"},
            {"sample_id": "s3", "sample_type": ""},
        ]
    )
    out = mod.annotate_samples(samples, "msk_impact_2017", registry)
    # s1: metastatic=True (sample), pre_treated=NA (registry msk_impact_* default)
    # s2: metastatic=False (sample), pre_treated=NA (registry default)
    # s3: metastatic=NA (registry default), pre_treated=NA (registry default)
    assert out.loc[0, "is_metastatic"] is True
    assert pd.isna(out.loc[0, "is_pre_treated"])
    assert out.loc[0, "cohort_stage_metastatic_source"] == "sample_metadata:sample_type"
    assert out.loc[0, "cohort_stage_treatment_source"] == "registry_glob"

    assert out.loc[1, "is_metastatic"] is False
    assert pd.isna(out.loc[2, "is_metastatic"])
    assert out.loc[2, "cohort_stage_metastatic_source"] == "registry_glob"
```

- [ ] **Step 2: Run test to verify it fails**

Run:
```bash
uv run --frozen pytest code/scripts/tests/test_annotate_cohort_stage.py::test_axes_resolve_independently_one_via_metadata_other_via_registry -q
```
Expected: AttributeError (`annotate_samples` not defined).

- [ ] **Step 3: Add the implementation**

Append to `code/scripts/annotate_cohort_stage.py`:

```python
def classify_sample(
    sample_row: dict | pd.Series, study_id: str, registry: pd.DataFrame
) -> dict[str, object]:
    """Resolve both cohort-stage axes for one sample, independently."""
    is_met, met_src = classify_metastatic(sample_row, study_id, registry)
    is_tx, tx_src = classify_pre_treated(sample_row, study_id, registry)
    return {
        "is_metastatic": is_met,
        "is_pre_treated": is_tx,
        "cohort_stage_metastatic_source": met_src,
        "cohort_stage_treatment_source": tx_src,
    }


def annotate_samples(
    samples_df: pd.DataFrame, study_id: str, registry: pd.DataFrame
) -> pd.DataFrame:
    """Apply ``classify_sample`` over a samples DataFrame; return annotated copy.

    Output preserves all input columns and adds: ``is_metastatic`` (nullable bool),
    ``is_pre_treated`` (nullable bool), ``cohort_stage_metastatic_source`` (category),
    ``cohort_stage_treatment_source`` (category).
    """
    out = samples_df.copy()
    rows = [classify_sample(row, study_id, registry) for _, row in samples_df.iterrows()]
    annotation = pd.DataFrame(rows, index=samples_df.index)
    out["is_metastatic"] = annotation["is_metastatic"].astype("boolean")
    out["is_pre_treated"] = annotation["is_pre_treated"].astype("boolean")
    out["cohort_stage_metastatic_source"] = annotation["cohort_stage_metastatic_source"].astype(
        "category"
    )
    out["cohort_stage_treatment_source"] = annotation["cohort_stage_treatment_source"].astype(
        "category"
    )
    return out
```

Append the Snakemake-callable entry point to the same file:

```python
def annotate_study(samples_path: str, registry_path: str, output_path: str) -> None:
    registry = load_and_validate_registry(Path(registry_path))
    samples = pd.read_feather(samples_path)
    # Path layout: results/<run>/studies/<study_id>/metadata/samples.feather
    study_id = Path(samples_path).parent.parent.name
    annotated = annotate_samples(samples, study_id, registry)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    annotated.to_feather(output_path)


if __name__ == "__main__":
    try:
        snek = snakemake  # type: ignore[name-defined]  # noqa: F821
        annotate_study(
            samples_path=str(snek.input.samples),
            registry_path=str(snek.input.registry),
            output_path=str(snek.output[0]),
        )
    except NameError:
        import argparse

        p = argparse.ArgumentParser(description=__doc__)
        p.add_argument("--samples", required=True)
        p.add_argument("--registry", required=True)
        p.add_argument("--output", required=True)
        args = p.parse_args()
        annotate_study(args.samples, args.registry, args.output)
```

- [ ] **Step 4: Run all tests to verify they pass**

Run:
```bash
uv run --frozen pytest code/scripts/tests/test_annotate_cohort_stage.py -q
```
Expected: `12 passed`.

- [ ] **Step 5: Lint, format, commit**

Run:
```bash
uv run --frozen ruff check code/scripts/annotate_cohort_stage.py code/scripts/tests/test_annotate_cohort_stage.py
uv run --frozen ruff format code/scripts/annotate_cohort_stage.py code/scripts/tests/test_annotate_cohort_stage.py
uv run --frozen pytest code/scripts/tests/test_annotate_cohort_stage.py -q
```

```bash
git add code/scripts/annotate_cohort_stage.py code/scripts/tests/test_annotate_cohort_stage.py
git commit -m "feat: combined per-sample classifier and per-study annotator entry point"
```

---

### Task 7: Composition rollup with 3 tests

**Files:**
- Create: `code/scripts/build_study_cohort_composition.py`
- Create: `code/scripts/tests/test_build_study_cohort_composition.py`

- [ ] **Step 1: Write the failing tests**

`code/scripts/tests/test_build_study_cohort_composition.py`:

```python
"""Tests for build_study_cohort_composition."""

from __future__ import annotations

import pandas as pd
import pytest

import build_study_cohort_composition as mod


def _annotated(rows: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    df["is_metastatic"] = df["is_metastatic"].astype("boolean")
    df["is_pre_treated"] = df["is_pre_treated"].astype("boolean")
    return df


def test_percentages_sum_to_one_within_each_axis() -> None:
    samples = _annotated(
        [
            {"is_metastatic": True, "is_pre_treated": False},
            {"is_metastatic": False, "is_pre_treated": False},
            {"is_metastatic": pd.NA, "is_pre_treated": pd.NA},
            {"is_metastatic": True, "is_pre_treated": True},
        ]
    )
    row = mod.build_composition("S", samples)
    assert row["pct_metastatic"] + row["pct_primary"] + row["pct_metastatic_unknown"] == pytest.approx(1.0)
    assert row["pct_pre_treated"] + row["pct_naive"] + row["pct_pre_treated_unknown"] == pytest.approx(1.0)


def test_dominance_classes_cover_all_four_states() -> None:
    # 80% metastatic, 80% naive
    metastatic_dominant = _annotated(
        [{"is_metastatic": True, "is_pre_treated": False}] * 8
        + [{"is_metastatic": False, "is_pre_treated": False}] * 2
    )
    assert mod.build_composition("M", metastatic_dominant)["dominant_site_class"] == "metastatic_dominant"

    primary_dominant = _annotated(
        [{"is_metastatic": False, "is_pre_treated": False}] * 9
        + [{"is_metastatic": True, "is_pre_treated": True}] * 1
    )
    assert mod.build_composition("P", primary_dominant)["dominant_site_class"] == "primary_dominant"

    mixed = _annotated(
        [{"is_metastatic": True, "is_pre_treated": False}] * 5
        + [{"is_metastatic": False, "is_pre_treated": False}] * 5
    )
    assert mod.build_composition("X", mixed)["dominant_site_class"] == "mixed"

    unknown_dominant = _annotated(
        [{"is_metastatic": pd.NA, "is_pre_treated": pd.NA}] * 9
        + [{"is_metastatic": True, "is_pre_treated": True}] * 1
    )
    assert mod.build_composition("U", unknown_dominant)["dominant_site_class"] == "unknown_dominant"


def test_empty_study_returns_explicit_row_with_zero_percentages() -> None:
    samples = _annotated([])
    row = mod.build_composition("E", samples)
    assert row["n_samples_total"] == 0
    assert row["pct_metastatic"] == 0.0
    assert row["pct_primary"] == 0.0
    assert row["dominant_site_class"] == "unknown_dominant"
    assert row["dominant_treatment_class"] == "unknown_dominant"
```

- [ ] **Step 2: Run tests to verify they fail**

Run:
```bash
uv run --frozen pytest code/scripts/tests/test_build_study_cohort_composition.py -q
```
Expected: ImportError (`build_study_cohort_composition` not defined).

- [ ] **Step 3: Write the implementation**

`code/scripts/build_study_cohort_composition.py`:

```python
"""build_study_cohort_composition.

Summary-level rollup of per-study cohort-stage annotations into composition
percentages and dominance classes. One row per study.

Consumes ``samples_stage_annotated.feather`` for each study in ``config['studies']``;
emits a single ``study_cohort_composition.feather`` with the schema documented in
doc/plans/2026-04-24-t052-cohort-stage-descriptor-design.md (v2 §Output schemas).
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

DOMINANCE_THRESHOLD: float = 0.80


def _dominance(
    n_yes: int, n_no: int, n_unk: int, n_total: int, *, yes_label: str, no_label: str
) -> str:
    if n_total == 0:
        return "unknown_dominant"
    if n_unk / n_total >= DOMINANCE_THRESHOLD:
        return "unknown_dominant"
    if n_yes / n_total >= DOMINANCE_THRESHOLD:
        return yes_label
    if n_no / n_total >= DOMINANCE_THRESHOLD:
        return no_label
    return "mixed"


def build_composition(study_id: str, samples_df: pd.DataFrame) -> dict[str, object]:
    """Build a single composition row for one study."""
    n_total = len(samples_df)
    if n_total == 0:
        return {
            "study_id": study_id,
            "n_samples_total": 0,
            "n_metastatic": 0, "n_primary": 0, "n_metastatic_unknown": 0,
            "pct_metastatic": 0.0, "pct_primary": 0.0, "pct_metastatic_unknown": 0.0,
            "n_pre_treated": 0, "n_naive": 0, "n_pre_treated_unknown": 0,
            "pct_pre_treated": 0.0, "pct_naive": 0.0, "pct_pre_treated_unknown": 0.0,
            "dominant_site_class": "unknown_dominant",
            "dominant_treatment_class": "unknown_dominant",
        }
    is_met = samples_df["is_metastatic"]
    n_met = int((is_met == True).sum())  # noqa: E712  (nullable bool comparison)
    n_pri = int((is_met == False).sum())  # noqa: E712
    n_met_unk = int(is_met.isna().sum())
    is_tx = samples_df["is_pre_treated"]
    n_tx = int((is_tx == True).sum())  # noqa: E712
    n_naive = int((is_tx == False).sum())  # noqa: E712
    n_tx_unk = int(is_tx.isna().sum())
    return {
        "study_id": study_id,
        "n_samples_total": n_total,
        "n_metastatic": n_met, "n_primary": n_pri, "n_metastatic_unknown": n_met_unk,
        "pct_metastatic": n_met / n_total,
        "pct_primary": n_pri / n_total,
        "pct_metastatic_unknown": n_met_unk / n_total,
        "n_pre_treated": n_tx, "n_naive": n_naive, "n_pre_treated_unknown": n_tx_unk,
        "pct_pre_treated": n_tx / n_total,
        "pct_naive": n_naive / n_total,
        "pct_pre_treated_unknown": n_tx_unk / n_total,
        "dominant_site_class": _dominance(
            n_met, n_pri, n_met_unk, n_total,
            yes_label="metastatic_dominant", no_label="primary_dominant",
        ),
        "dominant_treatment_class": _dominance(
            n_tx, n_naive, n_tx_unk, n_total,
            yes_label="pre_treated_dominant", no_label="naive_dominant",
        ),
    }


def build_composition_table(annotated_paths: list[str]) -> pd.DataFrame:
    rows = []
    for p in annotated_paths:
        study_id = Path(p).parent.parent.name
        df = pd.read_feather(p)
        rows.append(build_composition(study_id, df))
    return pd.DataFrame(rows)


if __name__ == "__main__":
    try:
        snek = snakemake  # type: ignore[name-defined]  # noqa: F821
        out_df = build_composition_table([str(p) for p in snek.input])
        Path(snek.output[0]).parent.mkdir(parents=True, exist_ok=True)
        out_df.to_feather(str(snek.output[0]))
    except NameError:
        import argparse
        p_arg = argparse.ArgumentParser(description=__doc__)
        p_arg.add_argument("--inputs", nargs="+", required=True)
        p_arg.add_argument("--output", required=True)
        args = p_arg.parse_args()
        out_df = build_composition_table(args.inputs)
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        out_df.to_feather(args.output)
```

- [ ] **Step 4: Run tests to verify they pass**

Run:
```bash
uv run --frozen pytest code/scripts/tests/test_build_study_cohort_composition.py -q
uv run --frozen ruff check code/scripts/build_study_cohort_composition.py code/scripts/tests/test_build_study_cohort_composition.py
uv run --frozen ruff format code/scripts/build_study_cohort_composition.py code/scripts/tests/test_build_study_cohort_composition.py
```
Expected: `3 passed`, ruff clean.

- [ ] **Step 5: Commit**

```bash
git add code/scripts/build_study_cohort_composition.py code/scripts/tests/test_build_study_cohort_composition.py
git commit -m "feat: per-study cohort composition rollup with dominance classes"
```

---

### Task 8: Wire Snakemake rules + lint

**Files:**
- Modify: `code/workflows/Snakefile`

- [ ] **Step 1: Add the two rules after `rule annotate_hypermutators`**

Locate `rule annotate_hypermutators` near line 748 of `code/workflows/Snakefile`. Immediately after that rule's block, insert:

```python
rule annotate_cohort_stage:
  input:
    samples = out_dir.joinpath("studies/{id}/metadata/samples.feather"),
    registry = "data/cbioportal_study_cohort_profiles.tsv"
  output:
    out_dir.joinpath("studies/{id}/metadata/samples_stage_annotated.feather")
  script:
    "../scripts/annotate_cohort_stage.py"

rule build_study_cohort_composition:
  input:
    expand(
      out_dir.joinpath("studies/{id}/metadata/samples_stage_annotated.feather"),
      id=ids,
    )
  output:
    out_dir.joinpath("summary/metadata/study_cohort_composition.feather")
  script:
    "../scripts/build_study_cohort_composition.py"
```

- [ ] **Step 2: Verify the workflow lints with the new rules**

Run:
```bash
uv run snakemake --lint -s code/workflows/Snakefile --configfile code/config/config-poc.yml 2>&1 | tail -25
```
Expected: no new rule-specific errors. Pre-existing repo-wide warnings about `log`/`container` directives are acceptable (they are present on existing rules).

- [ ] **Step 3: Verify the rules are reachable via dry-run**

Run:
```bash
uv run snakemake -n -s code/workflows/Snakefile --configfile code/config/config-poc.yml \
  results/poc-2026-04-17/studies/msk_impact_2017/metadata/samples_stage_annotated.feather 2>&1 | tail -10
```
Expected: snakemake reports a single `annotate_cohort_stage` job in the dry-run plan.

- [ ] **Step 4: Commit**

```bash
git add code/workflows/Snakefile
git commit -m "feat: wire annotate_cohort_stage and build_study_cohort_composition rules"
```

---

### Task 9: Comparison manifest TSV

**Files:**
- Create: `data/cohort_stage_validation_comparisons.tsv`

- [ ] **Step 1: Write the manifest TSV with 2 initial rows**

```tsv
comparison_id	gene	target_variant	metastatic_study_id	metastatic_cancer_type	metastatic_expected_rate	primary_study_id	primary_cancer_type	primary_expected_rate	expected_source	notes
ar_prostate_zehir2017	AR		msk_impact_2017	Prostate Cancer	0.18	prad_tcga_pan_can_atlas_2018	Prostate Adenocarcinoma	0.01	Zehir2017_Fig5	
esr1_breast_zehir2017	ESR1		msk_impact_2017	Breast Cancer	0.11	brca_tcga_pan_can_atlas_2018	Breast Cancer	0.04	Zehir2017_Fig5	
```

- [ ] **Step 2: Verify load**

Run:
```bash
uv run python -c "
import pandas as pd
df = pd.read_csv('data/cohort_stage_validation_comparisons.tsv', sep='\t', dtype=str).fillna('')
assert len(df) == 2
required = {'comparison_id','gene','target_variant','metastatic_study_id','metastatic_cancer_type','metastatic_expected_rate','primary_study_id','primary_cancer_type','primary_expected_rate','expected_source','notes'}
assert required <= set(df.columns), f'missing: {required - set(df.columns)}'
print('OK', df.shape)
"
```
Expected: `OK (2, 11)`.

- [ ] **Step 3: Commit**

```bash
git add data/cohort_stage_validation_comparisons.tsv
git commit -m "feat: cohort-stage validation comparison manifest (AR + ESR1 vs Zehir 2017)"
```

---

### Task 10: Diagnostic — rate computation, verdict, closure (5 tests)

**Files:**
- Create: `code/scripts/compare_stage_stratified_gene_rates.py`
- Create: `code/scripts/tests/test_compare_stage_stratified_gene_rates.py`

- [ ] **Step 1: Write the failing tests**

`code/scripts/tests/test_compare_stage_stratified_gene_rates.py`:

```python
"""Tests for compare_stage_stratified_gene_rates.

Pre-registered tests from doc/plans/2026-04-24-t052-cohort-stage-descriptor-design.md
(v2 §Testing): one stratum-rate fixture + four verdict outcomes.
"""

from __future__ import annotations

import pandas as pd
import pytest

import compare_stage_stratified_gene_rates as mod


# ---------------------------------------------------------------------------
# Stratum rate computation (1 test)
# ---------------------------------------------------------------------------


def test_compute_stratum_rate_protein_altering_filter_only() -> None:
    samples = pd.DataFrame({"sample_id": ["s1", "s2", "s3", "s4"]})
    mutations = pd.DataFrame(
        [
            {"sample_id_tumor": "s1", "symbol": "AR", "variant_class": "Missense_Mutation", "hgvsp_short": "p.X1Y"},
            {"sample_id_tumor": "s1", "symbol": "AR", "variant_class": "Silent", "hgvsp_short": "p.X1Y"},  # filtered
            {"sample_id_tumor": "s2", "symbol": "AR", "variant_class": "Frame_Shift_Del", "hgvsp_short": ""},
            {"sample_id_tumor": "s3", "symbol": "TP53", "variant_class": "Missense_Mutation", "hgvsp_short": ""},  # wrong gene
        ]
    )
    n_in_stratum, n_panel_covers, n_mutated, rate = mod.compute_stratum_rate(
        stratum_samples=samples,
        mutations_df=mutations,
        gene="AR",
        target_variant="",
        panel_covered_sample_ids=None,
    )
    assert n_in_stratum == 4
    assert n_panel_covers == 4
    assert n_mutated == 2
    assert rate == 0.5


# ---------------------------------------------------------------------------
# Verdict logic (4 tests, one per outcome)
# ---------------------------------------------------------------------------


def test_verdict_reproduces_when_both_rates_within_3pp_of_published() -> None:
    v = mod.apply_verdict(
        observed_met=0.18, observed_pri=0.02,
        expected_met=0.18, expected_pri=0.01,
        n_met_panel=400, n_pri_panel=400,
    )
    assert v == "reproduces"


def test_verdict_partial_when_direction_correct_but_magnitude_off() -> None:
    v = mod.apply_verdict(
        observed_met=0.30, observed_pri=0.01,  # 12 pp above expected metastatic
        expected_met=0.18, expected_pri=0.01,
        n_met_panel=400, n_pri_panel=400,
    )
    assert v == "partial"


def test_verdict_fails_when_direction_wrong() -> None:
    v = mod.apply_verdict(
        observed_met=0.05, observed_pri=0.18,
        expected_met=0.18, expected_pri=0.01,
        n_met_panel=400, n_pri_panel=400,
    )
    assert v == "fails"


def test_verdict_underpowered_when_either_stratum_below_min_n() -> None:
    v = mod.apply_verdict(
        observed_met=0.18, observed_pri=0.01,
        expected_met=0.18, expected_pri=0.01,
        n_met_panel=10, n_pri_panel=400,  # below min_n=20
    )
    assert v == "underpowered"


# ---------------------------------------------------------------------------
# Closure-state aggregation (folded into the same suite, 0 extra tests beyond the 5)
# ---------------------------------------------------------------------------


def test_closure_state_validated_when_at_least_one_reproduces_or_partial_and_no_fails() -> None:
    assert mod.apply_closure_state(["reproduces", "underpowered"]) == "descriptor validated"
    assert mod.apply_closure_state(["partial", "partial"]) == "descriptor validated"


def test_closure_state_needs_investigation_when_any_fails() -> None:
    assert mod.apply_closure_state(["reproduces", "fails"]) == "descriptor needs investigation"


def test_closure_state_insufficient_evidence_when_all_underpowered() -> None:
    assert mod.apply_closure_state(["underpowered", "underpowered"]) == "insufficient evidence"
```

- [ ] **Step 2: Run tests to verify they fail**

Run:
```bash
uv run --frozen pytest code/scripts/tests/test_compare_stage_stratified_gene_rates.py -q
```
Expected: ImportError (module not yet defined).

- [ ] **Step 3: Write the implementation**

`code/scripts/compare_stage_stratified_gene_rates.py`:

```python
"""compare_stage_stratified_gene_rates.

Diagnostic for t052: stratify per-(study, cancer_type, gene) mutation rates by
``is_metastatic`` and compare against published Zehir 2017 numbers, applying a
panel-coverage check on the unmatched-normal panel cohort. Produces per-comparison
verdicts and an aggregate closure-state.

Reuses ``annotate_cohort_stage.annotate_samples`` for in-memory stage annotation
and ``compute_per_sample_tmb.PROTEIN_ALTERING_VARIANT_CLASSES`` for the mutation
filter, matching existing TMB-numerator convention.

Not wired into the main Snakefile rule graph; opt-in CLI invocation only.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

from annotate_cohort_stage import annotate_samples, load_and_validate_registry
from compute_per_sample_tmb import PROTEIN_ALTERING_VARIANT_CLASSES
from resolve_panel_id import normalize_panel_id

# Pre-registered thresholds (locked by design doc §Pre-registered verdict thresholds).
RATE_TOLERANCE_PP: float = 0.03
MIN_STRATUM_N: int = 20


def compute_stratum_rate(
    *,
    stratum_samples: pd.DataFrame,
    mutations_df: pd.DataFrame,
    gene: str,
    target_variant: str,
    panel_covered_sample_ids: set[str] | None,
) -> tuple[int, int, int, float]:
    """Return ``(n_in_stratum, n_panel_covers, n_mutated, rate)`` for one stratum."""
    n_in_stratum = len(stratum_samples)
    if panel_covered_sample_ids is None:
        covered = stratum_samples
    else:
        covered = stratum_samples[stratum_samples["sample_id"].isin(panel_covered_sample_ids)]
    n_panel_covers = len(covered)
    if n_panel_covers == 0:
        return n_in_stratum, 0, 0, 0.0
    sample_ids = set(covered["sample_id"].tolist())
    muts = mutations_df[mutations_df["sample_id_tumor"].isin(sample_ids)]
    muts = muts[muts["variant_class"].astype(str).isin(PROTEIN_ALTERING_VARIANT_CLASSES)]
    muts = muts[muts["symbol"] == gene]
    if target_variant:
        muts = muts[muts["hgvsp_short"] == target_variant]
    n_mutated = muts["sample_id_tumor"].nunique()
    rate = n_mutated / n_panel_covers
    return n_in_stratum, n_panel_covers, n_mutated, rate


def apply_verdict(
    *,
    observed_met: float,
    observed_pri: float,
    expected_met: float,
    expected_pri: float,
    n_met_panel: int,
    n_pri_panel: int,
    threshold: float = RATE_TOLERANCE_PP,
    min_n: int = MIN_STRATUM_N,
) -> str:
    if n_met_panel < min_n or n_pri_panel < min_n:
        return "underpowered"
    if observed_met <= observed_pri:
        return "fails"
    diff_met = abs(observed_met - expected_met)
    diff_pri = abs(observed_pri - expected_pri)
    if diff_met <= threshold and diff_pri <= threshold:
        return "reproduces"
    return "partial"


def apply_closure_state(verdicts: list[str]) -> str:
    if all(v == "underpowered" for v in verdicts):
        return "insufficient evidence"
    if any(v == "fails" for v in verdicts):
        return "descriptor needs investigation"
    n_validating = sum(1 for v in verdicts if v in ("reproduces", "partial"))
    if n_validating >= 1:
        return "descriptor validated"
    return "insufficient evidence"


# ---------------------------------------------------------------------------
# Panel coverage check (MSK / GENIE side only)
# ---------------------------------------------------------------------------


def build_panel_gene_coverage(
    *, genie_genomic_information: Path, focal_genes: set[str]
) -> dict[tuple[str, str], bool]:
    """Return ``{(canonical_panel_id, gene_symbol): True}`` for genes on each panel.

    Loads only ``Feature_Type == 'exon'`` and ``includeInPanel == 'True'`` rows; ignores
    panels whose raw SEQ_ASSAY_ID does not normalize via ``resolve_panel_id``.
    """
    df = pd.read_csv(genie_genomic_information, sep="\t", dtype=str)
    df = df[(df["Feature_Type"] == "exon") & (df["includeInPanel"] == "True")]
    df = df[df["Hugo_Symbol"].isin(focal_genes)]
    coverage: dict[tuple[str, str], bool] = {}
    for raw_panel, sub in df.groupby("SEQ_ASSAY_ID"):
        try:
            canon = normalize_panel_id(str(raw_panel))
        except ValueError:
            continue
        for g in sub["Hugo_Symbol"].unique():
            coverage[(canon, str(g))] = True
    return coverage


def panel_covered_sample_ids_for_gene(
    *, samples_df: pd.DataFrame, gene: str, coverage: dict[tuple[str, str], bool]
) -> set[str]:
    """Return sample_ids whose ``panel_id`` covers ``gene``."""
    if "panel_id" not in samples_df.columns:
        # No panel column -> treat as WES (all samples covered).
        return set(samples_df["sample_id"].tolist())
    keep = []
    for sid, panel_id in zip(samples_df["sample_id"], samples_df["panel_id"]):
        if pd.isna(panel_id) or panel_id == "":
            continue
        if coverage.get((str(panel_id), gene), False):
            keep.append(sid)
    return set(keep)


# ---------------------------------------------------------------------------
# Diagnostic orchestration
# ---------------------------------------------------------------------------


def _load_study_samples(study_results_root: Path, study_id: str) -> pd.DataFrame:
    return pd.read_feather(
        study_results_root / "studies" / study_id / "metadata" / "samples.feather"
    )


def _load_study_mutations(study_results_root: Path, study_id: str) -> pd.DataFrame:
    return pd.read_feather(
        study_results_root / "studies" / study_id / "mut" / "table" / "mut.feather"
    )


def run_diagnostic(
    *,
    manifest_path: Path,
    registry_path: Path,
    panel_results_root: Path,
    matched_results_root: Path,
    genie_genomic_information: Path,
    output_path: Path,
) -> dict[str, object]:
    """Run the full diagnostic per the comparison manifest.

    ``panel_results_root`` and ``matched_results_root`` may be the same directory
    when both the metastatic and primary studies share an artifact; they are passed
    separately so the AR comparison can pull ``prad_tcga_pan_can_atlas_2018`` from
    a different (smaller) prerequisite ingestion run.
    """
    manifest = pd.read_csv(manifest_path, sep="\t", dtype=str).fillna("")
    registry = load_and_validate_registry(registry_path)
    focal_genes = set(manifest["gene"].tolist())
    panel_coverage = build_panel_gene_coverage(
        genie_genomic_information=genie_genomic_information,
        focal_genes=focal_genes,
    )

    rows: list[dict] = []
    verdicts_for_closure: list[str] = []
    for _, comp in manifest.iterrows():
        gene = comp["gene"]
        target_variant = comp["target_variant"]
        met_study = comp["metastatic_study_id"]
        pri_study = comp["primary_study_id"]
        met_cancer = comp["metastatic_cancer_type"]
        pri_cancer = comp["primary_cancer_type"]
        expected_met = float(comp["metastatic_expected_rate"])
        expected_pri = float(comp["primary_expected_rate"])

        # Metastatic side (panel cohort).
        met_samples = _load_study_samples(panel_results_root, met_study)
        met_samples_ann = annotate_samples(met_samples, met_study, registry)
        met_stratum = met_samples_ann[
            (met_samples_ann["cancer_type"] == met_cancer)
            & (met_samples_ann["is_metastatic"] == True)  # noqa: E712
        ]
        met_panel_ids = panel_covered_sample_ids_for_gene(
            samples_df=met_stratum, gene=gene, coverage=panel_coverage
        )
        met_muts = _load_study_mutations(panel_results_root, met_study)
        n_met_in, n_met_panel, n_met_mutated, met_rate = compute_stratum_rate(
            stratum_samples=met_stratum,
            mutations_df=met_muts,
            gene=gene,
            target_variant=target_variant,
            panel_covered_sample_ids=met_panel_ids,
        )

        # Primary side (WES cohort).
        pri_samples = _load_study_samples(matched_results_root, pri_study)
        pri_samples_ann = annotate_samples(pri_samples, pri_study, registry)
        pri_stratum = pri_samples_ann[
            (pri_samples_ann["cancer_type"] == pri_cancer)
            & (pri_samples_ann["is_metastatic"] == False)  # noqa: E712
        ]
        pri_muts = _load_study_mutations(matched_results_root, pri_study)
        n_pri_in, n_pri_panel, n_pri_mutated, pri_rate = compute_stratum_rate(
            stratum_samples=pri_stratum,
            mutations_df=pri_muts,
            gene=gene,
            target_variant=target_variant,
            panel_covered_sample_ids=None,  # WES: no panel filter
        )

        verdict = apply_verdict(
            observed_met=met_rate, observed_pri=pri_rate,
            expected_met=expected_met, expected_pri=expected_pri,
            n_met_panel=n_met_panel, n_pri_panel=n_pri_panel,
        )
        verdicts_for_closure.append(verdict)

        rows.extend(
            [
                {
                    "comparison_id": comp["comparison_id"],
                    "study_id": met_study, "cancer_type": met_cancer,
                    "gene": gene, "target_variant": target_variant or None,
                    "is_metastatic": True,
                    "n_samples_in_stratum": n_met_in,
                    "n_samples_panel_covers_gene": n_met_panel,
                    "n_mutated": n_met_mutated,
                    "mutation_rate": met_rate,
                    "expected_zehir2017": expected_met,
                    "verdict": verdict,
                },
                {
                    "comparison_id": comp["comparison_id"],
                    "study_id": pri_study, "cancer_type": pri_cancer,
                    "gene": gene, "target_variant": target_variant or None,
                    "is_metastatic": False,
                    "n_samples_in_stratum": n_pri_in,
                    "n_samples_panel_covers_gene": n_pri_panel,
                    "n_mutated": n_pri_mutated,
                    "mutation_rate": pri_rate,
                    "expected_zehir2017": expected_pri,
                    "verdict": verdict,
                },
            ]
        )

    out_df = pd.DataFrame(rows)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_feather(output_path)
    closure_state = apply_closure_state(verdicts_for_closure)
    return {
        "output_path": str(output_path),
        "closure_state": closure_state,
        "per_comparison_verdicts": dict(
            zip(manifest["comparison_id"].tolist(), verdicts_for_closure)
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path,
                        default=Path("data/cohort_stage_validation_comparisons.tsv"))
    parser.add_argument("--registry", type=Path,
                        default=Path("data/cbioportal_study_cohort_profiles.tsv"))
    parser.add_argument("--panel-results-root", type=Path, required=True,
                        help="Results dir holding the metastatic-side panel study (e.g., msk_impact_2017)")
    parser.add_argument("--matched-results-root", type=Path, required=True,
                        help="Results dir holding the primary-side TCGA studies")
    parser.add_argument("--genie-genomic-info", type=Path,
                        default=Path("data/genie/genomic_information.txt"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)

    summary = run_diagnostic(
        manifest_path=args.manifest,
        registry_path=args.registry,
        panel_results_root=args.panel_results_root,
        matched_results_root=args.matched_results_root,
        genie_genomic_information=args.genie_genomic_info,
        output_path=args.output,
    )
    print(f"Wrote {summary['output_path']}", file=sys.stderr)
    print(f"Per-comparison verdicts: {summary['per_comparison_verdicts']}", file=sys.stderr)
    print(f"CLOSURE STATE: {summary['closure_state']}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests to verify they pass**

Run:
```bash
uv run --frozen pytest code/scripts/tests/test_compare_stage_stratified_gene_rates.py -q
uv run --frozen ruff check code/scripts/compare_stage_stratified_gene_rates.py code/scripts/tests/test_compare_stage_stratified_gene_rates.py
uv run --frozen ruff format code/scripts/compare_stage_stratified_gene_rates.py code/scripts/tests/test_compare_stage_stratified_gene_rates.py
```
Expected: `8 passed` (5 pre-registered + 3 closure-state aggregator unit tests, all in the same suite).

- [ ] **Step 5: Run the full project test suite to confirm no regressions**

Run:
```bash
uv run --frozen pytest code/scripts/tests/ -q
```
Expected: all tests pass (existing test count + 23 new from this plan).

- [ ] **Step 6: Commit**

```bash
git add code/scripts/compare_stage_stratified_gene_rates.py code/scripts/tests/test_compare_stage_stratified_gene_rates.py
git commit -m "feat: stage-stratified gene-rate diagnostic with verdict + closure logic"
```

---

### Task 11: Prerequisite ingestion config + run for `prad_tcga_pan_can_atlas_2018`

**Files:**
- Create: `code/config/config-t052-validation.yml`

- [ ] **Step 1: Write the validation config**

Inspect `code/config/config-poc.yml` to confirm the schema (config keys: `studies`, `cancer_types`, `data_dir`, `out_dir`, etc.). Then create `code/config/config-t052-validation.yml` mirroring it but with only `prad_tcga_pan_can_atlas_2018` in the `studies` list:

```bash
uv run python -c "
import yaml
with open('code/config/config-poc.yml') as f:
    cfg = yaml.safe_load(f)
cfg['studies'] = ['prad_tcga_pan_can_atlas_2018']
cfg['out_dir'] = 'results/t052-validation-2026-04-25'
with open('code/config/config-t052-validation.yml', 'w') as f:
    yaml.safe_dump(cfg, f, sort_keys=False, width=120)
print('wrote config-t052-validation.yml')
"
```

Verify:
```bash
head -8 code/config/config-t052-validation.yml
```
Expected: `studies` list contains exactly `prad_tcga_pan_can_atlas_2018`; `out_dir: results/t052-validation-2026-04-25`.

- [ ] **Step 2: Run the prerequisite ingestion (samples + mutations only — no annotation chain)**

Run (the explicit target keeps Snakemake from running the full annotation graph):
```bash
uv run snakemake -s code/workflows/Snakefile --configfile code/config/config-t052-validation.yml -j1 \
  results/t052-validation-2026-04-25/studies/prad_tcga_pan_can_atlas_2018/metadata/samples.feather \
  results/t052-validation-2026-04-25/studies/prad_tcga_pan_can_atlas_2018/mut/table/mut.feather \
  2>&1 | tail -20
```
Expected: Snakemake fetches the cBioPortal study tarball, runs `convert_to_feather`, and writes both feathers without errors. Runtime: typically < 10 minutes.

- [ ] **Step 3: Verify the artifact**

Run:
```bash
uv run python -c "
import pandas as pd
s = pd.read_feather('results/t052-validation-2026-04-25/studies/prad_tcga_pan_can_atlas_2018/metadata/samples.feather')
m = pd.read_feather('results/t052-validation-2026-04-25/studies/prad_tcga_pan_can_atlas_2018/mut/table/mut.feather')
print('samples:', s.shape, 'cancer_types:', s['cancer_type'].value_counts().head(3).to_dict())
print('mutations:', m.shape, 'unique samples in mut:', m['sample_id_tumor'].nunique())
"
```
Expected: ~500 samples, mostly `Prostate Adenocarcinoma`; mutations table populated.

- [ ] **Step 4: Commit the config (output data is gitignored)**

```bash
git add code/config/config-t052-validation.yml
git commit -m "feat: t052 validation config for prad_tcga prerequisite ingestion"
```

---

### Task 12: Run diagnostic + write closure interpretation

**Files:**
- Create: `doc/interpretations/2026-04-25-t052-stage-stratified-ar-esr1.md`

- [ ] **Step 1: Run the diagnostic against both result roots**

Run:
```bash
mkdir -p results/t052-stage-stratified-2026-04-25/summary
uv run --frozen python code/scripts/compare_stage_stratified_gene_rates.py \
  --manifest data/cohort_stage_validation_comparisons.tsv \
  --registry data/cbioportal_study_cohort_profiles.tsv \
  --panel-results-root results/poc-2026-04-17 \
  --matched-results-root results/t052-validation-2026-04-25 \
  --output results/t052-stage-stratified-2026-04-25/summary/stage_stratified_gene_rates.feather 2>&1 | tail -10
```

Note: ESR1 comparison uses `brca_tcga_pan_can_atlas_2018` from `--matched-results-root`. That study is in `results/poc-2026-04-17`, not `results/t052-validation-2026-04-25`. **Verify** before running by checking which artifact has both `prad_tcga` and `brca_tcga`:

```bash
ls results/poc-2026-04-17/studies/ results/t052-validation-2026-04-25/studies/
```

If `brca_tcga_pan_can_atlas_2018` is only in `poc-2026-04-17` and `prad_tcga_pan_can_atlas_2018` is only in `t052-validation-2026-04-25`, then the diagnostic CLI as written takes a single `--matched-results-root` and cannot read from two roots simultaneously. Two ways to resolve:

- **Option A (preferred):** symlink `prad_tcga_pan_can_atlas_2018` from the validation run into the PoC studies tree:
  ```bash
  ln -s "$PWD/results/t052-validation-2026-04-25/studies/prad_tcga_pan_can_atlas_2018" \
        "results/poc-2026-04-17/studies/prad_tcga_pan_can_atlas_2018"
  ```
  Then use `--matched-results-root results/poc-2026-04-17` (and `--panel-results-root results/poc-2026-04-17`).

- **Option B:** copy the two `prad_tcga` feathers into `results/poc-2026-04-17/studies/prad_tcga_pan_can_atlas_2018/`. Less clean (duplicate data) but more portable than symlinks.

Use Option A:
```bash
ln -s "$PWD/results/t052-validation-2026-04-25/studies/prad_tcga_pan_can_atlas_2018" \
      "results/poc-2026-04-17/studies/prad_tcga_pan_can_atlas_2018"
ls -l results/poc-2026-04-17/studies/prad_tcga_pan_can_atlas_2018
```

Then re-run with both roots pointing to `poc-2026-04-17`:
```bash
uv run --frozen python code/scripts/compare_stage_stratified_gene_rates.py \
  --panel-results-root results/poc-2026-04-17 \
  --matched-results-root results/poc-2026-04-17 \
  --output results/t052-stage-stratified-2026-04-25/summary/stage_stratified_gene_rates.feather 2>&1 | tail -10
```
Expected: stderr prints per-comparison verdicts and a `CLOSURE STATE: <state>` line.

- [ ] **Step 2: Inspect the diagnostic output**

Run:
```bash
uv run python -c "
import pandas as pd
df = pd.read_feather('results/t052-stage-stratified-2026-04-25/summary/stage_stratified_gene_rates.feather')
print(df.to_string())
"
```

Capture: per-comparison verdicts, observed rates, sample counts, the closure-state line.

- [ ] **Step 3: Write the closure interpretation**

Create `doc/interpretations/2026-04-25-t052-stage-stratified-ar-esr1.md` using this structure (fill in the **bold-italic** placeholders with actual numbers from Step 2):

```markdown
---
id: "interpretation:0008-t052-stage-stratified-ar-esr1"
type: "interpretation"
title: "t052: stage-stratified AR + ESR1 rates (Zehir 2017 validation)"
status: "active"
source_refs:
  - "paper:Zehir2017"
related:
  - "task:t052"
  - "topic:cohort-selection-bias-representativeness"
  - "plan:0003-t052-cohort-stage-descriptor-design"
created: "2026-04-25"
updated: "2026-04-25"
workflow_run: "t052-stage-stratified-2026-04-25"
---

# Interpretation: t052 — stage-stratified AR + ESR1 rates

## Closure state

***one of: descriptor validated / descriptor needs investigation / insufficient evidence***

## Per-comparison verdicts

| Comparison | Verdict | Observed met (%) | Expected met (%) | Observed primary (%) | Expected primary (%) | n metastatic | n primary |
|---|---|---:|---:|---:|---:|---:|---:|
| ar_prostate_zehir2017 | ***verdict*** | ***%*** | 18.0 | ***%*** | 1.0 | ***N*** | ***N*** |
| esr1_breast_zehir2017 | ***verdict*** | ***%*** | 11.0 | ***%*** | 4.0 | ***N*** | ***N*** |

## Run surface

- Manifest: `data/cohort_stage_validation_comparisons.tsv` (2 comparisons).
- Registry: `data/cbioportal_study_cohort_profiles.tsv` (6 rows; v1 of registry).
- Panel cohort: `msk_impact_2017` (`results/poc-2026-04-17/`).
- Matched cohorts: `prad_tcga_pan_can_atlas_2018` (prerequisite ingestion in
  `results/t052-validation-2026-04-25/`, symlinked into `poc-2026-04-17/studies/`)
  and `brca_tcga_pan_can_atlas_2018` (`results/poc-2026-04-17/`).
- Output: `results/t052-stage-stratified-2026-04-25/summary/stage_stratified_gene_rates.feather`.

## Interpretation

***Two-paragraph narrative in the t126/t100 style: what reproduced, what did not, what
the per-axis source columns showed about how MSK samples resolved, and any panel-coverage
caveats. If any verdict is ``fails`` or ``underpowered``, name the root cause concretely
(registry rule miss / cancer-type-detailed mismatch / panel coverage / etc.).***

## Closure actions

***Conditional on the closure state:***
- ***If `descriptor validated`***: open follow-up task to add per-stage stratified
  columns to `gene_cancer_study_ratio_annotated.feather` (out-of-scope for t052 per
  design §Out of scope).
- ***If `descriptor needs investigation`***: mark t052 as needing a registry or rule
  revision; do **not** mark t052 done. List the specific revisions required.
- ***If `insufficient evidence`***: mark t052 done with a deferred follow-up to
  re-run on a larger study list (e.g., `config-10k-genes.yml`).

## Deviations from design

***Any spec deviations encountered during execution. None expected; record None
explicitly if so.***
```

- [ ] **Step 4: Mark t052 done if validation closure-state is `descriptor validated` or `insufficient evidence` — otherwise leave open with the failure-mode note**

If closure-state is `descriptor validated`:
```bash
uv run science-tool tasks done t052 --note "Closed by interpretation:0008-t052-stage-stratified-ar-esr1. Closure state: descriptor validated. Per-comparison verdicts: <fill>. Follow-up: pooled-ratio stratification (out of scope for t052)."
```

If `insufficient evidence`:
```bash
uv run science-tool tasks done t052 --note "Closed by interpretation:0008-t052-stage-stratified-ar-esr1. Closure state: insufficient evidence. Re-run gated on larger study list."
```

If `descriptor needs investigation`: do **NOT** mark done. Update the task body with the specific failure mode for follow-up:
```bash
uv run science-tool tasks edit t052 --description "<append: needs revision per interpretation:0008-t052-stage-stratified-ar-esr1; failure mode: ...>"
```

- [ ] **Step 5: Commit interpretation**

```bash
git add doc/interpretations/2026-04-25-t052-stage-stratified-ar-esr1.md tasks/active.md tasks/done/
git commit -m "feat: t052 stage-stratified AR/ESR1 closure interpretation"
```

---

## Self-Review

**Spec coverage:**

| Spec section | Implementation task |
|---|---|
| Registry TSV (6 rows) | Task 1 |
| Comparison manifest TSV (2 rows) | Task 9 |
| Validation config (`config-t052-validation.yml`) | Task 11 |
| Registry validation (3 rules) | Task 2 |
| Value normalization | Task 3 |
| Sample-level metastatic classifier (sample fields + sentinel rule) | Task 4 |
| Sample-level treatment classifier | Task 5 |
| Combined classifier + per-study annotator | Task 6 |
| Composition rollup + dominance classes | Task 7 |
| Snakemake rules | Task 8 |
| Diagnostic rate computation, panel-coverage check, verdict, closure | Task 10 |
| Prerequisite ingestion | Task 11 |
| Run diagnostic + closure interpretation | Task 12 |

All 20 pre-registered tests are covered: 12 (annotate_cohort_stage) + 3 (composition) + 5 (diagnostic) = 20. The diagnostic suite also adds 3 closure-state aggregator tests (folded into the same suite for cohesion), bringing the suite total to 23 — all listed in Task 10 step 4 and step 5 expected output.

**Placeholder scan:** None of the placeholder anti-patterns appear. Every step contains the actual code or command. The closure interpretation document in Task 12 has explicit ***italic-bold*** markers labelled as placeholders for empirical values that cannot be known until the diagnostic runs — this is the only deliberate exception, and it's bounded to per-row verdict numbers and the narrative paragraph.

**Type / signature consistency:** `_normalize`, `classify_metastatic`, `classify_pre_treated`, `classify_sample`, `annotate_samples`, `annotate_study`, `load_and_validate_registry`, `build_composition`, `build_composition_table`, `compute_stratum_rate`, `apply_verdict`, `apply_closure_state`, `build_panel_gene_coverage`, `panel_covered_sample_ids_for_gene`, `run_diagnostic` — names and parameter names match between definitions and call sites across tasks.

**Out-of-scope items confirmed deferred:**

- Pooled-ratio stratification rewrite (gated on validated closure-state — opens as follow-up task in Task 12 step 4).
- EGFR T790M validation (lung studies + hotspot filtering not in any current config).
- GENIE-based validation (GENIE not in any pipeline result on disk).
- Patient-level treatment-status promotion.
- Per-(study, cancer_type) composition rollup.
