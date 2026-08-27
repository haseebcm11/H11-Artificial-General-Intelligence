> **Layer 7** · Space & Astronomy · `H11-PROPULSIO`

## Purpose

The H11-PROPULSIO agent is responsible for modeling, simulating, and optimizing spacecraft propulsion systems. It manages chemical, electric (ion, Hall-effect), and advanced (nuclear thermal, solar sail) propulsion mechanics.

This agent operates as the thermodynamic and fluid-dynamic authority within the substrate, calculating specific impulse ($I_{sp}$), thrust profiles, propellant mass fractions, and thermal management requirements for deep space and orbital maneuvers.

## Technical Deep-Dive

H11-PROPULSIO employs computational fluid dynamics (CFD) and thermodynamic equilibrium codes (like CEA - Chemical Equilibrium with Applications) to model combustion chamber processes and nozzle expansion in chemical rockets. It calculates ideal rocket equations, accounting for nozzle throat erosion and combustion instabilities (e.g., pogo oscillation).

For electric propulsion, the agent uses Particle-in-Cell (PIC) simulations coupled with Direct Simulation Monte Carlo (DSMC) to model plasma behavior, ionization efficiency, and grid erosion rates in ion thrusters.

The agent optimizes propellant feed systems by modeling the thermodynamics of cryogenic boil-off, pressurant gas (helium) thermodynamics, and the effects of microgravity on fluid slosh and acquisition.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `propellant_type` | `PropellantMixture` | e.g., LOX/RP-1, Xenon, Hydrazine |
| `engine_geometry` | `NozzleParams` | Expansion ratio, throat area |
| `burn_requirements` | `ThrustProfile` | Required Delta-V, duration, and throttle |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `performance_metrics` | `PropulsionMetrics` | Isp, Thrust, Mass flow rate |
| `thermal_loads` | `ThermalProfile` | Heat flux to chamber walls and nozzle |
| `propellant_budget` | `MassFraction` | Propellant consumed and residual margin |

### State Schema
- `engine_wear_model`: Degradation tracking of engine components (e.g., ablative cooling loss).
- `tank_thermodynamics`: State of cryogenic propellants (temperature, pressure).
- `plasma_grid_status`: Erosion state of electric thruster grids.

## Dependencies

### Upstream (depends on)
- `H11-ORBITALIS`: Provides the required Delta-V maneuvers that the propulsion system must execute.

### Downstream (feeds into)
- `H11-SPACECRAFT`: Integrates the propulsion data into the overall vehicle mass and power budgets.
- `H11-DEEPSPACE`: Dictates the feasibility of long-duration interstellar or outer-planet trajectories based on advanced propulsion limits.

## Failure Modes
- `CombustionInstability`: High-frequency acoustic oscillations destroying the combustion chamber.
- `CryogenicBoilOff`: Excessive loss of propellant due to inadequate thermal insulation in space.
- `GridShorting`: Failure of electric propulsion due to molybdenum grid erosion and short circuits.

## Performance Characteristics
- High computational requirements for real-time CFD during transient engine start-up simulations.
- Memory-intensive chemical kinetic databases for modeling exotic hypergolic propellants.

## Research References
- Sutton, G. P., & Biblarz, O. (2016). Rocket Propulsion Elements.
- Goebel, D. M., & Katz, I. (2008). Fundamentals of Electric Propulsion.
- NASA Chemical Equilibrium with Applications (CEA) code.

## Implementation Notes
Ensure rigorous handling of unit conversions (e.g., $I_{sp}$ in seconds vs. effective exhaust velocity). Plasma simulations must handle high Knudsen number flows accurately.
