> **Layer 2** · Data Plane & Ingestion · `H11-CORPUS`

## Purpose

The H11-CORPUS agent acts as the foundational data lake manager for the cognitive substrate. It handles the lifecycle of massive, raw text collections—such as Common Crawl dumps, Wikipedia dumps, GitHub repositories, and scientific paper archives. Its primary role is to ingest raw formats (WARC, JSONL, Parquet), extract clean text, perform exact and fuzzy deduplication, and compute deep corpus statistics.

This agent transforms petabytes of unstructured noise into a structured, queryable, and highly optimized corpus, laying the groundwork for downstream curation and training.

## Technical Deep-Dive

Text extraction from formats like Common Crawl (WARC) requires robust HTML parsing, boilerplate removal, and heuristic filtering (e.g., stopping short documents, filtering out lists or heavily templated pages). H11-CORPUS employs algorithms similar to trafilatura or jusText for high-yield content extraction.

Deduplication is a critical challenge at scale. H11-CORPUS performs a multi-stage deduplication:
1. **Exact Deduplication**: Using SHA-256 hashes of normalized documents.
2. **Fuzzy Deduplication**: Utilizing MinHash and Locality-Sensitive Hashing (LSH). The agent computes MinHash signatures over document n-grams and groups them into LSH bands. Documents falling into the same bucket are compared using Jaccard similarity, and connected components are formed. Only one document per connected component is retained.

The agent also tracks detailed corpus statistics: token length distributions, language identification (using FastText or CLD3), perplexity filtering (using a small, fast n-gram model to filter out gibberish), and PII (Personally Identifiable Information) masking.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `raw_sources` | `List[str]` | URIs to raw WARC/JSONL files. |
| `extraction_config` | `ExtractionRule` | Rules for boilerplate removal and language filtering. |
| `dedup_threshold` | `float` | Jaccard similarity threshold for fuzzy deduplication. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `parsed_corpus_uri` | `str` | URI to the deduplicated, clean Parquet dataset. |
| `corpus_stats` | `CorpusStats` | Token counts, language distribution, and quality metrics. |

### State Schema
- `lsh_index`: Persistent index of MinHash signatures for rolling deduplication.
- `processed_warc_records`: Checkpointing state for resumption of interrupted parses.
- `global_token_counts`: Running aggregate of token volume per domain.

## Dependencies

### Upstream (depends on)
- None (Direct interface to external blob storage).

### Downstream (feeds into)
- `H11-CURATOR`: Provides the pristine pools from which the curator selects.
- `H11-PROVENANCE`: Sends document ingestion events for lineage tracking.

## Failure Modes
- **LSH Hash Collision Overload**: Too many documents hashed into a single LSH bucket, causing O(N^2) comparison blowup.
- **Parser OOM**: Malformed HTML causing catastrophic backtracking in regex or massive DOM tree memory usage.
- **Over-deduplication**: Accidentally removing semantically distinct documents due to a low Jaccard threshold or poor hash function.

## Performance Characteristics
- **Compute**: Extremely high CPU usage for MinHash computation and text extraction.
- **Storage**: Requires massive temporary scratch space (NVMe) for MapReduce-style LSH bucket shuffling.
- **Throughput**: ~100GB/hour/core for extraction; deduplication requires large distributed joins.

## Research References
- Lee et al., "Deduplicating Training Data Makes Language Models Better"
- Wenzek et al., "CCNet: Extracting High Quality Monolingual Datasets from Web Crawl Data"
- Broder, "On the resemblance and containment of documents" (MinHash)

## Implementation Notes
Implement MinHash using optimized bitwise operations or FarmHash. Store the intermediate signatures in partitioned Parquet files and use PySpark or Ray for the global LSH bucket join to scale beyond single-node memory.
