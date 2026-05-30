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
import hashlib
import json
import sys
from pathlib import Path

import pandas as pd

snek = snakemake  # type: ignore[name-defined]  # noqa: F821

study_id = snek.wildcards["id"]
data_dir = Path(snek.config["data_dir"])
study_dir = data_dir / study_id
expr_out = Path(snek.output["expression"])
clin_out = Path(snek.output["clinical"])
dp_out = Path(snek.output["datapackage"])
qa_out = Path(snek.output["qa"])


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

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
# Coerce to numeric, but ACCOUNT for what coercion hides rather than silently dropping
# tokens. A cell becomes NaN if it was an empty/NA token OR an unexpected non-numeric
# string; both matter because CYCLOPS needs complete finite matrices (the consuming
# WP2 prep must drop or impute incomplete genes — see the design's missingness note).
before_na = expr[sample_cols].isna().to_numpy().sum()
expr[sample_cols] = expr[sample_cols].apply(pd.to_numeric, errors="coerce").astype("float32")
after_na = int(expr[sample_cols].isna().to_numpy().sum())
coerced = int(after_na - before_na)          # cells that were non-numeric (not already NA)
genes_with_na = int((expr[sample_cols].isna().any(axis=1)).sum())
_log(
    f"numeric coercion: {coerced} non-numeric cell(s) -> NaN, "
    f"{after_na} total missing cell(s) across {genes_with_na} gene(s) with >=1 missing "
    f"(of {expr.shape[0]} genes). WP2 must enforce complete finite matrices before Julia."
)
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

# --- QA report ------------------------------------------------------------------
expr_samples = set(sample_cols)
clin_samples = set(clinical["SAMPLE_ID"]) if "SAMPLE_ID" in clinical.columns else set()
overlap = expr_samples & clin_samples
qa_lines = [
    f"# QA report — {study_id} expression export",
    "",
    f"- source mRNA file: `{mrna_name}`",
    f"- expression: **{expr.shape[0]} genes × {len(sample_cols)} samples** "
    f"(duplicate Hugo_Symbol rows collapsed by mean: {n_dup})",
    f"- missing expression cells: **{after_na}** across **{genes_with_na}** gene(s) "
    f"with ≥1 missing ({coerced} were non-numeric tokens coerced to NaN). "
    f"Downstream CYCLOPS prep must enforce complete finite matrices.",
    f"- clinical: {clinical.shape[0]} rows × {clinical.shape[1]} fields",
    f"- sample overlap (expression ∩ clinical): **{len(overlap)}** "
    f"({len(expr_samples - clin_samples)} expr-only, {len(clin_samples - expr_samples)} clin-only)",
]
for sub_col in ("SUBTYPE", "CLAUDIN_SUBTYPE"):
    if sub_col in clinical.columns:
        vc = clinical[sub_col].fillna("(blank)").value_counts()
        qa_lines.append(f"- `{sub_col}` counts: " + ", ".join(f"{k}={v}" for k, v in vc.items()))
qa_out.write_text("\n".join(qa_lines) + "\n")

# --- datapackage (frictionless-style descriptor; makes the product promotable) ---
dp = {
    "name": f"{study_id}-expression",
    "title": f"{study_id} — mRNA expression + clinical (cBioPortal export)",
    "profile": "tabular-data-package",
    "source_study": study_id,
    "source_mrna_file": mrna_name,
    "resources": [
        {
            "name": "expression",
            "path": expr_out.name,
            "format": "parquet",
            "bytes": expr_out.stat().st_size,
            "hash": f"sha256:{_sha256(expr_out)}",
            "shape": {"genes": int(expr.shape[0]), "samples": int(len(sample_cols))},
            "missing_cells": after_na,
            "genes_with_missing": genes_with_na,
        },
        {
            "name": "clinical",
            "path": clin_out.name,
            "format": "parquet",
            "bytes": clin_out.stat().st_size,
            "hash": f"sha256:{_sha256(clin_out)}",
            "shape": {"rows": int(clinical.shape[0]), "fields": int(clinical.shape[1])},
        },
        {
            "name": "qa",
            "path": qa_out.name,
            "format": "md",
            "bytes": qa_out.stat().st_size,
            "hash": f"sha256:{_sha256(qa_out)}",
            "role": "qa",
        },
    ],
}
dp_out.write_text(json.dumps(dp, indent=2))
_log(
    f"DONE: {expr.shape[0]} genes x {len(sample_cols)} samples; "
    f"{len(overlap)} matched; datapackage + qa_report.md written -> {dp_out.parent}"
)
