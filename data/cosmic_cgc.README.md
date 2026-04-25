# data/cosmic_cgc.tsv

COSMIC Cancer Gene Census v100 (GRCh38).

- Source: /data/raw/cosmic/v100/Cosmic_CancerGeneCensus_v100_GRCh38.tsv (Sanger)
- Vendored at: 2026-04-25
- sha256 (12-char prefix): `abf3681d6d01`
- Re-derive: `uv run snakemake -s code/workflows/Snakefile -j1 \
  --configfile code/config/config-10k-genes.yml -- data/cosmic_cgc.tsv`
- Schema: tab-separated; primary column `Gene Symbol` (consumed by Task 5
  `build_select_gene_universe.py`).

To upgrade: replace the raw source file (or override `cosmic_cgc_raw_path` in
the config), bump `COSMIC_CGC_SHA256_PREFIX` in `code/workflows/Snakefile`,
re-run the rule, and bump `cgc_version` in the config block of
`code/config/config-10k-genes.yml`.
