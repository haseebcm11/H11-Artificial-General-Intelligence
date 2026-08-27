> **Layer 9** · Inference & Serving Engine · `H11-BATCHING-INF`

## Purpose

In-flight batching, chunked prefill, and request queueing.
This agent is critical for the Inference & Serving Engine by ensuring optimized and scalable continuous batching.

## Technical Deep-Dive

H11-BATCHING-INF implements continuous (in-flight) batching. It mixes prefill and decode phases in the same batch using chunked prefill to maximize GPU SM utilization while adhering to latency SLAs.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| new_requests | List[str] | Incoming requests |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| active_batch | List[str] | Requests selected for next iteration |

### State Schema
queue_depth: Pending requests in queue

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
