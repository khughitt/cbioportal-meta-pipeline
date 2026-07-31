---
id: t143
project: ''
title: Pre-bake dndscv into vendored conda env to remove install_github race
type: ''
aspects:
- software-development
priority: P3
status: proposed
blocked_by: []
related:
- task:t131
parent: ''
group: pipeline
artifacts: []
findings: []
created: '2026-04-26'
completed: null
---

**Issue.** `run_dndscv.R`'s self-bootstrap step (`remotes::install_github("im3sanger/dndscv@<sha>")`) races when called from parallel R processes that share the same conda env's R library. The smoke run 2026-04-25 hit this twice: the first parallel job to attempt install would succeed, but the second would error with `dndscv install_github reported success but namespace still missing` (RcppArmadillo install collision under the same library prefix). The race resolved itself on retry once dndscv was already installed in the env, but it makes the first fresh-env run flaky and bounds `-jN` parallelism for `run_dndscv_per_cancer` until the env warms up.

**Workarounds applied** so far: pre-installing `r-rcpp` and `r-rcpparmadillo` via conda (so they're not compiled from source under the install_github call). This narrows the race window but doesn't eliminate it.

**Real fix** options:
1. **Vendored dndscv tarball** — `code/envs/dndscv.yml` adds `r-dndscv` from a private conda channel built from a pinned dndscv tarball. Eliminates the bootstrap step entirely.
2. **Docker / Apptainer image** with dndscv pre-installed. Snakemake supports `container:` directives.
3. **File-system lock** in `run_dndscv.R`'s bootstrap function — `dir.create()` is atomic on POSIX; first process to create the lock dir does the install, others wait on a `.complete` marker.

**Acceptance**: a fresh `--use-conda` run with `-j8` does not hit the bootstrap race for `run_dndscv_per_cancer`.

**Cross-references**: identified during the t131 smoke run 2026-04-25 (commit `1dd1414` added the rcpparmadillo workaround).
