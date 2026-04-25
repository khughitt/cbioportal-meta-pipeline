"""compare_stage_stratified_gene_rates.

Diagnostic for t052: stratify per-(study, cancer_type, gene) mutation rates by
``is_metastatic`` and compare against published Zehir 2017 numbers, applying a
panel-coverage check on the unmatched-normal panel cohort. Produces per-comparison
verdicts and an aggregate closure-state.

Reuses ``annotate_cohort_stage.annotate_samples`` for in-memory stage annotation
and ``compute_per_sample_tmb.PROTEIN_ALTERING_VARIANT_CLASSES`` for the mutation
filter, matching existing TMB-numerator convention.

Not wired into the main Snakefile rule graph; opt-in CLI invocation only.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

from annotate_cohort_stage import annotate_samples, load_and_validate_registry
from compute_per_sample_tmb import PROTEIN_ALTERING_VARIANT_CLASSES
from resolve_panel_id import normalize_panel_id

# Pre-registered thresholds (locked by design doc §Pre-registered verdict thresholds).
RATE_TOLERANCE_PP: float = 0.03
MIN_STRATUM_N: int = 20


def compute_stratum_rate(
    *,
    stratum_samples: pd.DataFrame,
    mutations_df: pd.DataFrame,
    gene: str,
    target_variant: str,
    panel_covered_sample_ids: set[str] | None,
) -> tuple[int, int, int, float]:
    """Return ``(n_in_stratum, n_panel_covers, n_mutated, rate)`` for one stratum."""
    n_in_stratum = len(stratum_samples)
    if panel_covered_sample_ids is None:
        covered = stratum_samples
    else:
        covered = stratum_samples[
            stratum_samples["sample_id"].isin(panel_covered_sample_ids)
        ]
    n_panel_covers = len(covered)
    if n_panel_covers == 0:
        return n_in_stratum, 0, 0, 0.0
    sample_ids = set(covered["sample_id"].tolist())
    muts = mutations_df[mutations_df["sample_id_tumor"].isin(sample_ids)]
    muts = muts[
        muts["variant_class"].astype(str).isin(PROTEIN_ALTERING_VARIANT_CLASSES)
    ]
    muts = muts[muts["symbol"] == gene]
    if target_variant:
        muts = muts[muts["hgvsp_short"] == target_variant]
    n_mutated = muts["sample_id_tumor"].nunique()
    rate = n_mutated / n_panel_covers
    return n_in_stratum, n_panel_covers, n_mutated, rate


def apply_verdict(
    *,
    observed_met: float,
    observed_pri: float,
    expected_met: float,
    expected_pri: float,
    n_met_panel: int,
    n_pri_panel: int,
    threshold: float = RATE_TOLERANCE_PP,
    min_n: int = MIN_STRATUM_N,
) -> str:
    if n_met_panel < min_n or n_pri_panel < min_n:
        return "underpowered"
    if observed_met <= observed_pri:
        return "fails"
    diff_met = abs(observed_met - expected_met)
    diff_pri = abs(observed_pri - expected_pri)
    if diff_met <= threshold and diff_pri <= threshold:
        return "reproduces"
    return "partial"


def apply_closure_state(verdicts: list[str]) -> str:
    if all(v == "underpowered" for v in verdicts):
        return "insufficient evidence"
    if any(v == "fails" for v in verdicts):
        return "descriptor needs investigation"
    n_validating = sum(1 for v in verdicts if v in ("reproduces", "partial"))
    if n_validating >= 1:
        return "descriptor validated"
    return "insufficient evidence"


# ---------------------------------------------------------------------------
# Panel coverage check (MSK / GENIE side only)
# ---------------------------------------------------------------------------


def build_panel_gene_coverage(
    *, genie_genomic_information: Path, focal_genes: set[str]
) -> dict[tuple[str, str], bool]:
    """Return ``{(canonical_panel_id, gene_symbol): True}`` for genes on each panel.

    Loads only ``Feature_Type == 'exon'`` and ``includeInPanel == 'True'`` rows; ignores
    panels whose raw SEQ_ASSAY_ID does not normalize via ``resolve_panel_id``.
    """
    df = pd.read_csv(genie_genomic_information, sep="\t", dtype=str)
    df = df[(df["Feature_Type"] == "exon") & (df["includeInPanel"] == "True")]
    df = df[df["Hugo_Symbol"].isin(focal_genes)]
    coverage: dict[tuple[str, str], bool] = {}
    for raw_panel, sub in df.groupby("SEQ_ASSAY_ID"):
        try:
            canon = normalize_panel_id(str(raw_panel))
        except ValueError:
            continue
        for g in sub["Hugo_Symbol"].unique():
            coverage[(canon, str(g))] = True
    return coverage


def panel_covered_sample_ids_for_gene(
    *, samples_df: pd.DataFrame, gene: str, coverage: dict[tuple[str, str], bool]
) -> set[str]:
    """Return sample_ids whose ``panel_id`` covers ``gene``."""
    if "panel_id" not in samples_df.columns:
        # No panel column -> treat as WES (all samples covered).
        return set(samples_df["sample_id"].tolist())
    keep = []
    for sid, panel_id in zip(samples_df["sample_id"], samples_df["panel_id"]):
        if pd.isna(panel_id) or panel_id == "":
            continue
        if coverage.get((str(panel_id), gene), False):
            keep.append(sid)
    return set(keep)


# ---------------------------------------------------------------------------
# Diagnostic orchestration
# ---------------------------------------------------------------------------


def _load_study_samples(study_results_root: Path, study_id: str) -> pd.DataFrame:
    return pd.read_feather(
        study_results_root / "studies" / study_id / "metadata" / "samples.feather"
    )


def _load_study_mutations(study_results_root: Path, study_id: str) -> pd.DataFrame:
    return pd.read_feather(
        study_results_root / "studies" / study_id / "mut" / "table" / "mut.feather"
    )


def run_diagnostic(
    *,
    manifest_path: Path,
    registry_path: Path,
    panel_results_root: Path,
    matched_results_root: Path,
    genie_genomic_information: Path,
    output_path: Path,
) -> dict[str, object]:
    """Run the full diagnostic per the comparison manifest.

    ``panel_results_root`` and ``matched_results_root`` may be the same directory
    when both the metastatic and primary studies share an artifact; they are passed
    separately so the AR comparison can pull ``prad_tcga_pan_can_atlas_2018`` from
    a different (smaller) prerequisite ingestion run.
    """
    manifest = pd.read_csv(manifest_path, sep="\t", dtype=str).fillna("")
    registry = load_and_validate_registry(registry_path)
    focal_genes = set(manifest["gene"].tolist())
    panel_coverage = build_panel_gene_coverage(
        genie_genomic_information=genie_genomic_information,
        focal_genes=focal_genes,
    )

    rows: list[dict] = []
    verdicts_for_closure: list[str] = []
    for _, comp in manifest.iterrows():
        gene = comp["gene"]
        target_variant = comp["target_variant"]
        met_study = comp["metastatic_study_id"]
        pri_study = comp["primary_study_id"]
        met_cancer = comp["metastatic_cancer_type"]
        pri_cancer = comp["primary_cancer_type"]
        expected_met = float(comp["metastatic_expected_rate"])
        expected_pri = float(comp["primary_expected_rate"])

        # Metastatic side (panel cohort).
        met_samples = _load_study_samples(panel_results_root, met_study)
        met_samples_ann = annotate_samples(met_samples, met_study, registry)
        met_stratum = met_samples_ann[
            (met_samples_ann["cancer_type"] == met_cancer)
            & (met_samples_ann["is_metastatic"] == True)  # noqa: E712
        ]
        met_panel_ids = panel_covered_sample_ids_for_gene(
            samples_df=met_stratum, gene=gene, coverage=panel_coverage
        )
        met_muts = _load_study_mutations(panel_results_root, met_study)
        n_met_in, n_met_panel, n_met_mutated, met_rate = compute_stratum_rate(
            stratum_samples=met_stratum,
            mutations_df=met_muts,
            gene=gene,
            target_variant=target_variant,
            panel_covered_sample_ids=met_panel_ids,
        )

        # Primary side (WES cohort).
        pri_samples = _load_study_samples(matched_results_root, pri_study)
        pri_samples_ann = annotate_samples(pri_samples, pri_study, registry)
        pri_stratum = pri_samples_ann[
            (pri_samples_ann["cancer_type"] == pri_cancer)
            & (pri_samples_ann["is_metastatic"] == False)  # noqa: E712
        ]
        pri_muts = _load_study_mutations(matched_results_root, pri_study)
        n_pri_in, n_pri_panel, n_pri_mutated, pri_rate = compute_stratum_rate(
            stratum_samples=pri_stratum,
            mutations_df=pri_muts,
            gene=gene,
            target_variant=target_variant,
            panel_covered_sample_ids=None,  # WES: no panel filter
        )

        verdict = apply_verdict(
            observed_met=met_rate,
            observed_pri=pri_rate,
            expected_met=expected_met,
            expected_pri=expected_pri,
            n_met_panel=n_met_panel,
            n_pri_panel=n_pri_panel,
        )
        verdicts_for_closure.append(verdict)

        rows.extend(
            [
                {
                    "comparison_id": comp["comparison_id"],
                    "study_id": met_study,
                    "cancer_type": met_cancer,
                    "gene": gene,
                    "target_variant": target_variant or None,
                    "is_metastatic": True,
                    "n_samples_in_stratum": n_met_in,
                    "n_samples_panel_covers_gene": n_met_panel,
                    "n_mutated": n_met_mutated,
                    "mutation_rate": met_rate,
                    "expected_zehir2017": expected_met,
                    "verdict": verdict,
                },
                {
                    "comparison_id": comp["comparison_id"],
                    "study_id": pri_study,
                    "cancer_type": pri_cancer,
                    "gene": gene,
                    "target_variant": target_variant or None,
                    "is_metastatic": False,
                    "n_samples_in_stratum": n_pri_in,
                    "n_samples_panel_covers_gene": n_pri_panel,
                    "n_mutated": n_pri_mutated,
                    "mutation_rate": pri_rate,
                    "expected_zehir2017": expected_pri,
                    "verdict": verdict,
                },
            ]
        )

    out_df = pd.DataFrame(rows)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_feather(output_path)
    closure_state = apply_closure_state(verdicts_for_closure)
    return {
        "output_path": str(output_path),
        "closure_state": closure_state,
        "per_comparison_verdicts": dict(
            zip(manifest["comparison_id"].tolist(), verdicts_for_closure)
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("data/cohort_stage_validation_comparisons.tsv"),
    )
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path("data/cbioportal_study_cohort_profiles.tsv"),
    )
    parser.add_argument(
        "--panel-results-root",
        type=Path,
        required=True,
        help="Results dir holding the metastatic-side panel study (e.g., msk_impact_2017)",
    )
    parser.add_argument(
        "--matched-results-root",
        type=Path,
        required=True,
        help="Results dir holding the primary-side TCGA studies",
    )
    parser.add_argument(
        "--genie-genomic-info",
        type=Path,
        default=Path("data/genie/genomic_information.txt"),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)

    summary = run_diagnostic(
        manifest_path=args.manifest,
        registry_path=args.registry,
        panel_results_root=args.panel_results_root,
        matched_results_root=args.matched_results_root,
        genie_genomic_information=args.genie_genomic_info,
        output_path=args.output,
    )
    print(f"Wrote {summary['output_path']}", file=sys.stderr)
    print(
        f"Per-comparison verdicts: {summary['per_comparison_verdicts']}",
        file=sys.stderr,
    )
    print(f"CLOSURE STATE: {summary['closure_state']}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
