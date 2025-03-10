#
# create_gene_patient_mutation_count_matrix.py
#
import numpy as np
import pandas as pd

snek = snakemake

mut = pd.read_feather(snek.input[0])
sample_mdat = pd.read_feather(snek.input[1])

# sample id -> patient id
sample_mdat = sample_mdat[['sample_id', 'patient_id']]
sample_mdat = sample_mdat.set_index('sample_id')

mut = mut[["sample_id_tumor", "symbol"]].rename(columns={
    "sample_id_tumor": "sample_id"
})

mut = mut.set_index('sample_id').merge(sample_mdat, left_index=True, right_index=True)
mut = mut.reset_index()
mut = mut[['symbol', 'patient_id']]

# only count each unique patient id once for a given gene mutation
mut = mut.drop_duplicates()

# create gene x patient mutation matrix
mut.loc[:, 'indicator'] = 1

df = mut.pivot_table(index="symbol", columns="patient_id", values="indicator", fill_value=0)
df.reset_index().to_feather(snek.output[0])
