# H11C-NESTED-GOAL — Nested Goal Orchestrator

> **H11C Control Plane** · orchestrator · `H11C-NESTED-GOAL`

## Purpose
Child goals inherit parent compartments and licenses.

## Technical Deep-Dive
Handler `goal_stack` in `h11_runtime/control_kernel.py`. This agent is a
typed contract over that handler, not a restatement of L16/L18/L20 taxonomy.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| op | `Any` | Input field |
| goal | `Any` | Input field |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| stack | `Any` | Output field |

### State Schema
Shared `KernelState` (blackboard, audit chain, halt latch, spine registry).

## Dependencies
### Upstream (depends on)
`H11C-GOAL-STACK`

### Downstream (feeds into)
`H11C-COMPARTMENT`

## Failure Modes
- Handler failure fails closed.

## Performance Characteristics
In-process, stdlib, deterministic. Enabling embodiment for the AGI tick.

## Research References
- Lampson, B. (1974). Protection.
- Saltzer & Schroeder (1975). The Protection of Information in Computer Systems.
- Pearl (2009). Causality — used by domain spines this plane gates.

## Implementation Notes
Instantiate via `ControlAgent("H11C-NESTED-GOAL")`. Do not skip ALIGN-ENFORCE.
