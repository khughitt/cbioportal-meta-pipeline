# science:code
# status: workflow-owned
# science:end
"""
process_sanchez_vega_pathways.py

Processes Sanchez-Vega et al. 2018 (Cell) supplementary Table S3 — curated templates for the
10 canonical oncogenic signaling pathways — into a tidy feather of `(pathway, gene, ...)` rows.

Input
-----
- snakemake.input[0] : `data/sanchez_vega_2018_tables_s3.xlsx`

  Source: Sanchez-Vega F, et al. 2018. "Oncogenic Signaling Pathways in The Cancer Genome
  Atlas." *Cell* 173:321–337. PMID 29625050 / DOI 10.1016/j.cell.2018.03.035.

  The xlsx has one sheet per pathway (Cell Cycle, HIPPO, MYC, NOTCH, NRF2, PI3K, TGF-Beta,
  RTK RAS, TP53, WNT), plus `MutSig genes`, `OncoKB-CNAs-AMP`, `OncoKB-CNAs-HOMDEL` sheets
  that are ignored by this script. Each pathway sheet uses 14-15 columns including Gene,
  Aliases, OG/TSG, MutSig flag, GISTIC amp/del, Hotspots (AA#), 3D Hotspots, OncoKB
  copy-number / mutations, and OQL strings.

Output
------
- snakemake.output[0] : feather with one row per (pathway, gene), columns:
    pathway               (str)  — pathway name (normalized — e.g., "RTK_RAS", "TGF_BETA")
    gene                  (str)  — HGNC symbol
    og_tsg                (str)  — "OG" / "TSG" / "" per Sanchez-Vega annotation
    is_mutsig_driver      (bool) — Bailey MutSig flag
    has_gistic_amp        (bool) — present in GISTIC-amp column
    has_gistic_del        (bool) — present in GISTIC-del column
    hotspot_count         (int)  — number of 1D amino-acid hotspots reported
    hotspot_3d_count      (int)  — number of 3D-hotspot clusters reported
    source                (str)  — "SanchezVega2018"
"""

import sys
import warnings
from pathlib import Path

import pandas as pd

snek = snakemake  # type: ignore[name-defined]  # noqa: F821

input_path = Path(snek.input[0])
output_feather = snek.output[0]

# Sheets that are per-pathway gene templates; all others are ignored.
PATHWAY_SHEETS = {
    "Cell Cycle",
    "HIPPO",
    "MYC",
    "NOTCH",
    "NRF2",
    "PI3K",
    "TGF-Beta",
    "RTK RAS",
    "TP53",
    "WNT",
}


def _normalize_pathway_name(sheet_name: str) -> str:
    return sheet_name.strip().upper().replace("-", "_").replace(" ", "_")


def _count_residues(cell: object) -> int:
    """Count the number of AA residues / 3D hotspot clusters listed in a comma-separated cell."""
    if cell is None or (isinstance(cell, float) and pd.isna(cell)):
        return 0
    s = str(cell).strip()
    if not s or s.lower() == "nan":
        return 0
    return len([x for x in s.split(",") if x.strip()])


def _is_present(cell: object) -> bool:
    """True if the cell has any non-empty / non-NaN content."""
    if cell is None or (isinstance(cell, float) and pd.isna(cell)):
        return False
    s = str(cell).strip()
    return bool(s) and s.lower() != "nan"


# Some sheets in this supplement trigger openpyxl warnings about unknown Excel extensions
# that are harmless for our read.
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    sheets = pd.read_excel(input_path, sheet_name=None, engine="openpyxl")


def _locate_header_row(sheet_df: pd.DataFrame) -> int:
    """Return the row index containing the 'Gene' header, or -1 if not found.

    Some Sanchez-Vega sheets (e.g., Cell Cycle) carry a title row and a blank row before the
    real headers; other sheets have clean headers in row 0. Scan the first ~5 rows of the
    first column looking for a cell whose value is exactly "Gene".
    """
    if str(sheet_df.columns[0]).strip() == "Gene":
        return -1  # headers already in the column names
    for i in range(min(5, len(sheet_df))):
        if str(sheet_df.iloc[i, 0]).strip() == "Gene":
            return i
    return -2  # not found


frames: list[pd.DataFrame] = []
for sheet_name, sheet_df in sheets.items():
    if sheet_name not in PATHWAY_SHEETS:
        continue

    header_row = _locate_header_row(sheet_df)
    if header_row == -2:
        print(
            f"[skip] sheet {sheet_name!r}: could not locate 'Gene' header row",
            file=sys.stderr,
        )
        continue
    if header_row >= 0:
        sheet_df.columns = sheet_df.iloc[header_row].astype(str)
        sheet_df = sheet_df.iloc[header_row + 1 :].reset_index(drop=True)

    norm = {c: str(c).strip() for c in sheet_df.columns}
    sheet_df = sheet_df.rename(columns=norm)

    if "Gene" not in sheet_df.columns:
        print(
            f"[skip] sheet {sheet_name!r}: no 'Gene' column after header normalization",
            file=sys.stderr,
        )
        continue

    # Drop rows without a gene symbol.
    sheet_df = sheet_df[sheet_df["Gene"].astype(str).str.strip().str.len() > 0]

    def _column(name: str, default: object = None) -> pd.Series:
        """Return the named column as a Series, or a default-filled Series of the right length."""
        if name in sheet_df.columns:
            return sheet_df[name]
        return pd.Series([default] * len(sheet_df), index=sheet_df.index)

    out = pd.DataFrame(
        {
            "pathway": _normalize_pathway_name(sheet_name),
            "gene": sheet_df["Gene"].astype(str).str.strip().str.upper(),
            "og_tsg": _column("OG/TSG", "").astype(str).str.strip(),
            "is_mutsig_driver": _column("MutSig", 0).apply(
                lambda v: str(v).strip() == "1"
            ),
            "has_gistic_amp": _column("GISTIC amp").apply(_is_present),
            "has_gistic_del": _column("GISTIC del").apply(_is_present),
            "hotspot_count": _column("Hotspots (AA #)").apply(_count_residues),
            "hotspot_3d_count": _column("3D Hotspots (AA #)").apply(_count_residues),
        }
    )
    out["source"] = "SanchezVega2018"
    frames.append(out)

if not frames:
    raise RuntimeError(
        "No pathway sheets parsed from Sanchez-Vega 2018 Table S3. Verify sheet names match "
        "PATHWAY_SHEETS constant in this script."
    )

pathways = pd.concat(frames, ignore_index=True).drop_duplicates(
    subset=["pathway", "gene"]
)
pathways = pathways.reset_index(drop=True)
pathways.to_feather(output_feather)

print(
    f"Wrote {len(pathways)} (pathway, gene) rows across "
    f"{pathways['pathway'].nunique()} pathways to {output_feather}",
    file=sys.stderr,
)
