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
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

# Assay metadata constants. Sourced from Li 2021 Methods:
# SureSelectXT Human All Exon V6 (esophagus) or V7 (other tissues), callable ~60 Mb / ~48.2 Mb.
# Populated concretely in Task 5.
ASSAY_METADATA: dict[tuple[str, str | None], dict[str, object]] = {
    # Populated in Task 5.
}


def main() -> None:
    """Snakemake entry point. Not invoked directly — use `snakemake` CLI."""
    snek = snakemake  # type: ignore[name-defined]
    # Wired up in Task 13.
    raise NotImplementedError("Wired up in Task 13")


if __name__ == "__main__":
    main()
