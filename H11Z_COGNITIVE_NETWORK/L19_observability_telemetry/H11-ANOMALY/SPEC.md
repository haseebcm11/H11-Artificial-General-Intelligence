> **Layer 19** · Observability & Telemetry · `H11-ANOMALY`

## Purpose

The H11-ANOMALY agent is responsible for isolation forests, dbscan, ml-based detection, and concept drift handling. It forms a critical component of the Observability & Telemetry layer by ensuring that system state, performance, and anomalies are accurately captured, processed, and acted upon. Without this agent, the cognitive substrate would lack visibility into its own operations.

## Technical Deep-Dive

H11-ANOMALY employs a dual-model approach: a fast statistical Exponential Moving Average (EMA) for univariate time-series, and a stream-optimized Isolation Forest for multivariate anomaly detection. To combat concept drift, it utilizes the Page-Hinkley test to detect distributional shifts and automatically triggers a background retraining pipeline for the Isolation Forest. Anomalies are scored using a normalized probability density function, and false positives are suppressed using a reinforcement learning bandit that learns from operator feedback (acknowledgments vs. ignores).

The architecture is built on lock-free data structures to guarantee minimal interference with the host processes being observed. Concurrency is handled via a specialized thread-pool with NUMA-aware scheduling, ensuring memory accesses remain local to the processor socket handling the telemetry stream.

Data serialization is highly optimized, utilizing flatbuffers or custom zero-allocation binary formats over the wire, completely bypassing standard JSON overheads except at the final presentation layers.

## Architecture

### Input Contract
| Field | Type | Description |
|---|---|---|
| `feature_vector` | `List[float]` | Multivariate data points |
| `timestamp` | `float` | Event time |

### Output Contract
| Field | Type | Description |
|---|---|---|
| `is_anomaly` | `bool` | True if an anomaly is detected |
| `anomaly_score` | `float` | Score from 0.0 to 1.0 |
| `drift_detected` | `bool` | True if concept drift is occurring |

### State Schema
Isolation forest tree structures and Page-Hinkley test statistics accumulators.

## Dependencies

### Upstream (depends on)
- H11-NODE: For raw system access
- H11-NETWORK: For tracing packet flows

### Downstream (feeds into)
- H11-DASHBOARD: For visualization
- H11-ALERT: For threshold triggering

## Failure Modes
1. Catastrophic forgetting during rapid model updates.
2. Over-suppression of true positives by the RL bandit.
3. CPU saturation during Isolation Forest traversal.

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
