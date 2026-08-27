> **Layer 16** · Transportation & Mobility · `H11-SPACEFLIGHT`

## Purpose
H11-SPACEFLIGHT models orbital mechanics, launch vehicle staging, and spacecraft attitude control. It provides the computational framework for calculating delta-v, Hohmann transfers, and staging optimizations.

## Technical Deep-Dive
The agent utilizes patched conics for interplanetary trajectories and Cowell's method (direct numerical integration) with J2 perturbations for Low Earth Orbit (LEO). Attitude is managed via reaction wheels and RCS (Reaction Control System) modeled with quaternions. The launch ascent utilizes an open-loop pitch program transitioning to a closed-loop gravity turn.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| engine_throttle | float | Main engine throttle |
| rcs_commands | Vector3 | Torques from RCS |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| orbit_elements | Keplerian | a, e, i, Omega, omega, nu |
| telemetry | SpaceState | Altitude, velocity, fuel mass |

### State Schema
- `orbital_state`: 6D Cartesian ECI state vector
- `stage_mass`: Propellant remaining per stage
- `thermal_state`: Heat shield and radiator temps

## Dependencies
### Downstream
- Global logistics (for orbital deployment routing)

## Failure Modes
- Max-Q structural failure
- Kessler syndrome (orbital collision)

## Research References
- Bate, R. R., Mueller, D. D., & White, J. E. (1971). Fundamentals of Astrodynamics.
- Curtis, H. (2013). Orbital Mechanics for Engineering Students.
