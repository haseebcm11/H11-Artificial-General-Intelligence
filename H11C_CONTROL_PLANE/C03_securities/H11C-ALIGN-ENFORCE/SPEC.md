# H11C-ALIGN-ENFORCE — Align Enforce

> **H11C Control Plane** · security · `H11C-ALIGN-ENFORCE`

## Purpose
No ACT unless ALIGN has allowed this trace_id. Skipping ALIGN is a halt.

## Technical Deep-Dive
Handler `align_enforce` in `h11_runtime/control_kernel.py`. This agent is a
typed contract over that handler, not a restatement of L16/L18/L20 taxonomy.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| trace_id | `Any` | Input field |
| align_allowed | `Any` | Input field |
| would_act | `Any` | Input field |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| ok | `Any` | Output field |

### State Schema
Shared `KernelState` (blackboard, audit chain, halt latch, spine registry).

## Dependencies
### Upstream (depends on)
`H11-ALIGN`

### Downstream (feeds into)
`H11C-ACTION-CYCLE`

## Failure Modes
- Handler failure fails closed.

## Performance Characteristics
In-process, stdlib, deterministic. Enabling embodiment for the AGI tick.

## Research References
- Lampson, B. (1974). Protection.
- Saltzer & Schroeder (1975). The Protection of Information in Computer Systems.
- Pearl (2009). Causality — used by domain spines this plane gates.

## Implementation Notes
Instantiate via `ControlAgent("H11C-ALIGN-ENFORCE")`. Do not skip ALIGN-ENFORCE.
