> **Layer 4** · Veterinary Sciences · `H11-AVIARIA-VET`

## Purpose

The H11-AVIARIA-VET agent focuses on the unique anatomy, physiology, and pathology of aves. It handles both individual pet bird medicine (psittacines, passerines) and large-scale commercial poultry flock management. The agent is essential for diagnosing highly contagious avian respiratory diseases and managing egg-binding or nutritional deficiencies in companion birds.

## Technical Deep-Dive

For flock management, the agent utilizes a dynamic susceptible-exposed-infectious-recovered (SEIR) model tailored to high-density housing, calculating viral aerosol dispersion based on ventilation rates. It uses time-series analysis on daily mortality rates and water consumption drops to detect early outbreaks of Highly Pathogenic Avian Influenza (HPAI) or Newcastle Disease.

For individual avian patients, the agent parses hematological data uniquely (since avian erythrocytes are nucleated) and manages specific pharmacokinetic challenges, such as the rapid hepatic and renal clearance inherent to avian metabolisms.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| avian_context | AvianContextType | Indicates pet vs. commercial flock |
| species_data | AvianSpeciesInfo | e.g., Gallus gallus domesticus vs. Psittacus erithacus |
| flock_metrics | Optional[FlockData] | Mortality, water intake, egg production drop |
| individual_vitals | Optional[AvianVitals] | Weight in grams, crop status, respiratory rate |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| flock_action | Optional[FlockIntervention] | Biosecurity measures, mass culling orders |
| individual_tx | Optional[AvianTreatment] | Formulary dosages, nebulization protocols |
| zoonotic_risk | RiskLevel | Probability of human transmission (e.g., Chlamydia psittaci) |

### State Schema
Maintains an `AvianOutbreakTracker` for flock contexts, tracking geospatial viral spread. For pets, it maintains `AvianPatientRecord`.

## Dependencies

### Upstream (depends on)
- H11-VETEPIDEMIOLOGIA: For regional surveillance of HPAI.
- H11-VETPATHOLOGIA: For cytology (e.g., diagnosing Trichomonas gallinae).

### Downstream (feeds into)
- H11-VETPHARMACOLOGIA: For managing drug residues in commercial eggs/meat.

## Failure Modes
- Applying mammalian pharmacokinetic models to birds, leading to rapid under-dosing.
- Failure to recognize subtle behavioral signs (fluffing, bottom of cage) as critical emergencies in prey species.
- Ignoring zoonotic protocols when dealing with suspected psittacosis.

## Performance Characteristics
Requires rapid processing of time-series data for flock mortality to prevent exponential outbreak spread in commercial settings.

## Research References
- Harrison, G. J., & Lightfoot, T. L. (2006). Clinical Avian Medicine.
- Saif, Y. M. (2008). Diseases of Poultry.

## Implementation Notes
Implement strict separation between `pet` and `flock` pathways. The regulatory and biosecurity implications of a flock diagnosis (e.g., reportable diseases) require immediate escalation protocols that are absent in pet bird medicine.
