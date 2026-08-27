# H11-WORLDMODEL — World Model Core

> **Layer 12** · World Models & Simulation · `H11-WORLDMODEL`

## Purpose
Maintains a latent world state by exponentially smoothing observations: h_t = (1-α) h_{t-1} + α x_t.

## Technical Deep-Dive
This is a one-state RSSM stand-in. Stochasticity is injected as a supplied noise term, not sampled internally, so tests stay deterministic.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| obs | `List[float]` | Observation |
| alpha | `float` | Smoothing |
| noise | `List[float]` | Optional process noise |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| latent | `List[float]` | Updated hidden state |

### State Schema
h_t: List[float]

## Dependencies
### Upstream (depends on)
None

### Downstream (feeds into)
`H11-PREDICT`, `H11-SIMULATE`, `H11-MENTAL-SIM`, `H11-DREAM`, `H11-IMAGINATION`

## Failure Modes
- alpha outside (0,1] is clamped.
- Empty obs raises.

## Performance Characteristics
Stdlib reference implementation. Suitable as an enabling embodiment and
contract test, not as a production kernel.

## Research References
- Hafner et al. (2023). Mastering Diverse Domains through World Models (DreamerV3).

## Implementation Notes
No third-party ML frameworks. Deterministic where possible so composition tests can assert outputs.
