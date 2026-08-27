# H11C-PIPELINE-RUNNER — Pipeline Runner

> **H11C Control Plane** · orchestrator · `H11C-PIPELINE-RUNNER`

## Purpose
Runs a registered spine hop-by-hop under zero-trust and ALIGN-enforce.

## Technical Deep-Dive
Handler `run_pipeline` in `h11_runtime/control_kernel.py`. This agent is a
typed contract over that handler, not a restatement of L16/L18/L20 taxonomy.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| pipeline_id | `Any` | Input field |
| payload | `Any` | Input field |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| payload | `Any` | Output field |

### State Schema
Shared `KernelState` (blackboard, audit chain, halt latch, spine registry).

## Dependencies
### Upstream (depends on)
`H11C-SPINE-REGISTRAR`, `H11C-ZERO-TRUST-HOP`

### Downstream (feeds into)
`H11C-ALIGN-ENFORCE`

## Failure Modes
- Handler failure fails closed.

## Performance Characteristics
In-process, stdlib, deterministic. Enabling embodiment for the AGI tick.

## Research References
- Lampson, B. (1974). Protection.
- Saltzer & Schroeder (1975). The Protection of Information in Computer Systems.
- Pearl (2009). Causality — used by domain spines this plane gates.

## Implementation Notes
Instantiate via `ControlAgent("H11C-PIPELINE-RUNNER")`. Do not skip ALIGN-ENFORCE.
