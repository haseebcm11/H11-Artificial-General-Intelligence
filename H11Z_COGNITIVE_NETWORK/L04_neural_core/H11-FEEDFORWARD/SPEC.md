# H11-FEEDFORWARD Agent Specification

## 1. Overview
The H11-FEEDFORWARD agent governs Multi-Layer Perceptron (MLP) blocks, which form the channel-mixing component of transformers and other deep architectures. It supports advanced activation paradigms like SwiGLU, GeGLU, and handles Mixture of Experts (MoE) FFNs.

## 2. Capabilities
- **Activation Management**: Map standard (ReLU, GELU, Swish) and Gated Linear Unit variants.
- **Expansion Ratio Config**: Manage the intermediate hidden dimension (e.g., 4x or 8/3x in LLaMA).
- **MoE Routing**: Interface with routing agents to split FFN logic across multiple experts (top-K gating, capacity limits).
- **Bias Control**: Options for bias-free feedforward layers.

## 3. Data Flow
Takes embedded sequences, projects to high-dimensional space, applies non-linear gating, and projects back, scaling properly based on activation types.
