> **Layer 29** · Sports & Recreation · `H11-AQUATIC-SPORT`

## Purpose

H11-AQUATIC-SPORT models hydrodynamics, stroke biomechanics, and aquatic pacing for swimming, rowing, and water polo. 

Because aquatic sports involve moving through a medium 800 times denser than air, this agent focuses heavily on drag minimization (form drag, wave drag, skin friction) and propulsive efficiency (Froude efficiency) rather than just power generation.

## Technical Deep-Dive

AQUATIC-SPORT utilizes simplified Computational Fluid Dynamics (CFD) heuristics and the Active Drag System (MAD) models to estimate the drag coefficient (Cd) of a swimmer. 

It evaluates stroke length (SL) and stroke rate (SR) against the athlete's wingspan and buoyancy profile. The agent calculates the intra-stroke velocity fluctuations—a key indicator of inefficiency, as power required to overcome drag scales with the cube of velocity (V^3).

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `stroke_telemetry` | `List[StrokeCycle]` | Accelerometer/gyro data per stroke |
| `split_times` | `List[float]` | Lap times in seconds |
| `water_density` | `float` | Salinity/temperature adjusted density |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `propulsive_efficiency` | `float` | Percentage of power moving athlete forward |
| `active_drag_estimate` | `float` | Estimated drag in Newtons |
| `stroke_index` | `float` | V * SL metric for swimming economy |

### State Schema
Tracks historical stroke length/rate relationships to find the athlete's optimal intersection (the "sweet spot").

## Dependencies

### Upstream (depends on)
- H11-ATHLETICA (Kinematics)

### Downstream (feeds into)
- H11-COACHING (Stroke correction)

## Failure Modes
- **Sensor Damping:** Water interference causing dropped IMU packets.
- **Wave Drag Confounding:** Failing to account for wake interference from adjacent lanes.

## Performance Characteristics
Requires signal processing (Fast Fourier Transforms) to isolate stroke phases from noisy, damped aquatic sensor data.

## Research References
- Toussaint, H. M., & Beek, P. J. (1992). Biomechanics of competitive front crawl swimming.
- Zamparo, P., et al. (2020). The energetics of swimming.

## Implementation Notes
Include buoyancy corrections based on estimated body fat percentage and lung volume.
