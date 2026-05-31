# science:code
# status: workflow-owned
# science:end
"""
run_restricted_sigprofiler_assignment.py

Run SigProfilerAssignment on study-level or per-sample SBS96 spectra after restricting
the reference signature database to cancer-type-appropriate SBS signatures.

Input surface:
- mut.feather      — per-study mutations with sample_id_tumor / chromosome / alleles
- samples.feather  — per-study sample metadata with cancer_type
- cosmic lookup    — broad cancer-family allow-list derived from Alexandrov 2020

Output:
- restricted_assignment*.feather — long-format exposure table with fit statistics
  repeated on each signature row. Carries the t178/t179 provenance + trust columns:
  `caller_consensus` (bool/NaN per-study caller provenance), `total_sbs_count`,
  `count_floor`, `passes_count_floor`, plus the per-cancer-type decision recorded in the
  sidecar tables below.
- restricted_assignment*.signature_audit.feather — t178 sidecar: which positive-control /
  requested signatures were requested per lookup_key and whether they are present in the
  loaded COSMIC reference (loud "absorbed by nearest neighbours" warning when missing).
- restricted_assignment*.denovo_decision.feather — t179 sidecar: per-(cancer_type) decision
  table {de_novo, refit} keyed on per-cancer-type sample size + caller provenance.

t178 (signature-reference + caller-provenance audit) and t179 (per-sample count floor +
extraction-vs-refit decision rule) harden the per-sample exposures consumed by the h08
agnostic covariate-association scan (`method:h08-agnostic-association-model`). The decision
logic is deliberately *recorded only* — this script remains assignment/refit-based and does
NOT itself run a de-novo extractor. See `question:q020`, `question:q021`.

The heavy SigProfiler runtime (SigProfilerAssignment + SigProfilerMatrixGenerator, pulled in
via `extract_normal_tissue_spectra`) is imported lazily inside the functions that need it, so
the pure-python audit/decision helpers (t178/t179) can be unit-tested without that runtime.
"""

import logging
import os
import re
import shutil
from pathlib import Path

import pandas as pd

# `extract_normal_tissue_spectra` is import-cheap (it defers its own SigProfilerMatrixGenerator
# import inside `_sigprofiler_matrix`), so we bind CONTEXT_96 / _sigprofiler_matrix at module
# level. The genuinely heavy runtime — `SigProfilerAssignment` — is imported lazily inside the
# functions that need it, so the t178/t179 pure helpers can be unit-tested without it.
from extract_normal_tissue_spectra import CONTEXT_96, _sigprofiler_matrix

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

logger = logging.getLogger(__name__)
if not logging.getLogger().handlers:
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s %(name)s: %(message)s"
    )

# t178: positive-control signatures that the h08 scan relies on recovering. These must be
# audited against the *loaded* COSMIC reference at run time — if a requested signature is
# absent it would be "absorbed by nearest neighbours" during assignment, silently corrupting
# the exposure. SBS9 = AID / germinal-centre (lymphoid tissue-of-origin positive control,
# `paper:Machado2022`); SBS54 = possible-contamination / MSI discriminator (`paper:Ji2023`,
# pending germline-artefact adjudication — see `question:q021`).
POSITIVE_CONTROL_SIGNATURES: tuple[str, ...] = (
    "SBS2",
    "SBS4",
    "SBS6",
    "SBS7a",
    "SBS9",
    "SBS10a",
    "SBS13",
    "SBS15",
    "SBS26",
    "SBS54",
)

# t178: explicit default COSMIC SBS catalog version, surfaced as a config key
# (`signature_assignment_cosmic_version`) and logged + asserted at run time.
# Pinned to v3.4 — the version frozen by `pre-registration:h08-positive-control`
# (§ Total Comparison Count, "COSMIC v3.4 SBS reference"). NOTE: this is an intentional
# change from the script's historical implicit default of v3.5; both catalogs are shipped
# by SigProfilerAssignment, so set `signature_assignment_cosmic_version: "3.5"` in a run
# config to restore the old behaviour. resolve_cosmic_reference() fails loudly if the
# requested catalog is not shipped (no silent fallback to a different version).
DEFAULT_COSMIC_VERSION: str = "3.4"

# t179: per-sample SBS-count floors below which a sample's refit exposures are not trusted.
# WES floor ~383 SBS follows the SigProfilerAssignment / extraction-reliability literature
# (`paper:DiazGay2023`, `paper:Islam2022`); matched-normal / WGS samples carry far less
# germline/artefact contamination so a lower floor is defensible (`paper:Medo2024`).
DEFAULT_MIN_SBS_COUNT_WES: int = 383
DEFAULT_MIN_SBS_COUNT_MATCHED_NORMAL: int = 100

# t179: per-cancer-type sample-size threshold separating refit (assignment-to-reference, the
# safe default) from de-novo extraction. De-novo extraction needs adequate n AND consensus
# calls (`paper:Islam2022`, `paper:Medo2024`, `paper:DiazGay2023`, `paper:Pancotti2023`);
# below this, or without caller consensus, refit is the safer choice (`question:q020`).
DEFAULT_DENOVO_MIN_SAMPLES: int = 200

SPLIT_SIGNATURE_ALIASES: dict[str, list[str]] = {
    "SBS22": ["SBS22a", "SBS22b"],
    "SBS40": ["SBS40a", "SBS40b", "SBS40c"],
}
TCGA_CANCER_TYPE_MAP: dict[str, str] = {
    "ACC": "liver",
    "AML": "myeloid",
    "BLCA": "bladder",
    "BRCA": "breast",
    "CESC": "head_neck",
    "CHOL": "biliary",
    "COAD": "colorectal",
    "DLBC": "lymphoid",
    "ESCA": "esophageal",
    "GBM": "cns",
    "HNSC": "head_neck",
    "KICH": "kidney",
    "KIRC": "kidney",
    "KIRP": "kidney",
    "LAML": "myeloid",
    "LGG": "cns",
    "LIHC": "liver",
    "LUAD": "lung",
    "LUSC": "lung",
    "MESO": "soft_tissue",
    "OV": "ovary",
    "PAAD": "pancreas",
    "PRAD": "prostate",
    "READ": "colorectal",
    "SARC": "soft_tissue",
    "SKCM": "melanoma",
    "STAD": "stomach",
    "TGCT": "soft_tissue",
    "THCA": "thyroid",
    "UCEC": "uterus",
    "UCS": "uterus",
    "UVM": "melanoma",
}


def normalize_cancer_type(cancer_type: str) -> str:
    """Map heterogeneous cBioPortal cancer labels onto the broad lookup families.

    The lookup is intentionally conservative: broad cBioPortal families use the union of
    the relevant Alexandrov 2020 cancer-type columns so we do not over-exclude signatures
    when a study's label is coarser than the PCAWG nomenclature.
    """
    text = cancer_type.strip().lower()
    upper = cancer_type.strip().upper()

    if upper in TCGA_CANCER_TYPE_MAP:
        return TCGA_CANCER_TYPE_MAP[upper]

    if "breast" in text:
        return "breast"
    if "urothel" in text or "bladder" in text:
        return "bladder"
    if "melanoma" in text:
        return "melanoma"
    if "thyroid" in text:
        return "thyroid"
    if "prostate" in text:
        return "prostate"
    if "ovar" in text or "fallopian" in text:
        return "ovary"
    if "endometr" in text or "uter" in text:
        return "uterus"
    if "colorect" in text or "colon" in text or "rect" in text or "bowel" in text:
        return "colorectal"
    if "esoph" in text:
        return "esophageal"
    if "head and neck" in text or "head and neck" in text or "hnsc" in text:
        return "head_neck"
    if "cholang" in text or "biliary" in text or "gallbladder" in text:
        return "biliary"
    if "hepat" in text or "liver" in text:
        return "liver"
    if "pancre" in text or "ampull" in text:
        return "pancreas"
    if "lung" in text:
        return "lung"
    if "kidney" in text or "renal" in text:
        return "kidney"
    if (
        "glioblast" in text
        or "glioma" in text
        or "astrocyt" in text
        or "medulloblast" in text
        or "ependym" in text
        or "cns" in text
        or "brain" in text
    ):
        return "cns"
    if (
        "acute myeloid" in text
        or "myeloid" in text
        or "myelodysplastic" in text
        or "myeloproliferative" in text
    ):
        return "myeloid"
    if (
        "lymph" in text
        or "b-cell" in text
        or "b lymph" in text
        or "t-cell" in text
        or "hodgkin" in text
        or "mature b-cell" in text
    ):
        return "lymphoid"
    if "sarcoma" in text or "soft tissue" in text:
        return "soft_tissue"
    if "bone" in text or "osteosar" in text:
        return "bone"
    if "stomach" in text or "gastric" in text or "esophagogastric" in text:
        return "stomach"

    raise ValueError(
        f"Unsupported cancer_type for COSMIC restriction lookup: {cancer_type!r}"
    )


def load_signature_lookup(path: Path) -> dict[str, list[str]]:
    df = pd.read_csv(path, sep="\t", dtype=str)
    required = {"lookup_key", "figure_cancer_type", "signature"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Lookup table missing required columns: {sorted(missing)}")

    grouped: dict[str, list[str]] = {}
    for lookup_key, grp in df.groupby("lookup_key", sort=False):
        signatures = sorted(set(grp["signature"]))
        grouped[str(lookup_key)] = signatures
    return grouped


def expand_signature_aliases(
    requested_signatures: list[str], reference_columns: list[str]
) -> list[str]:
    expanded: list[str] = []
    for signature in requested_signatures:
        if signature in SPLIT_SIGNATURE_ALIASES:
            expanded.extend(
                [
                    s
                    for s in SPLIT_SIGNATURE_ALIASES[signature]
                    if s in reference_columns
                ]
            )
        elif signature in reference_columns:
            expanded.append(signature)

    unique = sorted(set(expanded), key=expanded.index)
    if not unique:
        raise ValueError(
            f"No requested signatures were present in the reference database: {requested_signatures!r}"
        )
    return unique


def default_signature_database_path(
    *, genome_build: str, cosmic_version: str, exome: bool
) -> Path:
    import SigProfilerAssignment

    module_file = SigProfilerAssignment.__file__
    if module_file is None:
        raise RuntimeError("Could not locate SigProfilerAssignment package directory.")
    root = Path(module_file).resolve().parent
    suffix = "_exome" if exome else ""
    return (
        root
        / "data"
        / "Reference_Signatures"
        / genome_build
        / f"COSMIC_v{cosmic_version}_SBS_{genome_build}{suffix}.txt"
    )


def resolve_cosmic_reference(
    *, genome_build: str, cosmic_version: str, exome: bool
) -> Path:
    """Resolve, confirm, and log the COSMIC SBS reference that will be loaded (t178 item 1).

    The COSMIC catalog version is otherwise implicit (it is only embedded in the resolved
    file name). This makes the resolved version explicit and loud, and fails early if the
    expected catalog file is not present rather than letting SigProfilerAssignment fall back
    to some other version.
    """
    reference_path = default_signature_database_path(
        genome_build=genome_build, cosmic_version=cosmic_version, exome=exome
    )
    if not reference_path.exists():
        raise FileNotFoundError(
            f"Expected COSMIC SBS reference not found: {reference_path}. Confirm "
            f"signature_assignment_cosmic_version={cosmic_version!r} is shipped by the "
            "installed SigProfilerAssignment package."
        )
    logger.info(
        "t178: resolved COSMIC SBS reference v%s %s (exome=%s) -> %s",
        cosmic_version,
        genome_build,
        exome,
        reference_path,
    )
    return reference_path


def read_reference_signature_columns(reference_path: Path) -> list[str]:
    """Return the signature column names present in a COSMIC reference (excludes Type col)."""
    header = pd.read_csv(reference_path, sep="\t", nrows=0)
    type_col = "Type" if "Type" in header.columns else "MutationType"
    return [c for c in header.columns if c != type_col]


def audit_signature_presence(
    *,
    requested_signatures: list[str],
    reference_columns: list[str],
    lookup_key: str,
) -> pd.DataFrame:
    """Audit requested signatures (incl. positive controls) against the loaded reference.

    A requested signature that is absent from the reference would be silently "absorbed by
    nearest neighbours" during assignment; per the project's loud-missingness covenant we
    emit a warning naming each missing signature and record the audit for the sidecar.

    Split-alias signatures (e.g. SBS40 -> SBS40a/b/c) count as present when *any* of their
    aliases is in the reference.
    """
    reference_set = set(reference_columns)
    audited = sorted(set(requested_signatures) | set(POSITIVE_CONTROL_SIGNATURES))
    rows: list[dict[str, object]] = []
    for signature in audited:
        aliases = SPLIT_SIGNATURE_ALIASES.get(signature, [signature])
        present_aliases = [a for a in aliases if a in reference_set]
        present = bool(present_aliases)
        is_positive_control = signature in POSITIVE_CONTROL_SIGNATURES
        is_requested = signature in set(requested_signatures)
        if not present and (is_requested or is_positive_control):
            logger.warning(
                "t178: requested signature %s is ABSENT from the loaded COSMIC reference "
                "(lookup_key=%s, positive_control=%s) — it would be absorbed by nearest "
                "neighbours; NOT silently proceeding without flagging.",
                signature,
                lookup_key,
                is_positive_control,
            )
        rows.append(
            {
                "lookup_key": lookup_key,
                "signature": signature,
                "requested": is_requested,
                "positive_control": is_positive_control,
                "present_in_reference": present,
                "matched_aliases": "|".join(present_aliases),
            }
        )
    return pd.DataFrame(rows)


def write_restricted_signature_database(
    *,
    reference_path: Path,
    requested_signatures: list[str],
    output_path: Path,
) -> Path:
    reference = pd.read_csv(reference_path, sep="\t")
    type_col = "Type" if "Type" in reference.columns else "MutationType"
    if type_col not in reference.columns:
        raise ValueError(
            f"Reference signature database missing Type column: {reference_path}"
        )

    expanded = expand_signature_aliases(requested_signatures, list(reference.columns))
    subset = reference[[type_col, *expanded]].copy()
    subset.to_csv(output_path, sep="\t", index=False)
    return output_path


def study_sample_name(study_id: str, lookup_key: str) -> str:
    safe_lookup = re.sub(r"[^A-Za-z0-9]+", "_", lookup_key).strip("_")
    return f"{study_id}__{safe_lookup}"


def donor_id_for_assignment(
    *, sample_id: str, sample_name: str, assignment_unit: str
) -> str:
    if assignment_unit == "study":
        return sample_name
    if assignment_unit == "sample":
        return sample_id
    raise ValueError(f"Unsupported assignment_unit: {assignment_unit!r}")


def normalize_chromosome_label(chromosome: str) -> str:
    text = chromosome.strip()
    if not text:
        return text

    upper = text.upper()
    if upper.startswith("CHR"):
        suffix = upper[3:]
    else:
        suffix = upper

    if suffix in {str(i) for i in range(1, 23)} | {"X", "Y"}:
        return f"chr{suffix}"
    return text


def prepare_sigprofiler_variants(
    *,
    mutations: pd.DataFrame,
    samples: pd.DataFrame,
    cancer_type: str,
    sample_name: str,
    assignment_unit: str,
) -> pd.DataFrame:
    cancer_samples = samples.loc[
        samples["cancer_type"] == cancer_type, ["sample_id"]
    ].copy()
    sample_ids = set(cancer_samples["sample_id"])
    subset = mutations.loc[mutations["sample_id_tumor"].isin(sample_ids)].copy()
    if subset.empty:
        return pd.DataFrame(columns=["donor_id", "chrom", "pos", "ref", "alt"])

    donor_map = {
        sample_id: donor_id_for_assignment(
            sample_id=sample_id,
            sample_name=sample_name,
            assignment_unit=assignment_unit,
        )
        for sample_id in cancer_samples["sample_id"].astype(str)
    }
    out = pd.DataFrame(
        {
            "donor_id": subset["sample_id_tumor"].astype(str).map(donor_map),
            "chrom": subset["chromosome"].astype(str).map(normalize_chromosome_label),
            "pos": subset["start"].astype(int),
            "ref": subset["reference_allele"].astype(str),
            "alt": subset["tumor_seq_allele2"].astype(str),
        }
    )
    out = out.loc[
        out["chrom"].isin([f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"])
        & (out["ref"].str.len() == 1)
        & (out["alt"].str.len() == 1)
        & out["ref"].isin(list("ACGT"))
        & out["alt"].isin(list("ACGT"))
    ].copy()
    return out


def build_sigprofiler_input_matrix(
    variants_df: pd.DataFrame, *, assembly: str
) -> pd.DataFrame:
    sbs96 = _sigprofiler_matrix(variants_df, assembly=assembly)
    return (
        sbs96.reindex(CONTEXT_96)
        .fillna(0)
        .reset_index()
        .rename(columns={"index": "MutationType"})
    )


def run_sigprofiler_assignment(
    *,
    matrix_path: Path,
    signature_database_path: Path,
    output_dir: Path,
    genome_build: str,
    cosmic_version: str,
    exome: bool,
) -> None:
    from SigProfilerAssignment import Analyzer

    Analyzer.cosmic_fit(
        samples=str(matrix_path),
        output=str(output_dir),
        signature_database=str(signature_database_path),
        input_type="matrix",
        context_type="96",
        collapse_to_SBS96=True,
        genome_build=genome_build,
        cosmic_version=float(cosmic_version),
        make_plots=False,
        sample_reconstruction_plots=False,
        export_probabilities=False,
        add_background_signatures=False,
        exome=exome,
        cpu=1,
        verbose=False,
    )


def read_assignment_output(
    *,
    output_dir: Path,
    study_id: str,
    cancer_type: str,
    lookup_key: str,
    figure_cancer_type: str,
    assignment_unit: str,
    caller_consensus: bool | None = None,
) -> pd.DataFrame:
    activities = pd.read_csv(
        output_dir
        / "Assignment_Solution"
        / "Activities"
        / "Assignment_Solution_Activities.txt",
        sep="\t",
    )
    stats = pd.read_csv(
        output_dir
        / "Assignment_Solution"
        / "Solution_Stats"
        / "Assignment_Solution_Samples_Stats.txt",
        sep="\t",
    )

    activities = activities.rename(columns={"Samples": "sample_name"})
    stats = stats.rename(columns={"Sample Names": "sample_name"})

    long = activities.melt(
        id_vars=["sample_name"],
        var_name="signature",
        value_name="exposure",
    )
    out = long.merge(stats, on="sample_name", how="left", validate="many_to_one")
    out.insert(0, "study_id", study_id)
    out.insert(1, "cancer_type", cancer_type)
    out.insert(2, "lookup_key", lookup_key)
    out.insert(3, "figure_cancer_type", figure_cancer_type)
    out.insert(4, "assignment_unit", assignment_unit)
    out["caller_consensus"] = caller_consensus
    out["status"] = "ok"
    out = out.rename(
        columns={
            "Total Mutations": "total_mutations",
            "Cosine Similarity": "cosine_similarity",
            "L1 Norm": "l1_norm",
            "L1_Norm_%": "l1_norm_pct",
            "L2 Norm": "l2_norm",
            "L2_Norm_%": "l2_norm_pct",
            "KL Divergence": "kl_divergence",
            "Correlation": "correlation",
        }
    )
    return out


def resolve_caller_consensus(
    *,
    study_id: str,
    multi_caller_consensus_studies: set[str],
    single_caller_studies: set[str],
) -> bool | None:
    """Resolve a study's variant-caller-consensus provenance (t178 item 3).

    Polarity is chosen so the *safe default is unknown*: a study that appears in neither
    config list returns ``None`` (provenance unknown, must not be assumed consensus). This
    mirrors the `matched_normal_studies` pattern but with an explicit three-state result so
    the downstream h08 scan can guard on single-caller artefacts (`paper:Jiang2025`).
    """
    in_multi = study_id in multi_caller_consensus_studies
    in_single = study_id in single_caller_studies
    if in_multi and in_single:
        raise ValueError(
            f"Study {study_id!r} is listed in both multi_caller_consensus_studies and "
            "single_caller_studies — caller provenance is contradictory."
        )
    if in_multi:
        return True
    if in_single:
        return False
    logger.warning(
        "t178: variant-caller provenance for study %s is UNKNOWN (absent from both "
        "multi_caller_consensus_studies and single_caller_studies) — marking "
        "caller_consensus=None; NOT assuming consensus.",
        study_id,
    )
    return None


def count_floor_for_sample(
    *,
    caller_consensus: bool | None,
    matched_normal: bool,
    min_sbs_count_wes: int,
    min_sbs_count_matched_normal: int,
) -> int:
    """Return the per-sample SBS-count floor applicable to a sample (t179 item 1).

    Matched-normal (and, by the same provenance argument, consensus-called) samples carry
    less germline/artefact contamination, so the lower floor applies; everything else uses
    the conservative WES floor.
    """
    if matched_normal:
        return min_sbs_count_matched_normal
    return min_sbs_count_wes


def annotate_count_floor(
    table: pd.DataFrame,
    *,
    count_floor: int,
) -> pd.DataFrame:
    """Add `total_sbs_count`, `count_floor`, `passes_count_floor` to a long exposure table.

    `total_sbs_count` is the per-sample sum of assigned exposures (one value per sample,
    broadcast across that sample's signature rows). Loud missingness: rather than dropping
    sub-floor samples, we flag them so a downstream low-count audit can see exactly what was
    excluded from the trusted-exposure set.
    """
    out = table.copy()
    per_sample_total = out.groupby("sample_name")["exposure"].transform("sum")
    out["total_sbs_count"] = per_sample_total
    out["count_floor"] = count_floor
    out["passes_count_floor"] = per_sample_total >= count_floor
    return out


def build_low_count_audit(table: pd.DataFrame) -> pd.DataFrame:
    """Per-sample audit of samples failing the count floor (t179 item 1, loud missingness)."""
    if table.empty:
        return pd.DataFrame(
            columns=[
                "study_id",
                "cancer_type",
                "lookup_key",
                "assignment_unit",
                "sample_name",
                "total_sbs_count",
                "count_floor",
                "reason",
            ]
        )
    per_sample = (
        table[
            [
                "study_id",
                "cancer_type",
                "lookup_key",
                "assignment_unit",
                "sample_name",
                "total_sbs_count",
                "count_floor",
                "passes_count_floor",
            ]
        ]
        .drop_duplicates("sample_name")
        .reset_index(drop=True)
    )
    failed = per_sample.loc[~per_sample["passes_count_floor"]].copy()
    failed["reason"] = "below_count_floor"
    return failed.drop(columns=["passes_count_floor"]).reset_index(drop=True)


def decide_denovo_vs_refit(
    *,
    n_samples: int,
    caller_consensus: bool | None,
    denovo_min_samples: int,
) -> str:
    """Per-cancer-type de-novo-vs-refit decision (t179 item 2; records, does not extract).

    De-novo extraction is warranted only when the stratum is both adequately sized AND
    consensus-called. Unknown caller provenance is treated conservatively (NOT consensus),
    so it forces ``refit``. This script never runs de-novo extraction; the verdict is
    recorded so a future extractor can act on it.
    """
    if caller_consensus is True and n_samples >= denovo_min_samples:
        return "de_novo"
    return "refit"


def build_denovo_decision_table(
    *,
    samples: pd.DataFrame,
    study_id: str,
    caller_consensus: bool | None,
    denovo_min_samples: int,
    allowed_lookup_keys: set[str] | None,
) -> pd.DataFrame:
    """Per-(cancer_type) decision table {de_novo, refit} (t179 item 2)."""
    rows: list[dict[str, object]] = []
    for cancer_type in sorted(samples["cancer_type"].dropna().astype(str).unique()):
        try:
            lookup_key = normalize_cancer_type(cancer_type)
        except ValueError:
            if allowed_lookup_keys is not None:
                continue
            raise
        if allowed_lookup_keys is not None and lookup_key not in allowed_lookup_keys:
            continue
        n_samples = int((samples["cancer_type"].astype(str) == cancer_type).sum())
        decision = decide_denovo_vs_refit(
            n_samples=n_samples,
            caller_consensus=caller_consensus,
            denovo_min_samples=denovo_min_samples,
        )
        logger.info(
            "t179: study=%s cancer_type=%s n=%d caller_consensus=%s -> decision=%s "
            "(threshold=%d)",
            study_id,
            cancer_type,
            n_samples,
            caller_consensus,
            decision,
            denovo_min_samples,
        )
        rows.append(
            {
                "study_id": study_id,
                "cancer_type": cancer_type,
                "lookup_key": lookup_key,
                "n_samples": n_samples,
                "caller_consensus": caller_consensus,
                "denovo_min_samples": denovo_min_samples,
                "decision": decision,
            }
        )
    return pd.DataFrame(rows)


def build_assignment_table_for_study(  # noqa: PLR0913
    *,
    study_id: str,
    mutations_path: Path,
    samples_path: Path,
    lookup_path: Path,
    genome_build: str,
    cosmic_version: str,
    exome: bool,
    work_dir: Path,
    assignment_unit: str = "study",
    allowed_lookup_keys: set[str] | None = None,
    caller_consensus: bool | None = None,
    matched_normal: bool = False,
    min_sbs_count_wes: int = DEFAULT_MIN_SBS_COUNT_WES,
    min_sbs_count_matched_normal: int = DEFAULT_MIN_SBS_COUNT_MATCHED_NORMAL,
    signature_audit_out: list[pd.DataFrame] | None = None,
) -> pd.DataFrame:
    mutations = pd.read_feather(mutations_path)
    samples = pd.read_feather(samples_path)
    lookup = load_signature_lookup(lookup_path)
    figure_sources = (
        pd.read_csv(lookup_path, sep="\t", dtype=str)
        .groupby("lookup_key", sort=False)["figure_cancer_type"]
        .apply(lambda s: "|".join(sorted(set(s))))
        .to_dict()
    )

    reference_path = resolve_cosmic_reference(
        genome_build=genome_build,
        cosmic_version=cosmic_version,
        exome=exome,
    )
    reference_columns = read_reference_signature_columns(reference_path)
    outputs: list[pd.DataFrame] = []
    audit_frames: list[pd.DataFrame] = []

    for cancer_type in sorted(samples["cancer_type"].dropna().astype(str).unique()):
        try:
            lookup_key = normalize_cancer_type(cancer_type)
        except ValueError:
            if allowed_lookup_keys is not None:
                continue
            raise

        if allowed_lookup_keys is not None and lookup_key not in allowed_lookup_keys:
            continue
        if lookup_key not in lookup:
            raise ValueError(
                f"No signature lookup entry for normalized key {lookup_key!r}"
            )

        audit_frames.append(
            audit_signature_presence(
                requested_signatures=lookup[lookup_key],
                reference_columns=reference_columns,
                lookup_key=lookup_key,
            )
        )

        sample_name = study_sample_name(study_id, lookup_key)
        variants = prepare_sigprofiler_variants(
            mutations=mutations,
            samples=samples,
            cancer_type=cancer_type,
            sample_name=sample_name,
            assignment_unit=assignment_unit,
        )
        if variants.empty:
            continue

        group_dir = work_dir / sample_name
        group_dir.mkdir(parents=True, exist_ok=True)
        matrix_path = group_dir / "sample_matrix.tsv"
        signature_db_path = group_dir / "restricted_signatures.tsv"
        assignment_dir = group_dir / "assignment"

        matrix = build_sigprofiler_input_matrix(variants, assembly=genome_build)
        matrix.to_csv(matrix_path, sep="\t", index=False)
        write_restricted_signature_database(
            reference_path=reference_path,
            requested_signatures=lookup[lookup_key],
            output_path=signature_db_path,
        )
        run_sigprofiler_assignment(
            matrix_path=matrix_path,
            signature_database_path=signature_db_path,
            output_dir=assignment_dir,
            genome_build=genome_build,
            cosmic_version=cosmic_version,
            exome=exome,
        )
        outputs.append(
            read_assignment_output(
                output_dir=assignment_dir,
                study_id=study_id,
                cancer_type=cancer_type,
                lookup_key=lookup_key,
                figure_cancer_type=figure_sources[lookup_key],
                assignment_unit=assignment_unit,
                caller_consensus=caller_consensus,
            )
        )

    if signature_audit_out is not None:
        signature_audit_out.append(
            pd.concat(audit_frames, ignore_index=True)
            if audit_frames
            else pd.DataFrame(
                columns=[
                    "lookup_key",
                    "signature",
                    "requested",
                    "positive_control",
                    "present_in_reference",
                    "matched_aliases",
                ]
            )
        )

    if not outputs:
        return pd.DataFrame(
            columns=[
                "study_id",
                "cancer_type",
                "lookup_key",
                "figure_cancer_type",
                "assignment_unit",
                "caller_consensus",
                "sample_name",
                "signature",
                "exposure",
                "total_sbs_count",
                "count_floor",
                "passes_count_floor",
                "total_mutations",
                "cosine_similarity",
                "l1_norm",
                "l1_norm_pct",
                "l2_norm",
                "l2_norm_pct",
                "kl_divergence",
                "correlation",
                "status",
            ]
        )

    count_floor = count_floor_for_sample(
        caller_consensus=caller_consensus,
        matched_normal=matched_normal,
        min_sbs_count_wes=min_sbs_count_wes,
        min_sbs_count_matched_normal=min_sbs_count_matched_normal,
    )
    out = pd.concat(outputs, ignore_index=True)
    out = annotate_count_floor(out, count_floor=count_floor)
    n_failed = int((~out.drop_duplicates("sample_name")["passes_count_floor"]).sum())
    if n_failed:
        logger.warning(
            "t179: %d sample(s) in study %s fell below the SBS count floor (%d) and are "
            "flagged passes_count_floor=False (loud missingness — not silently dropped).",
            n_failed,
            study_id,
            count_floor,
        )
    return out.sort_values(["cancer_type", "sample_name", "signature"]).reset_index(
        drop=True
    )


def main() -> None:
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821
    study_id = str(snek.wildcards["id"])
    genome_build = str(snek.config.get("signature_assignment_genome_build", "GRCh37"))
    cosmic_version = str(
        snek.config.get("signature_assignment_cosmic_version", DEFAULT_COSMIC_VERSION)
    )
    exome = bool(snek.config.get("signature_assignment_exome", True))
    assignment_unit = str(getattr(snek.params, "assignment_unit", "study"))
    allowed_lookup_keys = (
        set(snek.config.get("signature_assignment_lookup_keys", [])) or None
    )

    # t178: per-study variant-caller provenance + matched-normal flags.
    multi_caller_consensus_studies = set(
        snek.config.get("multi_caller_consensus_studies", [])
    )
    single_caller_studies = set(snek.config.get("single_caller_studies", []))
    matched_normal_studies = set(snek.config.get("matched_normal_studies", []))
    caller_consensus = resolve_caller_consensus(
        study_id=study_id,
        multi_caller_consensus_studies=multi_caller_consensus_studies,
        single_caller_studies=single_caller_studies,
    )
    matched_normal = study_id in matched_normal_studies

    # t179: per-sample count floors + de-novo-vs-refit sample-size threshold.
    min_sbs_count_wes = int(
        snek.config.get("signature_min_sbs_count_wes", DEFAULT_MIN_SBS_COUNT_WES)
    )
    min_sbs_count_matched_normal = int(
        snek.config.get(
            "signature_min_sbs_count_matched_normal",
            DEFAULT_MIN_SBS_COUNT_MATCHED_NORMAL,
        )
    )
    denovo_min_samples = int(
        snek.config.get("signature_denovo_min_samples", DEFAULT_DENOVO_MIN_SAMPLES)
    )

    output_path = Path(snek.output[0])
    audit_path = output_path.with_suffix(".signature_audit.feather")
    decision_path = output_path.with_suffix(".denovo_decision.feather")
    work_dir = output_path.parent / f".{output_path.stem}_work"
    if work_dir.exists():
        shutil.rmtree(work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)

    signature_audit_out: list[pd.DataFrame] = []
    try:
        out = build_assignment_table_for_study(
            study_id=study_id,
            mutations_path=Path(snek.input["mutations"]),
            samples_path=Path(snek.input["samples"]),
            lookup_path=Path(snek.input["lookup"]),
            genome_build=genome_build,
            cosmic_version=cosmic_version,
            exome=exome,
            work_dir=work_dir,
            assignment_unit=assignment_unit,
            allowed_lookup_keys=allowed_lookup_keys,
            caller_consensus=caller_consensus,
            matched_normal=matched_normal,
            min_sbs_count_wes=min_sbs_count_wes,
            min_sbs_count_matched_normal=min_sbs_count_matched_normal,
            signature_audit_out=signature_audit_out,
        )
        out.to_feather(output_path)

        # t178 sidecar: signature presence audit.
        audit = (
            signature_audit_out[0]
            if signature_audit_out
            else pd.DataFrame(
                columns=[
                    "lookup_key",
                    "signature",
                    "requested",
                    "positive_control",
                    "present_in_reference",
                    "matched_aliases",
                ]
            )
        )
        audit.to_feather(audit_path)

        # t179 sidecar: per-cancer-type de-novo-vs-refit decision table.
        samples = pd.read_feather(Path(snek.input["samples"]))
        decision = build_denovo_decision_table(
            samples=samples,
            study_id=study_id,
            caller_consensus=caller_consensus,
            denovo_min_samples=denovo_min_samples,
            allowed_lookup_keys=allowed_lookup_keys,
        )
        decision.to_feather(decision_path)
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
