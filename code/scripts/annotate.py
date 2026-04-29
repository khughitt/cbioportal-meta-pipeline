"""
annotate.py

Unified overlay-annotator for the cross-study gene x cancer mutation-frequency tables.
Applies all available reference-catalog overlays (Bailey 2018 drivers + COSMIC CGC +
Sanchez-Vega 2018 pathways) in one pass. Replaces the earlier chained `annotate_drivers.py`
pattern.

Table-shape-agnostic: works on both the count table (`gene_cancer_study.feather`) and the
ratio table (`gene_cancer_study_ratio.feather`). Both have `(symbol, cancer_type)` keys; the
overlays add the same set of columns regardless.

Inputs
------
- snakemake.input[0] : the raw cross-study feather (count or ratio).
- snakemake.input[1] : Bailey 2018 drivers feather (from `process_bailey2018_drivers.py`).
- snakemake.input[2] : COSMIC CGC feather (from `process_cgc.py`).
- snakemake.input[3] : Sanchez-Vega 2018 pathways feather (from
  `process_sanchez_vega_pathways.py`).

Added columns
-------------
- `bailey2018_driver`      (bool) — True if (gene, cancer_type) in Bailey 2018 OR gene is a
                                    pan-cancer Bailey driver.
- `bailey2018_source`      (str)  — version-stamp (input file path).
- `cgc_tier_1`             (bool)
- `cgc_tier_2`             (bool)
- `cgc_role_in_cancer`     (str)  — "oncogene", "TSG", "fusion" etc. (raw CGC value).
- `cgc_source`             (str)
- `sanchez_vega_pathway`   (str)  — comma-separated if gene is in multiple pathways.
- `sanchez_vega_og_tsg`    (str)  — SV's OG/TSG call (from the first pathway sheet for the gene).
- `sanchez_vega_source`    (str)

Notes
-----
- Bailey's (gene, cancer) match is tumor-type-specific; CGC and Sanchez-Vega are gene-level,
  so their annotations are identical across all cancer-type rows for the same gene.
- Bailey cancer-type abbreviations (e.g., "BRCA") may or may not match the cancer-type values
  in our aggregation (cBioPortal uses its own taxonomy). When they don't match, the pan-cancer
  (Bailey's "PANCAN") annotation still applies, preserving at least a pan-cancer driver flag.
"""

import sys
from pathlib import Path

import pandas as pd

snek = snakemake  # type: ignore[name-defined]  # noqa: F821

freq_path = Path(snek.input[0])
bailey_path = Path(snek.input[1])
cgc_path = Path(snek.input[2])
pathway_path = Path(snek.input[3])

freq = pd.read_feather(freq_path)
bailey = pd.read_feather(bailey_path)
cgc = pd.read_feather(cgc_path)
pathways = pd.read_feather(pathway_path)

gene_col = "symbol" if "symbol" in freq.columns else "gene"
cancer_col = "cancer_type" if "cancer_type" in freq.columns else "cancer"

g_upper = freq[gene_col].astype(str).str.upper()
c_upper = freq[cancer_col].astype(str).str.upper()

# --- Bailey 2018 overlay -----------------------------------------------------
driver_pairs = set(
    (bailey["gene"].str.upper() + "|" + bailey["cancer_type"].str.upper()).tolist()
)
pancan_drivers = set(bailey.loc[bailey["cancer_type"] == "PANCAN", "gene"].str.upper())
keys = g_upper + "|" + c_upper
freq["bailey2018_driver"] = keys.isin(driver_pairs) | g_upper.isin(pancan_drivers)
freq["bailey2018_source"] = str(bailey_path)

# --- COSMIC CGC overlay ------------------------------------------------------
cgc_by_gene = cgc.set_index("gene")
freq["cgc_tier_1"] = g_upper.isin(cgc_by_gene.index[cgc_by_gene["tier"] == 1])
freq["cgc_tier_2"] = g_upper.isin(cgc_by_gene.index[cgc_by_gene["tier"] == 2])
freq["cgc_role_in_cancer"] = (
    g_upper.map(cgc_by_gene["role_in_cancer"].to_dict()).fillna("").astype(str)
)
freq["cgc_source"] = str(cgc_path)

# --- Sanchez-Vega 2018 pathway overlay ---------------------------------------
# A gene can appear in multiple pathways; concatenate them with commas.
pathway_by_gene = (
    pathways.groupby("gene")["pathway"]
    .apply(lambda s: ",".join(sorted(set(s))))
    .to_dict()
)
# OG/TSG call per gene — take the first non-empty value across pathway rows for the same gene.
og_tsg_by_gene = (
    pathways.loc[pathways["og_tsg"].astype(str).str.len() > 0]
    .drop_duplicates(subset=["gene"])
    .set_index("gene")["og_tsg"]
    .to_dict()
)
freq["sanchez_vega_pathway"] = g_upper.map(pathway_by_gene).fillna("").astype(str)
freq["sanchez_vega_og_tsg"] = g_upper.map(og_tsg_by_gene).fillna("").astype(str)
freq["sanchez_vega_source"] = str(pathway_path)

freq.to_feather(snek.output[0])

n_bailey = int(freq["bailey2018_driver"].sum())
n_cgc_t1 = int(freq["cgc_tier_1"].sum())
n_cgc_t2 = int(freq["cgc_tier_2"].sum())
n_pathway = int((freq["sanchez_vega_pathway"].astype(str).str.len() > 0).sum())
print(
    f"Annotated {len(freq)} rows: {n_bailey} bailey / {n_cgc_t1} cgc-T1 / "
    f"{n_cgc_t2} cgc-T2 / {n_pathway} sanchez-vega-pathway hits",
    file=sys.stderr,
)
