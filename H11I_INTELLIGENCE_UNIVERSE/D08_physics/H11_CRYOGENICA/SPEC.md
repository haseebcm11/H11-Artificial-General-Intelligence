> **Layer 8** · Physics · `H11-CRYOGENICA`

## Purpose

The H11-CRYOGENICA agent handles thermodynamics near absolute zero, simulating the anomalous properties of quantum fluids, specifically Liquid Helium-4 and Helium-3, and evaluating cooling strategies.

## Technical Deep-Dive

It calculates Kapitza boundary resistances which dominate thermal transport at milliKelvin temperatures. It implements Landau's two-fluid model for superfluid hydrodynamics, calculating the dispersion of first, second, and third sounds. For cooling, it models the thermodynamics of He3-He4 dilution refrigerators relying on the enthalpy of mixing.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| coolant | CoolantType | Cryogenic fluid |
| heat_load_watts | float | Parasitic heat |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| superfluid_fraction | float | $\rho_s / \rho$ |

### State Schema
Tracks `current_temp` and `mixture_phase_separated`.

## Dependencies
### Upstream (depends on)
- H11-THERMODYNAMICA

### Downstream (feeds into)
- H11-CONDENSATA (cooling for quantum materials)

## Failure Modes
- Enthalpy mismatch leading to failed dilution cooling
- Quench events exceeding available cooling power

## Performance Characteristics
Low computational overhead; primarily algebraic and ODE based.

## Research References
- Pobell, F. (2007). Matter and Methods at Low Temperatures.
- Landau, L. D. (1941). Theory of the Superfluidity of Helium II.

## Implementation Notes
Implement specific heat scaling ($T^3$ for phonons, $T$ for electrons) strictly below 1K.
