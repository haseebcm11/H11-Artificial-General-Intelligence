# H11C-ACTION-LICENSE — Action License

> **H11C Control Plane** · security · `H11C-ACTION-LICENSE`

## Purpose
Issues a one-hop ACT license only when align_enforce, sandbox, and policy pass.

## Technical Deep-Dive
Handler `license` in `h11_runtime/control_kernel.py`. This agent is a
typed contract over that handler, not a restatement of L16/L18/L20 taxonomy.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| ok_flags | `Any` | Input field |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| licensed | `Any` | Output field |

### State Schema
Shared `KernelState` (blackboard, audit chain, halt latch, spine registry).

## Dependencies
### Upstream (depends on)
`H11C-ALIGN-ENFORCE`, `H11C-SANDBOX-GATE`, `H11C-POLICY-ENGINE`

### Downstream (feeds into)
`H11C-ACTION-BINDER`

## Failure Modes
- Handler failure fails closed.

## Performance Characteristics
In-process, stdlib, deterministic. Enabling embodiment for the AGI tick.

## Research References
- Lampson, B. (1974). Protection.
- Saltzer & Schroeder (1975). The Protection of Information in Computer Systems.
- Pearl (2009). Causality — used by domain spines this plane gates.

## Implementation Notes
Instantiate via `ControlAgent("H11C-ACTION-LICENSE")`. Do not skip ALIGN-ENFORCE.
