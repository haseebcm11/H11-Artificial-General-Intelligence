# H11C-CAPABILITY-TOKEN — Capability Token

> **H11C Control Plane** · security · `H11C-CAPABILITY-TOKEN`

## Purpose
Mints HMAC-style capability tokens. Scopes are explicit; absence is deny.

## Technical Deep-Dive
Handler `capability` in `h11_runtime/control_kernel.py`. This agent is a
typed contract over that handler, not a restatement of L16/L18/L20 taxonomy.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| identity | `Any` | Input field |
| scopes | `Any` | Input field |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| token | `Any` | Output field |

### State Schema
Shared `KernelState` (blackboard, audit chain, halt latch, spine registry).

## Dependencies
### Upstream (depends on)
`H11C-IDENTITY`

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
Instantiate via `ControlAgent("H11C-CAPABILITY-TOKEN")`. Do not skip ALIGN-ENFORCE.
