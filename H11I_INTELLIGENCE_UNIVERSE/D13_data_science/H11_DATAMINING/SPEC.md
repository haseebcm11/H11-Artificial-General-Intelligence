# H11-DATAMINING Specification

## Overview
H11-DATAMINING is an agent focused on data mining, clustering, anomaly detection, and pattern recognition. It extracts actionable insights and groups from unstructured or large structured datasets without relying exclusively on supervised labels.

## Core Capabilities
- **Clustering:** Performs K-Means, DBSCAN, Hierarchical Clustering.
- **Pattern Recognition:** Frequent itemset mining, association rules (Apriori).
- **Dimensionality Reduction:** PCA, t-SNE, UMAP for visualization and noise reduction.
- **Anomaly Detection:** Identifies outliers using Isolation Forests and Local Outlier Factors.

## Inputs
- Dataset (matrix or structured tables)
- Mining objective (e.g., cluster, find rules, detect anomalies)
- Algorithm hyperparameters.

## Outputs
- Mined patterns, cluster labels, or anomaly scores.
- Quality metrics (e.g., silhouette score, lift, confidence).
