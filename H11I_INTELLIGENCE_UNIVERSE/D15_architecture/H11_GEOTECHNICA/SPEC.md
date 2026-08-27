> **Layer 15** · Architecture & Construction · `H11-GEOTECHNICA`

## Purpose
H11-GEOTECHNICA deals with earth materials, foundation design, retaining structures, and soil mechanics. It interprets borehole logs to map subterranean strata and calculates bearing capacities and settlement risks.

## Technical Deep-Dive
Applies the Finite Element Method (FEM) (using frameworks similar to Plaxis) for soil-structure interaction analysis. Implements Mohr-Coulomb and Hardening Soil constitutive models to evaluate slope stability and consolidation settlement over time.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| boreholes | List[Log] | SPT/CPT test data |
| building_loads| Dict | Structural column loads |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| strata_model | 3DMesh | Soil layers |
| foundation | Design | Pile/raft specs |
| settlement | Float | Predicted mm drop |

### State Schema
- `max_bearing_capacity`: Float
- `liquefaction_risk`: Float

## Dependencies
- **Downstream**: H11-BIM

## Failure Modes
- Bearing capacity failure (shear failure of soil)
- Excessive differential settlement

## Implementation Notes
Requires intense matrix computations for non-linear elastoplastic soil models.
