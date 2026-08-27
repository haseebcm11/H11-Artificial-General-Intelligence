> **Layer 10** · Memory Architecture · `H11-RETRIEVAL`

## Purpose
H11-RETRIEVAL orchestrates complex querying against the episodic and semantic memory stores. It provides state-of-the-art Retrieval-Augmented Generation (RAG) capabilities via hybrid search (dense embeddings + sparse BM25) and multi-hop reasoning networks, transforming vague prompts into precise context payloads.

## Technical Deep-Dive
The core of H11-RETRIEVAL is a bi-encoder/cross-encoder pipeline. Stage 1 involves a high-recall, low-precision hybrid retrieval combining HNSW for dense vectors (representing semantic similarity) and an inverted index for sparse vectors (representing lexical match). Alpha-blending normalizes these scores.
Stage 2 utilizes a smaller cross-encoder model to re-rank the top-K candidates. For multi-hop queries, the agent employs Entity-Linked Traversal, recursively querying nearest neighbors of entities identified in the first hop.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `query` | `str` | The natural language query. |
| `alpha` | `float` | Blending factor for Hybrid Search (0 = sparse, 1 = dense). |
| `multi_hop` | `bool` | Enable iterative traversal. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `chunks` | `List[ChunkMetadata]` | Re-ranked chunks. |
| `confidence` | `float` | Aggregate relevance score. |

### State Schema
Maintains transient caching for hot queries and indexing structures (mocked or interfaced to external vector DBs).

## Dependencies
### Upstream
- `H11-SEMANTIC`: Core knowledge graph.
- `H11-EMBEDDING`: Provides vector representations for queries.
### Downstream
- `H11-SYNTHESIS`: Consumes the retrieved context for generation.

## Failure Modes
- **Lost in the Middle**: Providing too many chunks reduces downstream LLM attention on middle segments.
- **Lexical Drift**: Over-reliance on dense vectors leads to hallucinated similarities.
- **Traversal Loops**: Multi-hop reasoning caught in cyclic entity references.

## Performance Characteristics
- Latency: <200ms for single hop, up to 1500ms for multi-hop re-ranking.
- Throughput: High parallel querying capability.

## Research References
- Karpukhin et al. (2020). Dense Passage Retrieval for Open-Domain QA.
- Gao et al. (2023). Retrieval-Augmented Generation for Large Language Models: A Survey.
