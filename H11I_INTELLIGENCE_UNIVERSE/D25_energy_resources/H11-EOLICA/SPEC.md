> **Layer 25** · Energy & Resources · `H11-EOLICA`

## Purpose

The H11-EOLICA agent simulates and optimizes wind turbine performance and farm layout aerodynamics. It addresses turbine wake effects, yaw misalignment, and blade pitch control to maximize aerodynamic efficiency and structural lifespan under turbulent wind conditions.

## Technical Deep-Dive

EOLICA models wind power generation using the Jensen wake model and more advanced Gaussian wake models for deep array effects. It processes multi-dimensional wind resource data (speed, direction, turbulence intensity) to compute the thrust coefficient and power coefficient for each turbine.

For control optimization, EOLICA implements Active Wake Control (AWC) by intentionally yawing upwind turbines to steer their wakes away from downwind turbines. This cooperative control strategy increases the overall wind farm power production despite slightly reducing the efficiency of the upwind turbines.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| wind_speed | float | Hub-height wind speed (m/s) |
| wind_direction | float | Wind direction (degrees) |
| turbulence_intensity | float | Turbulence intensity (%) |
| yaw_angles | List[float] | Current yaw angle per turbine |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| farm_power | float | Total farm active power (MW) |
| optimal_yaws | List[float] | Recommended yaw angles |
| wake_losses | float | Wake loss percentage |
| fatigue_loads | List[float] | Estimated structural fatigue loads |

### State Schema
- `rotor_speeds`: List[float]
- `blade_pitches`: List[float]
- `cumulative_fatigue`: List[float]

## Dependencies

### Upstream
- H11-METEO

### Downstream
- H11-GRID

## Failure Modes
- Wake model divergence in extreme turbulence
- Actuator limits exceeded in yaw commands

## Performance Characteristics
- Latency: <100ms for 50-turbine farm wake computation
- Parallel evaluation of yaw combinations

## Research References
- "Cooperative active wake control for wind farms"
- "Gaussian wake model for offshore wind farms"
