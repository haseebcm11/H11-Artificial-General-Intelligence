> **Layer 1** · Medicine & Health Sciences · `H11-ANAESTHESIA`

## Purpose
The H11-ANAESTHESIA agent manages the complex interplay of hypnosis, analgesia, and muscle relaxation during surgical procedures. It ensures the patient remains completely unconscious and pain-free without suffering hemodynamic collapse, relying on real-time simulation of drug kinetics and electroencephalographic (EEG) feedback.

## Technical Deep-Dive
This agent relies on continuous multicompartment Pharmacokinetic (PK) and Pharmacodynamic (PD) modeling. Specifically, it employs the Schnider model for Propofol and the Minto model for Remifentanil, calculating effect-site concentrations ($C_e$) using first-order rate constants ($k_{1e}$, $k_{e0}$).
It features a closed-loop controller (Proportional-Integral-Derivative augmented with Model Predictive Control) that predicts the future depth of anesthesia (e.g., using Bispectral Index or Patient State Index) and dynamically suggests adjustments to Target-Controlled Infusion (TCI) pumps.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `demographics` | `PatientDemographics` | Includes lean body mass (LBM) via James equation |
| `sensor_data` | `SensorFeed` | Heart rate, MAP, BIS, Nociception index (NOL) |
| `drug_rates` | `Dict[str, float]` | Current mg/hr or mcg/kg/min infusions |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `ce_estimations` | `Dict[str, float]` | Real-time estimated effect-site concentrations |
| `tci_recommendations` | `List[PumpAdjustment]` | Optimal rate changes to maintain targets |

### State Schema
Tracks the mass (in mg) of each drug in three central/peripheral compartments ($X_1, X_2, X_3$) and the hypothetical effect-site compartment ($X_e$).

## Dependencies
### Upstream (depends on)
* H11-PHARMACOLOGIA: Source of truth for PK/PD population rate constants.
### Downstream (feeds into)
* H11-CHIRURGIA: Informs the surgical agent of optimal windows for extreme stimulation (e.g., incision).

## Failure Modes
1. **Context-Sensitive Half-Time Underestimation:** Prolonged infusions cause peripheral compartment saturation, leading to excessively delayed wake-up times if predictions ignore total mass.
2. **EEG Artifact Misinterpretation:** Electrocautery interference acting as a false high BIS score, prompting dangerous overdose.
3. **Synergistic Hemodynamic Collapse:** Overestimating sympathetic tone, leading to profound bradycardia from remifentanil + propofol synergy.

## Performance Characteristics
Must run extremely fast (Hz to kHz) to process high-resolution physiological waveforms. Latency must be <10ms for closed-loop TCI adjustments.

## Research References
1. Schnider, T. W., et al. (1998). "The influence of method of administration and covariates on the pharmacokinetics of propofol in adult volunteers." *Anesthesiology*.
2. Minto, C. F., et al. (1997). "Influence of age and gender on the pharmacokinetics and pharmacodynamics of remifentanil." *Anesthesiology*.

## Implementation Notes
Use Runge-Kutta 4th order (RK4) integration for updating the differential equations of compartment masses between sensor ticks.
