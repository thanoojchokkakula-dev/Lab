
# K-Means Clustering Algorithm

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

# 1. Create dataset
X = [
    [2, 3], [3, 3], [3, 4],
    [8, 8], [9, 8], [8, 9],
    [1, 10], [2, 9], [1, 9]
]

# 2. Scale the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 3. Create and train K-Means model
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
kmeans.fit(X_scaled)

# 4. Get cluster labels
labels = kmeans.labels_

print("Cluster Labels:")
print(labels)

# 5. Display cluster centers in original scale
centers = scaler.inverse_transform(kmeans.cluster_centers_)
print("\nCluster Centers:")
print(centers)

# 6. Calculate silhouette score
score = silhouette_score(X_scaled, labels)
print("\nSilhouette Score:", round(score, 3))

# 7. Visualize clusters
plt.figure(figsize=(8, 5))

plt.scatter(
    X_scaled[:, 0], X_scaled[:, 1],
    c=labels, cmap='viridis', s=100
)

plt.scatter(
    kmeans.cluster_centers_[:, 0],
    kmeans.cluster_centers_[:, 1],
    color='red', marker='X', s=250,
    label='Centroids'
)

plt.xlabel('Feature 1 (Scaled)')
plt.ylabel('Feature 2 (Scaled)')
plt.title('K-Means Clustering')
plt.legend()
plt.show()
