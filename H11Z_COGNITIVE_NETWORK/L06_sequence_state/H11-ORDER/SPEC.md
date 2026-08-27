> **Layer 6** · Sequence & State-Space Engine · `H11-ORDER`

## Purpose

The H11-ORDER agent abstracts away sequence ordering, allowing the substrate to transition between strictly ordered sequences, permutation-invariant sets, and order-agnostic representations. It enables models like XLNet (permutation language modeling) and facilitates robust data augmentation via shuffling and sorting constraints.

## Technical Deep-Dive

Not all sequential data is strictly ordered (e.g., sets of detected objects, unordered document retrieval results). H11-ORDER manages order embeddings, allowing components to learn positional relativity rather than absolute position. It creates stochastic permutation matrices during training to maximize the expectation over all factorizations of the joint probability (XLNet approach).

It also manages document/sentence ordering logic, scoring the coherence of shuffled segments to predict topological structure. When inputting purely invariant sets, it strips standard positional encoding and injects "set-aggregating" dummy tokens to gather context symmetrically.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| sequence | List[Any] | Base sequence |
| order_mode | str | 'strict', 'permutation', 'set' |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| permuted_sequence | List[Any] | Reordered data |
| permutation_matrix | List[int] | Mapping for inverse transform |

### State Schema
Tracks random seed states for deterministic shuffling across distributed workers.

## Dependencies
- Upstream: H11-SEQUENCE
- Downstream: Loss Functions

## Failure Modes
- DeterminismBreak: Different workers shuffling differently, crashing distributed synchronization.
- PositionalLeakage: Providing strict positional embeddings to a sequence supposedly treated as an unordered set.

## Research References
- XLNet: Generalized Autoregressive Pretraining for Language Understanding
- Deep Sets (Zaheer et al.)
