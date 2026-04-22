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
  repeated on each signature row.
"""

import os
import re
import shutil
from pathlib import Path

import pandas as pd
import SigProfilerAssignment
from SigProfilerAssignment import Analyzer

from extract_normal_tissue_spectra import CONTEXT_96, _sigprofiler_matrix

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

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
    if "acute myeloid" in text or "myeloid" in text or "myelodysplastic" in text or "myeloproliferative" in text:
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

    raise ValueError(f"Unsupported cancer_type for COSMIC restriction lookup: {cancer_type!r}")


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


def expand_signature_aliases(requested_signatures: list[str], reference_columns: list[str]) -> list[str]:
    expanded: list[str] = []
    for signature in requested_signatures:
        if signature in SPLIT_SIGNATURE_ALIASES:
            expanded.extend([s for s in SPLIT_SIGNATURE_ALIASES[signature] if s in reference_columns])
        elif signature in reference_columns:
            expanded.append(signature)

    unique = sorted(set(expanded), key=expanded.index)
    if not unique:
        raise ValueError(f"No requested signatures were present in the reference database: {requested_signatures!r}")
    return unique


def default_signature_database_path(*, genome_build: str, cosmic_version: str, exome: bool) -> Path:
    root = Path(SigProfilerAssignment.__file__).resolve().parent
    suffix = "_exome" if exome else ""
    return root / "data" / "Reference_Signatures" / genome_build / f"COSMIC_v{cosmic_version}_SBS_{genome_build}{suffix}.txt"


def write_restricted_signature_database(
    *,
    reference_path: Path,
    requested_signatures: list[str],
    output_path: Path,
) -> Path:
    reference = pd.read_csv(reference_path, sep="\t")
    type_col = "Type" if "Type" in reference.columns else "MutationType"
    if type_col not in reference.columns:
        raise ValueError(f"Reference signature database missing Type column: {reference_path}")

    expanded = expand_signature_aliases(requested_signatures, list(reference.columns))
    subset = reference[[type_col, *expanded]].copy()
    subset.to_csv(output_path, sep="\t", index=False)
    return output_path


def study_sample_name(study_id: str, lookup_key: str) -> str:
    safe_lookup = re.sub(r"[^A-Za-z0-9]+", "_", lookup_key).strip("_")
    return f"{study_id}__{safe_lookup}"


def donor_id_for_assignment(*, sample_id: str, sample_name: str, assignment_unit: str) -> str:
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
    cancer_samples = samples.loc[samples["cancer_type"] == cancer_type, ["sample_id"]].copy()
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


def build_sigprofiler_input_matrix(variants_df: pd.DataFrame, *, assembly: str) -> pd.DataFrame:
    sbs96 = _sigprofiler_matrix(variants_df, assembly=assembly)
    return sbs96.reindex(CONTEXT_96).fillna(0).reset_index().rename(columns={"index": "MutationType"})


def run_sigprofiler_assignment(
    *,
    matrix_path: Path,
    signature_database_path: Path,
    output_dir: Path,
    genome_build: str,
    cosmic_version: str,
    exome: bool,
) -> None:
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
) -> pd.DataFrame:
    activities = pd.read_csv(
        output_dir / "Assignment_Solution" / "Activities" / "Assignment_Solution_Activities.txt",
        sep="\t",
    )
    stats = pd.read_csv(
        output_dir / "Assignment_Solution" / "Solution_Stats" / "Assignment_Solution_Samples_Stats.txt",
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

    reference_path = default_signature_database_path(
        genome_build=genome_build,
        cosmic_version=cosmic_version,
        exome=exome,
    )
    outputs: list[pd.DataFrame] = []

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
            raise ValueError(f"No signature lookup entry for normalized key {lookup_key!r}")

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
                "sample_name",
                "signature",
                "exposure",
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

    out = pd.concat(outputs, ignore_index=True)
    return out.sort_values(["cancer_type", "sample_name", "signature"]).reset_index(drop=True)


def main() -> None:
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821
    study_id = str(snek.wildcards["id"])
    genome_build = str(snek.config.get("signature_assignment_genome_build", "GRCh37"))
    cosmic_version = str(snek.config.get("signature_assignment_cosmic_version", "3.5"))
    exome = bool(snek.config.get("signature_assignment_exome", True))
    assignment_unit = str(getattr(snek.params, "assignment_unit", "study"))
    allowed_lookup_keys = set(snek.config.get("signature_assignment_lookup_keys", [])) or None
    output_path = Path(snek.output[0])
    work_dir = output_path.parent / f".{output_path.stem}_work"
    if work_dir.exists():
        shutil.rmtree(work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)

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
        )
        out.to_feather(output_path)
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
