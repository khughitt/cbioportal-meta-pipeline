# science:code
# status: workflow-owned
# science:end
"""
process_bailey2018_drivers.py

Processes the Bailey et al. 2018 (Cell) PanCanAtlas driver-gene consensus supplementary table
into a tidy feather of `(gene, cancer_type, ...)` rows.

Input
-----
- Bailey2018 Table S1 (TSV or XLSX). Source: PMID 30096302 / DOI 10.1016/j.cell.2018.02.060.

  Accepts either:
    - `data/bailey2018_table_s1.tsv` (preferred — clean single-sheet form)
    - `data/bailey2018_table_s1.xlsx` or `data/mmc1.xlsx` (full Cell supplement; Table S1 sheet
      with header-row cleanup)

Output
------
A feather file keyed by `(gene, cancer_type)` with columns:
    gene                  (str)  — HGNC symbol (upper-cased)
    cancer_type           (str)  — TCGA cancer-type abbreviation, or "PANCAN"
    prediction            (str)  — "oncogene" / "tsg" / "" (Bailey's 20/20+ prediction)
    decision              (str)  — Bailey's decision category (e.g., "official", "rescued")
    tissue_frequency      (str)  — per-cancer mutation frequency (as published, e.g., "5.30%")
    pancan_frequency      (str)  — pan-cancer mutation frequency
    consensus_score       (float)
    source                (str)  — "Bailey2018"
"""

import sys
from pathlib import Path

import pandas as pd

snek = snakemake  # type: ignore[name-defined]  # noqa: F821

input_path = Path(snek.input[0])
output_feather = snek.output[0]


def _read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", dtype=str, na_filter=False)


def _read_xlsx(path: Path) -> pd.DataFrame:
    """Read the multi-sheet Cell supplement; Table S1's header lives in row 1 (0-indexed)."""
    sheets = pd.read_excel(path, sheet_name=None, engine="openpyxl")
    table_s1 = sheets.get("Table S1") or next(iter(sheets.values()))
    # The first row of the Cell supplement sheet is the title; real headers are in row 1.
    table_s1.columns = table_s1.iloc[0].astype(str)
    return table_s1.iloc[1:].reset_index(drop=True)


if input_path.suffix.lower() in {".tsv", ".txt"}:
    raw = _read_tsv(input_path)
elif input_path.suffix.lower() == ".xlsx":
    raw = _read_xlsx(input_path)
else:
    raise ValueError(f"Unsupported Bailey input format: {input_path}")

# Column name normalization — lower-case, strip, replace whitespace with underscore.
norm_map = {c: c.strip().lower().replace(" ", "_") for c in raw.columns}
raw = raw.rename(columns=norm_map)

required = {"gene", "cancer"}
missing = required - set(raw.columns)
if missing:
    raise ValueError(
        f"Missing required columns {sorted(missing)} in Bailey Table S1. Got: {list(raw.columns)}"
    )


def _col(row: pd.Series, *names: str) -> str:
    for n in names:
        if n in row.index and bool(pd.notna(row[n])):
            v = str(row[n]).strip()
            if v and v != "nan":
                return v
    return ""


drivers = pd.DataFrame(
    {
        "gene": raw["gene"].astype(str).str.strip().str.upper(),
        "cancer_type": raw["cancer"].astype(str).str.strip().str.upper(),
        "prediction": raw.apply(
            lambda r: _col(
                r,
                "tumor_suppressor_or_oncogene_prediction_(by_20/20+)",
                "prediction",
                "og/tsg",
            ),
            axis=1,
        ),
        "decision": raw.apply(lambda r: _col(r, "decision"), axis=1),
        "tissue_frequency": raw.apply(lambda r: _col(r, "tissue_frequency"), axis=1),
        "pancan_frequency": raw.apply(lambda r: _col(r, "pancan_frequency"), axis=1),
    }
)

# Consensus score — numeric if present, else null.
if "consensus_score" in raw.columns:
    drivers["consensus_score"] = pd.to_numeric(raw["consensus_score"], errors="coerce")
else:
    drivers["consensus_score"] = pd.NA

drivers["source"] = "Bailey2018"

drivers = (
    drivers.loc[
        (drivers["gene"].str.len() > 0) & (drivers["cancer_type"].str.len() > 0)
    ]
    .drop_duplicates(subset=["gene", "cancer_type"])
    .reset_index(drop=True)
)

drivers.to_feather(output_feather)
print(
    f"Wrote {len(drivers)} (gene, cancer_type) driver rows to {output_feather} "
    f"({drivers['cancer_type'].nunique()} distinct cancer types including PANCAN)",
    file=sys.stderr,
)
