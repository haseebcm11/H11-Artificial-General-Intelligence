# H11-MONTECARLO — Monte Carlo Methods

> **Layer 12** · World Models & Simulation · `H11-MONTECARLO`

## Purpose
Systematic resampling of weighted particles; returns the weighted mean and effective sample size.

## Technical Deep-Dive
ESS = 1 / Σ w_i² after normalisation. Systematic resampling walks a single offset through the cumulative weights.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| particles | `List[float]` | Particle values |
| weights | `List[float]` | Unnormalised weights |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| resampled | `List[float]` | Resampled particles |
| mean | `float` | Weighted mean |
| ess | `float` | Effective sample size |

### State Schema
last_ess: float

## Dependencies
### Upstream (depends on)
`H11-UNCERTAINTY`, `H11-PREDICT`

### Downstream (feeds into)
`H11-SCENARIO`

## Failure Modes
- Mismatched lengths raise.
- All-zero weights raise.

## Performance Characteristics
Stdlib reference implementation. Suitable as an enabling embodiment and
contract test, not as a production kernel.

## Research References
- Doucet, de Freitas, Gordon (2001). Sequential Monte Carlo Methods in Practice.

## Implementation Notes
No third-party ML frameworks. Deterministic where possible so composition tests can assert outputs.
