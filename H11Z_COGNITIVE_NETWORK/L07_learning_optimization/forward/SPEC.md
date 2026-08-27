> **Layer 7** · Learning & Optimization · `H11-FORWARD`

## Purpose

The `H11-FORWARD` agent is responsible for forward propagation within the H11 Cognitive Substrate. 
Forward pass: layer-by-layer computation, activation caching for backward, forward hooks, selective activation checkpointing, forward pass memory estimation, forward pass FLOPs counting.

## Technical Deep-Dive

This agent implements advanced algorithms for forward propagation. It leverages state-of-the-art techniques to optimize performance and memory overhead. 
The internal state is carefully managed to support distributed training, mixed precision environments, and complex computational graphs. 
By isolating the domain of forward propagation, this agent allows for highly optimized mathematical operations that are strictly typed and verifiable.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| input_tensor | List[List[float]] | Input for input tensor |
| model_weights | Dict[str, List[float]] | Input for model weights |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| logits | List[float] | Output for logits |
| activation_cache_id | str | Output for activation cache id |

### State Schema
Tracks the internal lifecycle and optimization parameters unique to Forward Propagation.

## Dependencies
- Upstream: Depends on layer 6 data structures and immediate preceding layer computations.
- Downstream: Feeds into higher-level alignment or structural agents.

## Failure Modes
1. Numerical instability in forward propagation computations.
2. Out-of-memory errors during large batch processing.
3. Desynchronization in distributed states.

## Performance Characteristics
High throughput requirement. Optimized for GPU execution where applicable. Memory bandwidth bound.

## Research References
- Core papers related to Forward Propagation.
- Standard implementation techniques from PyTorch/JAX equivalents.

## Implementation Notes
Implement with strict typing and defensive numerical checks.
