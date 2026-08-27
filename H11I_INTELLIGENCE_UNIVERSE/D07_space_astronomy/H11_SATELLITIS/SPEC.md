> **Layer 7** · Space & Astronomy · `H11-SATELLITIS`

## Purpose

The H11-SATELLITIS agent manages large-scale, coordinated fleets of satellites (constellations). It handles topology management, inter-satellite link (ISL) routing, autonomous phase spacing, and constellation-wide resource optimization.

While H11-SPACECRAFT manages a single vehicle, H11-SATELLITIS treats hundreds or thousands of nodes as a single distributed organism, ensuring seamless Earth coverage for communications, Earth observation (EO), or navigation (GNSS).

## Technical Deep-Dive

H11-SATELLITIS uses graph theory to manage the dynamic topology of the constellation. As satellites orbit, optical or RF cross-links break and reform; the agent uses algorithms like modified Dijkstra's or Ant Colony Optimization to maintain optimal routing tables across the space segment to minimize latency.

For orbital maintenance, it employs decentralized consensus algorithms (like Swarm Intelligence models) for autonomous station-keeping. Instead of ground-in-the-loop control, nodes negotiate with neighbors to maintain relative phasing (e.g., within a Walker Delta pattern), calculating optimal small burns to correct drag discrepancies without colliding.

It also schedules constellation-wide tasks, resolving conflicts for Earth observation targets using Mixed-Integer Linear Programming (MILP) to maximize ground coverage and downlink throughput while respecting individual node power constraints.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `fleet_telemetry` | `List[NodeTelemetry]` | States from all constellation nodes |
| `task_requests` | `CoverageRequest` | Ground requests for imagery/data routing |
| `network_status` | `LinkGraph` | Current state of inter-satellite links |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `routing_tables` | `TopologyUpdate` | Next-hop tables for space data network |
| `station_keeping` | `ManeuverDirectives` | Coordinated burn commands for phase adjustment |
| `task_schedule` | `NodeAssignments` | Which node performs which observation |

### State Schema
- `walker_configuration`: Ideal orbital parameters (e.g., T/P/F notation).
- `link_topology`: Real-time graph of active laser/RF cross-links.
- `coverage_map`: Gridded matrix of recent Earth observation/communication coverage.

## Dependencies

### Upstream (depends on)
- `H11-SPACECRAFT`: Receives individual bus telemetry and health data.
- `H11-ORBITALIS`: Provides precise orbital mechanics for phase spacing.

### Downstream (feeds into)
- `H11-SPACEDEBRIS`: Coordinates constellation-wide maneuvers to avoid debris clouds.

## Failure Modes
- `KesslerCascadeTrigger`: A collision causing a chain reaction within a dense orbital plane.
- `RoutingLoop`: Topological changes causing data packets to loop endlessly between nodes.
- `PhaseDrift`: Satellites drifting out of their designated slots, creating coverage gaps (holes in the network).

## Performance Characteristics
- Requires extreme parallelization to compute routing tables for thousands of moving nodes every few seconds.
- High network I/O to ingest telemetry from the entire space segment.

## Research References
- Walker, J. G. (1984). Satellite constellations.
- Radhakrishnan, R., et al. (2016). Survey of inter-satellite communication for small satellite networks.
- Vasant, P., et al. (Metaheuristic optimization for satellite scheduling).

## Implementation Notes
Implement robust handling of node failures (network self-healing). The ISL routing must account for the speed of light delay and the shifting relative velocities (Doppler shifts).
