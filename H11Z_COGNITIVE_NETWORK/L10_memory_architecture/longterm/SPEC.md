> **Layer 10** · Memory Architecture · `H11-LONGTERM`

## Purpose
The H11-LONGTERM agent serves as the unbounded, persistent repository for the cognitive substrate. It captures highly consolidated memories and structural knowledge that have survived short-term decay. It employs a high-dimensional vector space coupled with hierarchical indexing to support both precision recall and fuzzy associative retrieval across vast epochs of operational time.

## Technical Deep-Dive
Unlike H11-WORKING or H11-SHORTTERM, H11-LONGTERM models the distinct psychological phases of Encoding, Storage, and Retrieval. 
- **Encoding**: Utilizes a contrastive learning objective to project complex symbolic payloads into a dense embedding space, ensuring semantically similar traces are clustered.
- **Storage**: Implements an HNSW (Hierarchical Navigable Small World) graph to index millions of vectors efficiently. The storage engine incorporates a consolidation daemon that slowly reshapes the graph, optimizing edges based on co-occurrence frequencies over time (simulating systems-level consolidation during 'sleep' or idle cycles).
- **Retrieval**: Uses a hybrid search model. It combines Approximate Nearest Neighbor (ANN) search on embeddings with BM25 keyword filtering to prevent associative hallucinations.

The system features "graceful degradation" where extreme temporal distances cause loss of high-frequency detail (flattening of sub-graph structures), leaving generalized schemas behind.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `consolidated_traces` | `List[Trace]` | High-strength items promoted from H11-SHORTTERM. |
| `retrieval_cue` | `Vector` | High-dimensional dense representation of a query. |
| `operation` | `OperationEnum` | ENCODE, RETRIEVE, CONSOLIDATE. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `retrieved_nodes` | `List[Node]` | Closest matching memories in LTM. |
| `confidence_scores` | `List[float]` | Cosine similarity or BM25 scores. |
| `index_health` | `float` | Metric of HNSW graph balance. |

### State Schema
The state is massive, consisting of a partitioned HNSW graph, a persistent inverted index, and a consolidation queue tracking items pending deep structural integration.

## Dependencies
### Upstream (depends on)
- `H11-SHORTTERM`: Source of raw traces.
- `H11-SEMANTIC`: Provides grounding for semantic expansion of queries.
### Downstream (feeds into)
- `H11-REASONING`: Supplies historical precedents.

## Failure Modes
- **Semantic Drift**: Embeddings shifting over long time periods, causing old memories to become irretrievable via modern queries.
- **Graph Fragmentation**: The HNSW index splintering into disconnected components, hiding islands of memory.
- **Overfitting to Recency**: If sleep/consolidation phases are skipped, the storage biases heavily toward recent items, behaving like a bloated short-term memory.

## Performance Characteristics
Optimized for high throughput batch encoding, but single-item retrieval latency can be higher (50-200ms) due to disk I/O and graph traversal. Requires significant storage/memory profiling (Memory Class: Massive).

## Research References
- Malkov, Y. A., & Yashunin, D. A. (2018). Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs.
- McClelland, J. L., McNaughton, B. L., & O'Reilly, R. C. (1995). Why there are complementary learning systems in the hippocampus and neocortex.
- Tulving, E. (1972). Episodic and semantic memory.

## Implementation Notes
Focus heavily on the `HNSW` simulation and the interface for the consolidation daemon. Ensure encoding is non-blocking.
