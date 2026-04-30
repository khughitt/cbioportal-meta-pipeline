from __future__ import annotations

from symbol_normalization import (
    driver_overlay_symbol,
    expand_reference_symbols_to_universe,
)


def test_driver_overlay_symbol_strips_dndscv_isoform_suffix() -> None:
    assert driver_overlay_symbol("CDKN2A.p16INK4a") == "CDKN2A"
    assert driver_overlay_symbol("CDKN2A.p14arf") == "CDKN2A"
    assert driver_overlay_symbol("TP53") == "TP53"


def test_expand_reference_symbols_to_universe_keeps_raw_universe_symbols() -> None:
    out = expand_reference_symbols_to_universe(
        reference_symbols={"CDKN2A", "TP53"},
        universe={"CDKN2A.p16INK4a", "CDKN2A.p14arf", "CDKN2AIP", "TP53"},
    )

    assert out == {"CDKN2A.p16INK4a", "CDKN2A.p14arf", "TP53"}
