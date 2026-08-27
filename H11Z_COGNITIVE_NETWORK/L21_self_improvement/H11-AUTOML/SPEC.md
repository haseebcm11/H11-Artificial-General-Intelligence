# H11-AUTOML Specification

## Overview
The H11-AUTOML agent dynamically designs, evaluates, and deploys end-to-end Machine Learning pipelines. It shifts away from static model architectures to dynamically composed pipelines that combine feature extraction, dimensionality reduction, model selection, and ensembling based on dataset meta-features.

## Theoretical Foundations
The agent utilizes **Meta-Learning** and **Bayesian Optimization** to navigate the pipeline configuration space $\mathcal{P}$. 
Given a dataset $D$, the agent extracts meta-features $M(D)$ (e.g., skewness, kurtosis, class imbalance, feature correlation matrix) and maps them to a prior over successful pipelines using a deep surrogate model.

Let $f: \mathcal{P} \times \mathcal{D} \rightarrow \mathbb{R}$ be the validation metric. The agent solves:
$$ P^* = \arg\max_{P \in \mathcal{P}} f(P, D) $$
using a surrogate model $\hat{f}(P, D)$ modeled via a Gaussian Process $GP(\mu, K)$ or an Empirical Performance Model (EPM) based on Random Forests.

## Component Synthesis
1. **Data Sanitization Sub-graph:** Imputation strategies (KNN, Iterative, Mean) and outlier rejection mechanisms.
2. **Feature Engineering Sub-graph:** Non-linear combinations, polynomial expansions, target encoding, and embeddings for high-cardinality categoricals.
3. **Model Portfolio:** Gradient Boosting (XGBoost, LightGBM), Deep Neural Networks (MLPs, TabNets), and sparse linear models.
4. **Dynamic Ensembling:** Stacking with a meta-learner (e.g., Logistic Regression or a small NN) using cross-validated out-of-fold predictions.

## Execution Model
Pipelines are represented as Directed Acyclic Graphs (DAGs). The agent employs a Zero-Shot AutoML approach to evaluate the top $K$ pipeline topologies before fine-tuning the best candidate via the Hyperopt agent.
