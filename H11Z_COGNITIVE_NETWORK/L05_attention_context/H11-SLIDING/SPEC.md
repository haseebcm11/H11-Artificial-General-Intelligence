> **Layer 5** · Attention & Context Engine · `H11-SLIDING`

## Purpose
Manages local sliding context windows (e.g., Mistral's SWA) to process infinite sequences with bounded memory footprint.

This agent ensures optimal performance in Layer 5 by encapsulating deep mathematical mechanics specific to its domain, isolating complex transformations from generic processing flows.

## Technical Deep-Dive
Sliding Window Attention (SWA) computes attention only over a fixed history window $W$. Layer stacking implicitly expands the receptive field, allowing a model with window $W$ and $L$ layers to attend to context $W \times L$. This agent handles overlapping chunk rollups and KV cache rotation.

The implementation strictly adheres to theoretical boundaries, avoiding heuristics where deterministic matrices govern the flow. Entropy tracking and structural integrity checks are native to its execution.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| sequence | Any | Input sequence |
| window_size | int | Local window bounds |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| windowed_context | Any | Sliding window output |

### State Schema
- `receptive_field`: Effective context size

## Dependencies
- **Downstream**: H11-KVCACHE, H11-CONTEXT-WINDOW

## Implementation Notes
Highly optimized pathing. Memory layouts assume continuous tensor spaces where applicable.
