"""
process_mc3.py

Ingests the MC3 TCGA pan-cancer unified MAF (Ellrott et al. 2018, Cell Syst; PMID 29596782)
as a single pseudo-study `tcga_mc3` in the cbioportal meta-analysis pipeline. Produces the
same per-study feather outputs that `convert_to_feather.py` produces for cBioPortal studies
(`mut.feather`, `samples.feather`, `patients.feather`, `study.feather`), so downstream rules
(`filter_genes`, `create_freq_tables`, etc.) consume MC3 identically.

Motivation
----------
cBioPortal exposes TCGA studies as a mix of legacy single-caller MAFs and newer PanCanAtlas-
derived tables. Quality is heterogeneous. MC3 is the unified 7-caller-consensus MAF covering
10,295 TCGA tumors across 33 cancer types — replacing per-study cBioPortal TCGA MAFs with
MC3 homogenizes calling quality for the TCGA portion of our cohort and adds ~25% more calls
than the older PanCan12 single-caller MAFs (Ellrott2018 Table 3). See audit F2 for
`topic:targeted-panel-sequencing-bias` + `topic:cross-study-harmonization`.

Inputs
------
- snakemake.input.mc3_maf          : `data/mc3.v0.2.8.PUBLIC.maf.gz` (GDC PASS release).
- snakemake.input.case_to_project  : `data/tcga_case_to_project.tsv` (submitter_id ->
                                      project_id; fetched once from the GDC API).

Outputs
-------
- studies/tcga_mc3/mut/table/mut.feather
- studies/tcga_mc3/metadata/samples.feather
- studies/tcga_mc3/metadata/patients.feather
- studies/tcga_mc3/metadata/study.feather

Schema is kept consistent with `convert_to_feather.py` (lowercase column names, same key
fields). Cancer type is the short TCGA project code (e.g., "BRCA", "LUAD", "COAD") derived
from the project_id after stripping the "TCGA-" prefix.

FILTER handling: only PASS variants are kept. MC3's non-PASS variants carry specific filter
flags (`oxog`, `nonpreferredpair`, `wga`, `common_in_exac`, etc.); consumers wanting non-PASS
data should use the controlled-access MC3 MAF + a custom processor.

Symbol filtering: only mutations whose Hugo_Symbol is in the project's GRCh37/GRCh38 gene
reference are kept (mirroring `convert_to_feather.py`'s filter).
"""

import sys

import pandas as pd

snek = snakemake  # type: ignore[name-defined]

mc3_path: str = snek.input.mc3_maf
case_to_project_path: str = snek.input.case_to_project
(
    out_mut_path,
    out_samples_path,
    out_patients_path,
    out_study_path,
    out_build_path,
) = snek.output

# ---------------------------------------------------------------------------
# Case-to-project mapping (submitter_id -> TCGA project_id -> cancer_type).
# ---------------------------------------------------------------------------
case_to_project = pd.read_csv(case_to_project_path, sep="\t", dtype=str)
case_to_project["cancer_type"] = (
    case_to_project["project_id"].str.replace(r"^TCGA-", "", regex=True)
)
case_to_project_map: dict[str, str] = dict(
    zip(case_to_project["submitter_id"], case_to_project["cancer_type"])
)
print(
    f"Loaded {len(case_to_project_map)} TCGA case -> project mappings covering "
    f"{case_to_project['cancer_type'].nunique()} projects",
    file=sys.stderr,
)

# ---------------------------------------------------------------------------
# Gene-symbol reference (matches convert_to_feather.py's filter).
# ---------------------------------------------------------------------------
grch37 = pd.read_csv("data/grch37.tsv", sep="\t")
grch38 = pd.read_csv("data/grch38.tsv", sep="\t")
valid_symbols: set[str] = set(grch37.symbol).union(grch38.symbol)
print(f"Reference gene set: {len(valid_symbols)} symbols (GRCh37 ∪ GRCh38)", file=sys.stderr)

# ---------------------------------------------------------------------------
# MC3 MAF ingestion. Read all columns we need, filter PASS, join to cancer_type.
# ---------------------------------------------------------------------------
mc3_cols_needed = [
    "Hugo_Symbol", "Entrez_Gene_Id", "Center", "Chromosome", "Start_Position",
    "End_Position", "Consequence", "Variant_Classification", "Variant_Type",
    "Reference_Allele", "Tumor_Seq_Allele1", "Tumor_Seq_Allele2", "dbSNP_RS",
    "Tumor_Sample_Barcode", "Matched_Norm_Sample_Barcode", "Mutation_Status",
    "HGVSp_Short", "Transcript_ID", "RefSeq", "Protein_position", "Codons", "FILTER",
]

dtypes = {
    "Hugo_Symbol": "category",
    "Center": "category",
    "Chromosome": "category",
    "Consequence": "category",
    "Variant_Classification": "category",
    "Variant_Type": "category",
    "Reference_Allele": "category",
    "Tumor_Seq_Allele1": "category",
    "Tumor_Seq_Allele2": "category",
    "Mutation_Status": "category",
    "Transcript_ID": "category",
    "RefSeq": "category",
    "Codons": "category",
    "FILTER": "category",
    "Start_Position": "Int64",
    "End_Position": "Int64",
}

print(f"Reading MC3 MAF from {mc3_path} ...", file=sys.stderr)
mut = pd.read_csv(
    mc3_path,
    sep="\t",
    comment="#",
    dtype=dtypes,
    usecols=mc3_cols_needed,
    compression="gzip",
)
print(f"  loaded {len(mut):,} total variant rows", file=sys.stderr)

# PASS-only filter (matches the open-access MC3 convention).
mut = mut[mut["FILTER"].astype(str) == "PASS"].copy()
print(f"  after FILTER=PASS: {len(mut):,} rows", file=sys.stderr)

# Symbol filter (matches convert_to_feather.py).
mut = mut[mut["Hugo_Symbol"].astype(str).isin(valid_symbols)].copy()
print(f"  after GRCh37/38 gene-symbol filter: {len(mut):,} rows", file=sys.stderr)

# ---------------------------------------------------------------------------
# Rename to the project's lowercase schema (same mapping as convert_to_feather.py).
# ---------------------------------------------------------------------------
col_mapping = {
    "Hugo_Symbol": "symbol",
    "Entrez_Gene_Id": "entrez_gene_id",
    "Center": "center",
    "Chromosome": "chromosome",
    "Start_Position": "start",
    "End_Position": "end",
    "Consequence": "consequence",
    "Variant_Classification": "variant_class",
    "Variant_Type": "variant_type",
    "Reference_Allele": "reference_allele",
    "Tumor_Seq_Allele1": "tumor_seq_allele1",
    "Tumor_Seq_Allele2": "tumor_seq_allele2",
    "dbSNP_RS": "dbsnp_rs",
    "Tumor_Sample_Barcode": "sample_id_tumor",
    "Matched_Norm_Sample_Barcode": "sample_id_norm",
    "Mutation_Status": "mutation_status",
    "HGVSp_Short": "hgvsp_short",
    "Transcript_ID": "transcript_id",
    "RefSeq": "refseq",
    "Protein_position": "protein_pos",
    "Codons": "codons",
}
mut = mut.rename(columns=col_mapping)
mut = mut[[v for v in col_mapping.values() if v in mut.columns]].reset_index(drop=True)

# ---------------------------------------------------------------------------
# Build the samples table.
#
# TCGA barcode format: TCGA-<TSS>-<participant>-<sample_vial>-<portion_analyte>-<plate>-<center>
# - patient_id  = first 12 chars (TCGA-<TSS>-<participant>)
# - sample_id   = full tumor barcode (unique per tumor specimen)
# - cancer_type = TCGA project code (stripped of "TCGA-" prefix), from the case mapping
# ---------------------------------------------------------------------------
samples = (
    mut[["sample_id_tumor"]]
    .drop_duplicates()
    .rename(columns={"sample_id_tumor": "sample_id"})
    .reset_index(drop=True)
)
samples["patient_id"] = samples["sample_id"].astype(str).str.slice(0, 12)
samples["cancer_type"] = samples["patient_id"].map(case_to_project_map).fillna("UNKNOWN")
# TCGA doesn't publish a "detailed" cancer-type column in the MC3 MAF; mirror the cBioPortal
# schema by duplicating cancer_type into cancer_type_detailed. Downstream-consumer-friendly.
samples["cancer_type_detailed"] = samples["cancer_type"]

for cat_col in ("cancer_type", "cancer_type_detailed"):
    samples[cat_col] = samples[cat_col].astype("category")

n_unknown = (samples["cancer_type"].astype(str) == "UNKNOWN").sum()
if n_unknown > 0:
    print(
        f"  WARNING: {n_unknown} samples could not be mapped to a TCGA project "
        f"(submitter_id not in data/tcga_case_to_project.tsv)",
        file=sys.stderr,
    )

# ---------------------------------------------------------------------------
# Build the patients table. MC3 MAF has no per-patient clinical metadata.
# ---------------------------------------------------------------------------
patients = (
    samples[["patient_id", "cancer_type"]]
    .drop_duplicates(subset=["patient_id"])
    .reset_index(drop=True)
)

# ---------------------------------------------------------------------------
# Build the study-summary table (matches convert_to_feather.py's shape).
# ---------------------------------------------------------------------------
study_mdat = {
    "genes": len(set(mut["symbol"])),
    "mutations": len(mut),
    "cancer_types": len(set(samples["cancer_type"])),
    "patients": len(set(samples["patient_id"])),
    "samples": len(set(samples["sample_id"])),
}
study_df = pd.DataFrame({"entity": list(study_mdat.keys()),
                         "num": list(study_mdat.values())})

# ---------------------------------------------------------------------------
# Write outputs.
# ---------------------------------------------------------------------------
mut.to_feather(out_mut_path)
samples.to_feather(out_samples_path)
patients.to_feather(out_patients_path)
study_df.to_feather(out_study_path)

# t131: persist study_build for downstream dNdScv routing.
# MC3 v0.2.8 PUBLIC is hg19/GRCh37 by definition (Ellrott 2018).
with open(out_build_path, "w") as fh:
    fh.write("hg19")

print(
    f"Wrote tcga_mc3 study: {len(mut):,} variants, "
    f"{len(samples):,} samples, {len(patients):,} patients, "
    f"{len(set(samples['cancer_type'])):,} cancer types",
    file=sys.stderr,
)
