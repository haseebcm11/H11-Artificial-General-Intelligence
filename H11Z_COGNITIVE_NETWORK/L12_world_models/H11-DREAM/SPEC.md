# H11-DREAM — Dream / Replay Generation

> **Layer 12** · World Models & Simulation · `H11-DREAM`

## Purpose
Hindsight replay: copies transitions and replaces the goal with the achieved state.

## Technical Deep-Dive
Each item is {state, action, goal, next_state}. Synthetic items set goal := next_state and reward := 1. This is HER's relabel contract.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| buffer | `List[dict]` | Real transitions |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| synthetic_batch | `List[dict]` | Relabelled transitions |

### State Schema
last_batch: int

## Dependencies
### Upstream (depends on)
`H11-WORLDMODEL`

### Downstream (feeds into)
`H11-PREDICT`

## Failure Modes
- Items missing next_state are skipped.

## Performance Characteristics
Stdlib reference implementation. Suitable as an enabling embodiment and
contract test, not as a production kernel.

## Research References
- Andrychowicz et al. (2017). Hindsight Experience Replay.

## Implementation Notes
No third-party ML frameworks. Deterministic where possible so composition tests can assert outputs.
