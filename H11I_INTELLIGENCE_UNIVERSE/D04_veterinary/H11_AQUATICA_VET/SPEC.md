> **Layer 4** · Veterinary Sciences · `H11-AQUATICA-VET`

## Purpose

The H11-AQUATICA-VET agent addresses the intersection of animal biology and fluid environments. It manages health in teleost fish, elasmobranchs, marine mammals, and aquatic invertebrates. Its defining feature is treating the *water* as a fundamental component of the patient's physiology, actively modeling nitrogen cycles, dissolved oxygen gradients, and salinity impacts on osmoregulation.

## Technical Deep-Dive

The agent utilizes a coupled bio-chemical engine to track water quality parameters (ammonia, nitrite, nitrate, pH, temperature, DO). It uses thermodynamic equilibrium models to calculate the concentration of un-ionized ammonia (NH3) relative to total ammonia nitrogen (TAN), as NH3 toxicity in fish is highly pH and temperature-dependent.

For marine mammals, the agent includes modules for dive physiology, calculating nitrogen supersaturation risks (bends) in compromised animals, and adapting standard pharmacokinetic models to account for thick blubber layers (altering the volume of distribution for lipophilic drugs).

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| aquatic_species | WaterTaxa | Species and environmental requirement (fresh/marine) |
| water_chemistry | WaterPanel | pH, TAN, Nitrite, Salinity, Temperature, DO |
| population_signs | List[AquaticSign] | e.g., Flashing, piping at surface, buoyancy issues |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| water_quality_alert | QualityWarning | Specific toxicities identified (e.g., NH3 spike) |
| therapeutic_bath | BathProtocol | Calculations for immersion treatments (e.g., Formalin) |
| systemic_treatment | MarineDose | Injectable/oral doses modified for aquatic taxa |

### State Schema
Maintains `BiofilterState` to model the maturation and health of the nitrifying bacteria (Nitrosomonas and Nitrobacter) within the closed aquatic system.

## Dependencies

### Upstream (depends on)
- H11-VETPATHOLOGIA: For wet-mount gill and skin cytology interpretation.

### Downstream (feeds into)
- H11-ZOOLOGIA-VET: For marine mammal enclosure design standards.

## Failure Modes
- Calculating drug dosages based on body weight without subtracting the volume of the shell/carapace in aquatic turtles or invertebrates.
- Recommending antibacterial treatments that annihilate the system's biofilter, causing secondary ammonia toxicity.
- Misinterpreting total ammonia nitrogen (TAN) as safe when pH and temperature shift the equilibrium toward toxic NH3.

## Performance Characteristics
Continuous integration of streaming water-quality sensor data. Rapid calculation of thermodynamic equilibria.

## Research References
- Noga, E. J. (2010). Fish Disease: Diagnosis and Treatment.
- Dierauf, L. A., & Gulland, F. M. (2001). CRC Handbook of Marine Mammal Medicine.

## Implementation Notes
The `WaterPanel` must be evaluated *before* any biological symptoms are processed. In aquatic medicine, 80% of pathologies are directly caused by environmental degradation.
