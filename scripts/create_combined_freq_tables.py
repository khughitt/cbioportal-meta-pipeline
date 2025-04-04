"""
create_combined_freq_tables
"""
import os
import pandas as pd

snek = snakemake

num_dfs = []
ratio_dfs = []

for infile in snek.input[:-1]:
    df = pd.read_feather(infile)
    df = df.set_index(df.columns[0])

    study = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(infile))))

    df1 = df['num']
    df2 = df['ratio']

    df1.name = study
    df2.name = study

    num_dfs.append(df1)
    ratio_dfs.append(df2)

num_df = pd.concat(num_dfs, axis=1)
ratio_df = pd.concat(ratio_dfs, axis=1)

num_total = num_df.sum(axis=1)
num_mean = num_df.mean(axis=1)

num_df.loc[:, 'sum'] = num_total
num_df.loc[:, 'mean'] = num_mean

ratio_df.loc[:, 'mean'] = ratio_df.mean(axis=1)

# for gene-level data, add protein length-adjusted versions of the 
# aggregate fields
if snek.wildcards['entity'] == "gene":
    protein_lengths = pd.read_feather(snek.input[-1])
    protein_lengths = protein_lengths[protein_lengths.symbol.isin(num_df.index)]
    protein_lengths = protein_lengths.set_index('symbol')

    num_mean = num_df.loc[:, 'mean']
    num_mean = pd.merge(num_mean, protein_lengths, left_index=True, right_index=True, how='left')

    # for genes with no associated protein length information, default to median protein length
    median_length = protein_lengths.length.median() 
    num_mean.loc[num_mean.length.isna(), "length"] = median_length

    num_df['mean_adj'] = num_mean['mean'] / num_mean['length']

    ratio_mean = ratio_df.loc[:, 'mean']
    ratio_mean = pd.merge(ratio_mean, protein_lengths, left_index=True, right_index=True, how='left')
    ratio_df['mean_adj'] = ratio_mean['mean'] / ratio_mean['length']

num_df = num_df.sort_values('mean', ascending=False)
ratio_df = ratio_df.sort_values('mean', ascending=False)

num_df.reset_index().to_feather(snek.output[0])
ratio_df.reset_index().to_feather(snek.output[1])
