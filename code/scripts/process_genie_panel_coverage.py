"""
process_genie_panel_coverage.py

Builds a `(panel_id, gene_symbol, chromosome, start, end, length_bp)` table from the
`genomic_information.txt` file shipped with each AACR Project GENIE release.

Input
-----
- snakemake.input[0] : the GENIE release's `genomic_information.txt`.

  This is the authoritative per-panel coverage file in GENIE releases — one row per
  (panel, bait region, exon/intron), with columns
  `Chromosome, Start_Position, End_Position, Hugo_Symbol, ID, SEQ_ASSAY_ID, Feature_Type,
  includeInPanel, clinicalReported`.

  GENIE does **not** ship per-assay BED files; the coverage data is consolidated into this
  single file. Download the GENIE release from Synapse (e.g., `syn72382128` for v19.0-public;
  released quarterly) and place `genomic_information.txt` at `data/genie/genomic_information.txt`
  (or update the Snakemake rule's input path).

  Synapse auth + GENIE Data Use Agreement required for download. The `gene_panels/` subfolder
  on Synapse contains flat gene-name lists per panel (no coordinates) and is not used by this
  script.

Output
------
- snakemake.output[0] : feather file with columns
    panel_id    (str)  — SEQ_ASSAY_ID (panel identifier), e.g., "DFCI-ONCOPANEL-3"
    gene        (str)  — HGNC symbol (upper-cased)
    chromosome  (str)
    start       (int)  — 1-based start position (GENIE convention)
    end         (int)
    length_bp   (int)  — end - start + 1
    feature_type (str) — exon / intron / etc. (preserves the raw value from the input)
    included    (bool) — True if `includeInPanel == True`

Only rows with `includeInPanel == True` and a non-empty SEQ_ASSAY_ID and Hugo_Symbol are kept
in the output (GENIE releases include some summary rows that should be dropped).
"""
import sys

import pandas as pd

snek = snakemake  # type: ignore[name-defined]

input_path = snek.input[0]
output_feather = snek.output[0]

raw = pd.read_csv(input_path, sep="\t", dtype=str, na_filter=False)
required = {"Chromosome", "Start_Position", "End_Position", "Hugo_Symbol",
            "SEQ_ASSAY_ID", "Feature_Type", "includeInPanel"}
missing = required - set(raw.columns)
if missing:
    raise ValueError(
        f"Unexpected genomic_information.txt schema — missing columns: {sorted(missing)}. "
        f"Got: {list(raw.columns)}"
    )

panel_id = raw["SEQ_ASSAY_ID"].astype(str).str.strip()
gene = raw["Hugo_Symbol"].astype(str).str.strip().str.upper()
chromosome = raw["Chromosome"].astype(str).str.strip()
start = pd.to_numeric(raw["Start_Position"], errors="coerce")
end = pd.to_numeric(raw["End_Position"], errors="coerce")
feature_type = raw["Feature_Type"].astype(str).str.strip()
included = raw["includeInPanel"].astype(str).str.strip().str.lower().eq("true")

out = pd.DataFrame({
    "panel_id": panel_id,
    "gene": gene,
    "chromosome": chromosome,
    "start": start,
    "end": end,
    "feature_type": feature_type,
    "included": included,
})

# Drop summary / malformed rows: empty panel_id / gene, non-integer coords, or not included.
out = out.loc[
    (out["panel_id"].str.len() > 0)
    & (out["gene"].str.len() > 0)
    & out["start"].notna()
    & out["end"].notna()
    & out["included"],
].copy()
out["start"] = out["start"].astype(int)
out["end"] = out["end"].astype(int)
out["length_bp"] = out["end"] - out["start"] + 1

out = out[["panel_id", "gene", "chromosome", "start", "end", "length_bp",
           "feature_type", "included"]].reset_index(drop=True)
out.to_feather(output_feather)

print(
    f"Wrote {len(out)} (panel, gene, region) rows across "
    f"{out['panel_id'].nunique()} panels to {output_feather}",
    file=sys.stderr,
)
