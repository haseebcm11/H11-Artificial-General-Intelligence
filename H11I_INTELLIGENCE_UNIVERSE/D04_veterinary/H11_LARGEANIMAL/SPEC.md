> **Layer 4** · Veterinary Sciences · `H11-LARGEANIMAL`

## Purpose

The H11-LARGEANIMAL agent focuses on production animal medicine, herd health, and metabolic diseases in bovine, porcine, and ovine species. It shifts the paradigm from individual patient care to population-level health economics, balancing disease mitigation with production efficiency and food safety.

## Technical Deep-Dive

This agent utilizes a Markov Decision Process (MDP) to optimize herd management strategies. It models the progression of infectious diseases (e.g., Bovine Respiratory Disease Complex) across spatially distributed units. The utility function of the MDP incorporates economic variables, cost of intervention, and potential production losses.

For metabolic disorders (like ketosis or milk fever), H11-LARGEANIMAL implements a kinetic nutritional model that evaluates dietary cation-anion difference (DCAD) and energy balances during transitional periods in dairy cattle. It computes complex nutritional matrices to prevent periparturient diseases.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| herd_demographics | HerdData | Species, size, production type (dairy/beef/swine) |
| production_metrics | ProductionStats | Yield, feed conversion ratio, morbidity rates |
| environmental_factors | EnvironmentData | Housing, climate, ration composition |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| intervention_strategy | HerdIntervention | Vaccination, treatment, or culling protocols |
| economic_impact | FinancialProjection | Cost-benefit analysis of intervention |
| nutritional_adjustments | RationModification | Recommended changes to feed composition |

### State Schema
Maintains `HerdLongitudinalState`, tracking disease prevalence, production curves, and historical response to metaphylactic treatments across distinct epidemiological units.

## Dependencies

### Upstream (depends on)
- H11-VETEPIDEMIOLOGIA: For regional disease outbreak intelligence.

### Downstream (feeds into)
- H11-VETPHARMACOLOGIA: For antibiotic residue and withdrawal period calculations.

## Failure Modes
- Miscalculation of the basic reproduction number (R0) leading to inadequate metaphylaxis.
- Overestimating feed conversion ratios, resulting in faulty metabolic disease predictions.
- Failing to account for micro-climatic variations in housing units.

## Performance Characteristics
Optimized for large-scale simulations (Monte Carlo methods) to project herd dynamics over long production cycles (e.g., 300-day lactation curves).

## Research References
- Radostits, O. M., et al. (2007). Veterinary Medicine: A textbook of the diseases of cattle, horses, sheep, pigs and goats.
- Houe, H., et al. (2004). Introduction to Veterinary Epidemiology.

## Implementation Notes
Pay special attention to the `FinancialProjection` module, as decisions in large animal medicine are heavily gated by economic viability matrices.
