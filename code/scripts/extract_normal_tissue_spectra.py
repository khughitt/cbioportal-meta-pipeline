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

# Assay metadata constants. Sourced from Li 2021 Nature Methods section:
# SureSelectXT Human All Exon V6 (esophagus biopsies only, all donors) or V7
# (all other tissues, all donors). Agilent-published callable-target sizes:
# V6 ≈ 60 Mb, V7 ≈ 48.2 Mb.
#
# Keyed by (source, tissue_label) with (source, None) as the per-source fallback.
# Xu 2025 deferred to t112 per scope amendment.
ASSAY_METADATA: dict[tuple[str, str | None], dict[str, object]] = {
    ("li2021", "Esophagus"): {
        "sequencing_modality": "WES",
        "capture_kit_or_panel": "SureSelectXT V6",
        "callable_mb": 60.0,
    },
    ("li2021", None): {
        "sequencing_modality": "WES",
        "capture_kit_or_panel": "SureSelectXT V7",
        "callable_mb": 48.2,
    },
}


# Tuples (not sets) so pandas .isin() accepts them cleanly; _VALID_CHROMS_SET is for
# set-difference operations. Pandas accepts sets at runtime but its type stubs do not.
_VALID_CHROMS: tuple[str, ...] = tuple(
    f"chr{c}" for c in list(range(1, 23)) + ["X", "Y"]
)
_VALID_CHROMS_SET: frozenset[str] = frozenset(_VALID_CHROMS)
_MITO_CHROMS: tuple[str, ...] = ("chrM", "chrMT")
_VALID_BASES: tuple[str, ...] = ("A", "C", "G", "T")


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
    df["chrom"] = (
        df["chrom"].astype(str).apply(lambda c: c if c.startswith("chr") else f"chr{c}")
    )
    df["ref"] = df["ref"].astype(str)
    df["alt"] = df["alt"].astype(str)

    if df["alt"].str.contains(",").any():
        bad = int(df["alt"].str.contains(",").sum())
        raise ValueError(
            f"{source}: {bad} multi-allelic rows (alt contains ','); split upstream"
        )

    # Mitochondrial drop
    mito_mask = df["chrom"].isin(_MITO_CHROMS)
    n_mito = int(mito_mask.sum())
    df = df.loc[~mito_mask].copy()

    # Unknown chromosomes
    unknown = set(df["chrom"].unique()) - _VALID_CHROMS_SET
    if unknown:
        raise ValueError(f"{source}: unknown chromosome values {sorted(unknown)}")

    # Indel drop (ref or alt not length-1)
    indel_mask = (df["ref"].str.len() != 1) | (df["alt"].str.len() != 1)
    n_indels = int(indel_mask.sum())
    df = df.loc[~indel_mask].copy()

    # Non-ACGT rejection
    bad_alleles = ~(df["ref"].isin(_VALID_BASES) & df["alt"].isin(_VALID_BASES))
    if bad_alleles.any():
        raise ValueError(
            f"{source}: {int(bad_alleles.sum())} rows with non-ACGT alleles"
        )

    # Exact-duplicate dedup (within donor + tissue)
    before = len(df)
    df = df.drop_duplicates(
        subset=["donor_id", "tissue_label", "chrom", "pos", "ref", "alt"]
    )
    n_dupes = before - len(df)

    return df.reset_index(drop=True), {
        "n_indels_dropped": n_indels,
        "n_mito_dropped": n_mito,
        "n_duplicates_collapsed": n_dupes,
    }


def attach_uberon(df: pd.DataFrame, mapping_tsv: Path, source: str) -> pd.DataFrame:
    """Left-join `tissue_uberon` and `uberon_label` onto df keyed on (source, tissue_label).

    Raises ValueError listing any unmapped (source, tissue_label) pairs — no silent drops.
    """
    mapping = pd.read_csv(mapping_tsv, sep="\t", dtype=str, na_filter=False)
    mapping = mapping.loc[
        mapping["source"] == source, ["tissue_label", "tissue_uberon", "uberon_label"]
    ]

    out = df.merge(mapping, on="tissue_label", how="left", validate="many_to_one")
    unmapped = out.loc[out["tissue_uberon"].isna(), "tissue_label"].unique().tolist()
    if unmapped:
        raise ValueError(
            f"{source}: unmapped tissue_label values {sorted(unmapped)}. "
            f"Append to {mapping_tsv}."
        )
    return out


def attach_assay_metadata(df: pd.DataFrame, source: str) -> pd.DataFrame:
    """Attach sequencing_modality / capture_kit_or_panel / callable_mb columns
    keyed by (source, tissue_label), with (source, None) as the per-source fallback.

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


def _run_via_snakemake() -> None:
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821 F841
    # (Task 13 fills in the body)
    raise NotImplementedError("Wired up in Task 13")


if "snakemake" in globals():
    _run_via_snakemake()
