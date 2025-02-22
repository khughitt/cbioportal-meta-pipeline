#
# convert_to_feather.py
#
# Creates filtered versions of input dataset with the fields of interest, using simpler names and
# and proper column encodings.
#
import pandas as pd

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

# chromo

#
# 2. sample metadata
#
mdat = pd.read_csv(snek.input[1], sep='\t', skiprows=4)

# "AGE_AT_SEQ_REPORT" includes non-integer values: 
#
# "<18"
# ">89"
# "Unknown"

# SAMPLE_CLASS.value_counts()
# Tumor    229015
# cfDNA       438
#

# drop columns not planned for use
#mdat = mdat.drop([""], axis=1)

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

mdat.to_feather(snek.output[1])

