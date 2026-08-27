> **Layer 3** · Dental Sciences · `H11-PAEDODONTIA`

## Purpose
H11-PAEDODONTIA manages the unique physiological, developmental, and behavioral aspects of pediatric dental care. It tracks the chronological eruption and exfoliation of primary (deciduous) dentition, intervenes in early childhood caries (ECC), and manages interceptive orthodontics (space maintenance).

Unlike adult agents, this unit heavily weights behavior management scales (e.g., Frankl Scale) and applies age-specific pharmacological dosages (e.g., localized anesthetics, nitrous oxide sedation) constrained by pediatric weight percentiles.

## Technical Deep-Dive
The agent models the mixed dentition phase dynamically. It utilizes Nolla's stages of tooth calcification to predict eruption timelines and identify impactions or ectopic eruptions early. For space management, it calculates Moyers' mixed dentition analysis to predict the size of unerupted permanent canines and premolars, prescribing space maintainers (e.g., band and loop, Nance appliance) when premature primary tooth loss occurs.

Preventive modeling involves fluoride pharmacokinetic tracking to balance caries prevention against the risk of dental fluorosis during amelogenesis. It calculates precise fluoride varnish (5% NaF) application frequencies based on individualized ECC risk vectors.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| patient_age_months | int | Chronological age |
| patient_weight_kg | float | Weight for dosage calculation |
| primary_odontogram | Dict[str, ToothState] | Charting using letters (A-T) |
| behavior_score | int | Frankl Behavior Rating Scale (1-4) |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| developmental_status | EruptionPhase | Primary, Mixed, or Permanent |
| space_analysis | SpaceDiscrepancy | Arch length minus required space |
| treatment_plan | List[PedoProcedure] | Restorations, SSCs, Pulpotomies |
| rx_dosage | Dict[str, float] | Safe anesthetic limits in mg |

### State Schema
Maintains a `DevelopmentalTimeline` forecasting the exfoliation of primary teeth and eruption of permanent successors, alerting on delayed milestones.

## Dependencies

### Upstream
- H11-MEDICALIS: Pediatric systemic health and growth charts.

### Downstream
- H11-ORTHODONTIA: Referrals for Phase I interceptive orthodontics.

## Failure Modes
1. **Local Anesthetic Toxicity:** Exceeding the maximum recommended dose (mg/kg) of lidocaine in a low-weight pediatric patient.
2. **Space Loss:** Failing to prescribe a space maintainer for a prematurely lost primary second molar, leading to permanent premolar impaction.
3. **Behavioral Breakdown:** Attempting complex restorative work on a Frankl 1 (definitely negative) patient without sedation.

## Performance Characteristics
Low computational overhead. High requirement for rapid heuristic rule evaluation based on age/weight matrices.

## Research References
- American Academy of Pediatric Dentistry (AAPD) Reference Manual.
- Moyers, R. E. (1988). Handbook of Orthodontics.

## Implementation Notes
Implement a state machine for the dentition transition, where each primary tooth holds a pointer to its permanent successor, updating eruption probabilities periodically.
