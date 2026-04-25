#
# prepare_dndscv_input.py (t131)
#
# Prepare a single-study, schema-validated input feather for the dNdScv pipeline.
# Consumes the unfiltered mut.feather (NOT mut_filtered.feather — the filter
# censors low-coverage genes which would miscalibrate dNdScv's trinucleotide
# background; see doc/plans/2026-04-24-t131-dndscv-three-way-comparison-design.md
# §"Latent bug found during planning").
#
# Inputs (snek.input):
#   mut       — studies/{id}/mut/table/mut.feather   (unfiltered)
#   samples   — studies/{id}/metadata/samples.feather
#   build     — studies/{id}/metadata/study_build.txt   (single token: "hg19" / "hg38")
#
# Output (snek.output):
#   studies/{id}/mut/dndscv_input.feather
#
# Output schema (lowercase, dndscv-friendly):
#   sample_id (str), cancer_type (category), chr (str, no "chr" prefix),
#   pos (int64), ref (str), alt (str), build (str), modality (category: wes/panel)
#
# Filters applied:
#   - SNV-only (variant_type == "SNP"). dndscv handles indels separately
#     (wind_cv); Phase 1 reports only the qglobal_cv signal.
#   - Drops rows with empty / "-" ref or alt.
#   - Drops rows whose sample_id has no row in samples.feather (cannot infer
#     cancer_type or modality).
#
import pandas as pd

REQUIRED_MUT_COLS = (
    "sample_id_tumor",
    "chromosome",
    "start",
    "reference_allele",
    "tumor_seq_allele2",
    "variant_type",
    "symbol",
)
REQUIRED_SAMPLE_COLS = ("sample_id", "cancer_type")
OUTPUT_SCHEMA = [
    "sample_id",
    "cancer_type",
    "chr",
    "pos",
    "ref",
    "alt",
    "build",
    "modality",
]


def prepare_dndscv_input(
    mut: pd.DataFrame,
    samples: pd.DataFrame,
    build: str,
    study_id: str = "<test>",
) -> pd.DataFrame:
    """Pure-Python core: validate inputs, filter to SNVs, attach
    ``cancer_type`` + ``modality`` per sample, and emit the dndscv input
    schema. Snakemake glue (file I/O) lives in ``_run_via_snakemake``.

    All sample_id columns are coerced to str so the join survives studies
    that store integer sample IDs (e.g. pog570_bcgsc_2020).
    """
    if build not in {"hg19", "hg38"}:
        raise ValueError(
            f"prepare_dndscv_input ({study_id}): study_build={build!r} not in {{hg19, hg38}}"
        )

    missing_mut = [c for c in REQUIRED_MUT_COLS if c not in mut.columns]
    if missing_mut:
        raise ValueError(
            f"prepare_dndscv_input ({study_id}): mut missing columns: {missing_mut}"
        )
    missing_samp = [c for c in REQUIRED_SAMPLE_COLS if c not in samples.columns]
    if missing_samp:
        raise ValueError(
            f"prepare_dndscv_input ({study_id}): samples missing columns: {missing_samp}"
        )

    # SNV-only filter (dndscv's per-codon background applies to SNVs).
    mut_snv = mut[mut["variant_type"].astype(str) == "SNP"].copy()

    # Drop rows with empty/sentinel ref or alt.
    ref = mut_snv["reference_allele"].astype(str).str.strip()
    alt = mut_snv["tumor_seq_allele2"].astype(str).str.strip()
    keep = (
        (ref != "")
        & (alt != "")
        & (ref != "-")
        & (alt != "-")
        & (ref != "nan")
        & (alt != "nan")
    )
    mut_snv = mut_snv.loc[keep].copy()

    # Build modality lookup from samples table. `panel_id` is populated by
    # resolve_panel_ids in convert_to_feather.py; panel-bearing studies have
    # a non-null panel_id per sample, WES studies have NaN.
    samples_modality = samples[["sample_id"]].copy()
    if "panel_id" in samples.columns:
        # NaN/None/empty-string → wes; any populated value → panel.
        # (Naive `.map(lambda v: 'panel' if str(v) != '' else 'wes')` mis-tags
        # NaN as 'panel' because str(NaN) == 'nan'.)
        has_panel = samples["panel_id"].notna() & (
            samples["panel_id"].astype(str).str.strip() != ""
        )
        samples_modality["modality"] = has_panel.map(
            {True: "panel", False: "wes"}
        ).astype(str)
    else:
        samples_modality["modality"] = "wes"

    samples_join = samples[["sample_id", "cancer_type"]].merge(
        samples_modality, on="sample_id", how="left"
    )
    # Some studies (pog570_bcgsc_2020) store sample_id as int64; the mut-side
    # cast below forces str, so coerce samples-side too to keep merge dtypes
    # aligned.
    samples_join["sample_id"] = samples_join["sample_id"].astype(str)

    out = pd.DataFrame(
        {
            "sample_id": mut_snv["sample_id_tumor"].astype(str).values,
            "chr": mut_snv["chromosome"].astype(str).str.replace(r"^chr", "", regex=True).values,
            "pos": pd.to_numeric(mut_snv["start"], errors="coerce").astype("Int64").values,
            "ref": ref.loc[mut_snv.index].values,
            "alt": alt.loc[mut_snv.index].values,
        }
    )

    # Inner join: rows with no sample-table entry have no cancer_type and
    # would corrupt downstream per-cancer combine.
    out = out.merge(samples_join, on="sample_id", how="inner")

    # Drop rows where pos or chr coerced to NA / empty.
    out = out.dropna(subset=["pos", "chr"]).copy()
    out = out[out["chr"].astype(str) != ""]

    out["build"] = build
    out["modality"] = out["modality"].astype("category")
    out["cancer_type"] = out["cancer_type"].astype("category")
    out = out[OUTPUT_SCHEMA].reset_index(drop=True)
    return out


def _run_via_snakemake() -> None:
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821
    study_id = snek.wildcards["id"]
    mut = pd.read_feather(snek.input.mut)
    samples = pd.read_feather(snek.input.samples)
    with open(snek.input.build) as fh:
        build = fh.read().strip()

    n_in = len(mut)
    out = prepare_dndscv_input(mut, samples, build, study_id=study_id)
    print(
        f"prepare_dndscv_input ({study_id}): wrote {len(out):,} / {n_in:,} rows "
        f"to {snek.output[0]}"
    )
    out.to_feather(snek.output[0])


if "snakemake" in globals():
    _run_via_snakemake()
