# H11-FAIRNESS-ALIGN Agent Specification

## 1. Overview
The H11-FAIRNESS-ALIGN agent actively mitigates the biases detected by the H11-BIAS-DETECT agent. It operates as an intervention layer, modifying cognitive states and models in real-time to enforce fairness constraints.

## 2. Theoretical Framework
Rather than passively identifying bias, this agent applies active alignment. It uses optimization techniques to project latent embeddings onto a subspace orthogonal to sensitive attributes, effectively "scrubbing" the sensitive information from the cognitive stream.

## 3. Core Algorithms
- **Iterative Null-Space Projection (INLP)**: Projects embeddings onto the null-space of classifiers trained to predict sensitive attributes, thereby erasing the information.
- **Adversarial Gradient Reversal**: When integrated into learning loops, it scales gradients from an adversarial bias-predictor by a negative factor to enforce invariant representations.
- **Margin Reweighting**: Dynamically adjusts sampling probabilities and loss margins for underrepresented or unfairly penalized groups.

## 4. Execution Model
Acts as an interceptor in the H11 substrate. When a cognitive vector passes through, the agent applies its learned orthogonal projection matrix before handing the vector back to the main processing pipeline.
