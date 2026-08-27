> **Layer 25** · Energy & Resources · `H11-SOLARIS`

## Purpose

The H11-SOLARIS agent provides high-fidelity simulation and optimization of solar photovoltaic (PV) generation systems. It is designed to model multi-junction cell efficiencies, track maximum power points under varying irradiance conditions, and estimate overall plant yield.

## Technical Deep-Dive

SOLARIS uses advanced Equivalent Circuit Models (ECM), specifically the five-parameter diode model, to simulate the non-linear I-V characteristics of PV arrays. It incorporates spectral mismatch factors and temperature coefficients to accurately reflect real-world performance under diffuse and direct normal irradiance (DNI). 

The agent utilizes Perturb and Observe (P&O) and Incremental Conductance (IncCond) algorithms to simulate MPPT (Maximum Power Point Tracking). It dynamically adjusts the operating voltage to maximize the output power while accounting for partial shading effects which cause multiple local maxima on the P-V curve.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| irradiance_dni | float | Direct Normal Irradiance (W/m^2) |
| irradiance_dhi | float | Diffuse Horizontal Irradiance (W/m^2) |
| ambient_temp | float | Ambient temperature (Celsius) |
| shading_matrix | List[List[float]] | Partial shading matrix |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| power_output | float | Calculated power output (W) |
| efficiency | float | System efficiency |
| mppt_voltage | float | Optimal operating voltage |
| thermal_loss | float | Loss due to temperature elevation |

### State Schema
- `current_mppt_voltage`: float
- `array_temperature`: float
- `historical_yield`: float

## Dependencies

### Upstream
- H11-METEO (Weather forecasts)

### Downstream
- H11-BATTERIA (Storage)
- H11-GRID (Grid dispatch)

## Failure Modes
- Convergence failure in 5-parameter model solving
- Inaccurate shading resolution

## Performance Characteristics
- Latency: <50ms per iteration
- Real-time simulation of up to 10MW arrays

## Research References
- "Photovoltaic equivalent circuit parameter extraction" (2018)
- "Global MPPT for partially shaded PV systems"
