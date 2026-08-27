> **Layer 29** · Sports & Recreation · `H11-OUTDOOR`

## Purpose

H11-OUTDOOR serves as a backcountry navigation, survival, and performance engine. It calculates energy expenditure for activities like hiking, mountaineering, and trail running across unstructured terrain.

Unlike track-based athletics, this agent must account for variable friction coefficients, altitudinal hypoxia, and weather-dependent metabolic shifts.

## Technical Deep-Dive

OUTDOOR utilizes the Pandolf equation and its modern derivatives to estimate metabolic cost (Watts) of load carriage over graded terrain. It integrates Digital Elevation Models (DEM) with meteorological data to adjust the predicted pacing.

For high-altitude modeling, it computes the partial pressure of oxygen (PaO2) to estimate the decline in VO2Max and the increased risk of Acute Mountain Sickness (AMS), using a compartmental model of acclimatization.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `route_dem` | `TerrainModel` | Topographical data array |
| `load_carriage_kg` | `float` | Backpack weight |
| `weather_conditions` | `WeatherState` | Temperature, wind, humidity |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `estimated_time_enroute` | `float` | Time to complete route (hrs) |
| `caloric_requirement` | `float` | Estimated kcal expenditure |
| `exposure_risk_index` | `float` | 0-1 risk of hypothermia/AMS |

### State Schema
Tracks acclimatization days, core body temperature estimates, and cumulative elevation gain.

## Dependencies

### Upstream (depends on)
- H11-SPORTSCI (for baseline metabolic thresholds)

### Downstream (feeds into)
- None

## Failure Modes
- **Microclimate Blindness:** DEM lacking resolution to show localized avalanche chutes or shade traps.
- **Pandolf Overestimation:** Inaccurate metabolic predictions for highly efficient downhill running techniques.

## Performance Characteristics
High memory usage for spatial DEM processing. Pathfinding requires A* or D* Lite variants with custom cost functions based on human physiology.

## Research References
- Pandolf, K. B., et al. (1977). Predicting energy expenditure with loads while standing or walking very slowly.
- Fulco, C. S., et al. (1998). Maximal and submaximal exercise performance at altitude.

## Implementation Notes
Implement terrain friction coefficients: e.g., paved (1.0), dirt (1.2), snow (1.6), sand (2.1).
