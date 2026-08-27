# H11C-RETRY — Retry Orchestrator

> **H11C Control Plane** · orchestrator · `H11C-RETRY`

## Purpose
Retries a failed hop with bounded attempts; does not retry HALT.

## Technical Deep-Dive
Handler `retry` in `h11_runtime/control_kernel.py`. This agent is a
typed contract over that handler, not a restatement of L16/L18/L20 taxonomy.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| attempts | `Any` | Input field |
| max_attempts | `Any` | Input field |
| halted | `Any` | Input field |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| retry | `Any` | Output field |

### State Schema
Shared `KernelState` (blackboard, audit chain, halt latch, spine registry).

## Dependencies
### Upstream (depends on)
`H11C-HALT`

### Downstream (feeds into)
`H11C-FALLBACK`

## Failure Modes
- Handler failure fails closed.

## Performance Characteristics
In-process, stdlib, deterministic. Enabling embodiment for the AGI tick.

## Research References
- Lampson, B. (1974). Protection.
- Saltzer & Schroeder (1975). The Protection of Information in Computer Systems.
- Pearl (2009). Causality — used by domain spines this plane gates.

## Implementation Notes
Instantiate via `ControlAgent("H11C-RETRY")`. Do not skip ALIGN-ENFORCE.
