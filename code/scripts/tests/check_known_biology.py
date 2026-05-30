# science:code
# status: library
# science:end
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
    PositiveControl("KRAS", "BRAF", "luad", "ME", "Cerami 2012"),
    PositiveControl("KRAS", "NRAS", "coadread", "ME", "RAS-pathway redundancy"),
    PositiveControl("KRAS", "NRAS", "skcm", "ME", "RAS-pathway redundancy"),
    PositiveControl("IDH1", "IDH2", "gbm", "ME", "Yan 2009"),
    PositiveControl("IDH1", "IDH2", "lgg", "ME", "Yan 2009"),
    PositiveControl("APC", "CTNNB1", "coadread", "ME", "Wnt-pathway redundancy"),
    PositiveControl("BRAF", "NRAS", "skcm", "ME", "Davies 2002"),
    PositiveControl("EGFR", "KRAS", "luad", "ME", "Pao 2005"),
    PositiveControl("TP53", "KEAP1", "luad", "CO", "Sanchez-Vega 2018"),
    PositiveControl("STK11", "KEAP1", "luad", "CO", "Skoulidis 2018"),
    PositiveControl("IDH1", "ATRX", "lgg", "CO", "Brat 2015 TCGA LGG"),
]


def _lookup(headline: pd.DataFrame, ga: str, gb: str, ct: str) -> pd.Series | None:
    sub = headline[headline["cancer_type"] == ct]
    sub = sub[sub["cohort"] == "exclusive"]
    candidate = sub[
        ((sub["gene_i"] == ga) & (sub["gene_j"] == gb))
        | ((sub["gene_i"] == gb) & (sub["gene_j"] == ga))
    ]
    if candidate.empty:
        return None
    return candidate.iloc[0]


def check(headline: pd.DataFrame, controls: list[PositiveControl] = CONTROLS) -> int:
    failures = 0
    for c in controls:
        row = _lookup(headline, c.gene_a, c.gene_b, c.cancer_type)
        if row is None:
            console.print(
                f"[yellow]SKIP[/yellow] {c.gene_a}<->{c.gene_b} in {c.cancer_type}: "
                "pair not in headline (likely panel intersection or prevalence floor)"
            )
            continue
        if pd.isna(row["b_n_samples"]) or row["b_n_samples"] < 30:
            console.print(
                f"[yellow]SKIP[/yellow] {c.gene_a}<->{c.gene_b} in {c.cancer_type}: "
                f"insufficient samples (n={row.get('b_n_samples')})"
            )
            continue
        q = row["b_q_wMI_within_stratum"]
        d = row["b_direction"]
        if pd.isna(q) or q >= 0.10:
            console.print(
                f"[red]FAIL[/red] {c.gene_a}<->{c.gene_b} in {c.cancer_type}: "
                f"q={q!r} expected <0.10. ({c.citation})"
            )
            failures += 1
            continue
        if d != c.expected_direction:
            console.print(
                f"[red]FAIL[/red] {c.gene_a}<->{c.gene_b} in {c.cancer_type}: "
                f"direction={d!r} expected {c.expected_direction!r}. ({c.citation})"
            )
            failures += 1
            continue
        console.print(
            f"[green]PASS[/green] {c.gene_a}<->{c.gene_b} in {c.cancer_type}: "
            f"q={q:.4f} direction={d}"
        )
    return failures


if __name__ == "__main__":
    import sys

    headline_path = (
        Path(sys.argv[1])
        if len(sys.argv) > 1
        else Path("results/select/gene_pair_select.feather")
    )
    headline = pd.read_feather(headline_path)
    n_failures = check(headline)
    sys.exit(1 if n_failures else 0)
