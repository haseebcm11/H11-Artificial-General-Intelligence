# H11C-ROUTER — Router

> **H11C Control Plane** · orchestrator · `H11C-ROUTER`

## Purpose
Routes an envelope to the next agent id in the compiled pipeline.

## Technical Deep-Dive
Handler `route` in `h11_runtime/control_kernel.py`. This agent is a
typed contract over that handler, not a restatement of L16/L18/L20 taxonomy.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| pipeline | `Any` | Input field |
| index | `Any` | Input field |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| next_agent | `Any` | Output field |

### State Schema
Shared `KernelState` (blackboard, audit chain, halt latch, spine registry).

## Dependencies
### Upstream (depends on)
`H11C-PIPELINE-COMPOSER`

### Downstream (feeds into)
`H11C-ZERO-TRUST-HOP`

## Failure Modes
- Handler failure fails closed.

## Performance Characteristics
In-process, stdlib, deterministic. Enabling embodiment for the AGI tick.

## Research References
- Lampson, B. (1974). Protection.
- Saltzer & Schroeder (1975). The Protection of Information in Computer Systems.
- Pearl (2009). Causality — used by domain spines this plane gates.

## Implementation Notes
Instantiate via `ControlAgent("H11C-ROUTER")`. Do not skip ALIGN-ENFORCE.
