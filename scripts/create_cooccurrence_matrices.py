#
# create_cooccurrence_matrices.py
#
import pandas as pd

snek = snakemake

df = pd.read_feather(snek.input[0]).set_index("symbol")

# filter diseases with zero variance
mask = df.var() > 0
df = df.loc[:, mask]

mask = df.var(axis=1) > 0
df = df.loc[mask, :]

# disease co-occurrence matrix
cor1 = df.T.dot(df)

# feature (gene) co-occurrence matrix
cor2 = df.dot(df.T)

cor1.reset_index().to_feather(snek.output[0])
cor2.reset_index().to_feather(snek.output[1])
