> **Layer 4** · Veterinary Sciences · `H11-EQUINA`

## Purpose

The H11-EQUINA agent is specialized in the complex physiology and pathology of the horse. It bridges the gap between general large animal medicine and high-performance sports medicine. Its core purpose is diagnosing and managing lameness, gastrointestinal emergencies (colic), and respiratory conditions that impact athletic performance.

## Technical Deep-Dive

H11-EQUINA incorporates a sophisticated kinematic analysis engine for lameness evaluation. It processes spatiotemporal gait metrics (e.g., from inertial sensor systems) using Fast Fourier Transforms (FFT) to isolate asymmetry in pelvic and head vertical movement. 

For colic triage, the agent uses a multi-variate logistic regression model trained on pain scores, cardiovascular parameters (heart rate, lactate, packed cell volume), and rectal palpation findings to output a predictive probability for surgical intervention versus medical management.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| equine_profile | EquineData | Breed, discipline (e.g., Dressage, Racing), age |
| kinematic_data | Optional[GaitAnalysis] | Sensor data for lameness evaluation |
| colic_parameters | Optional[ColicPanel] | Vitals, systemic lactate, abdominocentesis fluid |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| lameness_localization | JointLocalization | Probable site of lameness |
| surgical_index | float | Probability (0.0-1.0) that colic requires surgery |
| performance_plan | RehabProtocol | Rest, medication, and return-to-work schedule |

### State Schema
Maintains `EquineAthleteRecord`, tracking joint injections, intra-articular therapies, and longitudinal performance metrics over competition seasons.

## Dependencies

### Upstream (depends on)
- H11-VETCHIRURGIA: For surgical planning if surgical_index > 0.85.

### Downstream (feeds into)
- H11-VETPHARMACOLOGIA: For managing FEI (Fédération Équestre Internationale) withdrawal times for controlled substances.

## Failure Modes
- False localization of lameness due to compensatory movement (e.g., right hind lameness presenting as apparent left fore lameness).
- Underestimation of colic severity in stoic breeds (e.g., Draft horses) leading to delayed surgery.
- Recommending medications that violate competition rules for the specific discipline.

## Performance Characteristics
Low latency requirements for colic evaluation (critical emergency). Computationally intensive during FFT processing of multi-sensor high-frequency gait data.

## Research References
- Ross, M. W., & Dyson, S. J. (2010). Diagnosis and Management of Lameness in the Horse.
- White, N. A. (1990). The Equine Acute Abdomen.

## Implementation Notes
Ensure rigorous validation of the `discipline` field, as therapeutic decisions and drug choices are strictly governed by different sporting bodies (FEI, Jockey Club, etc.).
