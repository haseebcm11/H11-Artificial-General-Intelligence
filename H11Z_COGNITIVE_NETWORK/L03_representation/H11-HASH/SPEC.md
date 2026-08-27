# H11-HASH — Locality-Sensitive Hashing

> **Layer 3** · Representation & Embedding · `H11-HASH`

## Purpose
Projects a vector through random hyperplanes to a bit string (SimHash) for Hamming-space retrieval.

## Technical Deep-Dive
Each bit is sign(dot(v, plane_i)) where planes are generated from a seeded LCG so hashes are deterministic. Hamming distance between hashes estimates cosine.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| vector | `List[float]` | Input |
| bits | `int` | Hash width |
| seed | `int` | Plane seed |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| bits | `str` | Bit string |
| int_hash | `int` | Integer form |

### State Schema
last_bits: int

## Dependencies
### Upstream (depends on)
`H11-SIMILARITY`, `H11-EMBEDDER`

### Downstream (feeds into)
`H11-INDEX`

## Failure Modes
- bits < 1 raises.

## Performance Characteristics
Stdlib reference implementation. Suitable as an enabling embodiment and
contract test, not as a production kernel.

## Research References
- Charikar (2002). Similarity estimation techniques from rounding algorithms.

## Implementation Notes
No third-party ML frameworks. Deterministic where possible so composition tests can assert outputs.
