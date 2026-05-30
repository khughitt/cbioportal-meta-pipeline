# science:code
# status: workflow-owned
# science:end
"""
combine_samples_tmb.py

Concatenate per-study ``samples_tmb.feather`` tables into a single cross-study
table and left-join per-study ``sample_polymerase_hotspots.feather`` flags onto
it. Feeds the GMM fit (t096) and the composite hypermutator flag (t097).

Missing hotspot rows map to ``False`` (not NaN) — per-sample absence from the
POLE/POLD1 detector output means the sample had no POLE or POLD1 mutation at
all, which is an explicit negative for both flags.

Inputs
------
- ``snakemake.input.samples_tmb``    : list of ``out_dir/studies/{id}/metadata/
  samples_tmb.feather`` (one per study).
- ``snakemake.input.pole_hotspots``  : list of ``out_dir/studies/{id}/metadata/
  sample_polymerase_hotspots.feather`` (one per study).

Output
------
- ``snakemake.output[0]`` : ``out_dir/metadata/samples_tmb_combined.feather``
"""


import pandas as pd


def combine_samples_tmb(
    per_study_tmb: list[pd.DataFrame],
    per_study_hotspots: list[pd.DataFrame],
) -> pd.DataFrame:
    """Concatenate per-study TMB tables and left-join POLE/POLD1 hotspot flags.

    Returns a single DataFrame with all per-study ``samples_tmb`` columns plus
    ``pole_hotspot_detected`` / ``pold1_hotspot_detected`` (bool, defaulting to
    False where the sample had no matching hotspot row).
    """
    if not per_study_tmb:
        empty = pd.DataFrame(
            {
                "study_id": pd.Series(dtype=object),
                "sample_id": pd.Series(dtype=object),
                "cancer_type": pd.Series(dtype=object),
                "tmb": pd.Series(dtype=float),
                "tmb_log10": pd.Series(dtype=float),
                "panel_callable_mb": pd.Series(dtype=float),
                "tmb_source": pd.Series(dtype=object),
                "pole_hotspot_detected": pd.Series(dtype=bool),
                "pold1_hotspot_detected": pd.Series(dtype=bool),
            }
        )
        return empty

    tmb = pd.concat(per_study_tmb, ignore_index=True)

    # Some studies (e.g. pog570_bcgsc_2020) store identifier columns as int64;
    # concat across mixed-dtype frames yields an object column that pyarrow
    # cannot serialize. Coerce all known identifier columns to str.
    for col in ("study_id", "sample_id", "patient_id", "cancer_type", "sample_id_tumor"):
        if col in tmb.columns:
            tmb[col] = tmb[col].astype(str)

    if per_study_hotspots:
        hotspots = pd.concat(per_study_hotspots, ignore_index=True)
    else:
        hotspots = pd.DataFrame(
            columns=[
                "sample_id_tumor",
                "pole_hotspot_detected",
                "pold1_hotspot_detected",
            ]
        )

    hotspots = hotspots.rename(columns={"sample_id_tumor": "sample_id"})
    out = tmb.merge(
        hotspots[["sample_id", "pole_hotspot_detected", "pold1_hotspot_detected"]],
        on="sample_id",
        how="left",
    )
    out["pole_hotspot_detected"] = (
        out["pole_hotspot_detected"].fillna(False).astype(bool)
    )
    out["pold1_hotspot_detected"] = (
        out["pold1_hotspot_detected"].fillna(False).astype(bool)
    )
    return out


def _run_via_snakemake() -> None:
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821
    per_study_tmb = [pd.read_feather(p) for p in snek.input.samples_tmb]
    per_study_hotspots = [pd.read_feather(p) for p in snek.input.pole_hotspots]
    out = combine_samples_tmb(per_study_tmb, per_study_hotspots)
    out.to_feather(snek.output[0])


if "snakemake" in globals():
    _run_via_snakemake()
