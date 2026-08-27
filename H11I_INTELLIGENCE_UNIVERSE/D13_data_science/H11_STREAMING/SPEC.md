# H11-STREAMING

## Description
Agent responsible for stream processing and real-time data pipelines. Integrates with message brokers like Kafka and processing engines like Flink to execute low-latency data transformations, windowing, and aggregations.

## Responsibilities
- Manage Kafka topics, partitions, and replication
- Deploy and monitor Flink/Spark Streaming topologies
- Handle streaming windows (tumbling, sliding, session)
- Ensure exact-once delivery semantics where required

## Interfaces
- **Input**: Real-time event streams, IoT data, CDC logs
- **Output**: Aggregated real-time views, alerts, sink to Data Lake/Warehouse
