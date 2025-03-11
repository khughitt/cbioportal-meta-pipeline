#
# create_freq_tables.py
#
import pandas as pd

snek = snakemake

mut = pd.read_feather(snek.input[0])

mut = mut[['symbol', 'sample_id_tumor']].rename(columns={
    "sample_id_tumor": "sample_id"
})

mdat = pd.read_feather(snek.input[1])
mdat = mdat[['sample_id', 'cancer_type', 'cancer_type_detailed']]

mut = mut.merge(mdat, on="sample_id")

# total mutation counts
cancer_df = mut['cancer_type'].value_counts().sort_values(ascending=False).to_frame()
cancer_detailed_df = mut['cancer_type_detailed'].value_counts().sort_values(ascending=False).to_frame()
gene_df = mut['symbol'].value_counts().sort_values(ascending=False).to_frame()

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

# ratio of samples with mutation (by cancer type)
num_samples_by_cancer = mut.groupby('cancer_type').sample_id.nunique()
gene_cancer_ratio = mut.groupby(['cancer_type', 'symbol']).sample_id.nunique()
gene_cancer_ratio = (gene_cancer_ratio / num_samples_by_cancer).to_frame()
gene_cancer_ratio = gene_cancer_ratio.rename(columns={'sample_id': 'ratio'})

# total mutation counts (gene by cancer type)
gene_cancer_df = mut.groupby(['cancer_type', 'symbol']).count().loc[:, 'sample_id']
gene_cancer_df = gene_cancer_df.to_frame()
gene_cancer_df = gene_cancer_df.rename(columns={'sample_id': 'num'})

gene_cancer_df = gene_cancer_df.merge(gene_cancer_ratio, left_index=True, right_index=True)
gene_cancer_df = gene_cancer_df.reset_index()
gene_cancer_df = gene_cancer_df.sort_values(['cancer_type', 'ratio'], ascending=[True, False])

# save results
cancer_df = cancer_df.reset_index().sort_values('ratio', ascending=False)
cancer_detailed_df = cancer_detailed_df.reset_index().sort_values('ratio', ascending=False)
gene_df = gene_df.reset_index().sort_values('ratio', ascending=False)

cancer_df.reset_index(drop=True).to_feather(snek.output[0])
cancer_detailed_df.reset_index(drop=True).to_feather(snek.output[1])
gene_df.reset_index(drop=True).to_feather(snek.output[2])
gene_cancer_df.reset_index(drop=True).to_feather(snek.output[3])
