> **Layer 19** · Arts, Design & Creativity · `H11-SCULPTURA`

## Purpose

The H11-SCULPTURA agent operates on 3D manifolds, applying deformations, booleans, and topological modifications to simulate digital sculpting.

## Technical Deep-Dive

Utilizes half-edge data structures to manage dynamic topology. Employs OpenVDB for volumetric boolean operations and robust voxel remeshing.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| base_mesh | MeshData | Initial geometry |
| tool_strokes | List[Stroke] | Brushes |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| final_mesh | MeshData | Modified geometry |

### State Schema
- `is_manifold`: Boolean checking for non-manifold edges.

## Dependencies
- Upstream: Geomatrix agents.
- Downstream: Animation and Game Design.

## Failure Modes
- Non-manifold generation during decimation.
- Float precision loss in thin areas.

## Performance Characteristics
GPU memory bandwidth bound during VDB conversion.

## Implementation Notes
Rely on bounding volume hierarchies (BVH) for fast ray-mesh intersections during stroke projection.
