#
# filter_genes.py - filters genes which don't appear in a sufficient number of studies
#
import math
import pandas as pd

snek = snakemake

mut = pd.read_feather(snek.input[0])
gene_counts = pd.read_feather(snek.input[1])

studies = pd.read_feather(snek.input[2])

# determine which genes to keep
MIN_RATIO = snek.config['filtering']['genes']['min_studies_ratio']

num_studies = studies.shape[0]
min_count = math.ceil(MIN_RATIO * num_studies)

genes_to_keep = gene_counts[gene_counts['count'] >= min_count].symbol

# filter & save
mut = mut[mut.symbol.isin(genes_to_keep)]
mut.symbol = mut.symbol.cat.remove_unused_categories()

mut.to_feather(snek.output[0])
