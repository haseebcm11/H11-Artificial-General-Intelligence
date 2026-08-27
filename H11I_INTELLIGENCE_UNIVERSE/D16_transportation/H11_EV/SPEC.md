> **Layer 16** · Transportation & Mobility · `H11-EV`

## Purpose
H11-EV specializes in the complex interplay of high-voltage battery management systems (BMS), inverter dynamics, and electric motor (PMSM, AC Induction) vector control. It manages thermal limits, state of charge (SoC), state of health (SoH), and regenerative braking optimization.

## Technical Deep-Dive
The agent utilizes Field Oriented Control (FOC) algorithms for precise torque delivery, managing the d-q axis currents. The battery model includes equivalent circuit models (ECM) with RC pairs to track polarization and thermal degradation over time. Regenerative blending algorithms seamlessly transition between friction and electromagnetic braking.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| torque_demand | float | Desired torque output |
| battery_temp | float | Cell temperature |
| grid_voltage | float | For charging contexts |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| phase_currents | Vector3 | 3-phase AC currents to motor |
| soc_estimate | float | Battery State of Charge |

### State Schema
- `bms_state`: Voltage, current, temperature per cell
- `motor_state`: Rotor angle, flux linkage, rpm

## Dependencies
### Upstream
- H11-AUTOMOBILIS (shares chassis chassis state)

## Failure Modes
- Thermal runaway in cell modules
- Inverter IGBT failure

## Research References
- Plett, G. L. (2015). Battery Management Systems.
