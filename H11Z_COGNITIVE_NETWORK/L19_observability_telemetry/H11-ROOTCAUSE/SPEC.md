> **Layer 19** · Observability & Telemetry · `H11-ROOTCAUSE`

## Purpose

The H11-ROOTCAUSE agent is responsible for automated rca, causal inference, postmortem process, and fault tree analysis. It forms a critical component of the Observability & Telemetry layer by ensuring that system state, performance, and anomalies are accurately captured, processed, and acted upon. Without this agent, the cognitive substrate would lack visibility into its own operations.

## Technical Deep-Dive

H11-ROOTCAUSE leverages causal inference (specifically, the PC algorithm for discovering causal DAGs from observational time-series data) to distinguish correlation from causation during an incident. It analyzes trace hierarchies and infrastructure topology to construct a Fault Tree Analysis (FTA) dynamically. The agent also uses a Large Language Model fine-tuned on historical postmortems to automatically draft an initial Incident Timeline Reconstruction and a '5 Whys' report based on the causal graph's root node.

The architecture is built on lock-free data structures to guarantee minimal interference with the host processes being observed. Concurrency is handled via a specialized thread-pool with NUMA-aware scheduling, ensuring memory accesses remain local to the processor socket handling the telemetry stream.

Data serialization is highly optimized, utilizing flatbuffers or custom zero-allocation binary formats over the wire, completely bypassing standard JSON overheads except at the final presentation layers.

## Architecture

### Input Contract
| Field | Type | Description |
|---|---|---|
| `incident_id` | `str` | ID of the meta-incident |
| `affected_services` | `List[str]` | Services involved |

### Output Contract
| Field | Type | Description |
|---|---|---|
| `root_cause_service` | `str` | Probable service at fault |
| `confidence_score` | `float` | Statistical confidence |
| `causal_path` | `List[str]` | Path of cascading failures |

### State Schema
Causal directed acyclic graphs (DAGs) and probabilistic structural equation models.

## Dependencies

### Upstream (depends on)
- H11-NODE: For raw system access
- H11-NETWORK: For tracing packet flows

### Downstream (feeds into)
- H11-DASHBOARD: For visualization
- H11-ALERT: For threshold triggering

## Failure Modes
1. Spurious correlations in highly synchronous microservices.
2. Hidden confounders (e.g., network switch failure) not present in telemetry.
3. Inference timeouts on very large incident topologies.

## Performance Characteristics
- Latency: < 1ms processing overhead
- Throughput: 100k+ events/sec per core
- Memory: Bounded, configurable max heap size
- Compute: Background threads constrained via cgroups

## Research References
- Dapper, a Large-Scale Distributed Systems Tracing Infrastructure (Sigelman et al.)
- Outlier Detection for Time Series (Aggarwal)
- The Google File System (Ghemawat et al. - for underlying immutable logging patterns)

## Implementation Notes
Focus on avoiding global interpreter locks (GIL) in python extensions by delegating core processing loops to Rust or C++ via ctypes/CFFI where applicable.
