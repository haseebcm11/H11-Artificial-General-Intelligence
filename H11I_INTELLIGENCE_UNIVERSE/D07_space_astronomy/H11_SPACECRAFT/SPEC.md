> **Layer 7** · Space & Astronomy · `H11-SPACECRAFT`

## Purpose

The H11-SPACECRAFT agent operates as the overarching systems engineer and flight controller for autonomous vehicles within the H11 substrate. It is responsible for the holistic management of spacecraft subsystems, including Attitude Determination and Control (ADCS), Electrical Power Systems (EPS), Thermal Control (TCS), and Command and Data Handling (C&DH).

Unlike Orbitalis which tells the spacecraft *where* to go, and Propulsio which models *how* the engine fires, H11-SPACECRAFT ensures the vehicle survives the environment, maintains pointing requirements, and manages power budgets throughout the mission lifecycle.

## Technical Deep-Dive

H11-SPACECRAFT implements Multi-Variable Control (MVC) for coupled rotational dynamics, using reaction wheels, control moment gyroscopes (CMGs), and magnetorquers. It calculates the inertia tensor in real-time as propellant is consumed, continuously updating the control laws (e.g., LQR or PID variants) to maintain pointing accuracy for optical communication or science instruments.

For thermal control, it solves finite-element thermal networks using Stefan-Boltzmann radiation exchanges to manage active (fluid loops, heaters) and passive (MLI, radiators) components, preventing both freezing of propellants and overheating of sensitive electronics.

The EPS module runs power flow simulations, tracking solar array degradation from radiation, battery state-of-charge (SoC) using extended Kalman filters, and depth-of-discharge (DoD) limits during eclipse periods.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `environment` | `SpaceEnvironment` | Solar flux, albedo, Earth IR, eclipse state |
| `mission_mode` | `FlightMode` | E.g., Sun-pointing, Target-tracking, Safe-mode |
| `sensor_telemetry` | `ADCS_Sensors` | Star tracker, sun sensor, IMU data |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `actuator_commands` | `ADCS_Actuators` | Reaction wheel torques, thruster pulses |
| `thermal_state` | `ThermalNetwork` | Temperatures of critical nodes |
| `power_budget` | `PowerState` | Solar generation, load consumption, battery SoC |

### State Schema
- `inertia_tensor`: 3x3 matrix representing current mass distribution.
- `momentum_envelope`: Current angular momentum stored in reaction wheels.
- `component_health`: Degradation factors for solar panels, batteries, and gyros.

## Dependencies

### Upstream (depends on)
- `H11-ORBITALIS`: Provides position vector required for eclipse and pointing calculations.
- `H11-HELIOPHYSICA`: Provides solar radiation and single-event upset (SEU) probabilities.
- `H11-PROPULSIO`: Provides mass flow data to update the inertia tensor.

### Downstream (feeds into)
- `H11-SATELLITIS`: Provides bus telemetry to coordinate constellation-level actions.

## Failure Modes
- `MomentumSaturation`: Reaction wheels spin at maximum speed and can no longer provide torque in a specific axis.
- `ThermalRunaway`: Inability to radiate excess heat, causing sequential electronic failures.
- `LossOfLock`: Star trackers blinded by the sun or radiation, resulting in unknown attitude.

## Performance Characteristics
- Hard real-time constraints for ADCS control loops (e.g., 10-100 Hz).
- Strict memory bounds, mirroring typical flight software limits (e.g., cFE/cFS architecture).

## Research References
- Wertz, J. R. (1978). Spacecraft Attitude Determination and Control.
- NASA Core Flight System (cFS) architecture standards.
- Gilmore, D. G. (2002). Spacecraft Thermal Control Handbook.

## Implementation Notes
Quaternions must be used universally for attitude representation to avoid gimbal lock. Ensure mass property updates strictly conserve momentum during internal shifting.
