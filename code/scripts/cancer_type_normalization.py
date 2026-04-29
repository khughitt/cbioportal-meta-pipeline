"""Cancer-type label normalization for convert_to_feather.py.

Implements t083: deterministic whitespace/case cleanup plus optional config-driven
alias maps for cancer labels.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
import logging
import re

import pandas as pd

logger = logging.getLogger("cancer_type_normalization")

_WHITESPACE_RE = re.compile(r"\s+")

type LabelNormalizer = Callable[[object], str | None]


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


_ALIAS_CONFIG_TO_COLUMN: Mapping[str, tuple[str, LabelNormalizer]] = {
    "cancer_type_alias_map": ("cancer_type", normalize_human_label),
    "cancer_type_detailed_alias_map": ("cancer_type_detailed", normalize_human_label),
    "primary_site_alias_map": ("primary_site", normalize_human_label),
    "oncotree_code_alias_map": ("oncotree_code", normalize_code_label),
}

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
            raise ValueError(
                f"Label normalization alias map contains an empty alias value for {key!r}."
            )
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
            raise TypeError(
                f"{config_key} must be a mapping of raw label to canonical label."
            )
        aliases = canonicalize_alias_map(raw_aliases, normalizer=normalizer)
        if aliases:
            out[column] = aliases
    return out


def normalize_sample_labels(
    sample_mdat: pd.DataFrame, alias_maps: Mapping[str, Mapping[str, str]]
) -> tuple[pd.DataFrame, list[LabelNormalizationStats]]:
    """Normalize clinical sample label columns and rebuild target columns as categoricals."""
    out = sample_mdat.copy()
    stats: list[LabelNormalizationStats] = []
    for column in (*_HUMAN_LABEL_COLUMNS, *_CODE_LABEL_COLUMNS):
        if column not in out.columns:
            continue
        normalizer = (
            normalize_code_label if column in _CODE_LABEL_COLUMNS else normalize_human_label
        )
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
