> **Layer 8** · Physics · `H11-ACOUSTICA`

## Purpose

The H11-ACOUSTICA agent specializes in the simulation and analysis of mechanical wave propagation through fluid and solid media. It models room acoustics, psychoacoustics, noise control, and ultrasound phenomena for the H11 substrate.

## Technical Deep-Dive

ACOUSTICA solves the linear acoustic wave equation using finite difference time domain (FDTD) methods and boundary element methods (BEM) for complex geometries. It incorporates frequency-dependent absorption coefficients and Sabine's reverberation theory for macro-scale room acoustics.

For psychoacoustics, the agent applies equal-loudness contours (Fletcher-Munson) and critical band analysis to evaluate perceived loudness and masking effects. Helmholtz resonances are modeled via lumped parameter systems.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| geometry | Mesh | Enclosure geometry |
| sources | List[AudioSource] | Sound emitters |
| material_props| Dict | Absorption/reflection profiles |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| spl_field | Grid3D | Sound Pressure Level map |
| rt60 | float | Reverberation time |

### State Schema
Tracks acoustic pressure history for FDTD stepping.

## Dependencies

### Upstream (depends on)
H11-FLUIDA (for medium density and flow effects)

### Downstream (feeds into)
H11-BIOPHYSICA (for auditory system modeling)

## Failure Modes
- Courant–Friedrichs–Lewy (CFL) condition violations in FDTD
- Phantom resonances due to grid discretization

## Performance Characteristics
- High memory usage for 3D FDTD grids

## Research References
- Kinsler et al., Fundamentals of Acoustics
- Zwicker & Fastl, Psychoacoustics

## Implementation Notes
- Use perfectly matched layers (PML) for open boundaries.
