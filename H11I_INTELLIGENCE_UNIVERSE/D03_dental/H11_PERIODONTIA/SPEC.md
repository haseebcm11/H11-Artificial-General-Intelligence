> **Layer 3** · Dental Sciences · `H11-PERIODONTIA`

## Purpose
H11-PERIODONTIA specializes in diagnosing, modeling, and treating diseases of the supporting structures of teeth (periodontium, alveolar bone, cementum, and periodontal ligament). It evaluates soft-tissue inflammatory responses, calculates clinical attachment loss (CAL), and prescribes both non-surgical and surgical periodontal interventions.

This agent operates as a crucial stabilization unit; without periodontal health, restorative and orthodontic treatments are contraindicated. It models biofilm dysbiosis, calculus accumulation vectors, and host immune response parameters to accurately stage and grade periodontal disease.

## Technical Deep-Dive
The agent ingests standard 6-point periodontal probing depths, bleeding on probing (BOP), and furcation involvement matrices. It applies the 2017 World Workshop Classification framework to calculate Disease Stage (I-IV) based on interdental CAL and radiographic bone loss, and Disease Grade (A, B, C) based on progression rate, smoking history, and HbA1c levels.

It employs a fluid dynamics simulator to model subgingival plaque microbiome ecosystems, mapping the shift from gram-positive aerobic bacteria to gram-negative anaerobic pathogens (e.g., Porphyromonas gingivalis). Treatment algorithms range from ultrasonic scaling and root planing (SRP) parameters to geometric planning for guided tissue regeneration (GTR) using collagen membranes and bone grafts in intrabony defects.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| probing_depths | Dict[int, List[float]] | 6-point pocket depths per tooth |
| recession_mm | Dict[int, List[float]] | Gingival recession at 6 points |
| mobility | Dict[int, int] | Miller's mobility scale (0-3) |
| risk_factors | PeriodontalRiskProfile | Smoking, diabetes, genetics |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| diagnosis | PerioDiagnosis | Stage (I-IV) and Grade (A-C) |
| srp_plan | List[Quadrant] | Scaling and root planing requirements |
| surgery_targets | List[SurgeryTarget] | Sites requiring flap surgery or grafts |

### State Schema
Maintains `PeriodontalChartState` recording historical CAL trajectories, alveolar crest height regressions, and longitudinal bleeding indices.

## Dependencies

### Upstream
- H11-DENTALIS: Initial charting and radiography inputs

### Downstream
- H11-PROSTHODONTIA: Pre-prosthetic crown lengthening surgery requests
- H11-ORALCHIRURGIA: Extraction orders for teeth with hopeless prognosis

## Failure Modes
1. **Underestimating Aggressive Periodontitis:** Misclassifying rapid CAL in young patients as chronic.
2. **Biologic Width Violation:** Failing to account for necessary supracrestal attached tissues during restorative recommendations.
3. **Over-treatment:** Recommending surgery for pseudopockets caused by gingival hyperplasia rather than true attachment loss.

## Performance Characteristics
High memory requirement for storing longitudinal probing matrices across multiple historical visits to compute progression rate differentials.

## Research References
- Tonetti, M. S., et al. (2018). Staging and grading of periodontitis.
- Socransky, S. S., et al. (1998). Microbial complexes in subgingival plaque.

## Implementation Notes
Implement a temporal differential engine that compares CAL(t) vs CAL(t-1) to calculate the progression derivative, crucial for Grade assignment.
