
# Hierarchical Clustering

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage

# 1. Create dataset
X = np.array([
    [2, 3],
    [3, 3],
    [3, 4],
    [8, 8],
    [9, 8],
    [8, 9],
    [1, 10],
    [2, 9],
    [1, 9]
])

# 2. Create linkage matrix
Z = linkage(X, method='ward')

# 3. Plot dendrogram
plt.figure(figsize=(9, 5))
dendrogram(Z)
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('Data Points')
plt.ylabel('Distance')
plt.show()

# 4. Create and train clustering model
model = AgglomerativeClustering(
    n_clusters=3,
    linkage='ward'
)

labels = model.fit_predict(X)

# 5. Display cluster labels
print("Cluster Labels:")
print(labels)

# 6. Visualize clusters
plt.figure(figsize=(8, 5))

plt.scatter(
    X[:, 0], X[:, 1],
    c=labels, cmap='viridis', s=100
)

plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('Hierarchical Clustering Results')
plt.show()

print("\nHierarchical Clustering completed successfully.")
