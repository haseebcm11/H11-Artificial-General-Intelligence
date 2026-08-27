> **Layer 24** · Agriculture & Food Sciences · `H11-HORTICULTURA`

## Purpose

The H11-HORTICULTURA agent manages high-value specialty crops, including fruits, vegetables, ornamentals, and greenhouse/controlled-environment agriculture (CEA). It optimizes microclimate controls (HVAC, supplemental lighting, CO2 enrichment) and monitors delicate physiological traits like fruit set, ripening indices, and cosmetic quality, which are critical for horticultural products.

## Technical Deep-Dive

This agent models the thermodynamics of greenhouse environments using sensible and latent heat balance equations. It integrates photosynthetic photon flux density (PPFD) metrics for Daily Light Integral (DLI) optimization. For fruiting crops, it models source-sink dynamics (carbohydrate partitioning) to predict fruit caliber and Brix (sugar content). The agent controls hydroponic nutrient dosing algorithms (EC/pH targets) based on crop transpiration rates derived from the Penman-Monteith equation modified for indoor canopies.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| indoor_climate | MicroclimateReadings | Temp, RH, CO2, PAR light |
| nutrient_solution | HydroponicState | pH, EC, ion concentrations |
| crop_type | HortiCropFamily | E.g., Solanaceae, Rosaceae |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| climate_setpoints | HVACCommands | Target temp, shade curtain, lights |
| fertigation_plan | DosingInstruction | Nutrient A/B pump ratios |
| harvest_readiness | QualityMetrics | Brix, firmness, color index |

### State Schema
Tracks the cumulative DLI, vapor pressure deficit (VPD) stress integrals, and current phenological load (number of active fruit trusses).

## Dependencies

### Upstream (depends on)
- H11-PRECISIONAG (for computer vision inputs of fruit color)
- H11-IRRIGATIO (for raw water quality constraints)

### Downstream (feeds into)
- H11-FOODTECH (for post-harvest processing parameters)

## Failure Modes
1. Blossom End Rot (BER) induction due to undetected localized VPD spikes causing calcium transport failure.
2. Runaway humidity leading to dew point crossing and Botrytis cinerea outbreak.
3. Phototoxicity from excessive supplemental LED lighting at wrong spectrum.

## Performance Characteristics
High frequency (sub-minute) control loops required for greenhouse climate state management. Uses lightweight PID control algorithms mixed with model predictive control (MPC).

## Research References
- Marcelis, L. F. M., et al. (1998). "Modelling biomass production and yield of horticultural crops: a review." Scientia Horticulturae.
- Albright, L. D., et al. (2000). "Controlling greenhouse light to a consistent daily integral." Transactions of the ASAE.

## Implementation Notes
Implement strict bounded optimizations for VPD; calculate saturated vapor pressure accurately using the Arden Buck equation.
