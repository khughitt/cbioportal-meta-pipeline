# data/panels/

Sequencing-panel BEDs used by t078 (`build_panel_gene_sets.py`, rule 1a).

## Files

| File | Source | Notes |
|---|---|---|
| `IMPACT341.bed` | GENIE consolidated `genomic_information.txt` (`SEQ_ASSAY_ID=MSK-IMPACT341`) | derived |
| `IMPACT410.bed` | GENIE consolidated `genomic_information.txt` (`SEQ_ASSAY_ID=MSK-IMPACT410`) | derived |
| `IMPACT468.bed` | GENIE consolidated `genomic_information.txt` (`SEQ_ASSAY_ID=MSK-IMPACT468`) | derived |
| `IMPACT505.bed` | GENIE consolidated `genomic_information.txt` (`SEQ_ASSAY_ID=MSK-IMPACT505`) | derived |
| `F1.bed` | GENIE proxy `SEQ_ASSAY_ID=PROV-FOUNDATIONONELIQUIDCDX` | proxy; may be empty placeholder |
| `F1CDx.bed` | GENIE proxy `SEQ_ASSAY_ID=DUKE-F1-DX1` | proxy; may be empty placeholder |

GENIE has no pure FoundationOne F1/F1CDx assay. The closest available proxies are
mapped above. If pure Foundation Medicine BEDs become available, replace the
placeholders. Studies mapped to F1/F1CDx will reflect the proxy's gene coverage in
the panel-intersection callability mask — call this out in the headline run's
provenance notes.

## Format

4-column TSV, no header: `chrom`, `start`, `end`, `symbol`. `symbol` is the
HGNC-canonical gene symbol used by `Hugo_Symbol` in GENIE. Multiple rows per gene
are allowed (one per exon); rule 1a dedupes per `(panel_id, symbol)`.

## Regenerating

```bash
uv run snakemake -s code/workflows/Snakefile -j1 \
  --configfile code/config/config-10k-genes.yml -- build_panel_beds
```

Driven by `code/scripts/build_panel_beds.py` (rule `build_panel_beds`). Input:
`{data_dir}/genie/genomic_information.txt`.
