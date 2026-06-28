# t111 — Normal-tissue spectra extraction — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `code/scripts/extract_normal_tissue_spectra.py` + Snakemake rule that emit two reference tables (`data/normal_tissue_spectra.tsv`, `data/normal_tissue_burden.tsv`) from Li2021 + Xu2025 per-variant supplementary data, gating `question:0007-cross-tissue-somatic-mutation-rate-variation-as-null-model` / `question:0008-signature-decomposition-tissue-background-subtraction` / `question:0010-cuplr-style-tof-classifier-for-suspect-normal-samples`.

**Architecture:** Single script decomposed into small testable functions (validator → filter → UBERON join → assay-metadata join → SigProfiler 96-context counts → aggregation → TSV writers). Follows the `process_bailey2018_drivers` pattern: `snakemake` object drives IO, functions are factored out for testability. Two-tier test suite: pure aggregation/validation tests (always run) plus one slow-marked integration test that exercises the real SigProfilerMatrixGenerator trinucleotide lookup.

**Tech Stack:** Python 3.13+, pandas, pyarrow, SigProfilerMatrixGenerator, pytest (pure + slow markers), uv, Snakemake 9.

**Design spec:** `doc/plans/2026-04-18-t111-normal-tissue-spectra-design.md`

---

## Scope amendment (post-Task 0, 2026-04-19)

Task 0 resolved to Li2021 = Branch A, Xu2025 = Branch B (dbGaP controlled-access).
User approved option (a): **reduce scope to Li2021 only**; Xu2025 and Lee-Six2018 deferred to follow-up task(s).

**Effect on the rest of the plan:**
- Task 2: UBERON mapping covers the 9 Li2021 organs only.
- Task 5: `ASSAY_METADATA` holds Li2021 entries only; skip the Xu2025 confirmation step.
- Task 13: `main()` processes one source (Li2021); `_SOURCE_ASSEMBLY` maps only `li2021 → GRCh37`; snakemake input lacks `xu2025`.
- Task 14: fixtures and slow integration test cover Li2021 only.
- Task 15: Snakemake rule has `li2021` as the single variant-data input.
- Task 16: stages only `data/li2021_somatic_mutations.tsv`. **New staging step**: Li2021 supplement is an XLSX (`41586_2021_3836_MOESM5_ESM.xlsx`); convert XLSX → TSV with a sampleID → (donor_id, tissue_label, sample_id) parser — see Task 16 Step 1 notes below.

The gate record is at `doc/plans/t111-data-gate-record.md` (commit `446f953`).

---

## Task 0: Data-access gate (pre-implementation verification)

This is the design's Branch-A/Branch-B gate. It MUST run before any code is written. If Branch B fires, STOP and raise to the user — scope changes materially.

**Files:**
- Touch: none yet
- Output: a short note in the conversation (Branch A confirmed ⇒ proceed; Branch B ⇒ halt)

- [ ] **Step 1: Verify Li2021 per-variant calls are publicly accessible**

Check, in order: Nature Supplementary Information for DOI `10.1038/s41586-021-03836-1`, bioRxiv supplement for `10.1101/2020.11.30.403436`, and any Zenodo/FigShare mirror. Look for a file containing per-variant rows with at least `donor_id, tissue_label, chrom, pos, ref, alt` (or equivalent columns; MAF-style fields are acceptable).

Record the URL, filename, retrieval date, and file SHA256 for later use in the provenance doc.

- [ ] **Step 2: Verify Xu2025 per-variant calls are publicly accessible**

Check bioRxiv supplement for `10.1101/2025.01.07.631808`. PMC mirror (PMC11741334) may also carry supplementary data. Same required columns as Li2021.

Record URL, filename, retrieval date, SHA256.

- [ ] **Step 3: Branch decision**

If both sources accessible: proceed to Task 1.

If either source is EGA/GSA controlled-access only: halt. Report to user with this exact message pattern:
> "Data-access gate: <source> is <EGA-only / GSA-only / otherwise gated>. Scope changes materially (DUA, reprocessing). Per design §Data-access gate, halting for user decision — options are (a) reduce scope to the accessible source and defer the other to a follow-up task, or (b) expand t111 to cover controlled-access acquisition."

Do NOT continue to Task 1 without explicit user approval.

- [ ] **Step 4: Record the gate outcome**

Add the Branch-A retrieval details (two URLs + SHA256s + retrieval date) to a scratch file at `doc/plans/t111-data-gate-record.md` for later use in Task 16 (provenance doc). The file is committed to git so the gate outcome is auditable.

```bash
git add doc/plans/t111-data-gate-record.md
git commit -m "$(cat <<'EOF'
doc: t111 data-access gate record (Branch A)

Li2021 source: <URL> SHA256:<hash> retrieved:<date>
Xu2025 source: <URL> SHA256:<hash> retrieved:<date>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 1: Dependency + pytest marker + skeleton script

**Files:**
- Modify: `pyproject.toml`
- Create: `code/scripts/extract_normal_tissue_spectra.py`
- Create: `code/scripts/tests/test_extract_normal_tissue_spectra.py` (empty placeholder for now)

- [ ] **Step 1: Add SigProfilerMatrixGenerator as a project dependency**

Run from repo root:
```bash
uv add sigprofilermatrixgenerator
```

Expected: `pyproject.toml` gains `sigprofilermatrixgenerator>=1.2` (or similar) under `[project.dependencies]`; `uv.lock` updates.

- [ ] **Step 2: Add `slow` pytest marker to pyproject.toml**

Append this block to `pyproject.toml`:

```toml
[tool.pytest.ini_options]
markers = [
    "slow: integration tests that download reference data or touch external tools",
]
```

- [ ] **Step 3: Create the script skeleton with docstring and snakemake-object wiring**

Create `code/scripts/extract_normal_tissue_spectra.py`:

```python
"""
extract_normal_tissue_spectra.py

Builds two reference tables from Li 2021 + Xu 2025 per-variant supplementary data:

- `data/normal_tissue_spectra.tsv` — 96-trinucleotide SBS spectra per normal tissue
  (three aggregations: pooled_counts, donor_averaged_fraction, per_donor)
- `data/normal_tissue_burden.tsv` — per-tissue / per-donor mutation burden with
  callable-Mb denominator and sequencing-modality metadata

Rows are keyed on UBERON ontology IDs; source tissue labels are preserved for audit.

Design: doc/plans/2026-04-18-t111-normal-tissue-spectra-design.md
Plan:   doc/plans/2026-04-18-t111-normal-tissue-spectra-plan.md
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

# Assay metadata constants. Sourced from each paper's Methods section.
# Li 2021 Nature Methods: SureSelectXT Human All Exon V6 (esophagus) or V7 (other tissues),
# callable target ~60 Mb (Agilent published spec).
# Xu 2025 bioRxiv Methods: <confirmed during Task 6>.
ASSAY_METADATA: dict[tuple[str, str | None], dict[str, object]] = {
    # Populated in Task 6.
}


def main() -> None:
    """Snakemake entry point. Not invoked directly — use `snakemake` CLI."""
    snek = snakemake  # type: ignore[name-defined]
    # Wired up in Task 13.
    raise NotImplementedError("Wired up in Task 13")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Create the test-file placeholder**

Create `code/scripts/tests/test_extract_normal_tissue_spectra.py`:

```python
"""Tests for extract_normal_tissue_spectra.

See plan Task 3 onward for detailed test specifications.
"""
```

- [ ] **Step 5: Verify the baseline tests still pass**

Run:
```bash
uv run --frozen pytest code/scripts/tests/ -q
```

Expected: all existing tests pass (we have not yet added new tests).

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml uv.lock code/scripts/extract_normal_tissue_spectra.py code/scripts/tests/test_extract_normal_tissue_spectra.py
git commit -m "$(cat <<'EOF'
t111: add SigProfiler dep, slow pytest marker, script + test skeleton

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: Hand-curate UBERON mapping

**Files:**
- Create: `data/tissue_uberon_mapping.tsv`

- [ ] **Step 1: Enumerate unique tissue labels across both sources**

From Li 2021 (9 organs, preprint PDF already read in earlier session): `Bronchia, Esophagus, Cardia, Stomach, Duodenum, Colon, Rectum, Liver, Pancreas`.

From Xu 2025 (46 tissues — exact list comes from the supplementary data inspected in Task 0 Step 2). Expected GTEx-derived tissue labels include `Adipose - Subcutaneous, Artery - Aorta, Brain - Cerebellum, Heart - Left Ventricle, Lung, Muscle - Skeletal, Nerve - Tibial, Skin - Sun Exposed (Lower leg), Thyroid, Whole Blood`, etc. Record the exact labels encountered.

- [ ] **Step 2: Resolve each unique `(source, tissue_label)` to a UBERON ID via EBI OLS**

For each unique tissue_label, query `https://www.ebi.ac.uk/ols4/api/search?q=<label>&ontology=uberon` (via WebFetch). Pick the most specific anatomical term. Examples:

| source | tissue_label | tissue_uberon | uberon_label |
|---|---|---|---|
| li2021 | Bronchia | UBERON:0002185 | bronchus |
| li2021 | Esophagus | UBERON:0001043 | esophagus |
| li2021 | Cardia | UBERON:0007650 | gastric cardia |
| li2021 | Stomach | UBERON:0000945 | stomach |
| li2021 | Duodenum | UBERON:0002114 | duodenum |
| li2021 | Colon | UBERON:0001155 | colon |
| li2021 | Rectum | UBERON:0001052 | rectum |
| li2021 | Liver | UBERON:0002107 | liver |
| li2021 | Pancreas | UBERON:0001264 | pancreas |

For GTEx composite labels that don't map 1:1 (e.g., "Skin - Sun Exposed (Lower leg)"), pick the most anatomically specific term available and record the judgment call in the `notes` column.

- [ ] **Step 3: Write `data/tissue_uberon_mapping.tsv`**

Schema: `source<TAB>tissue_label<TAB>tissue_uberon<TAB>uberon_label<TAB>notes`

Required: header row + one row per unique `(source, tissue_label)` encountered in Step 1. Include all 9 Li2021 tissues above and all ~46 Xu2025 tissues observed in the supplementary data.

Example:
```
source	tissue_label	tissue_uberon	uberon_label	notes
li2021	Bronchia	UBERON:0002185	bronchus	li2021 "Bronchia" → primary bronchus
li2021	Esophagus	UBERON:0001043	esophagus	
...
```

- [ ] **Step 4: Commit**

Count the populated rows for the commit message body:
```bash
N=$(($(wc -l < data/tissue_uberon_mapping.tsv) - 1))
git add data/tissue_uberon_mapping.tsv
git commit -m "$(cat <<EOF
t111: hand-curated UBERON mapping for Li2021 + Xu2025 tissues

${N} unique (source, tissue_label) pairs mapped via EBI OLS. GTEx composite
labels mapped to the most specific anatomical term with judgment notes.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: Input contract validator

**Files:**
- Modify: `code/scripts/extract_normal_tissue_spectra.py`
- Modify: `code/scripts/tests/test_extract_normal_tissue_spectra.py`

- [ ] **Step 1: Write failing tests for each contract rule**

Append to `code/scripts/tests/test_extract_normal_tissue_spectra.py`:

```python
import pandas as pd
import pytest

from extract_normal_tissue_spectra import validate_input_contract


def _df(**cols: list) -> pd.DataFrame:
    return pd.DataFrame(cols)


def test_contract_rejects_multiallelic_alt() -> None:
    df = _df(
        donor_id=["D1"], tissue_label=["Liver"],
        chrom=["chr1"], pos=[1000], ref=["A"], alt=["C,T"],
    )
    with pytest.raises(ValueError, match="multi-allelic"):
        validate_input_contract(df, source="li2021", assembly="GRCh37")


def test_contract_drops_indel_rows_and_reports_count() -> None:
    df = _df(
        donor_id=["D1", "D1"], tissue_label=["Liver", "Liver"],
        chrom=["chr1", "chr1"], pos=[1000, 2000],
        ref=["A", "AG"], alt=["C", "A"],  # second row is an indel (ref length 2)
    )
    cleaned, stats = validate_input_contract(df, source="li2021", assembly="GRCh37")
    assert len(cleaned) == 1
    assert stats["n_indels_dropped"] == 1
    assert cleaned.iloc[0]["ref"] == "A"


def test_contract_rejects_non_acgt_alleles() -> None:
    df = _df(
        donor_id=["D1"], tissue_label=["Liver"],
        chrom=["chr1"], pos=[1000], ref=["A"], alt=["N"],
    )
    with pytest.raises(ValueError, match="non-ACGT"):
        validate_input_contract(df, source="li2021", assembly="GRCh37")


def test_contract_drops_mitochondrial_rows() -> None:
    df = _df(
        donor_id=["D1", "D1"], tissue_label=["Liver", "Liver"],
        chrom=["chr1", "chrM"], pos=[1000, 500],
        ref=["A", "C"], alt=["C", "T"],
    )
    cleaned, stats = validate_input_contract(df, source="li2021", assembly="GRCh37")
    assert len(cleaned) == 1
    assert stats["n_mito_dropped"] == 1
    assert cleaned.iloc[0]["chrom"] == "chr1"


def test_contract_dedups_exact_duplicates() -> None:
    df = _df(
        donor_id=["D1", "D1"], tissue_label=["Liver", "Liver"],
        chrom=["chr1", "chr1"], pos=[1000, 1000],
        ref=["A", "A"], alt=["C", "C"],
    )
    cleaned, stats = validate_input_contract(df, source="li2021", assembly="GRCh37")
    assert len(cleaned) == 1
    assert stats["n_duplicates_collapsed"] == 1


def test_contract_keeps_cross_donor_duplicates() -> None:
    df = _df(
        donor_id=["D1", "D2"], tissue_label=["Liver", "Liver"],
        chrom=["chr1", "chr1"], pos=[1000, 1000],
        ref=["A", "A"], alt=["C", "C"],
    )
    cleaned, stats = validate_input_contract(df, source="li2021", assembly="GRCh37")
    assert len(cleaned) == 2
    assert stats["n_duplicates_collapsed"] == 0


def test_contract_normalises_chrom_prefix() -> None:
    # Input without chr prefix should be normalised to chrN
    df = _df(
        donor_id=["D1"], tissue_label=["Liver"],
        chrom=["1"], pos=[1000], ref=["A"], alt=["C"],
    )
    cleaned, stats = validate_input_contract(df, source="li2021", assembly="GRCh37")
    assert cleaned.iloc[0]["chrom"] == "chr1"


def test_contract_rejects_invalid_chromosome() -> None:
    df = _df(
        donor_id=["D1"], tissue_label=["Liver"],
        chrom=["chrZ"], pos=[1000], ref=["A"], alt=["C"],
    )
    with pytest.raises(ValueError, match="unknown chromosome"):
        validate_input_contract(df, source="li2021", assembly="GRCh37")
```

- [ ] **Step 2: Run tests to verify they fail**

Run:
```bash
uv run --frozen pytest code/scripts/tests/test_extract_normal_tissue_spectra.py -v
```

Expected: all 8 new tests FAIL with `ImportError` / `AttributeError` for `validate_input_contract`.

- [ ] **Step 3: Implement `validate_input_contract`**

Add to `code/scripts/extract_normal_tissue_spectra.py` (above `main`):

```python
_VALID_CHROMS = {f"chr{c}" for c in list(range(1, 23)) + ["X", "Y"]}


def validate_input_contract(
    df: pd.DataFrame, source: str, assembly: str
) -> tuple[pd.DataFrame, dict[str, int]]:
    """Enforce the input contract defined in the design spec.

    Drops (with counters): indels, mitochondrial rows, exact within-donor duplicates.
    Raises ValueError for: multi-allelic rows, non-ACGT alleles, unknown chromosomes.
    Normalises `chrom` to the `chrN` form.

    Returns (cleaned_df, stats_dict) where stats_dict has keys:
    n_indels_dropped, n_mito_dropped, n_duplicates_collapsed.
    """
    required = {"donor_id", "tissue_label", "chrom", "pos", "ref", "alt"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{source}: missing required columns {sorted(missing)}")

    df = df.copy()
    df["chrom"] = df["chrom"].astype(str).apply(lambda c: c if c.startswith("chr") else f"chr{c}")
    df["ref"] = df["ref"].astype(str)
    df["alt"] = df["alt"].astype(str)

    if df["alt"].str.contains(",").any():
        bad = int(df["alt"].str.contains(",").sum())
        raise ValueError(f"{source}: {bad} multi-allelic rows (alt contains ','); split upstream")

    # Mitochondrial drop
    mito_mask = df["chrom"].isin({"chrM", "chrMT"})
    n_mito = int(mito_mask.sum())
    df = df.loc[~mito_mask].copy()

    # Unknown chromosomes
    unknown = set(df["chrom"].unique()) - _VALID_CHROMS
    if unknown:
        raise ValueError(f"{source}: unknown chromosome values {sorted(unknown)}")

    # Indel drop (ref or alt not length-1)
    indel_mask = (df["ref"].str.len() != 1) | (df["alt"].str.len() != 1)
    n_indels = int(indel_mask.sum())
    df = df.loc[~indel_mask].copy()

    # Non-ACGT rejection
    valid = {"A", "C", "G", "T"}
    bad_alleles = ~(df["ref"].isin(valid) & df["alt"].isin(valid))
    if bad_alleles.any():
        raise ValueError(
            f"{source}: {int(bad_alleles.sum())} rows with non-ACGT alleles"
        )

    # Exact-duplicate dedup (within donor + tissue)
    before = len(df)
    df = df.drop_duplicates(subset=["donor_id", "tissue_label", "chrom", "pos", "ref", "alt"])
    n_dupes = before - len(df)

    return df.reset_index(drop=True), {
        "n_indels_dropped": n_indels,
        "n_mito_dropped": n_mito,
        "n_duplicates_collapsed": n_dupes,
    }
```

- [ ] **Step 4: Run tests to verify they pass**

Run:
```bash
uv run --frozen pytest code/scripts/tests/test_extract_normal_tissue_spectra.py -v
```

Expected: all 8 contract tests PASS.

- [ ] **Step 5: Commit**

```bash
git add code/scripts/extract_normal_tissue_spectra.py code/scripts/tests/test_extract_normal_tissue_spectra.py
git commit -m "$(cat <<'EOF'
t111: input contract validator + tests

Drops indels / mitochondrial / duplicates with counters; raises for
multi-allelic / non-ACGT / unknown-chromosome rows. 8 pure unit tests.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: UBERON mapping attachment

**Files:**
- Modify: `code/scripts/extract_normal_tissue_spectra.py`
- Modify: `code/scripts/tests/test_extract_normal_tissue_spectra.py`

- [ ] **Step 1: Write failing tests**

Append to the test file:

```python
from pathlib import Path

from extract_normal_tissue_spectra import attach_uberon


def _mapping_tsv(tmp_path: Path) -> Path:
    p = tmp_path / "map.tsv"
    p.write_text(
        "source\ttissue_label\ttissue_uberon\tuberon_label\tnotes\n"
        "li2021\tLiver\tUBERON:0002107\tliver\t\n"
        "li2021\tEsophagus\tUBERON:0001043\tesophagus\t\n"
    )
    return p


def test_attach_uberon_joins_on_source_and_tissue_label(tmp_path: Path) -> None:
    df = _df(
        donor_id=["D1", "D1"], tissue_label=["Liver", "Esophagus"],
        chrom=["chr1", "chr1"], pos=[1, 2], ref=["A", "A"], alt=["C", "C"],
    )
    out = attach_uberon(df, _mapping_tsv(tmp_path), source="li2021")
    assert list(out["tissue_uberon"]) == ["UBERON:0002107", "UBERON:0001043"]
    assert list(out["uberon_label"]) == ["liver", "esophagus"]


def test_attach_uberon_raises_on_unmapped_tissue(tmp_path: Path) -> None:
    df = _df(
        donor_id=["D1"], tissue_label=["Pancreas"],
        chrom=["chr1"], pos=[1], ref=["A"], alt=["C"],
    )
    with pytest.raises(ValueError, match="unmapped"):
        attach_uberon(df, _mapping_tsv(tmp_path), source="li2021")
```

- [ ] **Step 2: Run tests to verify they fail**

Run:
```bash
uv run --frozen pytest code/scripts/tests/test_extract_normal_tissue_spectra.py::test_attach_uberon_joins_on_source_and_tissue_label code/scripts/tests/test_extract_normal_tissue_spectra.py::test_attach_uberon_raises_on_unmapped_tissue -v
```

Expected: FAIL with `ImportError: cannot import name 'attach_uberon'`.

- [ ] **Step 3: Implement `attach_uberon`**

Add to `code/scripts/extract_normal_tissue_spectra.py`:

```python
def attach_uberon(df: pd.DataFrame, mapping_tsv: Path, source: str) -> pd.DataFrame:
    """Left-join `tissue_uberon` and `uberon_label` onto df keyed on (source, tissue_label).

    Raises ValueError listing any unmapped (source, tissue_label) pairs — no silent drops.
    """
    mapping = pd.read_csv(mapping_tsv, sep="\t", dtype=str, na_filter=False)
    mapping = mapping.loc[mapping["source"] == source, ["tissue_label", "tissue_uberon", "uberon_label"]]

    out = df.merge(mapping, on="tissue_label", how="left", validate="many_to_one")
    unmapped = out.loc[out["tissue_uberon"].isna(), "tissue_label"].unique().tolist()
    if unmapped:
        raise ValueError(
            f"{source}: unmapped tissue_label values {sorted(unmapped)}. "
            f"Append to {mapping_tsv}."
        )
    return out
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
uv run --frozen pytest code/scripts/tests/test_extract_normal_tissue_spectra.py -v
```

Expected: all tests PASS.

- [ ] **Step 5: Commit**

```bash
git add code/scripts/extract_normal_tissue_spectra.py code/scripts/tests/test_extract_normal_tissue_spectra.py
git commit -m "$(cat <<'EOF'
t111: UBERON mapping attachment + tests

attach_uberon joins on (source, tissue_label); raises on unmapped rows.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 5: Assay-metadata attachment

**Files:**
- Modify: `code/scripts/extract_normal_tissue_spectra.py`
- Modify: `code/scripts/tests/test_extract_normal_tissue_spectra.py`

- [ ] **Step 1: Confirm Xu2025 Methods section — capture kit + callable_mb**

Read Xu2025 bioRxiv preprint Methods section (DOI 10.1101/2025.01.07.631808) — confirm: sequencing modality (WES? WGS?), capture kit (if WES), approximate callable Mb. If not spelled out, default to WES + "Unknown" kit + 60 Mb with a note in the provenance doc.

Record the exact values to use.

- [ ] **Step 2: Populate `ASSAY_METADATA` dict in the script**

Replace the `ASSAY_METADATA = {}` stub in `code/scripts/extract_normal_tissue_spectra.py` with:

```python
# Assay metadata constants. Sourced from each paper's Methods section.
#
# Li 2021 Nature Methods: SureSelectXT Human All Exon V6 (esophagus biopsies only)
# or V7 (all other tissues). Agilent-published callable targets: V6 ~60 Mb, V7 ~48.2 Mb.
# Xu 2025 Methods: <values confirmed in Task 5 Step 1>
ASSAY_METADATA: dict[tuple[str, str | None], dict[str, object]] = {
    ("li2021", "Esophagus"): {"sequencing_modality": "WES", "capture_kit_or_panel": "SureSelectXT V6", "callable_mb": 60.0},
    ("li2021", None): {"sequencing_modality": "WES", "capture_kit_or_panel": "SureSelectXT V7", "callable_mb": 48.2},
    ("xu2025", None): {"sequencing_modality": "WES", "capture_kit_or_panel": "<confirmed in step 1>", "callable_mb": 60.0},
}
```

The `(source, None)` tuple is the fallback for the source when a specific tissue_label is not keyed explicitly.

- [ ] **Step 3: Write failing tests**

Append to the test file:

```python
from extract_normal_tissue_spectra import attach_assay_metadata


def test_attach_assay_metadata_li2021_esophagus_gets_v6() -> None:
    df = _df(
        donor_id=["D1"], tissue_label=["Esophagus"],
        chrom=["chr1"], pos=[1], ref=["A"], alt=["C"],
    )
    out = attach_assay_metadata(df, source="li2021")
    row = out.iloc[0]
    assert row["sequencing_modality"] == "WES"
    assert row["capture_kit_or_panel"] == "SureSelectXT V6"
    assert row["callable_mb"] == 60.0


def test_attach_assay_metadata_li2021_nonesophagus_gets_v7() -> None:
    df = _df(
        donor_id=["D1"], tissue_label=["Liver"],
        chrom=["chr1"], pos=[1], ref=["A"], alt=["C"],
    )
    out = attach_assay_metadata(df, source="li2021")
    row = out.iloc[0]
    assert row["capture_kit_or_panel"] == "SureSelectXT V7"
    assert row["callable_mb"] == 48.2


def test_attach_assay_metadata_missing_source_raises() -> None:
    df = _df(
        donor_id=["D1"], tissue_label=["Liver"],
        chrom=["chr1"], pos=[1], ref=["A"], alt=["C"],
    )
    with pytest.raises(KeyError, match="nonexistent"):
        attach_assay_metadata(df, source="nonexistent")
```

- [ ] **Step 4: Run tests to verify they fail**

Run:
```bash
uv run --frozen pytest code/scripts/tests/test_extract_normal_tissue_spectra.py -k assay -v
```

Expected: FAIL with `ImportError: cannot import name 'attach_assay_metadata'`.

- [ ] **Step 5: Implement `attach_assay_metadata`**

Add to `code/scripts/extract_normal_tissue_spectra.py`:

```python
def attach_assay_metadata(df: pd.DataFrame, source: str) -> pd.DataFrame:
    """Attach sequencing_modality / capture_kit_or_panel / callable_mb columns keyed by
    (source, tissue_label) with (source, None) as the per-source fallback.

    Raises KeyError if source is unknown to ASSAY_METADATA.
    """
    source_keys = [k for k in ASSAY_METADATA if k[0] == source]
    if not source_keys:
        raise KeyError(f"ASSAY_METADATA has no entry for source={source!r}")

    def _lookup(tissue_label: str) -> dict[str, object]:
        if (source, tissue_label) in ASSAY_METADATA:
            return ASSAY_METADATA[(source, tissue_label)]
        if (source, None) in ASSAY_METADATA:
            return ASSAY_METADATA[(source, None)]
        raise KeyError(f"ASSAY_METADATA: no entry for ({source!r}, {tissue_label!r})")

    meta = df["tissue_label"].apply(_lookup).tolist()
    out = df.copy()
    out["sequencing_modality"] = [m["sequencing_modality"] for m in meta]
    out["capture_kit_or_panel"] = [m["capture_kit_or_panel"] for m in meta]
    out["callable_mb"] = [float(m["callable_mb"]) for m in meta]
    return out
```

- [ ] **Step 6: Run tests to verify they pass**

```bash
uv run --frozen pytest code/scripts/tests/test_extract_normal_tissue_spectra.py -v
```

Expected: all tests PASS.

- [ ] **Step 7: Commit**

```bash
git add code/scripts/extract_normal_tissue_spectra.py code/scripts/tests/test_extract_normal_tissue_spectra.py
git commit -m "$(cat <<'EOF'
t111: assay-metadata attachment + tests

Per-(source, tissue_label) lookup with (source, None) fallback. Li2021
esophagus gets V6 kit, other tissues V7. Xu2025 from paper Methods.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 6: Pooled counts aggregation

**Files:**
- Modify: `code/scripts/extract_normal_tissue_spectra.py`
- Modify: `code/scripts/tests/test_extract_normal_tissue_spectra.py`

- [ ] **Step 1: Write failing test**

Append to the test file:

```python
from extract_normal_tissue_spectra import CONTEXT_96, aggregate_pooled_counts


def _synthetic_context_df(donor_counts: dict[str, dict[str, int]]) -> pd.DataFrame:
    """Build a per-donor 96-context count DataFrame from a nested dict.

    donor_counts: {donor_id: {context: count, ...}}
    Contexts not listed default to 0.
    """
    rows = []
    for donor, ctx_counts in donor_counts.items():
        row = {ctx: 0 for ctx in CONTEXT_96}
        row.update(ctx_counts)
        row["donor_id"] = donor
        rows.append(row)
    return pd.DataFrame(rows)


def test_pooled_counts_is_column_wise_sum_across_donors() -> None:
    per_donor = _synthetic_context_df({
        "D1": {"A[C>A]A": 3, "T[T>G]T": 2},
        "D2": {"A[C>A]A": 1, "T[T>G]T": 7},
        "D3": {"A[C>A]A": 5},
    })
    row = aggregate_pooled_counts(per_donor)
    assert row["A[C>A]A"] == 9
    assert row["T[T>G]T"] == 9
    assert row["total_snvs"] == 18
    assert row["n_donors"] == 3
```

- [ ] **Step 2: Run test to verify it fails**

```bash
uv run --frozen pytest code/scripts/tests/test_extract_normal_tissue_spectra.py -k pooled_counts -v
```

Expected: FAIL — `CONTEXT_96` and `aggregate_pooled_counts` not defined.

- [ ] **Step 3: Implement CONTEXT_96 constant and aggregate_pooled_counts**

Add near the top of `code/scripts/extract_normal_tissue_spectra.py` (below `ASSAY_METADATA`):

```python
# SigProfiler's canonical 96-trinucleotide context ordering:
# {5'-base}[{ref}>{alt}]{3'-base}, with {ref, alt} restricted to pyrimidine-centric changes
# (C>A, C>G, C>T, T>A, T>C, T>G).
_SUBS = ["C>A", "C>G", "C>T", "T>A", "T>C", "T>G"]
_BASES = ["A", "C", "G", "T"]
CONTEXT_96: list[str] = [
    f"{five}[{sub}]{three}" for five in _BASES for sub in _SUBS for three in _BASES
]
assert len(CONTEXT_96) == 96


def aggregate_pooled_counts(per_donor_ctx: pd.DataFrame) -> dict[str, object]:
    """Column-wise sum of per-donor 96-context counts → single pooled row.

    Input: per-donor DataFrame with 96 context columns + 'donor_id'.
    Output: dict with 96 context columns (int), 'total_snvs' (int), 'n_donors' (int).
    """
    totals = {ctx: int(per_donor_ctx[ctx].sum()) for ctx in CONTEXT_96}
    totals["total_snvs"] = sum(totals[ctx] for ctx in CONTEXT_96)
    totals["n_donors"] = int(per_donor_ctx["donor_id"].nunique())
    return totals
```

- [ ] **Step 4: Run test to verify it passes**

```bash
uv run --frozen pytest code/scripts/tests/test_extract_normal_tissue_spectra.py -k pooled_counts -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add code/scripts/extract_normal_tissue_spectra.py code/scripts/tests/test_extract_normal_tissue_spectra.py
git commit -m "$(cat <<'EOF'
t111: pooled-counts aggregation + CONTEXT_96 constant

Column-wise sum of per-donor 96-context counts into one pooled row.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 7: Donor-averaged fraction aggregation

**Files:**
- Modify: `code/scripts/extract_normal_tissue_spectra.py`
- Modify: `code/scripts/tests/test_extract_normal_tissue_spectra.py`

- [ ] **Step 1: Write failing tests**

Append to the test file:

```python
from extract_normal_tissue_spectra import aggregate_donor_averaged_fraction


def test_donor_averaged_fraction_sums_to_one() -> None:
    per_donor = _synthetic_context_df({
        "D1": {"A[C>A]A": 4, "T[T>G]T": 6},   # 10 total
        "D2": {"A[C>A]A": 8, "T[T>G]T": 2},   # 10 total
    })
    row, audit = aggregate_donor_averaged_fraction(per_donor, threshold=2)
    total = sum(row[ctx] for ctx in CONTEXT_96)
    assert total == pytest.approx(1.0, abs=1e-9)
    # D1 fraction: 0.4/0.6; D2: 0.8/0.2 → averaged: 0.6/0.4
    assert row["A[C>A]A"] == pytest.approx(0.6, abs=1e-9)
    assert row["T[T>G]T"] == pytest.approx(0.4, abs=1e-9)
    assert audit["n_donors_included"] == 2
    assert audit["n_donors_excluded_low_snvs"] == 0


def test_donor_averaged_fraction_excludes_low_snv_donors() -> None:
    per_donor = _synthetic_context_df({
        "D1": {"A[C>A]A": 50, "T[T>G]T": 50},   # 100 total — included
        "D2": {"A[C>A]A": 49},                  # 49 total — excluded at threshold=50
    })
    row, audit = aggregate_donor_averaged_fraction(per_donor, threshold=50)
    assert audit["n_donors_included"] == 1
    assert audit["n_donors_excluded_low_snvs"] == 1
    assert row["A[C>A]A"] == pytest.approx(0.5, abs=1e-9)
    assert row["T[T>G]T"] == pytest.approx(0.5, abs=1e-9)


def test_donor_averaged_fraction_empty_when_all_excluded() -> None:
    per_donor = _synthetic_context_df({
        "D1": {"A[C>A]A": 10},
        "D2": {"T[T>G]T": 5},
    })
    row, audit = aggregate_donor_averaged_fraction(per_donor, threshold=50)
    # With zero donors included, row values should all be 0 and audit counts reflect it
    assert audit["n_donors_included"] == 0
    assert audit["n_donors_excluded_low_snvs"] == 2
    assert sum(row[ctx] for ctx in CONTEXT_96) == 0.0
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run --frozen pytest code/scripts/tests/test_extract_normal_tissue_spectra.py -k donor_averaged -v
```

Expected: FAIL — `aggregate_donor_averaged_fraction` not defined.

- [ ] **Step 3: Implement `aggregate_donor_averaged_fraction`**

Add to `code/scripts/extract_normal_tissue_spectra.py`:

```python
def aggregate_donor_averaged_fraction(
    per_donor_ctx: pd.DataFrame, threshold: int = 50
) -> tuple[dict[str, float], dict[str, int]]:
    """Normalise each donor's 96-vector to a fraction, then average across donors.

    Donors with fewer than `threshold` SNVs are excluded from the average.

    Returns (row_dict, audit_dict). audit_dict has n_donors_total,
    n_donors_included, n_donors_excluded_low_snvs, low_snv_threshold.
    """
    n_total = int(per_donor_ctx["donor_id"].nunique())
    totals = per_donor_ctx[CONTEXT_96].sum(axis=1)
    include_mask = totals >= threshold
    n_incl = int(include_mask.sum())
    n_excl = n_total - n_incl

    audit = {
        "n_donors_total": n_total,
        "n_donors_included": n_incl,
        "n_donors_excluded_low_snvs": n_excl,
        "low_snv_threshold": threshold,
    }

    if n_incl == 0:
        return {ctx: 0.0 for ctx in CONTEXT_96}, audit

    included = per_donor_ctx.loc[include_mask, CONTEXT_96]
    totals_incl = included.sum(axis=1).to_numpy()
    fractions = included.to_numpy() / totals_incl[:, None]
    averaged = fractions.mean(axis=0)

    # Re-normalize to guard against rounding drift
    averaged = averaged / averaged.sum()

    return {ctx: float(averaged[i]) for i, ctx in enumerate(CONTEXT_96)}, audit
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
uv run --frozen pytest code/scripts/tests/test_extract_normal_tissue_spectra.py -v
```

Expected: all tests PASS.

- [ ] **Step 5: Commit**

```bash
git add code/scripts/extract_normal_tissue_spectra.py code/scripts/tests/test_extract_normal_tissue_spectra.py
git commit -m "$(cat <<'EOF'
t111: donor-averaged fraction aggregation + audit fields

Normalise per-donor before averaging, exclude low-SNV donors at threshold,
return audit dict with n_donors_total / _included / _excluded / threshold.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 8: Per-donor rows

**Files:**
- Modify: `code/scripts/extract_normal_tissue_spectra.py`
- Modify: `code/scripts/tests/test_extract_normal_tissue_spectra.py`

- [ ] **Step 1: Write failing test**

Append to the test file:

```python
from extract_normal_tissue_spectra import aggregate_per_donor_rows


def test_per_donor_rows_one_row_per_donor_with_counts() -> None:
    per_donor = _synthetic_context_df({
        "D1": {"A[C>A]A": 3},
        "D2": {"T[T>G]T": 5},
        "D3": {"A[C>A]A": 1, "T[T>G]T": 2},
    })
    rows = aggregate_per_donor_rows(per_donor)
    assert len(rows) == 3
    by_donor = {r["donor_id"]: r for r in rows}
    assert by_donor["D1"]["A[C>A]A"] == 3
    assert by_donor["D1"]["total_snvs"] == 3
    assert by_donor["D2"]["T[T>G]T"] == 5
    assert by_donor["D3"]["total_snvs"] == 3
```

- [ ] **Step 2: Run test to verify it fails**

```bash
uv run --frozen pytest code/scripts/tests/test_extract_normal_tissue_spectra.py -k per_donor_rows -v
```

Expected: FAIL — `aggregate_per_donor_rows` not defined.

- [ ] **Step 3: Implement `aggregate_per_donor_rows`**

Add to `code/scripts/extract_normal_tissue_spectra.py`:

```python
def aggregate_per_donor_rows(per_donor_ctx: pd.DataFrame) -> list[dict[str, object]]:
    """Emit one row per donor, carrying the donor's 96-context counts + total_snvs."""
    rows: list[dict[str, object]] = []
    for _, donor_row in per_donor_ctx.iterrows():
        row: dict[str, object] = {ctx: int(donor_row[ctx]) for ctx in CONTEXT_96}
        row["donor_id"] = str(donor_row["donor_id"])
        row["total_snvs"] = sum(row[ctx] for ctx in CONTEXT_96)
        rows.append(row)
    return rows
```

- [ ] **Step 4: Run test to verify it passes**

```bash
uv run --frozen pytest code/scripts/tests/test_extract_normal_tissue_spectra.py -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add code/scripts/extract_normal_tissue_spectra.py code/scripts/tests/test_extract_normal_tissue_spectra.py
git commit -m "$(cat <<'EOF'
t111: per-donor row emission + tests

One row per donor with raw counts and total_snvs.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 9: Burden math

**Files:**
- Modify: `code/scripts/extract_normal_tissue_spectra.py`
- Modify: `code/scripts/tests/test_extract_normal_tissue_spectra.py`

- [ ] **Step 1: Write failing tests**

Append to the test file:

```python
from extract_normal_tissue_spectra import (
    aggregate_pooled_burden,
    aggregate_per_donor_burden_rows,
)


def _burden_input_df(rows: list[tuple[str, int]]) -> pd.DataFrame:
    """rows: list of (donor_id, n_snvs). Returns a per-variant-style df
    with callable_mb=50.0, n_samples=1 per donor."""
    data = []
    for donor_id, n in rows:
        for i in range(n):
            data.append({
                "donor_id": donor_id,
                "callable_mb": 50.0,
                "sample_id": f"{donor_id}-1",
            })
    return pd.DataFrame(data)


def test_pooled_burden_snvs_per_mb_computation() -> None:
    df = _burden_input_df([("D1", 100), ("D2", 200)])
    row = aggregate_pooled_burden(df)
    assert row["snvs"] == 300
    assert row["n_donors"] == 2
    assert row["n_samples"] == 2  # two distinct sample_ids
    assert row["callable_mb"] == 50.0
    assert row["snvs_per_mb"] == pytest.approx(300.0 / 50.0 / 2, abs=1e-9)


def test_per_donor_burden_one_row_per_donor() -> None:
    df = _burden_input_df([("D1", 100), ("D2", 200)])
    rows = aggregate_per_donor_burden_rows(df)
    assert len(rows) == 2
    by_donor = {r["donor_id"]: r for r in rows}
    assert by_donor["D1"]["snvs"] == 100
    assert by_donor["D1"]["snvs_per_mb"] == pytest.approx(100.0 / 50.0, abs=1e-9)
    assert by_donor["D2"]["snvs"] == 200


def test_pooled_burden_raises_on_mixed_callable_mb() -> None:
    df = pd.DataFrame([
        {"donor_id": "D1", "callable_mb": 50.0, "sample_id": "S1"},
        {"donor_id": "D2", "callable_mb": 60.0, "sample_id": "S2"},
    ])
    with pytest.raises(ValueError, match="mixed callable_mb"):
        aggregate_pooled_burden(df)
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run --frozen pytest code/scripts/tests/test_extract_normal_tissue_spectra.py -k burden -v
```

Expected: FAIL — functions not defined.

- [ ] **Step 3: Implement burden aggregations**

Add to `code/scripts/extract_normal_tissue_spectra.py`:

```python
def aggregate_pooled_burden(variants_df: pd.DataFrame) -> dict[str, object]:
    """Pooled per-tissue burden. Expects per-variant rows with donor_id, sample_id,
    callable_mb (constant per tissue, enforced).

    snvs_per_mb = snvs / callable_mb / n_samples (per-sample rate).
    """
    callable_values = variants_df["callable_mb"].unique()
    if len(callable_values) != 1:
        raise ValueError(
            f"aggregate_pooled_burden: mixed callable_mb values {sorted(callable_values)}"
        )
    callable_mb = float(callable_values[0])
    snvs = int(len(variants_df))
    n_donors = int(variants_df["donor_id"].nunique())
    n_samples = int(variants_df["sample_id"].nunique())
    snvs_per_mb = snvs / callable_mb / max(n_samples, 1)
    return {
        "snvs": snvs,
        "n_donors": n_donors,
        "n_samples": n_samples,
        "callable_mb": callable_mb,
        "snvs_per_mb": float(snvs_per_mb),
    }


def aggregate_per_donor_burden_rows(variants_df: pd.DataFrame) -> list[dict[str, object]]:
    """Per-donor burden rows. Assumes callable_mb constant per donor."""
    rows: list[dict[str, object]] = []
    for donor_id, grp in variants_df.groupby("donor_id"):
        callable_values = grp["callable_mb"].unique()
        if len(callable_values) != 1:
            raise ValueError(
                f"aggregate_per_donor_burden_rows: donor {donor_id} has mixed callable_mb"
            )
        callable_mb = float(callable_values[0])
        n_samples = int(grp["sample_id"].nunique())
        snvs = int(len(grp))
        rows.append({
            "donor_id": str(donor_id),
            "snvs": snvs,
            "n_samples": n_samples,
            "callable_mb": callable_mb,
            "snvs_per_mb": float(snvs / callable_mb / max(n_samples, 1)),
        })
    return rows
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
uv run --frozen pytest code/scripts/tests/test_extract_normal_tissue_spectra.py -v
```

Expected: all tests PASS.

- [ ] **Step 5: Commit**

```bash
git add code/scripts/extract_normal_tissue_spectra.py code/scripts/tests/test_extract_normal_tissue_spectra.py
git commit -m "$(cat <<'EOF'
t111: burden aggregations (pooled + per-donor) with snvs_per_mb

Pooled raises on mixed callable_mb; per-donor enforces constant callable_mb
per donor. Rate formula: snvs / callable_mb / n_samples.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 10: SigProfiler wrapper (per-variant → per-donor 96-context counts)

**Files:**
- Modify: `code/scripts/extract_normal_tissue_spectra.py`
- Modify: `code/scripts/tests/test_extract_normal_tissue_spectra.py`

This task isolates the SigProfiler dependency behind a single function. It gets one pure test (input/output schema only) and a slow-marked integration test (Task 14) that exercises the real reference lookup.

- [ ] **Step 1: Write the schema test**

Append to the test file:

```python
def test_compute_96_context_counts_schema_from_fake_matrix(monkeypatch) -> None:
    """Schema test: if SigProfiler returns a known 96-context matrix, our wrapper
    re-shapes it into the expected per-donor DataFrame."""
    from extract_normal_tissue_spectra import compute_96_context_counts

    # Fake SigProfiler output: 96 rows (contexts) × 3 columns (donors)
    fake_matrix = pd.DataFrame(
        0,
        index=CONTEXT_96,
        columns=["D1", "D2", "D3"],
    )
    fake_matrix.loc["A[C>A]A", "D1"] = 7
    fake_matrix.loc["T[T>G]T", "D2"] = 4

    def _fake_sigprofiler(variants_df, assembly):  # noqa: ARG001
        return fake_matrix

    monkeypatch.setattr(
        "extract_normal_tissue_spectra._sigprofiler_matrix",
        _fake_sigprofiler,
    )

    variants = _df(
        donor_id=["D1", "D2", "D3"],
        tissue_label=["Liver"] * 3,
        chrom=["chr1"] * 3, pos=[1, 2, 3],
        ref=["A", "T", "C"], alt=["C", "G", "A"],
    )
    out = compute_96_context_counts(variants, assembly="GRCh37")
    assert set(out.columns) >= set(CONTEXT_96) | {"donor_id"}
    assert len(out) == 3
    d1 = out.loc[out["donor_id"] == "D1"].iloc[0]
    assert d1["A[C>A]A"] == 7
    d2 = out.loc[out["donor_id"] == "D2"].iloc[0]
    assert d2["T[T>G]T"] == 4
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
uv run --frozen pytest code/scripts/tests/test_extract_normal_tissue_spectra.py -k compute_96 -v
```

Expected: FAIL — `compute_96_context_counts` / `_sigprofiler_matrix` not defined.

- [ ] **Step 3: Implement the wrapper + real SigProfiler call**

Add to `code/scripts/extract_normal_tissue_spectra.py`:

```python
def _sigprofiler_matrix(variants_df: pd.DataFrame, assembly: str) -> pd.DataFrame:
    """Run SigProfilerMatrixGenerator on an in-memory per-variant table.

    Writes a temporary VCF-like MAF, invokes the matrix generator, reads the resulting
    SBS96 matrix, returns it as a DataFrame with 96 rows (contexts) × N columns (donors).

    This is the single SigProfiler touch-point. Mocked out by tests except in the slow
    integration test (Task 14).

    First call for a given assembly may fail with FileNotFoundError if the reference
    bundle is not yet installed; we catch, install idempotently, and retry once.
    """
    import tempfile

    from SigProfilerMatrixGenerator import install as sigprofiler_install
    from SigProfilerMatrixGenerator.scripts import SigProfilerMatrixGeneratorFunc as matGen

    def _run(vcf_dir: Path) -> pd.DataFrame:
        matrices = matGen.SigProfilerMatrixGeneratorFunc(
            "normal_tissue",
            assembly,
            str(vcf_dir),
            exome=False, bed_file=None, chrom_based=False, plot=False,
            tsb_stat=False, seqInfo=False,
        )
        return matrices["96"]  # DataFrame: 96 rows × N donor cols

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        vcf_dir = tmp_path / "vcfs"
        vcf_dir.mkdir()
        # SigProfiler expects one VCF per sample in the input directory,
        # or a single combined MAF. We emit per-donor VCFs.
        for donor_id, grp in variants_df.groupby("donor_id"):
            vcf_path = vcf_dir / f"{donor_id}.vcf"
            with vcf_path.open("w") as fh:
                fh.write("##fileformat=VCFv4.2\n")
                fh.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
                for _, r in grp.iterrows():
                    fh.write(
                        f"{r['chrom']}\t{r['pos']}\t.\t{r['ref']}\t{r['alt']}\t.\tPASS\t.\n"
                    )

        try:
            sbs96 = _run(vcf_dir)
        except FileNotFoundError as exc:
            print(
                f"SigProfiler reference bundle for {assembly} not found ({exc}); "
                f"installing and retrying once.",
                file=sys.stderr,
            )
            sigprofiler_install.install(assembly, bash=True)
            sbs96 = _run(vcf_dir)
    return sbs96


def compute_96_context_counts(variants_df: pd.DataFrame, assembly: str) -> pd.DataFrame:
    """Wrapper returning per-donor 96-context counts as a DataFrame with
    columns: [CONTEXT_96..., donor_id, total_snvs].

    Input: validated, SNV-only per-variant rows with `donor_id, chrom, pos, ref, alt`.
    """
    sbs96 = _sigprofiler_matrix(variants_df, assembly=assembly)
    # Transpose: 96 rows × N donors → N rows (donors) × 96 cols (contexts)
    wide = sbs96.T
    wide = wide.reindex(columns=CONTEXT_96, fill_value=0)
    wide = wide.reset_index().rename(columns={"index": "donor_id"})
    wide["total_snvs"] = wide[CONTEXT_96].sum(axis=1).astype(int)
    return wide
```

- [ ] **Step 4: Run the test to verify it passes**

```bash
uv run --frozen pytest code/scripts/tests/test_extract_normal_tissue_spectra.py -v
```

Expected: all tests PASS (the SigProfiler call is mocked in the schema test).

- [ ] **Step 5: Commit**

```bash
git add code/scripts/extract_normal_tissue_spectra.py code/scripts/tests/test_extract_normal_tissue_spectra.py
git commit -m "$(cat <<'EOF'
t111: SigProfilerMatrixGenerator wrapper + schema test

Isolates the SigProfiler touch-point behind compute_96_context_counts().
Pure schema test via monkeypatch; real reference lookup exercised in
slow integration test (Task 14).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 11: Spectra row assembly

**Files:**
- Modify: `code/scripts/extract_normal_tissue_spectra.py`
- Modify: `code/scripts/tests/test_extract_normal_tissue_spectra.py`

This task ties the three aggregations together into a list of full spectra rows with all audit + metadata columns populated.

- [ ] **Step 1: Write failing tests**

Append to the test file:

```python
from extract_normal_tissue_spectra import build_spectra_rows_for_tissue


def test_build_spectra_rows_has_three_aggregations() -> None:
    per_donor_ctx = _synthetic_context_df({
        "D1": {"A[C>A]A": 60, "T[T>G]T": 40},   # 100 SNVs
        "D2": {"A[C>A]A": 80, "T[T>G]T": 20},   # 100 SNVs
    })
    rows = build_spectra_rows_for_tissue(
        per_donor_ctx=per_donor_ctx,
        source_id="li2021",
        tissue_uberon="UBERON:0002107",
        tissue_label="Liver",
        uberon_label="liver",
        assembly="GRCh37",
        sequencing_modality="WES",
        capture_kit_or_panel="SureSelectXT V7",
        callable_mb=48.2,
        n_samples=10,
        low_snv_threshold=50,
    )
    aggregations = {r["aggregation"] for r in rows}
    assert aggregations == {"pooled_counts", "donor_averaged_fraction", "per_donor"}
    # 1 pooled + 1 averaged + 2 per-donor = 4 rows
    assert len(rows) == 4


def test_build_spectra_rows_value_type_matches_aggregation() -> None:
    per_donor_ctx = _synthetic_context_df({"D1": {"A[C>A]A": 100}})
    rows = build_spectra_rows_for_tissue(
        per_donor_ctx=per_donor_ctx, source_id="li2021",
        tissue_uberon="UBERON:0002107", tissue_label="Liver", uberon_label="liver",
        assembly="GRCh37", sequencing_modality="WES",
        capture_kit_or_panel="SureSelectXT V7", callable_mb=48.2, n_samples=1,
        low_snv_threshold=50,
    )
    for r in rows:
        if r["aggregation"] == "donor_averaged_fraction":
            assert r["value_type"] == "fractions"
        else:
            assert r["value_type"] == "counts"


def test_build_spectra_rows_audit_columns_present_on_all_rows() -> None:
    per_donor_ctx = _synthetic_context_df({
        "D1": {"A[C>A]A": 100},
        "D2": {"A[C>A]A": 10},   # below default threshold 50
    })
    rows = build_spectra_rows_for_tissue(
        per_donor_ctx=per_donor_ctx, source_id="li2021",
        tissue_uberon="UBERON:0002107", tissue_label="Liver", uberon_label="liver",
        assembly="GRCh37", sequencing_modality="WES",
        capture_kit_or_panel="SureSelectXT V7", callable_mb=48.2, n_samples=2,
        low_snv_threshold=50,
    )
    for r in rows:
        assert r["n_donors_total"] == 2
        assert r["low_snv_threshold"] == 50
    avg_row = next(r for r in rows if r["aggregation"] == "donor_averaged_fraction")
    assert avg_row["n_donors_included"] == 1
    assert avg_row["n_donors_excluded_low_snvs"] == 1
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run --frozen pytest code/scripts/tests/test_extract_normal_tissue_spectra.py -k build_spectra -v
```

Expected: FAIL — `build_spectra_rows_for_tissue` not defined.

- [ ] **Step 3: Implement `build_spectra_rows_for_tissue`**

Add to `code/scripts/extract_normal_tissue_spectra.py`:

```python
def build_spectra_rows_for_tissue(  # noqa: PLR0913
    *,
    per_donor_ctx: pd.DataFrame,
    source_id: str,
    tissue_uberon: str,
    tissue_label: str,
    uberon_label: str,
    assembly: str,
    sequencing_modality: str,
    capture_kit_or_panel: str,
    callable_mb: float,
    n_samples: int,
    low_snv_threshold: int = 50,
) -> list[dict[str, object]]:
    """Produce all spectra rows (pooled + averaged + per-donor) for one tissue."""
    n_donors_total = int(per_donor_ctx["donor_id"].nunique())

    def _common(aggregation: str, value_type: str, **audit: object) -> dict[str, object]:
        return {
            "source_id": source_id,
            "tissue_uberon": tissue_uberon,
            "tissue_label": tissue_label,
            "uberon_label": uberon_label,
            "aggregation": aggregation,
            "value_type": value_type,
            "assembly": assembly,
            "sequencing_modality": sequencing_modality,
            "capture_kit_or_panel": capture_kit_or_panel,
            "callable_mb": callable_mb,
            "n_donors_total": n_donors_total,
            "n_samples": n_samples,
            "low_snv_threshold": low_snv_threshold,
            "donor_id": "",
            **audit,
        }

    rows: list[dict[str, object]] = []

    pooled = aggregate_pooled_counts(per_donor_ctx)
    rows.append({
        **_common(
            "pooled_counts", "counts",
            n_donors_included=n_donors_total,
            n_donors_excluded_low_snvs=0,
        ),
        **{ctx: pooled[ctx] for ctx in CONTEXT_96},
        "total_snvs": pooled["total_snvs"],
        "n_donors": n_donors_total,
    })

    averaged, audit = aggregate_donor_averaged_fraction(per_donor_ctx, threshold=low_snv_threshold)
    rows.append({
        **_common(
            "donor_averaged_fraction", "fractions",
            n_donors_included=audit["n_donors_included"],
            n_donors_excluded_low_snvs=audit["n_donors_excluded_low_snvs"],
        ),
        **averaged,
        "total_snvs": 0,  # fractions — not a meaningful count
        "n_donors": audit["n_donors_included"],
    })

    for donor_row in aggregate_per_donor_rows(per_donor_ctx):
        rows.append({
            **_common(
                "per_donor", "counts",
                n_donors_included=1,
                n_donors_excluded_low_snvs=0,
            ),
            **{ctx: donor_row[ctx] for ctx in CONTEXT_96},
            "total_snvs": donor_row["total_snvs"],
            "donor_id": donor_row["donor_id"],
            "n_donors": 1,
        })

    return rows
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
uv run --frozen pytest code/scripts/tests/test_extract_normal_tissue_spectra.py -v
```

Expected: all tests PASS.

- [ ] **Step 5: Commit**

```bash
git add code/scripts/extract_normal_tissue_spectra.py code/scripts/tests/test_extract_normal_tissue_spectra.py
git commit -m "$(cat <<'EOF'
t111: assemble spectra rows per tissue with value_type + audit columns

Ties pooled / averaged / per-donor aggregations into full rows carrying
assay metadata and donor-exclusion audit trail on every row.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 12: Burden row assembly + TSV writers

**Files:**
- Modify: `code/scripts/extract_normal_tissue_spectra.py`
- Modify: `code/scripts/tests/test_extract_normal_tissue_spectra.py`

- [ ] **Step 1: Write failing tests**

Append to the test file:

```python
from extract_normal_tissue_spectra import (
    build_burden_rows_for_tissue,
    write_spectra_tsv,
    write_burden_tsv,
    SPECTRA_COLUMNS,
    BURDEN_COLUMNS,
)


def test_build_burden_rows_has_pooled_plus_per_donor() -> None:
    variants = pd.DataFrame([
        {"donor_id": "D1", "sample_id": "S1", "callable_mb": 50.0},
        {"donor_id": "D1", "sample_id": "S1", "callable_mb": 50.0},
        {"donor_id": "D2", "sample_id": "S2", "callable_mb": 50.0},
    ])
    rows = build_burden_rows_for_tissue(
        variants_df=variants,
        source_id="li2021",
        tissue_uberon="UBERON:0002107",
        tissue_label="Liver",
        uberon_label="liver",
        assembly="GRCh37",
        sequencing_modality="WES",
        capture_kit_or_panel="SureSelectXT V7",
    )
    aggregations = [r["aggregation"] for r in rows]
    assert aggregations.count("pooled") == 1
    assert aggregations.count("per_donor") == 2


def test_write_spectra_tsv_column_order(tmp_path: Path) -> None:
    per_donor_ctx = _synthetic_context_df({"D1": {"A[C>A]A": 100}})
    rows = build_spectra_rows_for_tissue(
        per_donor_ctx=per_donor_ctx, source_id="li2021",
        tissue_uberon="UBERON:0002107", tissue_label="Liver", uberon_label="liver",
        assembly="GRCh37", sequencing_modality="WES",
        capture_kit_or_panel="SureSelectXT V7", callable_mb=48.2, n_samples=1,
        low_snv_threshold=50,
    )
    out = tmp_path / "out.tsv"
    write_spectra_tsv(rows, out)
    df = pd.read_csv(out, sep="\t")
    assert list(df.columns) == SPECTRA_COLUMNS


def test_write_burden_tsv_column_order(tmp_path: Path) -> None:
    variants = pd.DataFrame([
        {"donor_id": "D1", "sample_id": "S1", "callable_mb": 50.0},
    ])
    rows = build_burden_rows_for_tissue(
        variants_df=variants, source_id="li2021",
        tissue_uberon="UBERON:0002107", tissue_label="Liver", uberon_label="liver",
        assembly="GRCh37", sequencing_modality="WES",
        capture_kit_or_panel="SureSelectXT V7",
    )
    out = tmp_path / "out.tsv"
    write_burden_tsv(rows, out)
    df = pd.read_csv(out, sep="\t")
    assert list(df.columns) == BURDEN_COLUMNS
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run --frozen pytest code/scripts/tests/test_extract_normal_tissue_spectra.py -k "build_burden or write_spectra or write_burden" -v
```

Expected: FAIL — functions/constants not defined.

- [ ] **Step 3: Implement burden-row assembly, column orderings, and TSV writers**

Add to `code/scripts/extract_normal_tissue_spectra.py`:

```python
SPECTRA_COLUMNS: list[str] = [
    "source_id", "tissue_uberon", "tissue_label", "uberon_label",
    "aggregation", "value_type", "donor_id",
    "assembly", "sequencing_modality", "capture_kit_or_panel", "callable_mb",
    "n_donors_total", "n_donors_included", "n_donors_excluded_low_snvs",
    "low_snv_threshold",
    "n_donors", "n_samples", "total_snvs",
    *CONTEXT_96,
]

BURDEN_COLUMNS: list[str] = [
    "source_id", "tissue_uberon", "tissue_label", "uberon_label",
    "aggregation", "donor_id",
    "assembly", "sequencing_modality", "capture_kit_or_panel", "callable_mb",
    "n_donors", "n_samples", "snvs", "snvs_per_mb",
]


def build_burden_rows_for_tissue(  # noqa: PLR0913
    *,
    variants_df: pd.DataFrame,
    source_id: str,
    tissue_uberon: str,
    tissue_label: str,
    uberon_label: str,
    assembly: str,
    sequencing_modality: str,
    capture_kit_or_panel: str,
) -> list[dict[str, object]]:
    """Produce pooled + per-donor burden rows for one tissue."""
    def _common(aggregation: str) -> dict[str, object]:
        return {
            "source_id": source_id,
            "tissue_uberon": tissue_uberon,
            "tissue_label": tissue_label,
            "uberon_label": uberon_label,
            "aggregation": aggregation,
            "assembly": assembly,
            "sequencing_modality": sequencing_modality,
            "capture_kit_or_panel": capture_kit_or_panel,
            "donor_id": "",
        }

    rows: list[dict[str, object]] = []

    pooled = aggregate_pooled_burden(variants_df)
    rows.append({**_common("pooled"), **pooled})

    for per_donor in aggregate_per_donor_burden_rows(variants_df):
        row = {**_common("per_donor"), **per_donor, "n_donors": 1}
        rows.append(row)

    return rows


def write_spectra_tsv(rows: list[dict[str, object]], path: Path) -> None:
    df = pd.DataFrame(rows)
    # Enforce column order; fill any missing with 0 (should never happen, but defend the schema).
    for col in SPECTRA_COLUMNS:
        if col not in df.columns:
            df[col] = 0
    df = df[SPECTRA_COLUMNS]
    df.to_csv(path, sep="\t", index=False)


def write_burden_tsv(rows: list[dict[str, object]], path: Path) -> None:
    df = pd.DataFrame(rows)
    for col in BURDEN_COLUMNS:
        if col not in df.columns:
            df[col] = 0
    df = df[BURDEN_COLUMNS]
    df.to_csv(path, sep="\t", index=False)
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
uv run --frozen pytest code/scripts/tests/test_extract_normal_tissue_spectra.py -v
```

Expected: all tests PASS.

- [ ] **Step 5: Commit**

```bash
git add code/scripts/extract_normal_tissue_spectra.py code/scripts/tests/test_extract_normal_tissue_spectra.py
git commit -m "$(cat <<'EOF'
t111: burden row assembly + TSV writers with column-ordering constants

SPECTRA_COLUMNS (18 metadata + 96 context = 114) and BURDEN_COLUMNS (14).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 13: Main orchestration + snakemake wiring

**Files:**
- Modify: `code/scripts/extract_normal_tissue_spectra.py`
- Modify: `code/scripts/tests/test_extract_normal_tissue_spectra.py`

- [ ] **Step 1: Write failing test that drives the per-source extraction end-to-end with a mocked SigProfiler**

Append to the test file:

```python
from extract_normal_tissue_spectra import extract_for_source


def test_extract_for_source_emits_spectra_and_burden_rows(monkeypatch, tmp_path: Path) -> None:
    # 6 variants: 2 donors × 3 variants each, all liver, all SBS, all chr1.
    variants_tsv = tmp_path / "variants.tsv"
    variants_tsv.write_text(
        "donor_id\ttissue_label\tsample_id\tchrom\tpos\tref\talt\n"
        "D1\tLiver\tD1-s1\tchr1\t100\tC\tA\n"
        "D1\tLiver\tD1-s1\tchr1\t" "200\tC\tA\n"
        "D1\tLiver\tD1-s1\tchr1\t" "300\tC\tA\n"
        "D2\tLiver\tD2-s1\tchr1\t" "400\tC\tA\n"
        "D2\tLiver\tD2-s1\tchr1\t" "500\tC\tA\n"
        "D2\tLiver\tD2-s1\tchr1\t" "600\tC\tA\n"
    )
    mapping_tsv = tmp_path / "map.tsv"
    mapping_tsv.write_text(
        "source\ttissue_label\ttissue_uberon\tuberon_label\tnotes\n"
        "li2021\tLiver\tUBERON:0002107\tliver\t\n"
    )

    def _fake_sigprofiler(variants_df, assembly):  # noqa: ARG001
        m = pd.DataFrame(0, index=CONTEXT_96, columns=sorted(variants_df["donor_id"].unique()))
        m.loc["A[C>A]A", :] = 3  # 3 SBS per donor
        return m

    monkeypatch.setattr(
        "extract_normal_tissue_spectra._sigprofiler_matrix", _fake_sigprofiler
    )

    spectra_rows, burden_rows = extract_for_source(
        source="li2021",
        variants_tsv=variants_tsv,
        mapping_tsv=mapping_tsv,
        assembly="GRCh37",
        low_snv_threshold=2,  # low threshold so both D1 and D2 are included
    )

    # 1 tissue × (1 pooled + 1 averaged + 2 per-donor) = 4 spectra rows
    assert len(spectra_rows) == 4
    # 1 tissue × (1 pooled + 2 per-donor) = 3 burden rows
    assert len(burden_rows) == 3
    pooled_spectra = next(r for r in spectra_rows if r["aggregation"] == "pooled_counts")
    assert pooled_spectra["tissue_uberon"] == "UBERON:0002107"
    assert pooled_spectra["total_snvs"] == 6
    pooled_burden = next(r for r in burden_rows if r["aggregation"] == "pooled")
    assert pooled_burden["snvs"] == 6
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
uv run --frozen pytest code/scripts/tests/test_extract_normal_tissue_spectra.py -k extract_for_source -v
```

Expected: FAIL — `extract_for_source` not defined.

- [ ] **Step 3: Implement `extract_for_source` + main wiring**

Add to `code/scripts/extract_normal_tissue_spectra.py`:

```python
_SOURCE_ASSEMBLY = {"li2021": "GRCh37", "xu2025": "GRCh38"}


def extract_for_source(
    *,
    source: str,
    variants_tsv: Path,
    mapping_tsv: Path,
    assembly: str | None = None,
    low_snv_threshold: int = 50,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """Run the full extraction for a single source. Returns (spectra_rows, burden_rows)."""
    if assembly is None:
        assembly = _SOURCE_ASSEMBLY[source]

    raw = pd.read_csv(variants_tsv, sep="\t", dtype=str, na_filter=False)
    raw["pos"] = raw["pos"].astype(int)

    cleaned, contract_stats = validate_input_contract(raw, source=source, assembly=assembly)
    print(
        f"{source}: {contract_stats['n_indels_dropped']} indel rows dropped, "
        f"{contract_stats['n_mito_dropped']} mitochondrial rows dropped, "
        f"{contract_stats['n_duplicates_collapsed']} within-donor duplicates collapsed",
        file=sys.stderr,
    )

    cleaned = attach_uberon(cleaned, mapping_tsv=mapping_tsv, source=source)
    cleaned = attach_assay_metadata(cleaned, source=source)

    spectra_rows: list[dict[str, object]] = []
    burden_rows: list[dict[str, object]] = []

    for (tissue_label, tissue_uberon, uberon_label, modality, kit, callable_mb), tissue_df in \
            cleaned.groupby(
                ["tissue_label", "tissue_uberon", "uberon_label",
                 "sequencing_modality", "capture_kit_or_panel", "callable_mb"]
            ):
        # One SigProfiler invocation per tissue — emits per-donor 96-context rows.
        per_donor_ctx = compute_96_context_counts(tissue_df, assembly=assembly)

        n_samples = int(tissue_df.get("sample_id", tissue_df["donor_id"]).nunique())

        spectra_rows.extend(build_spectra_rows_for_tissue(
            per_donor_ctx=per_donor_ctx,
            source_id=source,
            tissue_uberon=tissue_uberon,
            tissue_label=tissue_label,
            uberon_label=uberon_label,
            assembly=assembly,
            sequencing_modality=modality,
            capture_kit_or_panel=kit,
            callable_mb=float(callable_mb),
            n_samples=n_samples,
            low_snv_threshold=low_snv_threshold,
        ))

        burden_df = tissue_df.assign(
            sample_id=tissue_df.get("sample_id", tissue_df["donor_id"]),
        )
        burden_rows.extend(build_burden_rows_for_tissue(
            variants_df=burden_df,
            source_id=source,
            tissue_uberon=tissue_uberon,
            tissue_label=tissue_label,
            uberon_label=uberon_label,
            assembly=assembly,
            sequencing_modality=modality,
            capture_kit_or_panel=kit,
        ))

    return spectra_rows, burden_rows


def main() -> None:
    """Snakemake entry point."""
    snek = snakemake  # type: ignore[name-defined]

    li2021_tsv = Path(snek.input.li2021)
    xu2025_tsv = Path(snek.input.xu2025)
    mapping_tsv = Path(snek.input.mapping)

    spectra_out = Path(snek.output.spectra)
    burden_out = Path(snek.output.burden)

    spectra_rows: list[dict[str, object]] = []
    burden_rows: list[dict[str, object]] = []

    for source, variants_tsv in [("li2021", li2021_tsv), ("xu2025", xu2025_tsv)]:
        s, b = extract_for_source(
            source=source, variants_tsv=variants_tsv, mapping_tsv=mapping_tsv,
        )
        spectra_rows.extend(s)
        burden_rows.extend(b)

    write_spectra_tsv(spectra_rows, spectra_out)
    write_burden_tsv(burden_rows, burden_out)

    print(
        f"Wrote {len(spectra_rows)} spectra rows to {spectra_out}; "
        f"{len(burden_rows)} burden rows to {burden_out}",
        file=sys.stderr,
    )
```

- [ ] **Step 4: Run the test to verify it passes**

```bash
uv run --frozen pytest code/scripts/tests/test_extract_normal_tissue_spectra.py -v
```

Expected: all tests PASS.

- [ ] **Step 5: Commit**

```bash
git add code/scripts/extract_normal_tissue_spectra.py code/scripts/tests/test_extract_normal_tissue_spectra.py
git commit -m "$(cat <<'EOF'
t111: extract_for_source orchestration + snakemake main()

Walks cleaned per-variant rows once, groups by tissue, emits both spectra
and burden rows per tissue. main() wires snakemake input/output to the
two-source loop.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 14: Slow integration test with real SigProfiler

**Files:**
- Modify: `code/scripts/tests/test_extract_normal_tissue_spectra.py`
- Create: `code/scripts/tests/fixtures/li2021_fixture.tsv`
- Create: `code/scripts/tests/fixtures/xu2025_fixture.tsv`
- Create: `code/scripts/tests/fixtures/mapping_fixture.tsv`

- [ ] **Step 1: Create the three fixture files**

Create `code/scripts/tests/fixtures/li2021_fixture.tsv`:

```
donor_id	tissue_label	sample_id	chrom	pos	ref	alt
PN1	Liver	PN1-L-1	chr1	1000000	C	A
PN1	Liver	PN1-L-1	chr1	2000000	C	A
PN1	Liver	PN1-L-1	chr1	3000000	C	A
PN2	Liver	PN2-L-1	chr1	4000000	T	C
PN2	Liver	PN2-L-1	chr1	5000000	T	C
PN2	Liver	PN2-L-1	chr1	6000000	T	C
PN1	Esophagus	PN1-E-1	chr2	1000000	C	T
PN2	Esophagus	PN2-E-1	chr2	2000000	C	T
PN2	Esophagus	PN2-E-1	chr2	3000000	C	T
```

Create `code/scripts/tests/fixtures/xu2025_fixture.tsv`:

```
donor_id	tissue_label	sample_id	chrom	pos	ref	alt
GTEX-D1	Liver	GTEX-D1-L	chr1	1000000	C	A
GTEX-D1	Liver	GTEX-D1-L	chr1	2000000	C	A
GTEX-D2	Liver	GTEX-D2-L	chr1	3000000	T	G
```

Create `code/scripts/tests/fixtures/mapping_fixture.tsv`:

```
source	tissue_label	tissue_uberon	uberon_label	notes
li2021	Liver	UBERON:0002107	liver	
li2021	Esophagus	UBERON:0001043	esophagus	
xu2025	Liver	UBERON:0002107	liver	
```

- [ ] **Step 2: Write the slow integration test**

Append to `code/scripts/tests/test_extract_normal_tissue_spectra.py`:

```python
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


@pytest.mark.slow
def test_end_to_end_with_real_sigprofiler_grch37() -> None:
    """Full extraction on a tiny fixture using the real SigProfiler reference lookup.

    Validates:
    - 96 context columns actually computed (non-zero counts)
    - pooled_counts total_snvs matches input variant count
    - spectra / burden schemas round-trip
    """
    spectra_rows, burden_rows = extract_for_source(
        source="li2021",
        variants_tsv=FIXTURES_DIR / "li2021_fixture.tsv",
        mapping_tsv=FIXTURES_DIR / "mapping_fixture.tsv",
        low_snv_threshold=2,
    )

    # Two tissues (Liver, Esophagus) × (1 pooled + 1 averaged + 2 per-donor) = 8 spectra rows
    assert len(spectra_rows) == 8
    # Two tissues × (1 pooled + 2 per-donor) = 6 burden rows
    assert len(burden_rows) == 6

    liver_pooled = next(
        r for r in spectra_rows
        if r["tissue_label"] == "Liver" and r["aggregation"] == "pooled_counts"
    )
    assert liver_pooled["total_snvs"] == 6
    # All 6 liver variants were C>A or T>C — expect non-zero in those context families
    ctx_sum = sum(liver_pooled[ctx] for ctx in CONTEXT_96)
    assert ctx_sum == 6
```

- [ ] **Step 3: Run the pure tests without -m slow to confirm unchanged behaviour**

```bash
uv run --frozen pytest code/scripts/tests/ -q
```

Expected: all pure tests pass; the `test_end_to_end_with_real_sigprofiler_grch37` is skipped (unmarked runs skip slow-marked tests by default).

- [ ] **Step 4: Run the slow integration test explicitly**

```bash
uv run --frozen pytest code/scripts/tests/test_extract_normal_tissue_spectra.py -m slow -v
```

Expected: PASS. First run will download the GRCh37 reference bundle (~1.5 GB) — this may take several minutes.

- [ ] **Step 5: Commit**

```bash
git add code/scripts/tests/test_extract_normal_tissue_spectra.py code/scripts/tests/fixtures/
git commit -m "$(cat <<'EOF'
t111: slow-marked integration test with real SigProfiler + fixtures

9-variant Li2021 fixture + 3-variant Xu2025 fixture + minimal mapping.
Validates end-to-end schema + counts against the real reference lookup.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 15: Snakemake rule

**Files:**
- Modify: `code/workflows/Snakefile`

- [ ] **Step 1: Locate the right insertion point**

Read `code/workflows/Snakefile` near the existing `process_bailey2018_drivers` / `process_sanchez_vega_pathways` rules (around lines 35–80). The new rule is peer-shaped and belongs among them.

- [ ] **Step 2: Add the rule**

Insert after `process_cgc` (after the block ending roughly at line 78):

```
#
# Normal-tissue reference spectra + burden. Builds two reference tables from per-variant
# supplementary data from Li 2021 (Nature, hg19) + Xu 2025 (bioRxiv, GRCh38).
#
# Outputs:
#   data/normal_tissue_spectra.tsv — 96-context SBS spectra per (tissue, aggregation)
#   data/normal_tissue_burden.tsv  — per-tissue / per-donor burden (snvs_per_mb)
#
# Manual prerequisites (gated by Task 0 data-access gate):
#   data/li2021_somatic_mutations.tsv
#   data/xu2025_somatic_mutations.tsv
#   data/tissue_uberon_mapping.tsv  (committed to git)
#
# First run downloads SigProfilerMatrixGenerator reference bundles (~1.5 GB/assembly)
# to the user cache.
#
rule extract_normal_tissue_spectra:
  input:
    li2021="data/li2021_somatic_mutations.tsv",
    xu2025="data/xu2025_somatic_mutations.tsv",
    mapping="data/tissue_uberon_mapping.tsv"
  output:
    spectra="data/normal_tissue_spectra.tsv",
    burden="data/normal_tissue_burden.tsv"
  script:
    "../scripts/extract_normal_tissue_spectra.py"
```

- [ ] **Step 3: Lint the Snakefile**

```bash
uv run snakemake --lint -s code/workflows/Snakefile --configfile code/config/config-10k-genes.yml
```

Expected: no new lint warnings attributable to the new rule.

- [ ] **Step 4: Smoke-test the rule with `--dry-run` (does not require the real input data yet)**

```bash
uv run snakemake -s code/workflows/Snakefile --configfile code/config/config-10k-genes.yml --dry-run data/normal_tissue_spectra.tsv data/normal_tissue_burden.tsv 2>&1 | tail -20
```

Expected: Snakemake reports the rule would run (or reports the manual-prereq inputs are missing — both outcomes confirm the rule is discoverable). It must not report a syntax error.

- [ ] **Step 5: Commit**

```bash
git add code/workflows/Snakefile
git commit -m "$(cat <<'EOF'
t111: Snakemake rule extract_normal_tissue_spectra

Wires the script into the workflow. Outputs data/normal_tissue_spectra.tsv
and data/normal_tissue_burden.tsv keyed on UBERON; inputs gated by the
data-access verification in Task 0.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 16: Real-data execution + provenance doc

**Files:**
- Create/Stage: `data/li2021_somatic_mutations.tsv` (from Task 0)
- Create/Stage: `data/xu2025_somatic_mutations.tsv` (from Task 0)
- Create: `doc/datasets/normal-tissue-spectra.md`

- [ ] **Step 1: Stage the Li2021 supplementary data (XLSX → TSV conversion)**

Per the scope amendment, we only stage Li2021. The Task 0 gate record confirmed the supplementary file is an XLSX, not a TSV, so staging requires a conversion step:

1. Download `41586_2021_3836_MOESM5_ESM.xlsx` from the URL in `doc/plans/t111-data-gate-record.md` (if not already downloaded). Verify SHA256 matches the gate record.
2. Write a small one-off staging script at `code/scripts/stage_li2021_somatic_mutations.py` that:
   - Reads the first sheet (Sheet1) of the XLSX, skipping the 2 title/blank header rows so row 3 becomes the data header.
   - Parses the `sampleID` column of the form `PN{donor}{tissue_code}-{layer}-{biopsy}` into three columns: `donor_id` (e.g., `PN1`), `tissue_label` (looked up from the tissue_code — see below), `sample_id` (the original sampleID).
   - Renames `chr → chrom`, `mut → alt`; keeps `pos`, `ref`.
   - Emits the columns expected by the input contract: `donor_id, tissue_label, sample_id, chrom, pos, ref, alt`.
   - Writes to `data/li2021_somatic_mutations.tsv`.

   The tissue_code → tissue_label lookup (to be confirmed empirically by sampling a few sampleIDs of each tissue from the XLSX):
   ```python
   TISSUE_CODE_MAP = {
       "B": "Bronchia",
       "E": "Esophagus",
       "Ca": "Cardia",     # two-letter code to disambiguate from Colon
       "S": "Stomach",
       "D": "Duodenum",
       "C": "Colon",
       "R": "Rectum",
       "L": "Liver",
       "P": "Pancreas",
   }
   ```
   Match the longest-prefix code first (greedy) so `Ca` beats `C`. If any sampleID fails to match a known code, raise rather than silently drop.

3. Run the staging script once:
   ```bash
   uv run python code/scripts/stage_li2021_somatic_mutations.py \
       --xlsx data/41586_2021_3836_MOESM5_ESM.xlsx \
       --out data/li2021_somatic_mutations.tsv
   ```
4. Spot-check the output:
   ```bash
   head -5 data/li2021_somatic_mutations.tsv
   wc -l data/li2021_somatic_mutations.tsv  # expect ~66,188 + 1 header
   uv run python -c "import pandas as pd; df = pd.read_csv('data/li2021_somatic_mutations.tsv', sep='\t'); print(df.tissue_label.value_counts()); print(df.donor_id.value_counts())"
   ```

The staging script is committed to git; the source XLSX and the staged TSV are gitignored (large files; the gate record plus the staging script are sufficient for reproducibility).

- [ ] **Step 2: Run the full Snakemake rule against real data**

```bash
uv run snakemake -s code/workflows/Snakefile --configfile code/config/config-10k-genes.yml -j1 data/normal_tissue_spectra.tsv data/normal_tissue_burden.tsv 2>&1 | tee /tmp/t111_run.log
```

Expected: rule runs to completion. First run downloads GRCh37 reference bundle (Xu2025 dropped from scope, so no GRCh38 download). Stderr captures the contract summaries (indels/mito/duplicates dropped, tissues found, donors per tissue).

- [ ] **Step 3: Sanity-check the outputs**

```bash
uv run python -c "
import pandas as pd
s = pd.read_csv('data/normal_tissue_spectra.tsv', sep='\t')
b = pd.read_csv('data/normal_tissue_burden.tsv', sep='\t')
print(f'spectra: {len(s)} rows, {len(s.columns)} cols')
print(f'  aggregations: {s.aggregation.value_counts().to_dict()}')
print(f'  unique tissues: {s.tissue_uberon.nunique()}')
print(f'  sources: {s.source_id.value_counts().to_dict()}')
print(f'burden: {len(b)} rows')
print(f'  pooled snvs_per_mb range: {b[b.aggregation==\"pooled\"].snvs_per_mb.agg([\"min\", \"max\"]).to_dict()}')
"
```

Expected: rough per-source row counts match design estimates (~250 spectra rows total, ~100 burden rows); pooled `snvs_per_mb` falls in the 0.1–20 mut/Mb range for normal tissue.

- [ ] **Step 4: Write the provenance doc**

Create `doc/datasets/normal-tissue-spectra.md`:

```markdown
# Normal-tissue 96-context SBS spectra and burden

Generated by `rule extract_normal_tissue_spectra` (`code/scripts/extract_normal_tissue_spectra.py`).

Outputs:
- `data/normal_tissue_spectra.tsv` — 96-trinucleotide spectra per (tissue, aggregation)
- `data/normal_tissue_burden.tsv` — per-tissue / per-donor mutation burden

## Sources

| Source | Paper | DOI | Assembly | Supplementary file URL | SHA256 | Retrieved |
|---|---|---|---|---|---|---|
| li2021 | Li et al. 2021 *Nature* | 10.1038/s41586-021-03836-1 | GRCh37 | <URL from Task 0> | <sha256> | <date> |
| xu2025 | Xu et al. 2025 bioRxiv | 10.1101/2025.01.07.631808 | GRCh38 | <URL from Task 0> | <sha256> | <date> |

## Extraction-run summary

(Captured from the Task 16 Step 2 log — most recent extraction.)

```
<paste the stderr summary block from /tmp/t111_run.log here>
```

## Per-tissue provenance

| source | tissue_uberon | tissue_label | n_donors | notable exposures | uberon_mapping_notes |
|---|---|---|---|---|---|
| li2021 | UBERON:0002107 | Liver | 5 | PN2 liver = aristolochic acid; PN9 liver = tobacco | direct mapping |
| li2021 | UBERON:0001043 | Esophagus | 5 | tobacco in PN9 | direct mapping |
| li2021 | UBERON:0007650 | Cardia | 3 | — | gastric cardia; distinct from stomach body |
| li2021 | UBERON:0000945 | Stomach | 4 | — | direct mapping |
| li2021 | UBERON:0002114 | Duodenum | 4 | — | direct mapping |
| li2021 | UBERON:0001155 | Colon | 5 | — | direct mapping |
| li2021 | UBERON:0001052 | Rectum | 4 | — | direct mapping |
| li2021 | UBERON:0002185 | Bronchia | 3 | tobacco in PN9 | "Bronchia" → primary bronchus |
| li2021 | UBERON:0001264 | Pancreas | 5 | — | direct mapping |
| xu2025 | … | … | … | … | … |

(fill the xu2025 rows from the actual data)

## Aggregation definitions

- **pooled_counts** — column-wise sum of per-donor 96-context counts across all donors for the tissue. Integer counts. Highest-burden donor dominates.
- **donor_averaged_fraction** — per-donor 96-vector normalised to a fraction (sum = 1), then averaged across donors. Re-normalised to guard against rounding drift. Fractions summing to exactly 1. Donors with fewer than `low_snv_threshold` (default 50) SNVs in the tissue are excluded; excluded counts surface on the output row via `n_donors_excluded_low_snvs` / `low_snv_threshold`.
- **per_donor** — raw per-donor 96-context counts. Integer counts. One row per donor per tissue.

## SBS-only filtering

Indels and DBS variants are filtered out (SigProfiler SBS96 matrix only). Drop counts surface in the extraction-run summary; any non-zero indel/DBS count is documented above.

## Replication

Regenerate with:

```bash
uv run snakemake -s code/workflows/Snakefile --configfile code/config/config-10k-genes.yml -j1 \
    data/normal_tissue_spectra.tsv data/normal_tissue_burden.tsv
```

Requires:
- `data/li2021_somatic_mutations.tsv` staged per the URL above
- `data/xu2025_somatic_mutations.tsv` staged per the URL above
- `data/tissue_uberon_mapping.tsv` (in repo)
- Internet access on first run (SigProfilerMatrixGenerator downloads GRCh37 + GRCh38 reference bundles to the user cache, ~1.5 GB each)

## Related

- Design: `doc/plans/2026-04-18-t111-normal-tissue-spectra-design.md`
- Plan: `doc/plans/2026-04-18-t111-normal-tissue-spectra-plan.md`
- Data-access gate record: `doc/plans/t111-data-gate-record.md`
- Topic: `topic:signature-decomposition-unmatched-normal`
- Questions consuming this output: q007, q008, q010
```

Fill in the placeholders (`<URL from Task 0>`, `<sha256>`, `<date>`, `<paste the stderr summary block>`, and the xu2025 per-tissue rows) with the actual values from this run.

- [ ] **Step 5: Commit the provenance doc + the real extraction outputs**

The outputs go to `data/` — confirm they're gitignored (the existing pattern treats large data files as gitignored and regenerable). Only commit the provenance doc and any mapping additions.

```bash
git add doc/datasets/normal-tissue-spectra.md
# If Task 16 Step 1 revealed new tissues not in data/tissue_uberon_mapping.tsv, amend that file too:
# git add data/tissue_uberon_mapping.tsv
git commit -m "$(cat <<'EOF'
t111: provenance doc for normal_tissue_spectra + normal_tissue_burden

Records source URLs + SHA256, aggregation definitions, per-tissue
donor counts and notable exposures, regeneration instructions.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 6: Verify `data/normal_tissue_spectra.tsv` and `data/normal_tissue_burden.tsv` are gitignored**

```bash
git check-ignore data/normal_tissue_spectra.tsv data/normal_tissue_burden.tsv
```

Expected output: both paths echoed (confirming they are gitignored by an existing pattern in `.gitignore`). If not, add to `.gitignore`:

```
data/normal_tissue_spectra.tsv
data/normal_tissue_burden.tsv
```

If `.gitignore` needs editing, commit:
```bash
git add .gitignore
git commit -m "$(cat <<'EOF'
t111: gitignore regenerable normal-tissue reference tables

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 17: Close out + task status update

**Files:**
- Update: science-tool task status (t111 → completed)

- [ ] **Step 1: Full test suite run**

```bash
uv run --frozen pytest code/scripts/tests/ -q
```

Expected: all pure tests pass. Slow tests skipped (opt-in via `-m slow`).

- [ ] **Step 2: Ruff lint + format check**

```bash
uv run --frozen ruff check code/scripts/extract_normal_tissue_spectra.py code/scripts/tests/test_extract_normal_tissue_spectra.py
uv run --frozen ruff format --check code/scripts/extract_normal_tissue_spectra.py code/scripts/tests/test_extract_normal_tissue_spectra.py
```

Expected: clean. If format-check fails, run `uv run --frozen ruff format code/scripts/extract_normal_tissue_spectra.py code/scripts/tests/test_extract_normal_tissue_spectra.py` and commit the formatting fix.

- [ ] **Step 3: Snakefile lint**

```bash
uv run snakemake --lint -s code/workflows/Snakefile --configfile code/config/config-10k-genes.yml
```

Expected: no new lint warnings.

- [ ] **Step 4: Mark t111 completed in science-tool**

```bash
uv run science-tool tasks complete t111
```

Expected output: `[t111] completed`.

Also verify t109 (blocked-by state) is unchanged, and t110 is still blocked by t109:

```bash
uv run science-tool tasks list | grep -E "t109|t110|t111"
```

- [ ] **Step 5: Final commit (task status file if it tracks state in git)**

```bash
git add tasks/
git diff --cached --quiet || git commit -m "$(cat <<'EOF'
tasks: t111 complete — normal-tissue spectra extraction pipeline

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 6: Report outcome**

Summarise in the conversation: (a) row counts emitted, (b) any still-unconfirmed fields in the provenance doc, (c) any tissues that needed UBERON-mapping judgment calls, (d) whether `question:0007-cross-tissue-somatic-mutation-rate-variation-as-null-model` / `question:0008-signature-decomposition-tissue-background-subtraction` / `question:0010-cuplr-style-tof-classifier-for-suspect-normal-samples` are now unblocked, (e) whether any follow-up tasks should be filed (e.g., t109's now-unblocked SigProfiler-pipeline-integration, or a deferred Xu2025-signature-decomposition check if paper Methods surfaces a published decomposition).
