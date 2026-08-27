> **Layer 3** · Dental Sciences · `H11-DENTALIS`

## Purpose
H11-DENTALIS acts as the primary diagnostic and planning node for general dentistry and oral health within the H11 Intelligence Universe. It models complex tooth anatomy, processes cariology data, and simulates restorative outcomes using diverse dental materials. By establishing foundational dental records, it sets the stage for specialized downstream treatments.

This agent evaluates overall oral hygiene, detects early signs of caries through multi-modal inputs (including digital radiography vectors and tactile probe data equivalents), and proposes comprehensive preventive and restorative treatment plans.

## Technical Deep-Dive
H11-DENTALIS utilizes a spatial-volumetric mapping model of the oral cavity, representing teeth using the Universal Numbering System intertwined with FDI notation mappings for global interoperability. Each tooth is modeled as a 3D mesh with distinct anatomical layers (enamel, dentin, pulp), tracked dynamically for structural integrity and demineralization levels.

Caries pathogenesis is modeled via a modified Stephan Curve simulator and the International Caries Detection and Assessment System (ICDAS). The agent probabilistically predicts lesion progression based on saliva pH time-series, dietary carbohydrate intake vectors, and fluoride exposure histories. Restorative planning involves finite element analysis (FEA) to determine the stress distribution on various materials (composite resins, amalgams, glass ionomers) under simulated occlusal loads.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| patient_id | str | Unique patient identifier |
| charting_data | Dict[int, List[ChartingEvent]] | Baseline tooth charting |
| radiographs | List[RadiographVector] | Processed imaging features |
| icdas_scores | Dict[int, float] | ICDAS visual scores per tooth |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| caries_risk | CariesRiskAssessment | Overall caries risk profile |
| treatment_plan | List[RestorativeProcedure] | Proposed restorative interventions |
| materials_spec | Dict[str, MaterialProperty] | Recommended restorative materials |

### State Schema
Maintains a `DentalArchState` detailing real-time charting status, active restorations, and caries lesion depths for 32 permanent and/or 20 primary teeth.

## Dependencies

### Upstream
- H11-MEDICALIS: Systemic health conditions impacting oral health

### Downstream
- H11-ENDODONTIA: Irreversible pulpitis referrals
- H11-PROSTHODONTIA: Extensive coronal destruction requiring crowns

## Failure Modes
1. **False-Positive Cavitation:** Overestimating lesion depth from radiograph artifacts.
2. **Material Mismatch:** Selecting a restorative material that fails under maximum intercuspation forces.
3. **Numbering Collision:** Confusion between primary and permanent tooth identifiers in mixed dentitions.

## Performance Characteristics
Optimized for real-time charting updates with low-latency (<50ms) topological updates to the 3D dental arch state.

## Research References
- International Caries Detection and Assessment System (ICDAS) Coordinating Committee (2005)
- Featherstone, J. D. B. (2000). The Science and Practice of Caries Prevention.

## Implementation Notes
Employs a custom `DentalArchGraph` where nodes are teeth and edges represent interproximal contacts to propagate caries risk probabilistically.
