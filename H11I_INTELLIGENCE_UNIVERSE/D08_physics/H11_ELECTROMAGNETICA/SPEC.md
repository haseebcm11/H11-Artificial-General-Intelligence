> **Layer 8** · Physics · `H11-ELECTROMAGNETICA`

## Purpose

The H11-ELECTROMAGNETICA agent simulates time-domain Maxwell's equations using advanced FDTD (Finite-Difference Time-Domain) methodologies on a staggered Yee grid.

## Technical Deep-Dive

It employs perfectly matched layers (PML) to absorb outgoing waves at grid boundaries, eliminating unphysical reflections. It explicitly updates E and H fields in a leapfrog temporal scheme, governed by the Courant stability condition. Sub-pixel smoothing is used for resolving material interfaces.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| grid | Grid3D | Spatial discretization |
| time_steps | int | Integration iterations |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| total_energy_e | float | Integrated E-field energy |

### State Schema
Tracks `current_step` and `active_sources`.

## Dependencies
### Upstream (depends on)
- None

### Downstream (feeds into)
- H11-OPTICA
- H11-PARTICULA

## Failure Modes
- CFL condition violation (numerical explosion)
- Grid dispersion errors at high frequencies

## Performance Characteristics
Highly parallelizable; requires extreme memory bandwidth.

## Research References
- Yee, K. (1966). Numerical solution of initial boundary value problems involving Maxwell's equations in isotropic media.
- Taflove, A. (1995). Computational Electrodynamics: The Finite-Difference Time-Domain Method.

## Implementation Notes
Use CUDA/OpenCL for 3D grid updates.
