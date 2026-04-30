"""Gene-symbol normalization helpers for driver-reference overlays."""

from __future__ import annotations

from collections.abc import Iterable


def driver_overlay_symbol(symbol: object) -> str:
    """Return the symbol key used for external driver overlays.

    dNdScv can emit isoform-level CDKN2A labels such as ``CDKN2A.p16INK4a``.
    Bailey/CGC overlays use bare HGNC symbols, so only the suffix after the
    first dot is stripped. Raw symbols remain unchanged in output tables.
    """
    return str(symbol).split(".", maxsplit=1)[0].upper()


def expand_reference_symbols_to_universe(
    reference_symbols: Iterable[object],
    universe: Iterable[object],
) -> set[str]:
    """Return raw universe symbols whose bare overlay key is in a reference set."""
    reference_keys = {driver_overlay_symbol(symbol) for symbol in reference_symbols}
    return {
        str(symbol)
        for symbol in universe
        if driver_overlay_symbol(symbol) in reference_keys
    }
