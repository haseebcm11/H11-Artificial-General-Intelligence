# H11-EMBEDDER — Embedding Generation

> **Layer 3** · Representation & Embedding · `H11-EMBEDDER`

## Purpose
Maps tokens to dense vectors with a deterministic hashing trick so identical tokens always produce identical vectors.

## Technical Deep-Dive
Each token is hashed into dim buckets with two hash seeds and accumulated, then L2-normalised. This is the FNV-style hashing trick, not a trained matrix; it exists so memory and similarity agents have a stable vector contract.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| tokens | `List[str]` | Token or subword sequence |
| dim | `int` | Vector width |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| vector | `List[float]` | L2-normalised embedding |

### State Schema
last_dim: int

## Dependencies
### Upstream (depends on)
`H11-TOKENIZER`, `H11-SUBWORD`

### Downstream (feeds into)
`H11-VECTORDb`, `H11-INDEX`, `H11-SIMILARITY`, `H11-CONTRASTIVE`, `H11-LATENT`, `H11-COMPRESSION-EMB`

## Failure Modes
- Empty token list raises.
- dim < 1 raises.

## Performance Characteristics
Stdlib reference implementation. Suitable as an enabling embodiment and
contract test, not as a production kernel.

## Research References
- Weinberger et al. (2009). Feature Hashing for Large Scale Multitask Learning.

## Implementation Notes
No third-party ML frameworks. Deterministic where possible so composition tests can assert outputs.
