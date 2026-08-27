# H11-MENTAL-SIM — Mental Simulation

> **Layer 12** · World Models & Simulation · `H11-MENTAL-SIM`

## Purpose
Unrolls a list of step rewards and returns their discounted sum as plan value.

## Technical Deep-Dive
V = Σ γ^t r_t. This is the MuZero-style evaluation contract over an imagined plan, without a learned model.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| rewards | `List[float]` | Imagined rewards |
| gamma | `float` | Discount |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| expected_value | `float` | Discounted return |

### State Schema
last_value: float

## Dependencies
### Upstream (depends on)
`H11-WORLDMODEL`, `H11-IMAGINATION`

### Downstream (feeds into)
`H11-SCENARIO`

## Failure Modes
- gamma outside [0,1] is clamped.

## Performance Characteristics
Stdlib reference implementation. Suitable as an enabling embodiment and
contract test, not as a production kernel.

## Research References
- Schrittwieser et al. (2020). Mastering Atari, Go, Chess and Shogi by Planning with a Learned Model.

## Implementation Notes
No third-party ML frameworks. Deterministic where possible so composition tests can assert outputs.
