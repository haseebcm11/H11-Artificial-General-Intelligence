> **Layer 1** · Medicine & Health Sciences · `H11-TOXICOLOGIA`

## Purpose
The H11-TOXICOLOGIA agent rapidly diagnoses clinical poisoning based on physiological toxidrome patterns and simulates the Toxicokinetics (absorption, distribution, metabolism, excretion) of xenobiotics. It provides critical, time-sensitive guidance for antidote administration and decontamination protocols.

## Technical Deep-Dive
It utilizes a dual approach: 
1. **Pattern Recognition (Toxidromes):** Employs a naive Bayes or decision tree classifier to map clinical signs (e.g., miosis, diaphoresis, bradycardia) to classic toxidromes (e.g., Cholinergic, Opiate). 
2. **Physiologically Based Toxicokinetic (PBTK) Modeling:** Simulates the mass transfer of toxins across multi-organ compartments, explicitly modeling Cytochrome P450 (CYP) biotransformation. This is crucial for toxins like acetaminophen, where the parent compound is safe, but a specific fraction metabolized by CYP2E1 creates the highly reactive and hepatotoxic NAPQI.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `clinical_signs` | `Dict[str, str/float]` | HR, RR, Temp, Pupil Size, Skin Moisture |
| `exposure_data` | `Exposure` | Substance, dose, route, time since exposure |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `toxidrome` | `str` | Probabilistic classification |
| `pbtk_forecast` | `Dict[str, float]` | Predicted peak concentrations in target organs |
| `antidote` | `AntidoteRecommendation` | Drug, dose, and administration criteria |

### State Schema
Tracks the ongoing biotransformation pathways, specifically the depletion of endogenous protective substrates (like glutathione).

## Dependencies
### Upstream (depends on)
* H11-PHARMACOLOGIA: For baseline enzyme kinetic data (Vmax, Km).
### Downstream (feeds into)
* H11-NEUROLOGIA / H11-CARDIOLOGIA: Informing them of expected toxic end-organ effects (e.g., QTc prolongation, seizures).

## Failure Modes
1. **Polysubstance Masking:** A patient overdoses on both a stimulant and a depressant, resulting in "normal" vitals that fool the toxidrome classifier.
2. **First-Pass Miscalculation:** Incorrectly assuming intravenous bioavailability for an orally ingested toxin undergoing massive hepatic first-pass metabolism.
3. **Glutathione Rebound Ignorance:** Halting N-acetylcysteine (NAC) therapy too early because parent acetaminophen levels dropped, ignoring ongoing NAPQI cellular damage.

## Performance Characteristics
Must execute toxidrome classification instantly (sub-millisecond). PBTK ODE simulations can take up to 1 second for a 72-hour forecast.

## Research References
1. Clewell, H. J., & Andersen, M. E. (1985). "Risk assessment extrapolations and physiological modeling." *Toxicology and Industrial Health*.
2. Erickson, T. B., et al. (2007). "Toxidromes." *Emergency Medicine Clinics of North America*.

## Implementation Notes
Use Michaelis-Menten kinetics to model the saturable pathways of hepatic metabolism, as zero-order kinetics heavily dominate toxic overdose scenarios once therapeutic enzymes are saturated.
