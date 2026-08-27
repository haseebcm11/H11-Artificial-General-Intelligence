# H11-CONTRASTIVE — Contrastive Representation

> **Layer 3** · Representation & Embedding · `H11-CONTRASTIVE`

## Purpose
Computes an NT-Xent-style loss between a positive pair and a set of negatives.

## Technical Deep-Dive
score(i,j) = cosine(i,j)/temperature. Loss is -log softmax of the positive among negatives. Used as a training signal contract, not a trainer.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| anchor | `List[float]` | Anchor |
| positive | `List[float]` | Positive |
| negatives | `List[List[float]]` | Negatives |
| temperature | `float` | Temperature |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| loss | `float` | NT-Xent loss |
| positive_sim | `float` | Anchor-positive cosine |

### State Schema
last_loss: float

## Dependencies
### Upstream (depends on)
`H11-EMBEDDER`

### Downstream (feeds into)
`H11-LATENT`

## Failure Modes
- temperature <= 0 raises.
- Empty negatives still compute a defined loss against the positive only.

## Performance Characteristics
Stdlib reference implementation. Suitable as an enabling embodiment and
contract test, not as a production kernel.

## Research References
- Chen et al. (2020). A Simple Framework for Contrastive Learning of Visual Representations.

## Implementation Notes
No third-party ML frameworks. Deterministic where possible so composition tests can assert outputs.
