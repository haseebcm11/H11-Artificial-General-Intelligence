# H11-BAYES — Bayesian Inference

> **Layer 12** · World Models & Simulation · `H11-BAYES`

## Purpose
Conjugate Beta-Binomial update: posterior = Beta(α+successes, β+failures).

## Technical Deep-Dive
Prior (alpha, beta), likelihood (successes, failures). Posterior mean is (α')/(α'+β'). Variational Gaussian posteriors are the production target.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| alpha | `float` | Prior α |
| beta | `float` | Prior β |
| successes | `int` | Observed successes |
| failures | `int` | Observed failures |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| alpha | `float` | Posterior α |
| beta | `float` | Posterior β |
| mean | `float` | Posterior mean |

### State Schema
last_mean: float

## Dependencies
### Upstream (depends on)
`H11-UNCERTAINTY`

### Downstream (feeds into)
`H11-MONTECARLO`

## Failure Modes
- Non-positive prior parameters raise.
- Negative counts raise.

## Performance Characteristics
Stdlib reference implementation. Suitable as an enabling embodiment and
contract test, not as a production kernel.

## Research References
- Gelman et al. (2013). Bayesian Data Analysis.

## Implementation Notes
No third-party ML frameworks. Deterministic where possible so composition tests can assert outputs.
