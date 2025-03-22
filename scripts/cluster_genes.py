"""
cluster_genes.py
"""
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans

snek = snakemake # type: ignore

df = pd.read_feather(snek.input[0]).set_index("symbol")

# Filter genes/cancers by mutation count
gene_min = snek.config["clustering"]["gene"]["gene_min_mutations"]
cancer_min = snek.config["clustering"]["gene"]["cancer_min_mutations"]

df = df.loc[df.sum(axis=1) >= gene_min, :]
df = df.loc[:, df.sum() >= cancer_min]

# Compute cosine similarity between genes
similarity_matrix = cosine_similarity(df)

# Perform k-means clustering on the similarity matrix
kmeans = KMeans(n_clusters=snek.config["clustering"]["gene"]["k"],
                random_state=snek.config["clustering"]["gene"]["random_seed"])
clusters = kmeans.fit_predict(similarity_matrix)

# Create DataFrame with clustering results
cluster_df = pd.DataFrame({
    'gene': df.index,
    'cluster': clusters + 1
})

cluster_df.cluster = cluster_df.cluster.astype("category")

cluster_df.to_feather(snek.output[0])
