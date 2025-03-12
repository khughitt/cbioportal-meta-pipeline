"""
check_gene_coverage.py - creates a table indicating how many studies each gene appears in.
"""
import pandas as pd

snek = snakemake

dfs = [pd.read_feather(x).set_index('symbol') for x in snek.input]

gene_lists = [df.index.values.tolist() for df in dfs]
genes:list[str] = sum(gene_lists, [])

gene_counts = pd.Series(genes).value_counts().to_frame().reset_index()

gene_counts.columns = ['symbol', 'count']

gene_counts.to_feather(snek.output[0])
