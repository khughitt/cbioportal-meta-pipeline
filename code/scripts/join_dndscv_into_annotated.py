# science:code
# status: workflow-owned
# science:end
#
# join_dndscv_into_annotated.py (t131)
#
# Join per-(symbol, cancer_type) dNdScv columns into the canonical
# `gene_cancer_study_ratio_annotated.feather`. New columns added per the
# §"Schema contract on canonical feather" section of the t131 design plan.
# Existing columns preserved unchanged.
#
# Inputs (snek.input):
#   annotated     — summary/mut/table/gene_cancer_study_ratio_annotated.feather
#                   (from rule join_gene_cancer_meta_in_ratio_table)
#   per_cancer    — list of summary/mut/dndscv/per_cancer/{slug}/genes.feather
#
# Output (snek.output[0]):
#   summary/mut/table/gene_cancer_study_ratio_annotated_dndscv.feather
#   (replaces the un-suffixed file via a downstream alias rule, OR the
#   Snakefile renames the rule chain so this becomes the canonical path —
#   see §"File-by-file delta" decision in the plan.)
#
# Schema added (per §"Schema contract on canonical feather"):
#   dndscv_qglobal_cv               float64, nullable
#   dndscv_significant_q05          boolean, nullable
#   dndscv_input_status             category (not_run / below_threshold /
#                                   failed_qc / tested_not_significant /
#                                   tested_significant)
#   dndscv_input_modality           category (wes / panel / mixed)
#   dndscv_panel_only               boolean, nullable
#   dndscv_n_samples                int64, nullable
#   dndscv_n_variants               int64, nullable
#   dndscv_split_build              boolean, nullable
#   dndscv_refdb                    string (hg19/hg38)
#   dndscv_package_version          string
#   dndscv_git_sha                  string
#
# Cancer types in `annotated` that have NO dndscv per_cancer file land
# `dndscv_input_status = "not_run"` and all other dndscv columns null.
#
import pandas as pd

snek = snakemake  # type: ignore[name-defined]  # noqa: F821

DNDSCV_COLS = [
    "dndscv_qglobal_cv",
    "dndscv_significant_q05",
    "dndscv_input_status",
    "dndscv_input_modality",
    "dndscv_panel_only",
    "dndscv_n_samples",
    "dndscv_n_variants",
    "dndscv_split_build",
    "dndscv_refdb",
    "dndscv_package_version",
    "dndscv_git_sha",
]

# ---------------------------------------------------------------------------
# Load existing annotated feather + concatenate per-cancer dNdScv outputs.
# ---------------------------------------------------------------------------
annotated = pd.read_feather(snek.input.annotated)
per_cancer_paths = list(snek.input.per_cancer)
print(
    f"join_dndscv_into_annotated: annotated has {len(annotated):,} rows; "
    f"reading {len(per_cancer_paths):,} per-cancer dndscv outputs"
)

dndscv_frames = []
for path in per_cancer_paths:
    df = pd.read_feather(path)
    if df.empty:
        continue
    # Drop placeholder rows where symbol is NA (cancer types where no real
    # gene rows were emitted; their cohort metadata is preserved in run
    # summaries elsewhere).
    df = df[df["symbol"].notna()].copy()
    if df.empty:
        continue
    dndscv_frames.append(df)

if dndscv_frames:
    dndscv_long = pd.concat(dndscv_frames, ignore_index=True)
    dndscv_long["symbol"] = dndscv_long["symbol"].astype(str)
    dndscv_long["cancer_type"] = dndscv_long["cancer_type"].astype(str)
else:
    dndscv_long = pd.DataFrame(columns=pd.Index(["symbol", "cancer_type"] + DNDSCV_COLS))

print(
    f"join_dndscv_into_annotated: dndscv_long has {len(dndscv_long):,} "
    "(symbol, cancer_type) rows"
)

# ---------------------------------------------------------------------------
# Left-join on (symbol, cancer_type). Cast annotated.symbol/cancer_type to
# str to match (the annotated feather stores them as categorical).
# ---------------------------------------------------------------------------
annot_str = annotated.copy()
annot_str["symbol_str"] = annot_str["symbol"].astype(str)
annot_str["cancer_type_str"] = annot_str["cancer_type"].astype(str)

joined = annot_str.merge(
    dndscv_long.rename(columns={"symbol": "symbol_str", "cancer_type": "cancer_type_str"}),
    on=["symbol_str", "cancer_type_str"],
    how="left",
)
joined = joined.drop(columns=["symbol_str", "cancer_type_str"])

# ---------------------------------------------------------------------------
# Default `dndscv_input_status` = "not_run" for rows where the join produced
# no dndscv signal AT ALL (cancer type was not in the dndscv input set).
# ---------------------------------------------------------------------------
status_col = joined["dndscv_input_status"].astype(object)
status_col = status_col.where(status_col.notna(), other="not_run")
joined["dndscv_input_status"] = pd.Categorical(
    status_col,
    categories=[
        "not_run",
        "below_threshold",
        "failed_qc",
        "tested_not_significant",
        "tested_significant",
    ],
)

# Modality is a meaningful categorical; pin it for storage compactness.
modality_col = joined["dndscv_input_modality"].astype(object)
joined["dndscv_input_modality"] = pd.Categorical(
    modality_col,
    categories=["wes", "panel", "mixed"],
)

# Boolean columns: preserve nullable semantics via pandas BooleanDtype.
for bcol in ("dndscv_significant_q05", "dndscv_panel_only", "dndscv_split_build"):
    joined[bcol] = joined[bcol].astype("boolean")

# Numeric columns: use nullable Int64 for counts.
for icol in ("dndscv_n_samples", "dndscv_n_variants"):
    joined[icol] = joined[icol].astype("Int64")

# Strings: refdb / version / sha
for scol in ("dndscv_refdb", "dndscv_package_version", "dndscv_git_sha"):
    joined[scol] = joined[scol].astype(object)

joined = joined.reset_index(drop=True)
joined.to_feather(snek.output[0])

n_with_q = int(joined["dndscv_qglobal_cv"].notna().sum())
n_sig = int(((joined["dndscv_significant_q05"].fillna(False)).astype(bool)).sum())
print(
    f"join_dndscv_into_annotated: wrote {len(joined):,} rows to {snek.output[0]} "
    f"({n_with_q:,} with non-null dndscv_qglobal_cv; {n_sig:,} with q < 0.05)"
)
