# H11C-SESSION — Session Orchestrator

> **H11C Control Plane** · orchestrator · `H11C-SESSION`

## Purpose
Session-scoped blackboard that dies with the session token.

## Technical Deep-Dive
Handler `blackboard` in `h11_runtime/control_kernel.py`. This agent is a
typed contract over that handler, not a restatement of L16/L18/L20 taxonomy.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| op | `Any` | Input field |
| key | `Any` | Input field |
| value | `Any` | Input field |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| board | `Any` | Output field |

### State Schema
Shared `KernelState` (blackboard, audit chain, halt latch, spine registry).

## Dependencies
### Upstream (depends on)
`H11C-SESSION-BOUND`

### Downstream (feeds into)
`H11C-BLACKBOARD`

## Failure Modes
- Handler failure fails closed.

## Performance Characteristics
In-process, stdlib, deterministic. Enabling embodiment for the AGI tick.

## Research References
- Lampson, B. (1974). Protection.
- Saltzer & Schroeder (1975). The Protection of Information in Computer Systems.
- Pearl (2009). Causality — used by domain spines this plane gates.

## Implementation Notes
Instantiate via `ControlAgent("H11C-SESSION")`. Do not skip ALIGN-ENFORCE.
