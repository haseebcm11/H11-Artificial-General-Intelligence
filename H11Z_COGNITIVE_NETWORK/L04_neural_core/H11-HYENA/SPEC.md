# H11-HYENA Specification

## Overview
H11-HYENA develops and integrates long-convolution operators, specifically focusing on the Hyena hierarchy. It replaces attention with implicit long convolutions and data-controlled gating to achieve sub-quadratic scaling with context length.

## Core Capabilities
- **Hyena Operator**: Constructing data-controlled gating with long implicit convolutions.
- **FFT Convolutions**: Fast convolution evaluation using Fast Fourier Transforms for massive sequences.
- **Implicit Filters**: Generating filter weights dynamically using small MLPs with positional embeddings.
- **Sub-quadratic Attention Alternatives**: Scaling to 100k+ tokens without KV cache explosion.

## Inputs
- Context length (L).
- Filter MLP dimensions.
- Order of the Hyena recurrence (N).

## Outputs
- Hyena recurrence compute graph.
- Filter MLP structural definitions.
- FFT plan for convolution scaling.

## Evaluation
- Long-sequence recall (e.g., passkey retrieval).
- Empirical scaling vs O(L^2) attention.
- Memory footprint during inference.
