> **Layer 8** · Physics · `H11-GRAVITATIO`

## Purpose

The H11-GRAVITATIO agent simulates the dynamical evolution of massive bodies under mutual gravitational attraction. It supports scale hierarchies from planetary rings to galactic clusters.

## Technical Deep-Dive

It implements an O(N log N) Barnes-Hut octree alongside O(N) Fast Multipole Methods (FMM). For precise orbital tracking, it utilizes 4th-order symplectic integrators to conserve the Hamiltonian over geological timescales. Post-Newtonian (PN) corrections up to 2.5PN are selectively applied to bodies exhibiting highly relativistic velocities.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| bodies | List[CelestialBody] | State vectors of mass entities |
| method | IntegrationMethod | Symplectic or RK4 |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| total_energy | float | Conserved quantity check |

### State Schema
Tracks `collision_count` and `energy_error`.

## Dependencies
### Upstream (depends on)
- None

### Downstream (feeds into)
- H11-RELATIVITAS

## Failure Modes
- Integration blow-up for extremely close encounters
- Softening parameter over-smoothing

## Performance Characteristics
Heavily relies on GPU tree-traversal algorithms.

## Research References
- Barnes, J., & Hut, P. (1986). A hierarchical O(N log N) force-calculation algorithm.
- Wisdom, J., & Holman, M. (1991). Symplectic maps for the n-body problem.

## Implementation Notes
CUDA kernels should be used for the FMM expansions.
