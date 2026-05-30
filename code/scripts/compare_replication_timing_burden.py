# science:code
# status: workflow-owned
# science:end
"""
compare_replication_timing_burden.py

Compare per-sample mutation burden in constitutive early (`CE`) vs constitutive late (`CL`)
replication-timing genes across matched-normal and unmatched-normal study pairs.
"""

import math
import re
from pathlib import Path

import pandas as pd
from scipy.stats import mannwhitneyu

PRIMARY_CHROMOSOME_PATTERN = re.compile(r"^(?:[1-9]|1[0-9]|2[0-2]|X|Y)$")

PER_SAMPLE_COLUMNS = [
    "study_id",
    "lookup_key",
    "sample_name",
    "CE",
    "CL",
    "cl_ce_ratio",
    "log10_cl_ce_ratio",
]

COMPARISON_COLUMNS = [
    "lookup_key",
    "matched_study_id",
    "unmatched_study_id",
    "matched_n_samples",
    "unmatched_n_samples",
    "matched_median_ce",
    "unmatched_median_ce",
    "matched_median_cl",
    "unmatched_median_cl",
    "matched_median_log10_cl_ce_ratio",
    "unmatched_median_log10_cl_ce_ratio",
    "median_ce_shift",
    "median_cl_shift",
    "median_log10_cl_ce_ratio_shift",
    "observed_ce_direction",
    "observed_cl_direction",
    "observed_log10_cl_ce_ratio_direction",
    "unmatched_gt_matched_cl_pvalue",
    "unmatched_gt_matched_log10_cl_ce_ratio_pvalue",
    "cl_two_sided_pvalue",
    "log10_cl_ce_ratio_two_sided_pvalue",
]


def build_symbol_rt_map(genes: pd.DataFrame) -> pd.DataFrame:
    filtered = genes.loc[
        genes["biotype"].astype(str).eq("protein_coding")
        & genes["chr"].astype(str).str.fullmatch(PRIMARY_CHROMOSOME_PATTERN)
    ].copy()

    grouped = (
        filtered.groupby("symbol", as_index=False)[["rt_ce_bp", "rt_cl_bp"]]
        .sum()
        .sort_values("symbol")
        .reset_index(drop=True)
    )

    def _label(row: pd.Series) -> str:
        ce_bp = int(row["rt_ce_bp"])
        cl_bp = int(row["rt_cl_bp"])
        if ce_bp == 0 and cl_bp == 0:
            return "unassigned"
        if ce_bp > cl_bp:
            return "CE"
        if cl_bp > ce_bp:
            return "CL"
        return "mixed"

    grouped["rt_constitutive_label"] = grouped.apply(_label, axis=1)
    return grouped[["symbol", "rt_ce_bp", "rt_cl_bp", "rt_constitutive_label"]]


def build_sample_rt_burden_table(
    *,
    study_id: str,
    mutations: pd.DataFrame,
    assignments: pd.DataFrame,
    symbol_rt: pd.DataFrame,
    ratio_pseudocount: float,
) -> pd.DataFrame:
    assignment_subset = assignments[["lookup_key", "sample_name"]].drop_duplicates().copy()
    labeled_mutations = mutations.merge(
        assignment_subset,
        left_on="sample_id_tumor",
        right_on="sample_name",
        how="inner",
    ).merge(
        symbol_rt[["symbol", "rt_constitutive_label"]],
        on="symbol",
        how="left",
    )
    labeled_mutations = labeled_mutations.loc[labeled_mutations["rt_constitutive_label"].isin(["CE", "CL"])].copy()

    if labeled_mutations.empty:
        return pd.DataFrame(columns=PER_SAMPLE_COLUMNS)

    counts = (
        labeled_mutations.groupby(["lookup_key", "sample_name", "rt_constitutive_label"])
        .size()
        .rename("n_mutations")
        .reset_index()
    )
    wide = (
        counts.pivot_table(
            index=["lookup_key", "sample_name"],
            columns="rt_constitutive_label",
            values="n_mutations",
            aggfunc="sum",
            fill_value=0,
        )
        .reset_index()
    )
    for col in ("CE", "CL"):
        if col not in wide.columns:
            wide[col] = 0

    wide["study_id"] = study_id
    wide["cl_ce_ratio"] = (wide["CL"] + ratio_pseudocount) / (wide["CE"] + ratio_pseudocount)
    wide["log10_cl_ce_ratio"] = wide["cl_ce_ratio"].map(math.log10)
    return wide[PER_SAMPLE_COLUMNS].sort_values(["lookup_key", "sample_name"]).reset_index(drop=True)


def load_assignment_inputs(
    study_inputs: list[dict[str, str | Path]],
    *,
    symbol_rt: pd.DataFrame,
    ratio_pseudocount: float,
) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for item in study_inputs:
        frame = build_sample_rt_burden_table(
            study_id=str(item["study_id"]),
            mutations=pd.read_feather(Path(item["mutations"])),
            assignments=pd.read_feather(Path(item["assignments"])),
            symbol_rt=symbol_rt,
            ratio_pseudocount=ratio_pseudocount,
        )
        if not frame.empty:
            frames.append(frame)

    if not frames:
        return pd.DataFrame(columns=PER_SAMPLE_COLUMNS)
    return pd.concat(frames, ignore_index=True)


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
) -> pd.DataFrame:
    sample_table = per_sample.copy()
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

                median_ce_shift = float(unmatched_study_df["CE"].median() - matched_study_df["CE"].median())
                median_cl_shift = float(unmatched_study_df["CL"].median() - matched_study_df["CL"].median())
                median_ratio_shift = float(
                    unmatched_study_df["log10_cl_ce_ratio"].median() - matched_study_df["log10_cl_ce_ratio"].median()
                )
                cl_greater_pvalue, cl_two_sided_pvalue = mann_whitney_pvalues(
                    unmatched_study_df["CL"],
                    matched_study_df["CL"],
                )
                ratio_greater_pvalue, ratio_two_sided_pvalue = mann_whitney_pvalues(
                    unmatched_study_df["log10_cl_ce_ratio"],
                    matched_study_df["log10_cl_ce_ratio"],
                )
                rows.append(
                    {
                        "lookup_key": lookup_key,
                        "matched_study_id": matched_study_id,
                        "unmatched_study_id": unmatched_study_id,
                        "matched_n_samples": int(len(matched_study_df)),
                        "unmatched_n_samples": int(len(unmatched_study_df)),
                        "matched_median_ce": float(matched_study_df["CE"].median()),
                        "unmatched_median_ce": float(unmatched_study_df["CE"].median()),
                        "matched_median_cl": float(matched_study_df["CL"].median()),
                        "unmatched_median_cl": float(unmatched_study_df["CL"].median()),
                        "matched_median_log10_cl_ce_ratio": float(matched_study_df["log10_cl_ce_ratio"].median()),
                        "unmatched_median_log10_cl_ce_ratio": float(
                            unmatched_study_df["log10_cl_ce_ratio"].median()
                        ),
                        "median_ce_shift": median_ce_shift,
                        "median_cl_shift": median_cl_shift,
                        "median_log10_cl_ce_ratio_shift": median_ratio_shift,
                        "observed_ce_direction": direction_from_shift(median_ce_shift),
                        "observed_cl_direction": direction_from_shift(median_cl_shift),
                        "observed_log10_cl_ce_ratio_direction": direction_from_shift(median_ratio_shift),
                        "unmatched_gt_matched_cl_pvalue": cl_greater_pvalue,
                        "unmatched_gt_matched_log10_cl_ce_ratio_pvalue": ratio_greater_pvalue,
                        "cl_two_sided_pvalue": cl_two_sided_pvalue,
                        "log10_cl_ce_ratio_two_sided_pvalue": ratio_two_sided_pvalue,
                    }
                )

    if not rows:
        return pd.DataFrame(columns=COMPARISON_COLUMNS)

    return pd.DataFrame(rows, columns=COMPARISON_COLUMNS).sort_values(
        ["lookup_key", "matched_study_id", "unmatched_study_id"]
    ).reset_index(drop=True)


def main() -> None:
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821
    gene_rt = pd.read_feather(snek.input.gene_rt)
    symbol_rt = build_symbol_rt_map(gene_rt)

    study_inputs = [
        {
            "study_id": study_id,
            "mutations": mutation_path,
            "assignments": assignment_path,
        }
        for study_id, mutation_path, assignment_path in zip(
            list(snek.params.ids),
            list(snek.input.mutations),
            list(snek.input.assignments),
            strict=True,
        )
    ]

    ratio_pseudocount = float(snek.config.get("signature_ratio_pseudocount", 0.5))
    per_sample = load_assignment_inputs(
        study_inputs,
        symbol_rt=symbol_rt,
        ratio_pseudocount=ratio_pseudocount,
    )
    comparison = build_comparison_table(
        per_sample,
        matched_normal_studies=set(snek.config.get("matched_normal_studies", [])),
        min_samples_per_group=int(snek.config.get("signature_ratio_min_samples_per_group", 25)),
    )

    per_sample.to_feather(snek.output.per_sample)
    comparison.to_feather(snek.output.summary)


if __name__ == "__main__":
    main()
