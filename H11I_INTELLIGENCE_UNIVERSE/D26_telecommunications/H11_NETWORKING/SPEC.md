> **Layer 4** · Telecommunications · `H11-NETWORKING`

## Purpose

The H11-NETWORKING agent serves as the logical backbone, bridging L2 physical mediums (Fiber, 5G, Wi-Fi) with upper-layer routing (OSPF, BGP) and transport (TCP/QUIC). It models queueing theory at switching nodes and end-to-end traffic engineering.

## Technical Deep-Dive

It implements token bucket shaping, RED (Random Early Detection) queuing, and BGP route propagation delays. It evaluates congestion collapse scenarios when downstream agents push traffic exceeding aggregated link capacities.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| source_ip | str | Origin IPv6/IPv4 |
| dest_ip | str | Target IP |
| flow_rate_bps | float | Requested bandwidth |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| achieved_bps | float | Actual throughput |
| jitter_ms | float | Delay variation |

### State Schema
Global routing table graphs, AS (Autonomous System) topological maps, and router queue states.

## Dependencies
- Upstream: H11-FIBER, H11-5G, H11-WIFI, H11-SATCOM
- Downstream: None

## Failure Modes
- BGP route flapping causing transient loops
- Microbursts causing buffer bloat

## Performance Characteristics
High memory requirement to store per-flow state and large routing tables.

## Research References
- RFC 4271 (BGP-4)
- RFC 2309 (Queue Management)

## Implementation Notes
Use Dijkstra's algorithm for IGP pathfinding, with caching for steady-state topologies to save compute.
