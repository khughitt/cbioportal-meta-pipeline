"""
create_combined_gene_patient_matrix.py
"""
import pandas as pd

snek = snakemake

SUBSAMPLE_PATIENTS = snek.config["subsampling"]["patients"]

dfs:list[pd.DataFrame] = []

for x in snek.input:
    df = pd.read_feather(x).set_index('symbol')

    if SUBSAMPLE_PATIENTS < 1:
        df = df.sample(round(SUBSAMPLE_PATIENTS * df.shape[1]), axis=1, random_state=123)

    dfs.append(df)

mat = pd.concat(dfs, axis=1)
mat.reset_index().to_feather(snek.output[0])
