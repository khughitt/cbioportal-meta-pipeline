# science:code
# status: workflow-owned
# science:end
#
# export_study_expression.py
#
# Surface a cBioPortal study's mRNA expression matrix + merged clinical table as
# tidy parquet products, for downstream expression analyses (e.g. the health-cycles
# tumor-CMag prognostic validation, t046). This is a GENERIC, faithful export: it
# does not subset by subtype or derive analysis-specific endpoints — those belong to
# the consuming analysis. It only (a) picks the study's mRNA matrix, (b) merges the
# patient + sample clinical files into one sample-level frame, and (c) reports QA.
#
# Inputs (already staged on disk by download_study; the .staged marker gates this):
#   data_dir/{id}/{mrna_file}            -- genes x samples, tab-separated, with
#                                           leading Hugo_Symbol + Entrez_Gene_Id cols
#   data_dir/{id}/data_clinical_patient.txt
#   data_dir/{id}/data_clinical_sample.txt
#
# Outputs:
#   out_dir/studies/{id}/expression/expression.parquet  -- Hugo_Symbol + one col/sample
#   out_dir/studies/{id}/expression/clinical.parquet     -- one row per sample
#
import sys
from pathlib import Path

import pandas as pd

snek = snakemake  # type: ignore[name-defined]  # noqa: F821

study_id = snek.wildcards["id"]
data_dir = Path(snek.config["data_dir"])
study_dir = data_dir / study_id
expr_out = Path(snek.output["expression"])
clin_out = Path(snek.output["clinical"])

# mRNA filename: config override per study, else auto-detect by priority. Expression
# file names differ by platform (RNA-seq RSEM vs microarray), so this is study-specific.
_PRIORITY = [
    "data_mrna_seq_v2_rsem.txt",            # TCGA pan-can-atlas RNA-seq (RSEM)
    "data_mrna_seq_v2_rsem_zscores_ref_all_samples.txt",
    "data_mrna_illumina_microarray.txt",    # METABRIC Illumina microarray
    "data_mrna_agilent_microarray.txt",
    "data_mrna_seq_rpkm.txt",
    "data_mrna_v2_rsem.txt",
]
cfg_map = (snek.config.get("expression", {}) or {}).get("mrna_file", {}) or {}
mrna_name = cfg_map.get(study_id)
if mrna_name is None:
    mrna_name = next((n for n in _PRIORITY if (study_dir / n).exists()), None)
if mrna_name is None:
    raise FileNotFoundError(
        f"export_study_expression ({study_id}): no mRNA matrix found in {study_dir} "
        f"(looked for config override + {_PRIORITY})"
    )
mrna_path = study_dir / mrna_name


def _read_clinical(path: Path) -> pd.DataFrame:
    """cBioPortal clinical: N leading '#'-prefixed metadata rows, then a header row
    of attribute IDs, then data. Skip the '#' rows; the next row is the header."""
    with path.open() as fh:
        n_hash = 0
        for line in fh:
            if line.startswith("#"):
                n_hash += 1
            else:
                break
    return pd.read_csv(path, sep="\t", skiprows=n_hash, dtype=str)


def _log(msg: str) -> None:
    print(f"export_study_expression ({study_id}): {msg}", file=sys.stderr)


# --- expression -----------------------------------------------------------------
_log(f"reading mRNA matrix {mrna_name}")
expr = pd.read_csv(mrna_path, sep="\t", low_memory=False)
# Drop the Entrez id column; key on Hugo_Symbol. Drop blank/NaN symbols, collapse
# duplicate symbols by mean (a handful of microarray probes map to the same gene).
drop_cols = [c for c in ("Entrez_Gene_Id", "Entrez_Gene_ID") if c in expr.columns]
expr = expr.drop(columns=drop_cols)
sym_col = "Hugo_Symbol" if "Hugo_Symbol" in expr.columns else str(expr.columns[0])
expr = expr.rename(columns={sym_col: "Hugo_Symbol"})
expr["Hugo_Symbol"] = expr["Hugo_Symbol"].astype(str).str.strip()
keep = (expr["Hugo_Symbol"] != "") & (expr["Hugo_Symbol"].str.lower() != "nan")
expr = expr.loc[keep].copy()
sample_cols = [c for c in expr.columns if c != "Hugo_Symbol"]
expr[sample_cols] = expr[sample_cols].apply(pd.to_numeric, errors="coerce").astype("float32")
n_dup = int(expr["Hugo_Symbol"].duplicated().sum())
if n_dup:
    _log(f"collapsing {n_dup} duplicate Hugo_Symbol rows by mean")
    expr = expr.groupby("Hugo_Symbol", as_index=False)[sample_cols].mean()
expr_out.parent.mkdir(parents=True, exist_ok=True)
expr.to_parquet(expr_out, index=False)

# --- clinical -------------------------------------------------------------------
_log("merging patient + sample clinical tables")
patient = _read_clinical(study_dir / "data_clinical_patient.txt")
sample = _read_clinical(study_dir / "data_clinical_sample.txt")
clinical = sample.merge(patient, on="PATIENT_ID", how="left", suffixes=("", "_patient"))
clinical.insert(0, "study_id", study_id)
clinical.to_parquet(clin_out, index=False)

# --- QA -------------------------------------------------------------------------
expr_samples = set(sample_cols)
clin_samples = set(clinical["SAMPLE_ID"]) if "SAMPLE_ID" in clinical.columns else set()
overlap = expr_samples & clin_samples
_log(
    f"DONE: {expr.shape[0]} genes x {len(sample_cols)} expression samples; "
    f"{clinical.shape[0]} clinical rows; "
    f"{len(overlap)} samples with BOTH expression + clinical "
    f"({len(expr_samples - clin_samples)} expr-only, {len(clin_samples - expr_samples)} clin-only)"
)
