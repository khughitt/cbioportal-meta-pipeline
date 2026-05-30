# science:code
# status: workflow-owned
# science:end
"""
process_cgc.py

Processes a COSMIC Cancer Gene Census (CGC) TSV into a tidy feather keyed by gene.

Input
-----
- snakemake.input[0] : CGC TSV download from https://cancer.sanger.ac.uk/cosmic/download.
  Expected columns include `Gene Symbol`, `Tier`, `Hallmark`, `Role in Cancer`,
  `Tumour Types(Somatic)`, `Tumour Types(Germline)`, `Molecular Genetics`, `Mutation Types`,
  etc.

  CGC version drift is slow (~5-15 gene changes per annual release). v100 (late 2023 / early
  2024) vs current releases differ by a handful of genes on the margins. The `cgc_source`
  column stamped onto downstream outputs records the exact input file path so re-runs against
  different versions are detectable.

Output
------
- snakemake.output[0] : feather keyed by (gene) with columns:
    gene                 (str)    — HGNC symbol (upper-cased)
    tier                 (int)    — 1 or 2
    hallmark             (bool)   — marked as a cancer Hallmark gene
    role_in_cancer       (str)    — "oncogene", "TSG", "fusion" (comma-separated if multiple)
    somatic              (bool)
    germline             (bool)
    tumour_types_somatic (str)    — raw comma-separated list from CGC
    mutation_types       (str)    — raw CGC mutation-type codes
    source               (str)    — "COSMIC-CGC"
"""

import sys
from pathlib import Path

import pandas as pd

snek = snakemake  # type: ignore[name-defined]  # noqa: F821

input_path = Path(snek.input[0])
output_feather = snek.output[0]

raw = pd.read_csv(input_path, sep="\t", dtype=str, na_filter=False)

required = {"Gene Symbol", "Tier", "Role in Cancer"}
missing = required - set(raw.columns)
if missing:
    raise ValueError(
        f"Unexpected CGC schema — missing columns: {sorted(missing)}. "
        f"Got: {list(raw.columns)}"
    )


def _bool(series_name: str, true_values: set[str] | None = None) -> pd.Series:
    vals = raw.get(series_name, pd.Series([""] * len(raw), index=raw.index))
    if true_values is None:
        true_values = {"yes", "y", "true", "1"}
    return vals.astype(str).str.strip().str.lower().isin(true_values)


def _str(series_name: str) -> pd.Series:
    vals = raw.get(series_name, pd.Series([""] * len(raw), index=raw.index))
    return vals.astype(str).str.strip()


tier_series = pd.to_numeric(raw["Tier"], errors="coerce")

out = pd.DataFrame(
    {
        "gene": raw["Gene Symbol"].astype(str).str.strip().str.upper(),
        "tier": tier_series.fillna(0).astype(int),
        "hallmark": _bool("Hallmark"),
        "role_in_cancer": _str("Role in Cancer"),
        "somatic": _bool("Somatic"),
        "germline": _bool("Germline"),
        "tumour_types_somatic": _str("Tumour Types(Somatic)"),
        "mutation_types": _str("Mutation Types"),
        "source": "COSMIC-CGC",
    }
)

# Drop rows without a gene symbol or valid tier.
out = out.loc[(out["gene"].str.len() > 0) & (out["tier"].isin([1, 2]))].copy()
out = out.drop_duplicates(subset=["gene"]).reset_index(drop=True)

out.to_feather(output_feather)
print(
    f"Wrote {len(out)} CGC genes to {output_feather} "
    f"(Tier 1: {(out['tier'] == 1).sum()}, Tier 2: {(out['tier'] == 2).sum()})",
    file=sys.stderr,
)
