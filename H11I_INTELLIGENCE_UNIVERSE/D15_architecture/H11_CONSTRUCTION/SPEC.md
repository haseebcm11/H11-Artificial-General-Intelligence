> **Layer 15** · Architecture & Construction · `H11-CONSTRUCTION`

## Purpose
H11-CONSTRUCTION governs the physical realization of the building. It manages 4D scheduling (time), 5D estimating (cost), supply chain logistics, and on-site robotics coordination.

## Technical Deep-Dive
Implements the Critical Path Method (CPM) and PERT for probabilistic project scheduling. Uses Mixed-Integer Linear Programming (MILP) to optimize crane placement and material laydown areas dynamically as the site evolves.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| bim_model | IFCModel | The building data |
| resource_pool| Dict | Labor and equipment |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| schedule | Gantt | CPM schedule |
| site_plan | Map | Logistics layout |
| cost_curve | Curve | S-curve cash flow |

### State Schema
- `current_day`: Int
- `spi`: Float (Schedule Performance Index)
- `cpi`: Float (Cost Performance Index)

## Dependencies
- **Upstream**: H11-BIM

## Failure Modes
- Resource overallocation creating schedule deadlocks
- Supply chain disruptions delaying critical path tasks

## Implementation Notes
Heavily utilizes graph theory for task dependency resolution.
