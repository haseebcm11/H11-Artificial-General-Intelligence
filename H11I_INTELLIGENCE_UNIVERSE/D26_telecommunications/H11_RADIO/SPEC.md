> **Layer 2** · Telecommunications · `H11-RADIO`

## Purpose

The H11-RADIO agent models and simulates terrestrial broadcasting, covering AM/FM, DAB, and other large-scale broadcast radio transmission techniques. Its main responsibility within the substrate is mapping terrain-aware propagation loss and designing efficient broadcast coverage areas.

## Technical Deep-Dive

H11-RADIO relies heavily on the Longley-Rice (ITM) propagation model to predict attenuation of radio signals for point-to-point and point-to-area communication paths. It evaluates diffraction over obstacles, tropospheric scatter, and surface reflection.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| transmitter_power_w | float | Transmission power in Watts |
| frequency_hz | float | Transmission frequency |
| antenna_height_m | float | Height of antenna |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| coverage_area_sq_km | float | Estimated effective broadcast range |
| shadow_zones | List[Dict] | Areas with signal degradation |

### State Schema
Maintains a spatial map of current radio transmitters and their overlapping interference boundaries.

## Dependencies
- Upstream: H11-SPECTRUM
- Downstream: None

## Failure Modes
- Severe weather causing unforeseen signal attenuation
- High interference from unmapped topography

## Performance Characteristics
Compute intensive for large area coverage mapping.

## Research References
- Longley-Rice Irregular Terrain Model

## Implementation Notes
Focus on optimizing the diffraction calculations over complex DEMs.
