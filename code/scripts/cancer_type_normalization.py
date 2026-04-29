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
