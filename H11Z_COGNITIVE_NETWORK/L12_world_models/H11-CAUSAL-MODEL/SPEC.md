# H11-CAUSAL-MODEL — Causal World Model

> **Layer 12** · World Models & Simulation · `H11-CAUSAL-MODEL`

## Purpose
Builds a DAG by thresholding absolute Pearson correlation and directing edges from earlier to later indices.

## Technical Deep-Dive
This is not PC/GES. It is an enabling discovery contract: correlated variables get a directed edge consistent with a supplied variable order, and cycles are impossible because order is topological.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| columns | `List[List[float]]` | Variable-major samples |
| threshold | `float` | Abs-correlation cutoff |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| edges | `List[Tuple[int,int,float]]` | i→j with correlation |

### State Schema
n_vars: int

## Dependencies
### Upstream (depends on)
None

### Downstream (feeds into)
`H11-COUNTERFACTUAL-WORLD`

## Failure Modes
- Fewer than 2 samples yields no edges.
- Ragged columns are truncated.

## Performance Characteristics
Stdlib reference implementation. Suitable as an enabling embodiment and
contract test, not as a production kernel.

## Research References
- Spirtes, Glymour, Scheines (2000). Causation, Prediction, and Search.

## Implementation Notes
No third-party ML frameworks. Deterministic where possible so composition tests can assert outputs.
