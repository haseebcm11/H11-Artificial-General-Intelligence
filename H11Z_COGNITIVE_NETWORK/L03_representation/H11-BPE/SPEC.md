# H11-BPE — Byte-Pair Encoding

> **Layer 3** · Representation & Embedding · `H11-BPE`

## Purpose
Learns a merge table from a corpus by iteratively pairing the most frequent adjacent symbols.

## Technical Deep-Dive
Each word is split into characters plus a word-boundary marker. At every step the most frequent adjacent pair is recorded as a merge and collapsed. The resulting table is the contract consumed by H11-TOKENIZER.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| corpus | `List[str]` | Training texts |
| num_merges | `int` | Number of merge operations |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| merges | `List[Tuple[str,str]]` | Ordered merge table |
| vocab_size | `int` | Symbol count after merges |

### State Schema
pair_stats: Counter

## Dependencies
### Upstream (depends on)
None

### Downstream (feeds into)
`H11-TOKENIZER`, `H11-SUBWORD`

## Failure Modes
- Corpus of empty strings yields an empty merge table.
- Ties in pair frequency are broken lexicographically for determinism.

## Performance Characteristics
Stdlib reference implementation. Suitable as an enabling embodiment and
contract test, not as a production kernel.

## Research References
- Gage (1994). A New Algorithm for Data Compression.
- Sennrich et al. (2016). Neural Machine Translation of Rare Words with Subword Units.

## Implementation Notes
No third-party ML frameworks. Deterministic where possible so composition tests can assert outputs.
