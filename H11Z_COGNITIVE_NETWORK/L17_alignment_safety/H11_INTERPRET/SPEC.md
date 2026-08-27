# H11-INTERPRET: Mechanistic Interpretability Engine

## Overview
H11-INTERPRET performs deep, granular analysis of the model's inner workings during inference. It opens the "black box" by tracking attention heads, neuron activations, and calculating logit attributions to understand *why* a model generated a specific output.

## Core Mechanisms
1. **Activation Tracking**: Captures feed-forward network (FFN) activations and attention maps across all layers.
2. **Ablation Studies**: Programmatically zeroes out specific attention heads or neurons to measure causal impact on the output.
3. **Logit Lens**: Projects intermediate hidden states directly to the vocabulary to trace concept formation through the layers.

## Interfaces
- `track_forward_pass(inputs, return_attentions)`
- `perform_ablation(layer_idx, head_idx)`
- `compute_logit_attribution()`
