"""
create_combined_gene_cancer_freq_table.py

Concatenates per-study gene x cancer mutation frequency tables into cross-study wide-format
feathers keyed by (cancer_type, symbol).

Outputs:
  - gene_cancer_study.feather       : per-study mutation counts, one column per study, plus
                                      callability metadata columns (see below).
  - gene_cancer_study_ratio.feather : per-study mutation ratios (sample-level), one column
                                      per study, plus `mean`, `mean_adj`, and callability
                                      metadata columns.

Callability columns (added per row, closes audit F2 partially — annotation-only pass):

  - n_total_studies           : total number of studies in the aggregation.
  - n_contributing_studies    : count of per-study columns with a non-null value for this row
                                (i.e., studies where at least one mutation was observed in
                                this (gene, cancer_type) cell).
  - n_panel_covered_studies   : number of studies whose panel covers this gene. WES / WGS
                                studies and studies not in the `study_panel_map` config key
                                are assumed to cover all genes. Studies mapped to a GENIE
                                SEQ_ASSAY_ID only count if the gene is callable on that panel
                                (per the GENIE genomic_information.txt ingestion).
  - callable_fraction         : n_panel_covered_studies / n_total_studies.

The aggregation itself (`mean`) is not changed by this pass — the existing behavior of
`.mean(axis=1, skipna=True)` is preserved. Consumers wanting panel-aware pooling can use the
callability columns to filter / weight the per-study columns themselves. A follow-on task
will tighten the NaN-vs-0 handling (currently NaN conflates "gene not on panel", "gene on
panel but unmutated", and "cancer type not represented in study" — disambiguating the third
case requires per-(study, cancer_type) sample counts, which are not yet ingested here).

Aggregation choice (audit 2026-04-13, F1 + F9):

- For **ratios**, an unweighted mean across studies is used ('mean' column). This treats each
  per-study ratio as an exchangeable observation of the per-cancer rate. A sample-size-weighted
  or random-effects-pooled alternative is preferable and is tracked by t062 / t071 — deferred
  until per-study sample counts are ingested upstream.

- For **raw counts**, no summary column is computed. Averaging raw counts across studies of
  different sizes is statistically incoherent.

`mean_adj` on the ratio output divides by protein length — a first-order per-gene background-
rate correction (see topic:mutation-rate-normalization).

Config
------

- `study_panel_map` (dict of `study_id -> SEQ_ASSAY_ID`): optional. Studies listed here are
  treated as panel-restricted (callability per the GENIE coverage feather). Studies NOT in
  this map are treated as WES / unrestricted. Default: empty (all studies WES).
"""
import os
import sys

import pandas as pd

snek = snakemake  # type: ignore[name-defined]

# Named inputs: per_study (list), protein_lengths, panel_coverage.
per_study_paths: list[str] = list(snek.input.per_study)
protein_lengths_path: str = snek.input.protein_lengths
panel_coverage_path: str = snek.input.panel_coverage

num_dfs = []
ratio_dfs = []
studies: list[str] = []

for infile in per_study_paths:
    df = pd.read_feather(infile)
    df = df.set_index(list(df.columns[:2]))

    study = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(infile))))
    studies.append(study)

    df1 = df['num']
    df2 = df['ratio']
    df1.name = study
    df2.name = study

    num_dfs.append(df1)
    ratio_dfs.append(df2)

num_df = pd.concat(num_dfs, axis=1)
ratio_df = pd.concat(ratio_dfs, axis=1)

# Compute pooled ratio (unweighted mean of per-study rates — see module docstring).
ratio_df.loc[:, 'mean'] = ratio_df.mean(axis=1)
ratio_df = ratio_df.sort_values('mean', ascending=False)

# Align num_df to ratio_df's row order so paired outputs share an ordering.
num_df = num_df.reindex(ratio_df.index)

# Protein-length-adjusted pooled ratio. Missing protein lengths fall back to the median.
protein_lengths = pd.read_feather(protein_lengths_path)
protein_lengths = protein_lengths[
    protein_lengths.symbol.isin(ratio_df.index.get_level_values('symbol'))
]
protein_lengths = protein_lengths.set_index('symbol')
median_length = protein_lengths.length.median()

ratio_mean = ratio_df.loc[:, 'mean']
ratio_mean = pd.merge(ratio_mean, protein_lengths, left_index=True, right_index=True, how='left')
# Cast length to float so the median-fallback (which may be a half-integer) is a valid value.
ratio_mean['length'] = ratio_mean['length'].astype(float)
ratio_mean.loc[ratio_mean.length.isna(), 'length'] = float(median_length)
ratio_df['mean_adj'] = ratio_mean['mean'] / ratio_mean['length']

# --- Callability annotation (audit F2 partial close) -------------------------
#
# Build per-gene panel-covered-study count using the GENIE panel coverage feather and the
# config `study_panel_map`. Studies not in the map are assumed WES (all genes callable).
#
panel_coverage = pd.read_feather(panel_coverage_path)
# gene -> set of SEQ_ASSAY_IDs that cover it
gene_to_panels: dict[str, set[str]] = (
    panel_coverage.groupby('gene')['panel_id'].apply(lambda s: set(s)).to_dict()
)

study_panel_map: dict[str, str] = snek.config.get('study_panel_map', {}) or {}

# Per-gene list of studies where the gene is callable.
gene_symbols_in_output = ratio_df.index.get_level_values('symbol').astype(str).str.upper()

n_total_studies = len(studies)


def _count_covered(gene_upper: str) -> int:
    covering = 0
    covering_panels = gene_to_panels.get(gene_upper, set())
    for study in studies:
        panel = study_panel_map.get(study)
        if panel is None:
            # WES / unmapped — assume all genes callable.
            covering += 1
        elif panel in covering_panels:
            covering += 1
    return covering


# Compute per-unique-gene first (many rows share symbols), then broadcast.
unique_genes = pd.Series(gene_symbols_in_output.unique())
unique_gene_cov = {g: _count_covered(g) for g in unique_genes}

n_panel_covered_per_row = gene_symbols_in_output.map(unique_gene_cov).astype(int)

# n_contributing_studies: count of per-study columns that are non-null for each row.
study_cols = [c for c in ratio_df.columns if c in studies]
n_contributing_per_row = ratio_df[study_cols].notna().sum(axis=1).astype(int)

ratio_df['n_total_studies'] = n_total_studies
ratio_df['n_contributing_studies'] = n_contributing_per_row.to_numpy()
ratio_df['n_panel_covered_studies'] = n_panel_covered_per_row.to_numpy()
ratio_df['callable_fraction'] = ratio_df['n_panel_covered_studies'] / n_total_studies

# Mirror the callability columns onto num_df for symmetry (reindex keeps row alignment).
num_df['n_total_studies'] = n_total_studies
num_df['n_contributing_studies'] = (
    num_df[study_cols].notna().sum(axis=1).astype(int).to_numpy()
)
num_df['n_panel_covered_studies'] = n_panel_covered_per_row.to_numpy()
num_df['callable_fraction'] = num_df['n_panel_covered_studies'] / n_total_studies

num_df = num_df.reset_index()
ratio_df = ratio_df.reset_index()

num_df = num_df.astype({
    'cancer_type': 'category',
    'symbol': 'category'
})

ratio_df = ratio_df.astype({
    'cancer_type': 'category',
    'symbol': 'category'
})

num_df.to_feather(snek.output[0])
ratio_df.to_feather(snek.output[1])

# Diagnostic summary: report the callability landscape for the cohort.
n_mapped = sum(1 for s in studies if s in study_panel_map)
print(
    f"Callability annotation: {n_total_studies} studies total "
    f"({n_mapped} mapped to a GENIE panel, {n_total_studies - n_mapped} treated as WES). "
    f"Median per-gene callable_fraction = {ratio_df['callable_fraction'].median():.3f}.",
    file=sys.stderr,
)
