"""
create_protein_length_mapping.py

Creates a mapping from Uniprot "Gene Name" -> mean protein length.
"""
import pandas as pd

snek = snakemake

df = pd.read_csv(snek.input[0], sep='\t')

df['Gene Names'] = df['Gene Names'].str.split()
df = df.explode('Gene Names')

df = df.rename(columns={
    "Gene Names": "symbol",
    "Length": "length"
})

df = df.loc[:, ["symbol", "length"]].drop_duplicates().dropna()

df = df.groupby('symbol').mean().reset_index()

df.to_feather(snek.output[0])
