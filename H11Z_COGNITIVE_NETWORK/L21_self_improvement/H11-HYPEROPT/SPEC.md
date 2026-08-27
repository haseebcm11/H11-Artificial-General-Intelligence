# H11-HYPEROPT Specification

## Overview
The H11-HYPEROPT agent resolves the continuous, discrete, and conditional hyperparameter optimization (HPO) domains for model training and pipeline execution. It focuses on finding the Pareto optimal front between resource consumption and performance.

## Core Optimization Algorithms
1. **Tree-structured Parzen Estimator (TPE):**
   Instead of modeling $p(y|x)$ directly (like standard Gaussian Processes), TPE models $p(x|y)$ and $p(y)$. It defines two densities for the parameters $x$:
   $$ 
   l(x) = p(x | y < y^*) 
   $$
   $$
   g(x) = p(x | y \ge y^*)
   $$
   Where $y^*$ is the quantile threshold of the objective values. The acquisition function maximizes Expected Improvement (EI), which is proportional to the ratio $l(x)/g(x)$.

2. **BOHB (Bayesian Optimization and Hyperband):**
   The agent utilizes Multi-Fidelity optimization to discard unpromising configurations early. Hyperband defines a schedule of successive halving. BOHB replaces Hyperband's random sampling with TPE, ensuring that configurations selected for the lowest fidelity level are drawn from an informed prior.

3. **Population Based Training (PBT):**
   For deep learning models, hyperparameters (like learning rate, momentum) are not static. The agent runs a population of models. Periodically, underperforming models copy the weights of top performers (exploit) and mutate their hyperparameters (explore), allowing for the discovery of optimal dynamic hyperparameter schedules.

## Parameter Space Representation
The parameter space $\Lambda$ is represented as a typed configuration tree, supporting constraints like:
- Conditionally active parameters (e.g., `if optimizer == 'adam': lr ~ loguniform(1e-5, 1e-2)`).
- Quantized and discrete variables.
- Categorical variables with structural dependencies.
