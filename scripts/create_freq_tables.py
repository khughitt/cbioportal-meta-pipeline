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

# total mutation counts
cancer_df = mut['cancer_type'].value_counts().sort_values(ascending=False).to_frame()
cancer_detailed_df = mut['cancer_type_detailed'].value_counts().sort_values(ascending=False).to_frame()
gene_df = mut['symbol'].value_counts().sort_values(ascending=False).to_frame()
sample_type_df = mut['sample_type'].value_counts().sort_values(ascending=False).to_frame()

# ratio of samples with mutation
num_samples = len(mut.sample_id.unique())

cancer_freq = mut.groupby('cancer_type').sample_id.nunique().to_frame() / num_samples
cancer_df = cancer_df.merge(cancer_freq, left_index=True, right_index=True)
cancer_df.columns = ['num', 'ratio']

cancer_detailed_freq = mut.groupby('cancer_type_detailed').sample_id.nunique().to_frame() / num_samples
cancer_detailed_df = cancer_detailed_df.merge(cancer_detailed_freq, left_index=True, right_index=True)
cancer_detailed_df.columns = ['num', 'ratio']

gene_freq = mut.groupby('symbol').sample_id.nunique().to_frame() / num_samples
gene_df = gene_df.merge(gene_freq, left_index=True, right_index=True)
gene_df.columns = ['num', 'ratio']

sample_type_freq = mut.groupby('sample_type').sample_id.nunique().to_frame() / num_samples
sample_type_df = sample_type_df.merge(sample_type_freq, left_index=True, right_index=True)
sample_type_df.columns = ['num', 'ratio']

# save results
cancer_df.reset_index().sort_values('ratio', ascending=False).to_feather(snek.output[0])
cancer_detailed_df.reset_index().sort_values('ratio', ascending=False).to_feather(snek.output[1])
gene_df.reset_index().sort_values('ratio', ascending=False).to_feather(snek.output[2])
sample_type_df.reset_index().sort_values('ratio', ascending=False).to_feather(snek.output[3])
