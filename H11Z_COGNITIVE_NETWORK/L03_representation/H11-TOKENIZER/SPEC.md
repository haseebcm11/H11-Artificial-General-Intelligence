# H11-TOKENIZER — Tokenizer

> **Layer 3** · Representation & Embedding · `H11-TOKENIZER`

## Purpose
Splits raw text into tokens using a Unicode-aware word/punct scanner, optionally applying a supplied BPE merge table.

## Technical Deep-Dive
The scanner emits maximal alphanumeric runs and isolated punctuation. If merge pairs are provided, they are applied left-to-right exactly as in Sennrich BPE, so this agent is the execution surface for H11-BPE rather than a second tokenizer.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| text | `str` | Raw input text |
| merges | `List[Tuple[str,str]]` | Optional BPE merge table |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| tokens | `List[str]` | Token sequence |

### State Schema
vocab_seen: Counter[str]

## Dependencies
### Upstream (depends on)
`H11-BPE`

### Downstream (feeds into)
`H11-EMBEDDER`, `H11-SUBWORD`, `H11-POSITIONAL-ENC`, `H11-FEATURE`

## Failure Modes
- Empty input yields an empty sequence, which downstream embedders must reject.
- Merge tables that contain unseen pairs are skipped, not errors.

## Performance Characteristics
Stdlib reference implementation. Suitable as an enabling embodiment and
contract test, not as a production kernel.

## Research References
- Sennrich et al. (2016). Neural Machine Translation of Rare Words with Subword Units.

## Implementation Notes
No third-party ML frameworks. Deterministic where possible so composition tests can assert outputs.
