> **Layer 24** · Agriculture & Food Sciences · `H11-CROP`

## Purpose

The H11-CROP agent models and optimizes large-scale field crop production (agronomy), focusing on staple crops such as wheat, corn, soy, and rice. It simulates the phenological stages of crops under varying climatic and soil conditions to predict yield and optimize planting density, fertilizer application timing, and harvest windows.

## Technical Deep-Dive

H11-CROP utilizes a modified version of the CERES (Crop Environment Resource Synthesis) models and APSIM (Agricultural Production Systems sIMulator) frameworks. It implements state-machine-based phenological tracking where state transitions are governed by growing degree days (GDD) and photoperiod interactions. The agent evaluates photosynthetic efficiency through light interception models (Beer-Lambert law for canopy architecture) and carbon partitioning matrices to allocate biomass to roots, stems, leaves, and grain.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| field_data | FieldTopography | Area, coordinates, elevation |
| cultivar_params | CultivarPhenotype | Genetic coefficients for maturity |
| daily_weather | List[WeatherObservation] | T_max, T_min, solar radiation, precip |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| yield_forecast | BiomassEstimate | Grain and stover yield in kg/ha |
| growth_stage | PhenologicalStage | Current BBCH scale stage |
| limiting_factors | List[StressIndex] | Water, nitrogen, or temperature stress flags |

### State Schema
Maintains a localized crop canopy state, tracking accumulated GDD, leaf area index (LAI), root depth, and current soil moisture profile limits.

## Dependencies

### Upstream (depends on)
- H11-SOILSCI (Provides baseline soil fertility and bulk density)
- H11-IRRIGATIO (Provides water application data)

### Downstream (feeds into)
- H11-PRECISIONAG (Feeds yield forecasts for spatial analysis)

## Failure Modes
1. Canopy senescence desynchronization due to extreme heat spikes.
2. Underestimation of lodging risk during high-wind events at physiological maturity.
3. Vernalization requirement failure in winter crops due to mild winters.

## Performance Characteristics
High computational load for daily timestep simulations across heterogeneous field grids. Memory footprint scales with the spatial resolution of the field simulation grid.

## Research References
- Jones, J. W., et al. (2003). "The DSSAT cropping system model." European Journal of Agronomy.
- Holzworth, D. P., et al. (2014). "APSIM – Evolution towards a new generation of agricultural systems simulation." Environmental Modelling & Software.

## Implementation Notes
Implement vectorization for spatial grids to avoid looping over thousands of field zones when computing daily GDD and LAI updates.
