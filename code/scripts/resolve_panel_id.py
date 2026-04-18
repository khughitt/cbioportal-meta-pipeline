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
            f"Unrecognized panel_id {raw!r}; add to PANEL_ALIASES if real, "
            "or fix upstream data."
        )
    return canonical
