# science:code
# status: library
# science:end
from __future__ import annotations

import pandas as pd

from validate_dndscv_external import extract_reference_sets


def test_extract_reference_sets_expands_cdkn2a_isoforms_to_bare_driver_symbol() -> None:
    annotated = pd.DataFrame(
        {
            "symbol": ["CDKN2A", "TP53", "CDKN2AIP"],
            "bailey2018_driver": [True, True, False],
            "cgc_tier_1": [True, True, False],
            "cgc_tier_2": [False, False, False],
        }
    )

    refs = extract_reference_sets(
        annotated,
        universe={"CDKN2A.p16INK4a", "CDKN2A.p14arf", "CDKN2AIP", "TP53"},
    )

    assert refs["bailey2018"] == {"CDKN2A.p16INK4a", "CDKN2A.p14arf", "TP53"}
    assert refs["cgc_tier1"] == {"CDKN2A.p16INK4a", "CDKN2A.p14arf", "TP53"}
    assert refs["cgc_tier1_or_2"] == {"CDKN2A.p16INK4a", "CDKN2A.p14arf", "TP53"}
