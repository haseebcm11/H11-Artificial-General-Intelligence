> **Layer 7** · Space & Astronomy · `H11-MARTIALIS`

## Purpose

The H11-MARTIALIS agent manages missions, surface operations, and atmospheric flight specific to the Martian environment. It handles the unique challenges of Entry, Descent, and Landing (EDL) in a thin atmosphere, aerocapture maneuvers, and the command of surface assets like rovers and coaxial helicopters (e.g., Ingenuity).

This agent provides the specialized aerodynamics and geology modeling required for Mars, distinguishing itself from Lunar operations by factoring in atmospheric drag, supersonic parachute deployment, and global dust storm climatology.

## Technical Deep-Dive

H11-MARTIALIS models the Martian atmosphere using variations of the Mars Global Reference Atmospheric Model (Mars-GRAM), predicting density variations crucial for the hypersonic aerothermodynamics of EDL. It computes the "7 minutes of terror" trajectory, integrating hypersonic lifting-body aerodynamics, supersonic retro-propulsion, and sky-crane winch dynamics.

For surface operations, the agent employs visual odometry and SLAM (Simultaneous Localization and Mapping) optimized for the feature-poor, repetitive Martian terrain. It manages the energy budget of solar-powered assets by predicting the Optical Depth ($\tau$) of the atmosphere, forecasting dust storms that can rapidly degrade power generation.

The agent also calculates flight envelopes for Martian rotorcraft, solving the Navier-Stokes equations for low-Reynolds-number compressible flow (due to the low density and low speed of sound in CO2).

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `atmospheric_data` | `MarsAtmosphere` | Dust opacity, density profile, wind vectors |
| `vehicle_state` | `EDLState` | Hypersonic velocity, heat shield temps |
| `surface_imagery` | `NavCamImages` | Stereo imagery for SLAM and driving |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `edl_triggers` | `EDLSequence` | Timing for parachute deploy, heat shield jettison |
| `rover_path` | `MarsTraverse` | Safe path avoiding sand traps (ripple dunes) |
| `rotorcraft_flight` | `FlightPlan` | Waypoints and rotor RPM commands |

### State Schema
- `current_ls`: Solar longitude ($L_s$), tracking the Martian season.
- `dust_optical_depth`: Current atmospheric opacity ($\tau$).
- `comm_relay_window`: Next available time slot for passing data to orbiters (e.g., MRO).

## Dependencies

### Upstream (depends on)
- `H11-PLANETOLOGIA`: Provides the base areological (Martian geological) models.
- `H11-ORBITALIS`: Provides interplanetary approach vectors.

### Downstream (feeds into)
- `H11-SPACECRAFT`: Receives the raw actuator commands for the aeroshell or rover chassis.

## Failure Modes
- `ParachuteTear`: Deployment at too high a dynamic pressure ($q$) causing structural failure.
- `SandTrap`: Driving into a ripple dune with high slip, permanently embedding the rover wheels.
- `CommBlackout`: Failing to uplink the daily command sequence before the orbiter sets below the horizon, wasting a Sol (Martian day).

## Performance Characteristics
- Highly autonomous: light-travel time (up to 22 minutes one-way) strictly prohibits real-time joystick control.
- Computational constraints: forced to use radiation-hardened, low-clock-speed processors (e.g., RAD750) for critical EDL phases.

## Research References
- Braun, R. D., & Manning, R. M. (2006). Mars exploration entry, descent, and landing challenges.
- Balaram, J., et al. (2018). Mars Helicopter Technology Demonstrator.
- Mars Global Reference Atmospheric Model (Mars-GRAM).

## Implementation Notes
Include specific handling for the Martian speed of sound (approx. 240 m/s), which causes rotor tips to reach critical Mach numbers much earlier than on Earth.
