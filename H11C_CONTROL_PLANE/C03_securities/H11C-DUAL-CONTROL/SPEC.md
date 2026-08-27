# H11C-DUAL-CONTROL — Dual Control

> **H11C Control Plane** · security · `H11C-DUAL-CONTROL`

## Purpose
High-stakes ACT requires two independent approvals.

## Technical Deep-Dive
Handler `dual` in `h11_runtime/control_kernel.py`. This agent is a
typed contract over that handler, not a restatement of L16/L18/L20 taxonomy.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| approvals | `Any` | Input field |
| need | `Any` | Input field |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| ok | `Any` | Output field |

### State Schema
Shared `KernelState` (blackboard, audit chain, halt latch, spine registry).

## Dependencies
### Upstream (depends on)
`H11C-HIGH-STAKES`

### Downstream (feeds into)
`H11C-ACTION-LICENSE`

## Failure Modes
- Handler failure fails closed.

## Performance Characteristics
In-process, stdlib, deterministic. Enabling embodiment for the AGI tick.

## Research References
- Lampson, B. (1974). Protection.
- Saltzer & Schroeder (1975). The Protection of Information in Computer Systems.
- Pearl (2009). Causality — used by domain spines this plane gates.

## Implementation Notes
Instantiate via `ControlAgent("H11C-DUAL-CONTROL")`. Do not skip ALIGN-ENFORCE.
