# science:code
# status: workflow-owned
# science:end
"""
compare_sbs1_sbs5_ratio.py

Summarize matched-vs-unmatched SBS1/SBS5 shifts from per-sample restricted
signature-assignment outputs.
"""

import math
from pathlib import Path

import pandas as pd
from scipy.stats import mannwhitneyu

COMPARISON_COLUMNS = [
    "lookup_key",
    "matched_study_id",
    "unmatched_study_id",
    "matched_n_samples",
    "unmatched_n_samples",
    "matched_median_sbs1",
    "unmatched_median_sbs1",
    "matched_median_sbs5",
    "unmatched_median_sbs5",
    "matched_median_log10_ratio",
    "unmatched_median_log10_ratio",
    "median_sbs1_shift",
    "median_log10_ratio_shift",
    "observed_sbs1_direction",
    "observed_log10_ratio_direction",
    "unmatched_gt_matched_sbs1_pvalue",
    "unmatched_gt_matched_log10_ratio_pvalue",
    "sbs1_two_sided_pvalue",
    "log10_ratio_two_sided_pvalue",
]


def load_per_sample_assignments(paths: list[Path]) -> pd.DataFrame:
    frames = [pd.read_feather(path) for path in paths]
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def build_sample_ratio_table(per_sample: pd.DataFrame, *, ratio_pseudocount: float) -> pd.DataFrame:
    needed = per_sample.loc[per_sample["signature"].isin(["SBS1", "SBS5"])].copy()
    wide = (
        needed.pivot_table(
            index=["study_id", "cancer_type", "lookup_key", "sample_name"],
            columns="signature",
            values="exposure",
            aggfunc="sum",
            fill_value=0.0,
        )
        .reset_index()
    )
    for col in ("SBS1", "SBS5"):
        if col not in wide.columns:
            wide[col] = 0.0
    wide["sbs1_sbs5_ratio"] = (wide["SBS1"] + ratio_pseudocount) / (wide["SBS5"] + ratio_pseudocount)
    wide["log10_sbs1_sbs5_ratio"] = wide["sbs1_sbs5_ratio"].map(math.log10)
    return wide


def direction_from_shift(shift: float) -> str:
    if shift > 0:
        return "unmatched_higher"
    if shift < 0:
        return "matched_higher"
    return "tie"


def mann_whitney_pvalues(unmatched: pd.Series, matched: pd.Series) -> tuple[float, float]:
    greater = mannwhitneyu(unmatched, matched, alternative="greater", method="asymptotic")
    two_sided = mannwhitneyu(unmatched, matched, alternative="two-sided", method="asymptotic")
    return float(greater.pvalue), float(two_sided.pvalue)


def build_comparison_table(
    per_sample: pd.DataFrame,
    *,
    matched_normal_studies: set[str],
    min_samples_per_group: int,
    ratio_pseudocount: float,
) -> pd.DataFrame:
    sample_table = build_sample_ratio_table(per_sample, ratio_pseudocount=ratio_pseudocount)
    sample_table["normal_status"] = sample_table["study_id"].map(
        lambda study_id: "matched" if study_id in matched_normal_studies else "unmatched"
    )

    rows: list[dict[str, object]] = []
    for lookup_key, lookup_df in sample_table.groupby("lookup_key", sort=True):
        matched_df = lookup_df.loc[lookup_df["normal_status"] == "matched"]
        unmatched_df = lookup_df.loc[lookup_df["normal_status"] == "unmatched"]
        if matched_df.empty or unmatched_df.empty:
            continue

        for matched_study_id, matched_study_df in matched_df.groupby("study_id", sort=True):
            for unmatched_study_id, unmatched_study_df in unmatched_df.groupby("study_id", sort=True):
                if len(matched_study_df) < min_samples_per_group or len(unmatched_study_df) < min_samples_per_group:
                    continue
                median_sbs1_shift = float(unmatched_study_df["SBS1"].median() - matched_study_df["SBS1"].median())
                median_log10_ratio_shift = float(
                    unmatched_study_df["log10_sbs1_sbs5_ratio"].median()
                    - matched_study_df["log10_sbs1_sbs5_ratio"].median()
                )
                sbs1_greater_pvalue, sbs1_two_sided_pvalue = mann_whitney_pvalues(
                    unmatched_study_df["SBS1"],
                    matched_study_df["SBS1"],
                )
                log10_ratio_greater_pvalue, log10_ratio_two_sided_pvalue = mann_whitney_pvalues(
                    unmatched_study_df["log10_sbs1_sbs5_ratio"],
                    matched_study_df["log10_sbs1_sbs5_ratio"],
                )
                rows.append(
                    {
                        "lookup_key": lookup_key,
                        "matched_study_id": matched_study_id,
                        "unmatched_study_id": unmatched_study_id,
                        "matched_n_samples": int(len(matched_study_df)),
                        "unmatched_n_samples": int(len(unmatched_study_df)),
                        "matched_median_sbs1": float(matched_study_df["SBS1"].median()),
                        "unmatched_median_sbs1": float(unmatched_study_df["SBS1"].median()),
                        "matched_median_sbs5": float(matched_study_df["SBS5"].median()),
                        "unmatched_median_sbs5": float(unmatched_study_df["SBS5"].median()),
                        "matched_median_log10_ratio": float(matched_study_df["log10_sbs1_sbs5_ratio"].median()),
                        "unmatched_median_log10_ratio": float(unmatched_study_df["log10_sbs1_sbs5_ratio"].median()),
                        "median_sbs1_shift": median_sbs1_shift,
                        "median_log10_ratio_shift": median_log10_ratio_shift,
                        "observed_sbs1_direction": direction_from_shift(median_sbs1_shift),
                        "observed_log10_ratio_direction": direction_from_shift(median_log10_ratio_shift),
                        "unmatched_gt_matched_sbs1_pvalue": sbs1_greater_pvalue,
                        "unmatched_gt_matched_log10_ratio_pvalue": log10_ratio_greater_pvalue,
                        "sbs1_two_sided_pvalue": sbs1_two_sided_pvalue,
                        "log10_ratio_two_sided_pvalue": log10_ratio_two_sided_pvalue,
                    }
                )

    if not rows:
        return pd.DataFrame(columns=COMPARISON_COLUMNS)

    return pd.DataFrame(rows, columns=COMPARISON_COLUMNS).sort_values(
        ["lookup_key", "matched_study_id", "unmatched_study_id"]
    ).reset_index(drop=True)


def main() -> None:
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821
    per_sample = load_per_sample_assignments([Path(p) for p in snek.input])
    matched_normal_studies = set(snek.config.get("matched_normal_studies", []))
    min_samples_per_group = int(snek.config.get("signature_ratio_min_samples_per_group", 25))
    ratio_pseudocount = float(snek.config.get("signature_ratio_pseudocount", 0.5))

    comparison = build_comparison_table(
        per_sample,
        matched_normal_studies=matched_normal_studies,
        min_samples_per_group=min_samples_per_group,
        ratio_pseudocount=ratio_pseudocount,
    )
    comparison.to_feather(snek.output[0])


if __name__ == "__main__":
    main()
