> **Layer 9** · Inference & Serving Engine · `H11-TOPK`

## Purpose

Truncating probability distributions to the top K tokens.
This agent is critical for the Inference & Serving Engine by ensuring optimized and scalable top-k filtering.

## Technical Deep-Dive

H11-TOPK implements efficient top-k retrieval on probability distributions. It utilizes GPU-optimized partial sorts and can dynamically adjust K based on distribution entropy to preserve viable choices.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| logits | List[float] | Logits to filter |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| filtered_logits | List[float] | Logits with non-top-k set to -inf |

### State Schema
dynamic_k_history: History of dynamically chosen K values

## Dependencies
- Upstream: H11-INFER
- Downstream: H11-SERVING

## Failure Modes
- OOM Errors
- High Latency Spikes
- Precision Degradation

## Performance Characteristics
- Optimized for GPU throughput.
- Minimizes VRAM fragmentation.

## Research References
- vLLM PagedAttention
- Accelerating Large Language Model Decoding with Speculative Sampling

## Implementation Notes
Focus on avoiding Python GIL locks and optimizing kernel execution.
