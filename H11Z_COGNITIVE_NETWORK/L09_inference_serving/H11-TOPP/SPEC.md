> **Layer 9** · Inference & Serving Engine · `H11-TOPP`

## Purpose

Top-p (nucleus) sampling based on cumulative probability mass.
This agent is critical for the Inference & Serving Engine by ensuring optimized and scalable nucleus sampling.

## Technical Deep-Dive

H11-TOPP focuses on nucleus sampling, where only tokens comprising the top p portion of probability mass are kept. It also includes Tail-Free Sampling to smooth over heavy-tailed distributions.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| probs | List[float] | Token probabilities |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| filtered_probs | List[float] | Probs restricted to top-p mass |

### State Schema
last_p: Last p threshold used

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
