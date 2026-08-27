# H11C-CURIOSITY-DRIVER — Curiosity Driver

> **H11C Control Plane** · orchestrator · `H11C-CURIOSITY-DRIVER`

## Purpose
Pushes an epistemic goal only when budget remains after safety hops.

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
`H11C-BUDGET-CONTROLLER`

### Downstream (feeds into)
`H11C-GOAL-STACK`

## Failure Modes
- Handler failure fails closed.

## Performance Characteristics
In-process, stdlib, deterministic. Enabling embodiment for the AGI tick.

## Research References
- Lampson, B. (1974). Protection.
- Saltzer & Schroeder (1975). The Protection of Information in Computer Systems.
- Pearl (2009). Causality — used by domain spines this plane gates.

## Implementation Notes
Instantiate via `ControlAgent("H11C-CURIOSITY-DRIVER")`. Do not skip ALIGN-ENFORCE.
