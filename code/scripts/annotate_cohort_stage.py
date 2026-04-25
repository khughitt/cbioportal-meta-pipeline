"""annotate_cohort_stage.

Per-study cohort-stage annotation for cBioPortal clinical sample tables. Adds two
nullable-boolean columns (``is_metastatic``, ``is_pre_treated``) plus a per-axis audit
trail. Resolution order per axis (independently): sample-level metadata extraction ->
registry study_id row -> registry glob row -> fallback unknown.

See doc/plans/2026-04-24-t052-cohort-stage-descriptor-design.md (v2) for the spec.
"""

from __future__ import annotations

import fnmatch
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
    raw_site = (
        sample_row.get("METASTATIC_SITE", "") if hasattr(sample_row, "get") else ""
    )
    if raw_site is not None:
        norm_site = _normalize(str(raw_site))
        if norm_site and norm_site not in METASTATIC_SITE_SENTINELS:
            return True, "sample_metadata:metastatic_site"
    return _resolve_from_registry(registry, study_id, "default_is_metastatic")


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
    rows = [
        classify_sample(row, study_id, registry) for _, row in samples_df.iterrows()
    ]
    annotation = pd.DataFrame(rows, index=samples_df.index)
    # Use object dtype to preserve Python bool/None values for nullable semantics
    out["is_metastatic"] = annotation["is_metastatic"]
    out["is_pre_treated"] = annotation["is_pre_treated"]
    out["cohort_stage_metastatic_source"] = annotation[
        "cohort_stage_metastatic_source"
    ].astype("category")
    out["cohort_stage_treatment_source"] = annotation[
        "cohort_stage_treatment_source"
    ].astype("category")
    return out


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
