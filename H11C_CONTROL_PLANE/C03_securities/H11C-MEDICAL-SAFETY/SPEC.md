# H11C-MEDICAL-SAFETY — Medical Safety Gate

> **H11C Control Plane** · security · `H11C-MEDICAL-SAFETY`

## Purpose
Medical ACT requires confidence ≥ threshold and ALIGN allowed.

## Technical Deep-Dive
Handler `policy` in `h11_runtime/control_kernel.py`. This agent is a
typed contract over that handler, not a restatement of L16/L18/L20 taxonomy.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| rules | `Any` | Input field |
| attrs | `Any` | Input field |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| decision | `Any` | Output field |

### State Schema
Shared `KernelState` (blackboard, audit chain, halt latch, spine registry).

## Dependencies
### Upstream (depends on)
`H11C-ALIGN-ENFORCE`

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
Instantiate via `ControlAgent("H11C-MEDICAL-SAFETY")`. Do not skip ALIGN-ENFORCE.
