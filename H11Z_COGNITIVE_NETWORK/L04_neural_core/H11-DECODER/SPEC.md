# H11-DECODER Specification

## Overview
H11-DECODER is responsible for the design, optimization, and orchestration of decoder-based architectures in the H11 Cognitive Substrate. It specializes in autoregressive generation paradigms, implementing causal masking, multi-query attention (MQA), grouped-query attention (GQA), and KV-cache management.

## Core Capabilities
- **Autoregressive Generation**: Handling sequential token prediction with masked self-attention.
- **KV Cache Optimization**: Implementing PagedAttention, ring attention, and continuous batching.
- **Cross-Attention Mechanisms**: Bridging encoder-decoder paradigms (e.g., conditioning generation on multimodal context).
- **Positional Encodings**: Managing RoPE (Rotary Position Embeddings), ALiBi, and absolute embeddings.

## Inputs
- Model specifications (layers, heads, dimensions).
- Context lengths and batching strategies.
- Latency and throughput targets for inference.

## Outputs
- Sub-graph configurations for decoder blocks.
- Optimized attention execution plans.
- KV cache memory allocations.

## Evaluation
- PPL (Perplexity) matching.
- Time-to-first-token (TTFT).
- Time-per-output-token (TPOT).
