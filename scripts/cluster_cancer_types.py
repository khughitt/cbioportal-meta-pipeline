"""
cluster_cancer_types.py
"""
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans

snek = snakemake # type: ignore

df = pd.read_feather(snek.input[0]).set_index("symbol")

# Filter genes/cancers by mutation count
gene_min = snek.config["clustering"]["cancer"]["gene_min_mutations"]
cancer_min = snek.config["clustering"]["cancer"]["cancer_min_mutations"]

df = df.loc[df.sum(axis=1) >= gene_min, :]
df = df.loc[:, df.sum() >= cancer_min]

# Compute cosine similarity between cancer types (columns)
similarity_matrix = cosine_similarity(df.T)

# Perform k-means clustering on the similarity matrix
kmeans = KMeans(n_clusters=snek.config["clustering"]["cancer"]["k"],
                random_state=snek.config["clustering"]["cancer"]["random_seed"])
clusters = kmeans.fit_predict(similarity_matrix)

# Create DataFrame with clustering results
cluster_df = pd.DataFrame({
    'cancer_type': df.columns,
    'cluster': clusters + 1
})

cluster_df.cluster = cluster_df.cluster.astype("category")

cluster_df.to_feather(snek.output[0])
