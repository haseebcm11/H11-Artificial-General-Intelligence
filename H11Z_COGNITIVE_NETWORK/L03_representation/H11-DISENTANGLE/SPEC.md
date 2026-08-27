# H11-DISENTANGLE — Disentangled Representations

> **Layer 3** · Representation & Embedding · `H11-DISENTANGLE`

## Purpose
Scores each latent coordinate by its variance across a batch, treating high-variance axes as factors.

## Technical Deep-Dive
For a batch of latent vectors, per-dimension variance is computed. Axes below epsilon are marked collapsed. This is the β-VAE monitoring contract, not a trained disentangler.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| latents | `List[List[float]]` | Batch of latents |
| epsilon | `float` | Collapse threshold |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| variances | `List[float]` | Per-axis variance |
| collapsed | `List[int]` | Collapsed axis indices |

### State Schema
last_collapsed: int

## Dependencies
### Upstream (depends on)
`H11-LATENT`

### Downstream (feeds into)
`H11-SEMANTIC-EMB`

## Failure Modes
- Empty batch raises.
- Ragged latents are truncated to the shortest.

## Performance Characteristics
Stdlib reference implementation. Suitable as an enabling embodiment and
contract test, not as a production kernel.

## Research References
- Higgins et al. (2017). β-VAE: Learning Basic Visual Concepts with a Constrained Variational Framework.

## Implementation Notes
No third-party ML frameworks. Deterministic where possible so composition tests can assert outputs.
