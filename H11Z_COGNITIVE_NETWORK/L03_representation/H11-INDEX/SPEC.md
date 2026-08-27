# H11-INDEX — ANN Index

> **Layer 3** · Representation & Embedding · `H11-INDEX`

## Purpose
Builds a brute-force cosine index over stored vectors and returns top-k neighbours.

## Technical Deep-Dive
For the enabling embodiment, 'ANN' is exact cosine over the whole store (k-NN). Graph approximations belong in a later kernel; the contract (query vector in, ranked ids out) stays.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| vectors | `Dict[str,List[float]]` | Id to vector |
| query | `List[float]` | Query vector |
| k | `int` | Neighbour count |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| neighbors | `List[Tuple[str,float]]` | Id and cosine, descending |

### State Schema
size: int

## Dependencies
### Upstream (depends on)
`H11-VECTORDb`, `H11-EMBEDDER`

### Downstream (feeds into)
`H11-SIMILARITY`

## Failure Modes
- k < 1 raises.
- Empty store returns an empty neighbour list.

## Performance Characteristics
Stdlib reference implementation. Suitable as an enabling embodiment and
contract test, not as a production kernel.

## Research References
- Malkov & Yashunin (2018). HNSW graphs — cited as the production target, not this kernel.

## Implementation Notes
No third-party ML frameworks. Deterministic where possible so composition tests can assert outputs.
