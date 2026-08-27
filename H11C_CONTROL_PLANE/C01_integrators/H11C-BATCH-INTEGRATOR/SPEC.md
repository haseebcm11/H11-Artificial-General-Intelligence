# H11C-BATCH-INTEGRATOR — Batch Integrator

> **H11C Control Plane** · integrator · `H11C-BATCH-INTEGRATOR`

## Purpose
Folds a batch of cases into per-case summaries without cross-leak.

## Technical Deep-Dive
Handler `reduce_results` in `h11_runtime/control_kernel.py`. This agent is a
typed contract over that handler, not a restatement of L16/L18/L20 taxonomy.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| payload | `Any` | Input field |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| summary | `Any` | Output field |

### State Schema
Shared `KernelState` (blackboard, audit chain, halt latch, spine registry).

## Dependencies
### Upstream (depends on)
`H11C-ISOLATION-DOMAIN`

### Downstream (feeds into)
`H11C-MULTI-CASE`

## Failure Modes
- Handler failure fails closed.

## Performance Characteristics
In-process, stdlib, deterministic. Enabling embodiment for the AGI tick.

## Research References
- Lampson, B. (1974). Protection.
- Saltzer & Schroeder (1975). The Protection of Information in Computer Systems.
- Pearl (2009). Causality — used by domain spines this plane gates.

## Implementation Notes
Instantiate via `ControlAgent("H11C-BATCH-INTEGRATOR")`. Do not skip ALIGN-ENFORCE.
