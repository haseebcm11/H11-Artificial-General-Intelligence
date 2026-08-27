# H11C-JOIN-BARRIER — Join Barrier

> **H11C Control Plane** · orchestrator · `H11C-JOIN-BARRIER`

## Purpose
Joins fanout branches; incomplete sets do not pass.

## Technical Deep-Dive
Handler `join` in `h11_runtime/control_kernel.py`. This agent is a
typed contract over that handler, not a restatement of L16/L18/L20 taxonomy.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| branches | `Any` | Input field |
| expected | `Any` | Input field |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| joined | `Any` | Output field |

### State Schema
Shared `KernelState` (blackboard, audit chain, halt latch, spine registry).

## Dependencies
### Upstream (depends on)
`H11C-PARALLEL-FANOUT`

### Downstream (feeds into)
`H11C-RESULT-REDUCER`

## Failure Modes
- Handler failure fails closed.

## Performance Characteristics
In-process, stdlib, deterministic. Enabling embodiment for the AGI tick.

## Research References
- Lampson, B. (1974). Protection.
- Saltzer & Schroeder (1975). The Protection of Information in Computer Systems.
- Pearl (2009). Causality — used by domain spines this plane gates.

## Implementation Notes
Instantiate via `ControlAgent("H11C-JOIN-BARRIER")`. Do not skip ALIGN-ENFORCE.
