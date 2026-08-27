> **Layer 2** · Data Plane & Ingestion · `H11-INGEST`

## Purpose

The H11-INGEST agent serves as the entry point for all external and internal data flows entering the H11 Cognitive Substrate. It is responsible for multi-modal, multi-source data intake, supporting file systems, object stores, RDBMS/NoSQL databases, and high-velocity message queues like Kafka and Pulsar. 

Beyond merely moving bytes, H11-INGEST provides dynamic schema detection, runtime backpressure negotiation, and exactly-once delivery guarantees. It ensures that downstream analytical and learning agents are never overwhelmed and always receive well-formed, cryptographically verified data payloads.

## Technical Deep-Dive

To achieve high throughput while maintaining exactly-once semantics, H11-INGEST relies on a Distributed Write-Ahead Log (WAL) and Idempotent Commit Markers. When consuming from ephemeral sources (e.g., REST API webhooks), the payload is immediately serialized to the WAL using a highly optimized binary format (e.g., Protobuf or FlatBuffers) before acknowledgment is sent to the source.

Schema inference utilizes a Reservoir Sampling approach combined with a Probabilistic Type Automaton. By sampling the first $k$ records of a streaming batch, it infers nested schema structures with 99.9% confidence without buffering the entire dataset. 

For backpressure handling, the agent implements a Token Bucket algorithm combined with TCP-like Additive Increase / Multiplicative Decrease (AIMD) flow control. If downstream buffers fill, the ingestion rate is multiplicatively scaled back to prevent out-of-memory cascades, smoothly increasing once the pressure subsides.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `source_uri` | `URI` | Protocol-specific identifier (e.g., `kafka://broker/topic`, `s3://bucket/path`) |
| `expected_throughput_mbps` | `float` | Target velocity for adaptive rate limiting |
| `format_hint` | `DataFormat` | Optional hint (JSON, Parquet, Protobuf, CSV) to bypass inference |
| `delivery_guarantee` | `GuaranteeLevel` | `AT_LEAST_ONCE`, `EXACTLY_ONCE`, `BEST_EFFORT` |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `transaction_id` | `UUID` | Idempotent token for downstream deduplication |
| `inferred_schema` | `SchemaDef` | Detected structural schema of the payload |
| `data_refs` | `List[DataPointer]` | Memory/storage pointers to the persisted raw data |

### State Schema
- `active_connections`: Ephemeral state of open sockets/channels.
- `watermarks`: High-water marks for offset tracking in continuous streams.
- `backpressure_tokens`: Current token bucket allocations per source.

## Dependencies

### Upstream (depends on)
- `H11-AUTH`: For fetching IAM credentials to access S3/GCS or secured Kafka clusters.

### Downstream (feeds into)
- `H11-CLEANSER`: Feeds raw data blocks for immediate deduplication and anomaly detection.
- `H11-METASTORE`: Registers the inferred schema and data lineage.

## Failure Modes
1. **Schema Drift Avalanche**: Source schema changes rapidly, causing thrashing in the type automaton.
2. **Backpressure Deadlock**: Circular dependency in stream processing stalling all token replenishment.
3. **Poison Pill Messages**: Unparseable binary blobs that crash the fast-path parser (requires fallback to slow-path robust parsing).

## Performance Characteristics
- **Throughput**: Sustains up to 4.5 GB/s per node on NVMe-backed instances.
- **Latency**: P99 < 12ms for acknowledgment in exactly-once mode (dominated by fsync to WAL).

## Research References
- "The Log: What every software engineer should know about real-time data's unifying abstraction" by Jay Kreps.
- "Adaptive Backpressure Routing for Yield Optimization" (Georgiadis et al.).
- "Reservoir-based Random Sampling with Replacement from Data Stream" (Park et al.).

## Implementation Notes
Use `asyncio` streams heavily. For Protobuf parsing, compile C-extensions rather than pure Python. The Token Bucket should update at millisecond granularity.
