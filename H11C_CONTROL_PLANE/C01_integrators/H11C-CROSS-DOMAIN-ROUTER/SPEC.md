# H11C-CROSS-DOMAIN-ROUTER — Cross-Domain Router

> **H11C Control Plane** · integrator · `H11C-CROSS-DOMAIN-ROUTER`

## Purpose
Classifies a case into medical/legal/finance/engineering/science/general.

## Technical Deep-Dive
Handler `route_domain` in `h11_runtime/control_kernel.py`. This agent is a
typed contract over that handler, not a restatement of L16/L18/L20 taxonomy.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| case | `Any` | Input field |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| domain | `Any` | Output field |
| pipeline_id | `Any` | Output field |

### State Schema
Shared `KernelState` (blackboard, audit chain, halt latch, spine registry).

## Dependencies
### Upstream (depends on)
`H11C-ADMISSION-CONTROL`

### Downstream (feeds into)
`H11C-MEDICAL-INTEGRATOR`

## Failure Modes
- Handler failure fails closed.

## Performance Characteristics
In-process, stdlib, deterministic. Enabling embodiment for the AGI tick.

## Research References
- Lampson, B. (1974). Protection.
- Saltzer & Schroeder (1975). The Protection of Information in Computer Systems.
- Pearl (2009). Causality — used by domain spines this plane gates.

## Implementation Notes
Instantiate via `ControlAgent("H11C-CROSS-DOMAIN-ROUTER")`. Do not skip ALIGN-ENFORCE.
