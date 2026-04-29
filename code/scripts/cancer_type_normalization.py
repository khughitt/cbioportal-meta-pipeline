"""Cancer-type label normalization for convert_to_feather.py.

Implements t083: deterministic whitespace/case cleanup plus optional config-driven
alias maps for cancer labels.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
import re

import pandas as pd

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
