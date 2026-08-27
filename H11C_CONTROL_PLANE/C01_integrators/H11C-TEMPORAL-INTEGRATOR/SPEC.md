# H11C-TEMPORAL-INTEGRATOR — Temporal Integrator

> **H11C Control Plane** · integrator · `H11C-TEMPORAL-INTEGRATOR`

## Purpose
Orders hops by timestamp so later hops cannot rewrite earlier ones.

## Technical Deep-Dive
Handler `join_traces` in `h11_runtime/control_kernel.py`. This agent is a
typed contract over that handler, not a restatement of L16/L18/L20 taxonomy.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| traces | `Any` | Input field |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| trace | `Any` | Output field |

### State Schema
Shared `KernelState` (blackboard, audit chain, halt latch, spine registry).

## Dependencies
### Upstream (depends on)
`H11C-TRACE-JOINER`

### Downstream (feeds into)
`H11C-WORLD-BINDER`

## Failure Modes
- Handler failure fails closed.

## Performance Characteristics
In-process, stdlib, deterministic. Enabling embodiment for the AGI tick.

## Research References
- Lampson, B. (1974). Protection.
- Saltzer & Schroeder (1975). The Protection of Information in Computer Systems.
- Pearl (2009). Causality — used by domain spines this plane gates.

## Implementation Notes
Instantiate via `ControlAgent("H11C-TEMPORAL-INTEGRATOR")`. Do not skip ALIGN-ENFORCE.
