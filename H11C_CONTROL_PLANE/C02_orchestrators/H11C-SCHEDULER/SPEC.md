# H11C-SCHEDULER — Scheduler

> **H11C Control Plane** · orchestrator · `H11C-SCHEDULER`

## Purpose
Priority queue of ready hops. Safety-gated hops outrank speculative ones.

## Technical Deep-Dive
Handler `schedule` in `h11_runtime/control_kernel.py`. This agent is a
typed contract over that handler, not a restatement of L16/L18/L20 taxonomy.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| queue | `Any` | Input field |
| item | `Any` | Input field |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| queue | `Any` | Output field |

### State Schema
Shared `KernelState` (blackboard, audit chain, halt latch, spine registry).

## Dependencies
### Upstream (depends on)
`H11C-BUDGET-CONTROLLER`

### Downstream (feeds into)
`H11C-ROUTER`

## Failure Modes
- Handler failure fails closed.

## Performance Characteristics
In-process, stdlib, deterministic. Enabling embodiment for the AGI tick.

## Research References
- Lampson, B. (1974). Protection.
- Saltzer & Schroeder (1975). The Protection of Information in Computer Systems.
- Pearl (2009). Causality — used by domain spines this plane gates.

## Implementation Notes
Instantiate via `ControlAgent("H11C-SCHEDULER")`. Do not skip ALIGN-ENFORCE.
