> **Layer 8** · Physics · `H11-OPTICA`

## Purpose

The H11-OPTICA agent specializes in the simulation and analysis of light behavior, encompassing geometric optics, wave optics, interference, diffraction, and non-linear photonics. It computes photon paths, ray-tracing, and wave front propagation across the intelligence universe.

## Technical Deep-Dive

OPTICA models light as both rays (via the Eikonal equation) and waves (via scalar diffraction theory). It employs split-step Fourier methods for non-linear Schrödinger equations describing pulse propagation in optical fibers. For geometric optics, it utilizes robust ray-tracing with recursive reflection and refraction based on Snell's law and Fresnel equations.

The agent handles polarization state vectors using Jones calculus and Mueller matrices, allowing for advanced simulations of waveplates and polarizers. It can compute the Point Spread Function (PSF) and Optical Transfer Function (OTF) for complex lens systems.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| light_sources | List[LightSource] | Sources of photons/waves |
| optical_elements | List[OpticalElement]| Lenses, mirrors, media |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| intensity_field | Grid2D | Intensity distribution |
| ray_paths | List[Path] | Traced ray paths |

### State Schema
Caches material refractive indices and spectral data.

## Dependencies

### Upstream (depends on)
H11-ELECTROMAGNETICA (for fundamental Maxwell equations)

### Downstream (feeds into)
H11-QUANTUMOPTICA (for macroscopic constraints)

## Failure Modes
- Ray trapping in total internal reflection loops
- Aliasing in high-frequency diffraction grids

## Performance Characteristics
- Highly parallelizable ray-tracing (GPU friendly)

## Research References
- Born & Wolf, Principles of Optics
- Goodman, Introduction to Fourier Optics

## Implementation Notes
- Use vectorization for Jones matrices.
