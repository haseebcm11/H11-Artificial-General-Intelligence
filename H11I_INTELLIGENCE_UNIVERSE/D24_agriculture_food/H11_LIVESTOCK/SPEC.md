> **Layer 24** · Agriculture & Food Sciences · `H11-LIVESTOCK`

## Purpose

The H11-LIVESTOCK agent handles herd and flock management, emphasizing biometric tracking, feed conversion ratio (FCR) optimization, and disease vector prediction. It models metabolic rates and nutritional requirements of ruminants and monogastrics to formulate optimal rations and monitors behavioral anomalies to detect estrus, lameness, or illness early.

## Technical Deep-Dive

Utilizing hidden Markov models (HMM) for behavioral state classification from accelerometer data (e.g., grazing, ruminating, resting), the agent profiles individual animal health. It implements the Cornell Net Carbohydrate and Protein System (CNCPS) to evaluate diets and predict performance. The agent also incorporates thermal humidity index (THI) models to mitigate heat stress, dynamically adjusting feed energy density.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| biometrics | List[AnimalTelemetry] | Accelerometer, GPS, body temp |
| environment | THI_Data | Temp and humidity index |
| feed_inventory| NutritionalProfile | Available silage, grain, supplements |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| ration_formula| RationMix | Formulated daily feed per group |
| health_alerts | List[HealthFlag] | Flags for estrus or illness |
| growth_curve  | FCR_Prediction | Expected weight gain |

### State Schema
Maintains individual animal state matrices including lactation curves, gestation days, and rolling 7-day rumination baselines.

## Dependencies

### Upstream (depends on)
- H11-CROP (Feed and forage quality availability)
- H11-FOODSCI (Links to milk/meat quality output)

### Downstream (feeds into)
- H11-PRECISIONAG (Manure/nutrient mapping)

## Failure Modes
1. False positive estrus detection due to social herd disturbances (e.g., predator presence).
2. CNCPS model divergence if forage dry matter (DM) variance is not updated correctly.
3. Overestimation of intake capacity during severe heat stress, leading to feed wastage.

## Performance Characteristics
High message-passing throughput required for continuous telemetry from thousands of RFID/accelerometer ear tags.

## Research References
- Fox, D. G., et al. (2004). "The Cornell Net Carbohydrate and Protein System model for evaluating herd nutrition and nutrient excretion." Animal Feed Science and Technology.
- Rutten, C. J., et al. (2013). "Sensors to support health management on dairy farms." Journal of Dairy Science.

## Implementation Notes
Use an event-driven architecture to process tag bursts, filtering noise with a Kalman filter before classifying behavior states.
