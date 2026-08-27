# H11-LATENT — Latent Space Modeling

> **Layer 3** · Representation & Embedding · `H11-LATENT`

## Purpose
Projects a vector into a lower-dimensional latent by chunk-pooling, then reconstructs by repeating chunks.

## Technical Deep-Dive
This is a linear autoencoder stand-in: encode averages consecutive blocks of width dim/latent_dim; decode repeats each latent coordinate. Reconstruction error is MSE. Real VAEs replace this kernel without changing the contract.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| vector | `List[float]` | Observed vector |
| latent_dim | `int` | Bottleneck width |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| latent | `List[float]` | Encoded |
| reconstruction | `List[float]` | Decoded |
| mse | `float` | Reconstruction error |

### State Schema
last_mse: float

## Dependencies
### Upstream (depends on)
`H11-EMBEDDER`

### Downstream (feeds into)
`H11-DISENTANGLE`

## Failure Modes
- latent_dim < 1 raises.
- latent_dim > len(vector) is clamped.

## Performance Characteristics
Stdlib reference implementation. Suitable as an enabling embodiment and
contract test, not as a production kernel.

## Research References
- Kingma & Welling (2014). Auto-Encoding Variational Bayes — production target.

## Implementation Notes
No third-party ML frameworks. Deterministic where possible so composition tests can assert outputs.
