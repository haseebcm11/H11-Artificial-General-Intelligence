> **Layer 16** · Transportation & Mobility · `H11-AUTOMOBILIS`

## Purpose
H11-AUTOMOBILIS manages the fundamental physical models of wheeled ground vehicles. It models tire friction (Pacejka magic formula), suspension kinematics, chassis dynamics, and standard ICE (Internal Combustion Engine) powertrain behavior, providing a realistic simulation and control substrate for vehicles.

## Technical Deep-Dive
The agent utilizes multibody dynamics and specific empirical tire models to accurately simulate vehicle behavior under extreme conditions. It handles weight transfer, longitudinal and lateral slip, and aerodynamic drag coefficients. The ICE powertrain model includes torque mapping, gear ratios, and differential slip. 

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| vehicle_params | Dict | Mass, inertia, wheelbase, CG height |
| control_inputs | ControlState | Throttle, brake, steering angle |
| environment | EnvState | Friction coefficients, incline, wind |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| kinematic_state | KinematicState | Position, velocity, acceleration |
| dynamic_forces | ForceVector | Tire forces, drag, weight transfer |

### State Schema
- `chassis_state`: 6-DOF chassis position/orientation
- `wheel_states`: Angular velocity and slip for each wheel
- `engine_state`: RPM, temperature, torque output

## Dependencies
### Downstream (feeds into)
- H11-AUTONOMOUS (provides the plant model for control algorithms)

## Failure Modes
- Integration instability at high speeds
- Pacejka model singularity at zero velocity

## Research References
- Pacejka, H. B. (2012). Tire and Vehicle Dynamics.
- Gillespie, T. D. (1992). Fundamentals of Vehicle Dynamics.
