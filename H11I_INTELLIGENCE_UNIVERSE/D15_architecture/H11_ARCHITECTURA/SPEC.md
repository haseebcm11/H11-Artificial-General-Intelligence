> **Layer 15** · Architecture & Construction · `H11-ARCHITECTURA`

## Purpose
H11-ARCHITECTURA specializes in macroscopic building design and spatial configuration. It handles the initial conceptualization, functional zoning, layout optimization, and aesthetic design of residential, commercial, and mixed-use structures. It acts as the core creative and structural decision-maker in the architectural layer.

## Technical Deep-Dive
The agent utilizes space syntax analysis to determine optimal spatial arrangements. It applies constraint satisfaction models to satisfy building codes and egress requirements. Topology optimization techniques are used for massing generation.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| site_boundary | Polygon | Coordinates of the site |
| zoning_laws | Dict | Local zoning and height restrictions |
| program_reqs | List[Program] | Required spaces and square footage |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| massing | 3DModel | Generated building massing |
| layouts | List[FloorPlan] | 2D layouts per floor |
| egress_paths | List[Path] | Evaluated fire escape routes |

### State Schema
- `current_stage`: Concept, Schematic, or Design Development
- `spatial_graph`: Graph of adjacencies

## Dependencies
- **Downstream**: H11-BIM, H11-SUSTAINABLEARCH

## Failure Modes
- Unresolvable program constraints
- Zoning violations in generated massing

## Implementation Notes
Focuses on topological validity and circulation efficiency.
