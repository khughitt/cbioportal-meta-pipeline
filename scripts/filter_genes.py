#
# filter_genes.py - filters genes which don't appear in a sufficient number of studies
#
import pandas as pd

snek = snakemake

mut = pd.read_feather(snek.input[0])
gene_counts = pd.read_feather(snek.input[1])

# determine which genes to keep
MIN_COUNT = snek.config['filtering']['genes']['min_studies']
gene_counts[gene_counts['count'] >= MIN_COUNT]

genes_to_keep = gene_counts[gene_counts['count'] >= MIN_COUNT].symbol

# filter & save
mut = mut[mut.symbol.isin(genes_to_keep)]
mut.symbol = mut.symbol.cat.remove_unused_categories()

mut.to_feather(snek.output[0])
