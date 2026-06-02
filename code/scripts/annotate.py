# science:code
# status: workflow-owned
# science:end
"""
annotate.py

Unified overlay-annotator for the cross-study gene x cancer mutation-frequency tables.
Applies all available reference-catalog overlays (Bailey 2018 drivers + COSMIC CGC +
Sanchez-Vega 2018 pathways) in one pass. Replaces the earlier chained `annotate_drivers.py`
pattern. The overlay logic lives in `annotate_lib.py` (importable + unit-tested); this file
is the thin Snakemake IO glue.

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
- `bailey2018_source`      (str)  — version stamp read from the Bailey feather's `source`
                                    column (e.g. "Bailey2018"), NOT a per-run path.
- `cgc_tier_1`             (bool)
- `cgc_tier_2`             (bool)
- `cgc_role_in_cancer`     (str)  — "oncogene", "TSG", "fusion" etc. (raw CGC value).
- `cgc_source`             (str)  — version stamp from the CGC feather's `source` column.
- `sanchez_vega_pathway`   (str)  — comma-separated if gene is in multiple pathways.
- `sanchez_vega_og_tsg`    (str)  — SV's OG/TSG call (from the first pathway sheet for the gene).
- `sanchez_vega_source`    (str)  — version stamp from the pathways feather's `source` column.

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

from annotate_lib import apply_overlays

snek = snakemake  # type: ignore[name-defined]  # noqa: F821

freq = pd.read_feather(Path(snek.input[0]))
bailey = pd.read_feather(Path(snek.input[1]))
cgc = pd.read_feather(Path(snek.input[2]))
pathways = pd.read_feather(Path(snek.input[3]))

freq = apply_overlays(freq, bailey, cgc, pathways)

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
