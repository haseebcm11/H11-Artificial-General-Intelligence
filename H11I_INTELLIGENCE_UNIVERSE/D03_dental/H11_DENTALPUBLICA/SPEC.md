> **Layer 3** · Dental Sciences · `H11-DENTALPUBLICA`

## Purpose
H11-DENTALPUBLICA scales oral health analysis from the individual patient to the population level. It focuses on epidemiology, health policy, community water fluoridation optimization, and oral health disparity tracking.

Unlike clinical agents, this agent processes large-scale demographic datasets to formulate community interventions. It simulates the impact of sugar taxes, school-based sealant programs, and Medicaid dental coverage expansions on population-level DMFT (Decayed, Missing, Filled Teeth) scores.

## Technical Deep-Dive
The agent utilizes epidemiological modeling (compartmental models adapted for non-communicable diseases) to track caries and periodontitis prevalence across socio-economic strata. It calculates optimal fluoride concentration in municipal water supplies factoring in ambient climate temperature (which affects daily water consumption) to achieve maximum caries reduction with minimal fluorosis risk (typically ~0.7 ppm).

It employs geospatial mapping (GIS) to identify "dental deserts"—regions lacking sufficient access to dental professionals. Cost-benefit analysis algorithms are used to evaluate the economic return on investment (ROI) for preventive community programs, calculating Disability-Adjusted Life Years (DALYs) saved through early intervention.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| population_data | DemographicSet | Age, income, location matrices |
| water_supply | WaterSystem | Current fluoride ppm, climate data |
| survey_results | List[DMFTScore] | Sampled epidemiological data |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| fluoridation_target | float | Recommended ppm adjustment |
| intervention_roi | Dict[str, float] | Cost-benefit of various policies |
| disparity_map | GeospatialGrid | Highlighted high-risk populations |

### State Schema
Maintains a `PopulationHealthState` tracking longitudinal DMFT averages, Medicaid utilization rates, and active community programs per region.

## Dependencies

### Upstream
- H11-DENTALIS: Anonymized, aggregated charting data to feed epidemiological models.

### Downstream
- H11-POLICY (Hypothetical upper-layer agent): Provides data for state/federal healthcare policy generation.

## Failure Modes
1. **Ecological Fallacy:** Incorrectly applying population-level averages to predict individual outcomes in localized high-risk pockets.
2. **Fluorosis Spikes:** Over-fluoridation recommendation due to faulty climate/consumption assumptions.
3. **Sampling Bias:** Underestimating caries prevalence because marginalized populations are under-represented in survey data.

## Performance Characteristics
Processes large batch datasets asynchronously. Heavy use of statistical and econometric modeling libraries.

## Research References
- Centers for Disease Control and Prevention (CDC). (2001). Recommendations for using fluoride to prevent and control dental caries in the United States.
- Petersen, P. E. (2003). The World Oral Health Report 2003.

## Implementation Notes
Implement a stochastic simulation engine to forecast the 10-year impact of a proposed school sealant program on the Medicaid budget.
