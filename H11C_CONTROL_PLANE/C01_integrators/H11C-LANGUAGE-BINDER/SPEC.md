# H11C-LANGUAGE-BINDER — Language Binder

> **H11C Control Plane** · integrator · `H11C-LANGUAGE-BINDER`

## Purpose
Binds NLP extraction into typed envelope fields.

## Technical Deep-Dive
Handler `bind_role` in `h11_runtime/control_kernel.py`. This agent is a
typed contract over that handler, not a restatement of L16/L18/L20 taxonomy.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| case | `Any` | Input field |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| bindings | `Any` | Output field |

### State Schema
Shared `KernelState` (blackboard, audit chain, halt latch, spine registry).

## Dependencies
### Upstream (depends on)
None

### Downstream (feeds into)
`H11C-SCHEMA-BRIDGE`

## Failure Modes
- Handler failure fails closed.

## Performance Characteristics
In-process, stdlib, deterministic. Enabling embodiment for the AGI tick.

## Research References
- Lampson, B. (1974). Protection.
- Saltzer & Schroeder (1975). The Protection of Information in Computer Systems.
- Pearl (2009). Causality — used by domain spines this plane gates.

## Implementation Notes
Instantiate via `ControlAgent("H11C-LANGUAGE-BINDER")`. Do not skip ALIGN-ENFORCE.
