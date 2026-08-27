> **Layer 25** · Energy & Resources · `H11-HYDROPOWER`

## Purpose

The H11-HYDROPOWER agent manages the dispatch and modeling of hydroelectric dam systems, pumped-storage hydropower (PSH), and wave energy converters. It balances water reservoir levels, downstream ecological flow constraints, and electricity market prices.

## Technical Deep-Dive

HYDROPOWER utilizes multi-objective dynamic programming to solve the unit commitment problem for cascades of hydro generators. It models the non-linear relationship between net head, flow rate, and turbine efficiency using Hill Charts. 

For wave energy arrays, it simulates hydrodynamic interactions using Boundary Element Methods (BEM) to calculate radiation and diffraction forces, optimizing the power take-off (PTO) damping in real-time to achieve resonance with incoming wave spectra.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| inflow_rate | float | Catchment inflow rate (m^3/s) |
| market_price | float | Current electricity price ($/MWh) |
| grid_demand | float | Required power dispatch (MW) |
| wave_spectrum | Dict[str, float] | Wave significant height and peak period |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| dispatched_power | float | Actual power generated (MW) |
| reservoir_level | float | Updated reservoir elevation (m) |
| spillway_flow | float | Flow bypassed without generation (m^3/s) |
| pto_damping | float | Optimal PTO damping for wave array |

### State Schema
- `current_head_m`: float
- `reservoir_volume_m3`: float
- `turbine_states`: List[bool]

## Dependencies

### Upstream
- H11-METEO (precipitation)
- H11-GRID (market signals)

### Downstream
- H11-GRID (power delivery)

## Failure Modes
- Penstock water hammer modeling failures
- Violation of downstream minimum environmental flow

## Performance Characteristics
- Latency: <200ms for cascade optimization
- Large memory footprint for hydrodynamic BEM matrices

## Research References
- "Short-term scheduling of cascaded hydroelectric systems"
- "Real-time control of wave energy converters"
