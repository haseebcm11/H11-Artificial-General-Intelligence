> **Layer 24** · Agriculture & Food Sciences · `H11-AQUACULTURA`

## Purpose

The H11-AQUACULTURA agent manages closed (RAS - Recirculating Aquaculture Systems) and open (net pen, pond) aquaculture environments. It focuses on water chemistry homeostasis, optimizing stocking densities, managing biofilter performance, and minimizing feed conversion ratios for aquatic species.

## Technical Deep-Dive

Models the nitrogen cycle (ammonia -> nitrite -> nitrate) dynamics in biofilters using Monod kinetics for nitrifying bacteria (Nitrosomonas and Nitrobacter). It computes dissolved oxygen (DO) transfer efficiency based on temperature, salinity, and altitude. Feed rations are dynamically adjusted based on metabolic equations dependent on species, mass, and water temperature.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| water_quality | WaterMetrics | DO, pH, NH3, NO2, NO3, Temp |
| stock_data | BiomassInfo | Species, average mass, count |
| system_type | FarmType | RAS, POND, MARINE_PEN |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| feed_schedule | FeedCommand | Pellet size, weight per meal |
| aeration_cmd  | O2Command | Blower speed, O2 cone flow |
| alerts | List[WaterAlert] | Toxic thresholds breached |

### State Schema
Tracks estimated total biomass, biofilter maturity index, and cumulative feed fed.

## Dependencies
- Upstream: H11-FOODSCI (Fish health and product quality)
- Downstream: H11-FOODTECH (Harvest scheduling)

## Failure Modes
- Biofilter crash due to medication or sudden pH drop.
- Oxygen depletion from algal blooms crashing at night (in ponds).

## Implementation Notes
Implement robust hysteresis on O2 controls to prevent rapid switching of blowers.
