# H11-NAS Specification

## Overview
The H11-NAS (Neural Architecture Search) agent discovers novel, highly-optimized neural architectures tailored to specific data distributions and hardware constraints. It focuses on the topological arrangement of tensor operations rather than hyperparameter tuning.

## Differentiable Architecture Search (DARTS)
The agent heavily utilizes DARTS to make the discrete search space continuous. 
A cell is a directed acyclic graph where each node $x^{(i)}$ is a latent representation, and each directed edge $(i, j)$ is associated with an operation $o^{(i,j)}$ chosen from a set of candidate operations $\mathcal{O}$.

To make the search space continuous, we relax the categorical choice of a particular operation to a softmax over all possible operations:
$$ \bar{o}^{(i,j)}(x) = \sum_{o \in \mathcal{O}} \frac{\exp(\alpha_{o}^{(i,j)})}{\sum_{o' \in \mathcal{O}} \exp(\alpha_{o'}^{(i,j)})} o(x) $$
where $\alpha^{(i,j)}$ represents the architecture mixing weights.

The optimization problem is a bi-level continuous optimization:
$$ \min_{\alpha} \mathcal{L}_{val}(w^*(\alpha), \alpha) $$
$$ \text{s.t. } w^*(\alpha) = \text{argmin}_w \mathcal{L}_{train}(w, \alpha) $$

## Search Space Constraints
1. **Macro vs. Micro Structure:** The macro structure dictates how cells are stacked (e.g., spatial reduction layers, skip connections), while the micro structure dictates the operations within a cell (e.g., 3x3 depthwise separable conv, zero-padding, max pooling).
2. **Hardware-Aware NAS (HW-NAS):** The agent incorporates latency constraints directly into the loss function: $\mathcal{L}_{total} = \mathcal{L}_{val} + \lambda \log(\text{Latency}(\alpha))^{\beta}$.

## Evolution and Proxy Metrics
To avoid the computational burden of full training, the agent utilizes zero-cost proxy metrics (like Neural Tangent Kernel condition numbers or Synaptic Flow) to prune the search space early in the evolutionary cycles.
