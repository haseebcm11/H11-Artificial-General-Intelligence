> **Layer 25** · Energy & Resources · `H11-GEOTHERMALIS`

## Purpose

The H11-GEOTHERMALIS agent models and optimizes Enhanced Geothermal Systems (EGS) and traditional hydrothermal reservoirs. It monitors subsurface thermodynamic flows, manages injection/production well balances to prevent thermal drawdown, and optimizes the Organic Rankine Cycle (ORC) power plant efficiency.

## Technical Deep-Dive

GEOTHERMALIS utilizes TOUGH2-compliant multiphase fluid and heat flow algorithms to model fracture networks in the crystalline basement. It tracks pressure-enthalpy (P-h) dynamics to avoid unwanted phase changes (flashing) inside the reservoir which can cause mineral scaling.

The agent actively controls injection pumps to maintain reservoir pressure while minimizing induced seismicity. It calculates the optimal working fluid mass flow rate in the ORC based on real-time brine temperature and ambient condensing temperatures, applying exergy analysis to minimize thermodynamic destruction in the heat exchangers.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| production_temp | float | Wellhead brine temperature (Celsius) |
| production_pressure | float | Wellhead pressure (bar) |
| ambient_temp | float | Condenser ambient temperature (Celsius) |
| seismic_events | List[Dict] | Microseismic event data |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| injection_rate | float | Recommended injection flow rate (kg/s) |
| orc_power | float | Electrical power output (MW) |
| scaling_risk | float | Probability of mineral scaling (0-1) |
| thermal_drawdown | float | Estimated reservoir depletion rate |

### State Schema
- `reservoir_pressure_bar`: float
- `exergy_efficiency`: float
- `induced_seismicity_index`: float

## Dependencies

### Upstream
- H11-METEO (ambient temp for ORC)

### Downstream
- H11-GRID

## Failure Modes
- Thermal breakthrough (cold injection fluid reaching production well too fast)
- Exceeding induced seismicity thresholds
- Silica scaling in heat exchangers

## Performance Characteristics
- Latency: <500ms for reservoir P-T state updates
- Requires long-horizon predictive modeling (years)

## Research References
- "Multiphase flow in fractured porous media"
- "Exergy optimization of Organic Rankine Cycles in EGS"
