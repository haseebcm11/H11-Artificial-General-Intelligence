# H11-SIMILARITY — Similarity Search

> **Layer 3** · Representation & Embedding · `H11-SIMILARITY`

## Purpose
Computes cosine, dot, or Euclidean distance between two equal-length vectors.

## Technical Deep-Dive
Metric is selected by name. Euclidean is returned as a distance (lower is closer); cosine and dot are similarities (higher is closer).

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| a | `List[float]` | Left vector |
| b | `List[float]` | Right vector |
| metric | `str` | cosine|dot|euclidean |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| score | `float` | Similarity or distance |

### State Schema
last_metric: str

## Dependencies
### Upstream (depends on)
`H11-EMBEDDER`, `H11-INDEX`

### Downstream (feeds into)
`H11-HASH`

## Failure Modes
- Unknown metric raises.
- Mismatched lengths raise.

## Performance Characteristics
Stdlib reference implementation. Suitable as an enabling embodiment and
contract test, not as a production kernel.

## Research References
- Charikar (2002). Similarity estimation techniques from rounding algorithms.

## Implementation Notes
No third-party ML frameworks. Deterministic where possible so composition tests can assert outputs.
