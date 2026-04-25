#
# convert_to_feather.py
#
# Creates filtered versions of input dataset with the fields of interest, using simpler names and
# and proper column encodings.
#
import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype

from msi_normalization import log_msi_type_counts, normalize_msi_columns
from resolve_panel_id import resolve_panel_ids  # type: ignore[import-not-found]

snek = snakemake  # type: ignore[name-defined]  # noqa: F821

# load GRCh37 / GRCh38 gene metadata
grch37 = pd.read_csv("data/grch37.tsv", sep="\t")
grch38 = pd.read_csv("data/grch38.tsv", sep="\t")

# fields to encode as categoricals
cat_fields = [
    "Hugo_Symbol",
    "Center",
    "Chromosome",
    "Consequence",
    "Variant_Classification",
    "Variant_Type",
    "Reference_Allele",
    "Tumor_Seq_Allele1",
    "Tumor_Seq_Allele2",
    "Mutation_Status",
    "Transcript_ID",
    "RefSeq",
    "Codons",
]

# fields to encode as integers
int_types = []

# fallback to strings
str_types = []

# 1. work-around: non-numeric values in Start_Position
if snek.wildcards["id"] in [
    "hcc_meric_2021",
    "lusc_cptac_2021",
    "prostate_pcbm_swiss_2019",
    "prostate_dkfz_2018",
    "sclc_ucologne_2015",
]:
    str_types.append("Start_Position")
else:
    int_types.append("Start_Position")

# 2. work-around: non-numeric value encountered in sclc_ucologne_2015
if snek.wildcards["id"] in ["sclc_ucologne_2015"]:
    str_types.append("End_Position")
else:
    int_types.append("End_Position")

# 3. work-around: non-numeric values in Entrez_Gene_Id
if snek.wildcards["id"] in [
    "hnsc_mdanderson_2013",
    "stmyec_wcm_2022",
    "mixed_pipseq_2017",
    "lihc_amc_prv",
    "skcm_dfci_2015",
    "stad_pfizer_uhongkong",
    "cscc_dfarber_2015",
    "nhl_bcgsc_2011",
]:
    str_types.append("Entrez_Gene_Id")
else:
    int_types.append("Entrez_Gene_Id")

# 4. work-around: non-numeric values for Protein_position
if snek.wildcards["id"] in ["prostate_dkfz_2018"]:
    str_types.append("Protein_position")

# 5. work-around: non-numeric values for dbSNP_RS
if snek.wildcards["id"] in ["cscc_ucsf_2021"]:
    str_types.append("dbSNP_RS")

dtypes = {x: "category" for x in cat_fields}

for itype in int_types:
    dtypes[itype] = "Int64"

for stype in str_types:
    dtypes[stype] = "str"

#
# 1. mutation data
#

# work-around: problematic lines
if snek.wildcards["id"] in ["angs_painter_2020", "ccrcc_utokyo_2013"]:
    mut = pd.read_csv(
        snek.input[0],
        sep="\t",
        comment="#",
        dtype=dtypes,
        engine="python",
        on_bad_lines="warn",
    )
else:
    # low_memory=False: disable the C parser's chunked-read path. With dtype=category on
    # large MAFs (e.g. skcm_tcga_pan_can_atlas_2018 with ~4e5 rows) different chunks can
    # produce categoricals whose category arrays have different dtypes, and the internal
    # union_categoricals then raises "dtype of categories must be the same". Reading the
    # whole file in one pass avoids the union and costs only peak memory.
    mut = pd.read_csv(
        snek.input[0], sep="\t", comment="#", dtype=dtypes, low_memory=False
    )

# work-around: duplicated fields with differing case (e.g. "Codons" / "codons")
if snek.wildcards["id"] == "aml_ohsu_2018":
    mut = mut.drop(columns=["codons"])
elif snek.wildcards["id"] == "aml_ohsu_2022":
    mut = mut.drop(columns=["codons", "protein_position", "refseq"])
elif snek.wildcards["id"] == "coad_cptac_2019":
    mut = mut.drop(columns=["transcript_id"])

# use simplified field names
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

# select fields of interest, excluding any missing in dataset
cols = [x for x in col_mapping.values() if x in mut]
mut = mut[cols]

# filter out any entries with gene symbols that cannot be mapped to GRCh37 or GRCh38
mut = mut[mut.symbol.isin(grch37.symbol) | mut.symbol.isin(grch38.symbol)]

# save result
mut.to_feather(snek.output[0])


# t131: persist per-study reference build (hg19/hg38) for downstream dNdScv routing.
# Source of truth: NCBI_Build column in data_mutations.txt (present in 234/234
# cBioPortal studies surveyed; 232/234 carry a value). Rare studies with empty
# or non-standard build values are handled via study_reference_build_override
# config map. Fail loud on unknown — no silent default per AGENTS.md.
_BUILD_ALIASES = {
    "GRCh37": "hg19", "grch37": "hg19", "hg19": "hg19", "b37": "hg19", "37": "hg19",
    "GRCh38": "hg38", "grch38": "hg38", "hg38": "hg38", "b38": "hg38", "38": "hg38",
}
study_id = snek.wildcards["id"]
override_map = snek.config.get("study_reference_build_override", {}) or {}
if study_id in override_map:
    build = override_map[study_id]
    if build not in {"hg19", "hg38"}:
        raise ValueError(
            f"study_reference_build_override[{study_id!r}] = {build!r} must be "
            "'hg19' or 'hg38'"
        )
else:
    raw_build_values = pd.read_csv(
        snek.input[0], sep="\t", comment="#", usecols=["NCBI_Build"], nrows=10
    )
    raw_unique = [
        v
        for v in raw_build_values["NCBI_Build"].dropna().astype(str).str.strip().unique()
        if v
    ]
    if not raw_unique:
        raise ValueError(
            f"convert_to_feather: study {study_id!r} has empty NCBI_Build column. "
            "Add an entry to config['study_reference_build_override'] = "
            f"{{{study_id!r}: 'hg19' or 'hg38'}}."
        )
    if len(raw_unique) > 1:
        raise ValueError(
            f"convert_to_feather: study {study_id!r} has mixed NCBI_Build values "
            f"in the first 10 rows: {raw_unique}. Resolve manually via "
            "study_reference_build_override."
        )
    raw = raw_unique[0]
    if raw not in _BUILD_ALIASES:
        raise ValueError(
            f"convert_to_feather: study {study_id!r} NCBI_Build = {raw!r} not "
            f"recognized. Known aliases: {sorted(_BUILD_ALIASES)}. Override via "
            "study_reference_build_override if needed."
        )
    build = _BUILD_ALIASES[raw]

# Outputs[4] = studies/{id}/metadata/study_build.txt — single token, no trailing newline.
with open(snek.output[4], "w") as fh:
    fh.write(build)

#
# 2. sample metadata
#
dtypes = {
    "CANCER_TYPE": "category",
    "CANCER_TYPE_DETAILED": "category",
    "ONCOTREE_CODE": "category",
    "PRIMARY_SITE": "category",
    "SAMPLE_CLASS": "category",
    "SAMPLE_TYPE": "category",
    "SAMPLE_TYPE_DETAILED": "category",
    "SEQ_ASSAY_ID": "category",
}

sample_mdat = pd.read_csv(snek.input[1], sep="\t", comment="#", dtype=dtypes)

sample_mdat = sample_mdat.rename(
    columns={
        "AGE_AT_SEQ_REPORT": "age",
        "CANCER_TYPE": "cancer_type",
        "CANCER_TYPE_DETAILED": "cancer_type_detailed",
        "ONCOTREE_CODE": "oncotree_code",
        "PATIENT_ID": "patient_id",
        "PRIMARY_SITE": "primary_site",
        "SAMPLE_CLASS": "sample_class",
        "SAMPLE_ID": "sample_id",
        "SAMPLE_TYPE": "sample_type",
        "SAMPLE_TYPE_DETAILED": "sample_type_detailed",
        "SEQ_ASSAY_ID": "seq_assay_id",
    }
)

# convert age to ordinal (genie)
if "age" in sample_mdat.columns:
    # there are 6 records where age=17;
    # for simplicity, these are added to the "<18" group
    sample_mdat.loc[sample_mdat.age.values == "17", "age"] = "<18"

    # "Unknown" -> np.nan
    sample_mdat.loc[sample_mdat.age.values == "Unknown", "age"] = np.nan

    age_levels = ["<18"] + [str(x) for x in range(18, 90)] + [">89"]
    age_cat = CategoricalDtype(categories=age_levels, ordered=True)
    sample_mdat.age = sample_mdat.age.astype(age_cat)

# MSI status ingestion (t095 / t081.4). Adds normalized `msi_type` (one of
# {MSI-H, MSI-L, MSS, Indeterminate, NaN}) and numeric `msi_score` columns.
# Source columns (MSI_TYPE / MSI_STATUS / MSI_SCORE / MSI_SENSOR_SCORE) are
# detected case-sensitively in the pre-rename schema — read from the raw
# file a second time so the original uppercase column names survive.
msi_source_df = pd.read_csv(snek.input[1], sep="\t", comment="#")
msi_cols = msi_source_df[
    [
        c
        for c in msi_source_df.columns
        if c.upper() in ("MSI_TYPE", "MSI_STATUS", "MSI_SCORE", "MSI_SENSOR_SCORE")
    ]
]
msi_cols.columns = [c.upper() for c in msi_cols.columns]
msi_annotated = normalize_msi_columns(msi_cols)
sample_mdat["msi_type"] = msi_annotated["msi_type"].to_numpy()
sample_mdat["msi_score"] = msi_annotated["msi_score"].to_numpy()
log_msi_type_counts(sample_mdat, study_id=snek.wildcards["id"])

# t070: per-sample panel_id resolution. Matrix file is a conditional input;
# absence => non-panel study (resolve_panel_ids returns all-NaN).
study_id = snek.wildcards["id"]
is_panel_study = study_id in snek.config.get("panel_bearing_studies", [])
matrix_path = getattr(snek.input, "panel_matrix", None)
matrix_df = pd.read_csv(matrix_path, sep="\t", dtype=str) if matrix_path else None
sample_mdat["panel_id"] = resolve_panel_ids(
    sample_mdat,
    matrix=matrix_df,
    study_id=study_id,
    study_panel_map=snek.config.get("study_panel_map", {}),
    is_panel_study=is_panel_study,
).to_numpy()

# save result
sample_mdat.to_feather(snek.output[1])

#
# 3. patient metadata
#

dtypes = {
    "SEX": "category",
    "RACE": "category",
    "AGE": "string",
    "ETHNICITY": "category",
    "OS_STATUS": "category",
    "DFS_STATUS": "category",
    "DSS_STATUS": "category",
    "PFS_STATUS": "category",
    "SUBTYPE": "category",
    "HISTOLOGY": "category",
    "DRUG_TYPE": "category",
    "PATH_M_STAGE": "category",
    "PATH_N_STAGE": "category",
    "RADIATION_THERAPY": "category",
}

patient_mdat = pd.read_csv(snek.input[2], sep="\t", comment="#", dtype=dtypes)

patient_mdat = patient_mdat.rename(
    columns={
        "PATIENT_ID": "patient_id",
        "AGE": "age",
        "SEX": "sex",
        "RACE": "race",
        "ETHNICITY": "ethnicity",
        "OS_STATUS": "os_status",
        "OS_MONTHS": "os_months",
        "DFS_STATUS": "dfs_status",
        "DFS_MONTHS": "dfs_months",
        "DSS_STATUS": "dss_status",
        "DSS_MONTHS": "dss_months",
        "PFS_STATUS": "pfs_status",
        "PFS_MONTHS": "pfs_months",
        "SUBTYPE": "subtype",
        "PATH_M_STAGE": "path_m_stage",
        "PATH_N_STAGE": "path_n_stage",
        "HISTOLOGY": "histology",
        "DRUG_TYPE": "drug_type",
        "RADIATION_THERAPY": "radiation_therapy",
        "WEIGHT": "weight",
    }
)

# convert age to ordinal (genie)
if "age" in patient_mdat.columns:
    # there are 6 records where age=17;
    # for simplicity, these are added to the "<18" group
    patient_mdat.loc[patient_mdat.age.values == "17", "age"] = "<18"

    # "Unknown" -> np.nan
    patient_mdat.loc[patient_mdat.age.values == "Unknown", "age"] = np.nan

    age_levels = ["<18"] + [str(x) for x in range(18, 90)] + [">89"]
    age_cat = CategoricalDtype(categories=age_levels, ordered=True)
    patient_mdat.age = patient_mdat.age.astype(age_cat)

# save result
patient_mdat.to_feather(snek.output[2])

# create study metadata
study_mdat = {
    "genes": len(set(mut.symbol)),
    "mutations": mut.shape[0],
    "cancer_types": len(set(sample_mdat.cancer_type)),
    "patients": len(set(sample_mdat.patient_id)),
    "samples": len(set(sample_mdat.sample_id)),
}

df = pd.DataFrame.from_dict(study_mdat, orient="index")
df = df.reset_index()

df.columns = ["entity", "num"]

df.to_feather(snek.output[3])
