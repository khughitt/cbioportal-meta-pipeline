# science:code
# status: workflow-owned
# science:end
"""
compute_per_sample_tmb.py

Per-sample TMB computation for the t081 hypermutator / TMB annotation pipeline
(see ``doc/plans/2026-04-13-t081-hypermutator-annotation-pipeline-plan.md`` task 2).

For a single study, compute per-sample:
- ``mutation_count`` — number of protein-altering mutations (Assumption 3 variant-class set)
- ``tmb`` — mutation_count / panel_callable_mb
- ``tmb_log10`` — log10(tmb + 1), chosen for zero-safety and comparability with the GMM
  fitting step downstream (Task 5)
- ``panel_callable_mb`` — the Mb denominator used (provenance column)
- ``tmb_source`` — the provenance category of that denominator: ``bed_sum`` /
  ``config_override`` / ``wes_default`` (propagated from ``panel_callable_mb.tsv``)
- ``study_id`` — the study this sample belongs to (F3 fix: every sample-level artifact
  must carry study_id as a first-class column for downstream cross-study joins)

Zero-mutation samples are preserved via a left join back to ``samples.feather``; the
samples table is authoritative for which sample IDs exist in the cohort.

Inputs
------
- ``snakemake.input.muts``    : ``out_dir/studies/{id}/mut/table/mut_filtered.feather``
  (per-study filtered mutation calls; output of the ``filter_genes`` rule)
- ``snakemake.input.samples`` : ``out_dir/studies/{id}/metadata/samples.feather``
  (per-study sample metadata)
- ``snakemake.input.panels``  : ``out_dir/metadata/panel_callable_mb.tsv`` (registry
  produced by ``build_panel_callable_sizes``)

Wildcards
---------
- ``{id}`` — the study ID being processed; propagated to the ``study_id`` column.

Config
------
- ``study_panel_map`` — ``dict[study_id, panel_id]``. If the current study has an entry,
  look up the panel's row in the registry and use its ``callable_mb`` / ``source``. If
  the study is unmapped, fall back to the ``wes_default`` row (a synthetic "WES"
  panel_id guaranteed to be in the registry because ``build_panel_callable_sizes``
  already materializes the fallback for unknown panels). If neither exists, hard-fall
  back to the in-script constants defined below.
- ``wes_default_callable_mb`` — fallback Mb (default 30.0) used when the registry has
  no ``wes_default`` row to look up (registry should always have one, but we defend).

Output
------
- ``snakemake.output[0]`` : ``out_dir/studies/{id}/metadata/samples_tmb.feather`` —
  NEW FILE; does NOT overwrite ``samples.feather`` so downstream consumers opt in.
"""

import logging
import math
from collections.abc import Iterable

import pandas as pd


logger = logging.getLogger("compute_per_sample_tmb")


# Assumption 3 (plan) — the protein-altering variant-class set used as the TMB numerator.
# Matches Chalmers 2017 F1CDx / FMI convention: missense, nonsense, frame-shift, in-frame
# indel, splice-site, translation-start, nonstop. Everything else (silent, intron, UTRs,
# RNA, IGR, flanks) is excluded.
PROTEIN_ALTERING_VARIANT_CLASSES: frozenset[str] = frozenset(
    {
        "Missense_Mutation",
        "Nonsense_Mutation",
        "Frame_Shift_Del",
        "Frame_Shift_Ins",
        "In_Frame_Del",
        "In_Frame_Ins",
        "Splice_Site",
        "Translation_Start_Site",
        "Nonstop_Mutation",
    }
)


_HUGE_MUT_COUNT_WARN_THRESHOLD = 5_000


def _check_no_duplicate_sample_ids(samples: pd.DataFrame, study_id: str) -> None:
    """Pipeline invariant: samples.feather must have unique sample_id values.

    Without this, ``Series.map()`` calls downstream raise ``InvalidIndexError``
    with no diagnostic context. Fail-loud here with a useful error.
    """
    if samples["sample_id"].duplicated().any():
        dups = (
            samples.loc[samples["sample_id"].duplicated(keep=False), "sample_id"]
            .unique()
            .tolist()
        )
        raise ValueError(
            f"Study {study_id!r}: samples table has duplicate sample_id values: "
            f"{dups[:10]!r}. Deduplicate upstream."
        )


def assert_panel_bearing_resolved(
    samples: pd.DataFrame,
    study_id: str,
    panel_bearing_studies: Iterable[str],
) -> None:
    """Fail-loud guard: a declared panel-bearing study MUST carry per-sample panel_id.

    A study listed in ``config['panel_bearing_studies']`` is panel-sequenced, so its TMB
    denominator must come from the per-sample panel_id (e.g. MSK-IMPACT-341/410). If the
    ``panel_id`` column is missing or all-null, ``compute_tmb_for_study`` would silently
    take the legacy study-level path and apply ``wes_default_callable_mb`` (~30 Mb) — a
    ~25x-too-large denominator that makes panel TMB ~25x too small and silently disables
    hypermutator detection for the whole study (the t226/2026-06-07 stale-artifact bug).
    Fail early instead of producing wrong-but-plausible TMB.
    """
    if study_id not in set(panel_bearing_studies):
        return
    if "panel_id" not in samples.columns or not samples["panel_id"].notna().any():
        raise ValueError(
            f"Study {study_id!r} is declared panel-bearing (config['panel_bearing_studies']) "
            "but its samples table has no usable per-sample 'panel_id'. The TMB denominator "
            "would silently fall back to wes_default (~30 Mb), ~25x too large for a targeted "
            "panel. Ensure convert_to_feather attached panel_id from "
            f"data_dir/{study_id}/data_gene_panel_matrix.txt, or remove {study_id!r} from "
            "panel_bearing_studies if it is genuinely WES."
        )


def compute_tmb_for_study(
    mutations: pd.DataFrame,
    samples: pd.DataFrame,
    study_id: str,
    panel_callable_mb: float | pd.Series,
    panel_source: str | pd.Series,
) -> pd.DataFrame:
    """Return a per-sample TMB table for a single study.

    Input schemas:
    - ``mutations`` must have at least ``sample_id_tumor`` and ``variant_class``.
    - ``samples`` must have at least ``sample_id``. Additional columns are preserved.

    ``panel_callable_mb`` and ``panel_source`` may each be either a scalar (existing
    per-study path) or a ``pd.Series`` indexed by ``sample_id`` (t070 per-sample path).

    Output columns (samples left-joined with per-sample mutation aggregates):
    all columns from ``samples``, plus ``study_id``, ``mutation_count``, ``tmb``,
    ``tmb_log10``, ``panel_callable_mb``, ``tmb_source``.
    """
    if not isinstance(panel_callable_mb, pd.Series) and panel_callable_mb <= 0.0:
        raise ValueError(
            f"panel_callable_mb must be positive; got {panel_callable_mb!r}"
        )

    # Filter to protein-altering and count per sample.
    protein_altering = mutations.loc[
        mutations["variant_class"]
        .astype(str)
        .isin(list(PROTEIN_ALTERING_VARIANT_CLASSES))
    ]
    counts = (
        protein_altering.groupby("sample_id_tumor", observed=True)
        .size()
        .rename("mutation_count")
        .reset_index()
        .rename(columns={"sample_id_tumor": "sample_id"})
    )

    # Left-join onto the authoritative samples table so zero-mutation samples survive
    # and phantom sample_id_tumor values in the mutation table are discarded.
    out = samples.merge(counts, on="sample_id", how="left")
    out["mutation_count"] = out["mutation_count"].fillna(0).astype(int)

    if isinstance(panel_callable_mb, pd.Series):
        # Per-sample path (t070): align by sample_id.
        mb_aligned = out["sample_id"].map(panel_callable_mb).astype(float)
        out["panel_callable_mb"] = mb_aligned
        out["tmb"] = out["mutation_count"].astype(float) / mb_aligned
    else:
        out["panel_callable_mb"] = float(panel_callable_mb)
        out["tmb"] = out["mutation_count"].astype(float) / float(panel_callable_mb)

    out["tmb_log10"] = out["tmb"].apply(lambda v: math.log10(v + 1.0))

    if isinstance(panel_source, pd.Series):
        out["tmb_source"] = out["sample_id"].map(panel_source).astype(str)
    else:
        out["tmb_source"] = str(panel_source)

    out["study_id"] = study_id

    _warn_on_huge_mutation_counts(out, study_id)
    return out


def _warn_on_huge_mutation_counts(df: pd.DataFrame, study_id: str) -> None:
    huge = df.loc[df["mutation_count"] > _HUGE_MUT_COUNT_WARN_THRESHOLD]
    if not huge.empty:
        sample_ids = huge["sample_id"].tolist()
        logger.warning(
            "Study %s has %d sample(s) with mutation_count > %d (likely CH-contaminated "
            "tumor-only or corrupted counts; worth investigating): %s",
            study_id,
            len(huge),
            _HUGE_MUT_COUNT_WARN_THRESHOLD,
            sample_ids[:10] + (["..."] if len(sample_ids) > 10 else []),
        )


def resolve_panel_for_study(
    study_id: str,
    study_panel_map: dict[str, str],
    panel_registry: pd.DataFrame,
    wes_default_callable_mb: float,
) -> tuple[float, str]:
    """Resolve ``(panel_callable_mb, panel_source)`` for a single study.

    Lookup order:
    1. If ``study_id`` is in ``study_panel_map``, find the panel row in the registry
       and return its ``callable_mb`` / ``source``.
    2. Else if the registry has a row for a ``wes_default`` source, return it.
    3. Else hard-fall back to ``wes_default_callable_mb`` with source ``wes_default``.
    """
    panel_id = study_panel_map.get(study_id)
    if panel_id is not None:
        matches = panel_registry.loc[panel_registry["panel_id"] == panel_id]
        if not matches.empty:
            row = matches.iloc[0]
            return float(row["callable_mb"]), str(row["source"])
        logger.warning(
            "Study %s maps to panel %r which is absent from panel_callable_mb registry; "
            "falling back to WES default.",
            study_id,
            panel_id,
        )

    wes_matches = panel_registry.loc[panel_registry["source"] == "wes_default"]
    if not wes_matches.empty:
        return float(wes_matches.iloc[0]["callable_mb"]), "wes_default"
    return float(wes_default_callable_mb), "wes_default"


def resolve_panel_for_sample(
    sample_panel_id: str | None,
    study_id: str,
    study_panel_map: dict[str, str],
    panel_registry: pd.DataFrame,
    wes_default_callable_mb: float,
) -> tuple[float, str]:
    """Per-sample callable-Mb lookup (t070).

    Lookup order:
      1. ``sample_panel_id`` (from samples.panel_id column) → panel registry
      2. ``study_panel_map[study_id]`` → panel registry (legacy / non-MSK panel studies)
      3. registry ``wes_default`` row
      4. ``wes_default_callable_mb`` literal

    Step 1 fails-loud (raises) if ``sample_panel_id`` is non-null but absent from
    the registry — t070 design Error Handling #3.
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

    # Fall through to existing study-level resolution.
    return resolve_panel_for_study(
        study_id,
        study_panel_map,
        panel_registry,
        wes_default_callable_mb,
    )


def _run_via_snakemake() -> None:
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821
    muts = pd.read_feather(snek.input.muts)
    samples = pd.read_feather(snek.input.samples)
    panel_registry = pd.read_csv(snek.input.panels, sep="\t")

    study_id = str(snek.wildcards.id)
    # t070: deduplication is a pipeline invariant; fail-loud with diagnostic if violated
    # (otherwise downstream Series.map() raises InvalidIndexError with no context).
    _check_no_duplicate_sample_ids(samples, study_id)
    assert_panel_bearing_resolved(
        samples, study_id, snek.config.get("panel_bearing_studies", [])
    )
    study_panel_map: dict[str, str] = dict(snek.config.get("study_panel_map", {}))
    wes_default_mb = float(snek.config.get("wes_default_callable_mb", 30.0))

    if "panel_id" in samples.columns and samples["panel_id"].notna().any():
        # Per-sample lookup (t070 path).
        lookups = samples["panel_id"].apply(
            lambda pid: resolve_panel_for_sample(
                pid,
                study_id,
                study_panel_map,
                panel_registry,
                wes_default_mb,
            )
        )
        panel_mb: float | pd.Series = pd.Series(
            [v[0] for v in lookups],
            index=samples["sample_id"].to_numpy(),
            name="panel_callable_mb",
        )
        panel_source: str | pd.Series = pd.Series(
            [v[1] for v in lookups],
            index=samples["sample_id"].to_numpy(),
            name="tmb_source",
        )
    else:
        # Legacy per-study scalar path (preserves existing behaviour for WES studies).
        panel_mb, panel_source = resolve_panel_for_study(
            study_id, study_panel_map, panel_registry, wes_default_mb
        )

    out = compute_tmb_for_study(
        muts,
        samples,
        study_id=study_id,
        panel_callable_mb=panel_mb,
        panel_source=panel_source,
    )
    out.to_feather(snek.output[0])
    median_tmb = float(out["tmb"].median())
    if isinstance(panel_mb, pd.Series):
        logger.info(
            "Study %s: %d samples, median TMB = %.2f mut/Mb (per-sample panel_id path)",
            study_id,
            len(out),
            median_tmb,
        )
    else:
        logger.info(
            "Study %s: %d samples, median TMB = %.2f mut/Mb (panel %s = %.3f Mb, source=%s)",
            study_id,
            len(out),
            median_tmb,
            study_panel_map.get(study_id, "<WES-default>"),
            panel_mb,
            panel_source,
        )


if "snakemake" in globals():
    _run_via_snakemake()
