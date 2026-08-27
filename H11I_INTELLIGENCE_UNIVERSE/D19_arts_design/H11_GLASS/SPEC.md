> **Layer 19** · Arts, Design & Creativity · `H11-GLASS`

## Purpose
Simulates the fluid dynamics of molten glass and the optical caustics of the cooled solid.

## Technical Deep-Dive
Applies bi-directional path tracing (BDPT) to accurately render internal light scattering and chromatic dispersion based on the Abbe number.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| design_spec | Dict | Parameters |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| caustic_map | bytes | Texture |

### State Schema
- `temperature_c`: Float.

## Dependencies
- Upstream: Raytracer

## Failure Modes
- Internal stress fracture.

## Implementation Notes
GPU required for volumetric photon mapping.
