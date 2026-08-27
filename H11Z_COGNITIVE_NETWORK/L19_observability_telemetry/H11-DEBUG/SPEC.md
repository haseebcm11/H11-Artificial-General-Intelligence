> **Layer 19** · Observability & Telemetry · `H11-DEBUG`

## Purpose

The H11-DEBUG agent is responsible for post-mortem debugging, trace-based debugging, and ai-assisted debugging. It forms a critical component of the Observability & Telemetry layer by ensuring that system state, performance, and anomalies are accurately captured, processed, and acted upon. Without this agent, the cognitive substrate would lack visibility into its own operations.

## Technical Deep-Dive

H11-DEBUG implements deterministic record-and-replay debugging using a hypervisor-level intercept to record non-deterministic inputs (network packets, thread scheduling interleavings, hardware interrupts). The replay engine uses a modified version of the rr (record and replay) algorithm. For AI-assisted root causing, it utilizes an AST (Abstract Syntax Tree) aware symbolic execution engine that works backwards from core dump registers to identify the precise code path and variable states that triggered a segfault or panic.

The architecture is built on lock-free data structures to guarantee minimal interference with the host processes being observed. Concurrency is handled via a specialized thread-pool with NUMA-aware scheduling, ensuring memory accesses remain local to the processor socket handling the telemetry stream.

Data serialization is highly optimized, utilizing flatbuffers or custom zero-allocation binary formats over the wire, completely bypassing standard JSON overheads except at the final presentation layers.

## Architecture

### Input Contract
| Field | Type | Description |
|---|---|---|
| `core_dump_path` | `str` | Path to the crash dump |
| `binary_hash` | `str` | Hash of the executable |

### Output Contract
| Field | Type | Description |
|---|---|---|
| `failing_line` | `str` | Predicted source file and line |
| `symbolic_path` | `List[str]` | Execution path leading to the crash |

### State Schema
Mappings of debug symbols (DWARF/PDB) and recorded execution traces.

## Dependencies

### Upstream (depends on)
- H11-NODE: For raw system access
- H11-NETWORK: For tracing packet flows

### Downstream (feeds into)
- H11-DASHBOARD: For visualization
- H11-ALERT: For threshold triggering

## Failure Modes
1. Divergence during replay execution.
2. OOM while loading massive core dumps.
3. Missing debug symbols for stripped binaries.

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
