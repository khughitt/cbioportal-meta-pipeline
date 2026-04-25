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
        bad = ~df[col].isin(list(ENUM_VALUES))
        if bad.any():
            raise ValueError(
                f"{col} has invalid values: {sorted(df.loc[bad, col].unique().tolist())}"
            )
    bad_kinds = ~df["pattern_kind"].isin(list(PATTERN_KIND_VALUES))
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
