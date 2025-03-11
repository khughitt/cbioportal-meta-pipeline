"""
create_combined_sample_table.py
"""
import pandas as pd

snek = snakemake

cols = ['patient_id', 'sample_id', 'cancer_type', 'cancer_type_detailed']

dfs = [pd.read_feather(x)[cols] for x in snek.input]

# rbind
df = pd.concat(dfs)

df['patient_id'] = df['patient_id'].astype('str')
df['sample_id'] = df['sample_id'].astype('str')
df['cancer_type'] = df['cancer_type'].astype('category')
df['cancer_type_detailed'] = df['cancer_type_detailed'].astype('category')

df.to_feather(snek.output[0])
