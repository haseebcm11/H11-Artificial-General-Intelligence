> **Layer 2** · Data Plane & Ingestion · `H11-SHARDER`

## Purpose

The H11-SHARDER agent is responsible for translating a monolithic, curated dataset into an optimized, distributed layout for parallel training. In large-scale LLM training, data must be streamed to hundreds or thousands of GPUs without bottlenecking. H11-SHARDER partitions the data into perfectly balanced shards, ensuring uniform token counts, maintaining curriculum distributions per shard, and mitigating hot spots.

It bridges the gap between Layer 2 (Data Plane) and Layer 4 (Training Loop) by providing deterministic routing tables and partition plans.

## Technical Deep-Dive

H11-SHARDER employs Consistent Hashing and capacity-aware bin packing. When a dataset version is ready, the agent segments it into micro-batches. To prevent straggler nodes during synchronous training (where one GPU waits for another to finish a batch), the agent guarantees that every shard contains the exact same number of tokens, padding dynamically if necessary.

The agent implements directory partitioning and range-based partitioning. It generates a `ShardManifest` that assigns specific byte-offsets of data files to specific global worker ranks. Furthermore, it implements Partition Pruning metadata: if a training run resumes from step $N$, the data loader can instantly prune all shards associated with steps $0$ to $N-1$ without scanning them.

For multi-modal datasets, it performs interleaved sharding, ensuring that text and image modalities are co-located or deterministically routed to avoid excessive cross-network shuffling during data loading.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `dataset_manifest` | `DatasetManifest` | List of curated files and their sizes/token counts. |
| `cluster_topology` | `TopologySpec` | Number of workers, data-parallel degree, node count. |
| `global_batch_size` | `int` | Total tokens per step across the cluster. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `shard_layout` | `List[ShardDef]` | Mapping of data chunks to physical shard files. |
| `routing_table` | `RoutingTable` | Map of Data Parallel Rank -> Shard URI. |

### State Schema
- `hash_ring`: Current consistent hash ring configuration.
- `active_layouts`: Cached partition plans for active training runs.

## Dependencies

### Upstream (depends on)
- `H11-VERSION`: Provides the exact, immutable snapshot to partition.
- `H11-CURATOR`: Dataset composition guarantees must be maintained per shard.

### Downstream (feeds into)
- `H11-DATALOADER` (Layer 4): Consumes the routing table to stream bytes to GPUs.

## Failure Modes
- **Straggler Imbalance**: If shards have varying sequence lengths, certain GPUs will finish forward passes faster, causing global barrier stalls.
- **Hot Spotting**: All workers trying to read from the same underlying storage node due to poor shard placement.
- **OOM during Bin Packing**: Trying to optimize shard placement globally on a massive dataset can exhaust RAM.

## Performance Characteristics
- **Compute**: Low compute, primarily mathematical packing algorithms.
- **Storage**: May physically rewrite data into `tfrecords` or `webdataset` shards, requiring high I/O throughput.
- **Latency**: Shard planning takes seconds; physical resharding takes hours.

## Research References
- Karger et al., "Consistent Hashing and Random Trees"
- WebDataset: High-performance scalable data access for Deep Learning
- PyTorch Distributed Data Parallel (DDP) data loading constraints.

## Implementation Notes
Use the `webdataset` format conventions (tar files containing .txt/.json/.img). Implement a greedy bin-packing algorithm with a max-heap to perfectly balance token counts across shards.
