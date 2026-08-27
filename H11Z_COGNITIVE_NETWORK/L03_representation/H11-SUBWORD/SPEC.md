# H11-SUBWORD — Subword Segmentation

> **Layer 3** · Representation & Embedding · `H11-SUBWORD`

## Purpose
Falls back from whole-word tokens to character n-grams when a token is absent from a known vocabulary.

## Technical Deep-Dive
Each token is kept if it is in vocab. Otherwise it is split into overlapping character n-grams of width n so rare or misspelled forms still produce a dense bag for H11-EMBEDDER.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| tokens | `List[str]` | Tokenizer output |
| vocab | `List[str]` | Known types |
| n | `int` | n-gram width |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| pieces | `List[str]` | Subword pieces |

### State Schema
oov_count: int

## Dependencies
### Upstream (depends on)
`H11-TOKENIZER`, `H11-BPE`

### Downstream (feeds into)
`H11-EMBEDDER`

## Failure Modes
- n < 1 is rejected.
- Empty vocab treats every token as OOV.

## Performance Characteristics
Stdlib reference implementation. Suitable as an enabling embodiment and
contract test, not as a production kernel.

## Research References
- Bojanowski et al. (2017). Enriching Word Vectors with Subword Information.

## Implementation Notes
No third-party ML frameworks. Deterministic where possible so composition tests can assert outputs.
