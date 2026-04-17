"""
build_panel_callable_sizes.py

Builds the per-panel callable-Mb registry that the t081 hypermutator / TMB annotation
pipeline consumes as its TMB denominator (see
``doc/plans/2026-04-13-t081-hypermutator-annotation-pipeline-plan.md`` task 1).

The output is a plain TSV at ``out_dir/metadata/panel_callable_mb.tsv`` with columns
``[panel_id, callable_mb, source]`` where ``source`` is one of:

- ``bed_sum``          — sum of exonic region lengths from the GENIE coverage feather.
- ``config_override``  — value from the ``panel_callable_mb_override`` config map.
- ``wes_default``      — fallback ``wes_default_callable_mb`` for panels with no BED
                         coverage and no override (used for studies whose panel identity
                         is unknown or for WES cohorts like MC3).

The TSV is a **generated build artifact** — not version-controlled. It is regenerated
whenever the GENIE coverage feather or the config-derived override map changes, via the
``build_panel_callable_sizes`` Snakemake rule declared in ``code/workflows/Snakefile``
(as a ``localrule`` so it runs locally and persists via normal DAG invalidation).

This registry is reusable beyond t081: it is consumed by t070 (panel-version drift),
t076 (NaN-vs-0 panel-aware aggregation), and t077 (GLMM-logit pooling as a study-level
covariate / offset).

Inputs
------
- snakemake.input[0] : ``out_dir/metadata/genie_panel_coverage.feather`` produced by
  ``process_genie_panel_coverage``. Schema: ``panel_id, gene, chromosome, start, end,
  length_bp, feature_type, included`` (see ``process_genie_panel_coverage.py``).

Config
------
- ``panel_callable_mb_override``: ``dict[str, float]`` — per-panel_id Mb override.
  Populated with the canonical published values for MSK-IMPACT-341/410/468/505,
  FoundationOne variants, Tempus xT, Caris MI, etc. Overrides always win; when a BED
  is also present, a warning is logged if the BED-derived size disagrees with the
  override by more than ``panel_callable_mb_tolerance`` (default 0.05 = 5%).
- ``wes_default_callable_mb``: float, default 30.0 — fallback used for panels with no
  BED coverage and no override.
- ``study_panel_map``: ``dict[study_id, panel_id]`` — used to enumerate the full set of
  panel IDs the run cares about so the registry has a row for every one of them,
  even if some have neither coverage nor override.
- ``panel_callable_mb_tolerance``: float, default 0.05 — ±5% agreement window between
  BED-derived sum and override; violations trigger a warning but do not change the
  output value.
"""


import logging
from typing import Iterable

import pandas as pd


logger = logging.getLogger("build_panel_callable_sizes")


SOURCE_BED_SUM = "bed_sum"
SOURCE_CONFIG_OVERRIDE = "config_override"
SOURCE_WES_DEFAULT = "wes_default"


def compute_callable_mb_table(
    coverage: pd.DataFrame,
    override_map: dict[str, float],
    wes_default_mb: float,
    required_panel_ids: Iterable[str],
    tolerance: float = 0.05,
) -> pd.DataFrame:
    """Return a ``[panel_id, callable_mb, source]`` DataFrame for each required panel.

    For each panel in ``required_panel_ids``:

    - if the panel is in ``override_map``, use the override value with
      ``source="config_override"``; if the panel is also present in ``coverage``, log
      a warning when the BED-derived sum disagrees with the override by more than
      ``tolerance``;
    - else if the panel has at least one exonic row in ``coverage``, sum
      ``length_bp`` across ``feature_type == "exon"`` rows and convert to Mb with
      ``source="bed_sum"``;
    - else fall back to ``wes_default_mb`` with ``source="wes_default"``.
    """
    bed_sums_mb = _bed_sums_mb(coverage)
    rows: list[dict[str, object]] = []
    for panel_id in required_panel_ids:
        if panel_id in override_map:
            override_value = float(override_map[panel_id])
            if panel_id in bed_sums_mb:
                _warn_if_out_of_tolerance(
                    panel_id, bed_sums_mb[panel_id], override_value, tolerance
                )
            rows.append(
                {
                    "panel_id": panel_id,
                    "callable_mb": override_value,
                    "source": SOURCE_CONFIG_OVERRIDE,
                }
            )
        elif panel_id in bed_sums_mb:
            rows.append(
                {
                    "panel_id": panel_id,
                    "callable_mb": bed_sums_mb[panel_id],
                    "source": SOURCE_BED_SUM,
                }
            )
        else:
            rows.append(
                {
                    "panel_id": panel_id,
                    "callable_mb": float(wes_default_mb),
                    "source": SOURCE_WES_DEFAULT,
                }
            )
    return pd.DataFrame(rows).reindex(columns=["panel_id", "callable_mb", "source"])


def _bed_sums_mb(coverage: pd.DataFrame) -> dict[str, float]:
    if coverage.empty:
        return {}
    exons = coverage.loc[coverage["feature_type"] == "exon"]
    if exons.empty:
        return {}
    by_panel = exons.groupby("panel_id")["length_bp"].sum().astype(float) / 1_000_000.0
    return by_panel.to_dict()


def _warn_if_out_of_tolerance(
    panel_id: str, bed_mb: float, override_mb: float, tolerance: float
) -> None:
    if override_mb == 0.0:
        return
    relative_delta = abs(bed_mb - override_mb) / override_mb
    if relative_delta > tolerance:
        logger.warning(
            "Panel %s BED-derived callable size %.4f Mb differs from config override "
            "%.4f Mb by %.1f%% (outside tolerance %.1f%%); using override.",
            panel_id,
            bed_mb,
            override_mb,
            relative_delta * 100.0,
            tolerance * 100.0,
        )


def _run_via_snakemake() -> None:
    """Entry point invoked when this module is imported by Snakemake."""
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821
    coverage = pd.read_feather(snek.input[0])
    override_map: dict[str, float] = dict(
        snek.config.get("panel_callable_mb_override", {})
    )
    wes_default_mb = float(snek.config.get("wes_default_callable_mb", 30.0))
    tolerance = float(snek.config.get("panel_callable_mb_tolerance", 0.05))
    study_panel_map: dict[str, str] = dict(snek.config.get("study_panel_map", {}))

    # Enumerate every panel we need a row for: declared via study_panel_map, explicitly
    # overridden, or seen in the BED.
    required = sorted(
        set(study_panel_map.values())
        | set(override_map.keys())
        | set(coverage["panel_id"].unique())
    )
    result = compute_callable_mb_table(
        coverage,
        override_map=override_map,
        wes_default_mb=wes_default_mb,
        required_panel_ids=required,
        tolerance=tolerance,
    )
    result.to_csv(snek.output[0], sep="\t", index=False)
    logger.info(
        "Wrote panel_callable_mb registry: %d panels (%d bed_sum, %d config_override, "
        "%d wes_default).",
        len(result),
        int((result["source"] == SOURCE_BED_SUM).sum()),
        int((result["source"] == SOURCE_CONFIG_OVERRIDE).sum()),
        int((result["source"] == SOURCE_WES_DEFAULT).sum()),
    )


if "snakemake" in globals():
    _run_via_snakemake()
