# H11-RWKV: Linear-attention RNN

## Overview
The H11-RWKV agent is responsible for synthesizing and managing RWKV (Receptance Weighted Key Value) style architectures, offering the parallel training benefits of transformers alongside the efficient O(1) inference of recurrent neural networks.

## Capabilities
- **WKV Kernel Design**: Implementation and optimization of the WKV linear attention kernel.
- **State Management**: Handling recurrent state propagation across chunks or tokens.
- **Time-Mix and Channel-Mix**: Managing the token-mixing and channel-mixing blocks of RWKV models.
- **Hybrid Inference Methods**: Supporting both RNN-mode and parallel/chunk-mode processing.
