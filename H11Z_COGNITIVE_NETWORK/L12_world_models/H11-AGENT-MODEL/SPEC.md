# H11-AGENT-MODEL — Theory-of-Mind Modeling

> **Layer 12** · World Models & Simulation · `H11-AGENT-MODEL`

## Purpose
Infers another agent's action preference as a normalised frequency table (level-0 ToM).

## Technical Deep-Dive
Level-0: P(a) = count(a)/N. Nested simulation (I-POMDP) is the production target; this kernel is the belief-state contract.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| actions | `List[str]` | Observed actions |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| beliefs | `Dict[str,float]` | Action probabilities |

### State Schema
counts: Counter

## Dependencies
### Upstream (depends on)
`H11-OBJECT-PERMANENCE`, `H11-WORLDMODEL`

### Downstream (feeds into)
`H11-MENTAL-SIM`

## Failure Modes
- Empty action list returns empty beliefs.

## Performance Characteristics
Stdlib reference implementation. Suitable as an enabling embodiment and
contract test, not as a production kernel.

## Research References
- Gmytrasiewicz & Doshi (2005). A Framework for Sequential Planning in Multi-Agent Settings.

## Implementation Notes
No third-party ML frameworks. Deterministic where possible so composition tests can assert outputs.
