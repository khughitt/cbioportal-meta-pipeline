#
# create_correlation_matrices.py
#
import pandas as pd

snek = snakemake

disease_mut = pd.read_feather(snek.input[0]).set_index("symbol")
patient_mut = pd.read_feather(snek.input[1]).set_index("symbol")

# filter diseases with zero variance
mask = disease_mut.var() > 0
disease_mut = disease_mut.loc[:, mask]

mask = disease_mut.var(axis=1) > 0
disease_mut = disease_mut.loc[mask, :]

mask = patient_mut.var() > 0
patient_mut = patient_mut.loc[:, mask]

mask = patient_mut.var(axis=1) > 0
patient_mut = patient_mut.loc[mask, :]

# disease correlation matrix
disease_cor = disease_mut.corr()

# gene correlation matrix
gene_cor = patient_mut.T.corr()

disease_cor.reset_index().to_feather(snek.output[0])
gene_cor.reset_index().to_feather(snek.output[1])
