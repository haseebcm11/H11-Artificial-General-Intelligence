> **Layer 2** · Data Plane & Ingestion · `H11-STREAMING-DATA`

## Purpose

The H11-STREAMING-DATA agent is responsible for real-time ingestion, stateful windowing, and temporal alignment of high-velocity event streams. Unlike batch processes, cognitive substrates require continuous, low-latency sensory input to react dynamically. This agent bridges the gap between raw messaging queues (like Apache Kafka) and the substrate's computational nodes.

By abstracting away the complexities of out-of-order events, late arrivals, and watermark generation, H11-STREAMING-DATA guarantees exactly-once processing semantics and ensures that temporal relationships—vital for sequence modeling—are perfectly preserved.

## Technical Deep-Dive

This agent operates on the principle of stream-table duality, wherein an event stream can be materialized into a state table, and a state table's mutations can be emitted as a changelog stream. It implements robust event-time processing as opposed to processing-time, relying on embedded timestamps and dynamically adjusted watermarks.

Watermarks (W_t) represent a computational assertion that no events with a timestamp T < W_t will arrive. The agent calculates W_t = max(event_timestamps) - max_out_of_order_tolerance. Late data arriving behind the watermark is handled either via side-outputs for distinct processing or discarded based on configuration.

Stateful windowing supports:
- **Tumbling Windows**: Fixed, non-overlapping (e.g., 5-minute chunks).
- **Sliding Windows**: Overlapping frames for continuous rolling aggregations.
- **Session Windows**: Dynamically sized windows bounded by a gap of inactivity (timeout).

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| event_id | UUID | Unique identifier for exactly-once tracking |
| payload | Bytes | The raw sensory or network data |
| event_time | Timestamp | When the event actually occurred |
| key | String | Partitioning key for stateful window routing |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| window_id | String | Identifier mapping to the temporal bounds |
| aggregated_events | List[Dict] | Events coalesced into this window |
| is_late | Boolean | Flag indicating if this was emitted post-watermark |

### State Schema
Maintains `WindowStore` (in-memory representations of active windows), `WatermarkTracker` (current W_t across partitions), and `DeduplicationFilter` (Bloom filter for event IDs).

## Dependencies

### Upstream (depends on)
External message brokers (Kafka/Redpanda) supplying raw data.

### Downstream (feeds into)
H11-SAMPLER, H11-FEATURE-STORE.

## Failure Modes
1. **Watermark Stagnation**: A blocked partition prevents the global watermark from advancing, causing memory exhaustion in active windows.
2. **State Bloat**: Unbounded session windows without strict timeouts consuming all heap space.
3. **Thundering Herd**: Flush of large tumbling windows causing CPU spikes downstream.

## Performance Characteristics
Must maintain sub-millisecond per-event overhead. Scales horizontally by partitioning the stream key space. High memory requirement (Class: High) to store active window frames in memory.

## Research References
- Akidau, T., et al. (2015). "The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing."
- Carbone, P., et al. (2015). "Apache Flink: Stream and Batch Processing in a Single Engine."

## Implementation Notes
Use a fast time-series data structure (e.g., interval trees) for sliding windows. For exactly-once semantics, use two-phase commits linked to offset progression.
