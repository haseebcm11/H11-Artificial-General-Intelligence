# H11-DROPOUT Agent Specification

## 1. Overview
The H11-DROPOUT agent is responsible for stochastic regularization techniques across the core. It manages DropConnect, standard dropout, Monte Carlo dropout for uncertainty estimation, and structural DropPath.

## 2. Capabilities
- **Regularization Control**: Schedule dropout probabilities based on training phase (curriculum dropout).
- **Spatial / Structural Drops**: Handle SpatialDropout1D/2D/3D and DropPath (Stochastic Depth).
- **MC-Dropout**: Manage forward passes with active dropout during inference to compute predictive variance.
- **DropConnect**: Zero out weights directly instead of activations.

## 3. Lifecycle
The agent coordinates with the training loop to ensure scaling by `1/(1-p)` is applied correctly in training, and disabled in eval (unless MC mode is active).
