# H11-TRANSFORMER Agent Specification

## 1. Overview
The H11-TRANSFORMER agent builds and orchestrates full Transformer blocks. It aggregates Self-Attention (from attention sub-agents), FeedForward blocks, Normalization, and Residual connections into a cohesive, highly optimized architectural unit.

## 2. Capabilities
- **Variant Construction**: Build GPT-style (decoder-only), BERT-style (encoder-only), or T5-style (encoder-decoder) layers.
- **Scaling Laws**: Provide dimension and layer scaling configurations aligned with Chinchilla/Kaplan scaling laws.
- **Micro-architectural Tweaks**: Parallel Attention/FFN formulation (GPT-J style), QK-Norm integration, Pre-Norm vs Post-Norm.
- **Block Checkpointing**: Provide gradient checkpointing hooks to save VRAM during training.

## 3. Lifecycle
Acts as a high-level composite agent within Layer 4, calling upon H11-NORMALIZE, H11-FEEDFORWARD, and H11-RESIDUAL to assemble blocks.
