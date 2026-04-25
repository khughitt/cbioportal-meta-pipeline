# data/external/

Vendored upstream packages with no conda-forge / Bioconductor distribution.

## select_v1.6.4.tar.gz

CSOgroup/select R package, v1.6.4 (released 2024-11-26).

- Source: https://github.com/CSOgroup/select/archive/refs/tags/v1.6.4.tar.gz
- License: LGPL-3.0
- sha256 (12-char prefix): `1927b9880132`
- Re-derive: `uv run snakemake -s code/workflows/Snakefile -j1 \
  --configfile code/config/config-10k-genes.yml -- data/external/select_v1.6.4.tar.gz`

Used by `code/envs/select.yml` + rule (0) `preflight_select_env` per
`doc/plans/2026-04-25-t078-select-cooccurrence-design.md` Section 4.1.

Do not delete or modify. To upgrade, bump `SELECT_VERSION` + `SELECT_SHA256_PREFIX`
in `code/workflows/Snakefile`, re-run the rule, then update `code/envs/select.yml`
and `code/scripts/preflight_select_env.R` to match. Re-run validation
(Section 8 of the design doc).
