> **Layer 24** · Agriculture & Food Sciences · `H11-IRRIGATIO`

## Purpose

The H11-IRRIGATIO agent manages agricultural water resources, calculating crop evapotranspiration (ETc) and soil moisture deficits to schedule precision irrigation. It minimizes water waste, prevents deep percolation (nutrient leaching), and ensures water is applied matching the temporal absorption curves of root systems.

## Technical Deep-Dive

It implements the FAO-56 dual crop coefficient approach, calculating reference evapotranspiration (ETo) via the ASCE Standardized Penman-Monteith equation, and applying basal crop (Kcb) and soil evaporation (Ke) coefficients. The agent runs a 1D Richards' equation solver for unsaturated flow in porous media to track moisture movement through the soil profile, predicting the matric potential at the root zone. 

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| weather | WeatherMetrics | Wind, solar rad, temp, RH |
| soil_moisture | List[SensorNode] | VWC readings at multiple depths |
| crop_coefficient | Float | Current Kc value |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| irrigation_schedule | List[ValveCommand] | Valve ID, start time, duration |
| estimated_et | Float | Calculated daily ETc in mm |
| leaching_fraction | Float | Estimated water lost below root zone |

### State Schema
Tracks the soil water balance (SWB) for multiple field management zones, including readily available water (RAW) and total available water (TAW).

## Dependencies

### Upstream (depends on)
- H11-SOILSCI (Soil texture, field capacity, wilting point)
- H11-CROP (Current crop growth stage to derive Kc)

### Downstream (feeds into)
- H11-PRECISIONAG (Spatial mapping of water stress)

## Failure Modes
1. Sensor drift in TDR (Time-Domain Reflectometry) sensors leading to over-irrigation.
2. Failure to account for localized rainfall runoff, causing saturation/anoxia.
3. Hydraulic lock in pipes due to aggressive valve scheduling algorithms.

## Performance Characteristics
Uses sparse matrices for the numerical integration of soil moisture gradients. Requires moderate memory to store spatio-temporal soil moisture histories.

## Research References
- Allen, R. G., et al. (1998). "Crop evapotranspiration-Guidelines for computing crop water requirements-FAO Irrigation and drainage paper 56."
- Simunek, J., et al. (2008). "The HYDRUS-1D software package for simulating the one-dimensional movement of water, heat, and multiple solutes in variably-saturated media."

## Implementation Notes
Pay attention to the hysteresis effect in soil water retention curves (van Genuchten parameters) for highly structured clay soils.
