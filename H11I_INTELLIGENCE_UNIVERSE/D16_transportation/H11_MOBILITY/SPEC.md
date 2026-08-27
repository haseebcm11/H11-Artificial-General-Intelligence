> **Layer 16** · Transportation & Mobility · `H11-MOBILITY`

## Purpose
H11-MOBILITY acts as the macroscopic fleet orchestrator. It solves complex Vehicle Routing Problems (VRP), dynamic fleet dispatching, and multimodal journey planning for MaaS (Mobility as a Service) ecosystems. 

## Technical Deep-Dive
The agent employs bipartite graph matching for rider-driver assignment and heuristic routing (Clarke-Wright Savings algorithm, Ant Colony Optimization) for shared rides. It predicts demand spatially and temporally using Spatio-Temporal Graph Convolutional Networks (STGCN) to pre-position fleets and minimize idle cruising.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| ride_requests | List[Request] | Origin, destination, timeframe |
| fleet_status | List[Vehicle] | Current GPS, capacity, SoC |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| assignments | DispatchGraph | Vehicle-to-rider mapping |
| pricing | SurgeModel | Dynamic pricing multipliers |

### State Schema
- `demand_heatmap`: Spatio-temporal grid of predicted requests
- `active_routes`: Graph edges currently being traversed

## Dependencies
### Downstream
- H11-AUTONOMOUS (issues route waypoints to self-driving pods)
- H11-EV (factors battery state into dispatching)

## Failure Modes
- Fleet starvation in high-demand zones
- Algorithmic gridlock in central business districts

## Research References
- Toth, P., & Vigo, D. (2014). Vehicle Routing: Problems, Methods, and Applications.
- Agatz, N., et al. (2012). Optimization for dynamic ride-sharing.
