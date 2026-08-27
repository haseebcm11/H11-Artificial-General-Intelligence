> **Layer 2** · Machine Learning · `H11-MACHINA-DISCENS`

## Purpose

H11-MACHINA-DISCENS is the classical machine learning engine of the substrate. It is responsible for statistical learning, feature engineering, and predictive modeling using non-deep algorithms (e.g., SVMs, Random Forests, Gradient Boosting, GLMs). It serves as the computationally efficient, highly interpretable fallback and baseline for predictive tasks.

When a dataset lacks the volume to train a deep neural network, or when stringent latency and interpretability constraints are present, MACHINA-DISCENS takes over. It excels at tabular data, small-to-medium text corpora (using TF-IDF/BM25), and structural inference tasks where exact statistical bounds (like PAC learning bounds) are required.

## Technical Deep-Dive

MACHINA-DISCENS employs an automated pipeline architecture (AutoML-inspired) that sequentially handles imputation, scaling, feature selection (via L1 regularization or Mutual Information), and model selection. It uses sequential model-based optimization (SMBO) with Gaussian Processes to tune hyperparameters.

The agent maintains an ensemble registry, dynamically constructing voting, bagging, and stacking models depending on the bias-variance tradeoff detected in the cross-validation folds. For anomaly detection, it leverages Isolation Forests and One-Class SVMs, providing robust Mahalanobis distance approximations.

Crucially, this agent calculates VC dimension and Rademacher complexity for its active models, feeding this structural risk minimization data back to the core routing layer to guarantee generalization bounds.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| dataset_uri | str | Pointer to tabular/structured dataset |
| target_column | Optional[str] | Column to predict (None for unsupervised) |
| task_type | MLTaskType | Classification, Regression, Clustering, Anomaly |
| latency_constraint_ms | int | Maximum inference time allowance |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| model_artifact | str | URI to serialized model pipeline |
| cv_metrics | Dict[str, float] | Cross-validation scores (F1, RMSE, etc.) |
| feature_importances | Dict[str, float] | Shapley values or permutation importance |
| generalization_bound | float | PAC bound epsilon |

### State Schema
- `hyperparameter_trials`: History of explored HP spaces.
- `active_pipelines`: Currently deployed ML pipelines and their drift metrics.

## Dependencies

### Upstream (depends on)
- H11-DATASTRUCTURA: For efficient in-memory data representations (e.g., Columnar formats).
- H11-DATABASE: To query training batches.

### Downstream (feeds into)
- H11-EXPLAINABLE: Receives the model for global and local surrogate explanations.
- H11-METALEARNING: Uses the learning curves for pipeline recommendation.

## Failure Modes
- `ConceptDriftException`: Statistical distribution of inference data significantly deviates from training.
- `CurseOfDimensionality`: Features drastically outnumber samples, causing L2 failure.
- `ConvergenceTimeout`: SVM/GLM fails to converge within the allowed iterations.

## Performance Characteristics
- Training time: Scale $O(N \log N)$ to $O(N^3)$ depending on model.
- Inference latency: < 5ms for trees/GLMs.

## Research References
- Vapnik, V. (1998). *Statistical Learning Theory*.
- Breiman, L. (2001). *Random Forests*. Machine Learning.

## Implementation Notes
Uses structured numpy arrays and cythonized tree primitives for execution speed.
