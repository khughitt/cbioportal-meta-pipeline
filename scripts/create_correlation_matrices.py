#
# create_correlation_matrices.py
#
import pandas as pd

snek = snakemake

df = pd.read_feather(snek.input[0]).set_index("symbol")

# filter diseases with zero variance
mask = df.var() > 0
df = df.loc[:, mask]

mask = df.var(axis=1) > 0
df = df.loc[mask, :]

# disease correlation matrix
cor1 = df.corr()

# feature (gene) correlation matrix
cor2 = df.T.corr()

cor1.reset_index().to_feather(snek.output[0])
cor2.reset_index().to_feather(snek.output[1])
