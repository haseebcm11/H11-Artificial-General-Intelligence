> **Layer 2** · Data Plane & Ingestion · `H11-ETL-DATA`

## Purpose

The H11-ETL-DATA agent is the backbone of batch data integration and historical data ingestion. While H11-STREAMING-DATA handles real-time nerve impulses, H11-ETL-DATA is responsible for massive overnight memory consolidations—Extracting from diverse source systems, Transforming schemas and formats, and Loading (ETL) into data warehouses or feature stores.

It manages Directed Acyclic Graphs (DAGs) of tasks, ensuring topological execution, idempotent retries, and strict data lineage. This is critical for preparing foundational datasets used in large-scale model pre-training and analytics.

## Technical Deep-Dive

H11-ETL-DATA implements DAG-based orchestration similar to Apache Airflow or Dagster. Tasks are nodes, and data dependencies are directed edges. A core principle enforced by this agent is **Idempotency**: executing a DAG multiple times for the same logical time window yields the exact same final state, preventing data duplication on retries.

Transformation logic involves schema mapping (translating source schemas into the canonical H11 unified schema), type casting, null handling, and join operations.

The agent also implements CDC (Change Data Capture) patterns for incremental loading. Instead of moving terabytes of data nightly, it reads WAL (Write-Ahead Logs) or binlogs from source databases to identify Inserts, Updates, and Deletes (I/U/D), applying them in sequence to the destination (SCD Type 1 or Type 2 tracking).

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| dag_id | String | Identifier for the ETL pipeline |
| execution_date | Timestamp | Logical date for the run |
| payload | Dict | Configuration or raw payload for extraction |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| status | Enum | SUCCESS, FAILED, RETRYING |
| records_processed | Integer | Number of rows moved |
| downstream_uri | String | Location of the loaded data |

### State Schema
Maintains `DagRunState` (status of currently executing DAGs), `TaskInstances` (status of individual nodes), and `CDCWatermark` (last processed offset per table).

## Dependencies

### Upstream (depends on)
External relational databases, API endpoints, flat file stores (S3/GCS).

### Downstream (feeds into)
H11-FEATURE-STORE, H11-PRIVACY-DATA.

## Failure Modes
1. **Topological Deadlock**: A cycle in the DAG dependencies preventing execution.
2. **Schema Drift**: Source system adds or removes columns, breaking rigid transform steps.
3. **Idempotency Violation**: A non-idempotent task fails midway, and on retry, duplicates records in the data warehouse.

## Performance Characteristics
Highly I/O bound. Transformations are executed in-memory or pushed down to target compute engines (ELT pattern using SQL). Scales by dispatching tasks to parallel worker nodes via message queues.

## Research References
- DeWitt, D., et al. (1992). "Parallel Database Systems: The Future of High Performance Database Systems."
- Armbrust, M., et al. (2015). "Spark SQL: Relational Data Processing in Spark."

## Implementation Notes
Implement a topological sort (Kahn's algorithm) before execution. Use connection pooling for database sources. Store state metadata in an ACID-compliant backend database to guarantee reliable state transitions and locking.
