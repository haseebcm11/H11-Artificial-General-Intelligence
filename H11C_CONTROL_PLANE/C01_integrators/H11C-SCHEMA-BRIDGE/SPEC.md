# H11C-SCHEMA-BRIDGE — Schema Bridge

> **H11C Control Plane** · integrator · `H11C-SCHEMA-BRIDGE`

## Purpose
Maps one agent's output fields onto another's input contract.

## Technical Deep-Dive
Handler `remap_fields` in `h11_runtime/control_kernel.py`. This agent is a
typed contract over that handler, not a restatement of L16/L18/L20 taxonomy.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| payload | `Any` | Input field |
| mapping | `Any` | Input field |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| payload | `Any` | Output field |

### State Schema
Shared `KernelState` (blackboard, audit chain, halt latch, spine registry).

## Dependencies
### Upstream (depends on)
`H11C-CONTRACT-CHECKER`

### Downstream (feeds into)
`H11C-PIPELINE-COMPOSER`

## Failure Modes
- Unmapped required keys fail closed.

## Performance Characteristics
In-process, stdlib, deterministic. Enabling embodiment for the AGI tick.

## Research References
- Lampson, B. (1974). Protection.
- Saltzer & Schroeder (1975). The Protection of Information in Computer Systems.
- Pearl (2009). Causality — used by domain spines this plane gates.

## Implementation Notes
Instantiate via `ControlAgent("H11C-SCHEMA-BRIDGE")`. Do not skip ALIGN-ENFORCE.
