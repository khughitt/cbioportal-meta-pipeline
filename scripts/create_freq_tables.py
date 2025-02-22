#
# create_freq_tables.py
#
import pandas as pd

# TODO: counts by (cancer type)?

snek = snakemake

mut = pd.read_feather(snek.input[0])

mut = mut[['symbol', 'sample_id_tumor']].rename(columns={
    "sample_id_tumor": "sample_id"
})

mdat = pd.read_feather(snek.input[1])

mut = mut.merge(mdat, on="sample_id")

cancer_freq = mut['cancer_type'].value_counts().sort_values(ascending=False)
cancer_detailed_freq = mut['cancer_type_detailed'].value_counts().sort_values(ascending=False)
gene_freq = mut['symbol'].value_counts().sort_values(ascending=False)
sample_type_freq = mut['sample_type'].value_counts().sort_values(ascending=False)

cancer_freq.to_frame().reset_index().to_feather(snek.output[0])
cancer_detailed_freq.to_frame().reset_index().to_feather(snek.output[1])
gene_freq.to_frame().reset_index().to_feather(snek.output[2])
sample_type_freq.to_frame().reset_index().to_feather(snek.output[3])
