# H11-FEATURE — Feature Extraction

> **Layer 3** · Representation & Embedding · `H11-FEATURE`

## Purpose
Extracts bag-of-tokens TF weights and the top-n salient types from a token sequence.

## Technical Deep-Dive
TF(t) = count(t)/N. Salience is TF (IDF needs a background corpus supplied later). Output is a stable feature dict for H11-EMBEDDER or classifiers.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| tokens | `List[str]` | Token sequence |
| top_n | `int` | How many salient types |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| tf | `Dict[str,float]` | Term frequencies |
| salient | `List[str]` | Top types |

### State Schema
last_n_types: int

## Dependencies
### Upstream (depends on)
`H11-TOKENIZER`

### Downstream (feeds into)
`H11-EMBEDDER`

## Failure Modes
- Empty tokens returns empty maps.
- top_n < 1 raises.

## Performance Characteristics
Stdlib reference implementation. Suitable as an enabling embodiment and
contract test, not as a production kernel.

## Research References
- Salton & Buckley (1988). Term-weighting approaches in automatic text retrieval.

## Implementation Notes
No third-party ML frameworks. Deterministic where possible so composition tests can assert outputs.
