# H11C-MODE-SWITCH — Cognitive Mode Switch

> **H11C Control Plane** · orchestrator · `H11C-MODE-SWITCH`

## Purpose
Switches fast/slow thinking modes; slow mode is mandatory for medical/legal.

## Technical Deep-Dive
Handler `state_machine` in `h11_runtime/control_kernel.py`. This agent is a
typed contract over that handler, not a restatement of L16/L18/L20 taxonomy.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| state | `Any` | Input field |
| event | `Any` | Input field |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| state | `Any` | Output field |

### State Schema
Shared `KernelState` (blackboard, audit chain, halt latch, spine registry).

## Dependencies
### Upstream (depends on)
`H11C-HIGH-STAKES`

### Downstream (feeds into)
`H11C-COGNITIVE-LOOP`

## Failure Modes
- Handler failure fails closed.

## Performance Characteristics
In-process, stdlib, deterministic. Enabling embodiment for the AGI tick.

## Research References
- Lampson, B. (1974). Protection.
- Saltzer & Schroeder (1975). The Protection of Information in Computer Systems.
- Pearl (2009). Causality — used by domain spines this plane gates.

## Implementation Notes
Instantiate via `ControlAgent("H11C-MODE-SWITCH")`. Do not skip ALIGN-ENFORCE.
