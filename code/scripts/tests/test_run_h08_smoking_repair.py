# science:code
# status: workflow-owned
# science:end

import math
import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1]))

from run_h08_smoking_repair import (  # noqa: E402
    PRIMARY_MIN_N,
    RepairCell,
    apply_bh,
    repair_verdict,
    replace_ranked_covariate,
)


def test_replace_ranked_covariate_swaps_original_smoking_slot_once() -> None:
    ranked = ["age", "pack_years", "tmb_nonsynonymous"]

    repaired = replace_ranked_covariate(
        ranked, original="pack_years", replacement="ever_smoker"
    )

    assert repaired == ["age", "ever_smoker", "tmb_nonsynonymous"]


def test_replace_ranked_covariate_fails_if_replacement_already_present() -> None:
    ranked = ["age", "pack_years", "ever_smoker"]

    try:
        replace_ranked_covariate(
            ranked, original="pack_years", replacement="ever_smoker"
        )
    except ValueError as exc:
        assert "already contains replacement" in str(exc)
    else:
        raise AssertionError("expected replacement collision to fail")


def test_apply_bh_uses_monotone_bh_adjustment() -> None:
    grid = pd.DataFrame(
        {
            "covariate": ["a", "b", "c"],
            "pvalue": [0.01, 0.04, 0.03],
        }
    )

    out = apply_bh(grid)

    q_by_covariate = dict(zip(out["covariate"], out["q_bh"], strict=True))
    assert math.isclose(q_by_covariate["a"], 0.03)
    assert math.isclose(q_by_covariate["b"], 0.04)
    assert math.isclose(q_by_covariate["c"], 0.04)


def test_repair_verdict_requires_direction_q_rank_and_n_floor() -> None:
    passing = RepairCell(n=PRIMARY_MIN_N, coef_std=0.2, q_bh=0.01, rank=2)

    assert repair_verdict(passing) == "+"
    assert (
        repair_verdict(RepairCell(n=PRIMARY_MIN_N - 1, coef_std=0.2, q_bh=0.01, rank=2))
        == "?"
    )
    assert (
        repair_verdict(RepairCell(n=PRIMARY_MIN_N, coef_std=0.2, q_bh=0.20, rank=2))
        == "?"
    )
    assert (
        repair_verdict(RepairCell(n=PRIMARY_MIN_N, coef_std=0.2, q_bh=0.01, rank=4))
        == "?"
    )
    assert (
        repair_verdict(RepairCell(n=PRIMARY_MIN_N, coef_std=-0.2, q_bh=0.01, rank=2))
        == "-"
    )
