# H11C-SANDBOX-GATE — Sandbox Gate

> **H11C Control Plane** · security · `H11C-SANDBOX-GATE`

## Purpose
Marks a hop sandboxed. Unsandboxed ACT is refused.

## Technical Deep-Dive
Handler `sandbox` in `h11_runtime/control_kernel.py`. This agent is a
typed contract over that handler, not a restatement of L16/L18/L20 taxonomy.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| hop | `Any` | Input field |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| sandboxed | `Any` | Output field |

### State Schema
Shared `KernelState` (blackboard, audit chain, halt latch, spine registry).

## Dependencies
### Upstream (depends on)
`H11C-ISOLATION-DOMAIN`

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
Instantiate via `ControlAgent("H11C-SANDBOX-GATE")`. Do not skip ALIGN-ENFORCE.
