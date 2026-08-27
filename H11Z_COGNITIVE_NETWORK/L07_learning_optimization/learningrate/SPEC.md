> **Layer 7** · Learning & Optimization · `H11-LEARNINGRATE`

## Purpose

The `H11-LEARNINGRATE` agent is responsible for lr scheduling within the H11 Cognitive Substrate. 
Learning rate schedules: warmup, linear decay, cosine annealing, cosine with restarts, step decay, polynomial decay, one-cycle policy, WSD.

## Technical Deep-Dive

This agent implements advanced algorithms for lr scheduling. It leverages state-of-the-art techniques to optimize performance and memory overhead. 
The internal state is carefully managed to support distributed training, mixed precision environments, and complex computational graphs. 
By isolating the domain of lr scheduling, this agent allows for highly optimized mathematical operations that are strictly typed and verifiable.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| current_step | int | Input for current step |
| total_steps | int | Input for total steps |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| current_lr | float | Output for current lr |
| phase | str | Output for phase |

### State Schema
Tracks the internal lifecycle and optimization parameters unique to LR Scheduling.

## Dependencies
- Upstream: Depends on layer 6 data structures and immediate preceding layer computations.
- Downstream: Feeds into higher-level alignment or structural agents.

## Failure Modes
1. Numerical instability in lr scheduling computations.
2. Out-of-memory errors during large batch processing.
3. Desynchronization in distributed states.

## Performance Characteristics
High throughput requirement. Optimized for GPU execution where applicable. Memory bandwidth bound.

## Research References
- Core papers related to LR Scheduling.
- Standard implementation techniques from PyTorch/JAX equivalents.

## Implementation Notes
Implement with strict typing and defensive numerical checks.
