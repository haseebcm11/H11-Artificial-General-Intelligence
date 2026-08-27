# H11-MULTIMODAL-EMB — Cross-Modal Embeddings

> **Layer 3** · Representation & Embedding · `H11-MULTIMODAL-EMB`

## Purpose
Aligns a text vector and an image-side vector by cosine, returning a joint score and a concatenated shared vector.

## Technical Deep-Dive
The joint embedding is the concatenation of both L2-normalised inputs followed by a second L2 pass. Alignment score is cosine. This is the CLIP-style contract without a trained encoder.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| text_vec | `List[float]` | Text embedding |
| image_vec | `List[float]` | Image embedding |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| alignment | `float` | Cosine |
| joint | `List[float]` | Shared vector |

### State Schema
last_alignment: float

## Dependencies
### Upstream (depends on)
`H11-EMBEDDER`

### Downstream (feeds into)
`H11-SIMILARITY`

## Failure Modes
- Either side empty raises.

## Performance Characteristics
Stdlib reference implementation. Suitable as an enabling embodiment and
contract test, not as a production kernel.

## Research References
- Radford et al. (2021). Learning Transferable Visual Models From Natural Language Supervision.

## Implementation Notes
No third-party ML frameworks. Deterministic where possible so composition tests can assert outputs.
