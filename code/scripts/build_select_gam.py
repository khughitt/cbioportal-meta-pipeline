"""Rule (2): build per-cell SELECT inputs (GAM + sample.class + alteration.class).

See doc/plans/2026-04-25-t078-select-cooccurrence-design.md Section 4.4.
"""

import json
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

import select_lib as lib


@dataclass(frozen=True, slots=True)
class Thresholds:
    min_stratum_samples: int
    min_gene_prevalence_frac: float
    min_gene_prevalence_count: int
    study_residual_threshold_frac: float


SKIP_INSUFFICIENT_SAMPLES = "n_samples_below_threshold"
SKIP_INSUFFICIENT_GENES = "insufficient_genes"
MIN_GENES_FOR_SELECT = 5  # Hard floor; SELECT below this is uninformative.


def _write_cell_outputs(
    out_dir: Path,
    gam: pd.DataFrame,
    sample_class: pd.DataFrame,
    alteration_class: pd.DataFrame,
    metadata: dict,
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    gam.to_feather(out_dir / "gam.feather")
    sample_class.to_feather(out_dir / "sample_class.feather")
    alteration_class.to_feather(out_dir / "alteration_class.feather")
    (out_dir / "cell_metadata.json").write_text(json.dumps(metadata, indent=2))


def _empty_outputs(out_dir: Path, skip_reason: str, n_samples: int = 0) -> None:
    """Write zero-row placeholder feathers + a populated cell_metadata.json."""
    gam = pd.DataFrame({"composite_sample_id": pd.Series(dtype="string")})
    sample_class = pd.DataFrame(
        {
            "composite_sample_id": pd.Series(dtype="string"),
            "sample_class": pd.Series(dtype="string"),
        }
    )
    alteration_class = pd.DataFrame(
        {
            "symbol": pd.Series(dtype="string"),
            "alteration_class": pd.Series(dtype="string"),
        }
    )
    metadata = {
        "skip_reason": skip_reason,
        "n_samples": n_samples,
        "n_genes": 0,
        "panel_intersection_size": 0,
    }
    _write_cell_outputs(out_dir, gam, sample_class, alteration_class, metadata)


def _intersect_panel_genes(
    panel_ids_in_cell: pd.Series,
    panel_gene_sets: dict[str, pd.DataFrame],
) -> set[str]:
    """Return symbols callable on every panel present in the cell."""
    unique_panels = panel_ids_in_cell.drop_duplicates().tolist()
    if not unique_panels:
        return set()
    sets = []
    for pid in unique_panels:
        if pid not in panel_gene_sets:
            raise KeyError(f"panel_gene_sets missing entry for panel_id={pid!r}")
        ps = panel_gene_sets[pid]
        sets.append(set(ps.loc[ps["callable"], "symbol"]))
    return set.intersection(*sets)


def _bucket_residual_studies(
    sample_class: pd.Series,
    threshold_frac: float,
) -> pd.Series:
    """Fold studies contributing < threshold_frac of samples into 'study_residual'."""
    counts = sample_class.value_counts()
    n = counts.sum()
    big = counts[counts / n >= threshold_frac].index
    return sample_class.where(sample_class.isin(big), other="study_residual")


def build_b_tier_cell(
    cancer_type: str,
    cohort: str,
    samples: pd.DataFrame,
    mutation_long: pd.DataFrame,
    sample_panel_map: pd.DataFrame,
    panel_gene_sets: dict[str, pd.DataFrame],
    gene_universe: pd.DataFrame,
    ch_priority_genes: set[str],
    sample_class_components: list[str],
    thresholds: Thresholds,
    out_dir: Path,
    bailey_alteration_class: pd.DataFrame | None = None,
) -> None:
    """Build one B-tier cell (cancer_type, cohort) of the SELECT input layer.

    samples:               (study_id, sample_id, composite_sample_id, cancer_type,
                            is_hypermutator, ...)
    mutation_long:         (composite_sample_id, symbol)
    sample_panel_map:      (study_id, sample_id, panel_id, panel_source)
    panel_gene_sets:       dict panel_id -> DataFrame(symbol, callable, ...)
    gene_universe:         result of rule (1b) build_select_gene_universe.
    ch_priority_genes:     boolean filter for cohort=='exclusive'.
    sample_class_components: ["study_id"] in MVP; t135 will add age_tertile.
    """
    cohort_samples = samples[samples["cancer_type"] == cancer_type]
    if cohort == "exclusive":
        cohort_samples = cohort_samples[~cohort_samples["is_hypermutator"]]

    n_samples = len(cohort_samples)
    if n_samples < thresholds.min_stratum_samples:
        _empty_outputs(out_dir, SKIP_INSUFFICIENT_SAMPLES, n_samples=n_samples)
        return

    # Determine panel intersection across the cell's samples.
    sp = sample_panel_map.merge(
        cohort_samples[["study_id", "sample_id"]],
        on=["study_id", "sample_id"],
        how="inner",
        validate="one_to_one",
    )
    callable_genes = _intersect_panel_genes(sp["panel_id"], panel_gene_sets)

    # Restrict to gene universe.
    universe_set = set(gene_universe["symbol"])
    candidate_genes = callable_genes & universe_set
    if cohort == "exclusive":
        candidate_genes -= ch_priority_genes

    # Build wide GAM in samples x candidate_genes.
    sample_ids = cohort_samples["composite_sample_id"].tolist()
    relevant = mutation_long[mutation_long["symbol"].isin(candidate_genes)]
    relevant = relevant[relevant["composite_sample_id"].isin(sample_ids)]
    gam_long = relevant.assign(value=True)
    gam = (
        gam_long.pivot_table(
            index="composite_sample_id",
            columns="symbol",
            values="value",
            fill_value=False,
            aggfunc="any",
        )
        .reindex(index=sample_ids, columns=sorted(candidate_genes))
        .fillna(False)
        .astype(bool)
    )
    gam.index.name = "composite_sample_id"

    # Prevalence floor.
    counts = gam.sum(axis=0)
    fracs = counts / n_samples
    keep_genes = (
        (counts >= thresholds.min_gene_prevalence_count)
        & (fracs >= thresholds.min_gene_prevalence_frac)
        & (counts < n_samples)  # drop fully-mutated
    )
    gam = gam.loc[:, keep_genes[keep_genes].index]

    if gam.shape[1] < MIN_GENES_FOR_SELECT:
        _empty_outputs(out_dir, SKIP_INSUFFICIENT_GENES, n_samples=n_samples)
        return

    # sample.class
    cohort_samples = cohort_samples.set_index("composite_sample_id", drop=False)
    sample_class = lib.build_sample_class(
        cohort_samples, components=sample_class_components
    )
    sample_class = _bucket_residual_studies(
        sample_class, thresholds.study_residual_threshold_frac
    )

    sample_class_df = pd.DataFrame(
        {
            "composite_sample_id": sample_class.index,
            "sample_class": sample_class.values.astype(str),
        }
    )

    # alteration.class -- Bailey-derived if provided, else 'unknown'.
    if bailey_alteration_class is not None:
        cls_lookup = bailey_alteration_class.set_index("symbol")["alteration_class"]
        alteration_class_series = (
            pd.Series(gam.columns).map(cls_lookup).fillna("unknown")
        )
    else:
        alteration_class_series = pd.Series(["unknown"] * gam.shape[1])
    alteration_class_df = pd.DataFrame(
        {
            "symbol": gam.columns.astype(str),
            "alteration_class": alteration_class_series.astype(str).values,
        }
    )

    metadata = {
        "skip_reason": None,
        "n_samples": int(n_samples),
        "n_genes": int(gam.shape[1]),
        "panel_intersection_size": int(len(callable_genes)),
        "panels_in_cell": sorted(set(sp["panel_id"])),
        "studies_in_cell": sorted(set(cohort_samples["study_id"])),
    }

    # Reset the index so feather can write it cleanly.
    gam_out = gam.reset_index()
    _write_cell_outputs(
        out_dir, gam_out, sample_class_df, alteration_class_df, metadata
    )


def build_a_tier_cell(
    cancer_type: str,
    cohort: str,
    study: str,
    samples: pd.DataFrame,
    mutation_long: pd.DataFrame,
    sample_panel_map: pd.DataFrame,
    panel_gene_sets: dict[str, pd.DataFrame],
    gene_universe: pd.DataFrame,
    ch_priority_genes: set[str],
    sample_class_components: list[str],
    thresholds: Thresholds,
    out_dir: Path,
    bailey_alteration_class: pd.DataFrame | None = None,
) -> None:
    """Same as build_b_tier_cell but pre-filtered to a single study."""
    sub = samples[samples["study_id"] == study].copy()
    build_b_tier_cell(
        cancer_type=cancer_type,
        cohort=cohort,
        samples=sub,
        mutation_long=mutation_long,
        sample_panel_map=sample_panel_map,
        panel_gene_sets=panel_gene_sets,
        gene_universe=gene_universe,
        ch_priority_genes=ch_priority_genes,
        sample_class_components=sample_class_components,
        thresholds=thresholds,
        out_dir=out_dir,
        bailey_alteration_class=bailey_alteration_class,
    )


if "snakemake" in globals():  # pragma: no cover  # set by Snakemake's script: directive
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821

    cancer_type = snek.wildcards["cancer_type"]
    tier = snek.wildcards["tier"]  # 'B' or 'A'
    cohort = snek.wildcards["cohort"]  # 'inclusive' or 'exclusive'
    study = snek.wildcards.get("study")  # only for tier == 'A'

    samples = pd.read_feather(snek.input["samples_annotated"])
    mutation_long = pd.read_feather(snek.input["mutation_long"])
    sample_panel_map = pd.read_feather(snek.input["sample_panel_map"])
    gene_universe = pd.read_csv(snek.input["gene_universe"], sep="\t")

    panel_gene_sets: dict[str, pd.DataFrame] = {}
    for path in snek.input["panel_gene_sets"]:
        df = pd.read_feather(path)
        if df.empty:
            continue
        pid = df["panel_id"].iloc[0]
        panel_gene_sets[pid] = df

    bailey = (
        pd.read_feather(snek.input["bailey_alteration_class"])
        if "bailey_alteration_class" in snek.input.keys()
        else None
    )

    ch_genes = set(snek.params.get("ch_priority_genes", []))
    sc_components = list(snek.params["sample_class_components"])
    thresholds = Thresholds(**snek.params["thresholds"])
    out_dir_path = Path(snek.output["cell_dir"])

    if tier == "B":
        build_b_tier_cell(
            cancer_type=cancer_type,
            cohort=cohort,
            samples=samples,
            mutation_long=mutation_long,
            sample_panel_map=sample_panel_map,
            panel_gene_sets=panel_gene_sets,
            gene_universe=gene_universe,
            ch_priority_genes=ch_genes,
            sample_class_components=sc_components,
            thresholds=thresholds,
            out_dir=out_dir_path,
            bailey_alteration_class=bailey,
        )
    elif tier == "A":
        if study is None:
            raise ValueError("A-tier cells require a 'study' wildcard")
        build_a_tier_cell(
            cancer_type=cancer_type,
            cohort=cohort,
            study=study,
            samples=samples,
            mutation_long=mutation_long,
            sample_panel_map=sample_panel_map,
            panel_gene_sets=panel_gene_sets,
            gene_universe=gene_universe,
            ch_priority_genes=ch_genes,
            sample_class_components=sc_components,
            thresholds=thresholds,
            out_dir=out_dir_path,
            bailey_alteration_class=bailey,
        )
    else:
        raise ValueError(f"unknown tier: {tier!r}")
