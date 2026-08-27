> **Layer 4** · Veterinary Sciences · `H11-SMALLANIMAL`

## Purpose

The H11-SMALLANIMAL agent is dedicated to the diagnosis, treatment, and ongoing care of small companion animals, primarily canines and felines. It provides critical decision-support for complex medical cases, interpreting multi-modal diagnostic data to generate nuanced treatment plans. Its role in the substrate is to act as the primary consult for companion animal health anomalies.

## Technical Deep-Dive

H11-SMALLANIMAL relies on a probabilistic graphical model (PGM) mapping clinical signs to differential diagnoses in canine and feline species. It employs Bayesian inference networks that account for breed-specific predispositions and age-related risk factors, integrating clinical pathology results and diagnostic imaging reports into its belief state.

The agent's reasoning engine utilizes the ACVIM (American College of Veterinary Internal Medicine) consensus statements as its primary knowledge graph, allowing it to adapt to evolving treatment protocols. It also maintains a dynamic pharmacokinetic model to tailor drug dosages for varying metabolic states (e.g., hepatic or renal insufficiency in geriatric patients).

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| patient_signalment | SignalmentData | Species, breed, age, sex, reproductive status |
| clinical_signs | List[ClinicalSign] | Observed symptoms and duration |
| lab_results | Optional[LabPanel] | CBC, serum chemistry, urinalysis |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| differentials | List[Differential] | Ranked list of possible diagnoses |
| treatment_plan | TreatmentProtocol | Recommended therapeutics and monitoring |
| prognosis | PrognosticIndicator | Expected outcome probability |

### State Schema
The agent maintains an active `PatientCaseProfile` which tracks longitudinal data across multiple consultations, retaining historical diagnostic outcomes and therapeutic responses.

## Dependencies

### Upstream (depends on)
- H11-VETPHARMACOLOGIA: For specific drug interaction and withdrawal metrics.
- H11-VETPATHOLOGIA: For histopathological and cytological interpretation.

### Downstream (feeds into)
- H11-VETCHIRURGIA: For cases requiring surgical intervention.

## Failure Modes
- Over-indexing on rare breed-specific diseases when presenting signs align with common pathologies.
- Failure to account for off-label drug sensitivities (e.g., MDR1 gene mutations in herding breeds) if signalment is incomplete.
- Diagnostic fixation leading to premature closure in atypical presentations.

## Performance Characteristics
High throughput for acute triage scenarios. Employs optimized matrix multiplication for rapid Bayesian updates during critical care evaluation.

## Research References
- Ettinger, S. J., et al. (2017). Textbook of Veterinary Internal Medicine.
- Nelson, R. W., & Couto, C. G. (2019). Small Animal Internal Medicine.

## Implementation Notes
Focus heavily on the SignalmentData validation, as subsequent probabilistic branching heavily relies on correct species and breed identification.
