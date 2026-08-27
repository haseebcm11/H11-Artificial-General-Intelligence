# H11-COUNTERFACTUAL-WORLD — Counterfactual Simulation

> **Layer 12** · World Models & Simulation · `H11-COUNTERFACTUAL-WORLD`

## Purpose
Applies Pearl's abduction–action–prediction on a linear SCM y = a*x + u.

## Technical Deep-Dive
Abduction: u = y_obs - a*x_obs. Action: x := x_do. Prediction: y_cf = a*x_do + u. Unobserved confounders are out of scope and listed as a failure mode.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| x_obs | `float` | Factual x |
| y_obs | `float` | Factual y |
| a | `float` | Structural coefficient |
| x_do | `float` | Intervention |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| u | `float` | Abduced noise |
| y_cf | `float` | Counterfactual y |

### State Schema
last_u: float

## Dependencies
### Upstream (depends on)
`H11-CAUSAL-MODEL`

### Downstream (feeds into)
`H11-SCENARIO`

## Failure Modes
- This kernel assumes no hidden confounder; if u is not independent of x the counterfactual is unidentifiable.

## Performance Characteristics
Stdlib reference implementation. Suitable as an enabling embodiment and
contract test, not as a production kernel.

## Research References
- Pearl (2009). Causality.

## Implementation Notes
No third-party ML frameworks. Deterministic where possible so composition tests can assert outputs.
