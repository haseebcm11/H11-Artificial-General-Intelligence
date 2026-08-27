> **Layer 9** · Inference & Serving Engine · `H11-SAMPLING`

## Purpose

Advanced token sampling techniques including mirostat and contrastive decoding.
This agent is critical for the Inference & Serving Engine by ensuring optimized and scalable token sampling.

## Technical Deep-Dive

H11-SAMPLING implements diverse strategies for token generation. Mirostat adaptively controls the perplexity of generated text, while contrastive decoding penalizes tokens preferred by a smaller draft model.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| logits | List[float] | Logits from model |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| sampled_token | int | Chosen token ID |

### State Schema
random_seed: Seed for deterministic sampling

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
