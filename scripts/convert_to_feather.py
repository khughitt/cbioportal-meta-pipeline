#
# convert_to_feather.py
#
# Creates filtered versions of input dataset with the fields of interest, using simpler names and
# and proper column encodings.
#
import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype

snek = snakemake

# fields to encode as categoricals
cat_fields = [
    'Hugo_Symbol', 'Center', 'Chromosome', 'Consequence', 'Variant_Classification',
    'Variant_Type', 'Reference_Allele', 'Tumor_Seq_Allele1', 'Tumor_Seq_Allele2', 'Mutation_Status',
    'Transcript_ID', 'RefSeq', 'Codons'
]

# fields to encode as integers
int_types = [
    'Entrez_Gene_Id', 'Start_Position', 'End_Position', 'Protein_position'
]

dtypes = { x: 'category' for x in cat_fields }

for itype in int_types:
    dtypes[itype] = "Int64"

#
# 1. mutation data
#
mut = pd.read_csv(snek.input[0], sep='\t', comment='#', dtype=dtypes)

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
    "Codons": "codons"
}

mut = mut.rename(columns=col_mapping)
mut = mut[col_mapping.values()]

mut.to_feather(snek.output[0])

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
    "SEQ_ASSAY_ID": "category"
}

mdat = pd.read_csv(snek.input[1], sep='\t', comment='#', dtype=dtypes)

mdat = mdat.rename(columns={
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
    "SEQ_ASSAY_ID": "seq_assay_id"
})

# convert age to ordinal (genie)
if "age" in mdat.columns:
    # there are 6 records where age=17;
    # for simplicity, these are added to the "<18" group
    mdat.loc[mdat.age.values == '17', "age"] = '<18'

    # "Unknown" -> np.nan
    mdat.loc[mdat.age.values == 'Unknown', "age"] = np.nan

    age_levels = ["<18"] + [str(x) for x in range(18, 90)] + [">89"]
    age_cat = CategoricalDtype(categories=age_levels, ordered=True)
    mdat.age = mdat.age.astype(age_cat)

# save result
mdat.to_feather(snek.output[1])

# create dataset metadata
dataset_mdat = {
    "genes": len(set(mut.symbol)),
    "mutations": mut.shape[0],
    "cancer_types": len(set(mdat.cancer_type)),
    "patients": len(set(mdat.patient_id)),
    "samples": len(set(mdat.sample_id))
}

df = pd.DataFrame.from_dict(dataset_mdat, orient='index')
df = df.reset_index()

df.columns = ['entity', 'num']

df.to_feather(snek.output[2])
