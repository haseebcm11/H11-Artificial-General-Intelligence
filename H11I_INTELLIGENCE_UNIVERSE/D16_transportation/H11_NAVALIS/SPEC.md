> **Layer 16** · Transportation & Mobility · `H11-NAVALIS`

## Purpose
H11-NAVALIS simulates the hydrodynamic forces acting on marine vessels. It models buoyancy, hull drag, wave resistance, added mass, and propeller cavitation. It provides the foundation for routing algorithms, ship autopilots, and maritime logistics.

## Technical Deep-Dive
The agent employs strip theory for seakeeping and Froude scaling for wave making resistance. It models 6-DOF vessel motions (surge, sway, heave, roll, pitch, yaw) coupled with sea state spectrums (Pierson-Moskowitz or JONSWAP). Thruster models use wake fraction and thrust deduction factors for realistic propulsion.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| helm_commands | HelmState | Engine telegraph, rudder angle |
| sea_state | SeaState | Wave height, period, current vector |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| vessel_pose | Pose6D | Position and orientation |
| hydro_forces | HydroForces | Froude, Reynolds, and wave forces |

### State Schema
- `hull_state`: Draft, trim, list angles
- `engine_telegraph`: RPM setpoint vs actual
- `fuel_mass`: Consumable mass affecting draft

## Dependencies
### Upstream
- H11-LOGISTICA (cargo loading affects CG and draft)

## Failure Modes
- Parametric rolling resonance
- Loss of dynamic stability / capsizing

## Research References
- Faltinsen, O. M. (1990). Sea Loads on Ships and Offshore Structures.
- Newman, J. N. (2018). Marine Hydrodynamics.
