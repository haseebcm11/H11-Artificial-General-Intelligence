# H11-UNCERTAINTY — Uncertainty Estimation

> **Layer 12** · World Models & Simulation · `H11-UNCERTAINTY`

## Purpose
Splits a list of numeric predictions into mean, variance (epistemic stand-in), and entropy of a softmax histogram (aleatoric stand-in).

## Technical Deep-Dive
Variance of the ensemble is epistemic. Entropy of a 4-bin histogram of the same values is aleatoric. Deep ensembles replace the list source later.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| predictions | `List[float]` | Ensemble outputs |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| mean | `float` | Mean |
| variance | `float` | Variance |
| entropy | `float` | Histogram entropy |

### State Schema
last_entropy: float

## Dependencies
### Upstream (depends on)
`H11-PREDICT`

### Downstream (feeds into)
`H11-BAYES`, `H11-MONTECARLO`

## Failure Modes
- Empty predictions raise.

## Performance Characteristics
Stdlib reference implementation. Suitable as an enabling embodiment and
contract test, not as a production kernel.

## Research References
- Lakshminarayanan et al. (2017). Simple and Scalable Predictive Uncertainty Estimation using Deep Ensembles.

## Implementation Notes
No third-party ML frameworks. Deterministic where possible so composition tests can assert outputs.
