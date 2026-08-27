# H11C-ZERO-TRUST-HOP — Zero-Trust Hop

> **H11C Control Plane** · security · `H11C-ZERO-TRUST-HOP`

## Purpose
Re-verifies identity, token, sandbox, and schema on every hop.

## Technical Deep-Dive
Handler `zero_trust` in `h11_runtime/control_kernel.py`. This agent is a
typed contract over that handler, not a restatement of L16/L18/L20 taxonomy.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| identity | `Any` | Input field |
| token | `Any` | Input field |
| sandboxed | `Any` | Input field |
| schema_ok | `Any` | Input field |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| ok | `Any` | Output field |

### State Schema
Shared `KernelState` (blackboard, audit chain, halt latch, spine registry).

## Dependencies
### Upstream (depends on)
`H11C-IDENTITY`, `H11C-CAPABILITY-TOKEN`, `H11C-SANDBOX-GATE`

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
Instantiate via `ControlAgent("H11C-ZERO-TRUST-HOP")`. Do not skip ALIGN-ENFORCE.
