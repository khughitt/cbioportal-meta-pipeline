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

#
# 1. mutation data
#
mut = pd.read_csv(snek.input[0], sep='\t', dtype={"Chromosome": "category"})

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

mut = mut.astype({
    "symbol": "category",
    "entrez_gene_id": "category",
    "center": "category",
    "consequence": "category",
    "variant_class": "category",
    "variant_type": "category",
    "reference_allele": "category",
    "tumor_seq_allele1": "category",
    "tumor_seq_allele2": "category",
    "mutation_status": "category",
    "transcript_id": "category",
    "refseq": "category",
    "codons": "category"
})

mut.to_feather(snek.output[0])

#
# 2. sample metadata
#
mdat = pd.read_csv(snek.input[1], sep='\t', skiprows=4)

mdat = mdat.rename(columns={
    "PATIENT_ID": "patient_id",
    "AGE_AT_SEQ_REPORT": "age",
    "ONCOTREE_CODE": "oncotree_code",
    "SAMPLE_ID": "sample_id",
    "SAMPLE_TYPE": "sample_type",
    "SEQ_ASSAY_ID": "seq_assay_id",
    "CANCER_TYPE": "cancer_type",
    "CANCER_TYPE_DETAILED": "cancer_type_detailed",
    "SAMPLE_TYPE_DETAILED": "sample_type_detailed",
    "SAMPLE_CLASS": "sample_class"
})

mdat = mdat.astype({
    "age": "category",
    "oncotree_code": "category",
    "sample_type": "category",
    "seq_assay_id": "category",
    "cancer_type": "category",
    "cancer_type_detailed": "category",
    "sample_type_detailed": "category",
    "sample_class": "category",
})

# convert age to ordinal

# feb25: there are 6 records where age=17; for simplicity, these are added to the "<18" group
mdat.loc[mdat.age.values == '17', "age"] = '<18'

# "Unknown" -> np.nan
mdat.loc[mdat.age.values == 'Unknown', "age"] = np.nan

age_levels = ["<18"] + [str(x) for x in range(18, 90)] + [">89"]
age_cat = CategoricalDtype(categories=age_levels, ordered=True)
mdat.age = mdat.age.astype(age_cat)

# save result
mdat.to_feather(snek.output[1])
