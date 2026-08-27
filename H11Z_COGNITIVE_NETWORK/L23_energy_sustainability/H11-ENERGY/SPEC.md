> **Layer 23** · Energy, Thermal & Sustainability · `H11-ENERGY`

## Purpose

The H11-ENERGY agent is responsible for dynamically profiling, budgeting, and orchestrating the power consumption across the H11 cognitive substrate. It tracks energy use at a highly granular level (per-GPU, per-node, per-rack) and enforces energy-aware scheduling to optimize the total cost of energy while ensuring operational bounds are respected.

In large-scale AI deployments, unmanaged energy spikes can trip data center breakers or incur severe peak-demand charges. This agent continuously samples telemetry from PDUs, BMCs, and out-of-band management controllers to formulate and solve constraint optimization problems for power allocation in real-time.

## Technical Deep-Dive

H11-ENERGY utilizes a Model Predictive Control (MPC) approach for energy allocation. By treating power as an allocatable resource that can be scaled dynamically through RAPL (Running Average Power Limit) on CPUs and NVML power limits on GPUs, the agent controls the power caps of individual nodes to follow a predefined macro-budget.

The core algorithm solves a Mixed-Integer Linear Programming (MILP) problem periodically to determine the optimal power cap $P_{cap,i}$ for each computational node $i$. The objective function minimizes the makespan of the scheduled training and inference jobs subject to the global power constraint $P_{global\_limit}$ and the individual performance/power characteristics of the workloads.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `telemetry_stream` | `NodePowerTelemetry` | Real-time voltage, current, and wattage from nodes |
| `job_queue` | `List[WorkloadProfile]` | Imminent and running tasks with power sensitivity curves |
| `global_cap` | `float` | Maximum aggregate wattage allowed |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `power_allocations` | `Dict[NodeID, PowerCap]` | Dictated power caps to be applied to infrastructure |
| `energy_cost_estimate` | `float` | Projected financial cost of energy for the current epoch |

### State Schema
The agent maintains a rolling window of historical power consumption, a dynamic model of workload power-performance scaling factors, and the current state of grid pricing (e.g., Time-of-Use rates).

## Dependencies

### Upstream (depends on)
- H11-TELEMETRY (L12): For raw hardware metrics.
- H11-ORCHESTRATOR (L5): For job metadata.

### Downstream (feeds into)
- H11-THERMAL-AI: Changes in power allocation directly impact thermal generation.

## Failure Modes
1. Telemetry Dropout: Loss of PDU metrics leads to conservative fail-safe power capping.
2. Cap Enforcement Latency: Delayed application of power caps leading to momentary power spikes above grid limits.

## Performance Characteristics
Control loop latency must remain under 500ms to effectively manage transient power spikes during coordinated workload phases (e.g., simultaneous gradient synchronization).

## Research References
- "Energy-Proportional Computing: A New Definition" (Barroso & Hölzle)
- "Power-aware Scheduling in Data Centers" (Garg et al.)
