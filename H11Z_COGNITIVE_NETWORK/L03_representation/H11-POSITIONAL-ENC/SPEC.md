# H11-POSITIONAL-ENC — Positional Encoding

> **Layer 3** · Representation & Embedding · `H11-POSITIONAL-ENC`

## Purpose
Adds sinusoidal or rotary positional coordinates to a sequence of token vectors.

## Technical Deep-Dive
Sinusoidal: PE(pos,2i)=sin(pos/10000^{2i/d}), PE(pos,2i+1)=cos(...). Rotary: 2D rotation of consecutive pairs by pos*theta. Both are stateless functions of position.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| vectors | `List[List[float]]` | Token vectors |
| mode | `str` | sinusoidal|rope |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| encoded | `List[List[float]]` | Position-aware vectors |

### State Schema
last_mode: str

## Dependencies
### Upstream (depends on)
`H11-TOKENIZER`, `H11-EMBEDDER`

### Downstream (feeds into)
`H11-INDEX`

## Failure Modes
- Unknown mode raises.
- Empty sequence returns empty.

## Performance Characteristics
Stdlib reference implementation. Suitable as an enabling embodiment and
contract test, not as a production kernel.

## Research References
- Vaswani et al. (2017). Attention Is All You Need.
- Su et al. (2021). RoFormer: Enhanced Transformer with Rotary Position Embedding.

## Implementation Notes
No third-party ML frameworks. Deterministic where possible so composition tests can assert outputs.
