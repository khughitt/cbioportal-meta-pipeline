"""
cluster_genes.py
"""
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans

snek = snakemake # type: ignore

df = pd.read_feather(snek.input[0]).set_index("symbol")

# Filter genes with fewer than min_gene_mutations mutations
min_mutations = snek.config["clustering"]["gene"]["min_gene_mutations"]
df = df[df.sum(axis=1) >= min_mutations]

# Compute cosine similarity between genes
similarity_matrix = cosine_similarity(df)

# Perform k-means clustering on the similarity matrix
kmeans = KMeans(n_clusters=snek.config["clustering"]["gene"]["k"],
                random_state=snek.config["clustering"]["gene"]["random_seed"])
clusters = kmeans.fit_predict(similarity_matrix)

# Create DataFrame with clustering results
cluster_df = pd.DataFrame({
    'gene': df.index,
    'cluster': clusters
})

cluster_df.to_feather(snek.output[0])
