# science:code
# status: workflow-owned
# science:end
"""Audit candidate studies for q027 therapy-signature-high feasibility."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import click
import pandas as pd
import yaml

from run_restricted_sigprofiler_assignment import (
    DEFAULT_COSMIC_VERSION,
    DEFAULT_MIN_SBS_COUNT_MATCHED_NORMAL,
    DEFAULT_MIN_SBS_COUNT_WES,
    SPLIT_SIGNATURE_ALIASES,
    count_floor_for_sample,
    normalize_cancer_type,
    prepare_sigprofiler_variants,
    read_reference_signature_columns,
    resolve_cosmic_reference,
)


RESULTS_DIR = Path("results/q027-therapy-signature-high-2026-06-01")
DEFAULT_MIN_PASSING_SAMPLES = 25
THERAPY_SIGNATURES = ("SBS11", "SBS31", "SBS35", "SBS87")
ANY_LOOKUP_KEY = "*"


@dataclass(frozen=True)
class CandidateStudy:
    study_id: str
    target_signatures: tuple[str, ...]
    expected_lookup_key: str
    primary_patient_denominator: bool
    expectation_tier: str = "explicit"
    clinical_signal: str = ""
    rationale: str = ""


DEFAULT_CANDIDATES: tuple[CandidateStudy, ...] = (
    CandidateStudy(
        study_id="difg_glass_2019",
        target_signatures=("SBS11",),
        expected_lookup_key="cns",
        primary_patient_denominator=True,
        rationale="TMZ field with treated, explicit-no, and unknown samples",
    ),
    CandidateStudy(
        study_id="blca_cornell_2016",
        target_signatures=("SBS31", "SBS35"),
        expected_lookup_key="bladder",
        primary_patient_denominator=True,
        rationale="post-chemotherapy and pre-chemotherapy samples",
    ),
    CandidateStudy(
        study_id="blca_dfarber_mskcc_2014",
        target_signatures=("SBS31", "SBS35"),
        expected_lookup_key="bladder",
        primary_patient_denominator=True,
        rationale="cisplatin-treated bladder cohort",
    ),
    CandidateStudy(
        study_id="sclc_cancercell_gardner_2017",
        target_signatures=("SBS31", "SBS35"),
        expected_lookup_key="lung",
        primary_patient_denominator=False,
        rationale="treatment-derived PDX sensitivity-only cohort",
    ),
    CandidateStudy(
        study_id="pptc_2019",
        target_signatures=("SBS11", "SBS31", "SBS35", "SBS87"),
        expected_lookup_key="cns",
        primary_patient_denominator=False,
        rationale="pediatric PDX sensitivity-only cohort",
    ),
)


def discover_candidate_studies(
    *, config: Mapping[str, Any], data_dir: Path
) -> tuple[CandidateStudy, ...]:
    """Build broad q027 discovery candidates from configured raw study metadata."""
    studies = tuple(str(study) for study in config.get("studies", []))
    if not studies:
        raise ValueError(
            "config studies list is empty; cannot discover q027 candidates"
        )

    candidates: list[CandidateStudy] = []
    for study_id in studies:
        study_text = _read_study_metadata_text(data_dir / study_id)
        target_signatures, expectation_tier, clinical_signal = (
            _infer_target_signature_expectation(study_text)
        )
        primary_patient_denominator = not _looks_like_pdx(study_text)
        candidates.append(
            CandidateStudy(
                study_id=study_id,
                target_signatures=target_signatures,
                expected_lookup_key=ANY_LOOKUP_KEY,
                primary_patient_denominator=primary_patient_denominator,
                expectation_tier=expectation_tier,
                clinical_signal=clinical_signal,
                rationale=_discovery_rationale(
                    expectation_tier=expectation_tier,
                    clinical_signal=clinical_signal,
                    primary_patient_denominator=primary_patient_denominator,
                ),
            )
        )
    return tuple(candidates)


def audit_candidate_study(
    *,
    candidate: CandidateStudy,
    mutations: pd.DataFrame,
    samples: pd.DataFrame,
    treatment_annotations: pd.DataFrame,
    reference_columns: list[str],
    count_floor: int,
    min_passing_samples: int = DEFAULT_MIN_PASSING_SAMPLES,
    allow_count_errors: bool = False,
) -> pd.DataFrame:
    """Return one feasibility row per candidate cancer-type stratum."""
    _require_columns(samples, {"sample_id", "cancer_type"}, "samples")
    _require_columns(
        treatment_annotations,
        {
            "sample_id",
            "no_detected_treatment_signal",
            "positive_naive_or_pretreatment",
            "treatment_metadata_unknown",
        },
        "samples_treatment_exposure",
    )
    samples = _normalize_sample_id_column(samples)
    treatment_annotations = _normalize_sample_id_column(treatment_annotations)
    mutations = _normalize_mutation_sample_id_column(mutations)

    study_samples = _filter_study(samples, candidate.study_id)
    study_treatment = _filter_study(treatment_annotations, candidate.study_id)
    _validate_sample_annotation_coverage(
        study_id=candidate.study_id,
        samples=study_samples,
        treatment_annotations=study_treatment,
    )

    rows: list[dict[str, object]] = []
    for cancer_type in sorted(
        study_samples["cancer_type"].dropna().astype(str).unique()
    ):
        stratum_samples = study_samples.loc[
            study_samples["cancer_type"].astype(str) == cancer_type
        ].copy()
        try:
            lookup_key = normalize_cancer_type(cancer_type)
        except ValueError:
            rows.append(
                _unsupported_cancer_type_row(
                    candidate=candidate,
                    cancer_type=cancer_type,
                    stratum_samples=stratum_samples,
                    study_treatment=study_treatment,
                    reference_columns=reference_columns,
                    count_floor=count_floor,
                )
            )
            continue
        if (
            candidate.expected_lookup_key != ANY_LOOKUP_KEY
            and lookup_key != candidate.expected_lookup_key
        ):
            continue
        if not candidate.target_signatures or candidate.expectation_tier == "none":
            rows.append(
                _no_count_candidate_row(
                    candidate=candidate,
                    cancer_type=cancer_type,
                    lookup_key=lookup_key,
                    stratum_samples=stratum_samples,
                    study_treatment=study_treatment,
                    reference_columns=reference_columns,
                    count_floor=count_floor,
                    unsupported_reason="no_treatment_signature_expectation",
                )
            )
            continue

        try:
            variants = prepare_sigprofiler_variants(
                mutations=mutations,
                samples=stratum_samples,
                cancer_type=cancer_type,
                sample_name=candidate.study_id,
                assignment_unit="sample",
            )
        except (KeyError, TypeError, ValueError) as exc:
            if not allow_count_errors:
                raise
            rows.append(
                _no_count_candidate_row(
                    candidate=candidate,
                    cancer_type=cancer_type,
                    lookup_key=lookup_key,
                    stratum_samples=stratum_samples,
                    study_treatment=study_treatment,
                    reference_columns=reference_columns,
                    count_floor=count_floor,
                    unsupported_reason="mutation_context_count_error",
                    error_detail=f"{type(exc).__name__}: {exc}",
                )
            )
            continue
        counts = (
            variants.groupby("donor_id", observed=True).size().rename("total_sbs_count")
        )
        sample_counts = stratum_samples[["sample_id"]].copy()
        sample_counts["total_sbs_count"] = (
            sample_counts["sample_id"].map(counts).fillna(0).astype(int)
        )
        sample_counts["passes_count_floor"] = (
            sample_counts["total_sbs_count"] >= count_floor
        )

        sample_treatment = sample_counts.merge(
            study_treatment[
                [
                    "sample_id",
                    "no_detected_treatment_signal",
                    "positive_naive_or_pretreatment",
                    "treatment_metadata_unknown",
                ]
            ],
            on="sample_id",
            how="left",
            validate="one_to_one",
        )
        retained_comparator = (
            sample_treatment["no_detected_treatment_signal"]
            | sample_treatment["positive_naive_or_pretreatment"]
        )
        count_floor_passing = sample_treatment["passes_count_floor"]
        n_count_floor_passing = int(count_floor_passing.sum())
        n_retained_passing = int((count_floor_passing & retained_comparator).sum())
        target_present = bool(candidate.target_signatures) and all(
            _signature_present(signature, reference_columns)
            for signature in candidate.target_signatures
        )
        has_treatment_signature_expectation = candidate.expectation_tier == "explicit"
        passes_gate = (
            candidate.primary_patient_denominator
            and target_present
            and n_count_floor_passing >= min_passing_samples
            and n_retained_passing > 0
            and has_treatment_signature_expectation
        )

        rows.append(
            {
                "study_id": candidate.study_id,
                "cancer_type": cancer_type,
                "lookup_key": lookup_key,
                "primary_patient_denominator": candidate.primary_patient_denominator,
                "target_signatures": "|".join(candidate.target_signatures),
                "target_signatures_present": target_present,
                "missing_target_signatures": "|".join(
                    signature
                    for signature in candidate.target_signatures
                    if not _signature_present(signature, reference_columns)
                ),
                "count_floor": count_floor,
                "n_samples": int(len(stratum_samples)),
                "n_sbs_filter_passing_variants": int(len(variants)),
                "n_count_floor_passing_samples": n_count_floor_passing,
                "frac_count_floor_passing_samples": _fraction(
                    n_count_floor_passing, len(stratum_samples)
                ),
                "n_count_floor_passing_retained_clinical_comparator": n_retained_passing,
                "has_retained_clinical_comparator": n_retained_passing > 0,
                "n_no_detected_treatment_signal": int(
                    sample_treatment["no_detected_treatment_signal"].sum()
                ),
                "n_positive_naive_or_pretreatment": int(
                    sample_treatment["positive_naive_or_pretreatment"].sum()
                ),
                "n_treatment_metadata_unknown": int(
                    sample_treatment["treatment_metadata_unknown"].sum()
                ),
                "expectation_tier": candidate.expectation_tier,
                "clinical_signal": candidate.clinical_signal,
                "has_treatment_signature_expectation": has_treatment_signature_expectation,
                "passes_wp1_gate": passes_gate,
                "unsupported_reason": "",
                "rationale": candidate.rationale,
            }
        )

    return pd.DataFrame(rows, columns=_audit_columns())


def decide_feasibility(
    audit: pd.DataFrame, *, min_passing_samples: int = DEFAULT_MIN_PASSING_SAMPLES
) -> dict[str, object]:
    """Decide whether q027 should continue to assignment substrate construction."""
    if audit.empty:
        return {
            "continue_to_wp2": False,
            "passing_primary_patient_studies": [],
            "reason": "no_candidate_rows",
            "min_passing_samples": min_passing_samples,
        }

    required = {
        "study_id",
        "primary_patient_denominator",
        "target_signatures_present",
        "n_count_floor_passing_samples",
        "has_retained_clinical_comparator",
        "has_treatment_signature_expectation",
    }
    _require_columns(audit, required, "audit")
    passing = audit.loc[
        audit["primary_patient_denominator"].astype(bool)
        & audit["target_signatures_present"].astype(bool)
        & (audit["n_count_floor_passing_samples"].astype(int) >= min_passing_samples)
        & audit["has_retained_clinical_comparator"].astype(bool)
        & audit["has_treatment_signature_expectation"].astype(bool)
    ]
    studies = sorted(passing["study_id"].astype(str).unique())
    return {
        "continue_to_wp2": bool(studies),
        "passing_primary_patient_studies": studies,
        "reason": "passed"
        if studies
        else "no_primary_patient_candidate_passed_wp1_gate",
        "min_passing_samples": min_passing_samples,
    }


def summarize_audit(
    audit: pd.DataFrame, decision: Mapping[str, object], *, min_passing_samples: int
) -> str:
    """Render a short markdown note for the WP1 feasibility audit."""
    verdict = (
        "continue to WP2"
        if decision.get("continue_to_wp2")
        else "non-arbitrating at WP1"
    )
    lines = [
        "# q027 therapy-signature substrate feasibility audit",
        "",
        f"Verdict: **{verdict}**.",
        "",
    ]
    if decision.get("continue_to_wp2"):
        passing = ", ".join(
            f"`{study}`" for study in decision["passing_primary_patient_studies"]
        )
        lines.extend(
            [
                "At least one primary patient candidate passed the WP1 feasibility gate.",
                f"Passing studies: {passing}.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "No primary patient candidate passed the WP1 feasibility gate, so q027 is non-arbitrating from this substrate.",
                f"The gate required >= {min_passing_samples} count-floor-passing samples, target signature availability, and at least one retained clinical comparator sample.",
                "",
            ]
        )

    lines.extend(
        [
            "| study | cancer_type | lookup | primary_patient | targets | target_present | n | n_floor_pass | n_retained_floor_pass | gate |",
            "|---|---|---|---:|---|---:|---:|---:|---:|---:|",
        ]
    )
    for row in audit.sort_values(["study_id", "cancer_type"]).to_dict("records"):
        lines.append(
            "| "
            f"`{row['study_id']}` | "
            f"{row['cancer_type']} | "
            f"`{row['lookup_key']}` | "
            f"{_yes_no(row['primary_patient_denominator'])} | "
            f"`{row['target_signatures']}` | "
            f"{_yes_no(row['target_signatures_present'])} | "
            f"{row['n_samples']} | "
            f"{row['n_count_floor_passing_samples']} | "
            f"{row['n_count_floor_passing_retained_clinical_comparator']} | "
            f"{_yes_no(row['passes_wp1_gate'])} |"
        )
    lines.append("")
    return "\n".join(lines)


def run_audit(
    *,
    config: Mapping[str, Any],
    reference_columns: list[str],
    candidates: tuple[CandidateStudy, ...] = DEFAULT_CANDIDATES,
    min_passing_samples: int = DEFAULT_MIN_PASSING_SAMPLES,
    allow_count_errors: bool = False,
) -> tuple[pd.DataFrame, dict[str, object], str]:
    out_dir = Path(str(config["out_dir"]))
    treatment_path = out_dir / "metadata" / "samples_treatment_exposure.feather"
    if not treatment_path.exists():
        raise FileNotFoundError(
            f"Missing H10 treatment annotations: {treatment_path}. Run all_h10_treatment_annotations first."
        )
    treatment_annotations = pd.read_feather(treatment_path)
    caller_consensus = None
    matched_normal_studies = set(config.get("matched_normal_studies", []))
    min_sbs_count_wes = int(
        config.get("signature_min_sbs_count_wes", DEFAULT_MIN_SBS_COUNT_WES)
    )
    min_sbs_count_matched_normal = int(
        config.get(
            "signature_min_sbs_count_matched_normal",
            DEFAULT_MIN_SBS_COUNT_MATCHED_NORMAL,
        )
    )

    frames: list[pd.DataFrame] = []
    for candidate in candidates:
        mutations_path = (
            out_dir / "studies" / candidate.study_id / "mut" / "table" / "mut.feather"
        )
        samples_path = (
            out_dir / "studies" / candidate.study_id / "metadata" / "samples.feather"
        )
        if not mutations_path.exists():
            raise FileNotFoundError(
                f"Missing candidate mutation table for {candidate.study_id}: {mutations_path}"
            )
        if not samples_path.exists():
            raise FileNotFoundError(
                f"Missing candidate sample table for {candidate.study_id}: {samples_path}"
            )

        count_floor = count_floor_for_sample(
            caller_consensus=caller_consensus,
            matched_normal=candidate.study_id in matched_normal_studies,
            min_sbs_count_wes=min_sbs_count_wes,
            min_sbs_count_matched_normal=min_sbs_count_matched_normal,
        )
        frames.append(
            audit_candidate_study(
                candidate=candidate,
                mutations=pd.read_feather(mutations_path),
                samples=pd.read_feather(samples_path),
                treatment_annotations=treatment_annotations,
                reference_columns=reference_columns,
                count_floor=count_floor,
                min_passing_samples=min_passing_samples,
                allow_count_errors=allow_count_errors,
            )
        )

    audit = (
        pd.concat(frames, ignore_index=True)
        if frames
        else pd.DataFrame(columns=_audit_columns())
    )
    decision = decide_feasibility(audit, min_passing_samples=min_passing_samples)
    note = summarize_audit(audit, decision, min_passing_samples=min_passing_samples)
    return audit, decision, note


@click.command()
@click.option(
    "--config",
    "config_path",
    type=click.Path(path_type=Path, exists=True),
    required=True,
)
@click.option(
    "--output-dir",
    type=click.Path(path_type=Path),
    default=RESULTS_DIR,
    show_default=True,
)
@click.option(
    "--min-passing-samples",
    type=int,
    default=DEFAULT_MIN_PASSING_SAMPLES,
    show_default=True,
)
@click.option(
    "--all-config-discovery",
    is_flag=True,
    help="Scan all configured studies with metadata/count triage instead of the t210 hard-coded candidates.",
)
def main(
    config_path: Path,
    output_dir: Path,
    min_passing_samples: int,
    all_config_discovery: bool,
) -> None:
    """Write q027 WP1 feasibility TSV and markdown note."""
    config = yaml.safe_load(config_path.read_text())
    genome_build = str(config.get("signature_assignment_genome_build", "GRCh37"))
    cosmic_version = str(
        config.get("signature_assignment_cosmic_version", DEFAULT_COSMIC_VERSION)
    )
    exome = bool(config.get("signature_assignment_exome", True))
    reference_path = resolve_cosmic_reference(
        genome_build=genome_build, cosmic_version=cosmic_version, exome=exome
    )
    reference_columns = read_reference_signature_columns(reference_path)
    missing = sorted(
        signature
        for signature in THERAPY_SIGNATURES
        if not _signature_present(signature, reference_columns)
    )
    if missing:
        raise ValueError(
            "Requested q027 therapy signatures are absent from the COSMIC reference: "
            f"{missing}. Do not silently proceed with absorbed signatures."
        )

    candidates = (
        discover_candidate_studies(
            config=config, data_dir=Path(str(config["data_dir"]))
        )
        if all_config_discovery
        else DEFAULT_CANDIDATES
    )
    audit, decision, note = run_audit(
        config=config,
        reference_columns=reference_columns,
        candidates=candidates,
        min_passing_samples=min_passing_samples,
        allow_count_errors=all_config_discovery,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    audit.to_csv(
        output_dir / "therapy_signature_substrate_feasibility.tsv",
        sep="\t",
        index=False,
    )
    (output_dir / "therapy_signature_substrate_feasibility.md").write_text(note)
    click.echo(
        f"Wrote {len(audit)} feasibility row(s) to {output_dir}; "
        f"continue_to_wp2={decision['continue_to_wp2']}"
    )


def _audit_columns() -> list[str]:
    return [
        "study_id",
        "cancer_type",
        "lookup_key",
        "primary_patient_denominator",
        "target_signatures",
        "target_signatures_present",
        "missing_target_signatures",
        "count_floor",
        "n_samples",
        "n_sbs_filter_passing_variants",
        "n_count_floor_passing_samples",
        "frac_count_floor_passing_samples",
        "n_count_floor_passing_retained_clinical_comparator",
        "has_retained_clinical_comparator",
        "n_no_detected_treatment_signal",
        "n_positive_naive_or_pretreatment",
        "n_treatment_metadata_unknown",
        "expectation_tier",
        "clinical_signal",
        "has_treatment_signature_expectation",
        "passes_wp1_gate",
        "unsupported_reason",
        "rationale",
    ]


def _filter_study(frame: pd.DataFrame, study_id: str) -> pd.DataFrame:
    if "study_id" not in frame.columns:
        return frame.copy()
    return frame.loc[frame["study_id"].astype(str) == study_id].copy()


def _normalize_sample_id_column(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    out["sample_id"] = out["sample_id"].astype(str)
    return out


def _normalize_mutation_sample_id_column(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    if "sample_id_tumor" in out.columns:
        out["sample_id_tumor"] = out["sample_id_tumor"].astype(str)
    return out


def _validate_sample_annotation_coverage(
    *,
    study_id: str,
    samples: pd.DataFrame,
    treatment_annotations: pd.DataFrame,
) -> None:
    sample_ids = set(samples["sample_id"].astype(str))
    annotated_ids = set(treatment_annotations["sample_id"].astype(str))
    missing = sorted(sample_ids - annotated_ids)
    if missing:
        raise ValueError(
            f"samples_treatment_exposure is missing {len(missing)} sample(s) for {study_id}: {missing[:10]}"
        )


def _unsupported_cancer_type_row(
    *,
    candidate: CandidateStudy,
    cancer_type: str,
    stratum_samples: pd.DataFrame,
    study_treatment: pd.DataFrame,
    reference_columns: list[str],
    count_floor: int,
) -> dict[str, object]:
    sample_treatment = stratum_samples[["sample_id"]].merge(
        study_treatment[
            [
                "sample_id",
                "no_detected_treatment_signal",
                "positive_naive_or_pretreatment",
                "treatment_metadata_unknown",
            ]
        ],
        on="sample_id",
        how="left",
        validate="one_to_one",
    )
    return {
        "study_id": candidate.study_id,
        "cancer_type": cancer_type,
        "lookup_key": "unsupported",
        "primary_patient_denominator": candidate.primary_patient_denominator,
        "target_signatures": "|".join(candidate.target_signatures),
        "target_signatures_present": bool(candidate.target_signatures)
        and all(
            _signature_present(signature, reference_columns)
            for signature in candidate.target_signatures
        ),
        "missing_target_signatures": "|".join(
            signature
            for signature in candidate.target_signatures
            if not _signature_present(signature, reference_columns)
        ),
        "count_floor": count_floor,
        "n_samples": int(len(stratum_samples)),
        "n_sbs_filter_passing_variants": 0,
        "n_count_floor_passing_samples": 0,
        "frac_count_floor_passing_samples": 0.0,
        "n_count_floor_passing_retained_clinical_comparator": 0,
        "has_retained_clinical_comparator": False,
        "n_no_detected_treatment_signal": int(
            sample_treatment["no_detected_treatment_signal"].sum()
        ),
        "n_positive_naive_or_pretreatment": int(
            sample_treatment["positive_naive_or_pretreatment"].sum()
        ),
        "n_treatment_metadata_unknown": int(
            sample_treatment["treatment_metadata_unknown"].sum()
        ),
        "expectation_tier": candidate.expectation_tier,
        "clinical_signal": candidate.clinical_signal,
        "has_treatment_signature_expectation": candidate.expectation_tier == "explicit",
        "passes_wp1_gate": False,
        "unsupported_reason": "unsupported_cancer_type_for_signature_lookup",
        "rationale": candidate.rationale,
    }


def _no_count_candidate_row(
    *,
    candidate: CandidateStudy,
    cancer_type: str,
    lookup_key: str,
    stratum_samples: pd.DataFrame,
    study_treatment: pd.DataFrame,
    reference_columns: list[str],
    count_floor: int,
    unsupported_reason: str,
    error_detail: str = "",
) -> dict[str, object]:
    sample_treatment = stratum_samples[["sample_id"]].merge(
        study_treatment[
            [
                "sample_id",
                "no_detected_treatment_signal",
                "positive_naive_or_pretreatment",
                "treatment_metadata_unknown",
            ]
        ],
        on="sample_id",
        how="left",
        validate="one_to_one",
    )
    target_present = bool(candidate.target_signatures) and all(
        _signature_present(signature, reference_columns)
        for signature in candidate.target_signatures
    )
    return {
        "study_id": candidate.study_id,
        "cancer_type": cancer_type,
        "lookup_key": lookup_key,
        "primary_patient_denominator": candidate.primary_patient_denominator,
        "target_signatures": "|".join(candidate.target_signatures),
        "target_signatures_present": target_present,
        "missing_target_signatures": "|".join(
            signature
            for signature in candidate.target_signatures
            if not _signature_present(signature, reference_columns)
        ),
        "count_floor": count_floor,
        "n_samples": int(len(stratum_samples)),
        "n_sbs_filter_passing_variants": 0,
        "n_count_floor_passing_samples": 0,
        "frac_count_floor_passing_samples": 0.0,
        "n_count_floor_passing_retained_clinical_comparator": 0,
        "has_retained_clinical_comparator": False,
        "n_no_detected_treatment_signal": int(
            sample_treatment["no_detected_treatment_signal"].sum()
        ),
        "n_positive_naive_or_pretreatment": int(
            sample_treatment["positive_naive_or_pretreatment"].sum()
        ),
        "n_treatment_metadata_unknown": int(
            sample_treatment["treatment_metadata_unknown"].sum()
        ),
        "expectation_tier": candidate.expectation_tier,
        "clinical_signal": candidate.clinical_signal,
        "has_treatment_signature_expectation": False,
        "passes_wp1_gate": False,
        "unsupported_reason": unsupported_reason,
        "rationale": candidate.rationale
        if not error_detail
        else f"{candidate.rationale}; {error_detail}",
    }


def _read_study_metadata_text(study_dir: Path) -> str:
    parts: list[str] = []
    for filename in ("meta_study.txt", "data_clinical_sample.txt"):
        path = study_dir / filename
        if path.exists():
            parts.append(path.read_text(errors="replace"))
    return "\n".join(parts).lower()


def _infer_target_signature_expectation(text: str) -> tuple[tuple[str, ...], str, str]:
    explicit_signatures: list[str] = []
    explicit_signals: list[str] = []
    if any(token in text for token in ("temozolomide", "tmz")):
        explicit_signatures.append("SBS11")
        explicit_signals.append("tmz")
    if any(
        token in text
        for token in ("platinum", "cisplatin", "carboplatin", "oxaliplatin")
    ):
        explicit_signatures.extend(["SBS31", "SBS35"])
        explicit_signals.append("platinum")
    if any(
        token in text
        for token in (
            "thiopurine",
            "azathioprine",
            "mercaptopurine",
            "6-mercaptopurine",
        )
    ):
        explicit_signatures.append("SBS87")
        explicit_signals.append("thiopurine")

    if explicit_signatures:
        return (
            tuple(dict.fromkeys(explicit_signatures)),
            "explicit",
            "|".join(explicit_signals),
        )

    if any(token in text for token in ("chemotherapy", "chemo")):
        return ("SBS11", "SBS31", "SBS35"), "generic", "generic_chemotherapy"

    return (), "none", ""


def _looks_like_pdx(text: str) -> bool:
    return any(
        token in text for token in ("pdx", "xenograft", "patient-derived xenograft")
    )


def _discovery_rationale(
    *,
    expectation_tier: str,
    clinical_signal: str,
    primary_patient_denominator: bool,
) -> str:
    denominator = (
        "primary patient denominator"
        if primary_patient_denominator
        else "PDX sensitivity-only candidate"
    )
    if expectation_tier == "none":
        return f"no detected treatment-signature metadata signal; {denominator}"
    return f"{expectation_tier} treatment-signature metadata signal: {clinical_signal}; {denominator}"


def _signature_present(signature: str, reference_columns: list[str]) -> bool:
    aliases = SPLIT_SIGNATURE_ALIASES.get(signature, [signature])
    return any(alias in set(reference_columns) for alias in aliases)


def _fraction(num: int, den: int) -> float:
    return float(num / den) if den else 0.0


def _yes_no(value: object) -> str:
    return "yes" if bool(value) else "no"


def _require_columns(frame: pd.DataFrame, required: set[str], name: str) -> None:
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"{name} missing required columns: {sorted(missing)}")


if __name__ == "__main__":
    main()
