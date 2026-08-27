> **Layer 16** · Transportation & Mobility · `H11-AVIATIO`

## Purpose
H11-AVIATIO manages the 6-DOF (Degrees of Freedom) flight dynamics of fixed-wing and rotary-wing aircraft. It implements aerodynamic coefficient mappings, propulsion (turbofan, turboprop, piston), and environmental atmospherics (ISA models, wind shear). 

## Technical Deep-Dive
The agent employs blade element momentum theory for rotors and lifting-line theory approximations for fixed wings. Flight dynamics are integrated using quaternion-based kinematics to avoid gimbal lock. The autopilot substrate handles PID cascades for altitude, heading, and attitude hold.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| flight_controls | FlightControls | Aileron, elevator, rudder, throttle |
| atmosphere | AtmosState | Density, pressure, temperature, wind |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| aero_forces | Wrench | Lift, drag, side force, moments |
| flight_state | FlightState | Airspeed, mach, altitude, attitude |

### State Schema
- `quaternion`: Aircraft orientation in 3D space
- `engine_states`: N1, N2 RPM, EGT, fuel flow
- `cg_location`: Center of gravity offset based on fuel burn

## Dependencies
### Upstream
- Atmosphere weather services

## Failure Modes
- Stall/Spin dynamics
- Compressor stall in turbofans

## Research References
- Stevens, B. L., & Lewis, F. L. (2015). Aircraft Control and Simulation.
- Nelson, R. C. (1998). Flight Stability and Automatic Control.
