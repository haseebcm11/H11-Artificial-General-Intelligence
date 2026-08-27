> **Layer 15** · Architecture & Construction · `H11-WATERINFRA`

## Purpose
H11-WATERINFRA designs fluid transport systems: potable water distribution, sanitary sewers, and stormwater drainage networks. It models hydraulics and hydrology to ensure adequate pressure and flow without flooding.

## Technical Deep-Dive
Utilizes the Hardy Cross method and Newton-Raphson solvers for pressurized pipe network analysis (similar to EPANET). Applies the Kinematic Wave routing method and the Rational Method (Q=ciA) for stormwater surface runoff calculations.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| terrain | TIN | Base surface |
| demand_nodes| List[Node] | Water consumption points |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| pipe_network| Graph | Diameters and slopes |
| pressure_map| Grid | Residual pressure |
| flood_risk  | Polygon | Inundation zones |

### State Schema
- `system_head`: Float
- `max_velocity`: Float

## Dependencies
- **Upstream**: H11-LANDSCAPE
- **Downstream**: H11-BIM

## Failure Modes
- Negative pressure in potable lines (contamination risk)
- Surcharge in gravity sewers

## Implementation Notes
Solves massive systems of non-linear equations for hydraulic equilibrium.
