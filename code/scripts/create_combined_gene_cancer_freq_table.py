"""
create_combined_gene_cancer_freq_table.py

Concatenates per-study gene x cancer mutation frequency tables into cross-study
wide-format feathers keyed by (cancer_type, symbol).

As of t098 part B / t081.7b, each per-study input is expected to carry paired
inclusive / exclusive columns (``num_inclusive``, ``num_exclusive``,
``ratio_inclusive``, ``ratio_exclusive``) produced by ``create_freq_tables.py``
once the hypermutator-annotation step (t097) has landed. The combined output
preserves that paired structure: every per-study column exists twice — once as
the legacy backward-compat name ``{study_id}`` (the inclusive view) and once
as ``{study_id}_exclusive`` (the hypermutator-excluded view). Two pooled-mean
columns (``mean_inclusive``, ``mean_exclusive``) are emitted alongside the
legacy ``mean`` / ``mean_adj`` aliases.

Deviation from plan review finding #3 (2026-04-14): the plan specifies
dropping the legacy ``mean`` column entirely to force consumers to pick
``mean_inclusive`` or ``mean_exclusive`` explicitly. We currently keep the
``mean`` / ``mean_adj`` aliases for backward compatibility with downstream
consumers (``annotate.py``, ``annotate_ch.py``, the R summary report) that
have not yet migrated. A follow-up task will drop the aliases once those
consumers are updated.

Outputs:
  - ``gene_cancer_study.feather``       : per-study mutation counts (num) with
                                          paired inclusive/exclusive columns
                                          plus callability metadata.
  - ``gene_cancer_study_ratio.feather`` : per-study mutation ratios with
                                          paired inclusive/exclusive columns,
                                          ``mean_inclusive`` / ``mean_exclusive``
                                          plus legacy ``mean`` / ``mean_adj``
                                          and callability metadata.

Callability annotation columns (closes audit F2 partially; unchanged from the
pre-t098 pass):

  - ``n_total_studies``           : total number of studies in the aggregation.
  - ``n_contributing_studies``    : count of per-study inclusive columns with
                                    a non-null value for this row.
  - ``n_panel_covered_studies``   : number of studies whose panel covers this
                                    gene (GENIE + ``study_panel_map``).
  - ``callable_fraction``         : ``n_panel_covered_studies / n_total_studies``.
  - ``n_panel_covered_samples_inclusive``  : sum across studies of per-(study,
                                    cancer, gene) panel-restricted
                                    inclusive denominators (t070).
  - ``n_panel_covered_samples_exclusive``  : same, restricted to non-hypermutators.
  - ``callable_sample_fraction_inclusive`` : ``n_panel_covered_samples_inclusive
                                    / n_total_samples_in_cancer``.
  - ``callable_sample_fraction_exclusive`` : same, restricted to non-hypermutators.

Config
------
- ``study_panel_map`` (``dict[str, str]``): optional. Studies listed here are
  treated as panel-restricted; studies not in the map are treated as WES.
"""

import os
import sys

import pandas as pd


def _study_id_from_path(infile: str) -> str:
    """Extract the study id from a per-study output path."""
    return os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(infile))))


def combine_paired_pivot(
    per_study_frames: list[tuple[str, pd.DataFrame]],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Pivot per-study paired columns into cross-study wide-format DataFrames.

    Input: list of ``(study_id, frame)`` pairs. Each ``frame`` must have
    ``cancer_type``, ``symbol``, ``num_inclusive``, ``num_exclusive``,
    ``ratio_inclusive``, ``ratio_exclusive``, ``n_samples_inclusive``,
    ``n_samples_exclusive`` columns.

    Returns ``(num_df, ratio_df, n_inclusive_df, n_exclusive_df)``. All four are
    indexed on ``(cancer_type, symbol)`` with one column per study (named by
    ``study_id``). For ``num_df`` and ``ratio_df``, columns appear twice as in
    the legacy contract (``{study_id}`` for inclusive, ``{study_id}_exclusive``
    for exclusive). For ``n_inclusive_df`` and ``n_exclusive_df``, columns
    appear once (study_id only) — they hold the per-study panel-restricted
    denominators that downstream sample-weighted callability metrics consume.
    """
    num_frames: list[pd.DataFrame] = []
    ratio_frames: list[pd.DataFrame] = []
    n_inclusive_frames: list[pd.DataFrame] = []
    n_exclusive_frames: list[pd.DataFrame] = []
    for study_id, frame in per_study_frames:
        if frame.empty:
            continue
        indexed = frame.set_index(["cancer_type", "symbol"])
        num_frames.append(
            pd.DataFrame(
                {
                    study_id: indexed["num_inclusive"],
                    f"{study_id}_exclusive": indexed["num_exclusive"],
                }
            )
        )
        ratio_frames.append(
            pd.DataFrame(
                {
                    study_id: indexed["ratio_inclusive"],
                    f"{study_id}_exclusive": indexed["ratio_exclusive"],
                }
            )
        )
        n_inclusive_frames.append(
            pd.DataFrame({study_id: indexed["n_samples_inclusive"]})
        )
        n_exclusive_frames.append(
            pd.DataFrame({study_id: indexed["n_samples_exclusive"]})
        )

    if not num_frames:
        empty_index = pd.MultiIndex.from_tuples([], names=["cancer_type", "symbol"])
        return (
            pd.DataFrame(index=empty_index),
            pd.DataFrame(index=empty_index),
            pd.DataFrame(index=empty_index),
            pd.DataFrame(index=empty_index),
        )

    num_df = pd.concat(num_frames, axis=1)
    ratio_df = pd.concat(ratio_frames, axis=1)
    n_inclusive_df = pd.concat(n_inclusive_frames, axis=1)
    n_exclusive_df = pd.concat(n_exclusive_frames, axis=1)

    ratio_df = _recompute_mean_columns(ratio_df)

    return num_df, ratio_df, n_inclusive_df, n_exclusive_df


def _recompute_mean_columns(ratio_df: pd.DataFrame) -> pd.DataFrame:
    """Recompute pooled mean columns from paired per-study ratio columns."""
    summary_cols = {"mean", "mean_inclusive", "mean_exclusive", "mean_adj"}
    inclusive_ratio_cols = [
        c
        for c in ratio_df.columns
        if isinstance(c, str)
        and c not in summary_cols
        and f"{c}_exclusive" in ratio_df.columns
    ]
    exclusive_ratio_cols = [f"{c}_exclusive" for c in inclusive_ratio_cols]
    ratio_df["mean_inclusive"] = ratio_df[inclusive_ratio_cols].mean(
        axis=1, skipna=True
    )
    ratio_df["mean_exclusive"] = ratio_df[exclusive_ratio_cols].mean(
        axis=1, skipna=True
    )
    # Legacy alias (deviation from plan review finding #3; see module docstring).
    ratio_df["mean"] = ratio_df["mean_inclusive"]
    return ratio_df


def _load_cancer_presence(
    per_study_cancer_paths: list[str],
) -> dict[str, dict[str, tuple[int, int]]]:
    """Load per-study cancer cohort denominators from cancer_study.feather files.

    Returns ``{study_id: {cancer_type: (n_samples_inclusive, n_samples_exclusive)}}``.
    """
    out: dict[str, dict[str, tuple[int, int]]] = {}
    for infile in per_study_cancer_paths:
        study = _study_id_from_path(infile)
        df = pd.read_feather(infile)
        if df.empty:
            out[study] = {}
            continue
        required = {"cancer_type", "n_samples_inclusive", "n_samples_exclusive"}
        missing = required - set(df.columns)
        if missing:
            raise ValueError(
                f"{infile} missing required cancer-summary columns: {sorted(missing)}"
            )
        out[study] = {
            str(row["cancer_type"]): (
                int(row["n_samples_inclusive"]),
                int(row["n_samples_exclusive"]),
            )
            for _, row in df[
                ["cancer_type", "n_samples_inclusive", "n_samples_exclusive"]
            ].iterrows()
        }
    return out


def _fill_missing_unmutated_cells(
    num_df: pd.DataFrame,
    ratio_df: pd.DataFrame,
    n_inclusive_df: pd.DataFrame,
    n_exclusive_df: pd.DataFrame,
    *,
    cancer_presence_by_study: dict[str, dict[str, tuple[int, int]]],
    study_panel_map: dict[str, str],
    panel_bearing_studies: set[str] | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Backfill WES/unmapped-study missing cells as zero when the cancer exists.

    The panel-aware per-study rule already emits dense callable `(cancer, gene)` rows,
    so missing cells in mapped panel studies remain informative (`gene not callable`
    or `cancer absent`) and must stay `NaN`. The remaining gap is WES / unmapped
    studies: every gene is callable, but unmutated `(cancer, gene)` combinations are
    absent from the per-study feather. For those studies only, fill missing cells with
    zero counts and the cancer-level cohort denominator.
    """
    cancer_index = num_df.index.get_level_values("cancer_type")

    panel_restricted_studies = set(study_panel_map) | (panel_bearing_studies or set())

    for study, cancer_info in cancer_presence_by_study.items():
        if study in panel_restricted_studies:
            continue
        if study not in num_df.columns or study not in n_inclusive_df.columns:
            continue

        exclusive_col = f"{study}_exclusive"
        if exclusive_col not in num_df.columns or exclusive_col not in ratio_df.columns:
            raise ValueError(f"Missing paired exclusive column for study {study!r}")

        for cancer_type, (n_inclusive, n_exclusive) in cancer_info.items():
            cancer_mask = cancer_index == cancer_type
            if not cancer_mask.any():
                continue

            missing_inclusive = num_df[study].isna() & cancer_mask
            missing_exclusive = num_df[exclusive_col].isna() & cancer_mask

            if missing_inclusive.any():
                num_df.loc[missing_inclusive, study] = 0
                ratio_df.loc[missing_inclusive, study] = (
                    0.0 if n_inclusive > 0 else float("nan")
                )
                n_inclusive_df.loc[missing_inclusive, study] = n_inclusive

            if missing_exclusive.any():
                num_df.loc[missing_exclusive, exclusive_col] = 0
                ratio_df.loc[missing_exclusive, exclusive_col] = (
                    0.0 if n_exclusive > 0 else float("nan")
                )
                n_exclusive_df.loc[missing_exclusive, study] = n_exclusive

    ratio_df = _recompute_mean_columns(ratio_df)
    return num_df, ratio_df, n_inclusive_df, n_exclusive_df


def _annotate_callability(
    num_df: pd.DataFrame,
    ratio_df: pd.DataFrame,
    studies: list[str],
    panel_coverage: pd.DataFrame,
    study_panel_map: dict[str, str],
    n_inclusive_df: pd.DataFrame,
    n_exclusive_df: pd.DataFrame,
    enforce_callability_nesting_check: bool = True,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Attach n_total_studies / n_contributing_studies / n_panel_covered_studies /
    callable_fraction columns to both num_df and ratio_df.

    Adds (t070):
      - n_panel_covered_samples_inclusive : sum across studies of per-(study,
        cancer, gene) panel-restricted inclusive denominators.
      - n_panel_covered_samples_exclusive : same for exclusive.
      - callable_sample_fraction_inclusive : n_panel_covered_samples_inclusive
        / n_total_samples_in_cancer_inclusive.
      - callable_sample_fraction_exclusive : same for exclusive.

    n_total_samples_in_cancer_{inclusive,exclusive} is defined as the sum of
    per-(study, cancer) cohort sizes across studies, computed as the
    per-cancer max of the panel-restricted denominator (since cohort sizes
    are per-cancer, not per-gene, before panel restriction; the max across
    genes within a cancer recovers the cohort size).

    Assumption: per-cancer cohort size is recovered as ``n_inclusive_df.groupby(
    "cancer_type").max()`` over genes — this works only when each panel in use
    within a study covers at least one common "backbone" gene present across
    all panels (true for nested panel families like MSK-IMPACT-{341 ⊂ 410 ⊂
    468 ⊂ 505} but NOT for non-nested mixes like IMPACT-HEME + solid-tumor).
    A heuristic check raises ``ValueError`` if the recovered max for a (cancer,
    study) cell is implausibly small relative to the maximum across all studies
    for that cancer (currently 0.05 = 5% threshold). If your run hits this and
    you're certain the panel mix is non-nested, supply per-(study, cancer)
    cohort sizes via a future explicit-input refactor.
    """
    gene_to_panels: dict[str, set[str]] = (
        panel_coverage.groupby("gene")["panel_id"].apply(lambda s: set(s)).to_dict()
    )
    n_total_studies = len(studies)
    gene_symbols_in_output = (
        ratio_df.index.get_level_values("symbol").astype(str).str.upper()
    )

    def _count_covered(gene_upper: str) -> int:
        covering = 0
        covering_panels = gene_to_panels.get(gene_upper, set())
        for study in studies:
            panel = study_panel_map.get(study)
            if panel is None or panel in covering_panels:
                covering += 1
        return covering

    unique_genes = pd.Series(gene_symbols_in_output.unique())
    unique_gene_cov = {g: _count_covered(g) for g in unique_genes}
    n_panel_covered_per_row = gene_symbols_in_output.map(unique_gene_cov).astype(int)

    inclusive_cols = [c for c in ratio_df.columns if c in studies]
    n_contributing_per_row = ratio_df[inclusive_cols].notna().sum(axis=1).astype(int)

    for df in (num_df, ratio_df):
        df["n_total_studies"] = n_total_studies
        df["n_panel_covered_studies"] = n_panel_covered_per_row.to_numpy()
        df["callable_fraction"] = df["n_panel_covered_studies"] / n_total_studies
    num_df["n_contributing_studies"] = (
        num_df[inclusive_cols].notna().sum(axis=1).astype(int).to_numpy()
    )
    ratio_df["n_contributing_studies"] = n_contributing_per_row.to_numpy()

    # t070: sample-weighted callability columns.
    # Per-(cancer, gene) sum across studies of panel-restricted denominator.
    n_panel_covered_inclusive = n_inclusive_df.sum(axis=1, skipna=True).astype("int64")
    n_panel_covered_exclusive = n_exclusive_df.sum(axis=1, skipna=True).astype("int64")

    # Per-cancer total samples = sum across studies of per-(study, cancer) cohort
    # size. Cohort size for a cancer in a study = max over genes of the
    # panel-restricted denominator (genes-on-all-panels recover the cohort size;
    # genes covered only by some panels report a smaller value, so taking the
    # per-cancer max recovers the cohort total).
    cancer_idx = ratio_df.index.get_level_values("cancer_type")

    cohort_per_study_per_cancer_inclusive = n_inclusive_df.groupby(
        level="cancer_type"
    ).max()
    cohort_per_study_per_cancer_exclusive = n_exclusive_df.groupby(
        level="cancer_type"
    ).max()
    # C1 guard: detect non-nested panel mixes where groupby-max under-counts.
    # If any (study, cancer) cell's recovered cohort size is implausibly small
    # relative to the cancer's max across studies, the assumption is violated.
    NESTING_THRESHOLD = 0.05
    maxes = cohort_per_study_per_cancer_inclusive.max(axis=1)
    ratios = cohort_per_study_per_cancer_inclusive.divide(maxes, axis=0)
    suspicious = (
        ratios < NESTING_THRESHOLD
    ) & cohort_per_study_per_cancer_inclusive.notna()
    if suspicious.any().any():
        suspicious_rows = []
        for cancer in suspicious.index:
            for study in suspicious.columns:
                if suspicious.loc[cancer, study]:
                    suspicious_rows.append(
                        f"({cancer!r}, study={study!r}): "
                        f"cohort_max_over_genes={cohort_per_study_per_cancer_inclusive.loc[cancer, study]:.0f} "
                        f"vs cancer_max_across_studies={maxes.loc[cancer]:.0f}"
                    )
        message = (
            "Per-cancer cohort-size recovery assumption violated — at least one (study, "
            "cancer) cell has a max-over-genes denominator < 5% of the cancer's max across "
            "studies, suggesting non-nested panel mix (e.g., MSK-IMPACT solid-tumor + "
            "IMPACT-HEME-400 share no genes). First 10:\n  "
            + "\n  ".join(suspicious_rows[:10])
        )
        # t139 transitional escape hatch: the load-bearing role of this validation
        # disappears once join_dndscv_into_annotated and other consumers source from
        # the t077 meta-analysis output instead of this naive sample-weighted
        # aggregation. Until then, callers running with mixed-panel cohorts can opt
        # out via `--config enforce_callability_nesting_check=false`. The downstream
        # `mean_inclusive` / `mean_exclusive` columns will be biased for the affected
        # cells; consumers should prefer the t077 pooled output for cross-study
        # claims. See task t139 and the t131 review.
        if enforce_callability_nesting_check:
            raise ValueError(message)
        print(
            "WARNING: "
            + message
            + "\nProceeding because enforce_callability_nesting_check=false (t139).",
            file=sys.stderr,
        )

    n_total_samples_inclusive = cohort_per_study_per_cancer_inclusive.sum(
        axis=1, skipna=True
    )
    n_total_samples_exclusive = cohort_per_study_per_cancer_exclusive.sum(
        axis=1, skipna=True
    )
    n_total_inclusive_per_row = pd.Series(
        cancer_idx.map(n_total_samples_inclusive), index=ratio_df.index
    )
    n_total_exclusive_per_row = pd.Series(
        cancer_idx.map(n_total_samples_exclusive), index=ratio_df.index
    )
    n_total_inclusive_per_row = n_total_inclusive_per_row.replace(0, float("nan"))
    n_total_exclusive_per_row = n_total_exclusive_per_row.replace(0, float("nan"))

    for df in (num_df, ratio_df):
        df["n_panel_covered_samples_inclusive"] = (
            n_panel_covered_inclusive.reindex(df.index)
            .fillna(0)
            .astype("int64")
            .to_numpy()
        )
        df["n_panel_covered_samples_exclusive"] = (
            n_panel_covered_exclusive.reindex(df.index)
            .fillna(0)
            .astype("int64")
            .to_numpy()
        )
        df["callable_sample_fraction_inclusive"] = (
            df["n_panel_covered_samples_inclusive"].astype(float)
            / n_total_inclusive_per_row.astype(float).to_numpy()
        )
        df["callable_sample_fraction_exclusive"] = (
            df["n_panel_covered_samples_exclusive"].astype(float)
            / n_total_exclusive_per_row.astype(float).to_numpy()
        )

    return num_df, ratio_df


def _protein_length_adjusted(
    ratio_df: pd.DataFrame, protein_lengths: pd.DataFrame
) -> pd.DataFrame:
    """Attach ``mean_adj`` (== ``mean_inclusive`` / protein_length, NaN-filled with median)."""
    plengths = protein_lengths[
        protein_lengths.symbol.isin(ratio_df.index.get_level_values("symbol"))
    ].set_index("symbol")
    median_length = float(plengths["length"].astype(float).median())
    mean_mi = ratio_df["mean_inclusive"]
    merged = pd.merge(mean_mi, plengths, left_index=True, right_index=True, how="left")
    merged["length"] = merged["length"].astype(float).fillna(median_length)
    ratio_df["mean_adj"] = merged["mean_inclusive"] / merged["length"]
    return ratio_df


def _run_via_snakemake() -> None:
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821

    per_study_paths: list[str] = list(snek.input.per_study)
    per_study_cancer_paths: list[str] = list(snek.input.per_study_cancer)
    protein_lengths_path: str = snek.input.protein_lengths
    panel_coverage_path: str = snek.input.panel_coverage

    frames: list[tuple[str, pd.DataFrame]] = []
    studies: list[str] = []
    for infile in per_study_paths:
        df = pd.read_feather(infile)
        study = _study_id_from_path(infile)
        studies.append(study)
        frames.append((study, df))

    num_df, ratio_df, n_inclusive_df, n_exclusive_df = combine_paired_pivot(frames)

    panel_coverage = pd.read_feather(panel_coverage_path)
    study_panel_map: dict[str, str] = snek.config.get("study_panel_map", {}) or {}
    cancer_presence_by_study = _load_cancer_presence(per_study_cancer_paths)
    num_df, ratio_df, n_inclusive_df, n_exclusive_df = _fill_missing_unmutated_cells(
        num_df,
        ratio_df,
        n_inclusive_df,
        n_exclusive_df,
        cancer_presence_by_study=cancer_presence_by_study,
        study_panel_map=study_panel_map,
        panel_bearing_studies=set(snek.config.get("panel_bearing_studies", [])),
    )
    # Sort and length-adjust after zero-fill so pooled summaries reflect the
    # final callable-but-unmutated WES cells.
    ratio_df = ratio_df.sort_values("mean_inclusive", ascending=False)
    num_df = num_df.reindex(ratio_df.index)
    n_inclusive_df = n_inclusive_df.reindex(ratio_df.index)
    n_exclusive_df = n_exclusive_df.reindex(ratio_df.index)

    ratio_df = _protein_length_adjusted(ratio_df, pd.read_feather(protein_lengths_path))

    # snakemake's `--config KEY=VALUE` keeps VALUE as a string, so `bool('false')`
    # is True. Coerce string forms explicitly.
    raw_enforce = snek.config.get("enforce_callability_nesting_check", True)
    if isinstance(raw_enforce, str):
        enforce = raw_enforce.strip().lower() not in {"false", "0", "no", ""}
    else:
        enforce = bool(raw_enforce)
    num_df, ratio_df = _annotate_callability(
        num_df,
        ratio_df,
        studies,
        panel_coverage,
        study_panel_map,
        n_inclusive_df,
        n_exclusive_df,
        enforce_callability_nesting_check=enforce,
    )

    num_df = num_df.reset_index()
    ratio_df = ratio_df.reset_index()

    num_df = num_df.astype({"cancer_type": "category", "symbol": "category"})
    ratio_df = ratio_df.astype({"cancer_type": "category", "symbol": "category"})

    num_df.to_feather(snek.output[0])
    ratio_df.to_feather(snek.output[1])

    n_mapped = sum(1 for s in studies if s in study_panel_map)
    print(
        f"Callability annotation: {len(studies)} studies total "
        f"({n_mapped} mapped to a GENIE panel, {len(studies) - n_mapped} treated as WES). "
        f"Median per-gene callable_fraction = {ratio_df['callable_fraction'].median():.3f}. "
        f"Hypermutator-paired columns emitted: mean_inclusive + mean_exclusive.",
        file=sys.stderr,
    )


if "snakemake" in globals():
    _run_via_snakemake()
