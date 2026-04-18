"""Per-sample panel-version resolution for MSK-IMPACT and related cBioPortal studies.

Implements t070 (see ``doc/plans/2026-04-18-t070-msk-impact-panel-version-drift-design.md``).

Three observed panel-naming conventions in upstream data are normalized to one
canonical form (matching `panel_callable_mb_override` config keys):

- cBioPortal `data_gene_panel_matrix.txt`: `IMPACT341`
- AACR GENIE `SEQ_ASSAY_ID`: `MSK-IMPACT341`
- Project-canonical: `MSK-IMPACT-341`

References:
- Cheng DT et al. 2015. *J Mol Diagn* 17(3):251-264. PMID 25801821. (IMPACT-341/410)
- Zehir A et al. 2017. *Nat Med* 23(6):703-713. PMID 28481359. (IMPACT-410/468)
- Bandlamudi C et al. 2026. *Cancer Cell*. PMID 41895280. (IMPACT-505)
"""

import pandas as pd

PANEL_ALIASES: dict[str, str] = {
    # IMPACT-341
    "IMPACT341": "MSK-IMPACT-341",
    "MSK-IMPACT341": "MSK-IMPACT-341",
    "MSK-IMPACT-341": "MSK-IMPACT-341",
    # IMPACT-410
    "IMPACT410": "MSK-IMPACT-410",
    "MSK-IMPACT410": "MSK-IMPACT-410",
    "MSK-IMPACT-410": "MSK-IMPACT-410",
    # IMPACT-468
    "IMPACT468": "MSK-IMPACT-468",
    "MSK-IMPACT468": "MSK-IMPACT-468",
    "MSK-IMPACT-468": "MSK-IMPACT-468",
    # IMPACT-505
    "IMPACT505": "MSK-IMPACT-505",
    "MSK-IMPACT505": "MSK-IMPACT-505",
    "MSK-IMPACT-505": "MSK-IMPACT-505",
    # IMPACT-HEME-400 / 468
    "IMPACT-HEME-400": "MSK-IMPACT-HEME-400",
    "MSK-IMPACT-HEME-400": "MSK-IMPACT-HEME-400",
    "IMPACT-HEME-468": "MSK-IMPACT-HEME-468",
    "MSK-IMPACT-HEME-468": "MSK-IMPACT-HEME-468",
}


def normalize_panel_id(raw: str) -> str:
    """Canonicalize a raw panel string to the project-canonical form.

    Raises ``ValueError`` for unrecognized panels — fail-loud, no silent fallback.
    """
    key = raw.strip()
    canonical = PANEL_ALIASES.get(key)
    if canonical is None:
        raise ValueError(
            f"Unrecognized panel_id {key!r}; add to PANEL_ALIASES if real, "
            "or fix upstream data."
        )
    return canonical


SAMPLE_ID_SUFFIX_MAP: dict[str, str] = {
    "IM3": "MSK-IMPACT-341",
    "IM5": "MSK-IMPACT-410",
    "IM6": "MSK-IMPACT-468",
    "IM7": "MSK-IMPACT-505",
    "IH3": "MSK-IMPACT-HEME-400",
}


def infer_panel_from_sample_id(sample_id: str) -> str | None:
    """Parse the trailing ``-IM[3567]`` / ``-IH3`` suffix from an MSK sample id.

    Returns ``None`` if the sample id has no recognized suffix (TCGA / GENIE /
    other formats). Suffix convention: Cheng 2015 + IMPACT release notes.
    """
    if not sample_id:
        return None
    suffix = sample_id.rsplit("-", 1)[-1]
    return SAMPLE_ID_SUFFIX_MAP.get(suffix)


def resolve_panel_ids(
    samples: pd.DataFrame,
    matrix: pd.DataFrame | None,
    study_id: str,
    study_panel_map: dict[str, str],
    is_panel_study: bool,
) -> pd.Series:
    """Return a panel_id Series indexed like ``samples`` (positionally).

    For non-panel studies (``is_panel_study=False``), returns all-NaN — downstream
    consumers treat this as the "panel-aware path bypassed" signal.

    For panel studies, the per-sample resolution chain is:
      1. ``matrix['mutations']`` column normalized via :data:`PANEL_ALIASES`
      2. :func:`infer_panel_from_sample_id` applied to ``sample_id``
      3. ``study_panel_map[study_id]`` (single panel applied to all samples)

    Anything unresolved raises ``ValueError`` carrying ``(study_id, sample_id)``.
    """
    if not is_panel_study:
        return pd.Series([None] * len(samples), index=samples.index, dtype="object")

    sample_ids = samples["sample_id"].astype(str)

    def _normalize_with_context(raw: object, sample_id: str) -> str:
        try:
            return normalize_panel_id(str(raw))
        except ValueError as exc:
            raise ValueError(
                f"matrix for study {study_id!r}: sample {sample_id!r} has "
                f"unrecognized panel {raw!r}"
            ) from exc

    matrix_lookup: dict[str, str] = {}
    if matrix is not None and not matrix.empty:
        if "SAMPLE_ID" not in matrix.columns or "mutations" not in matrix.columns:
            raise ValueError(
                f"matrix must have 'SAMPLE_ID' and 'mutations' columns; "
                f"got {list(matrix.columns)}"
            )
        matrix_lookup = {
            str(s): _normalize_with_context(p, str(s))
            for s, p in zip(matrix["SAMPLE_ID"], matrix["mutations"], strict=True)
            if pd.notna(p) and str(p).strip()
        }

    study_default = study_panel_map.get(study_id)
    if study_default is not None:
        study_default = normalize_panel_id(study_default)

    out: list[str] = []
    for sid in sample_ids:
        resolved = matrix_lookup.get(sid)
        if resolved is None:
            resolved = infer_panel_from_sample_id(sid)
        if resolved is None:
            resolved = study_default
        if resolved is None:
            raise ValueError(
                f"Cannot resolve panel_id for sample {sid!r} in panel study "
                f"{study_id!r}: not in matrix, no recognized sample-id suffix, "
                "no study_panel_map fallback. Investigate upstream data."
            )
        out.append(resolved)

    return pd.Series(out, index=samples.index, dtype="object")
