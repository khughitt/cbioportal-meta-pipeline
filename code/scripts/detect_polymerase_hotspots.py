"""
detect_polymerase_hotspots.py

POLE / POLD1 hotspot detector for the t081 hypermutator / TMB annotation pipeline
(see ``doc/plans/2026-04-13-t081-hypermutator-annotation-pipeline-plan.md`` task 3).

For each per-study mutation table, emit a per-sample boolean flag pair:

- ``pole_hotspot_detected`` — True iff the sample carries at least one mutation
  whose ``(symbol, hgvsp_short stripped of "p.")`` pair matches the canonical
  POLE hotspot set below.
- ``pold1_hotspot_detected`` — analogous for POLD1.

These flags feed deterministic rows 1 / 2 of the composite-score decision table in
Task 6 (``annotate_hypermutators``): a positive POLE or POLD1 hotspot forces
``is_hypermutator = True`` regardless of TMB, because clinical pathology treats
POLE-hypermutated endometrial cancer as a molecular-subtype diagnosis in its own
right (TCGA 2013 CRC / Cancer Genome Atlas 2013 UCEC).

Hotspot sets — literature-curated, not exhaustive. See Campbell 2017 (Cell),
Rayner 2016, Ma 2018.

Inputs
------
- ``snakemake.input[0]`` : ``out_dir/studies/{id}/mut/table/mut.feather`` — the
  raw per-study mutation table (before gene-coverage filtering, so that rare but
  real POLE/POLD1 mutations in less-sampled genes are not dropped upstream).

Output
------
- ``snakemake.output[0]`` : ``out_dir/studies/{id}/metadata/sample_polymerase_hotspots.feather``
  with columns ``[sample_id_tumor, pole_hotspot_detected, pold1_hotspot_detected]``.
  One row per sample that has at least one mutation in POLE or POLD1 in the input
  (samples with neither are absent; the downstream composite step treats their
  absence as ``False`` via a left join).
"""


import pandas as pd


POLE_HOTSPOTS: frozenset[str] = frozenset(
    {"P286R", "V411L", "S297F", "S459F", "A456P", "L424V", "M295V", "F367L"}
)
POLD1_HOTSPOTS: frozenset[str] = frozenset(
    {"P327L", "R689W", "S478N", "L474P", "D316H", "D316N"}
)


_OUTPUT_COLUMNS = [
    "sample_id_tumor",
    "pole_hotspot_detected",
    "pold1_hotspot_detected",
]


def detect_hotspots_per_sample(mutations: pd.DataFrame) -> pd.DataFrame:
    """Return a per-sample ``[sample_id_tumor, pole_hotspot_detected,
    pold1_hotspot_detected]`` DataFrame.

    Only samples that carry at least one POLE or POLD1 mutation (hotspot or not)
    appear in the output. Samples with no polymerase mutations are omitted;
    downstream consumers should left-join this table onto the authoritative
    per-study samples table and treat NaN as ``False``.

    Matching is gated on ``symbol`` (must be one of ``{"POLE", "POLD1"}``) and
    is a case-sensitive exact match of the amino-acid change after stripping the
    ``p.`` prefix from ``hgvsp_short``.
    """
    polymerase_rows = mutations.loc[
        mutations["symbol"].astype(str).isin(["POLE", "POLD1"])
    ].copy()
    if polymerase_rows.empty:
        empty = pd.DataFrame(
            {
                "sample_id_tumor": pd.Series(dtype=object),
                "pole_hotspot_detected": pd.Series(dtype=bool),
                "pold1_hotspot_detected": pd.Series(dtype=bool),
            }
        )
        return empty.reindex(columns=_OUTPUT_COLUMNS)

    aa_change = polymerase_rows["hgvsp_short"].astype("string").str.removeprefix("p.")
    is_pole_hotspot = (
        polymerase_rows["symbol"].astype(str) == "POLE"
    ) & aa_change.isin(list(POLE_HOTSPOTS))
    is_pold1_hotspot = (
        polymerase_rows["symbol"].astype(str) == "POLD1"
    ) & aa_change.isin(list(POLD1_HOTSPOTS))

    polymerase_rows["_is_pole_hs"] = is_pole_hotspot.fillna(False)
    polymerase_rows["_is_pold1_hs"] = is_pold1_hotspot.fillna(False)

    grouped = (
        polymerase_rows.groupby("sample_id_tumor", observed=True)
        .agg(
            pole_hotspot_detected=("_is_pole_hs", "any"),
            pold1_hotspot_detected=("_is_pold1_hs", "any"),
        )
        .reset_index()
    )
    grouped["pole_hotspot_detected"] = grouped["pole_hotspot_detected"].astype(bool)
    grouped["pold1_hotspot_detected"] = grouped["pold1_hotspot_detected"].astype(bool)
    return grouped.reindex(columns=_OUTPUT_COLUMNS)


def _run_via_snakemake() -> None:
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821
    muts = pd.read_feather(snek.input[0])
    out = detect_hotspots_per_sample(muts)
    out.to_feather(snek.output[0])


if "snakemake" in globals():
    _run_via_snakemake()
