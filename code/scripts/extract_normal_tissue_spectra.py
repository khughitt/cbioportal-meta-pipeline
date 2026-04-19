"""
extract_normal_tissue_spectra.py

Builds two reference tables from Li 2021 per-variant supplementary data:

- `data/normal_tissue_spectra.tsv` — 96-trinucleotide SBS spectra per normal tissue
  (three aggregations: pooled_counts, donor_averaged_fraction, per_donor)
- `data/normal_tissue_burden.tsv` — per-tissue / per-donor mutation burden with
  callable-Mb denominator and sequencing-modality metadata

Rows are keyed on UBERON ontology IDs; source tissue labels are preserved for audit.

Design: doc/plans/2026-04-18-t111-normal-tissue-spectra-design.md
Plan:   doc/plans/2026-04-18-t111-normal-tissue-spectra-plan.md
"""
import sys  # noqa: F401
from pathlib import Path  # noqa: F401

import pandas as pd  # noqa: F401

# Assay metadata constants. Sourced from Li 2021 Methods:
# SureSelectXT Human All Exon V6 (esophagus) or V7 (other tissues), callable ~60 Mb / ~48.2 Mb.
# Populated concretely in Task 5.
ASSAY_METADATA: dict[tuple[str, str | None], dict[str, object]] = {
    # Populated in Task 5.
}


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
    # TODO(t111-followup): assert chrom/pos ranges match the declared assembly.
    # Design spec §Input contract requires this check but defers encoding of
    # per-chromosome lengths for GRCh37/GRCh38. For now, `assembly` is accepted
    # and preserved on the stats object for audit, but no range check is applied.
    _ = assembly  # noqa: ARG001 — preserved for stats + future assembly range-check
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
        raise ValueError(f"{source}: {int(bad_alleles.sum())} rows with non-ACGT alleles")

    # Exact-duplicate dedup (within donor + tissue)
    before = len(df)
    df = df.drop_duplicates(subset=["donor_id", "tissue_label", "chrom", "pos", "ref", "alt"])
    n_dupes = before - len(df)

    return df.reset_index(drop=True), {
        "n_indels_dropped": n_indels,
        "n_mito_dropped": n_mito,
        "n_duplicates_collapsed": n_dupes,
    }


def _run_via_snakemake() -> None:
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821 F841
    # (Task 13 fills in the body)
    raise NotImplementedError("Wired up in Task 13")


if "snakemake" in globals():
    _run_via_snakemake()
