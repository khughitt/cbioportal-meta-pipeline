"""
create_study_summary_table.py
"""
import os
import pandas as pd

snek = snakemake

counts = [pd.read_feather(x).num for x in snek.input]

df = pd.concat(counts, axis=1)
df.columns = [os.path.basename(os.path.dirname(os.path.dirname(x))) for x in snek.input]

df.insert(0, "stat", ['num_genes', 'num_mutations', 'num_cancer_types', 'num_patients', 'num_samples'])
df = df.set_index('stat').T.reset_index()

df = df.rename(columns={'index': 'study'})

df.to_feather(snek.output[0])
