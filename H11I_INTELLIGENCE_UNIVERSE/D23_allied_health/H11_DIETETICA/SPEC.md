> **Layer 23** · Allied Health · `H11-DIETETICA`

## Purpose

The H11-DIETETICA agent computes complex nutritional biochemistry requirements based on metabolic state, disease vectors, and pharmacological interactions. It designs parenteral (TPN), enteral, and oral nutritional interventions to optimize metabolic homeostasis.

It plays a critical role in intensive care and chronic disease management within the substrate, dynamically altering macronutrient ratios based on inflammatory markers and organ function.

## Technical Deep-Dive

The agent utilizes the Harris-Benedict equation, modified by stress and activity factors (e.g., Penn State equation for ventilated patients), to determine exact resting energy expenditure (REE). It models nitrogen balance dynamically based on urea excretion to titrate amino acid infusions.

For micronutrients, it employs pharmacokinetic models to anticipate depletion caused by specific drug therapies (e.g., loop diuretics and potassium). It uses constraint-based optimization (Simplex algorithm) to formulate meal plans or TPN bags that meet exact macro/micronutrient goals without exceeding fluid volume limits.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| metabolic_panel | LabResults | Current serum biochemistry |
| anthropometrics | BodyMet | Weight, height, BMI, body comp |
| clinical_stress | float | Burn/Trauma/Sepsis multiplier |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| energy_target | float | Total kcal/day required |
| formulation | NutriForm | Exact breakdown of macro/micronutrients |
| delivery_route | Route | Enteral, Parenteral, Oral |

### State Schema
- `cumulative_caloric_deficit`: Tracking underfeeding/overfeeding over time.
- `fluid_allowance`: Strict limits dictated by renal/cardiac status.

## Dependencies

### Upstream (depends on)
- H11-ENDOCRINOLOGIA (insulin sensitivity)
- H11-SPEECH (for safe oral texture limits)

## Failure Modes
- Refeeding syndrome caused by rapid carbohydrate reintroduction in malnourished states.
- Fluid overload in TPN prescription for heart failure patients.

## Performance Characteristics
High precision required for TPN compounding calculations. Operates synchronously with laboratory result streams.

## Research References
- ASPEN/ESPEN Guidelines for Clinical Nutrition.
- Penn State equation for critically ill patients.

## Implementation Notes
Implement rigorous bounds-checking on potassium and phosphorus calculations to prevent fatal arrhythmias from TPN formulations.
