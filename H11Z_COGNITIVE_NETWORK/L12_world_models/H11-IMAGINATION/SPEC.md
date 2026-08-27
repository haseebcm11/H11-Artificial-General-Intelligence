# H11-IMAGINATION — Imagination Engine

> **Layer 12** · World Models & Simulation · `H11-IMAGINATION`

## Purpose
Enumerates the Cartesian product of discrete constraint tokens into candidate scenarios.

## Technical Deep-Dive
Each constraint is a list of allowed symbols. The engine emits every combination up to a cap. Energy-based sampling can replace enumeration later.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| options | `List[List[str]]` | Per-slot choices |
| cap | `int` | Max scenarios |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| scenarios | `List[List[str]]` | Enumerated combinations |

### State Schema
emitted: int

## Dependencies
### Upstream (depends on)
`H11-WORLDMODEL`

### Downstream (feeds into)
`H11-MENTAL-SIM`

## Failure Modes
- cap < 1 raises.
- Empty options yields one empty scenario.

## Performance Characteristics
Stdlib reference implementation. Suitable as an enabling embodiment and
contract test, not as a production kernel.

## Research References
- Du & Mordatch (2019). Implicit Generation and Generalization with Energy Based Models.

## Implementation Notes
No third-party ML frameworks. Deterministic where possible so composition tests can assert outputs.
