"""
annotate_ch.py

Clonal-hematopoiesis-aware annotation pass for the combined gene x cancer ratio table.
Closes audit findings F3 + F7 (see `doc/audits/2026-04-13-create-combined-gene-cancer-freq-table-audit.md`).

Adds three classes of annotation:
1. `ch_priority_gene` — boolean flag for the 7-gene Bolton 2020 priority list
   (DNMT3A, PPM1D, TET2, TP53, ASXL1, CHEK2, PRPF8). These are the genes most at risk of CH
   contamination in tumor-only-called panel cohorts.
2. `mean_matched` / `mean_unmatched` — pooled ratios computed separately over the matched-normal
   and tumor-only study sub-cohorts. For CH-priority genes, a large `mean_matched` vs
   `mean_unmatched` discordance is the signal that CH is contaminating the pooled rate.
3. `n_matched_studies` / `n_unmatched_studies` — per-row count of contributing studies in each
   sub-cohort.

Inputs
------
- snakemake.input[0] : `summary/mut/table/gene_cancer_study_ratio_overlay_annotated.feather`
  — the cross-study wide-format ratio table after the unified Bailey / CGC /
  Sanchez-Vega overlay step.

Config
------
Reads `config['matched_normal_studies']` — an explicit list of study IDs known to use
patient-matched buffy-coat / normal sequencing. Studies NOT in this list are treated as
tumor-only (the conservative default — CH-priority genes are flagged as potentially
contaminated in these cohorts). If the config key is missing or empty, all studies are
treated as tumor-only, `mean_matched` is NaN for every row, and the annotation is still
applied — but downstream consumers should recognize the absence of any matched-normal
signal.

Output
------
- snakemake.output[0] : `summary/mut/table/gene_cancer_study_ratio_ch_annotated.feather` —
  same table plus the columns above. A downstream join step adds the pooled t077
  meta-analysis columns onto the final canonical
  `summary/mut/table/gene_cancer_study_ratio_annotated.feather` surface.

References
----------
- Bolton et al. 2020, Nat Genet — the 7-gene priority list + therapy-selectivity spectrum.
- Cheng et al. 2015, J Mol Diagn — quantifies ~9 extra spurious private germline calls per
  unmatched-normal sample vs matched. Motivates treating unmatched-normal as the conservative
  default for CH-driver-gene interpretation.
- Pugh et al. 2022, Cancer Discov — documents that 52% of GENIE v9.1 is tumor-only.
- `topic:clonal-hematopoiesis-contamination` and `topic:cross-study-harmonization` for the
  full synthesis.
"""
import pandas as pd

snek = snakemake  # type: ignore[name-defined]  # noqa: F821

CH_PRIORITY_GENES: frozenset[str] = frozenset({
    "DNMT3A", "PPM1D", "TET2", "TP53", "ASXL1", "CHEK2", "PRPF8",
})

ratio = pd.read_feather(snek.input[0])

# Identify per-study columns (everything that isn't a key, summary, or pre-existing annotation).
reserved = {
    "cancer_type", "symbol", "mean", "mean_adj",
    # t098 part B: paired pooled columns + callability metadata.
    "mean_inclusive", "mean_exclusive",
    "n_total_studies", "n_contributing_studies", "n_panel_covered_studies",
    "callable_fraction",
    "ch_priority_gene", "mean_matched", "mean_unmatched",
    "n_matched_studies", "n_unmatched_studies",
    # Inherited from upstream annotate.py (unified overlay) rule:
    "bailey2018_driver", "bailey2018_source",
    "cgc_tier_1", "cgc_tier_2", "cgc_role_in_cancer", "cgc_source",
    "sanchez_vega_pathway", "sanchez_vega_og_tsg", "sanchez_vega_source",
}
# Per-study columns: legacy-named slot per study (= inclusive view). The paired
# ``{study}_exclusive`` columns emitted by t098 part B are skipped here so
# matched-normal / tumor-only stratification operates on the full-cohort rates
# (the interpretive frame CH aligns to). Exclusive-variant stratification, if
# ever needed, can be added as a separate pass.
study_cols: list[str] = [
    c for c in ratio.columns
    if c not in reserved and not c.endswith("_exclusive")
]

matched_studies: set[str] = set(snek.config.get("matched_normal_studies", []))
matched_cols: list[str] = [c for c in study_cols if c in matched_studies]
unmatched_cols: list[str] = [c for c in study_cols if c not in matched_studies]

# CH-priority flag — operates on the gene symbol regardless of cancer.
ratio["ch_priority_gene"] = ratio["symbol"].astype(str).str.upper().isin(CH_PRIORITY_GENES)

# Stratified pooled means over the per-study columns. NaN when a partition contributes no
# studies for a given row.
if matched_cols:
    matched_slice = ratio[matched_cols]
    ratio["mean_matched"] = matched_slice.mean(axis=1, skipna=True)
    ratio["n_matched_studies"] = matched_slice.notna().sum(axis=1)
else:
    ratio["mean_matched"] = float("nan")
    ratio["n_matched_studies"] = 0

unmatched_slice = ratio[unmatched_cols]
ratio["mean_unmatched"] = unmatched_slice.mean(axis=1, skipna=True)
ratio["n_unmatched_studies"] = unmatched_slice.notna().sum(axis=1)

ratio.to_feather(snek.output[0])
