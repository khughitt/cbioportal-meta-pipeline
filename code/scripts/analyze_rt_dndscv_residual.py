# science:code
# status: exploratory
# science:end
"""Replication-timing residual analysis for pan-cancer dNdScv rankings.

Task t163 tests whether gene-level constitutive late-replication overlap explains
residual dNdScv signal after the t144/t145 ranking fixes.
"""

from __future__ import annotations

import math
from pathlib import Path

import click
import numpy as np
import pandas as pd

MODEL_COLUMNS = ["rt_late_score", "log_length"]


def build_rt_dndscv_table(
    dndscv: pd.DataFrame, rt: pd.DataFrame, *, q_floor: float
) -> pd.DataFrame:
    """Join per-gene dNdScv rankings with gene-level RT annotations."""
    required_dndscv = {
        "symbol",
        "min_qglobal",
        "n_cancers_significant_q05",
        "rank_dndscv",
        "length",
    }
    missing_dndscv = required_dndscv - set(dndscv.columns)
    if missing_dndscv:
        raise ValueError(f"dndscv missing required columns: {sorted(missing_dndscv)}")
    required_rt = {
        "symbol",
        "rt_constitutive_label",
        "rt_ce_fraction",
        "rt_cl_fraction",
    }
    missing_rt = required_rt - set(rt.columns)
    if missing_rt:
        raise ValueError(f"rt missing required columns: {sorted(missing_rt)}")

    rt_one = rt[list(required_rt)].drop_duplicates("symbol").copy()
    out = dndscv.merge(rt_one, on="symbol", how="inner").copy()
    out["min_qglobal_floored"] = out["min_qglobal"].fillna(1.0).clip(lower=q_floor)
    out["dndscv_signal"] = -np.log10(out["min_qglobal_floored"].astype(float))
    out["rt_ce_fraction"] = out["rt_ce_fraction"].fillna(0.0).astype(float)
    out["rt_cl_fraction"] = out["rt_cl_fraction"].fillna(0.0).astype(float)
    out["rt_late_score"] = out["rt_cl_fraction"] - out["rt_ce_fraction"]
    out["log_length"] = (
        out["length"]
        .astype(float)
        .apply(lambda value: math.log10(value) if value > 0 else float("nan"))
    )
    return out.reset_index(drop=True)


def fit_rt_model(table: pd.DataFrame) -> dict[str, float | int]:
    """Fit dNdScv signal against RT score, length, and significance breadth."""
    required = {"dndscv_signal", *MODEL_COLUMNS}
    missing = required - set(table.columns)
    if missing:
        raise ValueError(f"table missing required columns: {sorted(missing)}")
    fit = table.dropna(subset=["dndscv_signal", *MODEL_COLUMNS]).copy()
    if len(fit) < 2:
        return {
            "n_genes": int(len(fit)),
            "intercept": float("nan"),
            "beta_rt_late_score": float("nan"),
            "beta_log_length": float("nan"),
            "r2": float("nan"),
        }
    x = np.column_stack(
        [
            np.ones(len(fit), dtype=float),
            fit["rt_late_score"].to_numpy(dtype=float),
            fit["log_length"].to_numpy(dtype=float),
        ]
    )
    y = fit["dndscv_signal"].to_numpy(dtype=float)
    beta, *_ = np.linalg.lstsq(x, y, rcond=None)
    pred = x @ beta
    ss_res = float(((y - pred) ** 2).sum())
    ss_tot = float(((y - y.mean()) ** 2).sum())
    return {
        "n_genes": int(len(fit)),
        "intercept": float(beta[0]),
        "beta_rt_late_score": float(beta[1]),
        "beta_log_length": float(beta[2]),
        "r2": 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan"),
    }


def bootstrap_rt_effect(
    table: pd.DataFrame, *, n_boot: int, seed: int
) -> dict[str, float | int]:
    """Bootstrap the late-RT coefficient using row resampling."""
    rng = np.random.default_rng(seed)
    fit = table.dropna(subset=["dndscv_signal", *MODEL_COLUMNS]).reset_index(drop=True)
    if fit.empty:
        return {
            "n_boot": 0,
            "beta_rt_late_score_mean": float("nan"),
            "beta_rt_late_score_ci_low": float("nan"),
            "beta_rt_late_score_ci_high": float("nan"),
        }
    betas: list[float] = []
    for _ in range(n_boot):
        idx = rng.integers(0, len(fit), size=len(fit))
        sample = fit.iloc[idx]
        betas.append(float(fit_rt_model(sample)["beta_rt_late_score"]))
    beta_arr = np.asarray(betas, dtype=float)
    return {
        "n_boot": int(n_boot),
        "beta_rt_late_score_mean": float(np.nanmean(beta_arr)),
        "beta_rt_late_score_ci_low": float(np.nanquantile(beta_arr, 0.025)),
        "beta_rt_late_score_ci_high": float(np.nanquantile(beta_arr, 0.975)),
    }


def add_rt_adjusted_signal(
    table: pd.DataFrame, model: dict[str, float | int]
) -> pd.DataFrame:
    """Subtract fitted RT/length/breadth component and rank residual signal."""
    out = table.copy()
    fitted = (
        float(model["intercept"])
        + float(model["beta_rt_late_score"]) * out["rt_late_score"].astype(float)
        + float(model["beta_log_length"]) * out["log_length"].astype(float)
    )
    out["rt_adjusted_signal"] = out["dndscv_signal"].astype(float) - fitted
    out = out.sort_values(
        ["rt_adjusted_signal", "n_cancers_significant_q05", "symbol"],
        ascending=[False, False, True],
        kind="mergesort",
    ).reset_index(drop=True)
    out["rt_adjusted_rank"] = np.arange(1, len(out) + 1)
    return out


def build_ttn_rank_check(table: pd.DataFrame) -> pd.DataFrame:
    """Return TTN's raw and RT-adjusted rank row for interpretation."""
    if "TTN" not in set(table["symbol"]):
        return pd.DataFrame(
            columns=[
                "symbol",
                "rank_dndscv",
                "rt_adjusted_rank",
                "dndscv_signal",
                "rt_adjusted_signal",
                "rt_late_score",
                "rt_constitutive_label",
            ]
        )
    cols = [
        "symbol",
        "rank_dndscv",
        "rt_adjusted_rank",
        "dndscv_signal",
        "rt_adjusted_signal",
        "rt_late_score",
        "rt_constitutive_label",
        "min_qglobal",
        "n_cancers_significant_q05",
    ]
    return table.loc[
        table["symbol"] == "TTN", [col for col in cols if col in table.columns]
    ].reset_index(drop=True)


@click.command()
@click.option("--dndscv", "dndscv_path", type=Path, required=True)
@click.option("--rt", "rt_path", type=Path, required=True)
@click.option("--out-dir", "out_dir", type=Path, required=True)
@click.option("--q-floor", type=float, default=1e-300, show_default=True)
@click.option("--n-boot", type=int, default=1000, show_default=True)
@click.option("--seed", type=int, default=0, show_default=True)
def main(
    dndscv_path: Path,
    rt_path: Path,
    out_dir: Path,
    q_floor: float,
    n_boot: int,
    seed: int,
) -> None:
    """Run the t163 RT residual regression analysis."""
    dndscv = pd.read_feather(dndscv_path)
    rt = pd.read_feather(rt_path)
    out_dir.mkdir(parents=True, exist_ok=True)

    table = build_rt_dndscv_table(dndscv, rt, q_floor=q_floor)
    model = fit_rt_model(table)
    bootstrap = bootstrap_rt_effect(table, n_boot=n_boot, seed=seed)
    adjusted = add_rt_adjusted_signal(table, model)
    ttn = build_ttn_rank_check(adjusted)

    adjusted.to_feather(out_dir / "rt_dndscv_table.feather")
    pd.DataFrame([model]).to_feather(out_dir / "rt_model_summary.feather")
    pd.DataFrame([bootstrap]).to_feather(out_dir / "rt_bootstrap.feather")
    ttn.to_feather(out_dir / "ttn_rank_check.feather")

    print(f"wrote: {out_dir / 'rt_dndscv_table.feather'}")
    print(f"wrote: {out_dir / 'rt_model_summary.feather'}")
    print(f"wrote: {out_dir / 'rt_bootstrap.feather'}")
    print(f"wrote: {out_dir / 'ttn_rank_check.feather'}")
    print(f"n_genes: {model['n_genes']}")


if __name__ == "__main__":
    main()
