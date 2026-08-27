# H11-DYNAMICS — Dynamics Modeling

> **Layer 12** · World Models & Simulation · `H11-DYNAMICS`

## Purpose
Estimates a local vector field by finite differences of a state trajectory.

## Technical Deep-Dive
f(x_t) ≈ (x_{t+1}-x_t)/dt. The field is returned as a list of deltas aligned with the trajectory (last point copies the previous delta).

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| state_traj | `List[float]` | Trajectory |
| dt | `float` | Sample interval |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| vector_field | `List[float]` | Per-step derivatives |

### State Schema
last_dt: float

## Dependencies
### Upstream (depends on)
`H11-PHYSICS-ENGINE`

### Downstream (feeds into)
`H11-WORLDMODEL`

## Failure Modes
- dt <= 0 raises.
- Trajectory shorter than 2 returns zeros.

## Performance Characteristics
Stdlib reference implementation. Suitable as an enabling embodiment and
contract test, not as a production kernel.

## Research References
- Chen et al. (2018). Neural Ordinary Differential Equations.

## Implementation Notes
No third-party ML frameworks. Deterministic where possible so composition tests can assert outputs.
