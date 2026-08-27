# H11-NORMALIZE Agent Specification

## 1. Overview
The H11-NORMALIZE agent manages normalization layers in the neural core, ensuring internal covariate shift reduction, stable gradients, and dynamic scaling. It oversees classical norms like BatchNorm and LayerNorm, as well as modern variants like RMSNorm and QK-Norm.

## 2. Capabilities
- **Normalization Selection**: Dynamically swap between LayerNorm, RMSNorm, InstanceNorm based on tensor rank.
- **Precision Tracking**: Ensure variance statistics don't underflow/overflow in fp16/bf16 via robust running stats.
- **QK-Norm Config**: Handle query-key normalization for stable attention in transformers.
- **Adaptive Norms**: Support FiLM (Feature-wise Linear Modulation) and AdaIN for conditioning.

## 3. Architecture
Works by providing localized norm operators that track their own affine parameters and running statistics. Supports fusion operations for efficient execution.
