> **Layer 19** · Observability & Telemetry · `H11-PROFILER`

## Purpose

The H11-PROFILER agent is responsible for cpu/gpu profiling, flame graphs, and continuous profiling (pyroscope). It forms a critical component of the Observability & Telemetry layer by ensuring that system state, performance, and anomalies are accurately captured, processed, and acted upon. Without this agent, the cognitive substrate would lack visibility into its own operations.

## Technical Deep-Dive

H11-PROFILER performs continuous fleet-wide profiling with minimal overhead using statistical sampling of the instruction pointer via hardware performance counters (PMU). It aggregates stack traces into a trie data structure optimized for differential flame graph generation. For GPU workloads, it interfaces with CUPTI (CUDA Profiling Tools Interface) to sample kernel execution times and memory transfers. The agent implements a backpressure mechanism that dynamically reduces the profiling sampling rate when host CPU utilization exceeds a critical threshold to prevent observer effect.

The architecture is built on lock-free data structures to guarantee minimal interference with the host processes being observed. Concurrency is handled via a specialized thread-pool with NUMA-aware scheduling, ensuring memory accesses remain local to the processor socket handling the telemetry stream.

Data serialization is highly optimized, utilizing flatbuffers or custom zero-allocation binary formats over the wire, completely bypassing standard JSON overheads except at the final presentation layers.

## Architecture

### Input Contract
| Field | Type | Description |
|---|---|---|
| `process_id` | `int` | PID to profile |
| `duration_ms` | `int` | Profiling window |

### Output Contract
| Field | Type | Description |
|---|---|---|
| `flamegraph_json` | `str` | Hierarchical stack trace data |
| `overhead_pct` | `float` | Estimated CPU overhead of the profiler |

### State Schema
Stack trace tries and dynamic sampling rate multipliers.

## Dependencies

### Upstream (depends on)
- H11-NODE: For raw system access
- H11-NETWORK: For tracing packet flows

### Downstream (feeds into)
- H11-DASHBOARD: For visualization
- H11-ALERT: For threshold triggering

## Failure Modes
1. PMU access denied by hypervisor.
2. Stack unwinding failures on JIT-compiled code.
3. Excessive memory usage from deeply recursive stack traces.

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
