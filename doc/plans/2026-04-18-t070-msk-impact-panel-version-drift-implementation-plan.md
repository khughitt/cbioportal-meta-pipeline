# t070 — MSK-IMPACT panel-version drift handling implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the pipeline's study-level panel assumption with per-sample panel resolution for MSK-IMPACT and related cBioPortal studies, fixing both the per-(cancer, gene) frequency-table denominator and the per-sample TMB denominator.

**Architecture:** A new pure module `resolve_panel_id.py` normalizes the three observed panel-naming conventions and applies a 3-step resolution chain (matrix file → sample-id suffix → study-level fallback). `convert_to_feather.py` ingests the per-sample `data_gene_panel_matrix.txt` and attaches a canonical `panel_id` column to `samples.feather`. Downstream, `compute_per_sample_tmb.py` keys its denominator on per-sample `panel_id`, `create_freq_tables.py` makes its gene-bearing denominators panel-aware, and `create_combined_gene_cancer_freq_table.py` adds sample-weighted callability columns.

**Tech Stack:** Python 3.11+, pandas, pyarrow, snakemake 9, pytest, uv.

**Spec:** `doc/plans/2026-04-18-t070-msk-impact-panel-version-drift-design.md`. Read the spec before starting; it defines the contract every task implements.

---

## File structure

| File | Action | Responsibility |
|---|---|---|
| `code/scripts/resolve_panel_id.py` | create | Pure resolution: aliases, suffix map, `normalize_panel_id`, `infer_panel_from_sample_id`, `resolve_panel_ids` |
| `code/scripts/tests/test_resolve_panel_id.py` | create | Unit tests for all three resolution paths + failure modes |
| `code/scripts/download_study.py` | modify | Tarball already includes matrix file when present; add explicit output declaration |
| `code/workflows/Snakefile` | modify | `download_study` + `convert_to_feather` rules — add conditional matrix-file plumbing |
| `code/scripts/convert_to_feather.py` | modify | Read matrix file (when present), call `resolve_panel_ids`, attach `panel_id` to `samples.feather` |
| `code/scripts/tests/test_convert_to_feather.py` | create | Integration test for matrix-file ingestion |
| `code/scripts/compute_per_sample_tmb.py` | modify | Replace study-level lookup with per-sample `panel_id` lookup |
| `code/scripts/tests/test_compute_per_sample_tmb.py` | modify | Add mixed-panel-within-study fixture |
| `code/scripts/create_freq_tables.py` | modify | Make gene/gene_cancer denominators panel-aware via `(panel_id, gene)` callability join |
| `code/scripts/tests/test_create_freq_tables.py` | modify | Add panel-aware fixture |
| `code/scripts/create_combined_gene_cancer_freq_table.py` | modify | Pivot per-study `n_inclusive`/`n_exclusive`; add 4 paired sample-weighted columns to `_annotate_callability` |
| `code/scripts/tests/test_create_combined_gene_cancer_freq_table.py` | modify | Add mixed-panel cross-study fixture |
| `code/config/config-poc.yml` | modify | Populate `panel_bearing_studies`, `study_panel_map` for `msk_impact_2017` |
| `code/config/config-10k-genes.yml`, `config-pan-cancer.yml`, `config-full.yml` | modify | Add `panel_bearing_studies` (empty or per-study list) so configs round-trip |
| `doc/interpretations/<implementation-date>-t070-poc-comparison.md` | create | Validation deliverable: pre/post comparison on `msk_impact_2017` |

---

## Task 1: `resolve_panel_id.py` — constants + `normalize_panel_id`

**Files:**
- Create: `code/scripts/resolve_panel_id.py`
- Test: `code/scripts/tests/test_resolve_panel_id.py`

- [ ] **Step 1: Write the failing test**

```python
# code/scripts/tests/test_resolve_panel_id.py
"""Tests for resolve_panel_id (t070 spec)."""
import pytest

from resolve_panel_id import normalize_panel_id


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("IMPACT341", "MSK-IMPACT-341"),
        ("MSK-IMPACT341", "MSK-IMPACT-341"),
        ("MSK-IMPACT-341", "MSK-IMPACT-341"),
        ("IMPACT410", "MSK-IMPACT-410"),
        ("IMPACT468", "MSK-IMPACT-468"),
        ("IMPACT505", "MSK-IMPACT-505"),
        ("IMPACT-HEME-400", "MSK-IMPACT-HEME-400"),
        ("MSK-IMPACT-HEME-400", "MSK-IMPACT-HEME-400"),
    ],
)
def test_normalize_panel_id_known(raw: str, expected: str) -> None:
    assert normalize_panel_id(raw) == expected


def test_normalize_panel_id_strips_whitespace() -> None:
    assert normalize_panel_id("  IMPACT468  ") == "MSK-IMPACT-468"


def test_normalize_panel_id_unknown_raises() -> None:
    with pytest.raises(ValueError, match="Unrecognized panel_id"):
        normalize_panel_id("FOUNDATIONONE-CDX")
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
cd /mnt/ssd/Dropbox/cancer/data-sources/cbioportal
uv run --frozen pytest code/scripts/tests/test_resolve_panel_id.py -v
```
Expected: ImportError on `resolve_panel_id`.

- [ ] **Step 3: Implement constants + `normalize_panel_id`**

```python
# code/scripts/resolve_panel_id.py
"""Per-sample panel-version resolution for MSK-IMPACT and related cBioPortal studies.

Implements t070 (see ``doc/plans/2026-04-18-t070-msk-impact-panel-version-drift-design.md``).

Three observed panel-naming conventions in upstream data are normalized to one
canonical form (matching `panel_callable_mb_override` config keys):

- cBioPortal `data_gene_panel_matrix.txt`: `IMPACT341`
- AACR GENIE `SEQ_ASSAY_ID`: `MSK-IMPACT341`
- Project-canonical: `MSK-IMPACT-341`

References:
- Cheng DT et al. 2015. *J Mol Diagn* 17(3):251-264. PMID 25801821. (IMPACT-341/410)
- Zehir A et al. 2017. *Nat Med* 23(6):703-713. PMID 28481359. (IMPACT-410/468)
- Bandlamudi C et al. 2026. *Cancer Cell*. PMID 41895280. (IMPACT-505)
"""

PANEL_ALIASES: dict[str, str] = {
    # IMPACT-341
    "IMPACT341": "MSK-IMPACT-341",
    "MSK-IMPACT341": "MSK-IMPACT-341",
    "MSK-IMPACT-341": "MSK-IMPACT-341",
    # IMPACT-410
    "IMPACT410": "MSK-IMPACT-410",
    "MSK-IMPACT410": "MSK-IMPACT-410",
    "MSK-IMPACT-410": "MSK-IMPACT-410",
    # IMPACT-468
    "IMPACT468": "MSK-IMPACT-468",
    "MSK-IMPACT468": "MSK-IMPACT-468",
    "MSK-IMPACT-468": "MSK-IMPACT-468",
    # IMPACT-505
    "IMPACT505": "MSK-IMPACT-505",
    "MSK-IMPACT505": "MSK-IMPACT-505",
    "MSK-IMPACT-505": "MSK-IMPACT-505",
    # IMPACT-HEME-400 / 468
    "IMPACT-HEME-400": "MSK-IMPACT-HEME-400",
    "MSK-IMPACT-HEME-400": "MSK-IMPACT-HEME-400",
    "IMPACT-HEME-468": "MSK-IMPACT-HEME-468",
    "MSK-IMPACT-HEME-468": "MSK-IMPACT-HEME-468",
}


def normalize_panel_id(raw: str) -> str:
    """Canonicalize a raw panel string to the project-canonical form.

    Raises ``ValueError`` for unrecognized panels — fail-loud, no silent fallback.
    """
    key = raw.strip()
    canonical = PANEL_ALIASES.get(key)
    if canonical is None:
        raise ValueError(
            f"Unrecognized panel_id {raw!r}; add to PANEL_ALIASES if real, "
            "or fix upstream data."
        )
    return canonical
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
uv run --frozen pytest code/scripts/tests/test_resolve_panel_id.py -v
```
Expected: 9 passed.

- [ ] **Step 5: Run lint + type check**

```bash
uv run --frozen ruff check code/scripts/resolve_panel_id.py code/scripts/tests/test_resolve_panel_id.py
uv run --frozen ruff format --check code/scripts/resolve_panel_id.py code/scripts/tests/test_resolve_panel_id.py
```
Expected: no errors. If formatting fails, run `uv run --frozen ruff format <files>` and re-check.

- [ ] **Step 6: Commit**

```bash
git add code/scripts/resolve_panel_id.py code/scripts/tests/test_resolve_panel_id.py
git commit -m "t070: resolve_panel_id — alias map + normalize_panel_id"
```

---

## Task 2: `infer_panel_from_sample_id`

**Files:**
- Modify: `code/scripts/resolve_panel_id.py`
- Modify: `code/scripts/tests/test_resolve_panel_id.py`

- [ ] **Step 1: Write the failing test**

Append to `code/scripts/tests/test_resolve_panel_id.py`:

```python
from resolve_panel_id import infer_panel_from_sample_id


@pytest.mark.parametrize(
    "sample_id,expected",
    [
        ("P-0000004-T01-IM3", "MSK-IMPACT-341"),
        ("P-0029495-T03-IM5", "MSK-IMPACT-410"),
        ("P-0029974-T02-IM6", "MSK-IMPACT-468"),
        ("P-0050000-T01-IM7", "MSK-IMPACT-505"),
        ("P-0034805-T01-IH3", "MSK-IMPACT-HEME-400"),
    ],
)
def test_infer_panel_from_sample_id_known(sample_id: str, expected: str) -> None:
    assert infer_panel_from_sample_id(sample_id) == expected


@pytest.mark.parametrize(
    "sample_id",
    [
        "TCGA-AB-1234-01",            # TCGA — no IMPACT suffix
        "P-0000001-T01",              # truncated
        "P-0000001-T01-XYZ",          # unrecognized suffix
        "",
    ],
)
def test_infer_panel_from_sample_id_returns_none(sample_id: str) -> None:
    assert infer_panel_from_sample_id(sample_id) is None
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
uv run --frozen pytest code/scripts/tests/test_resolve_panel_id.py -v
```
Expected: ImportError on `infer_panel_from_sample_id`.

- [ ] **Step 3: Implement `infer_panel_from_sample_id`**

Append to `code/scripts/resolve_panel_id.py` (after `normalize_panel_id`):

```python
SAMPLE_ID_SUFFIX_MAP: dict[str, str] = {
    "IM3": "MSK-IMPACT-341",
    "IM5": "MSK-IMPACT-410",
    "IM6": "MSK-IMPACT-468",
    "IM7": "MSK-IMPACT-505",
    "IH3": "MSK-IMPACT-HEME-400",
}


def infer_panel_from_sample_id(sample_id: str) -> str | None:
    """Parse the trailing ``-IM[3567]`` / ``-IH3`` suffix from an MSK sample id.

    Returns ``None`` if the sample id has no recognized suffix (TCGA / GENIE /
    other formats). Suffix convention: Cheng 2015 + IMPACT release notes.
    """
    if not sample_id:
        return None
    suffix = sample_id.rsplit("-", 1)[-1]
    return SAMPLE_ID_SUFFIX_MAP.get(suffix)
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
uv run --frozen pytest code/scripts/tests/test_resolve_panel_id.py -v
```
Expected: 18 passed (9 prior + 9 new).

- [ ] **Step 5: Lint check + commit**

```bash
uv run --frozen ruff check code/scripts/resolve_panel_id.py code/scripts/tests/test_resolve_panel_id.py
git add code/scripts/resolve_panel_id.py code/scripts/tests/test_resolve_panel_id.py
git commit -m "t070: resolve_panel_id — sample-id suffix inference"
```

---

## Task 3: `resolve_panel_ids` orchestrator

**Files:**
- Modify: `code/scripts/resolve_panel_id.py`
- Modify: `code/scripts/tests/test_resolve_panel_id.py`

- [ ] **Step 1: Write the failing tests**

Append to `code/scripts/tests/test_resolve_panel_id.py`:

```python
import pandas as pd

from resolve_panel_id import resolve_panel_ids


def _samples(ids: list[str]) -> pd.DataFrame:
    return pd.DataFrame({"sample_id": ids})


def _matrix(rows: list[tuple[str, str]]) -> pd.DataFrame:
    return pd.DataFrame.from_records(rows, columns=["SAMPLE_ID", "mutations"])


def test_resolve_via_matrix() -> None:
    samples = _samples(["P-0000004-T01-IM3", "P-0029974-T02-IM6"])
    matrix = _matrix([("P-0000004-T01-IM3", "IMPACT341"), ("P-0029974-T02-IM6", "IMPACT468")])
    result = resolve_panel_ids(
        samples, matrix=matrix, study_id="msk_impact_2017",
        study_panel_map={}, is_panel_study=True,
    )
    assert list(result) == ["MSK-IMPACT-341", "MSK-IMPACT-468"]


def test_resolve_via_suffix_when_matrix_missing() -> None:
    samples = _samples(["P-0000012-N02-IM6", "P-0000023-N01-IM3"])
    result = resolve_panel_ids(
        samples, matrix=None, study_id="msk_ch_2023",
        study_panel_map={}, is_panel_study=True,
    )
    assert list(result) == ["MSK-IMPACT-468", "MSK-IMPACT-341"]


def test_resolve_via_study_fallback() -> None:
    samples = _samples(["FOO-1", "FOO-2"])
    result = resolve_panel_ids(
        samples, matrix=None, study_id="custom_panel_2025",
        study_panel_map={"custom_panel_2025": "MSK-IMPACT-410"},
        is_panel_study=True,
    )
    assert list(result) == ["MSK-IMPACT-410", "MSK-IMPACT-410"]


def test_non_panel_study_returns_all_none() -> None:
    samples = _samples(["TCGA-AB-1234-01", "TCGA-CD-5678-01"])
    result = resolve_panel_ids(
        samples, matrix=None, study_id="brca_tcga",
        study_panel_map={}, is_panel_study=False,
    )
    assert result.isna().all()


def test_panel_study_with_unresolvable_sample_raises() -> None:
    samples = _samples(["P-0000001-T01-IM3", "MYSTERY-SAMPLE"])
    matrix = _matrix([("P-0000001-T01-IM3", "IMPACT341")])
    with pytest.raises(ValueError, match="MYSTERY-SAMPLE"):
        resolve_panel_ids(
            samples, matrix=matrix, study_id="msk_impact_2017",
            study_panel_map={}, is_panel_study=True,
        )


def test_matrix_takes_precedence_over_suffix() -> None:
    # If matrix says IMPACT468 but suffix says IMPACT341, matrix wins
    samples = _samples(["P-0000001-T01-IM3"])
    matrix = _matrix([("P-0000001-T01-IM3", "IMPACT468")])
    result = resolve_panel_ids(
        samples, matrix=matrix, study_id="msk_impact_2017",
        study_panel_map={}, is_panel_study=True,
    )
    assert list(result) == ["MSK-IMPACT-468"]
```

- [ ] **Step 2: Run the tests to verify they fail**

```bash
uv run --frozen pytest code/scripts/tests/test_resolve_panel_id.py -v
```
Expected: ImportError on `resolve_panel_ids`.

- [ ] **Step 3: Implement `resolve_panel_ids`**

Append to `code/scripts/resolve_panel_id.py`:

```python
import pandas as pd


def resolve_panel_ids(
    samples: pd.DataFrame,
    matrix: pd.DataFrame | None,
    study_id: str,
    study_panel_map: dict[str, str],
    is_panel_study: bool,
) -> pd.Series:
    """Return a panel_id Series indexed like ``samples`` (positionally).

    For non-panel studies (``is_panel_study=False``), returns all-NaN — downstream
    consumers treat this as the "panel-aware path bypassed" signal.

    For panel studies, the per-sample resolution chain is:
      1. ``matrix['mutations']`` column normalized via :data:`PANEL_ALIASES`
      2. :func:`infer_panel_from_sample_id` applied to ``sample_id``
      3. ``study_panel_map[study_id]`` (single panel applied to all samples)

    Anything unresolved raises ``ValueError`` carrying ``(study_id, sample_id)``.
    """
    if not is_panel_study:
        return pd.Series([None] * len(samples), index=samples.index, dtype="object")

    sample_ids = samples["sample_id"].astype(str)

    matrix_lookup: dict[str, str] = {}
    if matrix is not None and not matrix.empty:
        sid_col = "SAMPLE_ID" if "SAMPLE_ID" in matrix.columns else matrix.columns[0]
        mut_col = "mutations" if "mutations" in matrix.columns else matrix.columns[1]
        matrix_lookup = {
            str(s): normalize_panel_id(str(p))
            for s, p in zip(matrix[sid_col], matrix[mut_col], strict=False)
            if pd.notna(p) and str(p).strip()
        }

    study_default = study_panel_map.get(study_id)
    if study_default is not None:
        study_default = normalize_panel_id(study_default)

    out: list[str] = []
    for sid in sample_ids:
        resolved = matrix_lookup.get(sid)
        if resolved is None:
            resolved = infer_panel_from_sample_id(sid)
        if resolved is None:
            resolved = study_default
        if resolved is None:
            raise ValueError(
                f"Cannot resolve panel_id for sample {sid!r} in panel study "
                f"{study_id!r}: not in matrix, no recognized sample-id suffix, "
                "no study_panel_map fallback. Investigate upstream data."
            )
        out.append(resolved)

    return pd.Series(out, index=samples.index, dtype="object")
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
uv run --frozen pytest code/scripts/tests/test_resolve_panel_id.py -v
```
Expected: 24 passed.

- [ ] **Step 5: Lint + commit**

```bash
uv run --frozen ruff check code/scripts/resolve_panel_id.py code/scripts/tests/test_resolve_panel_id.py
uv run --frozen ruff format code/scripts/resolve_panel_id.py code/scripts/tests/test_resolve_panel_id.py
git add code/scripts/resolve_panel_id.py code/scripts/tests/test_resolve_panel_id.py
git commit -m "t070: resolve_panel_id — orchestrator with full resolution chain"
```

---

## Task 4: Snakemake DAG — `download_study` + `convert_to_feather` matrix wiring

**Files:**
- Modify: `code/scripts/download_study.py`
- Modify: `code/workflows/Snakefile` (rules `download_study` lines ~455–460 and `convert_to_feather` lines ~441–453)

- [ ] **Step 1: Inspect current Snakefile rule shapes**

```bash
grep -n -A 12 "rule download_study\|rule convert_to_feather" code/workflows/Snakefile
```

Confirm `download_study` outputs are `data_mutations.txt`, `data_clinical_sample.txt`, `data_clinical_patient.txt` and `convert_to_feather` inputs are the same three.

- [ ] **Step 2: Add the conditional input function above `convert_to_feather` rule**

In `code/workflows/Snakefile`, just above `rule convert_to_feather:`:

```python
def _convert_to_feather_inputs(wildcards):
    """Conditional input list: matrix file appended for panel-bearing studies.

    Matches the static classification in config[`panel_bearing_studies`]; do not
    file-existence-test (would make the DAG non-deterministic).
    """
    base = {
        "mutations": data_dir.joinpath(f"{wildcards.id}/data_mutations.txt"),
        "samples":   data_dir.joinpath(f"{wildcards.id}/data_clinical_sample.txt"),
        "patients":  data_dir.joinpath(f"{wildcards.id}/data_clinical_patient.txt"),
    }
    if wildcards.id in config.get("panel_bearing_studies", []):
        base["panel_matrix"] = data_dir.joinpath(
            f"{wildcards.id}/data_gene_panel_matrix.txt"
        )
    return base
```

- [ ] **Step 3: Update `rule convert_to_feather` to use the input function**

Replace the existing `input:` block of `rule convert_to_feather:` with:

```python
  input:
    unpack(_convert_to_feather_inputs)
```

Outputs and `script:` line stay unchanged.

- [ ] **Step 4: Update `rule download_study` to conditionally declare the matrix output**

Replace the `rule download_study` block with:

```python
def _download_study_outputs(wildcards):
    base = [
        data_dir.joinpath(f"{wildcards.id}/data_mutations.txt"),
        data_dir.joinpath(f"{wildcards.id}/data_clinical_sample.txt"),
        data_dir.joinpath(f"{wildcards.id}/data_clinical_patient.txt"),
    ]
    if wildcards.id in config.get("panel_bearing_studies", []):
        base.append(data_dir.joinpath(f"{wildcards.id}/data_gene_panel_matrix.txt"))
    return base


rule download_study:
  output:
    _download_study_outputs
  script:
    "../scripts/download_study.py"
```

(Snakemake supports a function returning a list for `output:` the same way it supports it for `input:`. The download script already extracts the full tarball, so the matrix file ends up on disk regardless; declaring it as an output makes the DAG aware of it.)

- [ ] **Step 5: Lint the workflow**

```bash
uv run snakemake --lint -s code/workflows/Snakefile --configfile code/config/config-poc.yml
```

Expected: clean (or only pre-existing warnings unrelated to these rules).

- [ ] **Step 6: Commit**

```bash
git add code/workflows/Snakefile code/scripts/download_study.py
git commit -m "t070: Snakemake DAG — conditional data_gene_panel_matrix.txt plumbing"
```

(`download_study.py` is unchanged in this task — the existing tarball-extract logic already produces the matrix file when the upstream tarball includes it. The rule-level output declaration is what makes the DAG aware.)

---

## Task 5: `convert_to_feather.py` — ingest matrix file, attach `panel_id`

**Files:**
- Modify: `code/scripts/convert_to_feather.py`
- Create: `code/scripts/tests/test_convert_to_feather.py`

- [ ] **Step 1: Write the failing test**

```python
# code/scripts/tests/test_convert_to_feather.py
"""Tests for convert_to_feather panel_id ingestion (t070)."""
from pathlib import Path

import pandas as pd
import pytest

from resolve_panel_id import resolve_panel_ids


def _write_clinical_sample(p: Path, ids: list[str]) -> None:
    header = "PATIENT_ID\tSAMPLE_ID\tCANCER_TYPE\tCANCER_TYPE_DETAILED\tONCOTREE_CODE\n"
    body = "".join(f"{i.split('-T')[0]}\t{i}\tLung Cancer\tLUAD\tLUAD\n" for i in ids)
    p.write_text("#" + header + "#" + header + "#STRING\n#1\n" + header + body)


def _write_matrix(p: Path, rows: list[tuple[str, str]]) -> None:
    p.write_text(
        "SAMPLE_ID\tmutations\tcna\tstructural_variants\n"
        + "".join(f"{sid}\t{panel}\t{panel}\t{panel}\n" for sid, panel in rows)
    )


def test_resolve_panel_ids_via_matrix(tmp_path: Path) -> None:
    """Smoke test: matrix-based resolution end-to-end through resolve_panel_ids."""
    sample_p = tmp_path / "data_clinical_sample.txt"
    matrix_p = tmp_path / "data_gene_panel_matrix.txt"
    _write_clinical_sample(sample_p, ["P-1-T01-IM3", "P-2-T01-IM6"])
    _write_matrix(matrix_p, [("P-1-T01-IM3", "IMPACT341"), ("P-2-T01-IM6", "IMPACT468")])

    samples = pd.read_csv(sample_p, sep="\t", comment="#")
    samples = samples.rename(columns={"SAMPLE_ID": "sample_id"})
    matrix = pd.read_csv(matrix_p, sep="\t")

    panel_ids = resolve_panel_ids(
        samples, matrix=matrix, study_id="msk_impact_2017",
        study_panel_map={}, is_panel_study=True,
    )
    assert list(panel_ids) == ["MSK-IMPACT-341", "MSK-IMPACT-468"]
```

- [ ] **Step 2: Run the test to verify it passes**

```bash
uv run --frozen pytest code/scripts/tests/test_convert_to_feather.py -v
```

Expected: 1 passed (this exercises `resolve_panel_ids` from Task 3 directly; it confirms that the file-format reading round-trips through the resolution function).

- [ ] **Step 3: Update `convert_to_feather.py` to attach `panel_id` column**

In `code/scripts/convert_to_feather.py`, just before `# save result` for the sample metadata block (before line ~189, the `sample_mdat.to_feather(snek.output[1])` for samples):

```python
# t070: per-sample panel_id resolution. Matrix file is a conditional input;
# absence => non-panel study (resolve_panel_ids returns all-NaN).
from resolve_panel_id import resolve_panel_ids  # type: ignore[import-not-found]

study_id = snek.wildcards["id"]
is_panel_study = study_id in snek.config.get("panel_bearing_studies", [])
matrix_path = getattr(snek.input, "panel_matrix", None)
matrix_df = (
    pd.read_csv(matrix_path, sep="\t", dtype=str) if matrix_path else None
)
sample_mdat["panel_id"] = resolve_panel_ids(
    sample_mdat,
    matrix=matrix_df,
    study_id=study_id,
    study_panel_map=snek.config.get("study_panel_map", {}),
    is_panel_study=is_panel_study,
).to_numpy()
```

- [ ] **Step 4: Lint the script**

```bash
uv run --frozen ruff check code/scripts/convert_to_feather.py code/scripts/tests/test_convert_to_feather.py
uv run --frozen ruff format code/scripts/convert_to_feather.py code/scripts/tests/test_convert_to_feather.py
```

- [ ] **Step 5: Smoke-test via PoC config (one panel study)**

```bash
cd /mnt/ssd/Dropbox/cancer/data-sources/cbioportal
uv run snakemake -s code/workflows/Snakefile -j1 --configfile code/config/config-poc.yml \
  --until convert_to_feather \
  /data/packages/cbioportal/poc-2026-04-17/studies/msk_impact_2017/metadata/samples.feather \
  --forceall
```

(If the PoC config doesn't yet have `panel_bearing_studies` populated, this will produce all-NaN `panel_id` — that's fine; the next task wires the config.)

- [ ] **Step 6: Verify `panel_id` column exists**

```bash
uv run python -c "
import pandas as pd
df = pd.read_feather('/data/packages/cbioportal/poc-2026-04-17/studies/msk_impact_2017/metadata/samples.feather')
print(df.columns.tolist())
print(df['panel_id'].value_counts(dropna=False))
"
```

Expected: column `panel_id` present. Values either all NaN (if config not yet updated) or a mix of `MSK-IMPACT-{341,410}` (after Task 9's config update; Task 9 is intentionally last).

- [ ] **Step 7: Commit**

```bash
git add code/scripts/convert_to_feather.py code/scripts/tests/test_convert_to_feather.py
git commit -m "t070: convert_to_feather — ingest data_gene_panel_matrix.txt, attach panel_id"
```

---

## Task 6: `compute_per_sample_tmb.py` — per-sample panel lookup

**Files:**
- Modify: `code/scripts/compute_per_sample_tmb.py`
- Modify: `code/scripts/tests/test_compute_per_sample_tmb.py`

- [ ] **Step 1: Read the current TMB lookup**

```bash
sed -n '155,195p' code/scripts/compute_per_sample_tmb.py
```

Note the `_lookup_panel_size_for_study(study_id, study_panel_map, panel_registry, ...)` function. The replacement keys on each sample's `panel_id` rather than on `study_panel_map[study_id]`.

- [ ] **Step 2: Read existing test fixtures**

```bash
grep -n "def test_\|def _samples\|def _muts" code/scripts/tests/test_compute_per_sample_tmb.py | head -30
```

Identify how the existing tests construct the samples DataFrame so the new test can extend the same pattern.

- [ ] **Step 3: Write the failing test**

Append to `code/scripts/tests/test_compute_per_sample_tmb.py`:

```python
def test_per_sample_panel_id_drives_denominator(tmp_path) -> None:
    """t070: two samples in the same study with different panel_id values
    must get different TMB denominators."""
    # Build minimal samples + mutations + panel registry inline.
    # (Reuse helpers from existing tests if present; otherwise inline a small DF.)
    samples = pd.DataFrame({
        "sample_id": ["S1", "S2"],
        "panel_id": ["MSK-IMPACT-341", "MSK-IMPACT-468"],
        "study_id": ["msk_impact_2017", "msk_impact_2017"],
    })
    mutations = pd.DataFrame({
        "sample_id_tumor": ["S1", "S1", "S2"],
        "symbol": ["TP53", "KRAS", "BRCA1"],
        "variant_class": ["Missense_Mutation"] * 3,
    })
    panel_registry = pd.DataFrame({
        "panel_id": ["MSK-IMPACT-341", "MSK-IMPACT-468"],
        "callable_mb": [0.89, 1.22],
        "source": ["config_override", "config_override"],
    })

    # Call the per-sample TMB function (or its renamed equivalent after Task 6 lands).
    from compute_per_sample_tmb import compute_per_sample_tmb_table
    out = compute_per_sample_tmb_table(
        mutations=mutations,
        samples=samples,
        panel_registry=panel_registry,
        study_id="msk_impact_2017",
        study_panel_map={},
        wes_default_callable_mb=30.0,
        nonsynonymous_classes={"Missense_Mutation"},
    )

    s1 = out.loc[out["sample_id"] == "S1"].iloc[0]
    s2 = out.loc[out["sample_id"] == "S2"].iloc[0]
    # 2 mutations / 0.89 Mb vs 1 mutation / 1.22 Mb
    assert s1["callable_mb"] == pytest.approx(0.89)
    assert s2["callable_mb"] == pytest.approx(1.22)
    assert s1["tmb"] == pytest.approx(2 / 0.89, rel=1e-6)
    assert s2["tmb"] == pytest.approx(1 / 1.22, rel=1e-6)
```

If the existing function signature differs, adapt the test to match — but assert per-sample denominator divergence either way.

- [ ] **Step 4: Run the test to verify it fails**

```bash
uv run --frozen pytest code/scripts/tests/test_compute_per_sample_tmb.py::test_per_sample_panel_id_drives_denominator -v
```

Expected: FAIL — current implementation uses one denominator per study.

- [ ] **Step 5: Refactor `_lookup_panel_size_for_study` → `_lookup_panel_size_for_sample`**

Replace the existing function (~line 155 onwards) with:

```python
def _lookup_panel_size_for_sample(
    sample_panel_id: str | None,
    study_id: str,
    study_panel_map: dict[str, str],
    panel_registry: pd.DataFrame,
    wes_default_callable_mb: float,
) -> tuple[float, str]:
    """Per-sample callable-Mb lookup (t070).

    Lookup order:
      1. ``sample_panel_id`` (from samples.feather panel_id column) → panel registry
      2. ``study_panel_map[study_id]`` → panel registry (legacy / non-MSK panel studies)
      3. registry ``wes_default`` row
      4. ``wes_default_callable_mb`` literal

    Step 1 fails-loud (raises) if ``sample_panel_id`` is non-null but absent from
    the registry — see t070 design Error Handling #3.
    """
    if sample_panel_id is not None and pd.notna(sample_panel_id):
        matches = panel_registry.loc[panel_registry["panel_id"] == sample_panel_id]
        if matches.empty:
            raise ValueError(
                f"Sample panel_id {sample_panel_id!r} (study={study_id!r}) is not in "
                "panel_callable_mb registry. Add an entry to "
                "config[panel_callable_mb_override] or supply BED coverage."
            )
        row = matches.iloc[0]
        return float(row["callable_mb"]), str(row["source"])

    panel_id = study_panel_map.get(study_id)
    if panel_id is not None:
        matches = panel_registry.loc[panel_registry["panel_id"] == panel_id]
        if not matches.empty:
            row = matches.iloc[0]
            return float(row["callable_mb"]), str(row["source"])
        logger.warning(
            "Study %s maps to panel %r which is absent from registry; "
            "falling back to WES default.", study_id, panel_id,
        )

    wes_matches = panel_registry.loc[panel_registry["source"] == "wes_default"]
    if not wes_matches.empty:
        return float(wes_matches.iloc[0]["callable_mb"]), "wes_default"
    return float(wes_default_callable_mb), "wes_default"
```

Then update the per-sample loop in `compute_per_sample_tmb_table` to call the new function once per sample, passing `sample.panel_id`. Specifically — locate the existing call site:

```bash
grep -n "_lookup_panel_size_for_study" code/scripts/compute_per_sample_tmb.py
```

Replace it with a per-sample iteration. The simplest change: build a `(callable_mb, source)` Series indexed by sample_id, then merge into the output. Inline the DataFrame join:

```python
panel_lookup = samples[["sample_id", "panel_id"]].apply(
    lambda r: _lookup_panel_size_for_sample(
        r["panel_id"], study_id, study_panel_map, panel_registry, wes_default_callable_mb,
    ),
    axis=1, result_type="expand",
)
panel_lookup.columns = ["callable_mb", "callable_mb_source"]
panel_lookup["sample_id"] = samples["sample_id"].to_numpy()
```

Then merge `panel_lookup` into the per-sample TMB output instead of broadcasting the single per-study value.

- [ ] **Step 6: Run all TMB tests**

```bash
uv run --frozen pytest code/scripts/tests/test_compute_per_sample_tmb.py -v
```

Expected: all pass (including the new one). Existing tests should still pass — for studies without `panel_id` (set in fixtures to NaN or absent), the function falls through to the study-level path.

- [ ] **Step 7: Lint + commit**

```bash
uv run --frozen ruff check code/scripts/compute_per_sample_tmb.py code/scripts/tests/test_compute_per_sample_tmb.py
uv run --frozen ruff format code/scripts/compute_per_sample_tmb.py code/scripts/tests/test_compute_per_sample_tmb.py
git add code/scripts/compute_per_sample_tmb.py code/scripts/tests/test_compute_per_sample_tmb.py
git commit -m "t070: compute_per_sample_tmb — per-sample panel_id lookup"
```

---

## Task 7: `create_freq_tables.py` — panel-aware gene-bearing denominators

**Files:**
- Modify: `code/scripts/create_freq_tables.py`
- Modify: `code/scripts/tests/test_create_freq_tables.py`

This is the most subtle task. The current `_build_gene_table` and `_build_gene_cancer_table` use cohort-wide / per-cancer denominators. The new versions must compute per-(gene) and per-(cancer, gene) panel-restricted denominators by joining samples on a `(panel_id, gene)` callability table.

- [ ] **Step 1: Inspect current function signatures**

```bash
grep -n "def compute_freq_tables\|def _build" code/scripts/create_freq_tables.py
```

Note: `compute_freq_tables(mutations, samples, hypermutator_flags)` returns 4 DataFrames. Tests call it with these positional args. The new signature adds an optional `panel_coverage` argument (per-`(panel_id, gene)` callability) — kept optional so WES studies and existing tests keep working.

- [ ] **Step 2: Write the failing test**

Append to `code/scripts/tests/test_create_freq_tables.py`:

```python
def test_panel_aware_gene_cancer_denominator() -> None:
    """t070: when samples are panel-mixed and panel_coverage is supplied, the
    denominator for a gene off the smaller panel must be reduced by the count
    of samples on that smaller panel."""
    muts = _muts([
        ("GENE_A", "S1"),  # GENE_A on both panels, mutated in 1 sample
        ("GENE_B", "S2"),  # GENE_B only on PANEL_BIG, mutated in 1 sample
    ])
    samples = pd.DataFrame({
        "sample_id": ["S1", "S2", "S3", "S4"],
        "cancer_type": ["Cancer A"] * 4,
        "cancer_type_detailed": ["A detailed"] * 4,
        "panel_id": ["PANEL_BIG", "PANEL_BIG", "PANEL_SMALL", "PANEL_SMALL"],
    })
    flags = _hypermutator_flags([(s, False) for s in ["S1", "S2", "S3", "S4"]])
    panel_coverage = pd.DataFrame({
        "panel_id": ["PANEL_BIG", "PANEL_BIG", "PANEL_SMALL"],
        "gene":     ["GENE_A",    "GENE_B",   "GENE_A"],
    })

    _, _, _, gene_cancer = compute_freq_tables(
        muts, samples, flags, panel_coverage=panel_coverage,
    )
    row_a = gene_cancer.loc[(gene_cancer["cancer_type"] == "Cancer A") & (gene_cancer["symbol"] == "GENE_A")].iloc[0]
    row_b = gene_cancer.loc[(gene_cancer["cancer_type"] == "Cancer A") & (gene_cancer["symbol"] == "GENE_B")].iloc[0]
    assert row_a["n_samples_inclusive"] == 4   # all panels cover GENE_A
    assert row_b["n_samples_inclusive"] == 2   # only PANEL_BIG covers GENE_B
    assert row_a["num_inclusive"] == 1
    assert row_b["num_inclusive"] == 1
    assert row_a["ratio_inclusive"] == pytest.approx(1 / 4)
    assert row_b["ratio_inclusive"] == pytest.approx(1 / 2)


def test_panel_coverage_none_preserves_cohort_denominator() -> None:
    """t070: when panel_coverage=None (WES study), behavior is unchanged."""
    muts = _muts([("GENE_A", "S1")])
    samples = pd.DataFrame({
        "sample_id": ["S1", "S2"],
        "cancer_type": ["Cancer A", "Cancer A"],
        "cancer_type_detailed": ["A detailed", "A detailed"],
    })
    flags = _hypermutator_flags([("S1", False), ("S2", False)])
    _, _, _, gene_cancer = compute_freq_tables(muts, samples, flags, panel_coverage=None)
    row = gene_cancer.iloc[0]
    assert row["n_samples_inclusive"] == 2
```

Add `import pytest` at the top of the file if not present.

- [ ] **Step 3: Run the tests to verify they fail**

```bash
uv run --frozen pytest code/scripts/tests/test_create_freq_tables.py -v
```

Expected: FAIL on `panel_coverage=` keyword (function doesn't accept it yet) — or test passes for the WES case but fails for the panel-aware case.

- [ ] **Step 4: Add `panel_coverage` parameter and panel-aware path**

Update `compute_freq_tables` signature and pass `panel_coverage` through to `_build_gene_table` and `_build_gene_cancer_table`:

```python
def compute_freq_tables(
    mutations: pd.DataFrame,
    samples: pd.DataFrame,
    hypermutator_flags: pd.DataFrame,
    panel_coverage: pd.DataFrame | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    ...
    gene_df = _build_gene_table(
        mut=mut, samples_meta=samples_meta_with_panel, flags=flags,
        panel_coverage=panel_coverage,
    )
    gene_cancer_df = _build_gene_cancer_table(
        mut=mut, samples_meta=samples_meta_with_panel, flags=flags,
        panel_coverage=panel_coverage,
    )
```

Where `samples_meta_with_panel` is `samples_meta` plus the `panel_id` column (preserved from the input `samples` DataFrame). Adjust the `samples_meta = samples[["sample_id", "cancer_type", "cancer_type_detailed"]]` line to also retain `panel_id` when present:

```python
sample_cols = ["sample_id", "cancer_type", "cancer_type_detailed"]
if "panel_id" in samples.columns:
    sample_cols.append("panel_id")
samples_meta = samples[sample_cols]
```

Then update `_build_gene_table` and `_build_gene_cancer_table` to accept `panel_coverage: pd.DataFrame | None` and branch:

```python
def _build_gene_cancer_table(
    mut: pd.DataFrame,
    samples_meta: pd.DataFrame,
    flags: pd.DataFrame,
    panel_coverage: pd.DataFrame | None = None,
) -> pd.DataFrame:
    samples_with_flag = samples_meta.merge(flags, on="sample_id")

    if panel_coverage is None or "panel_id" not in samples_with_flag.columns:
        # Cohort-wide denominator (legacy path).
        # PRESERVE the existing body of _build_gene_cancer_table verbatim here
        # (the n_inclusive_by_cancer / n_exclusive_by_cancer / num_inclusive /
        # num_exclusive computation and DataFrame assembly through the final
        # `return` statement). Wrap it in this `if` branch unchanged. This keeps
        # WES-study behavior bit-identical and ensures all existing tests pass.
        ...  # <-- existing function body goes here verbatim

    # Panel-aware path: per-(cancer, gene) denominator.
    callable_pairs = panel_coverage[["panel_id", "gene"]].drop_duplicates()
    callable_pairs = callable_pairs.rename(columns={"gene": "symbol"})
    panel_gene_samples = samples_with_flag.merge(callable_pairs, on="panel_id")
    # panel_gene_samples columns: sample_id, cancer_type, cancer_type_detailed,
    #   panel_id, is_hypermutator, symbol

    n_inclusive = panel_gene_samples.groupby(
        ["cancer_type", "symbol"], observed=True
    )["sample_id"].nunique()
    n_exclusive = (
        panel_gene_samples.loc[~panel_gene_samples["is_hypermutator"]]
        .groupby(["cancer_type", "symbol"], observed=True)["sample_id"].nunique()
    )

    num_inclusive = mut.groupby(
        ["cancer_type", "symbol"], observed=True
    )["sample_id"].nunique()
    num_exclusive = (
        mut.loc[~mut["is_hypermutator"]]
        .groupby(["cancer_type", "symbol"], observed=True)["sample_id"].nunique()
    )

    df = pd.DataFrame({
        "num_inclusive": num_inclusive,
        "num_exclusive": num_exclusive,
        "n_samples_inclusive": n_inclusive,
        "n_samples_exclusive": n_exclusive,
    })
    df = df.dropna(subset=["n_samples_inclusive"]).fillna(0)
    df = df.astype({
        "num_inclusive": int, "num_exclusive": int,
        "n_samples_inclusive": int, "n_samples_exclusive": int,
    })
    df["ratio_inclusive"] = _safe_ratio(df["num_inclusive"], df["n_samples_inclusive"])
    df["ratio_exclusive"] = _safe_ratio(df["num_exclusive"], df["n_samples_exclusive"])
    df["num"] = df["num_inclusive"]
    df["ratio"] = df["ratio_inclusive"]
    return df.reset_index().sort_values("ratio_inclusive", ascending=False).reset_index(drop=True)
```

For `_build_gene_table` (gene-only, no cancer dimension), apply the same pattern but drop the `cancer_type` grouping:

```python
def _build_gene_table(
    mut: pd.DataFrame,
    samples_meta: pd.DataFrame,
    flags: pd.DataFrame,
    panel_coverage: pd.DataFrame | None = None,
) -> pd.DataFrame:
    samples_with_flag = samples_meta.merge(flags, on="sample_id")

    if panel_coverage is None or "panel_id" not in samples_with_flag.columns:
        # Cohort-wide denominator (legacy path) — keep existing function body here, unchanged.
        n_inclusive = samples_with_flag["sample_id"].nunique()
        n_exclusive = samples_with_flag.loc[
            ~samples_with_flag["is_hypermutator"], "sample_id"
        ].nunique()
        num_inclusive = mut.groupby("symbol", observed=True)["sample_id"].nunique()
        num_exclusive = (
            mut.loc[~mut["is_hypermutator"]]
            .groupby("symbol", observed=True)["sample_id"].nunique()
        )
        df = pd.DataFrame({"num_inclusive": num_inclusive, "num_exclusive": num_exclusive}).fillna(0).astype(int)
        df["n_samples_inclusive"] = n_inclusive
        df["n_samples_exclusive"] = n_exclusive
    else:
        # Panel-aware path: per-gene denominator from panel coverage.
        callable_pairs = panel_coverage[["panel_id", "gene"]].drop_duplicates().rename(
            columns={"gene": "symbol"}
        )
        panel_gene_samples = samples_with_flag.merge(callable_pairs, on="panel_id")
        n_inclusive = panel_gene_samples.groupby("symbol", observed=True)["sample_id"].nunique()
        n_exclusive = (
            panel_gene_samples.loc[~panel_gene_samples["is_hypermutator"]]
            .groupby("symbol", observed=True)["sample_id"].nunique()
        )
        num_inclusive = mut.groupby("symbol", observed=True)["sample_id"].nunique()
        num_exclusive = (
            mut.loc[~mut["is_hypermutator"]]
            .groupby("symbol", observed=True)["sample_id"].nunique()
        )
        df = pd.DataFrame({
            "num_inclusive": num_inclusive,
            "num_exclusive": num_exclusive,
            "n_samples_inclusive": n_inclusive,
            "n_samples_exclusive": n_exclusive,
        }).dropna(subset=["n_samples_inclusive"]).fillna(0).astype({
            "num_inclusive": int, "num_exclusive": int,
            "n_samples_inclusive": int, "n_samples_exclusive": int,
        })

    df["ratio_inclusive"] = _safe_ratio(df["num_inclusive"], df["n_samples_inclusive"])
    df["ratio_exclusive"] = _safe_ratio(df["num_exclusive"], df["n_samples_exclusive"])
    df["num"] = df["num_inclusive"]
    df["ratio"] = df["ratio_inclusive"]
    return df.reset_index().sort_values("ratio_inclusive", ascending=False).reset_index(drop=True)
```

Strategy summary: keep the existing function body inline as the legacy branch (don't extract it into a helper unless the file already uses helpers — keeps the diff smaller and the logic local).

- [ ] **Step 5: Add the prerequisite check (fail-loud on missing coverage)**

In `compute_freq_tables`, before calling the gene-bearing table builders:

```python
if panel_coverage is not None and "panel_id" in samples.columns:
    used_panels = set(samples["panel_id"].dropna().unique())
    coverage_panels = set(panel_coverage["panel_id"].unique())
    missing = used_panels - coverage_panels
    if missing:
        raise ValueError(
            f"Panels {sorted(missing)!r} appear in samples but have no coverage rows "
            "in panel_coverage. Supply BED-derived coverage in genie_panel_coverage.feather, "
            "or remove the panel from PANEL_ALIASES, or remove the study from "
            "panel_bearing_studies."
        )
```

- [ ] **Step 6: Update `_run_via_snakemake` to read `panel_coverage`**

The Snakemake-invoked entry point at the bottom of `create_freq_tables.py` needs to load the panel coverage feather and pass it. Add to the rule's input list in the Snakefile (`rule create_freq_tables` block) — the path is `out_dir.joinpath("metadata/genie_panel_coverage.feather")`.

```python
# At the bottom of create_freq_tables.py
panel_coverage_path = getattr(snek.input, "panel_coverage", None)
panel_coverage_df = (
    pd.read_feather(panel_coverage_path) if panel_coverage_path else None
)
# ... pass into compute_freq_tables(... , panel_coverage=panel_coverage_df)
```

- [ ] **Step 7: Update the Snakefile rule**

In `code/workflows/Snakefile`, add the named input to `rule create_freq_tables` (locate via `grep -n "rule create_freq_tables" code/workflows/Snakefile`):

```python
  input:
    mutations = ...,    # existing
    samples = ...,      # existing
    samples_annotated = ..., # existing
    panel_coverage = out_dir.joinpath("metadata/genie_panel_coverage.feather"),
```

- [ ] **Step 8: Run the freq-table tests**

```bash
uv run --frozen pytest code/scripts/tests/test_create_freq_tables.py -v
```

Expected: all pass — both the new panel-aware tests and the existing tests (which pass `panel_coverage=None` implicitly).

- [ ] **Step 9: Lint + commit**

```bash
uv run --frozen ruff check code/scripts/create_freq_tables.py code/scripts/tests/test_create_freq_tables.py
uv run --frozen ruff format code/scripts/create_freq_tables.py code/scripts/tests/test_create_freq_tables.py
git add code/scripts/create_freq_tables.py code/scripts/tests/test_create_freq_tables.py code/workflows/Snakefile
git commit -m "t070: create_freq_tables — panel-aware per-(cancer, gene) denominator"
```

---

## Task 8: `create_combined_gene_cancer_freq_table.py` — propagate per-study denominators + sample-weighted columns

**Files:**
- Modify: `code/scripts/create_combined_gene_cancer_freq_table.py`
- Modify: `code/scripts/tests/test_create_combined_gene_cancer_freq_table.py`

- [ ] **Step 1: Inspect current `combine_paired_pivot` and `_annotate_callability`**

```bash
grep -n "def combine_paired_pivot\|def _annotate_callability\|combine_paired_pivot(" code/scripts/create_combined_gene_cancer_freq_table.py
```

`combine_paired_pivot` currently produces `(num_df, ratio_df)`. The change: also produce `(n_inclusive_df, n_exclusive_df)` matrices keyed on (cancer_type, symbol) with one column per study.

- [ ] **Step 2: Write the failing test**

Append to `code/scripts/tests/test_create_combined_gene_cancer_freq_table.py`:

```python
def test_paired_panel_covered_samples_columns() -> None:
    """t070: paired n_panel_covered_samples_{inclusive,exclusive} columns must
    differ by exactly the count of panel-callable hypermutator samples for that
    (cancer, gene) row."""
    # Two studies, mixed-panel; one has hypermutators.
    study_a = pd.DataFrame.from_records(
        [
            ("Cancer X", "GENE1", 5, 10, 4, 8, 0.5, 0.5),
            ("Cancer X", "GENE2", 2, 6,  2, 6, 0.333, 0.333),
        ],
        columns=["cancer_type", "symbol",
                 "num_inclusive", "n_samples_inclusive",
                 "num_exclusive", "n_samples_exclusive",
                 "ratio_inclusive", "ratio_exclusive"],
    )
    study_b = pd.DataFrame.from_records(
        [
            ("Cancer X", "GENE1", 3, 8, 3, 8, 0.375, 0.375),
        ],
        columns=["cancer_type", "symbol",
                 "num_inclusive", "n_samples_inclusive",
                 "num_exclusive", "n_samples_exclusive",
                 "ratio_inclusive", "ratio_exclusive"],
    )

    from create_combined_gene_cancer_freq_table import combine_paired_pivot, _annotate_callability

    num_df, ratio_df, n_incl_df, n_excl_df = combine_paired_pivot(
        [("study_a", study_a), ("study_b", study_b)]
    )

    panel_coverage = pd.DataFrame({
        "panel_id": ["PANEL"], "gene": ["GENE1"]  # GENE2 not on any panel
    })
    num_out, ratio_out = _annotate_callability(
        num_df, ratio_df,
        studies=["study_a", "study_b"],
        panel_coverage=panel_coverage,
        study_panel_map={"study_a": "PANEL", "study_b": "PANEL"},
        n_inclusive_df=n_incl_df,
        n_exclusive_df=n_excl_df,
    )

    g1_row = ratio_out.loc[("Cancer X", "GENE1")]
    assert g1_row["n_panel_covered_samples_inclusive"] == 10 + 8
    assert g1_row["n_panel_covered_samples_exclusive"] == 8 + 8
    # Difference is the count of panel-callable hypermutators for this (cancer, gene)
    assert (
        g1_row["n_panel_covered_samples_inclusive"]
        - g1_row["n_panel_covered_samples_exclusive"]
    ) == 2
```

- [ ] **Step 3: Run the test to verify it fails**

```bash
uv run --frozen pytest code/scripts/tests/test_create_combined_gene_cancer_freq_table.py::test_paired_panel_covered_samples_columns -v
```

Expected: FAIL — function signature mismatch, columns don't exist yet.

- [ ] **Step 4: Extend `combine_paired_pivot` to also pivot `n_inclusive`/`n_exclusive`**

Locate `def combine_paired_pivot` and update to return four DataFrames:

```python
def combine_paired_pivot(
    frames: list[tuple[str, pd.DataFrame]],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Pivot per-study frames into wide num/ratio/n_inclusive/n_exclusive matrices.

    Each input frame has rows (cancer_type, symbol) and columns including
    num_inclusive / num_exclusive / n_samples_inclusive / n_samples_exclusive
    / ratio_inclusive / ratio_exclusive.
    """
    num_frames: list[pd.DataFrame] = []
    ratio_frames: list[pd.DataFrame] = []
    n_inclusive_frames: list[pd.DataFrame] = []
    n_exclusive_frames: list[pd.DataFrame] = []

    for study_id, df in frames:
        idx = df.set_index(["cancer_type", "symbol"])
        num_frames.append(idx["num_inclusive"].rename(study_id).to_frame())
        ratio_frames.append(idx["ratio_inclusive"].rename(study_id).to_frame())
        n_inclusive_frames.append(
            idx["n_samples_inclusive"].rename(study_id).to_frame()
        )
        n_exclusive_frames.append(
            idx["n_samples_exclusive"].rename(study_id).to_frame()
        )
        # ... preserve any existing _exclusive-suffixed columns the current code emits

    if not num_frames:
        empty_index = pd.MultiIndex.from_arrays([[], []], names=["cancer_type", "symbol"])
        return tuple(pd.DataFrame(index=empty_index) for _ in range(4))

    num_df = pd.concat(num_frames, axis=1)
    ratio_df = pd.concat(ratio_frames, axis=1)
    n_inclusive_df = pd.concat(n_inclusive_frames, axis=1)
    n_exclusive_df = pd.concat(n_exclusive_frames, axis=1)

    # ... preserve existing mean_inclusive / mean_exclusive / mean derivations on ratio_df

    return num_df, ratio_df, n_inclusive_df, n_exclusive_df
```

Update all call sites of `combine_paired_pivot` to unpack four values instead of two.

- [ ] **Step 5: Update `_annotate_callability` signature and add the four new columns**

```python
def _annotate_callability(
    num_df: pd.DataFrame,
    ratio_df: pd.DataFrame,
    studies: list[str],
    panel_coverage: pd.DataFrame,
    study_panel_map: dict[str, str],
    n_inclusive_df: pd.DataFrame,
    n_exclusive_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Attach study-level + sample-weighted callability annotations (t070)."""
    # ... existing n_total_studies / n_panel_covered_studies / callable_fraction
    #     logic unchanged (preserves current column semantics).

    # New: sample-weighted callability (t070).
    # n_panel_covered_samples_{inclusive,exclusive}: sum across studies of the
    # per-study panel-restricted denominators that landed in n_inclusive_df /
    # n_exclusive_df. The per-study layer (Task 7) already filters these to
    # samples whose panel covers the gene, so summing across studies gives the
    # correct sample-weighted callability count.
    n_panel_covered_inclusive = n_inclusive_df.sum(axis=1, skipna=True).astype("int64")
    n_panel_covered_exclusive = n_exclusive_df.sum(axis=1, skipna=True).astype("int64")

    # n_total_samples_in_cancer: sum of cohort sizes for that cancer-type across
    # all studies, IGNORING panel coverage. For a (cancer, gene) row, the cohort
    # size is the max across genes within that cancer (since cohort sizes are
    # per-cancer, not per-gene, before panel restriction). Equivalent: per-study
    # max(n_samples_inclusive over genes for this cancer), summed across studies.
    cohort_per_study_per_cancer_inclusive = (
        n_inclusive_df.groupby(level="cancer_type").max()
    )
    cohort_per_study_per_cancer_exclusive = (
        n_exclusive_df.groupby(level="cancer_type").max()
    )
    n_total_inclusive = cohort_per_study_per_cancer_inclusive.sum(axis=1, skipna=True)
    n_total_exclusive = cohort_per_study_per_cancer_exclusive.sum(axis=1, skipna=True)

    cancer_index = ratio_df.index.get_level_values("cancer_type")
    n_total_inclusive_per_row = pd.Series(
        cancer_index.map(n_total_inclusive), index=ratio_df.index
    )
    n_total_exclusive_per_row = pd.Series(
        cancer_index.map(n_total_exclusive), index=ratio_df.index
    )

    for df in (num_df, ratio_df):
        df["n_panel_covered_samples_inclusive"] = n_panel_covered_inclusive
        df["n_panel_covered_samples_exclusive"] = n_panel_covered_exclusive
        df["callable_sample_fraction_inclusive"] = (
            n_panel_covered_inclusive / n_total_inclusive_per_row
        ).astype(float)
        df["callable_sample_fraction_exclusive"] = (
            n_panel_covered_exclusive / n_total_exclusive_per_row
        ).astype(float)

    return num_df, ratio_df
```

Update `_run_via_snakemake` to thread `n_inclusive_df` / `n_exclusive_df` from `combine_paired_pivot` into `_annotate_callability`.

- [ ] **Step 6: Run the combined-table tests**

```bash
uv run --frozen pytest code/scripts/tests/test_create_combined_gene_cancer_freq_table.py -v
```

Expected: all pass. If existing tests fail because they unpack `combine_paired_pivot` as a 2-tuple, update those tests to unpack the 4-tuple — that's a real interface change, not a regression.

- [ ] **Step 7: Lint + commit**

```bash
uv run --frozen ruff check code/scripts/create_combined_gene_cancer_freq_table.py code/scripts/tests/test_create_combined_gene_cancer_freq_table.py
uv run --frozen ruff format code/scripts/create_combined_gene_cancer_freq_table.py code/scripts/tests/test_create_combined_gene_cancer_freq_table.py
git add code/scripts/create_combined_gene_cancer_freq_table.py code/scripts/tests/test_create_combined_gene_cancer_freq_table.py
git commit -m "t070: cross-study annotation — sample-weighted paired callability columns"
```

---

## Task 9: Wire configs — `panel_bearing_studies` + `study_panel_map` per config

**Files:**
- Modify: `code/config/config-poc.yml`
- Modify: `code/config/config-10k-genes.yml`
- Modify: `code/config/config-pan-cancer.yml`
- Modify: `code/config/config-full.yml`

- [ ] **Step 1: Update `config-poc.yml`**

Replace the existing `study_panel_map: {}` block with:

```yaml
# t070: per-sample panel resolution for MSK studies. After t070 lands,
# study_panel_map is a fallback for studies WITHOUT a per-sample matrix file;
# the primary source of truth is data_gene_panel_matrix.txt (ingested by
# convert_to_feather for studies in panel_bearing_studies).
panel_bearing_studies:
  - msk_impact_2017
study_panel_map: {}
```

- [ ] **Step 2: Add empty `panel_bearing_studies` to other configs**

In `config-10k-genes.yml`, `config-pan-cancer.yml`, `config-full.yml`, add (just above `study_panel_map`):

```yaml
panel_bearing_studies: []
```

For `config-full.yml`, populate with the MSK studies that are in the active `studies:` list (`msk_chord_2024`, `msk_impact_50k_2026`, `msk_impact_2017`).

For `config-pan-cancer.yml`, populate with `msk_met_2021`.

- [ ] **Step 3: Quick sanity-check — re-run convert_to_feather for msk_impact_2017**

```bash
uv run snakemake -s code/workflows/Snakefile -j1 --configfile code/config/config-poc.yml \
  /data/packages/cbioportal/poc-2026-04-17/studies/msk_impact_2017/metadata/samples.feather \
  --forceall
```

```bash
uv run python -c "
import pandas as pd
df = pd.read_feather('/data/packages/cbioportal/poc-2026-04-17/studies/msk_impact_2017/metadata/samples.feather')
print(df['panel_id'].value_counts(dropna=False))
"
```

Expected: ~2,800 `MSK-IMPACT-341` + ~8,100 `MSK-IMPACT-410`. Matches Problem Statement audit table.

- [ ] **Step 4: Commit**

```bash
git add code/config/config-poc.yml code/config/config-10k-genes.yml code/config/config-pan-cancer.yml code/config/config-full.yml
git commit -m "t070: configs — panel_bearing_studies for MSK studies"
```

---

## Task 10: Validation deliverable — PoC pre/post comparison

**Files:**
- Create: `doc/interpretations/<implementation-date>-t070-poc-comparison.md`

This task quantifies the bias the design was meant to fix. It is the scientific deliverable that justifies the work.

- [ ] **Step 1: Capture the pre-t070 baseline**

Before re-running the PoC, snapshot the current outputs:

```bash
mkdir -p /tmp/t070-baseline
cp /data/packages/cbioportal/poc-2026-04-17/summary/mut/table/gene_cancer_study_ratio_annotated.feather /tmp/t070-baseline/
cp /data/packages/cbioportal/poc-2026-04-17/metadata/samples_tmb_combined.feather /tmp/t070-baseline/
cp /data/packages/cbioportal/poc-2026-04-17/metadata/samples_annotated.feather /tmp/t070-baseline/
```

(Alternative: pull the same files from a `git stash`-ed pre-t070 commit if they're in version control or a labeled run directory exists.)

- [ ] **Step 2: Re-run the PoC end-to-end**

```bash
uv run snakemake -s code/workflows/Snakefile -j1 --configfile code/config/config-poc.yml --forceall
```

- [ ] **Step 3: Generate the comparison report (marimo notebook)**

Write a marimo notebook at `code/notebooks/t070_poc_comparison.py` that:

1. Loads baseline + post outputs for the 3 axes (frequency rates, TMB, hypermutator flags).
2. Computes:
   - Top-20 gene rate deltas for `msk_impact_2017`, broken out by (cancer-type, gene).
   - Per-`panel_id`-stratified TMB histograms (pre vs post).
   - `is_hypermutator` flip counts and `hypermutator_reason` transition matrix.
3. Renders altair charts for each axis.
4. Exports markdown summary to `doc/interpretations/<implementation-date>-t070-poc-comparison.md`.

Notebook skeleton:

```python
# code/notebooks/t070_poc_comparison.py
import marimo as mo
import polars as pl
import altair as alt

baseline_dir = "/tmp/t070-baseline"
post_dir = "/data/packages/cbioportal/poc-2026-04-17"

# ---- Axis 1: frequency rates ----
pre_ratio = pl.read_ipc(f"{baseline_dir}/gene_cancer_study_ratio_annotated.feather")
post_ratio = pl.read_ipc(f"{post_dir}/summary/mut/table/gene_cancer_study_ratio_annotated.feather")
# Compare msk_impact_2017 column pre vs post; rank top-20 absolute deltas.

# ---- Axis 2: TMB ----
pre_tmb = pl.read_ipc(f"{baseline_dir}/samples_tmb_combined.feather")
post_tmb = pl.read_ipc(f"{post_dir}/metadata/samples_tmb_combined.feather")
# Filter to msk_impact_2017 samples; histogram tmb stratified by panel_id.

# ---- Axis 3: hypermutator flag transitions ----
pre_hm = pl.read_ipc(f"{baseline_dir}/samples_annotated.feather")
post_hm = pl.read_ipc(f"{post_dir}/metadata/samples_annotated.feather")
# Inner-join on sample_id; crosstab pre vs post is_hypermutator + reason.
```

- [ ] **Step 4: Write the interpretation document**

Create `doc/interpretations/<implementation-date>-t070-poc-comparison.md` with these sections:

1. **Summary** — one paragraph: what changed quantitatively, what bias was eliminated.
2. **Frequency rates** — table of top-20 affected (cancer, gene) cells with pre/post rates and % delta. Highlight any rows where the rate changed sign of clinical significance (e.g., crossed a 5% threshold).
3. **TMB distributions** — pre/post histograms stratified by `panel_id`. Cite the expected ~25–30× downward shift.
4. **Hypermutator flag transitions** — count of flips. List the most common `hypermutator_reason` transitions (e.g., `gmm_upper_mode → tmb_unavailable`).
5. **Caveats / limitations** — note that PoC is single-MSK-study; cross-study (`msk_met_2021`, `msk_chord_2024`) effects will be measured in a follow-on full-config run.

- [ ] **Step 5: Commit**

```bash
git add doc/interpretations/*-t070-poc-comparison.md code/notebooks/t070_poc_comparison.py
git commit -m "t070: validation — PoC pre/post comparison on msk_impact_2017"
```

- [ ] **Step 6: Mark t070 done in the task backlog**

The project uses `science:tasks` for task management. Use it to close t070:

```bash
uv run science tasks complete t070
```

If the science-tool isn't available or the command shape differs, edit `tasks/active.md` directly: locate the `## [t070]` block (line ~76), remove it, and append it to the appropriate file under `tasks/done/` (filename pattern: inspect `ls tasks/done/`). Then:

```bash
git add tasks/active.md tasks/done/
git commit -m "tasks: close t070 — MSK-IMPACT panel-version drift"
```

---

## Final verification

- [ ] **Run the full test suite**

```bash
uv run --frozen pytest code/scripts/tests/ -v
```

Expected: all green.

- [ ] **Lint the workflow**

```bash
uv run snakemake --lint -s code/workflows/Snakefile --configfile code/config/config-10k-genes.yml
uv run snakemake --lint -s code/workflows/Snakefile --configfile code/config/config-poc.yml
```

- [ ] **Lint + format check the codebase**

```bash
uv run --frozen ruff check code/
uv run --frozen ruff format --check code/
```

- [ ] **Confirm the validation deliverable is on disk**

```bash
ls doc/interpretations/*t070*
```

If everything green, t070 is complete.
