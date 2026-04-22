"""
build_pooled_gene_cancer_input.py

Builds the long-format per-(study, cancer, gene) table that the t077 GLMM-logit
meta-analysis consumes.

The pooled input is derived from the per-study ``gene_cancer_study.feather`` artifacts
because those already encode the paired inclusive/exclusive mutation counts and their
callability-aware denominators. WES studies emit sparse per-study tables, so this adapter
reuses the t076 missing-cell semantics:

- WES / unmapped studies: a missing `(cancer, gene)` row means callable-but-unmutated if
  the cancer exists in that study cohort, so emit zero-event rows with the cancer-level
  denominator.
- Panel-restricted studies (`study_panel_map` or `panel_bearing_studies`): missing rows
  remain absent because they can still mean "gene not callable".
"""

from pathlib import Path
from typing import Literal

import pandas as pd

from create_combined_gene_cancer_freq_table import (
    _fill_missing_unmutated_cells,
    _load_cancer_presence,
    _study_id_from_path,
    combine_paired_pivot,
)


type PanelClass = Literal["large_hybrid_capture", "small_amplicon", "WES", "MC3"]

PANEL_CLASS_LARGE = "large_hybrid_capture"
PANEL_CLASS_SMALL = "small_amplicon"
PANEL_CLASS_WES = "WES"
PANEL_CLASS_MC3 = "MC3"

_LARGE_PANEL_MARKERS = (
    "MSK-IMPACT",
    "MSKIMPACT",
    "FOUNDATIONONE",
    "FOUNDATION-ONE",
    "F1CDX",
    "F1CD",
    "TEMPUS",
    "CARIS",
)
_SMALL_PANEL_MARKERS = ("AMPLICON", "HOTSPOT", "HOT-SPOT", "TRUSIGHT", "TSACP")


def build_pooled_input(
    *,
    per_study_frames: list[tuple[str, pd.DataFrame]],
    cancer_presence_by_study: dict[str, dict[str, tuple[int, int]]],
    matched_normal_studies: set[str],
    study_panel_map: dict[str, str],
    panel_bearing_studies: set[str] | None = None,
    sample_panel_ids_by_study: dict[str, set[str]] | None = None,
    study_panel_class_map: dict[str, PanelClass] | None = None,
) -> pd.DataFrame:
    """Return one long-format row per callable ``(study_id, cancer_type, symbol)``."""
    panel_bearing_studies = panel_bearing_studies or set()
    sample_panel_ids_by_study = sample_panel_ids_by_study or {}
    study_panel_class_map = study_panel_class_map or {}

    num_df, ratio_df, n_inclusive_df, n_exclusive_df = combine_paired_pivot(per_study_frames)
    num_df, ratio_df, n_inclusive_df, n_exclusive_df = _fill_missing_unmutated_cells(
        num_df,
        ratio_df,
        n_inclusive_df,
        n_exclusive_df,
        cancer_presence_by_study=cancer_presence_by_study,
        study_panel_map=study_panel_map,
        panel_bearing_studies=panel_bearing_studies,
    )

    out_frames: list[pd.DataFrame] = []
    for study_id, _ in per_study_frames:
        if study_id not in num_df.columns or study_id not in n_inclusive_df.columns:
            continue

        study_df = pd.DataFrame(
            {
                "y_inclusive": num_df[study_id],
                "y_exclusive": num_df[f"{study_id}_exclusive"],
                "n_inclusive": n_inclusive_df[study_id],
                "n_exclusive": n_exclusive_df[study_id],
            }
        ).reset_index()
        study_df = study_df.loc[study_df["n_inclusive"].notna()].copy()
        if study_df.empty:
            continue

        study_df[["y_inclusive", "y_exclusive", "n_inclusive", "n_exclusive"]] = study_df[
            ["y_inclusive", "y_exclusive", "n_inclusive", "n_exclusive"]
        ].astype(int)
        study_df.insert(0, "study_id", study_id)
        study_df["panel_class"] = classify_study_panel_class(
            study_id=study_id,
            study_panel_map=study_panel_map,
            panel_bearing_studies=panel_bearing_studies,
            sample_panel_ids=sample_panel_ids_by_study.get(study_id, set()),
            study_panel_class_map=study_panel_class_map,
        )
        study_df["matched_normal"] = study_id in matched_normal_studies
        out_frames.append(study_df)

    if not out_frames:
        return pd.DataFrame(
            columns=[
                "study_id",
                "cancer_type",
                "symbol",
                "y_inclusive",
                "y_exclusive",
                "n_inclusive",
                "n_exclusive",
                "panel_class",
                "matched_normal",
            ]
        )

    return (
        pd.concat(out_frames, ignore_index=True)
        .sort_values(["cancer_type", "symbol", "study_id"])
        .reset_index(drop=True)
    )


def classify_study_panel_class(
    *,
    study_id: str,
    study_panel_map: dict[str, str],
    panel_bearing_studies: set[str],
    sample_panel_ids: set[str],
    study_panel_class_map: dict[str, PanelClass],
) -> PanelClass:
    """Classify each study into the pre-registered panel-class factor."""
    if study_id in study_panel_class_map:
        return study_panel_class_map[study_id]
    if study_id == "tcga_mc3":
        return PANEL_CLASS_MC3

    explicit_panel_id = study_panel_map.get(study_id)
    panel_ids = set(sample_panel_ids)
    if explicit_panel_id is not None:
        panel_ids.add(explicit_panel_id)

    if not panel_ids and study_id not in panel_bearing_studies and explicit_panel_id is None:
        return PANEL_CLASS_WES
    if not panel_ids:
        raise ValueError(
            f"Could not infer panel_class for study {study_id!r}: study is panel-restricted "
            "but no panel ids were available. Add study_panel_class_map if needed."
        )

    panel_classes = {_classify_panel_id(panel_id) for panel_id in panel_ids}
    if len(panel_classes) != 1:
        raise ValueError(
            f"Study {study_id!r} spans multiple panel classes {sorted(panel_classes)!r}; "
            "add an explicit study_panel_class_map entry."
        )
    return panel_classes.pop()


def _classify_panel_id(panel_id: str) -> PanelClass:
    normalized = panel_id.upper().replace("_", "-").replace(" ", "")
    if any(marker in normalized for marker in _LARGE_PANEL_MARKERS):
        return PANEL_CLASS_LARGE
    if any(marker in normalized for marker in _SMALL_PANEL_MARKERS):
        return PANEL_CLASS_SMALL
    raise ValueError(
        f"Could not infer panel_class from panel_id {panel_id!r}. "
        "Add study_panel_class_map if this study should be pooled."
    )


def _load_per_study_frames(paths: list[str]) -> list[tuple[str, pd.DataFrame]]:
    frames: list[tuple[str, pd.DataFrame]] = []
    for path in paths:
        study_id = _study_id_from_path(path)
        frames.append((study_id, pd.read_feather(path)))
    return frames


def _load_sample_panel_ids(sample_paths: list[str]) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    for path in sample_paths:
        study_id = _study_id_from_path(path)
        samples = pd.read_feather(path)
        if "panel_id" not in samples.columns:
            out[study_id] = set()
            continue
        out[study_id] = {
            str(panel_id) for panel_id in samples["panel_id"].dropna().unique().tolist()
        }
    return out


def _run_via_snakemake() -> None:
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821
    pooled = build_pooled_input(
        per_study_frames=_load_per_study_frames(list(snek.input.per_study)),
        cancer_presence_by_study=_load_cancer_presence(list(snek.input.per_study_cancer)),
        matched_normal_studies=set(snek.config.get("matched_normal_studies", [])),
        study_panel_map=dict(snek.config.get("study_panel_map", {})),
        panel_bearing_studies=set(snek.config.get("panel_bearing_studies", [])),
        sample_panel_ids_by_study=_load_sample_panel_ids(list(snek.input.samples)),
        study_panel_class_map=dict(snek.config.get("study_panel_class_map", {})),
    )
    Path(snek.output[0]).parent.mkdir(parents=True, exist_ok=True)
    pooled.to_feather(snek.output[0])


if "snakemake" in globals():
    _run_via_snakemake()
