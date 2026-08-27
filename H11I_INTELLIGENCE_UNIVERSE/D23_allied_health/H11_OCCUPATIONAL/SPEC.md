> **Layer 23** · Allied Health · `H11-OCCUPATIONAL`

## Purpose

The H11-OCCUPATIONAL agent specializes in the analysis of Activities of Daily Living (ADLs) and functional adaptation. It focuses on how physical, cognitive, or sensory impairments impact an individual's ability to engage in meaningful occupations, synthesizing environmental modifications and adaptive strategies.

It serves as the pragmatic translation layer in the substrate, converting medical and therapeutic constraints into real-world functional blueprints.

## Technical Deep-Dive

This agent models functional capacity using a Person-Environment-Occupation (PEO) fit algorithm. It evaluates topological models of living spaces and maps them against patient functional envelopes to detect barrier intersections.

By applying semantic network analysis to daily routines, it identifies critical path failures in ADLs. The agent uses constraint satisfaction programming to suggest adaptive equipment or task modifications that minimize required degrees of freedom while maximizing independence.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| physical_envelope | ReachVolume | 3D representation of patient reach/mobility |
| cognitive_load_capacity | float | Working memory/attention metric |
| environment_scan | TopologicalMap | 3D mesh or graph of living space |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| adl_modifications | List[TaskMod] | Adapted routines |
| equipment_prescription | List[Eqp] | Recommended adaptive gear |

### State Schema
- `identified_barriers`: Cache of mapped environmental obstacles.
- `functional_baseline`: Historical ADL independence scores.

## Dependencies

### Upstream (depends on)
- H11-PHYSIOTHERAPIA (physical capacity)
- H11-NEURO (cognitive capacity)

### Downstream (feeds into)
- H11-SOCIAL (community integration)

## Failure Modes
- Over-prescription of equipment leading to abandonment.
- Failure to account for fluctuating cognitive states in routine planning.

## Performance Characteristics
Heavily reliant on graph traversal for environment mapping. Low latency requirements, but high memory ceiling for complex 3D topological scans.

## Research References
- Person-Environment-Occupation (PEO) Model.
- Model of Human Occupation (MOHO).

## Implementation Notes
Focus on translating geometric spatial data into semantic barriers (e.g., "doorway too narrow for wheelchair turning radius").
