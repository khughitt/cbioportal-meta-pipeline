#
# create_combined_gene_cancer_mutation_matrices.py
#
import numpy as np
import pandas as pd

snek = snakemake

# 1. count matrix
df = pd.read_feather(snek.input[0])

mut_sums = df.loc[:, ~df.columns.isin(['cancer_type', 'symbol', 'mean', 'mean_adj'])].sum(axis=1)
long_df = pd.DataFrame({"cancer_type": df.cancer_type, "symbol": df.symbol, "num": mut_sums})
mat = long_df.pivot_table(index="symbol", columns="cancer_type", values="num", fill_value=0)

mat.reset_index().to_feather(snek.output[0])

# 2. ratio matrix
df = pd.read_feather(snek.input[1])

ratio_means = df.loc[:, ~df.columns.isin(['cancer_type', 'symbol', 'mean', 'mean_adj'])].mean(axis=1)
long_df = pd.DataFrame({"cancer_type": df.cancer_type, "symbol": df.symbol, "ratio": ratio_means})
mat = long_df.pivot_table(index="symbol", columns="cancer_type", values="ratio", fill_value=0)

mat.reset_index().to_feather(snek.output[1])
