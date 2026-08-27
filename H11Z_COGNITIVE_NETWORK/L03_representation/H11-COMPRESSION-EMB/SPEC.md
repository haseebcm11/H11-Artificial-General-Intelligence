# H11-COMPRESSION-EMB — Embedding Compression

> **Layer 3** · Representation & Embedding · `H11-COMPRESSION-EMB`

## Purpose
Truncates a vector to the first k dimensions and renormalises (Matryoshka-style prefix).

## Technical Deep-Dive
Prefix truncation is the enabling form of nested embeddings. Product quantization can replace this kernel later; the contract is (vector, k) → shorter vector.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| vector | `List[float]` | Full embedding |
| k | `int` | Kept dimensions |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| compressed | `List[float]` | Prefix, L2-normalised |
| kept | `int` | Actual width |

### State Schema
last_k: int

## Dependencies
### Upstream (depends on)
`H11-EMBEDDER`

### Downstream (feeds into)
`H11-VECTORDb`

## Failure Modes
- k < 1 raises.
- k > len(vector) is clamped.

## Performance Characteristics
Stdlib reference implementation. Suitable as an enabling embodiment and
contract test, not as a production kernel.

## Research References
- Kusupati et al. (2022). Matryoshka Representation Learning.

## Implementation Notes
No third-party ML frameworks. Deterministic where possible so composition tests can assert outputs.
