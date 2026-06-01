# science:code
# status: library
# science:end
"""Tests for q027 therapy-signature-high sample labels."""

from __future__ import annotations

import pandas as pd

from annotate_q027_signature_high import annotate_q027_signature_high


def _assignments() -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for sample_id, sbs11, sbs1, passes in [
        ("HIGH", 60.0, 40.0, True),
        ("LOW", 30.0, 270.0, True),
        ("FRACTION", 5.0, 35.0, True),
        ("UNEVAL", 80.0, 0.0, False),
    ]:
        for signature, exposure in [("SBS11", sbs11), ("SBS1", sbs1)]:
            rows.append(
                {
                    "study_id": "difg_glass_2019",
                    "cancer_type": "Glioma",
                    "sample_name": sample_id,
                    "signature": signature,
                    "exposure": exposure,
                    "total_sbs_count": sbs11 + sbs1,
                    "count_floor": 383,
                    "passes_count_floor": passes,
                }
            )
    return pd.DataFrame(rows)


def test_annotate_q027_signature_high_labels_primary_and_sensitivities() -> None:
    out = annotate_q027_signature_high(
        _assignments(),
        target_signatures_by_study={"difg_glass_2019": ("SBS11",)},
    ).set_index("sample_id")

    assert bool(out.loc["HIGH", "therapy_signature_high"]) is True
    assert out.loc["HIGH", "therapy_signature_label_reason"] == "primary_exposure_ge_50"
    assert out.loc["HIGH", "therapy_signature_exposure"] == 60.0
    assert out.loc["HIGH", "SBS11_exposure"] == 60.0
    assert out.loc["HIGH", "SBS31_exposure"] == 0.0

    assert bool(out.loc["LOW", "therapy_signature_high"]) is False
    assert bool(out.loc["LOW", "therapy_signature_high_sensitivity_20"]) is True
    assert out.loc["LOW", "therapy_signature_label_reason"] == "below_primary_threshold"

    assert (
        bool(out.loc["FRACTION", "therapy_signature_high_sensitivity_fraction_10"])
        is True
    )
    assert bool(out.loc["FRACTION", "therapy_signature_high_sensitivity_any"]) is True


def test_annotate_q027_signature_high_keeps_below_floor_samples_unevaluable() -> None:
    out = annotate_q027_signature_high(
        _assignments(),
        target_signatures_by_study={"difg_glass_2019": ("SBS11",)},
    ).set_index("sample_id")

    assert bool(out.loc["UNEVAL", "passes_count_floor"]) is False
    assert bool(out.loc["UNEVAL", "therapy_signature_high"]) is False
    assert bool(out.loc["UNEVAL", "therapy_signature_unevaluable"]) is True
    assert (
        out.loc["UNEVAL", "therapy_signature_label_reason"]
        == "unevaluable_below_count_floor"
    )
