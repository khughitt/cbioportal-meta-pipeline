---
type: plan
title: t078 SELECT co-occurrence pipeline implementation plan
status: draft
created: '2026-04-25'
updated: '2026-06-28'
id: plan:0004-t078-select-cooccurrence-implementation-plan
related:
- task:t078
---

# t078 SELECT co-occurrence pipeline — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: use `superpowers:subagent-driven-development`
> (recommended) or `superpowers:executing-plans` to implement this plan task-by-task.
> Steps use checkbox (`- [ ]`) syntax for tracking. Read the design first:
> `doc/plans/2026-04-25-t078-select-cooccurrence-design.md`. Read it again whenever a
> task references "the design" — it has all the rationale and the upstream column
> mapping that the steps below assume.

**Goal:** Implement the seven-rule SELECT-based cross-study co-occurrence /
mutual-exclusivity pipeline specified in
`doc/plans/2026-04-25-t078-select-cooccurrence-design.md`. Deliverables: three headline
feathers (`gene_pair_select`, `pathway_aggregated`, `pathway_rollup_gene_pairs`), one
sibling annotation feather, all gated behind `config["select"]["enabled"]`.
This plan implements `task:t078`.

**Architecture:** Snakemake DAG: rule (0) preflight smoke test → rules (1a)/(1b)
panel/universe artifacts → rule (2) per-cell GAM construction (Python, fan-out) → rule
(3) per-cell SELECT (R, fan-in) and rule (5) pathway-aggregated SELECT (R, parallel) →
rule (4) cross-cell aggregation (Python). Sentinel feathers for skipped cells; vendored
SELECT tarball with no network fallback.

**Tech Stack for `task:t078`:** Python 3.13 (pandas, pyarrow, click, rich, scipy.stats for Stouffer +
BH), R 4.4 (CSOgroup/select v1.6.4, arrow), Snakemake 9, pytest + pyfakefs for Python
unit tests, conda-forge + bioconda for env. uv for Python deps. No new top-level
Python deps required (pandas / pyarrow / scipy / click / rich are already present).

---

## File structure

### New files

```
code/envs/select.yml                                       # Conda env (R + arrow)
data/external/select_v1.6.4.tar.gz                         # Vendored SELECT package
data/panels/IMPACT341.bed                                  # Panel BEDs (committed)
data/panels/IMPACT410.bed
data/panels/IMPACT468.bed
data/panels/IMPACT505.bed
data/panels/F1.bed
data/panels/F1CDx.bed
data/study_panels.tsv                                      # Non-GENIE non-WES fallback

code/scripts/preflight_select_env.R                        # Rule 0
code/scripts/build_select_gene_universe.py                 # Rule 1b
code/scripts/build_panel_gene_sets.py                      # Rule 1a
code/scripts/select_lib.py                                 # Shared helpers (Python)
code/scripts/build_select_gam.py                           # Rule 2
code/scripts/run_select.R                                  # Rule 3
code/scripts/run_select_pathway_aggregated.R              # Rule 5
code/scripts/aggregate_select_results.py                   # Rule 4

code/scripts/tests/test_build_select_gene_universe.py
code/scripts/tests/test_build_panel_gene_sets.py
code/scripts/tests/test_select_lib.py
code/scripts/tests/test_build_select_gam.py
code/scripts/tests/test_aggregate_select_results.py
code/scripts/tests/test_run_select_wrapper.R              # testthat
code/scripts/tests/test_check_known_biology.py
code/scripts/tests/data/select_toy/                        # Toy integration data
```

### Modified files

```
code/scripts/create_combined_sample_table.py               # Add sample_panel_map output
code/workflows/Snakefile                                   # Add 7 new rules + opt-in gating
code/config/config-10k-genes.yml                           # Add select: block
```

### File responsibilities

- **`select_lib.py`** — small shared module: `build_sample_class()` compound-label
  builder, `apply_callability_mask()` panel-intersection, `apply_cohort_filter()` for
  CH/hypermutator drops, `bh_fdr_within_groups()` BH-FDR helper, `signed_stouffer()`
  weighted-Z combiner. Keeps each per-rule script lean.
- **`build_*.py`** scripts — one rule, one script. Each script's `if __name__ == ...`
  block reads `snakemake.input/.output/.params` and calls into `select_lib` helpers.
- **`run_select*.R`** scripts — thin wrappers around `select::select(...)` per the
  design Section 4.5/4.7 contract. Sentinel passthrough is the only "logic" they own.
- **`aggregate_select_results.py`** — single Python script that consumes all per-cell
  feathers and produces all four aggregate outputs.

---

## Conventions for every task in this plan

1. **TDD.** Every Python task: write the failing test first, run it to confirm it
   fails for the right reason, write the minimal implementation, run the test to
   confirm it passes, commit.
2. **Test location:** `code/scripts/tests/test_<script_name>.py` matching the project
   convention. R tests use `testthat`; placed in
   `code/scripts/tests/test_<script_name>.R`.
3. **Test runner:** Python: `uv run --frozen pytest code/scripts/tests/<file> -v`. R:
   `uv run --frozen Rscript code/scripts/tests/<file>` after the conda env exists.
4. **Lint:** after each implementation step, run `uv run --frozen ruff check
   code/scripts/<file>.py` and `uv run --frozen ruff format code/scripts/<file>.py`.
   Fix any failures inline before committing.
5. **Commits:** one commit per task (the final step). Use the existing project commit
   convention (commitlint with `docs:`/`feat:`/`test:`/`fix:`/etc. types). Tasks below
   show the exact commit command for their final step.
6. **No emoji in code.** No `print()` for debug — use `rich.print` or `logging`.
7. **Type hints required.** Use modern syntax: `list[str]`, `dict[str, int]`,
   `str | None`, `Literal[...]`.
8. **Line length 120.** Existing AGENTS.md rule.
9. **uv only.** Never `pip install`. Add deps via `uv add`.

---

## Task summary

| # | Task | Phase |
|---|---|---|
| 1 | Vendor SELECT v1.6.4 tarball + commit | 0 (infra) |
| 2 | Create `code/envs/select.yml` conda env | 0 (infra) |
| 3 | Vendor panel BEDs + `data/study_panels.tsv` | 0 (infra) |
| 4 | Implement rule (0) `preflight_select_env.R` + Snakefile wiring | 0 |
| 5 | Implement rule (1b) `build_select_gene_universe.py` | 1 |
| 6 | Implement rule (1a) `build_panel_gene_sets.py` | 1 |
| 7 | Extend `create_combined_sample_table.py` for `sample_panel_map.feather` | 1 |
| 8 | Implement `select_lib.py` shared helpers | 2 |
| 9 | Implement rule (2) `build_select_gam.py` — core B-tier cell | 2 |
| 10 | Extend rule (2) — A-tier scattering + sentinel skips | 2 |
| 11 | Extend rule (2) — pathway-aggregated sibling GAM | 2 |
| 12 | Implement rule (3) `run_select.R` wrapper | 3 |
| 13 | Implement rule (5) `run_select_pathway_aggregated.R` | 3 |
| 14 | Implement rule (4) `aggregate_select_results.py` — B-tier concat + BH-FDR | 4 |
| 15 | Extend rule (4) — A-tier signed Stouffer | 4 |
| 16 | Extend rule (4) — union-join + 7-category concordance flag | 4 |
| 17 | Extend rule (4) — pathway rollup + sibling annotation | 4 |
| 18 | Wire all rules into Snakefile + add `select:` config block | 5 |
| 19 | Add toy integration test data + DAG dry-run test | 5 |
| 20 | Add biological positive-control regression test | 6 |

(Continued in subsequent sections — tasks are defined below, one section per task.)

---

## Task 1: Vendor SELECT v1.6.4 tarball

**Why:** The design requires a single, reproducible SELECT install path with no network
fallback (design risk #2). Vendoring the upstream v1.6.4 source tarball into the repo
makes the install offline-able and stable against upstream repo deletion. The download
recipe is captured as a Snakemake rule (`fetch_select_tarball`) so the artifact is fully
reproducible — `git clean` can wipe `data/external/` and a single `snakemake` invocation
restores it bit-for-bit (sha256-verified).

**Files:**
- Create: `data/external/select_v1.6.4.tar.gz`
- Create: `data/external/README.md` (one-paragraph note: source URL, sha256, license)
- Modify: `code/workflows/Snakefile` — add `rule fetch_select_tarball`

- [ ] **Step 1: Add `rule fetch_select_tarball` to the Snakefile**

Append to `code/workflows/Snakefile` (alongside the existing manual-prereq rules like
`process_bailey2018_drivers`):

```python
#
# t078 SELECT pipeline — vendored upstream R package.
#
# Downloads the v1.6.4 source tarball from the public GitHub release and
# verifies its sha256 prefix. The artifact is committed to the repo so this
# rule normally never runs; it exists so the download recipe is reproducible
# (e.g., after `git clean -xdf data/external/` the rule restores the file
# byte-for-byte). To upgrade, bump SELECT_VERSION + SELECT_SHA256_PREFIX and
# re-run.
#
SELECT_VERSION = "1.6.4"
SELECT_SHA256_PREFIX = "<TBD-after-first-download>"   # 12-char prefix

rule fetch_select_tarball:
  output:
    "data/external/select_v{version}.tar.gz".format(version=SELECT_VERSION)
  params:
    url=lambda wc: (
      f"https://github.com/CSOgroup/select/archive/refs/tags/v{SELECT_VERSION}.tar.gz"
    ),
    expected_sha256_prefix=SELECT_SHA256_PREFIX,
  shell:
    r"""
    mkdir -p $(dirname {output})
    curl -sSfL {params.url} -o {output}.tmp
    actual=$(sha256sum {output}.tmp | cut -c1-12)
    if [ "{params.expected_sha256_prefix}" != "<TBD-after-first-download>" ] && \
       [ "$actual" != "{params.expected_sha256_prefix}" ]; then
      echo "ERROR: sha256 mismatch for {output}" >&2
      echo "  expected prefix: {params.expected_sha256_prefix}" >&2
      echo "  actual prefix:   $actual" >&2
      rm -f {output}.tmp
      exit 1
    fi
    file {output}.tmp | grep -q "gzip compressed" || (
      echo "ERROR: download is not a gzip tarball (likely an HTML error page)" >&2
      rm -f {output}.tmp
      exit 1
    )
    mv {output}.tmp {output}
    """
```

- [ ] **Step 2: Run the rule once to populate the artifact**

```bash
uv run snakemake -s code/workflows/Snakefile -j1 \
  --configfile code/config/config-10k-genes.yml \
  data/external/select_v1.6.4.tar.gz
```

Expected: file size ~few hundred KB. Verify with
`ls -lh data/external/select_v1.6.4.tar.gz` and
`file data/external/select_v1.6.4.tar.gz` (should report "gzip compressed data").

- [ ] **Step 3: Record the sha256 prefix and pin it in the Snakefile**

```bash
sha256sum data/external/select_v1.6.4.tar.gz | cut -c1-12
```

Edit the `SELECT_SHA256_PREFIX = "<TBD-after-first-download>"` line in
`code/workflows/Snakefile` and replace the placeholder with the 12-char prefix.
This pins future re-downloads to the verified bytes.

- [ ] **Step 4: Write `data/external/README.md`**

```markdown
# data/external/

Vendored upstream packages with no conda-forge / Bioconductor distribution.

## select_v1.6.4.tar.gz

CSOgroup/select R package, v1.6.4 (released 2024-11-26).

- Source: https://github.com/CSOgroup/select/archive/refs/tags/v1.6.4.tar.gz
- License: LGPL-3.0
- sha256 (12-char prefix): `<insert-from-step-3>`
- Re-derive: `uv run snakemake -s code/workflows/Snakefile -j1 \
  --configfile code/config/config-10k-genes.yml data/external/select_v1.6.4.tar.gz`

Used by `code/envs/select.yml` + rule (0) `preflight_select_env` per
`doc/plans/2026-04-25-t078-select-cooccurrence-design.md` Section 4.1.

Do not delete or modify. To upgrade, bump `SELECT_VERSION` + `SELECT_SHA256_PREFIX`
in `code/workflows/Snakefile`, re-run the rule, then update `code/envs/select.yml`
and `code/scripts/preflight_select_env.R` to match. Re-run validation
(Section 8 of the design doc).
```

- [ ] **Step 5: Commit**

```bash
git add data/external/select_v1.6.4.tar.gz data/external/README.md \
        code/workflows/Snakefile
git commit -m "$(cat <<'EOF'
chore(t078): vendor CSOgroup/select v1.6.4 source tarball

Pinned vendoring per design doc risk #2 (no network fallback for the
SELECT install path). Adds data/external/select_v1.6.4.tar.gz plus a
README capturing source URL, sha256, and license. Adds a Snakemake
rule `fetch_select_tarball` so the artifact can be restored byte-for-byte
from upstream after a clean (sha256-verified).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: Create `code/envs/select.yml` conda env file

**Why:** Snakemake's `conda:` directive needs an env file. Per design Section 4.8 the
env contains R + arrow + minor deps but **NO `r-devtools` and NO `r-remotes`** — the
only SELECT install path is the vendored tarball, hard-coded in rule (0).

**Files:**
- Create: `code/envs/select.yml`
- Create: `code/scripts/tests/test_select_env_file.py`

- [ ] **Step 1: Write the failing test**

```python
# code/scripts/tests/test_select_env_file.py
"""Smoke tests for the SELECT conda env file."""
from pathlib import Path

import yaml

ENV_PATH = Path(__file__).resolve().parents[3] / "code" / "envs" / "select.yml"


def test_env_file_exists():
    assert ENV_PATH.exists(), f"missing {ENV_PATH}"


def test_env_is_valid_yaml():
    with ENV_PATH.open() as f:
        data = yaml.safe_load(f)
    assert isinstance(data, dict)
    assert "name" in data
    assert "channels" in data
    assert "dependencies" in data


def test_env_pins_r44():
    with ENV_PATH.open() as f:
        data = yaml.safe_load(f)
    deps = data["dependencies"]
    r_base_pins = [d for d in deps if isinstance(d, str) and d.startswith("r-base")]
    assert r_base_pins, "must pin r-base"
    # Accept r-base=4.4 or r-base>=4.4
    assert any("4.4" in d for d in r_base_pins), f"must pin R 4.4, got {r_base_pins}"


def test_env_has_arrow():
    with ENV_PATH.open() as f:
        data = yaml.safe_load(f)
    assert any(d == "r-arrow" or (isinstance(d, str) and d.startswith("r-arrow"))
               for d in data["dependencies"]), "must include r-arrow for feather I/O"


def test_env_excludes_devtools_and_remotes():
    """Design Section 4.8: tarball is the only install path; no devtools/remotes."""
    with ENV_PATH.open() as f:
        data = yaml.safe_load(f)
    deps = [d for d in data["dependencies"] if isinstance(d, str)]
    forbidden = {"r-devtools", "r-remotes"}
    found = forbidden & set(deps)
    assert not found, (
        f"must NOT include {found} — only install path is the vendored tarball "
        f"(design Section 4.8)"
    )
```

- [ ] **Step 2: Run test to verify it fails**

```bash
uv run --frozen pytest code/scripts/tests/test_select_env_file.py -v
```

Expected: FAIL on `test_env_file_exists` (env file does not yet exist).

- [ ] **Step 3: Write the env file**

```yaml
# code/envs/select.yml
#
# Conda env for the t078 SELECT co-occurrence / mutual-exclusivity pipeline.
# Used by rules (0), (3), (5) in code/workflows/Snakefile.
#
# CSOgroup/select v1.6.4 itself is NOT installed here. It is installed into the
# active env's R library by rule (0) `preflight_select_env` from the vendored
# tarball at data/external/select_v1.6.4.tar.gz. Per design Section 4.8 there is
# NO `r-devtools` and NO `r-remotes` here — the vendored tarball is the only
# install path. If you find yourself wanting to add either dep, read the design
# doc risk #2 first.
#
# First-time env build is ~5-15 min on a warm conda cache.
name: select-t078
channels:
  - conda-forge
  - bioconda
dependencies:
  - r-base=4.4
  - r-arrow
  - r-igraph
  - r-rcppparallel
  - r-data.table
  - r-tidyverse
  - r-jsonlite
  - r-testthat
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
uv run --frozen pytest code/scripts/tests/test_select_env_file.py -v
```

Expected: 5 PASS.

- [ ] **Step 5: Commit**

```bash
git add code/envs/select.yml code/scripts/tests/test_select_env_file.py
git commit -m "$(cat <<'EOF'
feat(t078): add code/envs/select.yml conda env for SELECT pipeline

R 4.4 + arrow + minimal deps. Excludes devtools/remotes per design
Section 4.8 — vendored tarball is the only SELECT install path. Smoke
tests in test_select_env_file.py pin r-base 4.4, require r-arrow, and
forbid devtools/remotes.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: Vendor panel BEDs + `data/study_panels.tsv`

**Why:** Rule (1a) needs panel BED files on disk. The design enumerates IMPACT 341/410/
468/505 plus FoundationOne F1/F1CDx. We commit them as small reference data (each is
10–50 KB). `data/study_panels.tsv` is the fallback per-study panel mapping for non-GENIE
non-WES studies.

**Files:**
- Create: `data/panels/IMPACT341.bed`, `IMPACT410.bed`, `IMPACT468.bed`, `IMPACT505.bed`
- Create: `data/panels/F1.bed`, `data/panels/F1CDx.bed`
- Create: `data/panels/README.md`
- Create: `data/study_panels.tsv`
- Create: `code/scripts/build_panel_beds.py`
- Create: `code/scripts/tests/test_panel_beds.py`
- Modify: `code/workflows/Snakefile` — add `rule build_panel_beds`

- [ ] **Step 1a: Write `code/scripts/build_panel_beds.py`**

Lift the inline heredoc into a real script so the rule has a `script:` target. Use
the `snakemake.input/.output` pattern matching other scripts in `code/scripts/`.

```python
"""Derive per-panel BED files from the GENIE consolidated genomic_information.txt.

Snakemake-driven: input is the GENIE consolidated assay BED, output is one BED
per panel listed in PANEL_TO_ASSAY (MSK-IMPACT 341/410/468/505 and the F1/F1CDx
proxies). Empty placeholder files are written for assays absent from the GENIE
release so downstream rules see a stable file set.

The output BEDs are 4-column TSV (chrom, start, end, symbol) with no header, one
row per (assay × exon interval). Multiple rows per gene are expected; rule (1a)
deduplicates per (panel_id, symbol).
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
from rich import print as rprint

# GENIE assay id -> output BED path (relative to repo root).
# F1/F1CDx are proxies, not pure Foundation Medicine BEDs — see data/panels/README.md.
PANEL_TO_ASSAY: dict[str, str] = {
    "MSK-IMPACT341": "data/panels/IMPACT341.bed",
    "MSK-IMPACT410": "data/panels/IMPACT410.bed",
    "MSK-IMPACT468": "data/panels/IMPACT468.bed",
    "MSK-IMPACT505": "data/panels/IMPACT505.bed",
    "DUKE-F1-DX1": "data/panels/F1CDx.bed",
    "PROV-FOUNDATIONONELIQUIDCDX": "data/panels/F1.bed",
}


def build_panel_beds(genie_genomic_info: Path, out_paths: dict[str, Path]) -> None:
    """Write one BED per assay in PANEL_TO_ASSAY from the consolidated GENIE file."""
    if not genie_genomic_info.exists():
        raise FileNotFoundError(f"GENIE genomic_information.txt missing: {genie_genomic_info}")

    df = pd.read_csv(genie_genomic_info, sep="\t", dtype={"Chromosome": "string"})
    df = df[df["includeInPanel"].fillna(True).astype(bool)]
    df = df[df["Feature_Type"] == "exon"]

    for assay, out in out_paths.items():
        out.parent.mkdir(parents=True, exist_ok=True)
        sub = df[df["SEQ_ASSAY_ID"] == assay]
        if sub.empty:
            out.write_text("")
            rprint(f"[yellow]WARN[/]: no rows for {assay}; wrote empty placeholder {out}")
            continue
        bed = sub[["Chromosome", "Start_Position", "End_Position", "Hugo_Symbol"]].copy()
        bed.columns = ["chrom", "start", "end", "symbol"]
        bed.to_csv(out, sep="\t", index=False, header=False)
        rprint(f"wrote {out}: {len(bed)} intervals, {bed['symbol'].nunique()} symbols")


if __name__ == "__main__":
    # Snakemake entry point.
    src = Path(snakemake.input[0])  # type: ignore[name-defined]  # noqa: F821
    out_paths = {assay: Path(p) for assay, p in zip(PANEL_TO_ASSAY, snakemake.output)}  # type: ignore[name-defined]  # noqa: F821
    build_panel_beds(src, out_paths)
```

- [ ] **Step 1b: Add `rule build_panel_beds` to the Snakefile**

Append to `code/workflows/Snakefile`:

```python
#
# t078 SELECT pipeline — per-panel BED files derived from GENIE.
#
# Manual prereq: the GENIE consolidated genomic_information.txt at
# {data_dir}/genie/genomic_information.txt (Synapse-gated upstream — see AGENTS.md
# "External Reference Datasets"). Downstream rule (1a) consumes the per-panel BEDs.
#
rule build_panel_beds:
  input:
    data_dir.joinpath("genie/genomic_information.txt")
  output:
    "data/panels/IMPACT341.bed",
    "data/panels/IMPACT410.bed",
    "data/panels/IMPACT468.bed",
    "data/panels/IMPACT505.bed",
    "data/panels/F1CDx.bed",
    "data/panels/F1.bed",
  script:
    "../scripts/build_panel_beds.py"
```

(The script's `PANEL_TO_ASSAY` dict ordering matches the rule's `output:` order so
`zip(PANEL_TO_ASSAY, snakemake.output)` lines up assay → path. If you reorder one,
reorder both.)

- [ ] **Step 1c: Run the rule once to populate the BEDs**

```bash
uv run snakemake -s code/workflows/Snakefile -j1 \
  --configfile code/config/config-10k-genes.yml \
  build_panel_beds
```

Expected: six files under `data/panels/`. The four MSK-IMPACT panels should each
have ~341/410/468/505 unique symbols (subject to ±some slack for the test in step 2).
F1/F1CDx may be empty if those GENIE assay IDs are absent from the local consolidated
file — the script writes empty placeholders so the file paths exist.

The proxy F1/F1CDx mapping is documented in `data/panels/README.md`. If the project
later acquires pure Foundation Medicine BEDs, these placeholders should be replaced.
For studies mapped to the F1/F1CDx proxy panels, the panel-intersection callability
mask will reflect the proxy's gene coverage — call this out in the headline run's
provenance notes.

- [ ] **Step 2: Write the failing test**

```python
# code/scripts/tests/test_panel_beds.py
"""Sanity checks on vendored panel BEDs."""
from pathlib import Path

import pandas as pd
import pytest

PANELS_DIR = Path(__file__).resolve().parents[3] / "data" / "panels"
EXPECTED_PANELS = [
    "IMPACT341", "IMPACT410", "IMPACT468", "IMPACT505",
    "F1", "F1CDx",
]
BED_COLS = ["chrom", "start", "end", "symbol"]


def test_panels_dir_exists():
    assert PANELS_DIR.is_dir()


@pytest.mark.parametrize("name", EXPECTED_PANELS)
def test_panel_bed_present(name):
    p = PANELS_DIR / f"{name}.bed"
    assert p.exists(), f"missing {p}"


@pytest.mark.parametrize("name", EXPECTED_PANELS)
def test_panel_bed_has_required_columns(name):
    p = PANELS_DIR / f"{name}.bed"
    df = pd.read_csv(p, sep="\t", header=None, names=BED_COLS)
    if df.empty:
        pytest.skip(f"{name} bed is empty placeholder — see data/panels/README.md")
    for c in BED_COLS:
        assert c in df.columns


@pytest.mark.parametrize("name", ["IMPACT341", "IMPACT410", "IMPACT468", "IMPACT505"])
def test_msk_impact_panel_size_in_range(name):
    """MSK-IMPACT panels should have between 300 and 600 unique symbols."""
    p = PANELS_DIR / f"{name}.bed"
    df = pd.read_csv(p, sep="\t", header=None, names=BED_COLS)
    n_symbols = df["symbol"].nunique()
    assert 300 <= n_symbols <= 600, (
        f"{name} has {n_symbols} symbols; expected ~341/410/468/505 ± slack"
    )


def test_study_panels_tsv():
    f = PANELS_DIR.parent / "study_panels.tsv"
    assert f.exists(), f"missing {f}"
    df = pd.read_csv(f, sep="\t")
    for c in ["study_id", "panel_id", "sequencing_type"]:
        assert c in df.columns
    assert (df["sequencing_type"].isin(["wes", "panel"])).all()
```

- [ ] **Step 3: Write `data/study_panels.tsv` and `data/panels/README.md`**

```tsv
study_id	panel_id	sequencing_type
brca_tcga	wes	wes
coadread_tcga	wes	wes
luad_tcga	wes	wes
gbm_tcga	wes	wes
lgg_tcga	wes	wes
skcm_tcga	wes	wes
msk_impact_2017	msk_impact_410	panel
```

(Add rows for every non-GENIE study in `code/config/config-10k-genes.yml` `studies:`.
For studies whose panel is not yet known, add them with `panel_id="UNKNOWN"`; rule
(1a) will fail loudly on those, which is the desired behaviour per the
"fail-early" rule.)

```markdown
# data/panels/

Sequencing-panel BEDs used by t078 (`build_panel_gene_sets.py`, rule 1a).

## Files

| File | Source | Notes |
|---|---|---|
| `IMPACT341.bed` | GENIE v9.1 `MSK-IMPACT341/genomic_information.txt` | derived |
| `IMPACT410.bed` | GENIE v9.1 `MSK-IMPACT410/genomic_information.txt` | derived |
| `IMPACT468.bed` | GENIE v9.1 `MSK-IMPACT468/genomic_information.txt` | derived |
| `IMPACT505.bed` | GENIE v9.1 `MSK-IMPACT505/genomic_information.txt` | derived |
| `F1.bed` | Foundation Medicine — manual prerequisite | may be empty placeholder |
| `F1CDx.bed` | Foundation Medicine — manual prerequisite | may be empty placeholder |

## Format

4-column TSV, no header: `chrom`, `start`, `end`, `symbol`. `symbol` is the
HGNC-canonical gene symbol used by `Hugo_Symbol` in GENIE. Multiple rows per gene
are allowed (one per exon); rule 1a dedupes per `(panel_id, symbol)`.

## Regenerating MSK-IMPACT BEDs

See the script in the t078 implementation plan, Task 3 step 1.
```

- [ ] **Step 4: Run tests to verify they pass (or skip gracefully)**

```bash
uv run --frozen pytest code/scripts/tests/test_panel_beds.py -v
```

Expected: all PASS, or F1/F1CDx PASS-skip if empty placeholders.

- [ ] **Step 5: Commit**

```bash
git add data/panels/ data/study_panels.tsv \
        code/scripts/build_panel_beds.py \
        code/scripts/tests/test_panel_beds.py \
        code/workflows/Snakefile
git commit -m "$(cat <<'EOF'
chore(t078): vendor panel BEDs + data/study_panels.tsv

MSK-IMPACT 341/410/468/505 BEDs derived from the GENIE consolidated
genomic_information.txt via a new Snakemake rule build_panel_beds (script
code/scripts/build_panel_beds.py). F1/F1CDx vendored from Foundation
Medicine if available, empty placeholder otherwise. data/study_panels.tsv
is the non-GENIE non-WES fallback per-study mapping consumed by Task 7.
Sanity tests assert MSK-IMPACT panel sizes within expected ranges.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: Implement rule (0) `preflight_select_env.R` + Snakefile wiring

**Why:** Rule (0) is the gate that installs SELECT from the vendored tarball, runs a
smoke test on `luad_data`, and writes a token that all other SELECT rules depend on.
Failing fast here saves ~hours of fan-out compute when something is broken upstream.

**Files:**
- Create: `code/scripts/preflight_select_env.R`
- Modify: `code/workflows/Snakefile` (add rule + opt-in gating)
- Create: `code/scripts/tests/test_preflight_select_env.py` (Python-side smoke test on
  the rule definition; the R-side test is the rule itself)

- [ ] **Step 1: Write the failing Python-side test**

```python
# code/scripts/tests/test_preflight_select_env.py
"""Verifies rule (0) is wired into the Snakefile correctly."""
from pathlib import Path
import re

SNAKEFILE = Path(__file__).resolve().parents[3] / "code" / "workflows" / "Snakefile"


def test_snakefile_declares_preflight_rule():
    text = SNAKEFILE.read_text()
    assert "rule preflight_select_env:" in text


def test_preflight_rule_uses_select_conda_env():
    text = SNAKEFILE.read_text()
    block = _extract_rule_block(text, "preflight_select_env")
    assert "code/envs/select.yml" in block, "must use code/envs/select.yml"


def test_preflight_rule_consumes_vendored_tarball():
    text = SNAKEFILE.read_text()
    block = _extract_rule_block(text, "preflight_select_env")
    assert "data/external/select_v1.6.4.tar.gz" in block


def test_preflight_rule_writes_token():
    text = SNAKEFILE.read_text()
    block = _extract_rule_block(text, "preflight_select_env")
    assert ".preflight_ok" in block


def _extract_rule_block(text: str, rule_name: str) -> str:
    """Return the source of one rule block (rule_name + indented body)."""
    lines = text.splitlines()
    out: list[str] = []
    in_rule = False
    for line in lines:
        if line.startswith(f"rule {rule_name}:"):
            in_rule = True
            out.append(line)
            continue
        if in_rule:
            if line and not line.startswith((" ", "\t")):
                break
            out.append(line)
    assert out, f"rule {rule_name} not found"
    return "\n".join(out)
```

- [ ] **Step 2: Run test to verify it fails**

```bash
uv run --frozen pytest code/scripts/tests/test_preflight_select_env.py -v
```

Expected: 4 FAIL on missing rule definition.

- [ ] **Step 3: Write `code/scripts/preflight_select_env.R`**

```r
# code/scripts/preflight_select_env.R
#
# Rule (0) for the t078 SELECT pipeline. See
# doc/plans/2026-04-25-t078-select-cooccurrence-design.md Section 4.1.
#
# 1. Install CSOgroup/select v1.6.4 from the vendored tarball into the active
#    R library. Idempotent: if already installed at the right version, skip.
# 2. Smoke-test the install by calling select::select() on the package's
#    bundled luad_data with n.permut = 50.
# 3. Verify the result has every column the project's wrapper depends on.
# 4. Write the .preflight_ok token. All other SELECT rules depend on it.
#
# No network fallback. If the tarball is missing, this script aborts with a
# clear error and the entire DAG fails before fan-out.

suppressPackageStartupMessages({
  library(arrow)
})

snek <- snakemake

tarball_path <- snek@input[["tarball"]]
token_path   <- snek@output[["token"]]

stopifnot(file.exists(tarball_path))

target_version <- "1.6.4"

needs_install <- TRUE
if ("select" %in% rownames(installed.packages())) {
  installed_version <- as.character(packageVersion("select"))
  if (installed_version == target_version) {
    needs_install <- FALSE
    message(sprintf("[preflight] select %s already installed; skipping reinstall.",
                    installed_version))
  }
}

if (needs_install) {
  message(sprintf("[preflight] installing select %s from %s ...",
                  target_version, tarball_path))
  install.packages(tarball_path, repos = NULL, type = "source", quiet = TRUE)
  installed_version <- as.character(packageVersion("select"))
  if (installed_version != target_version) {
    stop(sprintf("[preflight] expected select %s, got %s after install.",
                 target_version, installed_version))
  }
}

# Smoke test on bundled luad_data.
suppressPackageStartupMessages({
  library(select)
})

data(luad_data)
M  <- luad_data$gam
sc <- luad_data$samples$sample.class
ac <- luad_data$alterations$alteration.class

stopifnot(is.matrix(M) || is.data.frame(M))
stopifnot(!is.null(rownames(M)))
stopifnot(!is.null(colnames(M)))

message("[preflight] running select::select on luad_data with n.permut = 50 ...")
res <- select::select(
  M                              = as.matrix(M),
  sample.class                   = sc,
  alteration.class               = ac,
  folder                         = tempfile("select_preflight_"),
  r.seed                         = 0,
  n.cores                        = 1,
  n.permut                       = 50,
  save.intermediate.files        = FALSE,
  randomization.switch.threshold = 30,
  max.memory.size                = 8,
  FDR.cutoff                     = 1.0,
  calculate_FDR                  = FALSE,
  verbose                        = FALSE
)

required_cols <- c("SFE_1", "SFE_2", "select_score",
                   "wMI_p.value", "ME_p.value", "direction")
missing <- setdiff(required_cols, colnames(res))
if (length(missing) > 0) {
  stop(sprintf("[preflight] select() output missing columns: %s",
               paste(missing, collapse = ", ")))
}

# Verify direction codomain.
allowed_dirs <- c("CO", "ME", "none")
bad_dirs <- setdiff(unique(res$direction), allowed_dirs)
if (length(bad_dirs) > 0) {
  stop(sprintf("[preflight] unexpected direction values: %s",
               paste(bad_dirs, collapse = ", ")))
}

dir.create(dirname(token_path), recursive = TRUE, showWarnings = FALSE)
writeLines(c(
  sprintf("preflight_ok %s", format(Sys.time(), "%Y-%m-%dT%H:%M:%S%z")),
  sprintf("select_version %s", as.character(packageVersion("select"))),
  sprintf("n_pairs_returned %d", nrow(res))
), token_path)

message(sprintf("[preflight] OK — wrote %s", token_path))
```

- [ ] **Step 4: Add the rule to `code/workflows/Snakefile`**

Add immediately after the `rule all:` block — the rule placement matches the existing
overlay-rule pattern (after `rule all`, before the heavyweight per-study rules).
Use 2-space indentation per existing convention.

```python
#
# t078 SELECT co-occurrence / mutual-exclusivity layer (opt-in via config["select"]
# ["enabled"]). See doc/plans/2026-04-25-t078-select-cooccurrence-design.md.
#

select_enabled = config.get("select", {}).get("enabled", False)

if select_enabled:

  rule preflight_select_env:
    """Rule (0): install CSOgroup/select v1.6.4 from vendored tarball, smoke
    test on luad_data, write token. Every other SELECT rule depends on this."""
    input:
      tarball = "data/external/select_v1.6.4.tar.gz"
    output:
      token = out_dir.joinpath("select/.preflight_ok")
    conda:
      "../envs/select.yml"
    script:
      "../scripts/preflight_select_env.R"
```

- [ ] **Step 5: Run Python test to verify rule wiring**

```bash
uv run --frozen pytest code/scripts/tests/test_preflight_select_env.py -v
```

Expected: 4 PASS.

- [ ] **Step 6: Snakemake dry-run to verify the rule resolves**

```bash
uv run --frozen snakemake \
  -s code/workflows/Snakefile \
  --configfile code/config/config-10k-genes.yml \
  --config select="{enabled: true}" \
  -n \
  results/select/.preflight_ok 2>&1 | tail -20
```

Expected: a one-job DAG plan showing `preflight_select_env` will execute. No errors.

- [ ] **Step 7: Commit**

```bash
git add code/scripts/preflight_select_env.R code/workflows/Snakefile \
  code/scripts/tests/test_preflight_select_env.py
git commit -m "$(cat <<'EOF'
feat(t078): rule (0) preflight_select_env — install + smoke test

Installs CSOgroup/select v1.6.4 from the vendored tarball into the
conda env's R library, runs select::select on bundled luad_data with
n.permut=50, verifies the upstream output schema, and writes the
.preflight_ok token. All other SELECT rules will depend on this token
so the DAG fails fast if SELECT install or API drifts.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 4.5: Vendor COSMIC Cancer Gene Census

**Why:** Task 5 reads `data/cosmic_cgc.tsv`. The project has the upstream file at
`/data/raw/cosmic/v100/Cosmic_CancerGeneCensus_v100_GRCh38.tsv` (CGC v100, GRCh38, ~180 KB).
Vendor a copy under `data/` + a README so the path is explicit and version-stamped, and
add a Snakemake rule (`vendor_cosmic_cgc`) that captures the copy + sha256 verification
recipe — the artifact is committed but the rule lets `git clean` survivors regenerate it
from the local raw snapshot.

**Files:**
- Create: `data/cosmic_cgc.tsv` (renamed copy)
- Create: `data/cosmic_cgc.README.md`
- Modify: `code/workflows/Snakefile` — add `rule vendor_cosmic_cgc`

- [ ] **Step 1: Add `rule vendor_cosmic_cgc` to the Snakefile**

Append to `code/workflows/Snakefile` (alongside the other t078 vendoring rules):

```python
#
# t078 SELECT pipeline — vendored COSMIC Cancer Gene Census snapshot.
#
# Manual prereq: the Sanger CGC TSV at
# config["cosmic_cgc_raw_path"] (default
# /data/raw/cosmic/v100/Cosmic_CancerGeneCensus_v100_GRCh38.tsv —
# auth-gated; download with a free academic COSMIC account). The artifact
# data/cosmic_cgc.tsv is committed; this rule documents the copy recipe and
# verifies the sha256 prefix to flag silent upstream substitution.
#
COSMIC_CGC_SHA256_PREFIX = "<TBD-after-first-copy>"   # 12-char prefix

rule vendor_cosmic_cgc:
  input:
    config.get(
      "cosmic_cgc_raw_path",
      "/data/raw/cosmic/v100/Cosmic_CancerGeneCensus_v100_GRCh38.tsv",
    )
  output:
    "data/cosmic_cgc.tsv"
  params:
    expected_sha256_prefix=COSMIC_CGC_SHA256_PREFIX
  shell:
    r"""
    cp {input} {output}.tmp
    actual=$(sha256sum {output}.tmp | cut -c1-12)
    if [ "{params.expected_sha256_prefix}" != "<TBD-after-first-copy>" ] && \
       [ "$actual" != "{params.expected_sha256_prefix}" ]; then
      echo "ERROR: sha256 mismatch for {output}" >&2
      echo "  expected prefix: {params.expected_sha256_prefix}" >&2
      echo "  actual prefix:   $actual" >&2
      rm -f {output}.tmp
      exit 1
    fi
    mv {output}.tmp {output}
    """
```

- [ ] **Step 2: Run the rule once to populate the artifact**

```bash
uv run snakemake -s code/workflows/Snakefile -j1 \
  --configfile code/config/config-10k-genes.yml \
  data/cosmic_cgc.tsv
```

Expected: ~180 KB tab-separated file at `data/cosmic_cgc.tsv` with `Gene Symbol`
header column.

- [ ] **Step 3: Record the sha256 prefix and pin it in the Snakefile**

```bash
sha256sum data/cosmic_cgc.tsv | cut -c1-12
```

Edit the `COSMIC_CGC_SHA256_PREFIX = "<TBD-after-first-copy>"` line in
`code/workflows/Snakefile` and replace the placeholder with the 12-char prefix.

- [ ] **Step 4: Write `data/cosmic_cgc.README.md`**

```markdown
# data/cosmic_cgc.tsv

COSMIC Cancer Gene Census v100 (GRCh38).

- Source: /data/raw/cosmic/v100/Cosmic_CancerGeneCensus_v100_GRCh38.tsv (Sanger)
- Vendored at: 2026-04-25
- sha256 (12-char prefix): `<insert-from-step-3>`
- Re-derive: `uv run snakemake -s code/workflows/Snakefile -j1 \
  --configfile code/config/config-10k-genes.yml data/cosmic_cgc.tsv`
- Schema: tab-separated; primary column `Gene Symbol` (consumed by Task 5
  `build_select_gene_universe.py`).

To upgrade: replace the raw source file (or override `cosmic_cgc_raw_path` in
the config), bump `COSMIC_CGC_SHA256_PREFIX` in `code/workflows/Snakefile`,
re-run the rule, and bump `cgc_version` in the config block of
`code/config/config-10k-genes.yml`.
```

- [ ] **Step 5: Commit**

```bash
git add data/cosmic_cgc.tsv data/cosmic_cgc.README.md code/workflows/Snakefile
git commit -m "$(cat <<'EOF'
chore(t078): vendor COSMIC Cancer Gene Census v100

Source: /data/raw/cosmic/v100/Cosmic_CancerGeneCensus_v100_GRCh38.tsv
(Sanger). Used by Task 5 build_select_gene_universe.py as one of the
three union sources (alongside Bailey 2018 and Sanchez-Vega 2018). Adds
a Snakemake rule vendor_cosmic_cgc capturing the copy recipe + sha256
verification so the artifact can be regenerated from the local raw
snapshot after a clean.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 5: Implement rule (1b) `build_select_gene_universe.py`

**Why:** The gene universe is the column space for every per-cell GAM. Per design
Section 4.3 it combines the driver list from [@Bailey2018] with COSMIC CGC,
Sanchez-Vega, and optional custom genes, with provenance columns (source flags + version + sha256) so that
downstream changes to any source are visible in the headline output.

**Files:**
- Create: `code/scripts/build_select_gene_universe.py`
- Create: `code/scripts/tests/test_build_select_gene_universe.py`

- [ ] **Step 1: Write the failing test**

```python
# code/scripts/tests/test_build_select_gene_universe.py
"""Unit tests for build_select_gene_universe."""
from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd
import pytest

import build_select_gene_universe as mod


def _write_tsv(path: Path, df: pd.DataFrame) -> None:
    df.to_csv(path, sep="\t", index=False)


def _sha256_prefix(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


@pytest.fixture
def sources(tmp_path: Path):
    """Three small source files: Bailey, CGC, Sanchez-Vega, partial overlap."""
    bailey = tmp_path / "bailey2018.tsv"
    _write_tsv(bailey, pd.DataFrame({"Gene": ["TP53", "KRAS", "EGFR"]}))
    cgc = tmp_path / "cgc.tsv"
    _write_tsv(cgc, pd.DataFrame({"Gene Symbol": ["KRAS", "BRAF", "MYC"]}))
    sv = tmp_path / "sanchez_vega.tsv"
    _write_tsv(sv, pd.DataFrame({
        "gene": ["EGFR", "BRAF", "PIK3CA"],
        "pathway": ["RTK_RAS", "RTK_RAS", "PI3K"],
    }))
    return bailey, cgc, sv


def test_build_universe_unions_three_sources(tmp_path: Path, sources):
    bailey, cgc, sv = sources
    out = tmp_path / "universe.tsv"
    mod.build_universe(
        bailey_path=bailey,
        cgc_path=cgc,
        sanchez_vega_path=sv,
        custom_path=None,
        out_path=out,
        bailey_version="2018",
        cgc_version="2024-09",
        sanchez_vega_version="2018",
    )
    df = pd.read_csv(out, sep="\t")
    assert set(df["symbol"]) == {"TP53", "KRAS", "EGFR", "BRAF", "MYC", "PIK3CA"}


def test_build_universe_provenance_columns_populated(tmp_path: Path, sources):
    bailey, cgc, sv = sources
    out = tmp_path / "universe.tsv"
    mod.build_universe(
        bailey_path=bailey, cgc_path=cgc, sanchez_vega_path=sv,
        custom_path=None, out_path=out,
        bailey_version="2018", cgc_version="2024-09",
        sanchez_vega_version="2018",
    )
    df = pd.read_csv(out, sep="\t")
    for col in ["from_bailey", "from_cgc", "from_sanchez_vega", "from_custom",
                "bailey_version", "cgc_version", "sanchez_vega_version",
                "bailey_sha256", "cgc_sha256", "sanchez_vega_sha256"]:
        assert col in df.columns, f"missing {col}"
    # KRAS in Bailey + CGC, not SV / custom
    row = df[df["symbol"] == "KRAS"].iloc[0]
    assert bool(row["from_bailey"]) is True
    assert bool(row["from_cgc"]) is True
    assert bool(row["from_sanchez_vega"]) is False
    assert bool(row["from_custom"]) is False
    assert row["bailey_sha256"] == _sha256_prefix(bailey)


def test_build_universe_custom_genes(tmp_path: Path, sources):
    bailey, cgc, sv = sources
    custom = tmp_path / "custom.tsv"
    custom.write_text("ZNF1\nZNF2\n")  # one symbol per line, no header
    out = tmp_path / "universe.tsv"
    mod.build_universe(
        bailey_path=bailey, cgc_path=cgc, sanchez_vega_path=sv,
        custom_path=custom, out_path=out,
        bailey_version="2018", cgc_version="2024-09",
        sanchez_vega_version="2018",
    )
    df = pd.read_csv(out, sep="\t")
    assert "ZNF1" in set(df["symbol"])
    assert "ZNF2" in set(df["symbol"])
    znf1 = df[df["symbol"] == "ZNF1"].iloc[0]
    assert bool(znf1["from_custom"]) is True
    assert bool(znf1["from_bailey"]) is False


def test_build_universe_empty_custom_path_means_none(tmp_path: Path, sources):
    bailey, cgc, sv = sources
    out = tmp_path / "universe.tsv"
    # Pass custom_path=None — should not crash and should leave from_custom False everywhere.
    mod.build_universe(
        bailey_path=bailey, cgc_path=cgc, sanchez_vega_path=sv,
        custom_path=None, out_path=out,
        bailey_version="2018", cgc_version="2024-09",
        sanchez_vega_version="2018",
    )
    df = pd.read_csv(out, sep="\t")
    assert (df["from_custom"] == False).all()  # noqa: E712
```

- [ ] **Step 2: Run test to verify it fails**

```bash
uv run --frozen pytest code/scripts/tests/test_build_select_gene_universe.py -v
```

Expected: FAIL with `ModuleNotFoundError: build_select_gene_universe`.

- [ ] **Step 3: Implement `code/scripts/build_select_gene_universe.py`**

```python
# code/scripts/build_select_gene_universe.py
"""Rule (1b): emit the SELECT gene-universe TSV with provenance columns.

See doc/plans/2026-04-25-t078-select-cooccurrence-design.md Section 4.3.

Reads:
  - Bailey 2018 Table S1 TSV (from data/bailey2018_table_s1.tsv)
  - COSMIC CGC TSV (from data/cosmic_cgc.tsv) — manual prereq
  - Sanchez-Vega pathway TSV (from data/sanchez_vega_pathways.tsv)
  - optional custom genes TSV (one symbol per line, no header)

Writes:
  - results/select/gene_universe.tsv

Columns: symbol, from_bailey, from_cgc, from_sanchez_vega, from_custom,
         bailey_version, cgc_version, sanchez_vega_version,
         bailey_sha256, cgc_sha256, sanchez_vega_sha256
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd

GeneSet = set[str]


def _sha256_prefix(path: Path, n_chars: int = 12) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:n_chars]


def _read_bailey(path: Path) -> GeneSet:
    df = pd.read_csv(path, sep="\t")
    return set(df["Gene"].dropna().astype(str).str.strip())


def _read_cgc(path: Path) -> GeneSet:
    df = pd.read_csv(path, sep="\t")
    col = "Gene Symbol" if "Gene Symbol" in df.columns else "symbol"
    return set(df[col].dropna().astype(str).str.strip())


def _read_sanchez_vega(path: Path) -> GeneSet:
    df = pd.read_csv(path, sep="\t")
    col = "gene" if "gene" in df.columns else "Gene"
    return set(df[col].dropna().astype(str).str.strip())


def _read_custom(path: Path | None) -> GeneSet:
    if path is None:
        return set()
    text = Path(path).read_text().strip()
    if not text:
        return set()
    return {line.strip() for line in text.splitlines() if line.strip()}


def build_universe(
    bailey_path: Path,
    cgc_path: Path,
    sanchez_vega_path: Path,
    custom_path: Path | None,
    out_path: Path,
    bailey_version: str,
    cgc_version: str,
    sanchez_vega_version: str,
) -> None:
    bailey = _read_bailey(bailey_path)
    cgc = _read_cgc(cgc_path)
    sv = _read_sanchez_vega(sanchez_vega_path)
    custom = _read_custom(custom_path)

    all_symbols = sorted(bailey | cgc | sv | custom)

    bailey_sha = _sha256_prefix(bailey_path)
    cgc_sha = _sha256_prefix(cgc_path)
    sv_sha = _sha256_prefix(sanchez_vega_path)

    df = pd.DataFrame({"symbol": all_symbols})
    df["from_bailey"] = df["symbol"].isin(bailey)
    df["from_cgc"] = df["symbol"].isin(cgc)
    df["from_sanchez_vega"] = df["symbol"].isin(sv)
    df["from_custom"] = df["symbol"].isin(custom)
    df["bailey_version"] = bailey_version
    df["cgc_version"] = cgc_version
    df["sanchez_vega_version"] = sanchez_vega_version
    df["bailey_sha256"] = bailey_sha
    df["cgc_sha256"] = cgc_sha
    df["sanchez_vega_sha256"] = sv_sha

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, sep="\t", index=False)


# Snakemake entry point.
if "snakemake" in globals():  # pragma: no cover  # set by Snakemake's script: directive
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821
    build_universe(
        bailey_path=Path(snek.input["bailey"]),
        cgc_path=Path(snek.input["cgc"]),
        sanchez_vega_path=Path(snek.input["sanchez_vega"]),
        custom_path=Path(snek.input["custom"]) if "custom" in snek.input.keys() else None,
        out_path=Path(snek.output["universe"]),
        bailey_version=snek.params["bailey_version"],
        cgc_version=snek.params["cgc_version"],
        sanchez_vega_version=snek.params["sanchez_vega_version"],
    )
```

- [ ] **Step 4: Verify the project's conftest is in place**

The project already has `code/scripts/tests/conftest.py` that adds `code/scripts/` to
`sys.path` so tests can `import build_select_gene_universe` directly (no package
structure). No changes required — the test pattern in step 1 follows the existing
project convention (see e.g. `test_annotate_hypermutators.py`). Verify with:

```bash
test -f code/scripts/tests/conftest.py && echo "conftest present"
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
uv run --frozen pytest code/scripts/tests/test_build_select_gene_universe.py -v
uv run --frozen ruff check code/scripts/build_select_gene_universe.py
uv run --frozen ruff format --check code/scripts/build_select_gene_universe.py
```

Expected: 4 PASS, lint clean.

- [ ] **Step 6: Commit**

```bash
git add code/scripts/build_select_gene_universe.py \
  code/scripts/tests/test_build_select_gene_universe.py
git commit -m "$(cat <<'EOF'
feat(t078): rule (1b) build_select_gene_universe.py

Emits the union of Bailey 2018 ∪ COSMIC CGC ∪ Sanchez-Vega ∪ optional
custom-genes-tsv as results/select/gene_universe.tsv with per-source
boolean flags + version + sha256 prefix. Provenance columns are
required so that downstream changes to any source are visible in the
headline output (design Section 4.3).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 6: Implement rule (1a) `build_panel_gene_sets.py`

**Why:** Rule (1a) emits per-panel callable-gene feathers from BED files. Sample-level
callability (Section 1.4) joins these via the per-sample panel mapping at GAM
construction time. Per design Section 4.2: scattering is per `panel_id`, not per
study; multiple intervals per gene dedupe; HGNC canonicalisation via existing
`data/grch38.tsv`; the `wes` pseudo-panel marks every gene callable.

**Files:**
- Create: `code/scripts/build_panel_gene_sets.py`
- Create: `code/scripts/tests/test_build_panel_gene_sets.py`

- [ ] **Step 1: Write the failing test**

```python
# code/scripts/tests/test_build_panel_gene_sets.py
"""Unit tests for build_panel_gene_sets."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

import build_panel_gene_sets as mod


@pytest.fixture
def grch38(tmp_path: Path):
    """Tiny grch38.tsv lookup with 4 canonical symbols."""
    p = tmp_path / "grch38.tsv"
    rows = [
        ["ensgene", "entrez", "symbol", "chr", "start", "end", "strand", "biotype", "description"],
        ["ENSG1", "1", "TP53", "17", "1", "100", "+", "protein_coding", "tp53 gene"],
        ["ENSG2", "2", "KRAS", "12", "1", "100", "+", "protein_coding", "kras"],
        ["ENSG3", "3", "EGFR", "7", "1", "100", "+", "protein_coding", "egfr"],
        ["ENSG4", "4", "BRAF", "7", "1", "100", "+", "protein_coding", "braf"],
    ]
    p.write_text(
        "\n".join("\t".join(row) for row in rows) + "\n"
    )
    return p


def test_panel_gene_set_dedupes_intervals(tmp_path: Path, grch38):
    bed = tmp_path / "tinypanel.bed"
    bed_rows = [
        ["chr17", "1", "100", "TP53"],
        ["chr17", "101", "200", "TP53"],  # second exon — must dedupe
        ["chr12", "1", "100", "KRAS"],
    ]
    bed.write_text(
        "\n".join("\t".join(row) for row in bed_rows) + "\n"
    )
    out = tmp_path / "tinypanel.feather"
    mod.build_panel_gene_set(
        panel_id="tinypanel",
        bed_path=bed,
        grch38_path=grch38,
        out_path=out,
    )
    df = pd.read_feather(out)
    assert len(df) == 2
    assert set(df["symbol"]) == {"TP53", "KRAS"}
    assert (df["callable"] == True).all()  # noqa: E712
    assert (df["panel_id"] == "tinypanel").all()
    assert (df["source"] == "bed").all()


def test_panel_gene_set_drops_non_hgnc(tmp_path: Path, grch38):
    bed = tmp_path / "tinypanel.bed"
    bed.write_text(
        "chr17\t1\t100\tTP53\n"
        "chr_unknown\t1\t100\tFOOBAR_NOT_HGNC\n"
    )
    out = tmp_path / "out.feather"
    mod.build_panel_gene_set(
        panel_id="tinypanel", bed_path=bed,
        grch38_path=grch38, out_path=out,
    )
    df = pd.read_feather(out)
    assert "FOOBAR_NOT_HGNC" not in set(df["symbol"])
    assert "TP53" in set(df["symbol"])


def test_wes_pseudo_panel_marks_all_callable(tmp_path: Path, grch38):
    """The 'wes' pseudo-panel emits one row per HGNC symbol with callable=True."""
    out = tmp_path / "wes.feather"
    mod.build_wes_pseudo_panel(grch38_path=grch38, out_path=out)
    df = pd.read_feather(out)
    assert len(df) == 4
    assert set(df["symbol"]) == {"TP53", "KRAS", "EGFR", "BRAF"}
    assert (df["callable"] == True).all()  # noqa: E712
    assert (df["panel_id"] == "wes").all()
    assert (df["source"] == "wes_default").all()


def test_panel_gene_set_missing_bed_raises(tmp_path: Path, grch38):
    out = tmp_path / "out.feather"
    with pytest.raises(FileNotFoundError):
        mod.build_panel_gene_set(
            panel_id="missing", bed_path=tmp_path / "does_not_exist.bed",
            grch38_path=grch38, out_path=out,
        )
```

- [ ] **Step 2: Run test to verify it fails**

```bash
uv run --frozen pytest code/scripts/tests/test_build_panel_gene_sets.py -v
```

Expected: FAIL on `ModuleNotFoundError`.

- [ ] **Step 3: Implement `code/scripts/build_panel_gene_sets.py`**

```python
# code/scripts/build_panel_gene_sets.py
"""Rule (1a): emit per-panel callable-gene feathers.

Per design Section 4.2: scatter is per panel_id (NOT per study). Reads a
4-column BED (chrom, start, end, symbol), dedupes per symbol, restricts to
HGNC-canonical symbols via data/grch38.tsv, writes a feather with columns
(symbol, callable, panel_id, source).

The pseudo-panel 'wes' is built differently: every HGNC symbol from grch38
is marked callable=True with source='wes_default'.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

BED_COLS = ["chrom", "start", "end", "symbol"]
OUT_COLS = ["symbol", "callable", "panel_id", "source"]


def _load_hgnc_symbols(grch38_path: Path) -> set[str]:
    df = pd.read_csv(grch38_path, sep="\t")
    col = "symbol" if "symbol" in df.columns else "Hugo_Symbol"
    return set(df[col].dropna().astype(str).str.strip())


def build_panel_gene_set(
    panel_id: str,
    bed_path: Path,
    grch38_path: Path,
    out_path: Path,
) -> None:
    if not Path(bed_path).exists():
        raise FileNotFoundError(f"panel BED not found: {bed_path}")

    hgnc = _load_hgnc_symbols(Path(grch38_path))

    bed = pd.read_csv(bed_path, sep="\t", header=None, names=BED_COLS,
                      dtype={"symbol": "string"})
    if bed.empty:
        # Empty placeholder — emit zero-row feather with the right schema.
        out = pd.DataFrame({c: pd.Series(dtype=t) for c, t in [
            ("symbol", "string"), ("callable", "bool"),
            ("panel_id", "string"), ("source", "string"),
        ]})
    else:
        symbols = bed["symbol"].str.strip().dropna().unique()
        canonical = [s for s in symbols if s in hgnc]
        out = pd.DataFrame({
            "symbol": canonical,
            "callable": True,
            "panel_id": panel_id,
            "source": "bed",
        })
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out[OUT_COLS].reset_index(drop=True).to_feather(out_path)


def build_wes_pseudo_panel(grch38_path: Path, out_path: Path) -> None:
    hgnc = sorted(_load_hgnc_symbols(Path(grch38_path)))
    out = pd.DataFrame({
        "symbol": hgnc,
        "callable": True,
        "panel_id": "wes",
        "source": "wes_default",
    })
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out[OUT_COLS].reset_index(drop=True).to_feather(out_path)


if "snakemake" in globals():  # pragma: no cover  # set by Snakemake's script: directive
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821
    panel_id = snek.wildcards["panel_id"]
    if panel_id == "wes":
        build_wes_pseudo_panel(
            grch38_path=Path(snek.input["grch38"]),
            out_path=Path(snek.output[0]),
        )
    else:
        build_panel_gene_set(
            panel_id=panel_id,
            bed_path=Path(snek.input["bed"]),
            grch38_path=Path(snek.input["grch38"]),
            out_path=Path(snek.output[0]),
        )
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
uv run --frozen pytest code/scripts/tests/test_build_panel_gene_sets.py -v
uv run --frozen ruff check code/scripts/build_panel_gene_sets.py
uv run --frozen ruff format --check code/scripts/build_panel_gene_sets.py
```

Expected: 4 PASS, lint clean.

- [ ] **Step 5: Commit**

```bash
git add code/scripts/build_panel_gene_sets.py \
  code/scripts/tests/test_build_panel_gene_sets.py
git commit -m "$(cat <<'EOF'
feat(t078): rule (1a) build_panel_gene_sets.py

Per-panel scatter (NOT per-study) emitting (symbol, callable, panel_id,
source) feathers. BED parsing dedupes intervals per symbol; restricts
to HGNC-canonical symbols via data/grch38.tsv; the 'wes' pseudo-panel
marks every HGNC symbol callable. Empty BEDs (placeholder F1/F1CDx)
produce zero-row feathers with the right schema.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 7: Extend `create_combined_sample_table.py` for `sample_panel_map.feather`

**Why:** Per design Section 1.4 the layer needs a per-sample `(study_id, sample_id) →
panel_id` mapping that distinguishes GENIE samples (per-assay) from non-GENIE samples
(per-study via `data/study_panels.tsv`) from WES studies (`panel_id="wes"`). The
existing script is 20 lines and only emits the cancer-type combined table; we extend
it to also emit `sample_panel_map.feather`.

**Files:**
- Modify: `code/scripts/create_combined_sample_table.py`
- Create: `code/scripts/tests/test_sample_panel_map.py`
- Modify: `code/workflows/Snakefile` (add new output to the existing rule)

- [ ] **Step 1: Write the failing test**

```python
# code/scripts/tests/test_sample_panel_map.py
"""Tests for the sample_panel_map output of create_combined_sample_table."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

import create_combined_sample_table as mod


@pytest.fixture
def study_panels_tsv(tmp_path: Path):
    p = tmp_path / "study_panels.tsv"
    p.write_text(
        "study_id\tpanel_id\tsequencing_type\n"
        "brca_tcga\twes\twes\n"
        "msk_impact_2017\tmsk_impact_410\tpanel\n"
    )
    return p


@pytest.fixture
def per_study_samples(tmp_path: Path):
    """Two non-GENIE per-study samples feathers."""
    out = []
    for sid, samples in [
        ("brca_tcga", [("p1", "s1"), ("p2", "s2")]),
        ("msk_impact_2017", [("p3", "s3")]),
    ]:
        df = pd.DataFrame({
            "patient_id": [s[0] for s in samples],
            "sample_id":  [s[1] for s in samples],
            "cancer_type": ["BRCA"] * len(samples),
            "cancer_type_detailed": ["BRCA"] * len(samples),
            "study_id": [sid] * len(samples),
        })
        p = tmp_path / f"{sid}_samples.feather"
        df.to_feather(p)
        out.append(p)
    return out


@pytest.fixture
def genie_assay_table(tmp_path: Path):
    """Tiny GENIE per-sample assay map: 2 samples in two different assays."""
    p = tmp_path / "genie_assay_table.tsv"
    p.write_text(
        "study_id\tsample_id\tpanel_id\n"
        "genie_v9.1\tGENIE-A\tmsk_impact_410\n"
        "genie_v9.1\tGENIE-B\tfoundation_one_cdx\n"
    )
    return p


def test_sample_panel_map_covers_all_samples_non_genie(
    tmp_path: Path, per_study_samples, study_panels_tsv, genie_assay_table
):
    out = tmp_path / "sample_panel_map.feather"
    mod.build_sample_panel_map(
        per_study_samples_paths=per_study_samples,
        study_panels_tsv=study_panels_tsv,
        genie_assay_table=genie_assay_table,
        out_path=out,
    )
    df = pd.read_feather(out)
    # 3 non-GENIE samples + 2 GENIE samples = 5 rows.
    assert len(df) == 5
    assert set(df.columns) >= {"study_id", "sample_id", "panel_id", "panel_source"}
    # WES study mapped to 'wes' with source 'wes_default'.
    brca = df[df["study_id"] == "brca_tcga"]
    assert (brca["panel_id"] == "wes").all()
    assert (brca["panel_source"] == "wes_default").all()
    # Panel study mapped from study_panels_tsv.
    msk = df[df["study_id"] == "msk_impact_2017"]
    assert (msk["panel_id"] == "msk_impact_410").all()
    assert (msk["panel_source"] == "study_panels_tsv").all()


def test_sample_panel_map_uses_genie_assay_table_for_genie_samples(
    tmp_path: Path, per_study_samples, study_panels_tsv, genie_assay_table
):
    out = tmp_path / "sample_panel_map.feather"
    mod.build_sample_panel_map(
        per_study_samples_paths=per_study_samples,
        study_panels_tsv=study_panels_tsv,
        genie_assay_table=genie_assay_table,
        out_path=out,
    )
    df = pd.read_feather(out)
    a = df[(df["study_id"] == "genie_v9.1") & (df["sample_id"] == "GENIE-A")].iloc[0]
    b = df[(df["study_id"] == "genie_v9.1") & (df["sample_id"] == "GENIE-B")].iloc[0]
    assert a["panel_id"] == "msk_impact_410"
    assert a["panel_source"] == "genie_assay_table"
    assert b["panel_id"] == "foundation_one_cdx"
    assert b["panel_source"] == "genie_assay_table"


def test_sample_panel_map_unmapped_study_raises(
    tmp_path: Path, study_panels_tsv, genie_assay_table
):
    """A non-GENIE study not in study_panels.tsv must fail."""
    rogue_df = pd.DataFrame({
        "patient_id": ["p1"], "sample_id": ["s1"],
        "cancer_type": ["BRCA"], "cancer_type_detailed": ["BRCA"],
        "study_id": ["unknown_study"],
    })
    rogue_path = tmp_path / "unknown_study_samples.feather"
    rogue_df.to_feather(rogue_path)
    out = tmp_path / "out.feather"
    with pytest.raises(KeyError, match="unknown_study"):
        mod.build_sample_panel_map(
            per_study_samples_paths=[rogue_path],
            study_panels_tsv=study_panels_tsv,
            genie_assay_table=genie_assay_table,
            out_path=out,
        )
```

- [ ] **Step 2: Run test to verify it fails**

```bash
uv run --frozen pytest code/scripts/tests/test_sample_panel_map.py -v
```

Expected: FAIL — `build_sample_panel_map` does not exist.

- [ ] **Step 3: Extend `code/scripts/create_combined_sample_table.py`**

```python
"""create_combined_sample_table.py.

Two outputs:
  1. The existing cancer-type combined table (concat of per-study
     samples feathers, projected to the canonical 4 columns).
  2. NEW (t078): sample_panel_map.feather mapping (study_id, sample_id)
     to panel_id, sourced from:
       - GENIE assay table (per-sample, study_id == 'genie_v9.1')
       - data/study_panels.tsv (per-study, sequencing_type='panel')
       - 'wes' pseudo-panel (per-study, sequencing_type='wes')
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd


CANONICAL_COLS = ["patient_id", "sample_id", "cancer_type", "cancer_type_detailed"]


def build_combined_sample_table(input_paths: list[Path], out_path: Path) -> None:
    dfs = [pd.read_feather(p)[CANONICAL_COLS] for p in input_paths]
    df = pd.concat(dfs)
    df["patient_id"] = df["patient_id"].astype("str")
    df["sample_id"] = df["sample_id"].astype("str")
    df["cancer_type"] = df["cancer_type"].astype("category")
    df["cancer_type_detailed"] = df["cancer_type_detailed"].astype("category")
    df.to_feather(out_path)


def build_sample_panel_map(
    per_study_samples_paths: list[Path],
    study_panels_tsv: Path,
    genie_assay_table: Path,
    out_path: Path,
) -> None:
    """Emit metadata/sample_panel_map.feather per design Section 1.4."""
    study_panels = pd.read_csv(study_panels_tsv, sep="\t")
    sp_lookup = study_panels.set_index("study_id")[["panel_id", "sequencing_type"]]

    # GENIE per-sample assay table — schema (study_id, sample_id, panel_id).
    genie = pd.read_csv(genie_assay_table, sep="\t") if Path(genie_assay_table).exists() \
        else pd.DataFrame(columns=["study_id", "sample_id", "panel_id"])

    rows: list[pd.DataFrame] = []
    for p in per_study_samples_paths:
        df = pd.read_feather(p)
        if "study_id" not in df.columns:
            # Existing per-study feathers may not yet carry study_id — derive
            # from filename. This is the convert_to_feather contract.
            study_id = Path(p).stem.replace("_samples", "")
            df = df.assign(study_id=study_id)

        for sid, sub in df.groupby("study_id", observed=True):
            if sid == "genie_v9.1":
                # Per-sample assignment from GENIE assay table.
                sub_g = sub[["study_id", "sample_id"]].merge(
                    genie[["sample_id", "panel_id"]],
                    on="sample_id", how="left", validate="many_to_one",
                )
                if sub_g["panel_id"].isna().any():
                    missing = sub_g[sub_g["panel_id"].isna()]["sample_id"].head(3).tolist()
                    raise KeyError(
                        f"GENIE samples missing from assay table: {missing} ..."
                    )
                sub_g["panel_source"] = "genie_assay_table"
                rows.append(sub_g[["study_id", "sample_id", "panel_id", "panel_source"]])
                continue

            # Non-GENIE: lookup in study_panels.tsv.
            if sid not in sp_lookup.index:
                raise KeyError(
                    f"study {sid!r} missing from study_panels.tsv — "
                    "add it before running the SELECT pipeline"
                )
            panel_id = sp_lookup.at[sid, "panel_id"]
            seq_type = sp_lookup.at[sid, "sequencing_type"]
            panel_source = "wes_default" if seq_type == "wes" else "study_panels_tsv"
            mapped = sub[["study_id", "sample_id"]].copy()
            mapped["panel_id"] = panel_id
            mapped["panel_source"] = panel_source
            rows.append(mapped)

    out = pd.concat(rows, ignore_index=True)
    out["study_id"] = out["study_id"].astype("string")
    out["sample_id"] = out["sample_id"].astype("string")
    out["panel_id"] = out["panel_id"].astype("string")
    out["panel_source"] = out["panel_source"].astype("string")
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_feather(out_path)


if "snakemake" in globals():  # pragma: no cover  # set by Snakemake's script: directive
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821
    build_combined_sample_table(
        input_paths=[Path(p) for p in snek.input["per_study"]],
        out_path=Path(snek.output["combined"]),
    )
    build_sample_panel_map(
        per_study_samples_paths=[Path(p) for p in snek.input["per_study"]],
        study_panels_tsv=Path(snek.input["study_panels"]),
        genie_assay_table=Path(snek.input["genie_assay_table"]),
        out_path=Path(snek.output["sample_panel_map"]),
    )
```

- [ ] **Step 4: Update the existing Snakefile rule**

Find the existing rule that emits the combined sample table (search for
`create_combined_sample_table` in `code/workflows/Snakefile`) and extend its
`input:`/`output:` to add `study_panels`, `genie_assay_table`, and
`sample_panel_map`. The exact name of the existing rule and its input shape needs to be
verified at edit time — do not assume; read the rule source first.

- [ ] **Step 5: Run tests + lint**

```bash
uv run --frozen pytest code/scripts/tests/test_sample_panel_map.py -v
uv run --frozen ruff check code/scripts/create_combined_sample_table.py
uv run --frozen ruff format --check code/scripts/create_combined_sample_table.py
```

Expected: 3 PASS, lint clean.

- [ ] **Step 6: Commit**

```bash
git add code/scripts/create_combined_sample_table.py \
  code/scripts/tests/test_sample_panel_map.py code/workflows/Snakefile
git commit -m "$(cat <<'EOF'
feat(t078): extend create_combined_sample_table for sample_panel_map

Adds build_sample_panel_map() emitting metadata/sample_panel_map.feather
per design Section 1.4. Resolves panel_id per (study_id, sample_id):
GENIE samples via per-assay table, non-GENIE panel studies via
data/study_panels.tsv, WES studies via 'wes' pseudo-panel. Unmapped
non-GENIE studies raise KeyError to enforce the fail-early invariant.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 8: Implement `select_lib.py` shared helpers

**Why:** Several scripts need the same primitives. Putting them in one tested module
keeps each rule's script lean and ensures the math (BH, signed Stouffer) is implemented
exactly once.

**Files:**
- Create: `code/scripts/select_lib.py`
- Create: `code/scripts/tests/test_select_lib.py`

- [ ] **Step 1: Write the failing test**

```python
# code/scripts/tests/test_select_lib.py
"""Unit tests for select_lib helpers."""
from __future__ import annotations

import math

import numpy as np
import pandas as pd
import pytest

import select_lib as lib


# ---- composite_sample_id ----

def test_composite_sample_id_format():
    assert lib.composite_sample_id("brca_tcga", "TCGA-A1") == "brca_tcga|TCGA-A1"


def test_composite_sample_id_pipe_in_input_raises():
    with pytest.raises(ValueError, match="pipe"):
        lib.composite_sample_id("brca|tcga", "s1")


# ---- build_sample_class ----

def test_build_sample_class_default_uses_study_only():
    samples = pd.DataFrame({
        "composite_sample_id": ["s|1", "s|2"],
        "study": ["a", "b"],
        "age_tertile": ["1", "2"],
    })
    out = lib.build_sample_class(samples, components=["study"])
    assert out.tolist() == ["a", "b"]
    assert out.index.tolist() == ["s|1", "s|2"]


def test_build_sample_class_compound():
    samples = pd.DataFrame({
        "composite_sample_id": ["s|1", "s|2"],
        "study": ["a", "b"],
        "age_tertile": ["1", "2"],
    })
    out = lib.build_sample_class(samples, components=["study", "age_tertile"])
    assert out.tolist() == ["a|1", "b|2"]


def test_build_sample_class_missing_component_raises():
    samples = pd.DataFrame({"composite_sample_id": ["x"], "study": ["a"]})
    with pytest.raises(KeyError, match="age_tertile"):
        lib.build_sample_class(samples, components=["study", "age_tertile"])


# ---- bh_fdr_within_groups ----

def test_bh_fdr_within_groups_recovers_known_q_values():
    """Two groups, each with [0.001, 0.5, 0.5] -> BH q [0.003, 0.5, 0.5]."""
    df = pd.DataFrame({
        "g": ["A", "A", "A", "B", "B", "B"],
        "p": [0.001, 0.5, 0.5, 0.01, 0.5, 0.5],
    })
    df["q"] = lib.bh_fdr_within_groups(df, group_cols=["g"], pvalue_col="p")
    a_qs = df[df["g"] == "A"]["q"].sort_values().tolist()
    np.testing.assert_allclose(a_qs, [0.003, 0.5, 0.5], rtol=1e-6)


def test_bh_fdr_within_groups_handles_nan():
    df = pd.DataFrame({"g": ["A"] * 4, "p": [0.001, 0.5, np.nan, 0.5]})
    df["q"] = lib.bh_fdr_within_groups(df, group_cols=["g"], pvalue_col="p")
    nan_q = df[df["p"].isna()]["q"].iloc[0]
    assert math.isnan(nan_q)


# ---- signed_stouffer ----

def test_signed_stouffer_all_positive_amplifies():
    """Three studies all CO with p=0.05 should give a stronger combined p."""
    z, p, n_used = lib.signed_stouffer(
        pvalues=np.array([0.05, 0.05, 0.05]),
        signs=np.array([+1, +1, +1]),
        weights=np.array([1.0, 1.0, 1.0]),
    )
    assert z > 0
    assert p < 0.05
    assert n_used == 3


def test_signed_stouffer_opposing_signs_cancel():
    """Three studies, half CO and half ME at the same p — combined Z near zero.

    This is the corrected expected behaviour per design Section 4.6 step 2 / risk #14.
    """
    z, p, n_used = lib.signed_stouffer(
        pvalues=np.array([0.01, 0.01, 0.01]),
        signs=np.array([+1, -1, +1]),
        weights=np.array([1.0, 1.0, 1.0]),
    )
    # 2 positive + 1 negative — partial cancellation, z still small relative to all-aligned
    assert abs(z) < 2.0
    z2, _, _ = lib.signed_stouffer(
        pvalues=np.array([0.01, 0.01, 0.01]),
        signs=np.array([+1, +1, +1]),
        weights=np.array([1.0, 1.0, 1.0]),
    )
    assert abs(z) < z2


def test_signed_stouffer_zero_sign_contributes_zero_z():
    """A study with direction=='none' gets sign 0 and contributes 0 weighted z."""
    z_with_none, _, _ = lib.signed_stouffer(
        pvalues=np.array([0.05, 0.5]),
        signs=np.array([+1, 0]),
        weights=np.array([1.0, 1.0]),
    )
    z_alone, _, _ = lib.signed_stouffer(
        pvalues=np.array([0.05]),
        signs=np.array([+1]),
        weights=np.array([1.0]),
    )
    # Adding a sign=0 study halves the weighted-z (denominator grows, numerator stays).
    assert abs(z_with_none) < abs(z_alone)


def test_signed_stouffer_drops_nan_pvalues():
    z, _, n_used = lib.signed_stouffer(
        pvalues=np.array([0.05, np.nan]),
        signs=np.array([+1, +1]),
        weights=np.array([1.0, 1.0]),
    )
    assert n_used == 1


# ---- direction_consensus_frac ----

def test_direction_consensus_frac():
    assert lib.direction_consensus_frac(["CO", "CO", "ME"]) == pytest.approx(2 / 3)
    assert lib.direction_consensus_frac(["CO", "CO", "CO"]) == 1.0
    assert lib.direction_consensus_frac(["CO", "ME"]) == 0.5
    # 'none' rows are excluded from the denominator (they carry no direction info).
    assert lib.direction_consensus_frac(["CO", "none", "none"]) == 1.0
    assert math.isnan(lib.direction_consensus_frac([]))
    assert math.isnan(lib.direction_consensus_frac(["none", "none"]))
```

- [ ] **Step 2: Run test to verify it fails**

```bash
uv run --frozen pytest code/scripts/tests/test_select_lib.py -v
```

Expected: FAIL on `ModuleNotFoundError`.

- [ ] **Step 3: Implement `code/scripts/select_lib.py`**

```python
# code/scripts/select_lib.py
"""Shared helpers for the t078 SELECT pipeline.

Functions are pure (no I/O) so they are easy to unit-test. I/O lives in the
per-rule scripts.
"""
from __future__ import annotations

from collections.abc import Sequence

import numpy as np
import pandas as pd
from scipy import stats


def composite_sample_id(study_id: str, sample_id: str) -> str:
    """Build the canonical (study_id, sample_id) composite key.

    Per design Section 1.3: row index of every per-cell GAM is
    "<study_id>|<sample_id>". The pipe is reserved.
    """
    if "|" in study_id or "|" in sample_id:
        raise ValueError(
            f"pipe character is reserved as the composite separator; "
            f"got study_id={study_id!r}, sample_id={sample_id!r}"
        )
    return f"{study_id}|{sample_id}"


def build_sample_class(
    samples: pd.DataFrame,
    components: Sequence[str],
) -> pd.Series:
    """Return a Series indexed by composite_sample_id with compound-label values.

    `components` controls the label assembly (design Section 4.4 / config key
    `select.sample_class_components`). The MVP uses ["study"]; t135 will pass
    ["study", "age_tertile"].
    """
    if "composite_sample_id" not in samples.columns:
        raise KeyError("samples must include composite_sample_id")
    for c in components:
        if c not in samples.columns:
            raise KeyError(f"component column not present in samples: {c!r}")
    parts = [samples[c].astype(str) for c in components]
    label = parts[0]
    for p in parts[1:]:
        label = label.str.cat(p, sep="|")
    return pd.Series(label.to_numpy(), index=samples["composite_sample_id"].to_numpy())


def bh_fdr_within_groups(
    df: pd.DataFrame,
    group_cols: Sequence[str],
    pvalue_col: str,
) -> pd.Series:
    """Benjamini-Hochberg FDR within groups; preserves NaN p-values as NaN q.

    Returns a Series aligned to df's index with the q-values.
    """
    out = pd.Series(np.nan, index=df.index, dtype="float64")
    for _, idx in df.groupby(list(group_cols), observed=True, sort=False).indices.items():
        sub = df.iloc[idx]
        mask = sub[pvalue_col].notna()
        if not mask.any():
            continue
        ps = sub.loc[mask, pvalue_col].to_numpy()
        # BH: q_i = min over j>=i of p_(j) * n / j (after sorting ascending).
        order = np.argsort(ps, kind="stable")
        n = len(ps)
        sorted_ps = ps[order]
        ranks = np.arange(1, n + 1)
        raw = sorted_ps * n / ranks
        # cumulative min from right to left, then clip at 1.
        adj = np.minimum.accumulate(raw[::-1])[::-1]
        adj = np.clip(adj, 0.0, 1.0)
        # restore original order.
        unsorted = np.empty_like(adj)
        unsorted[order] = adj
        out.iloc[idx[mask.to_numpy()]] = unsorted
    return out


def signed_stouffer(
    pvalues: np.ndarray,
    signs: np.ndarray,
    weights: np.ndarray,
) -> tuple[float, float, int]:
    """Sign-aware weighted-Z (Stouffer) combination.

    Returns (combined_z, two_sided_p, n_used). NaN p-values are dropped. Per
    design Section 4.6 step 2: opposing signs cancel by design — the caller
    is responsible for the separate direction-consensus diagnostic.

    Each input p is converted to a two-sided z = qnorm(1 - p/2) and signed
    with the corresponding sign in {-1, 0, +1}; sign==0 contributes a z of 0
    and still consumes weight.
    """
    pvalues = np.asarray(pvalues, dtype=float)
    signs = np.asarray(signs, dtype=float)
    weights = np.asarray(weights, dtype=float)

    mask = ~np.isnan(pvalues)
    n_used = int(mask.sum())
    if n_used == 0:
        return float("nan"), float("nan"), 0

    p = pvalues[mask]
    s = signs[mask]
    w = weights[mask]

    # Two-sided z. Clamp p to avoid inf at p == 0 / 1.
    p = np.clip(p, 1e-300, 1.0 - 1e-15)
    z_unsigned = stats.norm.isf(p / 2.0)
    z_signed = s * z_unsigned

    z_combined = float(np.sum(w * z_signed) / np.sqrt(np.sum(w * w)))
    p_combined = float(2.0 * stats.norm.sf(abs(z_combined)))
    return z_combined, p_combined, n_used


def direction_consensus_frac(directions: Sequence[str]) -> float:
    """Fraction of contributing studies that agreed on the dominant non-'none' direction.

    Returns NaN when no study reports a CO/ME direction.
    """
    items = [d for d in directions if d in ("CO", "ME")]
    if not items:
        return float("nan")
    n_co = items.count("CO")
    n_me = items.count("ME")
    return max(n_co, n_me) / len(items)
```

- [ ] **Step 4: Add the scipy + numpy deps if not already present**

```bash
uv run python -c "import scipy.stats, numpy"
```

If this fails, add via `uv add scipy numpy`. They are almost certainly already in
the project dep set — check `pyproject.toml` first.

- [ ] **Step 5: Run tests + lint**

```bash
uv run --frozen pytest code/scripts/tests/test_select_lib.py -v
uv run --frozen ruff check code/scripts/select_lib.py
uv run --frozen ruff format --check code/scripts/select_lib.py
```

Expected: 12 PASS, lint clean.

- [ ] **Step 6: Commit**

```bash
git add code/scripts/select_lib.py code/scripts/tests/test_select_lib.py
git commit -m "$(cat <<'EOF'
feat(t078): select_lib.py shared helpers (composite_sample_id,
build_sample_class, bh_fdr_within_groups, signed_stouffer,
direction_consensus_frac)

Pure-functional helpers used by build_select_gam.py and
aggregate_select_results.py. Tests cover the design-critical edge
cases: signed Stouffer cancels opposing signs (Section 4.6 step 2 +
risk #14); direction_consensus_frac excludes 'none' directions from
the denominator; build_sample_class is the t135 extension point.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 9: Implement rule (2) `build_select_gam.py` — core B-tier cell

**Why:** This is the workhorse of the input layer. It assembles one SELECT-ready cell
(GAM + sample_class + alteration_class + cell_metadata) for one
`(cancer_type, tier=B, cohort)` combination. We start with the simplest path — B-tier,
single-panel, inclusive cohort — and add complexity in subsequent tasks.

**Files:**
- Create: `code/scripts/build_select_gam.py`
- Create: `code/scripts/tests/test_build_select_gam.py`

- [ ] **Step 1: Write the failing test**

```python
# code/scripts/tests/test_build_select_gam.py
"""Unit tests for build_select_gam — core B-tier path."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pyarrow.feather as feather
import pytest

import build_select_gam as mod
import select_lib as lib


@pytest.fixture
def fixture_studies(tmp_path: Path):
    """Two-study fixture: 60 LUAD samples (30 per study), 5 genes, single panel."""
    rows = []
    for sid, prefix in [("st1", "A"), ("st2", "B")]:
        for i in range(30):
            sample_id = f"{prefix}{i:02d}"
            rows.append({
                "study_id": sid,
                "sample_id": sample_id,
                "composite_sample_id": lib.composite_sample_id(sid, sample_id),
                "cancer_type": "luad",
                "is_hypermutator": False,
            })
    samples = pd.DataFrame(rows)

    # Per-sample mutation calls. Construct a deliberate co-occurrence pattern
    # so we can later validate semantics: TP53 mutated in ~50%, KRAS in ~30%,
    # both together more often than independent in study A.
    rng = pd.RangeIndex(len(samples))
    mut = pd.DataFrame({
        "composite_sample_id": samples["composite_sample_id"],
        "TP53": rng.map(lambda i: i % 2 == 0),
        "KRAS": rng.map(lambda i: i % 3 == 0),
        "EGFR": rng.map(lambda i: i % 4 == 0),
        "BRAF": rng.map(lambda i: i % 5 == 0),
        "ZZTOPLOWFREQ": [False] * (len(samples) - 1) + [True],  # mutated in 1 sample
    })

    # Single panel that covers every gene for every sample.
    panel_map = pd.DataFrame({
        "study_id": samples["study_id"],
        "sample_id": samples["sample_id"],
        "panel_id": ["panel_x"] * len(samples),
        "panel_source": ["study_panels_tsv"] * len(samples),
    })
    panel_genes = pd.DataFrame({
        "symbol": ["TP53", "KRAS", "EGFR", "BRAF", "ZZTOPLOWFREQ"],
        "callable": [True] * 5,
        "panel_id": ["panel_x"] * 5,
        "source": ["bed"] * 5,
    })

    return samples, mut, panel_map, panel_genes


def test_build_b_inclusive_cell_basic_shape(tmp_path: Path, fixture_studies):
    samples, mut, panel_map, panel_genes = fixture_studies
    out = tmp_path / "cell"
    mod.build_b_tier_cell(
        cancer_type="luad",
        cohort="inclusive",
        samples=samples,
        mutation_long=_to_long(mut),
        sample_panel_map=panel_map,
        panel_gene_sets={"panel_x": panel_genes},
        gene_universe=pd.DataFrame({
            "symbol": ["TP53", "KRAS", "EGFR", "BRAF", "ZZTOPLOWFREQ", "OTHER"],
            "from_bailey": [True] * 6,
            "from_cgc": [False] * 6,
            "from_sanchez_vega": [False] * 6,
            "from_custom": [False] * 6,
        }),
        ch_priority_genes=set(),
        sample_class_components=["study_id"],
        thresholds=mod.Thresholds(
            min_stratum_samples=30,
            min_gene_prevalence_frac=0.03,
            min_gene_prevalence_count=3,
            study_residual_threshold_frac=0.10,
        ),
        out_dir=out,
    )

    gam = pd.read_feather(out / "gam.feather")
    sc  = pd.read_feather(out / "sample_class.feather")
    ac  = pd.read_feather(out / "alteration_class.feather")
    meta = json.loads((out / "cell_metadata.json").read_text())

    # Orientation: rows = samples, cols = genes (design Section 1.2).
    assert gam.shape[0] == 60                        # 60 samples
    # ZZTOPLOWFREQ mutated in 1 sample (<3 absolute count) -> dropped.
    assert "ZZTOPLOWFREQ" not in gam.columns
    # 4 surviving genes.
    assert sorted(c for c in gam.columns if c != "composite_sample_id") == [
        "BRAF", "EGFR", "KRAS", "TP53"
    ]
    assert sc.shape[0] == 60
    assert ac.shape[0] == 4
    assert meta["skip_reason"] is None
    assert meta["n_samples"] == 60
    assert meta["n_genes"] == 4


def test_b_cell_below_stratum_threshold_writes_sentinel(tmp_path: Path, fixture_studies):
    samples, mut, panel_map, panel_genes = fixture_studies
    samples_small = samples.head(20)  # below 30
    mut_long = _to_long(_subset(mut, samples_small))
    out = tmp_path / "cell_small"
    mod.build_b_tier_cell(
        cancer_type="luad",
        cohort="inclusive",
        samples=samples_small,
        mutation_long=mut_long,
        sample_panel_map=panel_map,
        panel_gene_sets={"panel_x": panel_genes},
        gene_universe=pd.DataFrame({"symbol": ["TP53"], "from_bailey": [True],
                                     "from_cgc": [False], "from_sanchez_vega": [False],
                                     "from_custom": [False]}),
        ch_priority_genes=set(),
        sample_class_components=["study_id"],
        thresholds=mod.Thresholds(min_stratum_samples=30,
                                  min_gene_prevalence_frac=0.03,
                                  min_gene_prevalence_count=3,
                                  study_residual_threshold_frac=0.10),
        out_dir=out,
    )

    meta = json.loads((out / "cell_metadata.json").read_text())
    assert meta["skip_reason"] == "n_samples_below_threshold"
    # Empty placeholder feathers must exist for DAG safety (Section 1.5).
    for fn in ["gam.feather", "sample_class.feather", "alteration_class.feather"]:
        assert (out / fn).exists()


def _to_long(wide: pd.DataFrame) -> pd.DataFrame:
    """Convert a wide (sample × gene) bool table to (composite_sample_id, gene) long."""
    long = wide.melt(
        id_vars=["composite_sample_id"], var_name="symbol", value_name="mutated"
    )
    return long[long["mutated"]][["composite_sample_id", "symbol"]].reset_index(drop=True)


def _subset(wide: pd.DataFrame, samples: pd.DataFrame) -> pd.DataFrame:
    return wide[wide["composite_sample_id"].isin(samples["composite_sample_id"])]
```

- [ ] **Step 2: Run test to verify it fails**

```bash
uv run --frozen pytest code/scripts/tests/test_build_select_gam.py -v
```

Expected: FAIL on `ModuleNotFoundError`.

- [ ] **Step 3: Implement `code/scripts/build_select_gam.py` (core only)**

Note: the full script also handles A-tier scattering (Task 10) and pathway-aggregated
sibling output (Task 11). This task implements `build_b_tier_cell()` and shared
machinery; the next two tasks extend the same file.

```python
# code/scripts/build_select_gam.py
"""Rule (2): build per-cell SELECT inputs (GAM + sample.class + alteration.class).

See doc/plans/2026-04-25-t078-select-cooccurrence-design.md Section 4.4.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

import select_lib as lib


@dataclass(frozen=True, slots=True)
class Thresholds:
    min_stratum_samples: int
    min_gene_prevalence_frac: float
    min_gene_prevalence_count: int
    study_residual_threshold_frac: float


SKIP_INSUFFICIENT_SAMPLES = "n_samples_below_threshold"
SKIP_INSUFFICIENT_GENES = "insufficient_genes"


def _write_cell_outputs(
    out_dir: Path,
    gam: pd.DataFrame,
    sample_class: pd.DataFrame,
    alteration_class: pd.DataFrame,
    metadata: dict,
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    gam.to_feather(out_dir / "gam.feather")
    sample_class.to_feather(out_dir / "sample_class.feather")
    alteration_class.to_feather(out_dir / "alteration_class.feather")
    (out_dir / "cell_metadata.json").write_text(json.dumps(metadata, indent=2))


def _empty_outputs(out_dir: Path, skip_reason: str, n_samples: int = 0) -> None:
    """Write zero-row placeholder feathers + a populated cell_metadata.json."""
    gam = pd.DataFrame({"composite_sample_id": pd.Series(dtype="string")})
    sample_class = pd.DataFrame({
        "composite_sample_id": pd.Series(dtype="string"),
        "sample_class": pd.Series(dtype="string"),
    })
    alteration_class = pd.DataFrame({
        "symbol": pd.Series(dtype="string"),
        "alteration_class": pd.Series(dtype="string"),
    })
    metadata = {
        "skip_reason": skip_reason,
        "n_samples": n_samples,
        "n_genes": 0,
        "panel_intersection_size": 0,
    }
    _write_cell_outputs(out_dir, gam, sample_class, alteration_class, metadata)


def _intersect_panel_genes(
    panel_ids_in_cell: pd.Series,
    panel_gene_sets: dict[str, pd.DataFrame],
) -> set[str]:
    """Return symbols callable on every panel present in the cell."""
    unique_panels = panel_ids_in_cell.drop_duplicates().tolist()
    if not unique_panels:
        return set()
    sets = []
    for pid in unique_panels:
        if pid not in panel_gene_sets:
            raise KeyError(f"panel_gene_sets missing entry for panel_id={pid!r}")
        ps = panel_gene_sets[pid]
        sets.append(set(ps.loc[ps["callable"], "symbol"]))
    return set.intersection(*sets)


def _bucket_residual_studies(
    sample_class: pd.Series,
    threshold_frac: float,
) -> pd.Series:
    """Fold studies contributing < threshold_frac of samples into 'study_residual'."""
    counts = sample_class.value_counts()
    n = counts.sum()
    big = counts[counts / n >= threshold_frac].index
    return sample_class.where(sample_class.isin(big), other="study_residual")


def build_b_tier_cell(
    cancer_type: str,
    cohort: str,
    samples: pd.DataFrame,
    mutation_long: pd.DataFrame,
    sample_panel_map: pd.DataFrame,
    panel_gene_sets: dict[str, pd.DataFrame],
    gene_universe: pd.DataFrame,
    ch_priority_genes: set[str],
    sample_class_components: list[str],
    thresholds: Thresholds,
    out_dir: Path,
) -> None:
    """Build one B-tier cell (cancer_type, cohort) of the SELECT input layer.

    samples:               (study_id, sample_id, composite_sample_id, cancer_type,
                            is_hypermutator, ...)
    mutation_long:         (composite_sample_id, symbol)
    sample_panel_map:      (study_id, sample_id, panel_id, panel_source)
    panel_gene_sets:       dict panel_id -> DataFrame(symbol, callable, ...)
    gene_universe:         result of rule (1b) build_select_gene_universe.
    ch_priority_genes:     boolean filter for cohort=='exclusive'.
    sample_class_components: ["study_id"] in MVP; t135 will add age_tertile.
    """
    cohort_samples = samples[samples["cancer_type"] == cancer_type]
    if cohort == "exclusive":
        cohort_samples = cohort_samples[~cohort_samples["is_hypermutator"]]

    n_samples = len(cohort_samples)
    if n_samples < thresholds.min_stratum_samples:
        _empty_outputs(out_dir, SKIP_INSUFFICIENT_SAMPLES, n_samples=n_samples)
        return

    # Determine panel intersection across the cell's samples.
    sp = sample_panel_map.merge(
        cohort_samples[["study_id", "sample_id"]],
        on=["study_id", "sample_id"], how="inner", validate="one_to_one",
    )
    callable_genes = _intersect_panel_genes(sp["panel_id"], panel_gene_sets)

    # Restrict to gene universe.
    universe_set = set(gene_universe["symbol"])
    candidate_genes = callable_genes & universe_set
    if cohort == "exclusive":
        candidate_genes -= ch_priority_genes

    # Build wide GAM in samples × candidate_genes.
    sample_ids = cohort_samples["composite_sample_id"].tolist()
    relevant = mutation_long[mutation_long["symbol"].isin(candidate_genes)]
    relevant = relevant[relevant["composite_sample_id"].isin(sample_ids)]
    gam_long = relevant.assign(value=True)
    gam = (
        gam_long.pivot_table(
            index="composite_sample_id", columns="symbol",
            values="value", fill_value=False, aggfunc="any",
        )
        .reindex(index=sample_ids, columns=sorted(candidate_genes))
        .fillna(False)
        .astype(bool)
    )
    gam.index.name = "composite_sample_id"

    # Prevalence floor.
    counts = gam.sum(axis=0)
    fracs = counts / n_samples
    keep_genes = (
        (counts >= thresholds.min_gene_prevalence_count)
        & (fracs >= thresholds.min_gene_prevalence_frac)
        & (counts < n_samples)  # drop fully-mutated
    )
    gam = gam.loc[:, keep_genes[keep_genes].index]

    if gam.shape[1] < 5:
        _empty_outputs(out_dir, SKIP_INSUFFICIENT_GENES, n_samples=n_samples)
        return

    # sample.class
    cohort_samples = cohort_samples.set_index("composite_sample_id", drop=False)
    sample_class = lib.build_sample_class(cohort_samples, components=sample_class_components)
    sample_class = _bucket_residual_studies(
        sample_class, thresholds.study_residual_threshold_frac
    )

    sample_class_df = pd.DataFrame({
        "composite_sample_id": sample_class.index,
        "sample_class": sample_class.values.astype(str),
    })

    # alteration.class — left as 'unknown' in this task; Bailey driver overlay
    # is wired in Task 10 once we accept the Bailey TSV input.
    alteration_class_df = pd.DataFrame({
        "symbol": gam.columns.astype(str),
        "alteration_class": "unknown",
    })

    metadata = {
        "skip_reason": None,
        "n_samples": int(n_samples),
        "n_genes": int(gam.shape[1]),
        "panel_intersection_size": int(len(callable_genes)),
        "panels_in_cell": sorted(set(sp["panel_id"])),
        "studies_in_cell": sorted(set(cohort_samples["study_id"])),
    }

    # Reset the index so feather can write it cleanly.
    gam_out = gam.reset_index()
    _write_cell_outputs(out_dir, gam_out, sample_class_df, alteration_class_df, metadata)


if "snakemake" in globals():  # pragma: no cover  # set by Snakemake's script: directive
    raise NotImplementedError(
        "Snakemake entry point wired in Task 10 once A-tier scattering lands."
    )
```

- [ ] **Step 4: Run tests + lint**

```bash
uv run --frozen pytest code/scripts/tests/test_build_select_gam.py -v
uv run --frozen ruff check code/scripts/build_select_gam.py
uv run --frozen ruff format --check code/scripts/build_select_gam.py
```

Expected: 2 PASS, lint clean.

- [ ] **Step 5: Commit**

```bash
git add code/scripts/build_select_gam.py code/scripts/tests/test_build_select_gam.py
git commit -m "$(cat <<'EOF'
feat(t078): rule (2) build_select_gam.py — B-tier core

Implements build_b_tier_cell() for the simplest path: one cancer_type ×
one cohort, multi-panel intersection, prevalence floor, study_residual
bucketing, samples × genes orientation per design Section 1.2.
Sentinel feathers + cell_metadata.json populated when n_samples < 30
(skip_reason='n_samples_below_threshold') or n_genes < 5 (skip_reason=
'insufficient_genes'), satisfying the Section 1.5 DAG-safety contract.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 10: Extend rule (2) — A-tier scattering + Bailey alteration_class + Snakemake entry point

**Why:** A-tier cells share the same machinery as B-tier but stratify additionally on a
single study. Also wires the alteration_class (oncogene/tsg/dual/unknown) per design
Section 4.4 step 8, and adds the Snakemake entry point that wraps the per-cell logic.

**Files:**
- Modify: `code/scripts/build_select_gam.py`
- Modify: `code/scripts/tests/test_build_select_gam.py`

- [ ] **Step 1: Add failing tests**

```python
# Append to code/scripts/tests/test_build_select_gam.py

def test_a_tier_filters_to_single_study(tmp_path: Path, fixture_studies):
    samples, mut, panel_map, panel_genes = fixture_studies
    out = tmp_path / "cell_a"
    mod.build_a_tier_cell(
        cancer_type="luad",
        cohort="inclusive",
        study="st1",
        samples=samples,
        mutation_long=_to_long(mut),
        sample_panel_map=panel_map,
        panel_gene_sets={"panel_x": panel_genes},
        gene_universe=pd.DataFrame({
            "symbol": ["TP53", "KRAS", "EGFR", "BRAF", "ZZTOPLOWFREQ"],
            "from_bailey": [True] * 5,
            "from_cgc": [False] * 5,
            "from_sanchez_vega": [False] * 5,
            "from_custom": [False] * 5,
        }),
        ch_priority_genes=set(),
        sample_class_components=["study_id"],
        thresholds=mod.Thresholds(
            min_stratum_samples=30,
            min_gene_prevalence_frac=0.03,
            min_gene_prevalence_count=3,
            study_residual_threshold_frac=0.10,
        ),
        out_dir=out,
    )
    sc = pd.read_feather(out / "sample_class.feather")
    # Only 30 samples from study st1.
    assert len(sc) == 30
    assert (sc["sample_class"] == "st1").all()


def test_alteration_class_uses_bailey_when_provided(tmp_path: Path, fixture_studies):
    samples, mut, panel_map, panel_genes = fixture_studies
    bailey_drivers = pd.DataFrame({
        "symbol":          ["TP53", "KRAS", "EGFR", "BRAF"],
        "alteration_class": ["tsg",  "oncogene", "oncogene", "oncogene"],
    })
    out = tmp_path / "cell_b_with_bailey"
    mod.build_b_tier_cell(
        cancer_type="luad", cohort="inclusive", samples=samples,
        mutation_long=_to_long(mut), sample_panel_map=panel_map,
        panel_gene_sets={"panel_x": panel_genes},
        gene_universe=pd.DataFrame({
            "symbol": ["TP53", "KRAS", "EGFR", "BRAF", "ZZTOPLOWFREQ"],
            "from_bailey": [True] * 5, "from_cgc": [False] * 5,
            "from_sanchez_vega": [False] * 5, "from_custom": [False] * 5,
        }),
        ch_priority_genes=set(), sample_class_components=["study_id"],
        thresholds=mod.Thresholds(min_stratum_samples=30,
                                  min_gene_prevalence_frac=0.03,
                                  min_gene_prevalence_count=3,
                                  study_residual_threshold_frac=0.10),
        out_dir=out,
        bailey_alteration_class=bailey_drivers,
    )
    ac = pd.read_feather(out / "alteration_class.feather")
    cls = ac.set_index("symbol")["alteration_class"].to_dict()
    assert cls["TP53"] == "tsg"
    assert cls["KRAS"] == "oncogene"
```

- [ ] **Step 2: Run to verify they fail**

```bash
uv run --frozen pytest code/scripts/tests/test_build_select_gam.py -v
```

Expected: 2 new FAIL on missing `build_a_tier_cell` and `bailey_alteration_class` arg.

- [ ] **Step 3: Extend `build_select_gam.py`**

Add the following, including modifying `build_b_tier_cell` to accept an optional
`bailey_alteration_class` parameter and use it when provided.

```python
# Inside build_select_gam.py, add `bailey_alteration_class` param to build_b_tier_cell:

def build_b_tier_cell(
    cancer_type: str,
    cohort: str,
    samples: pd.DataFrame,
    mutation_long: pd.DataFrame,
    sample_panel_map: pd.DataFrame,
    panel_gene_sets: dict[str, pd.DataFrame],
    gene_universe: pd.DataFrame,
    ch_priority_genes: set[str],
    sample_class_components: list[str],
    thresholds: Thresholds,
    out_dir: Path,
    bailey_alteration_class: pd.DataFrame | None = None,  # NEW
) -> None:
    ...  # existing body — replace the alteration_class section with:

    # alteration.class — Bailey-derived if provided, else 'unknown'.
    if bailey_alteration_class is not None:
        cls_lookup = bailey_alteration_class.set_index("symbol")["alteration_class"]
        alteration_class_series = (
            pd.Series(gam.columns).map(cls_lookup).fillna("unknown")
        )
    else:
        alteration_class_series = pd.Series(["unknown"] * gam.shape[1])
    alteration_class_df = pd.DataFrame({
        "symbol": gam.columns.astype(str),
        "alteration_class": alteration_class_series.astype(str).values,
    })
    ...


def build_a_tier_cell(
    cancer_type: str,
    cohort: str,
    study: str,
    samples: pd.DataFrame,
    mutation_long: pd.DataFrame,
    sample_panel_map: pd.DataFrame,
    panel_gene_sets: dict[str, pd.DataFrame],
    gene_universe: pd.DataFrame,
    ch_priority_genes: set[str],
    sample_class_components: list[str],
    thresholds: Thresholds,
    out_dir: Path,
    bailey_alteration_class: pd.DataFrame | None = None,
) -> None:
    """Same as build_b_tier_cell but pre-filtered to a single study."""
    sub = samples[samples["study_id"] == study].copy()
    build_b_tier_cell(
        cancer_type=cancer_type, cohort=cohort, samples=sub,
        mutation_long=mutation_long, sample_panel_map=sample_panel_map,
        panel_gene_sets=panel_gene_sets, gene_universe=gene_universe,
        ch_priority_genes=ch_priority_genes,
        sample_class_components=sample_class_components, thresholds=thresholds,
        out_dir=out_dir, bailey_alteration_class=bailey_alteration_class,
    )
```

Replace the Snakemake entry point at the bottom of the file:

```python
if "snakemake" in globals():  # pragma: no cover  # set by Snakemake's script: directive
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821

    cancer_type = snek.wildcards["cancer_type"]
    tier        = snek.wildcards["tier"]                # 'B' or 'A'
    cohort      = snek.wildcards["cohort"]              # 'inclusive' or 'exclusive'
    study       = snek.wildcards.get("study")           # only for tier == 'A'

    samples = pd.read_feather(snek.input["samples_annotated"])
    mutation_long = pd.read_feather(snek.input["mutation_long"])
    sample_panel_map = pd.read_feather(snek.input["sample_panel_map"])
    gene_universe = pd.read_csv(snek.input["gene_universe"], sep="\t")

    panel_gene_sets: dict[str, pd.DataFrame] = {}
    for path in snek.input["panel_gene_sets"]:
        df = pd.read_feather(path)
        if df.empty:
            continue
        pid = df["panel_id"].iloc[0]
        panel_gene_sets[pid] = df

    bailey = pd.read_feather(snek.input["bailey_alteration_class"]) \
        if "bailey_alteration_class" in snek.input.keys() else None

    ch_genes = set(snek.params.get("ch_priority_genes", []))
    sc_components = list(snek.params["sample_class_components"])
    thresholds = Thresholds(**snek.params["thresholds"])
    out_dir = Path(snek.output["cell_dir"])

    if tier == "B":
        build_b_tier_cell(
            cancer_type=cancer_type, cohort=cohort, samples=samples,
            mutation_long=mutation_long, sample_panel_map=sample_panel_map,
            panel_gene_sets=panel_gene_sets, gene_universe=gene_universe,
            ch_priority_genes=ch_genes,
            sample_class_components=sc_components, thresholds=thresholds,
            out_dir=out_dir, bailey_alteration_class=bailey,
        )
    elif tier == "A":
        if study is None:
            raise ValueError("A-tier cells require a 'study' wildcard")
        build_a_tier_cell(
            cancer_type=cancer_type, cohort=cohort, study=study,
            samples=samples, mutation_long=mutation_long,
            sample_panel_map=sample_panel_map,
            panel_gene_sets=panel_gene_sets, gene_universe=gene_universe,
            ch_priority_genes=ch_genes,
            sample_class_components=sc_components, thresholds=thresholds,
            out_dir=out_dir, bailey_alteration_class=bailey,
        )
    else:
        raise ValueError(f"unknown tier: {tier!r}")
```

- [ ] **Step 4: Run tests + lint**

```bash
uv run --frozen pytest code/scripts/tests/test_build_select_gam.py -v
uv run --frozen ruff check code/scripts/build_select_gam.py
uv run --frozen ruff format --check code/scripts/build_select_gam.py
```

Expected: 4 PASS, lint clean.

- [ ] **Step 5: Commit**

```bash
git add code/scripts/build_select_gam.py code/scripts/tests/test_build_select_gam.py
git commit -m "$(cat <<'EOF'
feat(t078): build_select_gam.py — A-tier + Bailey alteration class

Adds build_a_tier_cell() that wraps build_b_tier_cell with a single-
study pre-filter (per design Section 4.4). Adds optional
bailey_alteration_class parameter so SELECT receives oncogene/tsg/dual
labels per Section 4.4 step 8. Wires the Snakemake entry point that
dispatches on the 'tier' wildcard ('B'|'A').

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 11: Extend rule (2) — pathway-aggregated sibling GAM

**Why:** Rule (5) (`run_select_pathway_aggregated.R`) consumes a separate `samples × 10`
GAM where each cell is `1` iff any gene in that pathway is mutated. Per design
Section 4.4 final paragraph, this is a sibling output of rule (2) on the
B-tier-exclusive cohort only.

**Files:**
- Modify: `code/scripts/build_select_gam.py`
- Modify: `code/scripts/tests/test_build_select_gam.py`

- [ ] **Step 1: Add failing test**

```python
# Append to code/scripts/tests/test_build_select_gam.py

def test_pathway_aggregated_gam_or_semantics(tmp_path: Path, fixture_studies):
    samples, mut, panel_map, panel_genes = fixture_studies
    pathways = pd.DataFrame({
        "symbol":  ["TP53", "KRAS", "BRAF",   "EGFR"],
        "pathway": ["P53",  "RTK_RAS", "RTK_RAS", "RTK_RAS"],
    })
    out = tmp_path / "pa"
    mod.build_pathway_aggregated_gam(
        cancer_type="luad",
        samples=samples,
        mutation_long=_to_long(mut),
        sample_panel_map=panel_map,
        panel_gene_sets={"panel_x": panel_genes},
        pathway_membership=pathways,
        ch_priority_genes=set(),
        thresholds=mod.Thresholds(
            min_stratum_samples=30,
            min_gene_prevalence_frac=0.03,
            min_gene_prevalence_count=3,
            study_residual_threshold_frac=0.10,
        ),
        out_dir=out,
    )
    pa_gam = pd.read_feather(out / "pathway_aggregated" / "gam.feather")
    # Samples × 2 pathways.
    assert "P53" in pa_gam.columns
    assert "RTK_RAS" in pa_gam.columns
    # Sample with TP53 mutation has P53=True; sample with KRAS has RTK_RAS=True.
    sample_a00 = pa_gam[pa_gam["composite_sample_id"] == "st1|A00"].iloc[0]
    # A00 index 0 -> TP53 (i%2==0), KRAS (i%3==0), EGFR (i%4==0), BRAF (i%5==0). All True.
    assert bool(sample_a00["P53"]) is True
    assert bool(sample_a00["RTK_RAS"]) is True
```

- [ ] **Step 2: Run to verify it fails**

```bash
uv run --frozen pytest code/scripts/tests/test_build_select_gam.py::test_pathway_aggregated_gam_or_semantics -v
```

Expected: FAIL on missing `build_pathway_aggregated_gam`.

- [ ] **Step 3: Add `build_pathway_aggregated_gam` to `build_select_gam.py`**

```python
def build_pathway_aggregated_gam(
    cancer_type: str,
    samples: pd.DataFrame,
    mutation_long: pd.DataFrame,
    sample_panel_map: pd.DataFrame,
    panel_gene_sets: dict[str, pd.DataFrame],
    pathway_membership: pd.DataFrame,        # cols: symbol, pathway
    ch_priority_genes: set[str],
    thresholds: Thresholds,
    out_dir: Path,
) -> None:
    """Pathway-aggregated GAM (samples × 10 pathways), B-tier-exclusive cohort only."""
    cohort_samples = samples[
        (samples["cancer_type"] == cancer_type) & (~samples["is_hypermutator"])
    ]
    n_samples = len(cohort_samples)
    out_dir = Path(out_dir) / "pathway_aggregated"
    if n_samples < thresholds.min_stratum_samples:
        _empty_outputs(out_dir, SKIP_INSUFFICIENT_SAMPLES, n_samples=n_samples)
        return

    sp = sample_panel_map.merge(
        cohort_samples[["study_id", "sample_id"]],
        on=["study_id", "sample_id"], how="inner", validate="one_to_one",
    )
    callable_genes = _intersect_panel_genes(sp["panel_id"], panel_gene_sets)
    callable_genes -= ch_priority_genes

    # Restrict pathway membership to callable genes only.
    pm = pathway_membership[pathway_membership["symbol"].isin(callable_genes)]

    sample_ids = cohort_samples["composite_sample_id"].tolist()
    relevant = mutation_long[mutation_long["symbol"].isin(set(pm["symbol"]))]
    relevant = relevant[relevant["composite_sample_id"].isin(sample_ids)]

    # Join mutation events to pathways.
    joined = relevant.merge(pm, on="symbol", how="inner")
    pa_long = joined[["composite_sample_id", "pathway"]].drop_duplicates()
    pa_long["value"] = True

    pathways = sorted(set(pm["pathway"]))
    gam = (
        pa_long.pivot_table(
            index="composite_sample_id", columns="pathway",
            values="value", fill_value=False, aggfunc="any",
        )
        .reindex(index=sample_ids, columns=pathways)
        .fillna(False)
        .astype(bool)
    )
    gam.index.name = "composite_sample_id"

    sample_class = pd.DataFrame({
        "composite_sample_id": gam.index.tolist(),
        "sample_class": cohort_samples.set_index("composite_sample_id")
                                       .loc[gam.index, "study_id"].astype(str).values,
    })
    alteration_class = pd.DataFrame({
        "symbol": pathways,
        "alteration_class": "unknown",
    })
    metadata = {
        "skip_reason": None,
        "n_samples": int(n_samples),
        "n_genes": int(gam.shape[1]),
        "panel_intersection_size": int(len(callable_genes)),
        "kind": "pathway_aggregated",
    }
    _write_cell_outputs(out_dir, gam.reset_index(), sample_class, alteration_class, metadata)
```

- [ ] **Step 4: Run tests + lint**

```bash
uv run --frozen pytest code/scripts/tests/test_build_select_gam.py -v
uv run --frozen ruff check code/scripts/build_select_gam.py
uv run --frozen ruff format --check code/scripts/build_select_gam.py
```

Expected: 5 PASS, lint clean.

- [ ] **Step 5: Commit**

```bash
git add code/scripts/build_select_gam.py code/scripts/tests/test_build_select_gam.py
git commit -m "$(cat <<'EOF'
feat(t078): build_select_gam.py — pathway-aggregated sibling GAM

Adds build_pathway_aggregated_gam() emitting the samples × pathways
binary OR matrix consumed by rule (5). B-tier-exclusive cohort only
(hypermutator-inclusive aggregation is biologically un-interpretable —
hypermutators saturate every pathway). Pathway membership restricted
to genes callable in the panel intersection so the matrix is internally
consistent with the gene-pair GAM.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 12: Implement rule (3) `run_select.R` wrapper

**Why:** R-side wrapper that calls `select::select(...)` per design Section 4.5 with the
exact parameter names and column mapping verified against v1.6.4 source. Sentinel-aware:
skipped cells write a one-row sentinel feather.

**Files:**
- Create: `code/scripts/run_select.R`
- Create: `code/scripts/tests/test_run_select.R` (testthat)

The R-side test depends on the conda env being available locally. The CI flow is:
preflight rule (Task 4) installs SELECT into the env at `validate.sh --slow` time;
this task's test is in the same `--slow` tier.

- [ ] **Step 1: Write the failing R test (testthat)**

```r
# code/scripts/tests/test_run_select.R
#
# testthat tests for run_select.R sentinel handling and column mapping.
# Run via: Rscript code/scripts/tests/test_run_select.R (inside the SELECT conda env).

suppressPackageStartupMessages({
  library(testthat)
  library(arrow)
  library(jsonlite)
})

scripts_dir <- file.path(here::here(), "code", "scripts")
source(file.path(scripts_dir, "run_select.R"), local = TRUE)  # exposes run_one_cell()

write_sentinel_inputs <- function(dir, skip_reason) {
  dir.create(dir, recursive = TRUE, showWarnings = FALSE)
  arrow::write_feather(
    data.frame(composite_sample_id = character(0)),
    file.path(dir, "gam.feather"))
  arrow::write_feather(
    data.frame(composite_sample_id = character(0), sample_class = character(0)),
    file.path(dir, "sample_class.feather"))
  arrow::write_feather(
    data.frame(symbol = character(0), alteration_class = character(0)),
    file.path(dir, "alteration_class.feather"))
  jsonlite::write_json(
    list(skip_reason = skip_reason, n_samples = 0L, n_genes = 0L,
         panel_intersection_size = 0L),
    path = file.path(dir, "cell_metadata.json"), auto_unbox = TRUE)
}

test_that("sentinel passthrough writes empty pair_stats with skip_reason", {
  td <- tempfile("sel_test_")
  in_dir  <- file.path(td, "in")
  out_dir <- file.path(td, "out")
  write_sentinel_inputs(in_dir, "n_samples_below_threshold")

  run_one_cell(
    cell_dir       = in_dir,
    out_path       = file.path(out_dir, "pair_stats.feather"),
    cell_descriptor = list(
      cancer_type = "luad", tier = "B", study = NA,
      cohort = "inclusive"),
    runtime_config = list(
      n_permut = 50, n_cores = 1, max_memory_size_gb = 8,
      randomization_switch_threshold = 30,
      min_feature_support = 5, min_feature_freq = 0.001,
      save_intermediate_files = FALSE),
    random_seed = 0L)

  out <- arrow::read_feather(file.path(out_dir, "pair_stats.feather"))
  expect_equal(nrow(out), 1)
  expect_equal(out$skip_reason[[1]], "n_samples_below_threshold")
  expect_true(is.na(out$select_score[[1]]))
})

test_that("non-sentinel cell produces the expected output column set", {
  skip_if_not_installed("select")
  td <- tempfile("sel_real_")
  in_dir  <- file.path(td, "in")
  out_dir <- file.path(td, "out")
  dir.create(in_dir, recursive = TRUE)

  set.seed(0)
  n_samples <- 50
  composite_ids <- sprintf("st1|S%02d", seq_len(n_samples))
  m <- matrix(sample(c(FALSE, TRUE), 50 * 5, replace = TRUE, prob = c(0.7, 0.3)),
              nrow = 50, ncol = 5,
              dimnames = list(composite_ids, c("TP53", "KRAS", "EGFR", "BRAF", "MYC")))
  arrow::write_feather(
    data.frame(composite_sample_id = rownames(m), m, check.names = FALSE),
    file.path(in_dir, "gam.feather"))
  arrow::write_feather(
    data.frame(composite_sample_id = composite_ids,
               sample_class = rep("st1", n_samples)),
    file.path(in_dir, "sample_class.feather"))
  arrow::write_feather(
    data.frame(symbol = colnames(m),
               alteration_class = rep("unknown", ncol(m))),
    file.path(in_dir, "alteration_class.feather"))
  jsonlite::write_json(
    list(skip_reason = NULL, n_samples = n_samples, n_genes = ncol(m),
         panel_intersection_size = ncol(m)),
    path = file.path(in_dir, "cell_metadata.json"),
    auto_unbox = TRUE, null = "null")

  run_one_cell(
    cell_dir = in_dir,
    out_path = file.path(out_dir, "pair_stats.feather"),
    cell_descriptor = list(cancer_type = "luad", tier = "B", study = NA,
                           cohort = "inclusive"),
    runtime_config = list(
      n_permut = 50, n_cores = 1, max_memory_size_gb = 8,
      randomization_switch_threshold = 30,
      min_feature_support = 5, min_feature_freq = 0.001,
      save_intermediate_files = FALSE),
    random_seed = 0L)

  out <- arrow::read_feather(file.path(out_dir, "pair_stats.feather"))
  needed_cols <- c("gene_i", "gene_j", "select_score",
                   "p_wMI", "p_ME", "direction",
                   "n_both", "n_i_only", "n_j_only", "n_neither",
                   "cancer_type", "tier", "cohort")
  expect_true(all(needed_cols %in% colnames(out)))
  expect_true(all(out$direction %in% c("CO", "ME", "none")))
})

test_results <- test_dir(file.path(scripts_dir, "tests"),
                        filter = "test_run_select",
                        reporter = SummaryReporter)
if (any_failed(test_results)) quit(status = 1)
```

- [ ] **Step 2: Implement `code/scripts/run_select.R`**

```r
# code/scripts/run_select.R
#
# Rule (3): per-cell SELECT wrapper.
# Design: doc/plans/2026-04-25-t078-select-cooccurrence-design.md Section 4.5.
#
# Reads one cell's (gam, sample_class, alteration_class, cell_metadata) quad.
# If skip_reason is set, writes a one-row sentinel pair_stats.feather and exits.
# Otherwise calls select::select() with config-knobbed runtime parameters,
# normalises the upstream output schema, and writes pair_stats.feather.
#
# IMPORTANT: GAM input is samples-on-rows, genes-on-columns (design Section 1.2).
# This script does NOT transpose — passing the GAM through verbatim matches
# select::select()'s expected orientation.

suppressPackageStartupMessages({
  library(arrow)
  library(jsonlite)
})

OUT_COLS <- c(
  "gene_i", "gene_j", "select_score",
  "p_wMI", "p_ME", "direction",
  "n_samples", "n_i_only", "n_j_only", "n_both", "n_neither",
  "cancer_type", "tier", "study", "cohort", "skip_reason"
)

write_sentinel <- function(out_path, cell_descriptor, skip_reason) {
  dir.create(dirname(out_path), recursive = TRUE, showWarnings = FALSE)
  row <- data.frame(
    gene_i = NA_character_, gene_j = NA_character_,
    select_score = NA_real_, p_wMI = NA_real_, p_ME = NA_real_,
    direction = NA_character_,
    n_samples = NA_integer_, n_i_only = NA_integer_, n_j_only = NA_integer_,
    n_both = NA_integer_, n_neither = NA_integer_,
    cancer_type = cell_descriptor$cancer_type,
    tier        = cell_descriptor$tier,
    study       = if (is.null(cell_descriptor$study)) NA_character_
                  else as.character(cell_descriptor$study),
    cohort      = cell_descriptor$cohort,
    skip_reason = skip_reason,
    stringsAsFactors = FALSE
  )
  arrow::write_feather(row, out_path)
}

run_one_cell <- function(cell_dir, out_path, cell_descriptor,
                         runtime_config, random_seed) {
  meta <- jsonlite::read_json(file.path(cell_dir, "cell_metadata.json"))
  skip <- meta$skip_reason
  if (!is.null(skip) && !identical(skip, "null") && nchar(as.character(skip)) > 0) {
    write_sentinel(out_path, cell_descriptor, as.character(skip))
    return(invisible())
  }

  gam_df <- arrow::read_feather(file.path(cell_dir, "gam.feather"))
  sc_df  <- arrow::read_feather(file.path(cell_dir, "sample_class.feather"))
  ac_df  <- arrow::read_feather(file.path(cell_dir, "alteration_class.feather"))

  rownames_vec <- as.character(gam_df$composite_sample_id)
  gam <- as.matrix(gam_df[, setdiff(colnames(gam_df), "composite_sample_id"),
                          drop = FALSE])
  rownames(gam) <- rownames_vec
  storage.mode(gam) <- "logical"

  sample_class_vec <- setNames(as.character(sc_df$sample_class),
                                as.character(sc_df$composite_sample_id))
  alteration_class_vec <- setNames(as.character(ac_df$alteration_class),
                                    as.character(ac_df$symbol))

  stopifnot(identical(rownames(gam), names(sample_class_vec)))
  stopifnot(identical(colnames(gam), names(alteration_class_vec)))

  res <- select::select(
    M                              = gam,
    sample.class                   = sample_class_vec,
    alteration.class               = alteration_class_vec,
    folder                         = tempfile("select_run_"),
    r.seed                         = as.integer(random_seed),
    n.cores                        = as.integer(runtime_config$n_cores),
    n.permut                       = as.integer(runtime_config$n_permut),
    min.feature.support            = as.integer(runtime_config$min_feature_support),
    min.feature.freq               = as.numeric(runtime_config$min_feature_freq),
    remove.0.samples               = TRUE,
    remove.unknown.class.samples   = TRUE,
    rho                            = 0.1,
    lambda                         = 15,
    save.intermediate.files        = isTRUE(runtime_config$save_intermediate_files),
    randomization.switch.threshold = as.integer(runtime_config$randomization_switch_threshold),
    max.memory.size                = as.numeric(runtime_config$max_memory_size_gb),
    FDR.cutoff                     = 1.0,                # we recompute BH per stratum
    calculate_APC_threshold        = TRUE,
    calculate_FDR                  = FALSE,
    verbose                        = FALSE
  )

  # Build per-pair contingency from the GAM directly. (SELECT exposes overlap counts,
  # but we compute the four canonical cells for downstream consumers.)
  contingency <- function(gi, gj) {
    i <- gam[, gi]
    j <- gam[, gj]
    list(
      n_both    = sum(i & j),
      n_i_only  = sum(i & !j),
      n_j_only  = sum(!i & j),
      n_neither = sum(!i & !j),
      n_samples = length(i)
    )
  }

  out_rows <- vector("list", nrow(res))
  for (k in seq_len(nrow(res))) {
    cont <- contingency(res$SFE_1[k], res$SFE_2[k])
    out_rows[[k]] <- list(
      gene_i       = res$SFE_1[k],
      gene_j       = res$SFE_2[k],
      select_score = res$select_score[k],
      p_wMI        = res$wMI_p.value[k],
      p_ME         = res$ME_p.value[k],
      direction    = res$direction[k],
      n_samples    = cont$n_samples,
      n_i_only     = cont$n_i_only,
      n_j_only     = cont$n_j_only,
      n_both       = cont$n_both,
      n_neither    = cont$n_neither,
      cancer_type  = cell_descriptor$cancer_type,
      tier         = cell_descriptor$tier,
      study        = if (is.null(cell_descriptor$study)) NA_character_
                     else as.character(cell_descriptor$study),
      cohort       = cell_descriptor$cohort,
      skip_reason  = NA_character_
    )
  }
  out_df <- do.call(rbind, lapply(out_rows, as.data.frame, stringsAsFactors = FALSE))

  dir.create(dirname(out_path), recursive = TRUE, showWarnings = FALSE)
  arrow::write_feather(out_df[, OUT_COLS], out_path)
}

# Snakemake entry point.
if (exists("snakemake")) {
  snek <- snakemake
  run_one_cell(
    cell_dir       = snek@input[["cell_dir"]],
    out_path       = snek@output[["pair_stats"]],
    cell_descriptor = list(
      cancer_type = snek@wildcards[["cancer_type"]],
      tier        = snek@wildcards[["tier"]],
      study       = if ("study" %in% names(snek@wildcards))
                    snek@wildcards[["study"]] else NULL,
      cohort      = snek@wildcards[["cohort"]]
    ),
    runtime_config = snek@params[["runtime"]],
    random_seed    = snek@params[["random_seed"]]
  )
}
```

- [ ] **Step 3: Run the R test (sentinel-only path is testable without the full conda env if the testthat env is local)**

```bash
# Inside the activated SELECT conda env:
Rscript code/scripts/tests/test_run_select.R
```

Expected: both tests PASS. The non-sentinel test will skip if the `select` package
is not yet installed in the test runner's R; CI runs this in the SELECT conda env
where rule (0) has installed it.

- [ ] **Step 4: Commit**

```bash
git add code/scripts/run_select.R code/scripts/tests/test_run_select.R
git commit -m "$(cat <<'EOF'
feat(t078): rule (3) run_select.R wrapper with sentinel handling

Calls select::select() with the v1.6.4 API verified during the design
review: M is samples × genes (no transpose), sample.class /
alteration.class are named vectors matched by rownames/colnames,
output columns mapped wMI_p.value -> p_wMI, ME_p.value -> p_ME,
direction preserved as 'CO'/'ME'/'none'. FDR.cutoff = 1.0 deliberately
— BH is recomputed per stratum in rule (4). Sentinel passthrough
writes a one-row pair_stats.feather with skip_reason populated when
cell_metadata$skip_reason is set, satisfying Section 1.5.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 13: Implement rule (5) `run_select_pathway_aggregated.R`

**Why:** Same engine as rule (3) but on the `samples × 10` pathway-aggregated GAM.
Independent of rules (3)/(4) — emits its own headline feather directly.

**Files:**
- Create: `code/scripts/run_select_pathway_aggregated.R`

For `task:t078` rule (5), this rule shares 95% of its code with `run_select.R`; we factor
the shared logic into a small wrapper.

- [ ] **Step 1: Write the wrapper script**

```r
# code/scripts/run_select_pathway_aggregated.R
#
# Rule (5): pathway × pathway SELECT on the samples × 10 pathway-aggregated GAM.
# Reuses run_select.R's run_one_cell() unchanged — the pathway GAM has the same
# orientation contract (rows = samples, cols = pathways) and the same
# sample_class / alteration_class shape, so SELECT does not care that the
# columns are pathway names rather than gene symbols.

suppressPackageStartupMessages({
  library(arrow)
  library(jsonlite)
})

source(file.path(dirname(sys.frame(1)$ofile), "run_select.R"), local = FALSE)

if (exists("snakemake")) {
  snek <- snakemake
  run_one_cell(
    cell_dir       = snek@input[["cell_dir"]],
    out_path       = snek@output[["pair_stats"]],
    cell_descriptor = list(
      cancer_type = snek@wildcards[["cancer_type"]],
      tier        = "B",
      study       = NULL,
      cohort      = "exclusive"
    ),
    runtime_config = snek@params[["runtime"]],
    random_seed    = snek@params[["random_seed"]]
  )
}
```

- [ ] **Step 2: Commit**

```bash
git add code/scripts/run_select_pathway_aggregated.R
git commit -m "$(cat <<'EOF'
feat(t078): rule (5) run_select_pathway_aggregated.R

Thin wrapper that re-uses run_select.R's run_one_cell() on the
samples × 10 pathway-aggregated GAM. Output column 'gene_i' / 'gene_j'
will hold pathway names (e.g. 'P53', 'RTK_RAS') — downstream
aggregate_select_results.py joins on the same column names, so no
schema branching is needed.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 14: Implement rule (4) `aggregate_select_results.py` — B-tier concat + BH-FDR

**Why:** First slice of rule (4): concat all B-tier per-cell pair_stats feathers,
compute BH-FDR within each `(cancer_type, cohort)` stratum, emit the B-tier-only
intermediate that subsequent tasks build on.

**Files:**
- Create: `code/scripts/aggregate_select_results.py`
- Create: `code/scripts/tests/test_aggregate_select_results.py`

- [ ] **Step 1: Write the failing test**

```python
# code/scripts/tests/test_aggregate_select_results.py
"""Unit tests for aggregate_select_results."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.feather as feather

import aggregate_select_results as mod


def _per_cell(rows: list[dict]) -> pd.DataFrame:
    base = {
        "gene_i": "TP53", "gene_j": "KRAS",
        "select_score": 0.0, "p_wMI": np.nan, "p_ME": np.nan,
        "direction": "none",
        "n_samples": 100, "n_i_only": 10, "n_j_only": 10,
        "n_both": 5, "n_neither": 75,
        "cancer_type": "luad", "tier": "B", "study": pd.NA,
        "cohort": "exclusive", "skip_reason": pd.NA,
    }
    return pd.DataFrame([{**base, **r} for r in rows])


def test_concat_b_tier_strips_sentinel_rows(tmp_path: Path):
    cell_a = _per_cell([
        {"gene_i": "TP53", "gene_j": "KRAS", "p_wMI": 0.001, "direction": "ME"},
        {"gene_i": "TP53", "gene_j": "EGFR", "p_wMI": 0.5,   "direction": "CO"},
    ])
    cell_b_sentinel = _per_cell([
        {"gene_i": pd.NA, "gene_j": pd.NA, "p_wMI": np.nan,
         "skip_reason": "n_samples_below_threshold"},
    ])
    pa = tmp_path / "a.feather"; cell_a.to_feather(pa)
    pb = tmp_path / "b.feather"; cell_b_sentinel.to_feather(pb)
    out = mod.concat_b_tier([pa, pb])
    assert len(out) == 2  # sentinel dropped
    assert set(out["gene_j"]) == {"KRAS", "EGFR"}


def test_bh_fdr_within_stratum_applied(tmp_path: Path):
    df = _per_cell([
        {"gene_i": "TP53", "gene_j": "KRAS", "p_wMI": 0.001, "direction": "ME"},
        {"gene_i": "TP53", "gene_j": "EGFR", "p_wMI": 0.5,   "direction": "CO"},
        {"gene_i": "TP53", "gene_j": "BRAF", "p_wMI": 0.5,   "direction": "CO"},
    ])
    out = mod.compute_b_tier_qvalues(df)
    qs = out.set_index("gene_j")["b_q_wMI_within_stratum"].to_dict()
    np.testing.assert_allclose(qs["KRAS"], 0.003, rtol=1e-6)
    np.testing.assert_allclose(qs["EGFR"], 0.5, rtol=1e-6)
    np.testing.assert_allclose(qs["BRAF"], 0.5, rtol=1e-6)


def test_b_tier_columns_have_b_prefix(tmp_path: Path):
    df = _per_cell([{"gene_i": "TP53", "gene_j": "KRAS",
                     "p_wMI": 0.001, "direction": "ME"}])
    out = mod.compute_b_tier_qvalues(df)
    expected_b_cols = {
        "b_n_samples", "b_n_i_only", "b_n_j_only", "b_n_both", "b_n_neither",
        "b_select_score", "b_p_wMI", "b_p_ME", "b_direction",
        "b_q_wMI_within_stratum", "b_skip_reason",
    }
    assert expected_b_cols.issubset(set(out.columns))
```

- [ ] **Step 2: Run to verify it fails**

```bash
uv run --frozen pytest code/scripts/tests/test_aggregate_select_results.py -v
```

Expected: FAIL on `ModuleNotFoundError`.

- [ ] **Step 3: Implement `code/scripts/aggregate_select_results.py` (B-tier slice)**

```python
# code/scripts/aggregate_select_results.py
"""Rule (4): aggregate per-cell SELECT outputs into headline feathers.

This task implements the B-tier slice. Subsequent tasks add A-tier Stouffer,
union join + concordance flag, and pathway rollup + sibling annotation.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

import select_lib as lib


KEY_COLS = ["gene_i", "gene_j", "cancer_type", "cohort"]
B_RENAME = {
    "n_samples":    "b_n_samples",
    "n_i_only":     "b_n_i_only",
    "n_j_only":     "b_n_j_only",
    "n_both":       "b_n_both",
    "n_neither":    "b_n_neither",
    "select_score": "b_select_score",
    "p_wMI":        "b_p_wMI",
    "p_ME":         "b_p_ME",
    "direction":    "b_direction",
    "skip_reason":  "b_skip_reason",
}


def concat_b_tier(per_cell_paths: list[Path]) -> pd.DataFrame:
    """Concatenate all B-tier per-cell pair feathers, dropping sentinel rows."""
    frames = []
    for p in per_cell_paths:
        df = pd.read_feather(p)
        df = df[df["tier"] == "B"]
        df = df[df["skip_reason"].isna()]   # drop sentinel rows
        frames.append(df)
    if not frames:
        return pd.DataFrame(columns=list(B_RENAME.keys()) + KEY_COLS)
    return pd.concat(frames, ignore_index=True)


def compute_b_tier_qvalues(df_b: pd.DataFrame) -> pd.DataFrame:
    """Add b_q_wMI_within_stratum via BH-FDR per (cancer_type, cohort)."""
    df = df_b.rename(columns=B_RENAME).copy()
    if df.empty:
        df["b_q_wMI_within_stratum"] = pd.Series(dtype="float64")
        return df
    df["b_q_wMI_within_stratum"] = lib.bh_fdr_within_groups(
        df, group_cols=["cancer_type", "cohort"], pvalue_col="b_p_wMI"
    )
    return df


if "snakemake" in globals():  # pragma: no cover  # set by Snakemake's script: directive
    raise NotImplementedError("Snakemake entry point lands in Task 17.")
```

- [ ] **Step 4: Run tests + lint**

```bash
uv run --frozen pytest code/scripts/tests/test_aggregate_select_results.py -v
uv run --frozen ruff check code/scripts/aggregate_select_results.py
uv run --frozen ruff format --check code/scripts/aggregate_select_results.py
```

Expected: 3 PASS, lint clean.

- [ ] **Step 5: Commit**

```bash
git add code/scripts/aggregate_select_results.py \
  code/scripts/tests/test_aggregate_select_results.py
git commit -m "$(cat <<'EOF'
feat(t078): rule (4) aggregate_select_results.py — B-tier concat + BH

Concatenates all B-tier per-cell pair_stats feathers, drops sentinel
rows (skip_reason populated), prefixes the per-fit stat columns with
'b_', computes BH-FDR within each (cancer_type, cohort) stratum.
A-tier Stouffer + union-join land in subsequent tasks.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 15: Extend rule (4) — A-tier signed Stouffer

**Why:** Per-pair sign-aware weighted-Z over the per-study A-tier cells, plus
`a_direction_consensus_frac`. Reuses `select_lib.signed_stouffer()` and
`select_lib.direction_consensus_frac()`.

**Files:**
- Modify: `code/scripts/aggregate_select_results.py`
- Modify: `code/scripts/tests/test_aggregate_select_results.py`

- [ ] **Step 1: Add failing tests**

```python
# Append to test_aggregate_select_results.py

def _per_cell_a(study: str, p: float, direction: str, n: int = 100) -> dict:
    return {
        "gene_i": "TP53", "gene_j": "KRAS",
        "select_score": 0.0, "p_wMI": p, "p_ME": p, "direction": direction,
        "n_samples": n, "n_i_only": 10, "n_j_only": 10,
        "n_both": 5, "n_neither": n - 25,
        "cancer_type": "luad", "tier": "A", "study": study,
        "cohort": "exclusive", "skip_reason": pd.NA,
    }


def test_a_tier_stouffer_aggregates_by_pair(tmp_path: Path):
    rows = [
        _per_cell_a("st1", 0.01, "ME"),
        _per_cell_a("st2", 0.05, "ME"),
        _per_cell_a("st3", 0.02, "ME"),
    ]
    df_a = pd.DataFrame(rows)
    out = mod.compute_a_tier_stouffer(df_a)
    assert len(out) == 1
    row = out.iloc[0]
    assert row["a_k_studies_contributing"] == 3
    assert row["a_k_studies_attempted"] == 3
    # All ME — direction_consensus_frac should be 1.0.
    np.testing.assert_allclose(row["a_direction_consensus_frac"], 1.0)
    assert row["a_stouffer_p_wMI"] < 0.05


def test_a_tier_stouffer_handles_mixed_directions(tmp_path: Path):
    rows = [
        _per_cell_a("st1", 0.001, "ME"),
        _per_cell_a("st2", 0.001, "CO"),
        _per_cell_a("st3", 0.001, "ME"),
    ]
    df_a = pd.DataFrame(rows)
    out = mod.compute_a_tier_stouffer(df_a)
    row = out.iloc[0]
    np.testing.assert_allclose(row["a_direction_consensus_frac"], 2 / 3)
    # Cancellation reduces magnitude vs all-aligned case.
    rows_all_aligned = [_per_cell_a(f"st{i}", 0.001, "ME") for i in range(3)]
    aligned = mod.compute_a_tier_stouffer(pd.DataFrame(rows_all_aligned))
    assert abs(row["a_stouffer_z_wMI"]) < abs(aligned.iloc[0]["a_stouffer_z_wMI"])


def test_a_tier_counts_attempted_includes_sentinels(tmp_path: Path):
    rows = [
        _per_cell_a("st1", 0.01, "ME"),
        # Sentinel row from a small-N A-tier study cell.
        {"gene_i": pd.NA, "gene_j": pd.NA, "select_score": np.nan,
         "p_wMI": np.nan, "p_ME": np.nan, "direction": pd.NA,
         "n_samples": pd.NA, "n_i_only": pd.NA, "n_j_only": pd.NA,
         "n_both": pd.NA, "n_neither": pd.NA, "cancer_type": "luad",
         "tier": "A", "study": "st_small", "cohort": "exclusive",
         "skip_reason": "n_samples_below_threshold"},
    ]
    df_a = pd.DataFrame(rows)
    out = mod.compute_a_tier_stouffer(df_a)
    row = out.iloc[0]
    assert row["a_k_studies_contributing"] == 1
    assert row["a_k_studies_attempted"] == 2
```

- [ ] **Step 2: Run to verify they fail**

```bash
uv run --frozen pytest code/scripts/tests/test_aggregate_select_results.py -v
```

Expected: FAIL on missing `compute_a_tier_stouffer`.

- [ ] **Step 3: Add `compute_a_tier_stouffer` to `aggregate_select_results.py`**

```python
import numpy as np


def compute_a_tier_stouffer(df_a: pd.DataFrame) -> pd.DataFrame:
    """Sign-aware weighted-Z aggregate over A-tier per-study cells.

    Returns one row per (gene_i, gene_j, cancer_type, cohort) appearing in df_a
    with non-sentinel rows. Sentinel rows count toward `a_k_studies_attempted`
    but not `a_k_studies_contributing`.
    """
    if df_a.empty:
        return pd.DataFrame()

    df = df_a.copy()
    df["is_sentinel"] = df["skip_reason"].notna()

    # First, count attempted = real + sentinel per (pair, cancer_type, cohort, study).
    # Sentinel rows have NaN gene_i/gene_j — to attribute attempts to a pair, we treat
    # ALL pairs in the cancer_type × cohort as attempted by every contributing study.
    # In practice we only know which pairs the non-sentinel cells fit; we count
    # sentinel A-tier cells once per (cancer_type, cohort, study) and the attempted
    # count is per-study-per-cell, not per-pair-per-study. Document that simplification.

    real = df[~df["is_sentinel"]].copy()
    if real.empty:
        return pd.DataFrame()

    sign_map = {"CO": +1, "ME": -1, "none": 0}
    real["sign"] = real["direction"].map(sign_map).fillna(0).astype(int)
    real["weight"] = np.sqrt(real["n_samples"].astype(float))

    out_rows: list[dict] = []
    for keys, sub in real.groupby(KEY_COLS, observed=True):
        z, p, n_used = lib.signed_stouffer(
            pvalues=sub["p_wMI"].to_numpy(dtype=float),
            signs=sub["sign"].to_numpy(dtype=float),
            weights=sub["weight"].to_numpy(dtype=float),
        )
        d_frac = lib.direction_consensus_frac(sub["direction"].astype(str).tolist())

        # Attempted count: contributing studies for this pair plus sentinel A-tier
        # studies in the same cancer_type × cohort. Look back at df_a for those.
        ct, ch = keys[2], keys[3]
        sentinel_studies = df_a[
            (df_a["cancer_type"] == ct) & (df_a["cohort"] == ch)
            & df_a["skip_reason"].notna()
        ]["study"].dropna().unique()
        attempted = n_used + len(set(sentinel_studies))

        out_rows.append({
            "gene_i": keys[0], "gene_j": keys[1],
            "cancer_type": ct, "cohort": ch,
            "a_stouffer_z_wMI": z, "a_stouffer_p_wMI": p,
            "a_k_studies_contributing": int(n_used),
            "a_k_studies_attempted": int(attempted),
            "a_direction_consensus_frac": d_frac,
            "a_skip_reason": pd.NA,
        })
    out = pd.DataFrame(out_rows)
    if out.empty:
        return out
    out["a_q_wMI_within_stratum"] = lib.bh_fdr_within_groups(
        out, group_cols=["cancer_type", "cohort"], pvalue_col="a_stouffer_p_wMI"
    )
    return out


def concat_a_tier(per_cell_paths: list[Path]) -> pd.DataFrame:
    """Concatenate all A-tier per-cell pair feathers (sentinels included)."""
    frames = []
    for p in per_cell_paths:
        df = pd.read_feather(p)
        df = df[df["tier"] == "A"]
        frames.append(df)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)
```

- [ ] **Step 4: Run tests + lint**

```bash
uv run --frozen pytest code/scripts/tests/test_aggregate_select_results.py -v
uv run --frozen ruff check code/scripts/aggregate_select_results.py
uv run --frozen ruff format --check code/scripts/aggregate_select_results.py
```

Expected: 6 PASS, lint clean.

- [ ] **Step 5: Commit**

```bash
git add code/scripts/aggregate_select_results.py \
  code/scripts/tests/test_aggregate_select_results.py
git commit -m "$(cat <<'EOF'
feat(t078): aggregate_select_results.py — A-tier signed Stouffer

Adds compute_a_tier_stouffer() producing per (gene_i, gene_j,
cancer_type, cohort) sign-aware weighted-Z combinations across A-tier
per-study cells, with a_direction_consensus_frac as a separate
diagnostic. a_k_studies_contributing counts cells that produced a
real fit; a_k_studies_attempted additionally counts sentinel cells in
the same cancer_type × cohort. BH-FDR computed over Stouffer p-values
within each stratum.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 16: Extend rule (4) — union-join + 7-category concordance flag

**Why:** Per design Section 4.6 step 3 + 4 + risk #14: outer-join B-tier and A-tier on
the four key columns; preserve `a_only_b_absent` rows; populate `b_a_concordance`
with the 7 categories specified in the design.

**Files:**
- Modify: `code/scripts/aggregate_select_results.py`
- Modify: `code/scripts/tests/test_aggregate_select_results.py`

- [ ] **Step 1: Add failing test**

```python
# Append to test_aggregate_select_results.py

def test_union_join_preserves_a_only_b_absent(tmp_path: Path):
    df_b = pd.DataFrame([{
        "gene_i": "TP53", "gene_j": "KRAS",
        "cancer_type": "luad", "cohort": "exclusive",
        "b_n_samples": 100, "b_n_i_only": 10, "b_n_j_only": 10,
        "b_n_both": 5, "b_n_neither": 75,
        "b_select_score": 0.5, "b_p_wMI": 0.001, "b_p_ME": 0.002,
        "b_direction": "ME", "b_q_wMI_within_stratum": 0.005,
        "b_skip_reason": pd.NA,
    }])
    df_a = pd.DataFrame([{
        "gene_i": "EGFR", "gene_j": "MYC",  # not in B-tier (panel intersection dropped)
        "cancer_type": "luad", "cohort": "exclusive",
        "a_stouffer_z_wMI": 3.0, "a_stouffer_p_wMI": 0.003,
        "a_q_wMI_within_stratum": 0.01, "a_k_studies_contributing": 3,
        "a_k_studies_attempted": 3, "a_direction_consensus_frac": 1.0,
        "a_skip_reason": pd.NA,
    }])
    out = mod.union_join(df_b, df_a)
    assert len(out) == 2
    egfr_myc = out[(out["gene_i"] == "EGFR") & (out["gene_j"] == "MYC")].iloc[0]
    assert pd.isna(egfr_myc["b_p_wMI"])
    assert egfr_myc["a_q_wMI_within_stratum"] == pytest.approx(0.01)


@pytest.mark.parametrize("scenario,expected", [
    # (b_q, a_q, b_dir, a_dir, k, consensus) -> expected
    ((0.05, 0.05, "ME", "ME", 3, 1.0), "concordant"),
    ((0.05, 0.05, "ME", "CO", 3, 0.5), "direction_conflict"),
    ((0.05, 0.5,  "ME", "CO", 3, 1.0), "b_only"),
    ((0.5,  0.05, "ME", "CO", 3, 1.0), "a_only_b_present"),
    ((np.nan, 0.05, np.nan, "CO", 3, 1.0), "a_only_b_absent"),
    ((0.05, 0.5,  "ME", "CO", 1, 1.0), "insufficient_a_studies"),
    ((np.nan, np.nan, np.nan, np.nan, 0, np.nan), "untested"),
])
def test_concordance_flag_categories(scenario, expected):
    b_q, a_q, b_dir, a_dir, k, cons = scenario
    out = mod.compute_concordance_flag(
        pd.Series({
            "b_q_wMI_within_stratum": b_q, "a_q_wMI_within_stratum": a_q,
            "b_direction": b_dir, "a_direction_consensus_frac": cons,
            "a_k_studies_contributing": k,
        })
    )
    # Note: a_direction is encoded only via consensus_frac in this design.
    assert out == expected
```

- [ ] **Step 2: Run to verify it fails**

```bash
uv run --frozen pytest code/scripts/tests/test_aggregate_select_results.py -v
```

Expected: FAIL on missing `union_join` and `compute_concordance_flag`.

- [ ] **Step 3: Add `union_join` and `compute_concordance_flag`**

```python
def union_join(df_b: pd.DataFrame, df_a: pd.DataFrame) -> pd.DataFrame:
    """Outer join on (gene_i, gene_j, cancer_type, cohort) — preserves a_only / b_only."""
    if df_b.empty and df_a.empty:
        return pd.DataFrame()
    if df_b.empty:
        out = df_a.copy()
    elif df_a.empty:
        out = df_b.copy()
    else:
        out = df_b.merge(df_a, on=KEY_COLS, how="outer")
    return out


_FDR_THRESHOLD = 0.10
_CONSENSUS_THRESHOLD = 0.7


def compute_concordance_flag(row: pd.Series, fdr_alpha: float = _FDR_THRESHOLD,
                              consensus_threshold: float = _CONSENSUS_THRESHOLD) -> str:
    """Categorical concordance flag per design Section 4.6 step 4."""
    b_q = row.get("b_q_wMI_within_stratum")
    a_q = row.get("a_q_wMI_within_stratum")
    b_dir = row.get("b_direction")
    a_consensus = row.get("a_direction_consensus_frac")
    a_k = row.get("a_k_studies_contributing")

    b_present = pd.notna(b_q)
    a_present = pd.notna(a_q)
    b_sig = b_present and b_q < fdr_alpha
    a_sig = a_present and a_q < fdr_alpha

    if not b_present and not a_present:
        return "untested"

    if a_present and (a_k is None or pd.isna(a_k) or a_k < 2):
        return "insufficient_a_studies"

    if b_sig and a_sig:
        consensus_ok = pd.notna(a_consensus) and a_consensus >= consensus_threshold
        # In B-tier the direction is `b_direction`; in A-tier it is the dominant direction.
        # We approximate "directions agree" by requiring consensus_ok AND that the B-tier
        # direction matches the A-tier dominant direction. Since dominant direction is
        # not carried as a column (only consensus_frac is), we infer via sign of stouffer_z:
        # negative z means dominant ME, positive means dominant CO.
        a_z = row.get("a_stouffer_z_wMI")
        a_dom_dir = "CO" if pd.notna(a_z) and a_z > 0 else (
            "ME" if pd.notna(a_z) and a_z < 0 else None
        )
        signs_agree = (b_dir == a_dom_dir) and a_dom_dir is not None
        if signs_agree and consensus_ok:
            return "concordant"
        return "direction_conflict"

    if b_sig and not a_sig:
        return "b_only"

    if a_sig and not b_sig and b_present:
        return "a_only_b_present"

    if a_sig and not b_present:
        return "a_only_b_absent"

    return "untested"


def add_concordance_flag(df: pd.DataFrame) -> pd.DataFrame:
    """Apply compute_concordance_flag row-wise."""
    if df.empty:
        df = df.copy()
        df["b_a_concordance"] = pd.Series(dtype="string")
        return df
    df = df.copy()
    df["b_a_concordance"] = df.apply(compute_concordance_flag, axis=1).astype("string")
    return df
```

- [ ] **Step 4: Run tests + lint**

```bash
uv run --frozen pytest code/scripts/tests/test_aggregate_select_results.py -v
uv run --frozen ruff check code/scripts/aggregate_select_results.py
uv run --frozen ruff format --check code/scripts/aggregate_select_results.py
```

Expected: 14 PASS (6 prior + 1 new union-join + 7 parametrised concordance), lint clean.

- [ ] **Step 5: Commit**

```bash
git add code/scripts/aggregate_select_results.py \
  code/scripts/tests/test_aggregate_select_results.py
git commit -m "$(cat <<'EOF'
feat(t078): aggregate_select_results.py — union-join + concordance

Adds union_join() (outer join on (gene_i, gene_j, cancer_type, cohort)
preserving b_only / a_only_b_absent rows) and compute_concordance_flag
implementing the 7-category b_a_concordance from design Section 4.6
step 4. Direction-agreement infers A-tier dominant direction from the
sign of a_stouffer_z_wMI (CO if >0, ME if <0).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 17: Extend rule (4) — pathway rollup + sibling annotation + Snakemake entry point

**Why:** Final slice of rule (4): the exploratory pathway rollup of gene-pair Z-scores
and the sibling annotation feather. Plus the Snakemake entry point that ties it all
together and writes the four headline outputs.

**Files:**
- Modify: `code/scripts/aggregate_select_results.py`
- Modify: `code/scripts/tests/test_aggregate_select_results.py`

- [ ] **Step 1: Add failing tests**

```python
# Append to test_aggregate_select_results.py

def test_pathway_rollup_groups_by_pathway_pair(tmp_path: Path):
    """Stouffer over gene-pairs grouped by their pathway membership."""
    headline = pd.DataFrame([
        {"gene_i": "TP53", "gene_j": "KRAS", "cancer_type": "luad",
         "cohort": "exclusive", "b_p_wMI": 0.01, "b_direction": "ME",
         "b_n_samples": 100},
        {"gene_i": "TP53", "gene_j": "BRAF", "cancer_type": "luad",
         "cohort": "exclusive", "b_p_wMI": 0.05, "b_direction": "ME",
         "b_n_samples": 100},
        {"gene_i": "EGFR", "gene_j": "BRAF", "cancer_type": "luad",
         "cohort": "exclusive", "b_p_wMI": 0.01, "b_direction": "CO",
         "b_n_samples": 100},
    ])
    pathway_membership = pd.DataFrame({
        "symbol":  ["TP53", "KRAS", "BRAF", "EGFR"],
        "pathway": ["P53",  "RTK_RAS", "RTK_RAS", "RTK_RAS"],
    })
    out = mod.pathway_rollup(headline, pathway_membership)
    # P53 × RTK_RAS: 2 rows (TP53-KRAS, TP53-BRAF). RTK_RAS × RTK_RAS: 1 row (EGFR-BRAF).
    rolled = out.set_index(["pathway_i", "pathway_j", "cancer_type", "cohort"])
    assert ("P53", "RTK_RAS", "luad", "exclusive") in rolled.index
    assert rolled.loc[("P53", "RTK_RAS", "luad", "exclusive"),
                       "n_constituent_pairs"] == 2


def test_sibling_annotation_counts_partners(tmp_path: Path):
    headline = pd.DataFrame([
        {"gene_i": "TP53", "gene_j": "KRAS", "cancer_type": "luad",
         "cohort": "exclusive", "b_q_wMI_within_stratum": 0.005,
         "b_a_concordance": "concordant"},
        {"gene_i": "TP53", "gene_j": "EGFR", "cancer_type": "luad",
         "cohort": "exclusive", "b_q_wMI_within_stratum": 0.05,
         "b_a_concordance": "b_only"},
        {"gene_i": "TP53", "gene_j": "BRAF", "cancer_type": "luad",
         "cohort": "exclusive", "b_q_wMI_within_stratum": 0.5,
         "b_a_concordance": "untested"},
    ])
    out = mod.build_sibling_annotation(headline)
    tp53_luad = out[(out["symbol"] == "TP53") & (out["cancer_type"] == "luad")].iloc[0]
    assert tp53_luad["n_significant_select_partners_q01"] == 2
    assert tp53_luad["n_significant_select_partners_q01_concordant"] == 1
```

- [ ] **Step 2: Run to verify they fail**

```bash
uv run --frozen pytest code/scripts/tests/test_aggregate_select_results.py -v
```

Expected: FAIL on missing `pathway_rollup` and `build_sibling_annotation`.

- [ ] **Step 3: Add the two functions + Snakemake entry point**

```python
def pathway_rollup(
    headline: pd.DataFrame,
    pathway_membership: pd.DataFrame,
) -> pd.DataFrame:
    """EXPLORATORY: Stouffer over gene-pair Z-scores grouped by pathway pair.

    Per design Section 4.6 step 5 + risk #4: gene-pairs within a pathway block
    are correlated through shared genes, so Stouffer's null is mis-specified.
    This output is for hypothesis generation only.
    """
    if headline.empty:
        return pd.DataFrame(
            columns=["pathway_i", "pathway_j", "cancer_type", "cohort",
                     "rollup_stouffer_z", "rollup_stouffer_p",
                     "n_constituent_pairs"]
        )
    pm = pathway_membership.set_index("symbol")["pathway"]
    df = headline[["gene_i", "gene_j", "cancer_type", "cohort",
                   "b_p_wMI", "b_direction", "b_n_samples"]].copy()
    df["pathway_i"] = df["gene_i"].map(pm)
    df["pathway_j"] = df["gene_j"].map(pm)
    df = df.dropna(subset=["pathway_i", "pathway_j"])
    df = df.dropna(subset=["b_p_wMI"])

    sign_map = {"CO": +1, "ME": -1, "none": 0}
    df["sign"] = df["b_direction"].map(sign_map).fillna(0).astype(int)
    df["weight"] = np.sqrt(df["b_n_samples"].astype(float))

    rows: list[dict] = []
    for keys, sub in df.groupby(["pathway_i", "pathway_j", "cancer_type", "cohort"],
                                  observed=True):
        z, p, n_used = lib.signed_stouffer(
            pvalues=sub["b_p_wMI"].to_numpy(dtype=float),
            signs=sub["sign"].to_numpy(dtype=float),
            weights=sub["weight"].to_numpy(dtype=float),
        )
        rows.append({
            "pathway_i": keys[0], "pathway_j": keys[1],
            "cancer_type": keys[2], "cohort": keys[3],
            "rollup_stouffer_z": z, "rollup_stouffer_p": p,
            "n_constituent_pairs": int(n_used),
        })
    return pd.DataFrame(rows)


def build_sibling_annotation(headline: pd.DataFrame) -> pd.DataFrame:
    """Per (symbol, cancer_type) significant-partners count from B-tier exclusive cohort."""
    if headline.empty:
        return pd.DataFrame(columns=["symbol", "cancer_type",
                                       "n_significant_select_partners_q01",
                                       "n_significant_select_partners_q01_concordant"])
    excl = headline[headline["cohort"] == "exclusive"].copy()
    excl["q_sig"] = excl["b_q_wMI_within_stratum"].fillna(1.0) < 0.10
    excl["q_sig_concordant"] = excl["q_sig"] & (excl["b_a_concordance"] == "concordant")

    pieces: list[pd.DataFrame] = []
    for left_col in ("gene_i", "gene_j"):
        sub = excl[[left_col, "cancer_type", "q_sig", "q_sig_concordant"]].copy()
        sub = sub.rename(columns={left_col: "symbol"})
        pieces.append(sub)
    long = pd.concat(pieces, ignore_index=True)
    grouped = (
        long.groupby(["symbol", "cancer_type"], observed=True, as_index=False)
            .agg(n_significant_select_partners_q01=("q_sig", "sum"),
                 n_significant_select_partners_q01_concordant=("q_sig_concordant", "sum"))
    )
    grouped["n_significant_select_partners_q01"] = (
        grouped["n_significant_select_partners_q01"].astype(int)
    )
    grouped["n_significant_select_partners_q01_concordant"] = (
        grouped["n_significant_select_partners_q01_concordant"].astype(int)
    )
    return grouped


# Snakemake entry point.
if "snakemake" in globals():  # pragma: no cover  # set by Snakemake's script: directive
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821

    per_cell_paths = [Path(p) for p in snek.input["per_cell"]]
    pathway_membership = pd.read_csv(snek.input["pathway_membership"], sep="\t")

    df_b = compute_b_tier_qvalues(concat_b_tier(per_cell_paths))
    df_a = compute_a_tier_stouffer(concat_a_tier(per_cell_paths))
    headline = add_concordance_flag(union_join(df_b, df_a))
    rollup = pathway_rollup(headline, pathway_membership)
    annotation = build_sibling_annotation(headline)

    Path(snek.output["gene_pair"]).parent.mkdir(parents=True, exist_ok=True)
    headline.reset_index(drop=True).to_feather(snek.output["gene_pair"])
    rollup.reset_index(drop=True).to_feather(snek.output["pathway_rollup"])
    annotation.reset_index(drop=True).to_feather(snek.output["annotation"])
```

- [ ] **Step 4: Run tests + lint**

```bash
uv run --frozen pytest code/scripts/tests/test_aggregate_select_results.py -v
uv run --frozen ruff check code/scripts/aggregate_select_results.py
uv run --frozen ruff format --check code/scripts/aggregate_select_results.py
```

Expected: 16 PASS, lint clean.

- [ ] **Step 5: Commit**

```bash
git add code/scripts/aggregate_select_results.py \
  code/scripts/tests/test_aggregate_select_results.py
git commit -m "$(cat <<'EOF'
feat(t078): aggregate_select_results.py — pathway rollup + annotation

Adds pathway_rollup() (exploratory Stouffer of gene-pair Z grouped by
pathway pair, per design risk #4) and build_sibling_annotation()
(emits gene_cancer_study_select_annotation.feather joining on
(symbol, cancer_type) with significant-partner counts). Wires the
Snakemake entry point that produces all four headline outputs.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 18: Wire all rules into the Snakefile + add `select:` config block

**Why:** All 7 rules (0, 1a, 1b, 2, 3, 4, 5) get added to the Snakefile under the
`select_enabled` gate. The optional rule 7 (marimo report) is left as a stub. The
`config-10k-genes.yml` gets a default `select:` block.

**Files:**
- Modify: `code/workflows/Snakefile`
- Modify: `code/config/config-10k-genes.yml`
- Create: `code/scripts/tests/test_snakefile_select_wiring.py`

- [ ] **Step 1: Write the failing test**

```python
# code/scripts/tests/test_snakefile_select_wiring.py
"""Verify all SELECT rules are present in the Snakefile under the opt-in gate."""
from pathlib import Path

SNAKEFILE = Path(__file__).resolve().parents[3] / "code" / "workflows" / "Snakefile"

EXPECTED_RULES = [
    "preflight_select_env",
    "build_panel_gene_sets",
    "build_select_gene_universe",
    "build_select_gam",
    "run_select_per_cell",
    "aggregate_select_results",
    "run_select_pathway_aggregated",
]


def test_all_select_rules_present():
    text = SNAKEFILE.read_text()
    for rule_name in EXPECTED_RULES:
        assert f"rule {rule_name}:" in text, f"missing rule {rule_name}"


def test_select_rules_under_opt_in_gate():
    text = SNAKEFILE.read_text()
    # The if-block guarding the opt-in.
    assert "if select_enabled:" in text or 'config["select"]["enabled"]' in text


def test_run_select_rules_use_conda_env():
    text = SNAKEFILE.read_text()
    for rule_name in ("preflight_select_env", "run_select_per_cell",
                       "run_select_pathway_aggregated"):
        block = _extract_rule_block(text, rule_name)
        assert "code/envs/select.yml" in block, f"{rule_name} missing conda env"


def _extract_rule_block(text: str, rule_name: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    in_rule = False
    for line in lines:
        if line.lstrip().startswith(f"rule {rule_name}:"):
            in_rule = True
            out.append(line)
            continue
        if in_rule:
            if line and not line[0:1].isspace():
                break
            out.append(line)
    assert out, f"rule {rule_name} not found"
    return "\n".join(out)
```

- [ ] **Step 2: Run to verify it fails**

```bash
uv run --frozen pytest code/scripts/tests/test_snakefile_select_wiring.py -v
```

Expected: FAIL on missing rules.

- [ ] **Step 3: Add the rules to `code/workflows/Snakefile`**

The full rule block (append after the existing `if select_enabled:` block from Task 4):

```python
  rule build_panel_gene_sets:
    input:
      bed = "data/panels/{panel_id}.bed",
      grch38 = "data/grch38.tsv"
    output:
      out_dir.joinpath("select/panel_gene_sets/{panel_id}.feather")
    script:
      "../scripts/build_panel_gene_sets.py"

  rule build_select_gene_universe:
    input:
      bailey = "data/bailey2018_table_s1.tsv",
      cgc = "data/cosmic_cgc.tsv",
      sanchez_vega = "data/sanchez_vega_pathways.tsv"
    output:
      universe = out_dir.joinpath("select/gene_universe.tsv")
    params:
      bailey_version = "2018",
      cgc_version = "2024-09",
      sanchez_vega_version = "2018"
    script:
      "../scripts/build_select_gene_universe.py"

  # Cell wildcards: cancer_type, tier ∈ {B, A}, cohort ∈ {inclusive, exclusive},
  # study (only when tier == 'A').
  rule build_select_gam:
    input:
      samples_annotated = out_dir.joinpath("metadata/samples_annotated.feather"),
      mutation_long = out_dir.joinpath("summary/mut/table/gene_sample_long.feather"),
      sample_panel_map = out_dir.joinpath("metadata/sample_panel_map.feather"),
      panel_gene_sets = lambda wc: expand(
        str(out_dir.joinpath("select/panel_gene_sets/{panel_id}.feather")),
        panel_id=_panels_for_cell(config, wc)
      ),
      gene_universe = out_dir.joinpath("select/gene_universe.tsv"),
      bailey_alteration_class = out_dir.joinpath("metadata/bailey_alteration_class.feather"),
      preflight_token = out_dir.joinpath("select/.preflight_ok")
    output:
      cell_dir = directory(
        out_dir.joinpath("select/inputs/{cancer_type}/{tier}/{study}/{cohort}/")
      )
    params:
      thresholds = config["select"]["thresholds"],
      sample_class_components = config["select"]["sample_class_components"],
      ch_priority_genes = config["select"].get("ch_priority_genes",
        ["DNMT3A", "PPM1D", "TET2", "TP53", "ASXL1", "CHEK2", "PRPF8"])
    script:
      "../scripts/build_select_gam.py"

  rule run_select_per_cell:
    input:
      cell_dir = out_dir.joinpath("select/inputs/{cancer_type}/{tier}/{study}/{cohort}/"),
      preflight_token = out_dir.joinpath("select/.preflight_ok")
    output:
      pair_stats = out_dir.joinpath(
        "select/per_cell/{cancer_type}/{tier}/{study}/{cohort}/pair_stats.feather")
    params:
      runtime = config["select"]["runtime"],
      random_seed = config["select"]["random_seed"]
    conda:
      "../envs/select.yml"
    script:
      "../scripts/run_select.R"

  rule run_select_pathway_aggregated:
    input:
      cell_dir = out_dir.joinpath(
        "select/inputs/{cancer_type}/B/_/exclusive/pathway_aggregated/"),
      preflight_token = out_dir.joinpath("select/.preflight_ok")
    output:
      pair_stats = out_dir.joinpath(
        "select/per_cell/{cancer_type}/pathway_aggregated/pair_stats.feather")
    params:
      runtime = config["select"]["runtime"],
      random_seed = config["select"]["random_seed"]
    conda:
      "../envs/select.yml"
    script:
      "../scripts/run_select_pathway_aggregated.R"

  rule aggregate_select_results:
    input:
      per_cell = lambda wc: _all_per_cell_paths(config),
      pathway_membership = "data/sanchez_vega_pathways.tsv"
    output:
      gene_pair = out_dir.joinpath("select/gene_pair_select.feather"),
      pathway_rollup = out_dir.joinpath("select/pathway_rollup_gene_pairs.feather"),
      annotation = out_dir.joinpath("select/gene_cancer_study_select_annotation.feather")
    script:
      "../scripts/aggregate_select_results.py"
```

The `_panels_for_cell()` and `_all_per_cell_paths()` helpers are small Python functions
in the Snakefile preamble. Add them above the `rule all:` block:

```python
def _panels_for_cell(config: dict, wildcards) -> list[str]:
    """Panels needed by one (cancer_type, tier, study?, cohort) cell.

    For A-tier cells: only the panel(s) of the named study; usually 1 unless GENIE.
    For B-tier cells: every panel that any sample of that cancer type uses.

    Implementation: read sample_panel_map.feather lazily; cache result.
    """
    import pandas as pd
    spm = pd.read_feather(out_dir.joinpath("metadata/sample_panel_map.feather"))
    samples = pd.read_feather(out_dir.joinpath("metadata/samples_annotated.feather"))
    rel = samples.merge(spm, on=["study_id", "sample_id"], how="inner")
    rel = rel[rel["cancer_type"] == wildcards.cancer_type]
    if wildcards.tier == "A":
        rel = rel[rel["study_id"] == wildcards.study]
    return sorted(rel["panel_id"].dropna().unique().tolist())


def _all_per_cell_paths(config: dict) -> list[str]:
    """Enumerate every per-cell pair_stats.feather Snakemake should expand to."""
    import pandas as pd
    samples = pd.read_feather(out_dir.joinpath("metadata/samples_annotated.feather"))
    cancer_types = sorted(samples["cancer_type"].dropna().unique())
    studies = sorted(samples["study_id"].dropna().unique())
    paths: list[str] = []
    for ct in cancer_types:
        for cohort in ("inclusive", "exclusive"):
            paths.append(str(out_dir.joinpath(
                f"select/per_cell/{ct}/B/_/{cohort}/pair_stats.feather"
            )))
            for st in studies:
                paths.append(str(out_dir.joinpath(
                    f"select/per_cell/{ct}/A/{st}/{cohort}/pair_stats.feather"
                )))
    return paths
```

- [ ] **Step 4: Add the `select:` config block to `code/config/config-10k-genes.yml`**

```yaml
select:
  enabled: false                    # opt-in. Set to true on dev runs.

  gene_universe:
    bailey2018: true
    cosmic_cgc: true
    sanchez_vega: true
    custom_genes_tsv: null

  thresholds:
    min_stratum_samples: 30
    min_gene_prevalence_frac: 0.03
    min_gene_prevalence_count: 3
    min_pair_co_count: 3
    fdr_alpha: 0.10
    study_residual_threshold_frac: 0.10

  stouffer:
    weight: "sqrt_n"

  runtime:
    n_permut: 1000
    n_cores: 8
    max_memory_size_gb: 100
    save_intermediate_files: false
    randomization_switch_threshold: 30
    min_feature_support: 5
    min_feature_freq: 0.001

  output_dir: "results/select"
  random_seed: 0

  panel_beds:
    msk_impact_341: "data/panels/IMPACT341.bed"
    msk_impact_410: "data/panels/IMPACT410.bed"
    msk_impact_468: "data/panels/IMPACT468.bed"
    msk_impact_505: "data/panels/IMPACT505.bed"
    foundation_one: "data/panels/F1.bed"
    foundation_one_cdx: "data/panels/F1CDx.bed"

  sample_class_components: ["study_id"]

  make_select_report: false
```

- [ ] **Step 5: Run tests**

```bash
uv run --frozen pytest code/scripts/tests/test_snakefile_select_wiring.py -v
uv run --frozen snakemake \
  -s code/workflows/Snakefile \
  --configfile code/config/config-10k-genes.yml \
  --config select="{enabled: true}" \
  --lint
```

Expected: 3 PASS, no Snakemake lint errors.

- [ ] **Step 6: Commit**

```bash
git add code/workflows/Snakefile code/config/config-10k-genes.yml \
  code/scripts/tests/test_snakefile_select_wiring.py
git commit -m "$(cat <<'EOF'
feat(t078): wire all 7 SELECT rules into the Snakefile

Adds rules (1a/1b/2/3/4/5) under the existing if select_enabled: gate
from Task 4. _panels_for_cell() / _all_per_cell_paths() Snakefile-level
helpers compute per-cell panel sets and the full expand() universe.
config-10k-genes.yml gets a default select: block with enabled=false
so existing runs are unaffected.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 19: Add toy integration test data + DAG dry-run test

**Why:** Per design Section 8.6: ship a toy 2-study × 1-cancer-type × 5-gene fixture
that exercises sentinel cells, mixed-panel B-tier, and `a_only_b_absent` concordance.
`validate.sh --slow` runs `snakemake -n` against it, which catches DAG-level breakage.

**Files:**
- Create: `code/scripts/tests/data/select_toy/` (synthetic fixtures)
- Create: `code/scripts/tests/data/select_toy/config.yml`
- Modify: `validate.sh` (or wherever `--slow` checks live)
- Create: `code/scripts/tests/test_select_toy_dag.py`

- [ ] **Step 1: Generate the toy fixture**

```bash
uv run python - <<'PY'
"""Generate the t078 toy fixture."""
from pathlib import Path
import json
import pandas as pd

base = Path("code/scripts/tests/data/select_toy")
(base / "studies").mkdir(parents=True, exist_ok=True)
(base / "metadata").mkdir(exist_ok=True)
(base / "panels").mkdir(exist_ok=True)
(base / "data").mkdir(exist_ok=True)

# Two studies, 60 samples total in luad. st1 covers all 5 genes; st2 covers 4 of 5.
studies = {
    "st1": {"prefix": "A", "panel": "panel_full"},
    "st2": {"prefix": "B", "panel": "panel_partial"},
}
samples_rows = []
mut_rows = []
for sid, meta in studies.items():
    for i in range(30):
        sample_id = f"{meta['prefix']}{i:02d}"
        samples_rows.append({
            "study_id": sid, "sample_id": sample_id,
            "patient_id": sample_id,
            "composite_sample_id": f"{sid}|{sample_id}",
            "cancer_type": "luad", "cancer_type_detailed": "luad",
            "is_hypermutator": False,
            "ch_priority_gene": False,
        })
        # Inject a synthetic ME pattern: TP53 ⊥ KRAS within st1.
        if sid == "st1":
            tp53 = i % 2 == 0
            kras = (i % 2 == 1) and (i % 3 == 0)
        else:
            tp53 = i % 3 == 0
            kras = i % 5 == 0
        if tp53:
            mut_rows.append({"composite_sample_id": f"{sid}|{sample_id}", "symbol": "TP53"})
        if kras:
            mut_rows.append({"composite_sample_id": f"{sid}|{sample_id}", "symbol": "KRAS"})
        if i % 4 == 0:
            mut_rows.append({"composite_sample_id": f"{sid}|{sample_id}", "symbol": "EGFR"})
        if i % 5 == 0:
            mut_rows.append({"composite_sample_id": f"{sid}|{sample_id}", "symbol": "BRAF"})
        if sid == "st1" and i % 7 == 0:
            mut_rows.append({"composite_sample_id": f"{sid}|{sample_id}", "symbol": "MYC"})

samples_df = pd.DataFrame(samples_rows)
samples_df.to_feather(base / "metadata" / "samples_annotated.feather")
pd.DataFrame(mut_rows).to_feather(
    base / "metadata" / "gene_sample_long.feather"
)

# Sample panel map.
spm = samples_df[["study_id", "sample_id"]].copy()
spm["panel_id"] = spm["study_id"].map({
    "st1": "panel_full", "st2": "panel_partial"
})
spm["panel_source"] = "study_panels_tsv"
spm.to_feather(base / "metadata" / "sample_panel_map.feather")

# Panels: panel_full has all 5 genes; panel_partial omits MYC (so only st1 can fit MYC).
pd.DataFrame({"chrom": ["chr1"]*5, "start": [1]*5, "end": [100]*5,
              "symbol": ["TP53", "KRAS", "EGFR", "BRAF", "MYC"]}).to_csv(
    base / "panels" / "panel_full.bed", sep="\t", header=False, index=False)
pd.DataFrame({"chrom": ["chr1"]*4, "start": [1]*4, "end": [100]*4,
              "symbol": ["TP53", "KRAS", "EGFR", "BRAF"]}).to_csv(
    base / "panels" / "panel_partial.bed", sep="\t", header=False, index=False)

# Tiny grch38 lookup with all 5 symbols.
pd.DataFrame({
    "ensgene": [f"ENSG{i:03d}" for i in range(5)],
    "entrez":  [str(i) for i in range(5)],
    "symbol":  ["TP53", "KRAS", "EGFR", "BRAF", "MYC"],
    "chr":     ["chr1"]*5, "start": [1]*5, "end": [100]*5,
    "strand": ["+"]*5, "biotype": ["protein_coding"]*5,
    "description": ["g"]*5,
}).to_csv(base / "data" / "grch38.tsv", sep="\t", index=False)

# study_panels.tsv
pd.DataFrame({
    "study_id": ["st1", "st2"], "panel_id": ["panel_full", "panel_partial"],
    "sequencing_type": ["panel", "panel"],
}).to_csv(base / "data" / "study_panels.tsv", sep="\t", index=False)

# Gene universe inputs (Bailey, CGC, Sanchez-Vega).
pd.DataFrame({"Gene": ["TP53", "KRAS", "EGFR", "BRAF", "MYC"]}).to_csv(
    base / "data" / "bailey2018.tsv", sep="\t", index=False)
pd.DataFrame({"Gene Symbol": ["TP53", "KRAS"]}).to_csv(
    base / "data" / "cgc.tsv", sep="\t", index=False)
pd.DataFrame({"gene": ["TP53", "KRAS", "EGFR", "BRAF", "MYC"],
              "pathway": ["P53"] + ["RTK_RAS"] * 4}).to_csv(
    base / "data" / "sanchez_vega.tsv", sep="\t", index=False)

print("toy fixture generated under code/scripts/tests/data/select_toy/")
PY
```

- [ ] **Step 2: Write a tiny config for the toy fixture**

Save as `code/scripts/tests/data/select_toy/config.yml`:

```yaml
data_dir: "code/scripts/tests/data/select_toy"
out_dir: "code/scripts/tests/data/select_toy/_out"
studies: ["st1", "st2"]

select:
  enabled: true
  gene_universe:
    bailey2018: true
    cosmic_cgc: true
    sanchez_vega: true
    custom_genes_tsv: null
  thresholds:
    min_stratum_samples: 20         # lowered for the toy dataset
    min_gene_prevalence_frac: 0.03
    min_gene_prevalence_count: 2
    min_pair_co_count: 2
    fdr_alpha: 0.10
    study_residual_threshold_frac: 0.10
  stouffer:
    weight: "sqrt_n"
  runtime:
    n_permut: 50
    n_cores: 1
    max_memory_size_gb: 4
    save_intermediate_files: false
    randomization_switch_threshold: 30
    min_feature_support: 2
    min_feature_freq: 0.001
  output_dir: "code/scripts/tests/data/select_toy/_out/select"
  random_seed: 0
  panel_beds:
    panel_full: "code/scripts/tests/data/select_toy/panels/panel_full.bed"
    panel_partial: "code/scripts/tests/data/select_toy/panels/panel_partial.bed"
  sample_class_components: ["study_id"]
  make_select_report: false
```

- [ ] **Step 3: Write a Python test that does `snakemake -n` on the toy config**

```python
# code/scripts/tests/test_select_toy_dag.py
"""Toy fixture must produce a resolvable DAG."""
from __future__ import annotations

import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
CONFIG = REPO / "code/scripts/tests/data/select_toy/config.yml"


def test_dag_resolves_with_dry_run():
    cmd = [
        "uv", "run", "--frozen", "snakemake",
        "-s", str(REPO / "code/workflows/Snakefile"),
        "--configfile", str(CONFIG),
        "-n",
        str(REPO / "code/scripts/tests/data/select_toy/_out/select/gene_pair_select.feather"),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO)
    assert result.returncode == 0, (
        f"snakemake -n failed:\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert "preflight_select_env" in result.stdout
    assert "build_select_gam" in result.stdout
    assert "aggregate_select_results" in result.stdout
```

- [ ] **Step 4: Run the test**

```bash
uv run --frozen pytest code/scripts/tests/test_select_toy_dag.py -v
```

Expected: PASS. If it fails because of missing inputs (e.g. the project has rules
upstream that the toy fixture doesn't satisfy), narrow the dry-run target to a SELECT
intermediate output so only the SELECT rule chain is exercised.

- [ ] **Step 5: Commit**

```bash
git add code/scripts/tests/data/select_toy code/scripts/tests/test_select_toy_dag.py
git commit -m "$(cat <<'EOF'
test(t078): toy integration fixture + DAG dry-run check

Two-study × 1-cancer-type × 5-gene synthetic dataset that exercises
mixed-panel intersection (panel_full vs panel_partial — MYC dropped
from B-tier but kept in st1 A-tier, validating a_only_b_absent).
test_select_toy_dag runs snakemake -n and asserts DAG resolves with
all SELECT rules referenced.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 20: Add biological positive-control regression test

**Why:** Per design Section 8.3, the headline run must reproduce a list of textbook
mutation-observable interactions. Failing this is a `validate.sh` failure. This task
adds the test plus the conditional-skip logic for untestable pairs.

**Files:**
- Create: `code/scripts/tests/check_known_biology.py`
- Modify: `validate.sh` (or whichever script wires this in)

- [ ] **Step 1: Write the check script**

```python
# code/scripts/tests/check_known_biology.py
"""Biological positive-control regression for the t078 SELECT pipeline.

Run after a full run completes, against
results/select/gene_pair_select.feather. Asserts a curated list of
textbook mutation-observable interactions in specific cancer types
recover at b_q_wMI_within_stratum < 0.10 with the expected direction,
conditional on testability.

Testability gates (per design Section 8.3):
  - both genes pass per-cell prevalence floors (i.e. row exists in headline)
  - panel intersection covers both genes (b_n_samples non-NaN)
  - b_n_samples >= 30
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import rich.console

console = rich.console.Console()


@dataclass(frozen=True)
class PositiveControl:
    gene_a: str
    gene_b: str
    cancer_type: str
    expected_direction: str  # "ME" or "CO"
    citation: str


CONTROLS = [
    PositiveControl("KRAS", "BRAF", "coadread", "ME", "Cerami 2012"),
    PositiveControl("KRAS", "BRAF", "luad",     "ME", "Cerami 2012"),
    PositiveControl("KRAS", "NRAS", "coadread", "ME", "RAS-pathway redundancy"),
    PositiveControl("KRAS", "NRAS", "skcm",     "ME", "RAS-pathway redundancy"),
    PositiveControl("IDH1", "IDH2", "gbm",      "ME", "Yan 2009"),
    PositiveControl("IDH1", "IDH2", "lgg",      "ME", "Yan 2009"),
    PositiveControl("APC",  "CTNNB1","coadread","ME", "Wnt-pathway redundancy"),
    PositiveControl("BRAF", "NRAS", "skcm",     "ME", "Davies 2002"),
    PositiveControl("EGFR", "KRAS", "luad",     "ME", "Pao 2005"),
    PositiveControl("TP53", "KEAP1", "luad",    "CO", "Sanchez-Vega 2018"),
    PositiveControl("STK11", "KEAP1", "luad",   "CO", "Skoulidis 2018"),
    PositiveControl("IDH1", "ATRX", "lgg",      "CO", "Brat 2015 TCGA LGG"),
]


def _lookup(headline: pd.DataFrame, ga: str, gb: str, ct: str) -> pd.Series | None:
    sub = headline[headline["cancer_type"] == ct]
    sub = sub[sub["cohort"] == "exclusive"]
    candidate = sub[((sub["gene_i"] == ga) & (sub["gene_j"] == gb))
                    | ((sub["gene_i"] == gb) & (sub["gene_j"] == ga))]
    if candidate.empty:
        return None
    return candidate.iloc[0]


def check(headline: pd.DataFrame, controls: list[PositiveControl] = CONTROLS) -> int:
    failures = 0
    for c in controls:
        row = _lookup(headline, c.gene_a, c.gene_b, c.cancer_type)
        if row is None:
            console.print(
                f"[yellow]SKIP[/yellow] {c.gene_a}↔{c.gene_b} in {c.cancer_type}: "
                "pair not in headline (likely panel intersection or prevalence floor)"
            )
            continue
        if pd.isna(row["b_n_samples"]) or row["b_n_samples"] < 30:
            console.print(
                f"[yellow]SKIP[/yellow] {c.gene_a}↔{c.gene_b} in {c.cancer_type}: "
                f"insufficient samples (n={row.get('b_n_samples')})"
            )
            continue
        q = row["b_q_wMI_within_stratum"]
        d = row["b_direction"]
        if pd.isna(q) or q >= 0.10:
            console.print(
                f"[red]FAIL[/red] {c.gene_a}↔{c.gene_b} in {c.cancer_type}: "
                f"q={q!r} expected <0.10. ({c.citation})"
            )
            failures += 1
            continue
        if d != c.expected_direction:
            console.print(
                f"[red]FAIL[/red] {c.gene_a}↔{c.gene_b} in {c.cancer_type}: "
                f"direction={d!r} expected {c.expected_direction!r}. ({c.citation})"
            )
            failures += 1
            continue
        console.print(
            f"[green]PASS[/green] {c.gene_a}↔{c.gene_b} in {c.cancer_type}: "
            f"q={q:.4f} direction={d}"
        )
    return failures


if __name__ == "__main__":
    import sys
    headline_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
        "results/select/gene_pair_select.feather"
    )
    headline = pd.read_feather(headline_path)
    n_failures = check(headline)
    sys.exit(1 if n_failures else 0)
```

- [ ] **Step 2: Add a wiring test that the script imports cleanly and runs against an
  empty headline (degenerate skip path)**

```python
# code/scripts/tests/test_check_known_biology.py
import pandas as pd

import check_known_biology as mod  # conftest in tests/ adds tests/ to sys.path too


def test_empty_headline_yields_all_skips():
    empty = pd.DataFrame(columns=[
        "gene_i", "gene_j", "cancer_type", "cohort",
        "b_n_samples", "b_q_wMI_within_stratum", "b_direction",
    ])
    failures = mod.check(empty)
    assert failures == 0  # all skipped, none failed


def test_perfect_synthetic_headline_passes():
    rows = []
    for c in mod.CONTROLS:
        rows.append({
            "gene_i": c.gene_a, "gene_j": c.gene_b,
            "cancer_type": c.cancer_type, "cohort": "exclusive",
            "b_n_samples": 100,
            "b_q_wMI_within_stratum": 0.001,
            "b_direction": c.expected_direction,
        })
    df = pd.DataFrame(rows)
    failures = mod.check(df)
    assert failures == 0


def test_synthetic_headline_with_direction_flip_fails():
    c0 = mod.CONTROLS[0]
    rows = [{
        "gene_i": c0.gene_a, "gene_j": c0.gene_b,
        "cancer_type": c0.cancer_type, "cohort": "exclusive",
        "b_n_samples": 100,
        "b_q_wMI_within_stratum": 0.001,
        "b_direction": "CO" if c0.expected_direction == "ME" else "ME",
    }]
    df = pd.DataFrame(rows)
    failures = mod.check(df)
    assert failures == 1
```

- [ ] **Step 3: Run tests + lint**

```bash
uv run --frozen pytest code/scripts/tests/test_check_known_biology.py -v
uv run --frozen ruff check code/scripts/tests/check_known_biology.py
```

Expected: 3 PASS, lint clean.

- [ ] **Step 4: Wire into `validate.sh` (or equivalent)**

Add to the SELECT section of `validate.sh` (after the full-pipeline run):

```bash
if [[ -f "results/select/gene_pair_select.feather" ]]; then
  echo "[validate] running biological positive-control regression"
  uv run --frozen python code/scripts/tests/check_known_biology.py \
    results/select/gene_pair_select.feather
fi
```

- [ ] **Step 5: Commit**

```bash
git add code/scripts/tests/check_known_biology.py \
  code/scripts/tests/test_check_known_biology.py validate.sh
git commit -m "$(cat <<'EOF'
test(t078): biological positive-control regression check

12 textbook mutation-observable interactions (KRAS↔BRAF in coadread/
luad, IDH1↔IDH2 in gbm/lgg, EGFR↔KRAS in luad, TP53↔KEAP1 in luad,
etc.) with testability gates: pair must be in headline, panel
intersection must cover both genes, b_n_samples >= 30. Direction-
flip on any testable pair fails validate.sh. Excluded TP53↔MDM2
(CNA-driven) and any pseudo-cancer-type 'most solid' per design
Section 8.3.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Done

After Task 20:

- [ ] **Final smoke test:** with `select.enabled: true` in `code/config/config-10k-genes.yml`,
  run a full pipeline:

```bash
uv run --frozen snakemake \
  -s code/workflows/Snakefile \
  --configfile code/config/config-10k-genes.yml \
  --use-conda \
  -j8 \
  results/select/gene_pair_select.feather \
  results/select/pathway_aggregated.feather \
  results/select/pathway_rollup_gene_pairs.feather \
  results/select/gene_cancer_study_select_annotation.feather
```

Expected: completes overnight on a workstation; positive-control test passes; QQ plots
look uniform under the null.

- [ ] **Mark task t078 complete in `tasks/active.md`** via:

```bash
uv run science-tool tasks complete t078
```

- [ ] **Cross-link from the design doc:** add a closing note to
  `doc/plans/2026-04-25-t078-select-cooccurrence-design.md` pointing at this
  implementation plan as the executed plan and noting the actual completion date.
