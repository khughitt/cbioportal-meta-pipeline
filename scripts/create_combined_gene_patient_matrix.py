"""
create_combined_gene_patient_matrix.py
"""
import os
import pandas as pd

snek = snakemake

SUBSAMPLE_PATIENTS = snek.config["subsampling"]["patients"]

dfs:list[pd.DataFrame] = []

for infile in snek.input:
    df = pd.read_feather(infile).set_index('symbol')

    if SUBSAMPLE_PATIENTS < 1:
        df = df.sample(round(SUBSAMPLE_PATIENTS * df.shape[1]), axis=1, random_state=123)

    # add dataset name as prefix to column ids to avoid conflicts
    study = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(infile))))

    df.columns = [study + "_" + x for x in df.columns]

    dfs.append(df)

mat = pd.concat(dfs, axis=1)
mat.reset_index().to_feather(snek.output[0])
