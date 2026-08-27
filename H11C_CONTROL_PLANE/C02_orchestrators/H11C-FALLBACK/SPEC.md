# H11C-FALLBACK — Fallback Orchestrator

> **H11C Control Plane** · orchestrator · `H11C-FALLBACK`

## Purpose
Switches to a declared fallback pipeline when the primary fails.

## Technical Deep-Dive
Handler `fallback` in `h11_runtime/control_kernel.py`. This agent is a
typed contract over that handler, not a restatement of L16/L18/L20 taxonomy.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| primary_ok | `Any` | Input field |
| fallback_id | `Any` | Input field |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| pipeline_id | `Any` | Output field |

### State Schema
Shared `KernelState` (blackboard, audit chain, halt latch, spine registry).

## Dependencies
### Upstream (depends on)
`H11C-RETRY`

### Downstream (feeds into)
`H11C-PIPELINE-RUNNER`

## Failure Modes
- Handler failure fails closed.

## Performance Characteristics
In-process, stdlib, deterministic. Enabling embodiment for the AGI tick.

## Research References
- Lampson, B. (1974). Protection.
- Saltzer & Schroeder (1975). The Protection of Information in Computer Systems.
- Pearl (2009). Causality — used by domain spines this plane gates.

## Implementation Notes
Instantiate via `ControlAgent("H11C-FALLBACK")`. Do not skip ALIGN-ENFORCE.
