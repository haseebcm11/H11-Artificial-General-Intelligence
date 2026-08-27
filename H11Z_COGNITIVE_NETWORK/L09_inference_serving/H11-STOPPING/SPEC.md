> **Layer 9** · Inference & Serving Engine · `H11-STOPPING`

## Purpose

Multi-sequence matching, regex stopping, and structural limits.
This agent is critical for the Inference & Serving Engine by ensuring optimized and scalable stop sequences.

## Technical Deep-Dive

H11-STOPPING applies complex stopping criteria during generation. It supports standard EOS tokens, list of exact string matches, regex-based structured stopping, and logical combinations of constraints.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| generated_text | str | Currently generated string |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| should_stop | bool | Whether to halt generation |

### State Schema
active_rules: Number of registered stop rules

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
