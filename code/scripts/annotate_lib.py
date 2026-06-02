# science:code
# status: library
# science:end
"""annotate_lib

Pure overlay-annotation logic for the cross-study gene x cancer mutation-frequency tables,
shared by the `annotate.py` Snakemake script. Applies the Bailey 2018 driver, COSMIC CGC,
and Sanchez-Vega 2018 pathway overlays in one pass.

Provenance (t106): each `*_source` column is a stable version stamp read from the reference
feather's own `source` column (set by the producer script, e.g. "Bailey2018"), NOT the
per-run output path the Snakemake rule writes to. Per-run paths change every run, break
reproducibility, and leak `out_dir` into a downstream data file.
"""

from __future__ import annotations

import pandas as pd


def source_stamp(ref: pd.DataFrame, name: str) -> str:
    """Return the single version stamp carried by a reference feather's ``source`` column.

    Fails loudly (no silent fallback) when the column is absent or carries more than one
    distinct value — both indicate a malformed reference artifact.
    """
    if "source" not in ref.columns:
        raise ValueError(
            f"{name} reference feather is missing the required 'source' column; "
            "cannot derive a provenance version stamp"
        )
    values = ref["source"].dropna().unique().tolist()
    if len(values) != 1:
        raise ValueError(
            f"{name} reference feather must carry exactly one 'source' value, "
            f"found {values!r}"
        )
    return str(values[0])


def apply_overlays(
    freq: pd.DataFrame,
    bailey: pd.DataFrame,
    cgc: pd.DataFrame,
    pathways: pd.DataFrame,
) -> pd.DataFrame:
    """Apply all reference-catalog overlays to a gene x cancer frequency table.

    Table-shape-agnostic: works on both the count table and the ratio table, which share
    the `(symbol, cancer_type)` key. Mutates and returns ``freq``.
    """
    gene_col = "symbol" if "symbol" in freq.columns else "gene"
    cancer_col = "cancer_type" if "cancer_type" in freq.columns else "cancer"

    g_upper = freq[gene_col].astype(str).str.upper()
    c_upper = freq[cancer_col].astype(str).str.upper()

    # --- Bailey 2018 overlay -------------------------------------------------
    driver_pairs = set(
        (bailey["gene"].str.upper() + "|" + bailey["cancer_type"].str.upper()).tolist()
    )
    pancan_drivers = set(
        bailey.loc[bailey["cancer_type"] == "PANCAN", "gene"].str.upper()
    )
    keys = g_upper + "|" + c_upper
    freq["bailey2018_driver"] = keys.isin(driver_pairs) | g_upper.isin(pancan_drivers)
    freq["bailey2018_source"] = source_stamp(bailey, "bailey2018")

    # --- COSMIC CGC overlay --------------------------------------------------
    cgc_by_gene = cgc.set_index("gene")
    freq["cgc_tier_1"] = g_upper.isin(cgc_by_gene.index[cgc_by_gene["tier"] == 1])
    freq["cgc_tier_2"] = g_upper.isin(cgc_by_gene.index[cgc_by_gene["tier"] == 2])
    freq["cgc_role_in_cancer"] = (
        g_upper.map(cgc_by_gene["role_in_cancer"].to_dict()).fillna("").astype(str)
    )
    freq["cgc_source"] = source_stamp(cgc, "cgc")

    # --- Sanchez-Vega 2018 pathway overlay -----------------------------------
    # A gene can appear in multiple pathways; concatenate them with commas.
    pathway_by_gene = (
        pathways.groupby("gene")["pathway"]
        .apply(lambda s: ",".join(sorted(set(s))))
        .to_dict()
    )
    # OG/TSG call per gene — first non-empty value across pathway rows for the same gene.
    og_tsg_by_gene = (
        pathways.loc[pathways["og_tsg"].astype(str).str.len() > 0]
        .drop_duplicates(subset=["gene"])
        .set_index("gene")["og_tsg"]
        .to_dict()
    )
    freq["sanchez_vega_pathway"] = g_upper.map(pathway_by_gene).fillna("").astype(str)
    freq["sanchez_vega_og_tsg"] = g_upper.map(og_tsg_by_gene).fillna("").astype(str)
    freq["sanchez_vega_source"] = source_stamp(pathways, "sanchez_vega")

    return freq
