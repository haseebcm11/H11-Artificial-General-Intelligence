# H11-PHYSICS-ENGINE — Physics Simulation

> **Layer 12** · World Models & Simulation · `H11-PHYSICS-ENGINE`

## Purpose
Semi-implicit Euler integration of point masses: v += a*dt, x += v*dt.

## Technical Deep-Dive
Each body is {x,v,a,m}. No collision in this kernel; tunneling is documented as a failure mode for a later GJK pass.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| bodies | `List[dict]` | x,v,a,m |
| dt | `float` | Timestep |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| bodies | `List[dict]` | Updated kinematics |

### State Schema
t: float

## Dependencies
### Upstream (depends on)
`H11-SIMULATE`

### Downstream (feeds into)
`H11-DYNAMICS`

## Failure Modes
- dt <= 0 raises.
- Mass <= 0 is treated as 1.

## Performance Characteristics
Stdlib reference implementation. Suitable as an enabling embodiment and
contract test, not as a production kernel.

## Research References
- Baraff (1997). An Introduction to Physically Based Modeling.

## Implementation Notes
No third-party ML frameworks. Deterministic where possible so composition tests can assert outputs.
