# H11C-SCHEMA-FIREWALL — Schema Firewall

> **H11C Control Plane** · security · `H11C-SCHEMA-FIREWALL`

## Purpose
Drops envelopes that do not match the declared schema_id.

## Technical Deep-Dive
Handler `check_contract` in `h11_runtime/control_kernel.py`. This agent is a
typed contract over that handler, not a restatement of L16/L18/L20 taxonomy.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| payload | `Any` | Input field |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| ok | `Any` | Output field |

### State Schema
Shared `KernelState` (blackboard, audit chain, halt latch, spine registry).

## Dependencies
### Upstream (depends on)
`H11C-VERSION-ALIGNER`

### Downstream (feeds into)
`H11C-CONTRACT-CHECKER`

## Failure Modes
- Handler failure fails closed.

## Performance Characteristics
In-process, stdlib, deterministic. Enabling embodiment for the AGI tick.

## Research References
- Lampson, B. (1974). Protection.
- Saltzer & Schroeder (1975). The Protection of Information in Computer Systems.
- Pearl (2009). Causality — used by domain spines this plane gates.

## Implementation Notes
Instantiate via `ControlAgent("H11C-SCHEMA-FIREWALL")`. Do not skip ALIGN-ENFORCE.
