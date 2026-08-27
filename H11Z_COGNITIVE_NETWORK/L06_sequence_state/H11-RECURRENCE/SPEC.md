> **Layer 6** · Sequence & State-Space Engine · `H11-RECURRENCE`

## Purpose

The H11-RECURRENCE agent manages non-linear recurrent topologies (e.g., standard LSTMs, GRUs, or custom non-linear hidden state transitions). It handles explicit sequential execution, truncated backpropagation through time (TBPTT), and stateful boundary tracking across infinite input streams.

## Technical Deep-Dive

Unlike H11-SSM-CORE which relies on parallel associative scans, this agent is designed for dense, non-linear RNNs that cannot be fully parallelized. It performs precise hidden state propagation across chunks. The state matrix $h_{t}$ and cell state $c_t$ are strictly preserved at chunk boundaries, essentially forming a segment-level recurrence (Transformer-XL style) mechanism when interacting with attention blocks.

It explicitly controls the gradient flow in recurrence, allowing selective detachment of computational graphs (TBPTT) to prevent exploding memory while maintaining theoretically infinite forward-pass context. 

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| sequential_input | List[List[float]] | Sequence to recurse over |
| reset_state | bool | Clear hidden boundaries |
| detach_gradients | bool | Perform TBPTT cutoff |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| hidden_activations | List[List[float]] | Propagated sequences |
| state_snapshot | Dict[str, List[float]] | Checkpoint for next chunk |

### State Schema
Holds dynamic sizes of $c_t$ and $h_t$ based on batch dimensionality.

## Dependencies
### Upstream (depends on)
H11-SEQUENCE
### Downstream (feeds into)
H11-GATING

## Failure Modes
- GradientExplosion: State blowing up due to poor non-linear bounds.
- StateStaleness: Forgetting to reset states across unrelated document boundaries.

## Performance Characteristics
Sequential bottleneck; highly dependent on matrix-vector hardware accelerators.
