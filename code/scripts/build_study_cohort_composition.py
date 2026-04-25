"""build_study_cohort_composition.

Summary-level rollup of per-study cohort-stage annotations into composition
percentages and dominance classes. One row per study.

Consumes ``samples_stage_annotated.feather`` for each study in ``config['studies']``;
emits a single ``study_cohort_composition.feather`` with the schema documented in
doc/plans/2026-04-24-t052-cohort-stage-descriptor-design.md (v2 §Output schemas).
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

DOMINANCE_THRESHOLD: float = 0.80


def _dominance(
    n_yes: int, n_no: int, n_unk: int, n_total: int, *, yes_label: str, no_label: str
) -> str:
    if n_total == 0:
        return "unknown_dominant"
    if n_unk / n_total >= DOMINANCE_THRESHOLD:
        return "unknown_dominant"
    if n_yes / n_total >= DOMINANCE_THRESHOLD:
        return yes_label
    if n_no / n_total >= DOMINANCE_THRESHOLD:
        return no_label
    return "mixed"


def build_composition(study_id: str, samples_df: pd.DataFrame) -> dict[str, object]:
    """Build a single composition row for one study."""
    n_total = len(samples_df)
    if n_total == 0:
        return {
            "study_id": study_id,
            "n_samples_total": 0,
            "n_metastatic": 0,
            "n_primary": 0,
            "n_metastatic_unknown": 0,
            "pct_metastatic": 0.0,
            "pct_primary": 0.0,
            "pct_metastatic_unknown": 0.0,
            "n_pre_treated": 0,
            "n_naive": 0,
            "n_pre_treated_unknown": 0,
            "pct_pre_treated": 0.0,
            "pct_naive": 0.0,
            "pct_pre_treated_unknown": 0.0,
            "dominant_site_class": "unknown_dominant",
            "dominant_treatment_class": "unknown_dominant",
        }
    is_met = samples_df["is_metastatic"]
    n_met = int((is_met == True).sum())  # noqa: E712  (nullable bool comparison)
    n_pri = int((is_met == False).sum())  # noqa: E712
    n_met_unk = int(is_met.isna().sum())
    is_tx = samples_df["is_pre_treated"]
    n_tx = int((is_tx == True).sum())  # noqa: E712
    n_naive = int((is_tx == False).sum())  # noqa: E712
    n_tx_unk = int(is_tx.isna().sum())
    return {
        "study_id": study_id,
        "n_samples_total": n_total,
        "n_metastatic": n_met,
        "n_primary": n_pri,
        "n_metastatic_unknown": n_met_unk,
        "pct_metastatic": n_met / n_total,
        "pct_primary": n_pri / n_total,
        "pct_metastatic_unknown": n_met_unk / n_total,
        "n_pre_treated": n_tx,
        "n_naive": n_naive,
        "n_pre_treated_unknown": n_tx_unk,
        "pct_pre_treated": n_tx / n_total,
        "pct_naive": n_naive / n_total,
        "pct_pre_treated_unknown": n_tx_unk / n_total,
        "dominant_site_class": _dominance(
            n_met,
            n_pri,
            n_met_unk,
            n_total,
            yes_label="metastatic_dominant",
            no_label="primary_dominant",
        ),
        "dominant_treatment_class": _dominance(
            n_tx,
            n_naive,
            n_tx_unk,
            n_total,
            yes_label="pre_treated_dominant",
            no_label="naive_dominant",
        ),
    }


def build_composition_table(annotated_paths: list[str]) -> pd.DataFrame:
    rows = []
    for p in annotated_paths:
        study_id = Path(p).parent.parent.name
        df = pd.read_feather(p)
        rows.append(build_composition(study_id, df))
    return pd.DataFrame(rows)


if __name__ == "__main__":
    try:
        snek = snakemake  # type: ignore[name-defined]  # noqa: F821
        out_df = build_composition_table([str(p) for p in snek.input])
        Path(snek.output[0]).parent.mkdir(parents=True, exist_ok=True)
        out_df.to_feather(str(snek.output[0]))
    except NameError:
        import argparse

        p_arg = argparse.ArgumentParser(description=__doc__)
        p_arg.add_argument("--inputs", nargs="+", required=True)
        p_arg.add_argument("--output", required=True)
        args = p_arg.parse_args()
        out_df = build_composition_table(args.inputs)
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        out_df.to_feather(args.output)
