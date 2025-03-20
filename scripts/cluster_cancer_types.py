"""
cluster_cancer_types.py
"""
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans

snek = snakemake # type: ignore

df = pd.read_feather(snek.input[0]).set_index("symbol")

# Filter genes with fewer than min_gene_mutations mutations
min_mutations = snek.config["clustering"]["cancer"]["min_gene_mutations"]
df = df[df.sum(axis=1) >= min_mutations]

# Compute cosine similarity between cancer types (columns)
similarity_matrix = cosine_similarity(df.T)

# Perform k-means clustering on the similarity matrix
kmeans = KMeans(n_clusters=snek.config["clustering"]["cancer"]["k"],
                random_state=snek.config["clustering"]["cancer"]["random_seed"])
clusters = kmeans.fit_predict(similarity_matrix)

# Create DataFrame with clustering results
cluster_df = pd.DataFrame({
    'cancer_type': df.columns,
    'cluster': clusters
})

cluster_df.to_feather(snek.output[0])
