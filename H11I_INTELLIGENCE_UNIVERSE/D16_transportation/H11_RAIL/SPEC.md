> **Layer 16** · Transportation & Mobility · `H11-RAIL`

## Purpose
H11-RAIL manages the physics of rail locomotion (wheel-rail adhesion, traction motors) and network-level scheduling (signaling, block control, ERTMS). It is responsible for safe, optimized routing of freight and passenger trains across complex track topologies.

## Technical Deep-Dive
The agent models Polach adhesion for the contact patch, dealing with slip/slide at the rail interface. At the macro level, it uses moving-block signaling algorithms (CBTC) to maintain safe separation while maximizing throughput. Traction models cover Diesel-Electric and Catenary/Pantograph AC locomotives.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| locomotive_cmd | NotchCommand | Throttle notch, dynamic braking |
| track_conditions | TrackState | Grade, curvature, adhesion |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| train_kinematics | TrainState | Velocity, drawbar forces |
| signaling | BlockStatus | Movement authority, speed limits |

### State Schema
- `train_consist`: Number of cars, weight distribution
- `network_graph`: Directed graph of tracks and signals
- `pantograph_voltage`: Current drawn from catenary

## Dependencies
### Upstream
- H11-LOGISTICA (consist weight manifests)

## Failure Modes
- Derailment due to overspeed on curves
- Knuckle break from extreme drawbar forces

## Research References
- Iwnicki, S. (2006). Handbook of Railway Vehicle Dynamics.
- Pachl, J. (2014). Railway Timetable & Traffic.
