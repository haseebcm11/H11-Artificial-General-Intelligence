# H11-SCENARIO — Scenario Generation

> **Layer 12** · World Models & Simulation · `H11-SCENARIO`

## Purpose
From a base numeric map, emits branches that perturb each key by ±delta.

## Technical Deep-Dive
Worst-case stress is the branch whose sum of values is extreme. Branching factor is 2*|keys|. Combinatorial explosion is capped by taking keys in sorted order only (no cross terms in this kernel).

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| base_case | `Dict[str,float]` | Initial conditions |
| delta | `float` | Absolute perturbation |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| branches | `List[dict]` | Perturbed cases |

### State Schema
last_count: int

## Dependencies
### Upstream (depends on)
`H11-PREDICT`, `H11-MENTAL-SIM`

### Downstream (feeds into)
None

## Failure Modes
- Empty base_case returns no branches.

## Performance Characteristics
Stdlib reference implementation. Suitable as an enabling embodiment and
contract test, not as a production kernel.

## Research References
- Ben-Tal, El Ghaoui, Nemirovski (2009). Robust Optimization.

## Implementation Notes
No third-party ML frameworks. Deterministic where possible so composition tests can assert outputs.
