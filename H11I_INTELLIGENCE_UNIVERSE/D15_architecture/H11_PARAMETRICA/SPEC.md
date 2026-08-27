> **Layer 15** · Architecture & Construction · `H11-PARAMETRICA`

## Purpose
H11-PARAMETRICA specializes in algorithmic and parametric design generation. It utilizes generative design workflows to produce complex geometries, optimize facade panelization, and perform structural form-finding.

## Technical Deep-Dive
Implements Non-Uniform Rational B-Splines (NURBS) mathematical modeling and genetic algorithms (NSGA-II) for multi-objective optimization (e.g., minimizing solar heat gain while maximizing views). Voronoi and Delaunay tessellation algorithms are used for panellization.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| base_surface | NURBS | Base geometry to paramatize |
| parameters | Dict | Domain ranges for sliders |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| optimized_mesh | Mesh | The evolved geometric mesh |
| panel_data | List[Panel] | Fabrication data for panels |

### State Schema
- `generation_count`: Current GA generation
- `pareto_front`: Solutions on the optimal front

## Dependencies
- **Upstream**: H11-ARCHITECTURA
- **Downstream**: H11-BIM

## Failure Modes
- Non-manifold mesh generation
- Genetic algorithm premature convergence

## Implementation Notes
Computationally heavy; relies heavily on vector math and matrix transformations.
