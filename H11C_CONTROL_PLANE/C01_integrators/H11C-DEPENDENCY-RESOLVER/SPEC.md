# H11C-DEPENDENCY-RESOLVER — Dependency Resolver

> **H11C Control Plane** · integrator · `H11C-DEPENDENCY-RESOLVER`

## Purpose
Topologically sorts agent ids from declared upstream edges.

## Technical Deep-Dive
Handler `resolve_deps` in `h11_runtime/control_kernel.py`. This agent is a
typed contract over that handler, not a restatement of L16/L18/L20 taxonomy.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| nodes | `Any` | Input field |
| edges | `Any` | Input field |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| order | `Any` | Output field |

### State Schema
Shared `KernelState` (blackboard, audit chain, halt latch, spine registry).

## Dependencies
### Upstream (depends on)
`H11C-GRAPH-INTEGRATOR`

### Downstream (feeds into)
`H11C-PIPELINE-COMPOSER`

## Failure Modes
- Handler failure fails closed.

## Performance Characteristics
In-process, stdlib, deterministic. Enabling embodiment for the AGI tick.

## Research References
- Lampson, B. (1974). Protection.
- Saltzer & Schroeder (1975). The Protection of Information in Computer Systems.
- Pearl (2009). Causality — used by domain spines this plane gates.

## Implementation Notes
Instantiate via `ControlAgent("H11C-DEPENDENCY-RESOLVER")`. Do not skip ALIGN-ENFORCE.
