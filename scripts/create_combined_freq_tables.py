"""
create_combined_freq_tables
"""
import os
import pandas as pd

snek = snakemake

num_dfs = []
ratio_dfs = []

for infile in snek.input:
    df = pd.read_feather(infile)
    df = df.set_index(df.columns[0])

    dataset = os.path.basename(os.path.dirname(os.path.dirname(infile)))

    df1 = df['num']
    df2 = df['ratio']

    df1.name = dataset
    df2.name = dataset

    num_dfs.append(df1)
    ratio_dfs.append(df2)

num_df = pd.concat(num_dfs, axis=1)
ratio_df = pd.concat(ratio_dfs, axis=1)

num_df.loc[:, 'mean'] = num_df.mean(axis=1)
ratio_df.loc[:, 'mean'] = ratio_df.mean(axis=1)

num_df = num_df.sort_values('mean', ascending=False)
ratio_df = ratio_df.sort_values('mean', ascending=False)

num_df.reset_index().to_feather(snek.output[0])
ratio_df.reset_index().to_feather(snek.output[1])
