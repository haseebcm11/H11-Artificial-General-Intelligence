> **Layer 29** · Sports & Recreation · `H11-NUTRITION-SPORT`

## Purpose

H11-NUTRITION-SPORT dynamically models macronutrient and micronutrient requirements based on athletic energy expenditure and recovery states. It optimizes pre-workout fueling, intra-workout substrate replenishment (e.g., carbohydrate oxidation rates), and post-workout protein synthesis triggers.

It treats the human digestive and metabolic systems as a continuous flow process, aligning nutrient availability with physiological demand spikes.

## Technical Deep-Dive

NUTRITION-SPORT utilizes a dynamic biokinetic model of gastric emptying and intestinal absorption rates. It calculates carbohydrate oxidation caps (e.g., 60-90g/hr limit via SGLT1/GLUT5 transporters) to prescribe optimal carb-ratios (glucose:fructose) for endurance athletes.

For muscle hypertrophy/recovery, it tracks the Muscle Protein Synthesis (MPS) refractory period and maps Leucine threshold requirements against ingested amino acid profiles to calculate the true anabolic efficiency of meals.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `dietary_intake` | `List[MealEvent]` | Food consumed |
| `energy_expenditure` | `float` | Kilocalories burned |
| `workout_intensity` | `Enum` | LOW, MODERATE, HIGH, MAXIMAL |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `glycogen_status` | `float` | Estimated muscle glycogen % |
| `hydration_deficit` | `float` | Fluid replacement needed (L) |
| `recommended_intake` | `NutrientPrescription` | Next meal macros |

### State Schema
Tracks estimated hepatic and muscle glycogen reserves, fluid balance, and circulating blood glucose.

## Dependencies

### Upstream (depends on)
- H11-SPORTSCI (for energy expenditure and sweat rate)

### Downstream (feeds into)
- None directly (Feeds UI)

## Failure Modes
- **Gastric Distress Overload:** Prescribing carb intakes that exceed the athlete's gut trainability.
- **Glycogen Depletion Blindness:** Failing to account for multi-day cumulative depletion during tournament play.

## Performance Characteristics
Batch processing agent, low computational frequency. High database lookup overhead for nutritional density matrices.

## Research References
- Jeukendrup, A. E. (2014). A step towards personalized sports nutrition: carbohydrate intake during exercise.
- Morton, R. W., et al. (2018). A systematic review, meta-analysis and meta-regression of the effect of protein supplementation on resistance training-induced gains in muscle mass and strength in healthy adults.

## Implementation Notes
Implement specific handling for weight-classed sports, tracking acute fluid manipulation vs chronic tissue loss.
