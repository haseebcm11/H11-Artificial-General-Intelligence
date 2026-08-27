> **Layer 1** · Medicine & Health Sciences · `H11-NUTRITIO`

## Purpose
The H11-NUTRITIO agent provides precision metabolic modeling. It goes far beyond static calorie counting by simulating dynamic energy balance, substrate partitioning (fat vs. carbohydrate oxidation), and predicting individualized postprandial glycemic responses based on meal composition and patient metabolic state.

## Technical Deep-Dive
It utilizes the Hall Dynamic Energy Balance Model rather than the static 3500-calorie rule. This model accounts for metabolic adaptation, acknowledging that basal metabolic rate (BMR) changes as lean and fat mass change, and as thermogenesis down-regulates during caloric deficits.
For glycemic control, it employs a compartment model (gastric emptying -> intestinal absorption -> plasma appearance) coupled with minimal models of insulin sensitivity (Bergman Minimal Model). It predicts the continuous glucose excursion curve to help in diabetes management and athletic refueling.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `meal` | `MealData` | Grams of CHO, PRO, FAT, Fiber; Glycemic Index |
| `cgm_history` | `TimeSeries` | Glucose levels leading up to the meal |
| `patient_state` | `MetabolicState` | Current estimated glycogen stores |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `predicted_glucose` | `TimeSeries` | Expected glucose curve over next 3 hours |
| `substrate_utilization` | `Dict[str, float]` | Predicted fat vs carb oxidation rates |

### State Schema
Tracks liver and skeletal muscle glycogen reservoirs, adapting the rate of de novo lipogenesis versus glycogen replenishment based on capacity.

## Dependencies
### Upstream (depends on)
* H11-ENDOCRINOLOGIA: For basal insulin/glucagon tone and insulin sensitivity factors.
### Downstream (feeds into)
* H11-SPORTMEDICINA: Calculates fuel availability for high-intensity training.

## Failure Modes
1. **Gastric Emptying Miscalculation:** Failing to slow the absorption curve when a high-GI carb is co-ingested with high fat/fiber, causing erroneous early glucose spike predictions.
2. **Static BMR Fallacy:** Ignoring adaptive thermogenesis, leading to wildly inaccurate long-term weight loss projections.
3. **Microbiome Variance:** Missing individualized glycemic responses driven by gut microbiota (which can make oatmeal spike one person and ice cream spike another).

## Performance Characteristics
Simulation of a meal's metabolic fate uses ODE solvers over a 180-360 minute timeframe. Can be run asynchronously upon meal logging.

## Research References
1. Hall, K. D., et al. (2011). "Quantification of the effect of energy imbalance on bodyweight." *The Lancet*.
2. Bergman, R. N., et al. (1979). "Quantitative estimation of insulin sensitivity." *American Journal of Physiology*.

## Implementation Notes
Use a system of stiff Ordinary Differential Equations (ODEs) to model the Bergman minimal model variables (Plasma Glucose, Plasma Insulin, Remote Insulin Compartment).
