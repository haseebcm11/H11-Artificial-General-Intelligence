# H11-PREDICT — Predictive Modeling

> **Layer 12** · World Models & Simulation · `H11-PREDICT`

## Purpose
Extrapolates a numeric sequence by repeating the last finite difference for a given horizon.

## Technical Deep-Dive
x_{t+k} = x_t + k * (x_t - x_{t-1}). Conformal residual can be attached later; the contract is sequence in, trajectory out.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| sequence | `List[float]` | Observed series |
| horizon | `int` | Steps ahead |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| next_states | `List[float]` | Predicted trajectory |

### State Schema
last_delta: float

## Dependencies
### Upstream (depends on)
`H11-WORLDMODEL`

### Downstream (feeds into)
`H11-SCENARIO`, `H11-MONTECARLO`

## Failure Modes
- horizon < 1 raises.
- Sequence shorter than 2 uses delta=0.

## Performance Characteristics
Stdlib reference implementation. Suitable as an enabling embodiment and
contract test, not as a production kernel.

## Research References
- Angelopoulos & Bates (2023). A Gentle Introduction to Conformal Prediction.

## Implementation Notes
No third-party ML frameworks. Deterministic where possible so composition tests can assert outputs.
