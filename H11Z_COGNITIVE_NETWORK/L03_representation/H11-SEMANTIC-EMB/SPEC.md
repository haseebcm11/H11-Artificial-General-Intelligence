# H11-SEMANTIC-EMB — Semantic Encoding

> **Layer 3** · Representation & Embedding · `H11-SEMANTIC-EMB`

## Purpose
Builds a co-occurrence matrix from token windows and returns a distributional vector for a target type.

## Technical Deep-Dive
A sliding window accumulates joint counts. The target's row, L2-normalised, is the distributional embedding. This is the classic count-based semantic contract before neural encoders.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| tokens | `List[str]` | Corpus tokens |
| target | `str` | Type to encode |
| window | `int` | Context radius |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| vector | `List[float]` | Distributional vector |
| vocab | `List[str]` | Column order |

### State Schema
matrix_nnz: int

## Dependencies
### Upstream (depends on)
`H11-TOKENIZER`

### Downstream (feeds into)
`H11-EMBEDDER`

## Failure Modes
- Unknown target returns a zero vector over the vocab.
- window < 1 raises.

## Performance Characteristics
Stdlib reference implementation. Suitable as an enabling embodiment and
contract test, not as a production kernel.

## Research References
- Turney & Pantel (2010). From Frequency to Meaning: Vector Space Models of Semantics.

## Implementation Notes
No third-party ML frameworks. Deterministic where possible so composition tests can assert outputs.
