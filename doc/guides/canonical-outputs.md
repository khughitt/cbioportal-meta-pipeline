# Canonical pipeline outputs

*As-of: 2026-04-13*

This guide documents which outputs in `summary/mut/table/` are intended for downstream
consumers vs which are intermediate artifacts. Closes audit finding F4
(`doc/audits/2026-04-13-create-combined-gene-cancer-freq-table-audit.md`).

## Canonical outputs (use these)

Both canonical outputs carry three **gene-level** overlays (Bailey / CGC / Sanchez-Vega) from a
single unified annotation step (`annotate.py`). The canonical ratio table additionally carries
the CH-aware annotations from `annotate_ch.py`.

| File | Annotation columns added |
|---|---|
| `gene_cancer_study_annotated.feather` | `bailey2018_driver`, `bailey2018_source`, `cgc_tier_1`, `cgc_tier_2`, `cgc_role_in_cancer`, `cgc_source`, `sanchez_vega_pathway`, `sanchez_vega_og_tsg`, `sanchez_vega_source` |
| `gene_cancer_study_ratio_annotated.feather` | all of the above, plus `ch_priority_gene`, `mean_matched`, `mean_unmatched`, `n_matched_studies`, `n_unmatched_studies` |

These are the **only** tables consumers should read for cross-study mutation-frequency claims.

### Overlay semantics

- **Bailey 2018** (`bailey2018_driver`): per-(gene, cancer_type) boolean. True if the (gene,
  cancer_type) pair is in Bailey's per-cancer roster OR if the gene is a Bailey pan-cancer
  driver (PANCAN). Closes the interpretation gap between "high frequency in our data" and
  "known driver."
- **COSMIC CGC** (`cgc_tier_1`, `cgc_tier_2`, `cgc_role_in_cancer`): per-gene (same across all
  cancer-type rows for a gene). Tier 1 = strong evidence (curated mechanism + mutation pattern);
  Tier 2 = weaker curated evidence. Role is the raw CGC string (`oncogene`, `TSG`, `fusion`, or
  combinations).
- **Sanchez-Vega 2018** (`sanchez_vega_pathway`, `sanchez_vega_og_tsg`): per-gene. Pathway is
  a comma-separated list when a gene is in multiple of the 10 canonical pathways (rare).
  `og_tsg` is SV's curated OG/TSG call.

### Two-source / three-source consensus

Consumers wanting higher-precision driver filters can combine overlays:
- `bailey2018_driver & cgc_tier_1` → high-confidence two-source consensus.
- `bailey2018_driver & cgc_tier_1 & (sanchez_vega_pathway != "")` → three-source intersection,
  including pathway-membership.

The un-annotated intermediates remain (`gene_cancer_study.feather`,
`gene_cancer_study_ratio.feather`, `gene_cancer_study_ratio_overlay_annotated.feather`) for
debugging / backward-compatibility, but should not be consumed for quantitative claims.

## Intermediate / raw outputs (do not consume directly)

| File | Reason it's intermediate |
|---|---|
| `gene_cancer_study.feather` | raw cross-study count table; **no driver overlay**, no CH-priority flag, no matched-normal stratification. Audit F4: consumers should switch to the `_annotated` version. |
| `gene_cancer_study_ratio.feather` | raw cross-study ratio table; same shortcomings as above. |
| `gene_cancer_study_ratio_bailey_annotated.feather` | intermediate in the chain — has Bailey overlay but not CH annotations. |

These remain in the pipeline output for backward-compatibility and debugging, but `rule all`
declares the canonical (`_annotated`) versions as the documented final outputs.

## Catalog versioning

The canonical outputs carry a `bailey2018_source` column recording which Bailey supplement
file was used for annotation (path/filename of the input xlsx). When OncoKB / CGC overlays
are added (tasks t051, t053), they will follow the same pattern: a `<catalog>_source` or
`<catalog>_version` column per overlay.

This addresses the OncoKB-version-drift concern documented in
`topic:cross-study-harmonization` and `topic:variant-interpretation-oncokb-vus`. Per
Suehnholz 2024, OncoKB Level 1/2 actionability rose 8.9% → 31.6% in 5 years on the same
cohort — any catalog overlay must be version-stamped to be longitudinally meaningful.

## Pipeline DAG (annotation chain)

```
gene_cancer_study.feather (raw num)
  └─→ annotate.py (unified overlay) ──→ gene_cancer_study_annotated.feather (canonical num)

gene_cancer_study_ratio.feather (raw ratio)
  └─→ annotate.py (unified overlay) ──→ gene_cancer_study_ratio_overlay_annotated.feather (intermediate)
        └─→ annotate_ch.py ──→ gene_cancer_study_ratio_annotated.feather (canonical ratio)

Reference feathers feeding into annotate.py:
  - metadata/bailey2018_drivers.feather        (from data/bailey2018_table_s1.tsv)
  - metadata/cgc_drivers.feather                (from data/cancer_gene_census.csv or cosmic_cgc_path)
  - metadata/sanchez_vega_pathways.feather      (from data/sanchez_vega_2018_tables_s3.xlsx)
```

The unified annotator applies all three gene-level overlays in a single pass (replaces the
earlier per-overlay chained-rules pattern). CH annotation chains off the overlay-annotated
ratio so the canonical ratio output carries both gene-level overlays AND CH stratification.
Changes to any reference feather or its upstream data file propagate through to the canonical
outputs.
