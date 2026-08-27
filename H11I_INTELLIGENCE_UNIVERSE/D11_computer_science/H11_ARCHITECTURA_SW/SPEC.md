> **Layer 11** · Computer Science · `H11-ARCHITECTURA_SW`

## Purpose

The Software Architecture agent focuses on macro-level system design. It evaluates architectural patterns (Microservices, Event-Driven, Hexagonal/Ports-and-Adapters, CQRS) and enforces Domain-Driven Design (DDD) boundaries to manage systemic complexity.

## Technical Deep-Dive

Architecture is about managing coupling and cohesion. This agent models bounded contexts, evaluates dependency graphs for cyclic references or "Big Ball of Mud" anti-patterns, and calculates architectural metrics like instability and abstractness (Martin's metrics) to guide system evolution.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `component_graph` | `Graph` | Current system modules and deps |
| `business_domain` | `str` | Description of the problem space |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `target_architecture` | `ArchitectureDef` | Recommended pattern and components |
| `debt_analysis` | `Dict[str, float]` | Metrics indicating architectural debt |

### State Schema
Tracks `bounded_contexts`, `c4_models`, and `adr_log` (Architecture Decision Records).

## Dependencies

### Upstream (depends on)
H11-DEVOPS, H11-API (understanding how things are deployed and connected)

### Downstream (feeds into)
H11-SRE (defining failure domains)

## Failure Modes
- Tight coupling causing cascading failures
- Anemic domain models
- Distributed monolith anti-pattern

## Performance Characteristics
Compute bound during graph analysis of large codebases. Requires O(V+E) for dependency analysis.

## Research References
- Evans, E. (2003). Domain-Driven Design: Tackling Complexity in the Heart of Software.
- Martin, R. C. (2017). Clean Architecture.

## Implementation Notes
Analyzes directed graphs representing code dependencies.
