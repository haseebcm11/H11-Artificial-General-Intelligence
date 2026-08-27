# H11C-DELEGATION-LIMIT — Delegation Limit

> **H11C Control Plane** · security · `H11C-DELEGATION-LIMIT`

## Purpose
Caps how far a capability may be delegated.

## Technical Deep-Dive
Handler `privilege` in `h11_runtime/control_kernel.py`. This agent is a
typed contract over that handler, not a restatement of L16/L18/L20 taxonomy.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| scopes | `Any` | Input field |
| drop | `Any` | Input field |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| scopes | `Any` | Output field |

### State Schema
Shared `KernelState` (blackboard, audit chain, halt latch, spine registry).

## Dependencies
### Upstream (depends on)
`H11C-CONFUSED-DEPUTY`

### Downstream (feeds into)
`H11C-LEAST-PRIVILEGE`

## Failure Modes
- Handler failure fails closed.

## Performance Characteristics
In-process, stdlib, deterministic. Enabling embodiment for the AGI tick.

## Research References
- Lampson, B. (1974). Protection.
- Saltzer & Schroeder (1975). The Protection of Information in Computer Systems.
- Pearl (2009). Causality — used by domain spines this plane gates.

## Implementation Notes
Instantiate via `ControlAgent("H11C-DELEGATION-LIMIT")`. Do not skip ALIGN-ENFORCE.
