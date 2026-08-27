# H11-SIMULATE — Environment Simulation

> **Layer 12** · World Models & Simulation · `H11-SIMULATE`

## Purpose
Steps a 1-D bounded grid: position' = clip(position + action, 0, width-1).

## Technical Deep-Dive
This is the Gym-style step contract (obs, action) → (obs, reward, done) without an external simulator. Reward is +1 for moving toward a goal cell.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| position | `int` | Current cell |
| action | `int` | -1 or +1 |
| goal | `int` | Target cell |
| width | `int` | Grid size |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| position | `int` | Next cell |
| reward | `float` | Step reward |
| done | `bool` | At goal |

### State Schema
steps: int

## Dependencies
### Upstream (depends on)
`H11-WORLDMODEL`

### Downstream (feeds into)
`H11-PHYSICS-ENGINE`

## Failure Modes
- width < 2 raises.

## Performance Characteristics
Stdlib reference implementation. Suitable as an enabling embodiment and
contract test, not as a production kernel.

## Research References
- Towers et al. (2023). Gymnasium — interface prior art.

## Implementation Notes
No third-party ML frameworks. Deterministic where possible so composition tests can assert outputs.
