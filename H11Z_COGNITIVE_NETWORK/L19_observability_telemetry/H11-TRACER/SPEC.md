> **Layer 19** · Observability & Telemetry · `H11-TRACER`

## Purpose

The H11-TRACER agent is responsible for request tracing, span hierarchy, context propagation, and tail-based sampling. It forms a critical component of the Observability & Telemetry layer by ensuring that system state, performance, and anomalies are accurately captured, processed, and acted upon. Without this agent, the cognitive substrate would lack visibility into its own operations.

## Technical Deep-Dive

H11-TRACER leverages an OpenTelemetry-compliant model with W3C Trace Context propagation. It implements sophisticated tail-based sampling utilizing a distributed consensus algorithm (Raft) to agree on retaining traces with anomalous latency percentiles across microservices. Spans are stored temporarily in a memory-mapped circular buffer (mmap) before flush. The agent uses directed acyclic graphs (DAGs) to model span hierarchies and quickly identifies the critical path using a modified topological sort algorithm, enabling real-time bottleneck detection.

The architecture is built on lock-free data structures to guarantee minimal interference with the host processes being observed. Concurrency is handled via a specialized thread-pool with NUMA-aware scheduling, ensuring memory accesses remain local to the processor socket handling the telemetry stream.

Data serialization is highly optimized, utilizing flatbuffers or custom zero-allocation binary formats over the wire, completely bypassing standard JSON overheads except at the final presentation layers.

## Architecture

### Input Contract
| Field | Type | Description |
|---|---|---|
| `trace_id` | `str` | 128-bit W3C trace ID |
| `span_id` | `str` | 64-bit span ID |
| `parent_id` | `Optional[str]` | Parent span ID |

### Output Contract
| Field | Type | Description |
|---|---|---|
| `sampled` | `bool` | Whether this trace was selected for retention |
| `critical_path` | `bool` | True if this span is on the critical path |

### State Schema
Tracks active trace trees using an LRU cache and a concurrent hash map of span DAGs.

## Dependencies

### Upstream (depends on)
- H11-NODE: For raw system access
- H11-NETWORK: For tracing packet flows

### Downstream (feeds into)
- H11-DASHBOARD: For visualization
- H11-ALERT: For threshold triggering

## Failure Modes
1. Trace context loss across asynchronous boundaries.
2. Unbounded memory growth from unclosed spans.
3. Clock skew leading to negative span durations.

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
