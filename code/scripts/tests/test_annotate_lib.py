# science:code
# status: library
# science:end
"""Tests for the overlay-annotation library (annotate_lib).

Regression coverage for t106: the ``*_source`` provenance columns must carry a stable
version stamp sourced from each reference feather's own ``source`` column — never the
per-run output path that the Snakemake rule happens to write to.
"""

from __future__ import annotations

import pandas as pd
import pytest

from annotate_lib import apply_overlays, source_stamp


def _freq() -> pd.DataFrame:
    return pd.DataFrame({"symbol": ["TP53", "KRAS"], "cancer_type": ["BRCA", "LUAD"]})


def _bailey() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "gene": ["TP53", "KRAS"],
            "cancer_type": ["BRCA", "PANCAN"],
            "source": ["Bailey2018", "Bailey2018"],
        }
    )


def _cgc() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "gene": ["TP53"],
            "tier": [1],
            "role_in_cancer": ["TSG"],
            "source": ["COSMIC-CGC"],
        }
    )


def _pathways() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "gene": ["TP53"],
            "pathway": ["TP53"],
            "og_tsg": ["TSG"],
            "source": ["SanchezVega2018"],
        }
    )


def test_source_columns_carry_producer_stamp_not_path() -> None:
    out = apply_overlays(_freq(), _bailey(), _cgc(), _pathways())

    assert out["bailey2018_source"].unique().tolist() == ["Bailey2018"]
    assert out["cgc_source"].unique().tolist() == ["COSMIC-CGC"]
    assert out["sanchez_vega_source"].unique().tolist() == ["SanchezVega2018"]


def test_source_columns_never_leak_filesystem_paths() -> None:
    # The t106 bug: bailey2018_source held 'results/poc-2026-04-17/metadata/...feather'.
    out = apply_overlays(_freq(), _bailey(), _cgc(), _pathways())

    for col in ("bailey2018_source", "cgc_source", "sanchez_vega_source"):
        for value in out[col].astype(str):
            assert "/" not in value, f"{col} leaks a path: {value!r}"
            assert not value.endswith(".feather"), f"{col} leaks a filename: {value!r}"


def test_existing_overlay_behaviour_is_preserved() -> None:
    out = apply_overlays(_freq(), _bailey(), _cgc(), _pathways())

    # TP53/BRCA is an explicit Bailey pair; KRAS is a PANCAN driver.
    assert out.loc[out["symbol"] == "TP53", "bailey2018_driver"].iloc[0]
    assert out.loc[out["symbol"] == "KRAS", "bailey2018_driver"].iloc[0]
    assert out.loc[out["symbol"] == "TP53", "cgc_tier_1"].iloc[0]
    assert out.loc[out["symbol"] == "TP53", "sanchez_vega_pathway"].iloc[0] == "TP53"


def test_source_stamp_raises_when_source_column_missing() -> None:
    with pytest.raises(ValueError, match="source"):
        source_stamp(pd.DataFrame({"gene": ["TP53"]}), "bailey")


def test_source_stamp_raises_on_ambiguous_source() -> None:
    with pytest.raises(ValueError, match="exactly one"):
        source_stamp(pd.DataFrame({"source": ["Bailey2018", "Bailey2017"]}), "bailey")
