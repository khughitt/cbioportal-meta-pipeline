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

snek = snakemake  # type: ignore[name-defined]  # noqa: F821

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

study_id = snek.wildcards["id"]


def _fail(msg: str) -> None:
    raise ValueError(f"prepare_dndscv_input ({study_id}): {msg}")


# ---------------------------------------------------------------------------
# Load inputs.
# ---------------------------------------------------------------------------
mut = pd.read_feather(snek.input.mut)
samples = pd.read_feather(snek.input.samples)
with open(snek.input.build) as fh:
    build = fh.read().strip()

if build not in {"hg19", "hg38"}:
    _fail(f"study_build.txt content {build!r} not in {{hg19, hg38}}")

missing_mut = [c for c in REQUIRED_MUT_COLS if c not in mut.columns]
if missing_mut:
    _fail(f"mut.feather missing required columns: {missing_mut}")
missing_samp = [c for c in REQUIRED_SAMPLE_COLS if c not in samples.columns]
if missing_samp:
    _fail(f"samples.feather missing required columns: {missing_samp}")

# ---------------------------------------------------------------------------
# Filter to SNVs.
# ---------------------------------------------------------------------------
n_in = len(mut)
mut = mut[mut["variant_type"].astype(str) == "SNP"].copy()
n_snv = len(mut)
print(
    f"prepare_dndscv_input ({study_id}): SNV filter retained {n_snv:,} / {n_in:,} "
    f"rows ({100 * n_snv / max(n_in, 1):.1f}%)"
)

# Drop rows with empty/sentinel ref or alt.
ref = mut["reference_allele"].astype(str).str.strip()
alt = mut["tumor_seq_allele2"].astype(str).str.strip()
keep = (ref != "") & (alt != "") & (ref != "-") & (alt != "-") & (ref != "nan") & (alt != "nan")
n_pre = len(mut)
mut = mut.loc[keep].copy()
print(
    f"prepare_dndscv_input ({study_id}): allele filter retained {len(mut):,} / "
    f"{n_pre:,} rows"
)

# ---------------------------------------------------------------------------
# Build modality lookup from samples table.
# `panel_id` is populated by resolve_panel_ids in convert_to_feather.py;
# panel-bearing studies have a non-null panel_id per sample, WES studies
# have NaN.
# ---------------------------------------------------------------------------
if "panel_id" in samples.columns:
    samples_modality = samples[["sample_id"]].copy()
    samples_modality["modality"] = (
        samples["panel_id"]
        .where(samples["panel_id"].notna(), other=None)
        .map(lambda v: "panel" if v is not None and str(v) != "" else "wes")
    )
else:
    samples_modality = samples[["sample_id"]].copy()
    samples_modality["modality"] = "wes"

samples_join = samples[["sample_id", "cancer_type"]].merge(
    samples_modality, on="sample_id", how="left"
)

# ---------------------------------------------------------------------------
# Build the output frame.
# ---------------------------------------------------------------------------
out = pd.DataFrame(
    {
        "sample_id": mut["sample_id_tumor"].astype(str).values,
        "chr": mut["chromosome"].astype(str).str.replace(r"^chr", "", regex=True).values,
        "pos": pd.to_numeric(mut["start"], errors="coerce").astype("Int64").values,
        "ref": ref.loc[mut.index].values,
        "alt": alt.loc[mut.index].values,
    }
)

# Join cancer_type + modality. Inner join: rows with no sample-table entry
# cannot have cancer_type and would corrupt downstream per-cancer combine.
out = out.merge(samples_join, on="sample_id", how="inner")
print(
    f"prepare_dndscv_input ({study_id}): sample-join retained {len(out):,} rows"
)

# Drop rows where pos or chr is empty after coercion.
out = out.dropna(subset=["pos", "chr"]).copy()
out = out[out["chr"].astype(str) != ""]

# Pin schema-contract types.
out["build"] = build
out["modality"] = out["modality"].astype("category")
out["cancer_type"] = out["cancer_type"].astype("category")
out = out[["sample_id", "cancer_type", "chr", "pos", "ref", "alt", "build", "modality"]]

# Reset index so to_feather is happy.
out = out.reset_index(drop=True)
out.to_feather(snek.output[0])
print(
    f"prepare_dndscv_input ({study_id}): wrote {len(out):,} rows to {snek.output[0]}"
)
