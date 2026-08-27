> **Layer 4** · Veterinary Sciences · `H11-EXOTICA-VET`

## Purpose

The H11-EXOTICA-VET agent provides expert decision support for the medical and surgical management of non-traditional pets (reptiles, small mammals, amphibians). Because species variance is extreme in exotics, this agent focuses on extrapolating pharmacokinetic data across taxa and identifying husbandry-related pathologies that form the bulk of exotic medicine.

## Technical Deep-Dive

H11-EXOTICA-VET leverages an allometric scaling algorithm to adjust drug dosages originally formulated for domestic mammals or birds. It factors in basal metabolic rate (BMR), which varies significantly depending on the environmental temperature of poikilothermic species. 

A core component is the `HusbandryEvaluationEngine`, which maps environmental parameters (UVB gradient, ambient temperature, humidity) against species-specific optima using fuzzy logic. When parameters deviate, the engine generates metabolic bone disease risk scores or dysecdysis (abnormal shedding) probabilities.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| exotic_species_data | TaxonomicIdentifier | Class, order, family, genus, species |
| environmental_params | TerrariumData | Temp gradients, humidity, UV exposure |
| clinical_presentation | List[ExoticSymptom] | Symptoms and duration |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| husbandry_corrections | List[EnvironmentalFix] | Required terrarium modifications |
| scaled_dosages | PharmacokineticAdjustment | Allometrically derived drug doses |
| differential_list | List[ExoticDifferential] | Ranked differentials |

### State Schema
Maintains `TaxaMetabolicDatabase` mapping baseline metabolic indices to taxonomic clades, dynamically updated as new peer-reviewed scaling factors are ingested.

## Dependencies

### Upstream (depends on)
- H11-ZOOLOGIA-VET: For broader taxonomic baselines and captive care standards.

### Downstream (feeds into)
- H11-VETPHARMACOLOGIA: For final drug interaction checks after allometric scaling.

## Failure Modes
- Incorrect taxonomic identification leading to fatal allometric scaling errors (e.g., treating a hindgut fermenter like a foregut fermenter).
- Ignoring temperature-dependent drug metabolism in reptiles, leading to toxicity if the enclosure is too cold.
- Recommending nephrotoxic drugs in the caudal half of reptiles (due to the renal portal system).

## Performance Characteristics
High memory requirement to cache the extensive taxonomic tree and species-specific thermal gradients. Low latency for dosage calculation.

## Research References
- Carpenter, J. W. (2018). Exotic Animal Formulary.
- Mader, D. R. (2005). Reptile Medicine and Surgery.

## Implementation Notes
Implement strict validation for the `TaxonomicIdentifier`. Ambiguous species names (e.g., "turtle") should trigger a hard fault, requiring the precise genus/species (e.g., *Trachemys scripta elegans*).
