#
# create_disease_mutation_count_matrix.py
#
import numpy as np
import pandas as pd

snek = snakemake

mut = pd.read_feather(snek.input[0])
mdat = pd.read_feather(snek.input[1])

mut = mut[["sample_id_tumor", "symbol"]].rename(columns={
    "sample_id_tumor": "sample_id"
})

mdat = mdat[["cancer_type", "sample_id"]]

# only count each unique sample id once for a given gene mutation
mut = mut.drop_duplicates()

mut = mut.merge(mdat, on="sample_id")

# create gene x disease mutation matrix
mut_counts = mut.groupby(["symbol", "cancer_type"]).count().reset_index()

df = mut_counts.pivot_table(index="symbol", columns="cancer_type", values="sample_id", fill_value=0)
df.reset_index().to_feather(snek.output[0])
