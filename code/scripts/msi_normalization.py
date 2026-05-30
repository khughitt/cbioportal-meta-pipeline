# science:code
# status: library
# decision_bearing: false
# science:end
"""
msi_normalization.py

MSI (microsatellite instability) column parsing + value normalization for the
per-study ``samples.feather`` artifact. Factored out of ``convert_to_feather.py``
for testability; see t081 plan task 4 at
``doc/plans/2026-04-13-t081-hypermutator-annotation-pipeline-plan.md``.

Consumers (currently only ``convert_to_feather.py``) invoke
``normalize_msi_columns(sample_df)`` which returns a new DataFrame with two
additional columns:

- ``msi_type`` (str) : one of ``{"MSI-H", "MSI-L", "MSS", "Indeterminate"}`` or NaN.
  Parsed from whichever of ``MSI_TYPE`` / ``MSI_STATUS`` is present in the input
  (preferring ``MSI_TYPE`` when both are available), normalized via the explicit
  ``MSI_TYPE_NORMALIZATION`` mapping table, case-insensitive with whitespace
  stripped.
- ``msi_score`` (float) : numeric score when present in the input. Parsed from
  ``MSI_SCORE`` or ``MSI_SENSOR_SCORE`` (preferring ``MSI_SCORE``).

Both columns are always present in the output — NaN-filled when no source column
exists in the input. Unrecognized string values in the MSI text column normalize
to NaN (not the raw string) so downstream consumers see a closed vocabulary.

The canonical target vocabulary ``{"MSI-H", "MSI-L", "MSS", "Indeterminate"}``
matches cBioPortal convention and Campbell 2017 / Bonneville 2017 reporting.
"""


import logging
from typing import Mapping

import pandas as pd


logger = logging.getLogger("msi_normalization")


# Case-insensitive; keys are compared after ``.strip().lower()``.
MSI_TYPE_NORMALIZATION: Mapping[str, str] = {
    "msi-h": "MSI-H",
    "msi": "MSI-H",
    "instable": "MSI-H",
    "unstable": "MSI-H",
    "high": "MSI-H",
    "msi high": "MSI-H",
    "msi-high": "MSI-H",
    "msi-l": "MSI-L",
    "low": "MSI-L",
    "msi low": "MSI-L",
    "msi-low": "MSI-L",
    "mss": "MSS",
    "stable": "MSS",
    "microsatellite stable": "MSS",
    "indeterminate": "Indeterminate",
}


_MSI_TEXT_CANDIDATE_COLUMNS = ("MSI_TYPE", "MSI_STATUS")
_MSI_SCORE_CANDIDATE_COLUMNS = ("MSI_SCORE", "MSI_SENSOR_SCORE")


def normalize_msi_columns(sample_df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of ``sample_df`` with normalized ``msi_type`` / ``msi_score``
    columns appended (or NaN-filled if none of the source columns are present).
    """
    out = sample_df.copy()
    out["msi_type"] = _extract_msi_type(sample_df)
    out["msi_score"] = _extract_msi_score(sample_df)
    return out


def _extract_msi_type(df: pd.DataFrame) -> pd.Series:
    source_column = next(
        (col for col in _MSI_TEXT_CANDIDATE_COLUMNS if col in df.columns), None
    )
    if source_column is None:
        return pd.Series([pd.NA] * len(df), index=df.index, dtype="string")
    raw: pd.Series = df[source_column].astype("string")
    normalized: pd.Series = raw.map(_normalize_msi_value_cell).astype("string")
    n_unrecognized = int(
        (raw.notna() & raw.str.strip().str.len().gt(0) & normalized.isna()).sum()
    )
    if n_unrecognized > 0:
        logger.warning(
            "msi_normalization: %d value(s) in column %r did not match the "
            "canonical vocabulary and were set to NaN.",
            n_unrecognized,
            source_column,
        )
    return normalized


def _normalize_msi_value_cell(value: object) -> object:
    if pd.isna(value):
        return pd.NA
    key = str(value).strip().lower()
    if not key:
        return pd.NA
    return MSI_TYPE_NORMALIZATION.get(key, pd.NA)


def _extract_msi_score(df: pd.DataFrame) -> pd.Series:
    source_column = next(
        (col for col in _MSI_SCORE_CANDIDATE_COLUMNS if col in df.columns), None
    )
    if source_column is None:
        return pd.Series([float("nan")] * len(df), index=df.index, dtype=float)
    coerced = pd.to_numeric(df[source_column], errors="coerce")
    return pd.Series(coerced, index=df.index, dtype=float)


def log_msi_type_counts(df: pd.DataFrame, study_id: str) -> None:
    """Emit per-study diagnostic counts of ``msi_type`` values to the log.

    Called from the snakemake wrapper in ``convert_to_feather.py`` as a
    run-time sanity check per plan task 4 requirement.
    """
    if "msi_type" not in df.columns:
        return
    counts = df["msi_type"].value_counts(dropna=False).to_dict()
    logger.info("msi_normalization: study %s msi_type counts: %s", study_id, counts)
